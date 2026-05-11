from sqlalchemy.orm import Session
from app.domain.entities import Pet, User, Adoption
from app.domain.interfaces import PetRepositoryInterface, UserRepositoryInterface, AdoptionRepositoryInterface, ShelterRepositoryInterface
from app.infrastructure.db import PetDB, UserDB, AdoptionDB

class PetRepository(PetRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, pet_id: int) -> Pet | None:
        db_pet = self.session.query(PetDB).filter(PetDB.id == pet_id).first()
        if db_pet:
            return Pet.model_validate(db_pet)
        return None

    def list_all(self) -> list[Pet]:
        db_pets = self.session.query(PetDB).all()
        return [Pet.model_validate(p) for p in db_pets]

    def save(self, pet: Pet) -> Pet:
        if pet.id is None:
            # Create
            db_pet = PetDB(**pet.model_dump(exclude={'id'}))
            self.session.add(db_pet)
        else:
            # Update
            db_pet = self.session.query(PetDB).filter(PetDB.id == pet.id).first()
            for key, value in pet.model_dump(exclude={'id'}).items():
                setattr(db_pet, key, value)
        self.session.commit()
        self.session.refresh(db_pet)
        return Pet.model_validate(db_pet)

from app.domain.entities import Shelter
class ShelterRepository(ShelterRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, shelter: Shelter) -> Shelter:
        from app.infrastructure.db import ShelterDB
        if shelter.id is None:
            db_obj = ShelterDB(**shelter.model_dump(exclude={'id'}))
            self.session.add(db_obj)
        else:
            db_obj = self.session.query(ShelterDB).filter(ShelterDB.id == shelter.id).first()
            for key, value in shelter.model_dump(exclude={'id'}).items():
                setattr(db_obj, key, value)
        self.session.commit()
        self.session.refresh(db_obj)
        return Shelter.model_validate(db_obj)

    def list_all(self) -> list[Shelter]:
        from app.infrastructure.db import ShelterDB
        db_objs = self.session.query(ShelterDB).all()
        return [Shelter.model_validate(o) for o in db_objs]

    def get_by_id(self, shelter_id: int) -> Shelter | None:
        from app.infrastructure.db import ShelterDB
        db_obj = self.session.query(ShelterDB).filter(ShelterDB.id == shelter_id).first()
        if db_obj:
            return Shelter.model_validate(db_obj)
        return None

    def get_by_email(self, email: str) -> Shelter | None:
        from app.infrastructure.db import ShelterDB
        db_obj = self.session.query(ShelterDB).filter(ShelterDB.email == email).first()
        if db_obj:
            return Shelter.model_validate(db_obj)
        return None

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        if user.id is None:
            db_obj = UserDB(**user.model_dump(exclude={'id'}))
            self.session.add(db_obj)
        else:
            db_obj = self.session.query(UserDB).filter(UserDB.id == user.id).first()
            # simple update
            db_obj.name = user.name
        self.session.commit()
        self.session.refresh(db_obj)
        return User.model_validate(db_obj)
        
        
    def get_by_email(self, email: str) -> User | None:
        db_obj = self.session.query(UserDB).filter(UserDB.email == email).first()
        if db_obj:
            return User.model_validate(db_obj)
        return None

    def get_by_id(self, user_id: int) -> User | None:
        db_obj = self.session.query(UserDB).filter(UserDB.id == user_id).first()
        if db_obj:
            return User.model_validate(db_obj)
        return None

class AdoptionRepository(AdoptionRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, adoption: Adoption) -> Adoption:
        if adoption.id is None:
            db_obj = AdoptionDB(**adoption.model_dump(exclude={'id'}))
            self.session.add(db_obj)
        else:
            db_obj = self.session.query(AdoptionDB).filter(AdoptionDB.id == adoption.id).first()
            db_obj.status = adoption.status
        self.session.commit()
        self.session.refresh(db_obj)
        return Adoption.model_validate(db_obj)

    def get_by_id(self, adoption_id: int) -> Adoption | None:
        db_obj = self.session.query(AdoptionDB).filter(AdoptionDB.id == adoption_id).first()
        if db_obj:
            return Adoption.model_validate(db_obj)
        return None

    def list_all(self, pet_id: int | None = None) -> list[Adoption]:
        query = self.session.query(AdoptionDB)
        if pet_id is not None:
            query = query.filter(AdoptionDB.pet_id == pet_id)
        db_adopts = query.all()
        return [Adoption.model_validate(a) for a in db_adopts]
