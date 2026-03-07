from src.entity.repositories.mark_repository import MarkRepository
from src.entity.models import Mark, Card

from typing import Union

class CreateMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository
    
    def execute(self, name: str, current: Union[int, float], cards: list[Card] = [], required: int = 0) -> Mark:
        mark = Mark(name, current, cards, required)
        self._repository.save(mark)
        return mark