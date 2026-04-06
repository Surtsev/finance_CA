import pytest
from unittest.mock import AsyncMock, MagicMock

from infra.adapters.sqlalchemy_mark_repository import SQLAlchemyMarkRepository
from infra.models import Mark as MarkModel, Card as CardModel
from entity.models import Mark, Card


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    session.add = MagicMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def repository(mock_session):
    return SQLAlchemyMarkRepository(mock_session)


class TestSQLAlchemyMarkRepository:
    @pytest.mark.asyncio
    async def test_add_persists_mark_with_cards(self, repository, mock_session):
        mark = Mark("Test Mark", 100, required=200)
        card = Card("Card1", 50)
        mark.add_card(card)

        await repository.add(mark)

        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_persists_mark_without_cards(self, repository, mock_session):
        mark = Mark("Test Mark", 100)

        await repository.add(mark)

        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_existing_mark(self, repository, mock_session):
        mark = Mark("Test Mark", 100, required=200)

        db_mark = MarkModel(name="Test Mark", current=50, required=200)
        db_mark.cards = []

        result_mock = MagicMock()
        result_mock.scalar_one.return_value = db_mark
        mock_session.execute.return_value = result_mock

        await repository.update(mark)

        assert db_mark.current == 100
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_syncs_cards(self, repository, mock_session):
        mark = Mark("Test Mark", 100, required=200)
        card = Card("Card1", 75)
        mark.add_card(card)

        db_mark = MarkModel(name="Test Mark", current=50, required=200)
        db_mark.cards = [CardModel(name="OldCard", value=10, mark_name="Test Mark")]

        result_mock = MagicMock()
        result_mock.scalar_one.return_value = db_mark
        mock_session.execute.return_value = result_mock

        await repository.update(mark)

        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_deletes_removed_cards(self, repository, mock_session):
        mark = Mark("Test Mark", 100, required=200)

        db_mark = MarkModel(name="Test Mark", current=50, required=200)
        old_card = CardModel(name="OldCard", value=10, mark_name="Test Mark")
        db_mark.cards = [old_card]

        result_mock = MagicMock()
        result_mock.scalar_one.return_value = db_mark
        mock_session.execute.return_value = result_mock

        await repository.update(mark)

        mock_session.delete.assert_called_once_with(old_card)

    @pytest.mark.asyncio
    async def test_delete_removes_mark(self, repository, mock_session):
        mark = Mark("Test Mark", 100)

        db_mark = MarkModel(name="Test Mark", current=100, required=200)
        db_mark.cards = []

        result_mock = MagicMock()
        result_mock.scalar_one.return_value = db_mark
        mock_session.execute.return_value = result_mock

        await repository.delete(mark)

        mock_session.delete.assert_called_once_with(db_mark)
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_name_returns_mark(self, repository, mock_session):
        db_mark = MarkModel(name="Test Mark", current=100, required=200)
        db_mark.cards = [CardModel(name="Card1", value=50, mark_name="Test Mark")]

        result_mock = MagicMock()
        result_mock.scalar_one_or_none.return_value = db_mark
        mock_session.execute.return_value = result_mock

        result = await repository.get_by_name("Test Mark")

        assert isinstance(result, Mark)
        assert result.get_name() == "Test Mark"
        assert result.get_current() == 100
        assert len(result.get_cards()) == 1

    @pytest.mark.asyncio
    async def test_get_by_name_returns_none_when_not_found(self, repository, mock_session):
        result_mock = MagicMock()
        result_mock.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = result_mock

        result = await repository.get_by_name("Nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_returns_marks(self, repository, mock_session):
        db_mark1 = MarkModel(name="Mark1", current=100, required=200)
        db_mark1.cards = []
        db_mark2 = MarkModel(name="Mark2", current=50, required=100)
        db_mark2.cards = []

        scalars_mock = MagicMock()
        scalars_mock.all.return_value = [db_mark1, db_mark2]

        result_mock = MagicMock()
        result_mock.scalars.return_value = scalars_mock
        mock_session.execute.return_value = result_mock

        result = await repository.get_all()

        assert len(result) == 2
        assert all(isinstance(m, Mark) for m in result)
        assert result[0].get_name() == "Mark1"
        assert result[1].get_name() == "Mark2"

    @pytest.mark.asyncio
    async def test_get_all_returns_empty_list(self, repository, mock_session):
        scalars_mock = MagicMock()
        scalars_mock.all.return_value = []

        result_mock = MagicMock()
        result_mock.scalars.return_value = scalars_mock
        mock_session.execute.return_value = result_mock

        result = await repository.get_all()

        assert result == []
