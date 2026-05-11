from app.domain.entities import Pet, PetStatus

class PetCreationUseCase:
    """A simple Factory/UseCase for creating valid pets"""
    @staticmethod
    def execute(name: str, species: str, age: int, shelter_id: int) -> Pet:
        # Business logic goes here (mock logic)
        return Pet(
            name=name,
            species=species,
            age=age,
            shelter_id=shelter_id,
            status=PetStatus.AVAILABLE
        )

class PetRecommendationUseCase:
    """A simple Strategy/UseCase for recommending pets"""
    @staticmethod
    def execute(pets: list[Pet]) -> list[Pet]:
        # Return top 2 matching pets (mock logic)
        return pets[:2]
