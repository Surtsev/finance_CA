import pytest
from unittest.mock import AsyncMock

from usecases.update_mark import UpdateMarkUseCase
from entity.models import Mark, Card
from config.errors import MarkNotFoundError


class TestUpdateMarkUseCase:
    async def test_update_mark_current_only(self):
        """Test updating only current value of an existing mark"""
        mock_repo = AsyncMock()
        mark = Mark("Машина", 1000)
        mock_repo.get_by_name.return_value = mark

        use_case = UpdateMarkUseCase(mock_repo)
        result = await use_case.execute("Машина", current=500)

        assert result == mark
        assert mark.get_current() == 1500
        mock_repo.update.assert_called_once_with(mark)

    async def test_update_mark_card_only(self):
        """Test updating only card value of an existing mark"""
        mock_repo = AsyncMock()
        card = Card("ВТБ", 500)
        mark = Mark("Машина", 1000, cards=[card])
        mock_repo.get_by_name.return_value = mark

        use_case = UpdateMarkUseCase(mock_repo)
        result = await use_case.execute("Машина", card=Card("ВТБ", 200))

        assert result == mark
        assert card.get_value() == 700
        mock_repo.update.assert_called_once_with(mark)

    async def test_update_mark_current_and_card(self):
        """Test updating both current value and card of an existing mark"""
        mock_repo = AsyncMock()
        card = Card("ВТБ", 500)
        mark = Mark("Машина", 1000, cards=[card])
        mock_repo.get_by_name.return_value = mark

        use_case = UpdateMarkUseCase(mock_repo)
        result = await use_case.execute("Машина", current=300, card=Card("ВТБ", 200))

        assert result == mark
        assert mark.get_current() == 1300
        assert card.get_value() == 700
        mock_repo.update.assert_called_once_with(mark)

    async def test_update_mark_error(self):
        """Test that updating nonexistent mark raises MarkNotFoundError"""
        mock_repo = AsyncMock()
        mock_repo.get_by_name.return_value = None

        use_case = UpdateMarkUseCase(mock_repo)

        with pytest.raises(MarkNotFoundError):
            await use_case.execute("Nonexistent Mark", current=500)
