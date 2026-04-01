from src.entity.models import Mark
from src.entity.repositories.mark_repository import MarkRepository

from src.config.errors import MarkNotFoundError

class DeleteMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    def execute(self, mark_name: str) -> None:
        mark = self._repository.get_by_name(mark_name)
        if mark is None:
            raise MarkNotFoundError(f"Mark '{mark_name}' not found")
        self._repository.delete(mark)