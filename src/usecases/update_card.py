from src.entity.models import Card, Mark
from src.entity.repositories.mark_repository import MarkRepository
from src.config.types import Money
from src.config.errors import MarkNotFoundError

class UpdateCardUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository
        
    def execute(self, mark_name: str, card_name: str, card_value: Money) -> Mark:
        mark = self._repository.get_by_name(mark_name)
        if mark is None:
            raise MarkNotFoundError(f"Mark '{mark_name}' not found")
        
        card = Card(card_name, card_value)
        mark.update_card(card)
        return mark

