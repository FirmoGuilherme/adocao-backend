from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories import PetRepository, UserRepository, AdoptionRepository, ShelterRepository
from app.application.services import PetService, UserService, AdoptionService, ShelterService
from app.domain.entities import Pet, User, Adoption, Shelter
from pydantic import BaseModel

router = APIRouter()

def get_shelter_service(db: Session = Depends(get_db)):
    repo = ShelterRepository(db)
    return ShelterService(repo)

def get_pet_service(db: Session = Depends(get_db)):
    repo = PetRepository(db)
    return PetService(repo)

def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

def get_adoption_service(db: Session = Depends(get_db)):
    repo = AdoptionRepository(db)
    pet_repo = PetRepository(db)
    return AdoptionService(repo, pet_repo)

class ShelterCreateRequest(BaseModel):
    name: str
    location: str
    contact_phone: str
    email: str
    password: str

class PetCreateRequest(BaseModel):
    name: str
    species: str
    age: int
    shelter_id: int

class UserCreateRequest(BaseModel):
    email: str
    name: str
    password: str

class AdoptionCreateRequest(BaseModel):
    pet_id: int
    message: str = ""

@router.post("/shelters", response_model=Shelter)
def create_shelter(req: ShelterCreateRequest, service: ShelterService = Depends(get_shelter_service)):
    return service.register(req.name, req.location, req.contact_phone, req.email, req.password)

@router.get("/shelters", response_model=list[Shelter])
def list_shelters(service: ShelterService = Depends(get_shelter_service)):
    return service.list_shelters()

@router.post("/pets", response_model=Pet)
def create_pet(req: PetCreateRequest, service: PetService = Depends(get_pet_service)):
    return service.create_pet(req.name, req.species, req.age, req.shelter_id)

@router.get("/pets", response_model=list[Pet])
def list_pets(service: PetService = Depends(get_pet_service)):
    return service.list_pets()

@router.get("/pets/{id}", response_model=Pet)
def get_pet(id: int, service: PetService = Depends(get_pet_service)):
    pet = service.get_pet_by_id(id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

class PetStatusUpdateRequest(BaseModel):
    status: str

@router.patch("/pets/{id}/status", response_model=Pet)
def change_pet_status(id: int, req: PetStatusUpdateRequest, service: PetService = Depends(get_pet_service)):
    try:
        return service.change_status(id, req.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/users", response_model=User)
def create_user(req: UserCreateRequest, service: UserService = Depends(get_user_service)):
    return service.register(req.email, req.name, req.password)


class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/shelters/login", response_model=TokenResponse)
def login_shelter(req: LoginRequest, service: ShelterService = Depends(get_shelter_service)):
    from app.core.utils import create_access_token
    shelter = service.authenticate(req.email, req.password)
    if not shelter:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(data={"sub": str(shelter.id), "role": "shelter"})
    return {"access_token": token}

@router.post("/users/login", response_model=TokenResponse)
def login_user(req: LoginRequest, service: UserService = Depends(get_user_service)):
    from app.core.utils import create_access_token
    user = service.authenticate(req.email, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(data={"sub": str(user.id), "role": "user"})
    return {"access_token": token}

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def auth_shelter(credentials: HTTPAuthorizationCredentials = Depends(security)):
    from app.core.config import config
    try:
        payload = jwt.decode(credentials.credentials, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        if payload.get("role") != "shelter":
            raise HTTPException(status_code=403, detail="Not authorized. Shelter role required.")
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def auth_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    from app.core.config import config
    try:
        payload = jwt.decode(credentials.credentials, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        if payload.get("role") != "user":
            raise HTTPException(status_code=403, detail="Not authorized. User role required.")
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

class AdoptionStatusUpdateRequest(BaseModel):
    status: str

@router.patch("/adoptions/{id}/status", response_model=Adoption)
def change_adoption_status(id: int, req: AdoptionStatusUpdateRequest, service: AdoptionService = Depends(get_adoption_service), shelter_id: str = Depends(auth_shelter)):
    try:
        return service.change_adoption_status(id, req.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/adoptions", response_model=Adoption)
def apply_adoption(req: AdoptionCreateRequest, service: AdoptionService = Depends(get_adoption_service), user_id: str = Depends(auth_user)):
    try:
        return service.apply(req.pet_id, int(user_id), req.message)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/adoptions")
def list_adoptions(
    pet_id: int | None = None,
    service: AdoptionService = Depends(get_adoption_service),
    db: Session = Depends(get_db)
):
    from app.infrastructure.repositories import UserRepository
    user_repo = UserRepository(db)
    return service.list_adoptions(user_repo, pet_id=pet_id)
