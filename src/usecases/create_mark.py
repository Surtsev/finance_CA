from src.entity.repositories.mark_repository import MarkRepository
from src.entity.models import Mark, Card

from src.config.types import Money
from src.config.errors import MarkAlreadyExistsError

class CreateMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    async def execute(self, name: str, current: Money = 0, cards: list[Card] = [], required: int = 0) -> Mark:
        mark = Mark(name, current, cards, required)
        if await self._repository.get_by_name(name) is not None:
            raise MarkAlreadyExistsError(f"Mark '{name}' already exists")
        await self._repository.add(mark)
        return mark