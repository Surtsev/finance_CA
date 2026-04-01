from src.entity.models import Mark, Card
from src.entity.repositories.mark_repository import MarkRepository
from src.usecases.update_card import UpdateCardUseCase
from src.usecases.update_mark_current import UpdateMarkCurrentUseCase
from src.config.types import Money
from src.config.errors import MarkNotFoundError

from typing import Union

class UpdateMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    def execute(self, mark_name: str, current: Money = 0, card: Union[Card, None] = None) -> Mark:
        mark = self._repository.get_by_name(mark_name)
        if mark is None:
            raise MarkNotFoundError(f"Mark '{mark_name}' not found")
        
        if current:
            update_current = UpdateMarkCurrentUseCase(self._repository)
            mark = update_current.execute(mark_name, current)
        if card:
            update_card = UpdateCardUseCase(self._repository)
            mark = update_card.execute(mark_name, card.get_name(), card.get_value())
        self._repository.update(mark)
        return mark
        


        