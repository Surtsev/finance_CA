from src.entity.models import Mark, Card
from src.entity.repositories.mark_repository import MarkRepository
from src.usecases.update_card import UpdateCardUseCase
from src.usecases.update_mark_current import UpdateMarkCurrentUseCase

from typing import Union

class UpdateMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    def execute(self, mark_name: str, current: Union[int, float] = 0, card: Union[Card, None] = None) -> Mark:
        mark = self._repository.get_by_name(mark_name)
        if current:
            current_use_case = UpdateMarkCurrentUseCase(self._repository)
            mark = current_use_case.execute(mark_name, current)
        if card:
            card_use_case = UpdateCardUseCase(self._repository)
            mark = card_use_case.execute(mark_name, card.get_name(), card.get_value())
        self._repository.save(mark)
        return mark
        


        