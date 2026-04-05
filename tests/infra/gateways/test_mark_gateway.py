import pytest
from unittest.mock import AsyncMock

from src.infra.gateways.mark_gateway import CachedMarkGateway
from src.infra.adapters.redis_cache import CacheService
from src.infra.adapters.sqlalchemy_mark_repository import SQLAlchemyMarkRepository
from src.entity.models import Mark, Card


@pytest.fixture
def mock_repository():
    return AsyncMock(spec=SQLAlchemyMarkRepository)


@pytest.fixture
def mock_cache():
    return AsyncMock(spec=CacheService)


@pytest.fixture
def gateway(mock_repository, mock_cache):
    return CachedMarkGateway(mock_repository, mock_cache)


class TestCachedMarkGateway:
    @pytest.mark.asyncio
    async def test_add_delegates_to_repository_and_invalidates_cache(
        self, gateway, mock_repository, mock_cache
    ):
        mark = Mark("Test Mark", 100)

        await gateway.add(mark)

        mock_repository.add.assert_called_once_with(mark)
        mock_cache.invalidate_pattern.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_delegates_to_repository_and_invalidates_cache(
        self, gateway, mock_repository, mock_cache
    ):
        mark = Mark("Test Mark", 100)

        await gateway.update(mark)

        mock_repository.update.assert_called_once_with(mark)
        mock_cache.invalidate_pattern.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_delegates_to_repository_and_invalidates_cache(
        self, gateway, mock_repository, mock_cache
    ):
        mark = Mark("Test Mark", 100)

        await gateway.delete(mark)

        mock_repository.delete.assert_called_once_with(mark)
        mock_cache.invalidate_pattern.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_name_cache_hit(self, gateway, mock_repository, mock_cache):
        cached_data = {
            "name": "Test Mark",
            "current": 100,
            "required": 200,
            "cards": [{"name": "Card1", "value": 50}],
        }
        mock_cache.get.return_value = cached_data

        result = await gateway.get_by_name("Test Mark")

        assert isinstance(result, Mark)
        assert result.get_name() == "Test Mark"
        assert result.get_current() == 100
        mock_repository.get_by_name.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_name_cache_miss(self, gateway, mock_repository, mock_cache):
        mock_cache.get.return_value = None
        mark = Mark("Test Mark", 100, required=200)
        mock_repository.get_by_name.return_value = mark

        result = await gateway.get_by_name("Test Mark")

        assert isinstance(result, Mark)
        mock_repository.get_by_name.assert_called_once_with("Test Mark")
        mock_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_name_cache_miss_mark_not_found(
        self, gateway, mock_repository, mock_cache
    ):
        mock_cache.get.return_value = None
        mock_repository.get_by_name.return_value = None

        result = await gateway.get_by_name("Nonexistent")

        assert result is None
        mock_cache.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_cache_hit(self, gateway, mock_repository, mock_cache):
        cached_data = [
            {
                "name": "Mark1",
                "current": 100,
                "required": 200,
                "cards": [],
            },
            {
                "name": "Mark2",
                "current": 50,
                "required": 100,
                "cards": [{"name": "Card1", "value": 25}],
            },
        ]
        mock_cache.get.return_value = cached_data

        result = await gateway.get_all()

        assert len(result) == 2
        assert all(isinstance(m, Mark) for m in result)
        mock_repository.get_all.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_cache_miss(self, gateway, mock_repository, mock_cache):
        mock_cache.get.return_value = None
        marks = [
            Mark("Mark1", 100, required=200),
            Mark("Mark2", 50, required=100),
        ]
        mock_repository.get_all.return_value = marks

        result = await gateway.get_all()

        assert len(result) == 2
        mock_repository.get_all.assert_called_once()
        mock_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_serialize_mark(self, gateway):
        card = Card("Card1", 50)
        mark = Mark("Test Mark", 100, required=200, cards=[card])

        serialized = gateway._serialize_mark(mark)

        assert serialized["name"] == "Test Mark"
        assert serialized["current"] == 100
        assert serialized["required"] == 200
        assert len(serialized["cards"]) == 1
        assert serialized["cards"][0]["name"] == "Card1"
        assert serialized["cards"][0]["value"] == 50

    @pytest.mark.asyncio
    async def test_reconstruct_mark(self, gateway):
        data = {
            "name": "Test Mark",
            "current": 100,
            "required": 200,
            "cards": [{"name": "Card1", "value": 50}],
        }

        result = gateway._reconstruct_mark(data)

        assert isinstance(result, Mark)
        assert result.get_name() == "Test Mark"
        assert result.get_current() == 100
        assert result.get_required() == 200
        assert len(result.get_cards()) == 1
        assert result.get_cards()[0].get_name() == "Card1"
        assert result.get_cards()[0].get_value() == 50

    @pytest.mark.asyncio
    async def test_reconstruct_mark_without_cards(self, gateway):
        data = {
            "name": "Test Mark",
            "current": 100,
            "required": 200,
            "cards": [],
        }

        result = gateway._reconstruct_mark(data)

        assert isinstance(result, Mark)
        assert len(result.get_cards()) == 0
