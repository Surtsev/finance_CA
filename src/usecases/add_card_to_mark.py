from src.entity.models import Mark, Card
from src.entity.repositories.mark_repository import MarkRepository

class AddCardToMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository
        
    def execute(self, mark_name: str, card: Card) -> Mark:
        mark = self._repository.get_by_name(mark_name)
        mark.add_card(card)
        self._repository.save(mark)
        return mark
