from src.entity.models import Card, Mark
from src.entity.repositories.mark_repository import MarkRepository

from typing import Union

class UpdateCardUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository
        
    def execute(self, mark_name: str, card_name: str, card_value: Union[int, float]) -> Mark:
        mark = self._repository.get_by_name(mark_name)
        mark.update_card(card)
        return mark
