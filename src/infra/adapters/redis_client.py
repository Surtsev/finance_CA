from redis.asyncio import Redis

from config.settings import settings


class RedisClient:
    def __init__(self, redis_url: str):
        self._redis_url = redis_url
        self._redis: Redis | None = None

    @property
    def redis(self) -> Redis:
        if self._redis is None:
            raise RuntimeError("Redis client is not connected. Call connect() first.")
        return self._redis

    async def connect(self) -> None:
        self._redis = Redis.from_url(self._redis_url, decode_responses=True)

    async def disconnect(self) -> None:
        if self._redis is not None:
            await self._redis.close()
            self._redis = None

    async def set(self, key: str, value: str, expire: int = 3600) -> None:
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        """Delete all keys matching a glob-style pattern."""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)


redis_client = RedisClient(settings.REDIS_URL)
