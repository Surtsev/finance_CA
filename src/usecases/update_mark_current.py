from src.entity.models import Mark
from src.entity.repositories.mark_repository import MarkRepository

from src.config.types import Money
from src.config.errors import MarkNotFoundError

from typing import Union

class UpdateMarkCurrentUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    async def execute(self, mark_name: str, current: Money) -> Mark:
        mark = await self._repository.get_by_name(mark_name)
        if mark is None:
            raise MarkNotFoundError(f"Mark '{mark_name}' not found")

        if (mark.get_current() + current) < 0:
            raise ValueError("Current's result cannot be negative")
        mark.set_current(current)
        return mark
        