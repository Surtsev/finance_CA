from entity.models import Mark
from entity.repositories.mark_repository import MarkRepository
from infra.adapters.redis_cache import CacheService
from infra.adapters.sqlalchemy_mark_repository import SQLAlchemyMarkRepository
from infra.cache_keys import CacheKeys


class CachedMarkGateway(MarkRepository):
    """MarkRepository with Redis cache-aside pattern.

    Decorates SQLAlchemyMarkRepository to add caching on read operations
    and cache invalidation on write operations.
    """

    def __init__(
        self,
        repository: SQLAlchemyMarkRepository,
        cache: CacheService,
    ):
        self._repository = repository
        self._cache = cache

    async def add(self, mark: Mark) -> None:
        await self._repository.add(mark)
        await self._cache.invalidate_pattern(CacheKeys.mark_pattern())

    async def update(self, mark: Mark) -> None:
        await self._repository.update(mark)
        await self._cache.invalidate_pattern(CacheKeys.mark_pattern())

    async def delete(self, mark: Mark) -> None:
        await self._repository.delete(mark)
        await self._cache.invalidate_pattern(CacheKeys.mark_pattern())

    async def get_by_name(self, name: str) -> Mark | None:
        key = CacheKeys.mark(name)

        # 1. Check cache
        cached = await self._cache.get(key)
        if cached is not None:
            return self._reconstruct_mark(cached)

        # 2. Cache miss — go to database
        mark = await self._repository.get_by_name(name)
        if mark is not None:
            await self._cache.set(key, self._serialize_mark(mark))

        return mark

    async def get_all(self) -> list[Mark]:
        key = CacheKeys.marks_all()

        # 1. Check cache
        cached = await self._cache.get(key)
        if cached is not None:
            return [self._reconstruct_mark(item) for item in cached]

        # 2. Cache miss — go to database
        marks = await self._repository.get_all()
        await self._cache.set(
            key,
            [self._serialize_mark(m) for m in marks],
        )

        return marks

    @staticmethod
    def _serialize_mark(mark: Mark) -> dict:
        return {
            "name": mark.get_name(),
            "current": mark.get_current(),
            "required": mark.get_required(),
            "cards": [
                {"name": c.get_name(), "value": c.get_value()}
                for c in mark.get_cards()
            ],
        }

    @staticmethod
    def _reconstruct_mark(data: dict) -> Mark:
        from entity.models import Card

        cards = [Card(name=c["name"], value=c["value"]) for c in data["cards"]]
        return Mark(
            name=data["name"],
            current=data["current"],
            required=data["required"],
            cards=cards,
        )
