from src.entity.models import Mark
from src.entity.repositories.mark_repository import MarkRepository

from typing import Union

class UpdateMarkCurrentUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository
        
    def execute(self, mark_name: str, current: Union[int, float]) -> Mark:
        mark = self._repository.get_by_name(mark_name)
        if (mark.get_current() - current) < 0:
            raise ValueError("Current's result cannot be negative")
        mark.set_current(current)
        return mark
        