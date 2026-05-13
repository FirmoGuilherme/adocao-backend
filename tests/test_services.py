import unittest

from app.application.services import AdoptionService, PetService, UserService
from app.application.use_cases import PetCreationUseCase, PetRecommendationUseCase
from app.domain.entities import Adoption, AdoptionStatus, Pet, PetStatus, User
from app.core.utils import verify_password


class FakePetRepository:
    def __init__(self, pets=None):
        self.pets = {pet.id: pet for pet in pets or []}
        self.saved = []
        self.next_id = max(self.pets.keys(), default=0) + 1

    def get_by_id(self, pet_id: int):
        return self.pets.get(pet_id)

    def list_all(self):
        return list(self.pets.values())

    def save(self, pet: Pet):
        if pet.id is None:
            pet.id = self.next_id
            self.next_id += 1
        self.pets[pet.id] = pet
        self.saved.append(pet)
        return pet


class FakeUserRepository:
    def __init__(self, users=None):
        self.users = {user.email: user for user in users or []}
        self.next_id = 1

    def save(self, user: User):
        if user.id is None:
            user.id = self.next_id
            self.next_id += 1
        self.users[user.email] = user
        return user

    def get_by_email(self, email: str):
        return self.users.get(email)


class FakeAdoptionRepository:
    def __init__(self, adoptions=None):
        self.adoptions = {adoption.id: adoption for adoption in adoptions or []}
        self.next_id = max(self.adoptions.keys(), default=0) + 1

    def save(self, adoption: Adoption):
        if adoption.id is None:
            adoption.id = self.next_id
            self.next_id += 1
        self.adoptions[adoption.id] = adoption
        return adoption

    def get_by_id(self, adoption_id: int):
        return self.adoptions.get(adoption_id)

    def list_all(self, pet_id=None):
        adoptions = list(self.adoptions.values())
        if pet_id is None:
            return adoptions
        return [adoption for adoption in adoptions if adoption.pet_id == pet_id]


class PetUseCaseTests(unittest.TestCase):
    def test_pet_creation_use_case_sets_available_status(self):
        pet = PetCreationUseCase.execute("Luna", "Dog", 3, shelter_id=10)

        self.assertEqual(pet.name, "Luna")
        self.assertEqual(pet.species, "Dog")
        self.assertEqual(pet.age, 3)
        self.assertEqual(pet.shelter_id, 10)
        self.assertEqual(pet.status, PetStatus.AVAILABLE)

    def test_pet_recommendation_returns_first_two_pets(self):
        pets = [
            Pet(id=1, name="A", species="Dog", shelter_id=1),
            Pet(id=2, name="B", species="Cat", shelter_id=1),
            Pet(id=3, name="C", species="Bird", shelter_id=1),
        ]

        recommended = PetRecommendationUseCase.execute(pets)

        self.assertEqual([pet.id for pet in recommended], [1, 2])


class ServiceTests(unittest.TestCase):
    def test_pet_service_change_status_persists_new_status(self):
        repo = FakePetRepository([
            Pet(id=1, name="Nina", species="Cat", shelter_id=1),
        ])
        service = PetService(repo)

        pet = service.change_status(1, "ADOPTED")

        self.assertEqual(pet.status, PetStatus.ADOPTED)
        self.assertEqual(repo.get_by_id(1).status, PetStatus.ADOPTED)
        self.assertEqual(repo.saved[-1].id, 1)

    def test_user_service_register_hashes_password_and_authenticates(self):
        repo = FakeUserRepository()
        service = UserService(repo)

        user = service.register("ana@example.com", "Ana", "secret")

        self.assertNotEqual(user.password, "secret")
        self.assertTrue(verify_password("secret", user.password))
        self.assertEqual(service.authenticate("ana@example.com", "secret"), user)
        self.assertIsNone(service.authenticate("ana@example.com", "wrong"))

    def test_adoption_apply_marks_available_pet_pending(self):
        pet_repo = FakePetRepository([
            Pet(id=1, name="Toby", species="Dog", shelter_id=1),
        ])
        adoption_repo = FakeAdoptionRepository()
        service = AdoptionService(adoption_repo, pet_repo)

        adoption = service.apply(pet_id=1, user_id=7, message="I can adopt Toby")

        self.assertEqual(adoption.status, AdoptionStatus.PENDING)
        self.assertEqual(adoption.pet_id, 1)
        self.assertEqual(adoption.user_id, 7)
        self.assertEqual(pet_repo.get_by_id(1).status, PetStatus.PENDING)


if __name__ == "__main__":
    unittest.main()
