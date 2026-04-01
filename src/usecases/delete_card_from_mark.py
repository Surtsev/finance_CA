from src.entity.models import Mark, Card
from src.entity.repositories.mark_repository import MarkRepository

from src.config.errors import MarkNotFoundError

class DeleteCardFromMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    def execute(self, mark_name: str, card: Card) -> Mark:
        mark = self._repository.get_by_name(mark_name)
        if mark is None:
            raise MarkNotFoundError(f"Mark '{mark_name}' not found")
        mark.delete_card(card)
        self._repository.update(mark)
        return mark
