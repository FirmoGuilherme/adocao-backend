from app.domain.entities import Pet, User, Adoption, Shelter
from app.domain.interfaces import PetRepositoryInterface, UserRepositoryInterface, AdoptionRepositoryInterface, ShelterRepositoryInterface
from app.application.use_cases import PetCreationUseCase, PetRecommendationUseCase

class ShelterService:
    def __init__(self, repo: ShelterRepositoryInterface):
        self.repo = repo

    def register(self, name: str, location: str, contact_phone: str, email: str, password: str) -> Shelter:
        from app.core.utils import hash_password
        pwd_hash = hash_password(password)
        shelter = Shelter(name=name, location=location, contact_phone=contact_phone, email=email, password=pwd_hash)
        return self.repo.save(shelter)

    def authenticate(self, email: str, password: str) -> Shelter | None:
        from app.core.utils import verify_password
        shelter = self.repo.get_by_email(email)
        if not shelter:
            return None
        if not verify_password(password, shelter.password):
            return None
        return shelter

    def list_shelters(self) -> list[Shelter]:
        return self.repo.list_all()

class PetService:
    def __init__(self, repo: PetRepositoryInterface):
        self.repo = repo

    def create_pet(self, name: str, species: str, age: int, shelter_id: int) -> Pet:
        pet = PetCreationUseCase.execute(name, species, age, shelter_id)
        return self.repo.save(pet)

    def get_pet_by_id(self, pet_id: int) -> Pet | None:
        return self.repo.get_by_id(pet_id)

    def change_status(self, pet_id: int, new_status: str) -> Pet:
        from app.domain.entities import PetStatus
        pet = self.repo.get_by_id(pet_id)
        if not pet:
            raise ValueError("Pet not found")
        pet.status = PetStatus(new_status)
        return self.repo.save(pet)

    def list_pets(self) -> list[Pet]:
        return self.repo.list_all()
        
    def recommend_pets(self) -> list[Pet]:
        all_pets = self.repo.list_all()
        return PetRecommendationUseCase.execute(all_pets)

class UserService:
    def __init__(self, repo: UserRepositoryInterface):
        self.repo = repo

    def register(self, email: str, name: str, password: str) -> User:
        from app.core.utils import hash_password
        user = User(email=email, name=name, password=hash_password(password))
        return self.repo.save(user)
        
    def authenticate(self, email: str, password: str) -> User | None:
        from app.core.utils import verify_password
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return user
        
    def get_by_email(self, email: str) -> User | None:
        return self.repo.get_by_email(email)

class AdoptionService:
    def __init__(self, repo: AdoptionRepositoryInterface, pet_repo: PetRepositoryInterface):
        self.repo = repo
        self.pet_repo = pet_repo

    def apply(self, pet_id: int, user_id: int, message: str) -> Adoption:
        from app.domain.entities import PetStatus
        pet = self.pet_repo.get_by_id(pet_id)
        if not pet:
            raise ValueError("Pet not found")
        if pet.status != PetStatus.AVAILABLE:
            raise ValueError("Pet is not available for adoption")
            
        pet.status = PetStatus.PENDING
        self.pet_repo.save(pet)
            
        adoption = Adoption(pet_id=pet_id, user_id=user_id, message=message)
        return self.repo.save(adoption)

    def change_adoption_status(self, adoption_id: int, new_status: str) -> Adoption:
        from app.domain.entities import PetStatus, AdoptionStatus
        adoption = self.repo.get_by_id(adoption_id)
        if not adoption:
            raise ValueError("Adoption not found")
            
        req_status = AdoptionStatus(new_status)
        adoption.status = req_status
        self.repo.save(adoption)

        if req_status == AdoptionStatus.APPROVED:
            pet = self.pet_repo.get_by_id(adoption.pet_id)
            pet.status = PetStatus.ADOPTED
            self.pet_repo.save(pet)
        elif req_status == AdoptionStatus.REJECTED:
            pet = self.pet_repo.get_by_id(adoption.pet_id)
            pet.status = PetStatus.AVAILABLE
            self.pet_repo.save(pet)

        return adoption

    def list_adoptions(self, user_repo: UserRepositoryInterface, pet_id: int | None = None) -> list[dict]:
        adoptions = self.repo.list_all(pet_id=pet_id)
        result = []
        for adp in adoptions:
            user = user_repo.get_by_id(adp.user_id)
            adp_dict = adp.model_dump()
            adp_dict["adopter_name"] = user.name if user else "Unknown"
            adp_dict["adopter_email"] = user.email if user else "Unknown"
            result.append(adp_dict)
        return result
