from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Pet, User, Adoption

class PetRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, pet_id: int) -> Optional[Pet]: pass

    @abstractmethod
    def list_all(self) -> List[Pet]: pass

    @abstractmethod
    def save(self, pet: Pet) -> Pet: pass

class ShelterRepositoryInterface(ABC):
    @abstractmethod
    def save(self, shelter) -> 'Shelter': pass

    @abstractmethod
    def list_all(self) -> List['Shelter']: pass

    @abstractmethod
    def get_by_id(self, shelter_id: int) -> Optional['Shelter']: pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional['Shelter']: pass

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user: User) -> User: pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: pass

class AdoptionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, adoption: Adoption) -> Adoption: pass
    
    @abstractmethod
    def get_by_id(self, adoption_id: int) -> Optional[Adoption]: pass

    @abstractmethod
    def list_all(self, pet_id: Optional[int] = None) -> List[Adoption]: pass
