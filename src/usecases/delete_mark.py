from entity.models import Mark
from entity.repositories.mark_repository import MarkRepository

from config.errors import MarkNotFoundError

class DeleteMarkUseCase:
    def __init__(self, repository: MarkRepository):
        self._repository = repository

    async def execute(self, mark_name: str) -> None:
        mark = await self._repository.get_by_name(mark_name)
        if mark is None:
            raise MarkNotFoundError(f"Mark '{mark_name}' not found")
        await self._repository.delete(mark)