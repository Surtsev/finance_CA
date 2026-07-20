from entity.models import Mark, Card
from entity.repositories.mark_repository import MarkRepository
from usecases.update_card import UpdateCardUseCase
from usecases.update_mark_current import UpdateMarkCurrentUseCase
from config.types import Money
from config.errors import MarkNotFoundError

from typing import Union

class UpdateMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    async def execute(self, mark_name: str, current: Money = 0, card: Union[Card, None] = None) -> Mark:
        mark = await self._repository.get_by_name(mark_name)
        if mark is None:
            raise MarkNotFoundError(f"Mark '{mark_name}' not found")

        if current:
            update_current = UpdateMarkCurrentUseCase(self._repository)
            mark = await update_current.execute(mark_name, current)
        if card:
            update_card = UpdateCardUseCase(self._repository)
            mark = await update_card.execute(mark_name, card.get_name(), card.get_value())
        await self._repository.update(mark)
        return mark
        


        