import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.infra.adapters.redis_client import RedisClient


@pytest.fixture
def redis_client():
    client = RedisClient("redis://localhost:6379")
    return client


class TestRedisClient:
    def test_redis_property_raises_when_not_connected(self, redis_client):
        with pytest.raises(RuntimeError, match="Redis client is not connected"):
            _ = redis_client.redis

    @pytest.mark.asyncio
    async def test_connect_creates_redis_instance(self, redis_client):
        with patch("src.infra.adapters.redis_client.Redis") as mock_redis:
            mock_instance = AsyncMock()
            mock_redis.from_url.return_value = mock_instance

            await redis_client.connect()

            mock_redis.from_url.assert_called_once_with(
                "redis://localhost:6379", decode_responses=True
            )
            assert redis_client.redis is mock_instance

    @pytest.mark.asyncio
    async def test_disconnect_closes_and_clears_redis(self, redis_client):
        with patch("src.infra.adapters.redis_client.Redis") as mock_redis:
            mock_instance = AsyncMock()
            mock_redis.from_url.return_value = mock_instance

            await redis_client.connect()
            await redis_client.disconnect()

            mock_instance.close.assert_called_once()
            assert redis_client._redis is None

    @pytest.mark.asyncio
    async def test_disconnect_when_not_connected_does_nothing(self, redis_client):
        await redis_client.disconnect()
        assert redis_client._redis is None

    @pytest.mark.asyncio
    async def test_set(self, redis_client):
        with patch("src.infra.adapters.redis_client.Redis") as mock_redis:
            mock_instance = AsyncMock()
            mock_redis.from_url.return_value = mock_instance
            await redis_client.connect()

            await redis_client.set("key", "value", expire=60)

            mock_instance.set.assert_called_once_with("key", "value", ex=60)

    @pytest.mark.asyncio
    async def test_get(self, redis_client):
        with patch("src.infra.adapters.redis_client.Redis") as mock_redis:
            mock_instance = AsyncMock()
            mock_redis.from_url.return_value = mock_instance
            mock_instance.get.return_value = "value"
            await redis_client.connect()

            result = await redis_client.get("key")

            mock_instance.get.assert_called_once_with("key")
            assert result == "value"

    @pytest.mark.asyncio
    async def test_get_returns_none(self, redis_client):
        with patch("src.infra.adapters.redis_client.Redis") as mock_redis:
            mock_instance = AsyncMock()
            mock_redis.from_url.return_value = mock_instance
            mock_instance.get.return_value = None
            await redis_client.connect()

            result = await redis_client.get("nonexistent")

            assert result is None

    @pytest.mark.asyncio
    async def test_delete(self, redis_client):
        with patch("src.infra.adapters.redis_client.Redis") as mock_redis:
            mock_instance = AsyncMock()
            mock_redis.from_url.return_value = mock_instance
            await redis_client.connect()

            await redis_client.delete("key")

            mock_instance.delete.assert_called_once_with("key")

    @pytest.mark.asyncio
    async def test_delete_pattern_deletes_matching_keys(self, redis_client):
        with patch("src.infra.adapters.redis_client.Redis") as mock_redis:
            mock_instance = AsyncMock()
            mock_redis.from_url.return_value = mock_instance
            mock_instance.keys.return_value = ["mark:1", "mark:2"]
            await redis_client.connect()

            await redis_client.delete_pattern("mark:*")

            mock_instance.keys.assert_called_once_with("mark:*")
            mock_instance.delete.assert_called_once_with("mark:1", "mark:2")

    @pytest.mark.asyncio
    async def test_delete_pattern_does_nothing_when_no_keys_match(
        self, redis_client
    ):
        with patch("src.infra.adapters.redis_client.Redis") as mock_redis:
            mock_instance = AsyncMock()
            mock_redis.from_url.return_value = mock_instance
            mock_instance.keys.return_value = []
            await redis_client.connect()

            await redis_client.delete_pattern("nonexistent:*")

            mock_instance.keys.assert_called_once_with("nonexistent:*")
            mock_instance.delete.assert_not_called()
