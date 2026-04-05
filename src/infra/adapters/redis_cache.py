import json
from typing import Any

from src.infra.adapters.redis_client import RedisClient
from src.infra.cache_keys import CacheKeys


class CacheService:
    """Cache abstraction layer over Redis."""

    def __init__(self, redis_client: RedisClient):
        self._redis = redis_client

    async def get(self, key: str) -> Any | None:
        """Get value from cache. Returns deserialized object or None."""
        raw = await self._redis.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set(self, key: str, value: Any, ttl: int = CacheKeys.DEFAULT_TTL) -> None:
        """Set value in cache with TTL. Serializes to JSON."""
        await self._redis.set(key, json.dumps(value, default=str), expire=ttl)

    async def delete(self, key: str) -> None:
        """Delete a single key from cache."""
        await self._redis.delete(key)

    async def invalidate_pattern(self, pattern: str) -> None:
        """Delete all keys matching a glob-style pattern."""
        await self._redis.delete_pattern(pattern)
