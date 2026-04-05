import json
import pytest
from unittest.mock import AsyncMock

from src.infra.adapters.redis_cache import CacheService
from src.infra.adapters.redis_client import RedisClient
from src.infra.cache_keys import CacheKeys


@pytest.fixture
def mock_redis_client():
    client = AsyncMock(spec=RedisClient)
    return client


@pytest.fixture
def cache_service(mock_redis_client):
    return CacheService(mock_redis_client)


class TestCacheService:
    @pytest.mark.asyncio
    async def test_get_returns_none_when_key_missing(self, cache_service, mock_redis_client):
        mock_redis_client.get.return_value = None

        result = await cache_service.get("missing_key")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_returns_deserialized_value(self, cache_service, mock_redis_client):
        mock_redis_client.get.return_value = json.dumps({"name": "test", "value": 42})

        result = await cache_service.get("test_key")

        assert result == {"name": "test", "value": 42}

    @pytest.mark.asyncio
    async def test_set_serializes_and_stores_value(self, cache_service, mock_redis_client):
        value = {"name": "test", "value": 42}

        await cache_service.set("test_key", value, ttl=600)

        mock_redis_client.set.assert_called_once_with(
            "test_key", json.dumps(value, default=str), expire=600
        )

    @pytest.mark.asyncio
    async def test_set_uses_default_ttl(self, cache_service, mock_redis_client):
        value = "simple_value"

        await cache_service.set("key", value)

        mock_redis_client.set.assert_called_once_with(
            "key", json.dumps(value, default=str), expire=CacheKeys.DEFAULT_TTL
        )

    @pytest.mark.asyncio
    async def test_set_handles_complex_objects(self, cache_service, mock_redis_client):
        from datetime import datetime
        value = {"created": datetime(2024, 1, 1)}

        await cache_service.set("obj_key", value)

        mock_redis_client.set.assert_called_once()
        call_args = mock_redis_client.set.call_args
        assert call_args[0][0] == "obj_key"
        assert call_args[1]["expire"] == CacheKeys.DEFAULT_TTL

    @pytest.mark.asyncio
    async def test_delete_removes_key(self, cache_service, mock_redis_client):
        await cache_service.delete("test_key")

        mock_redis_client.delete.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_invalidate_pattern_deletes_matching_keys(self, cache_service, mock_redis_client):
        await cache_service.invalidate_pattern("mark:*")

        mock_redis_client.delete_pattern.assert_called_once_with("mark:*")
