from entity.models import Mark, Card
from entity.repositories.mark_repository import MarkRepository
from config.errors import MarkNotFoundError, CardAlreadyExistsError

class AddCardToMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    async def execute(self, mark_name: str, card: Card) -> Mark:
        mark = await self._repository.get_by_name(mark_name)
        if mark is None:
            raise MarkNotFoundError(f"Mark '{mark_name}' not found")
        if card in mark.get_cards():
            raise CardAlreadyExistsError(f"Card '{card.get_name()}' still exists!")
        mark.add_card(card)
        await self._repository.update(mark)
        return mark
