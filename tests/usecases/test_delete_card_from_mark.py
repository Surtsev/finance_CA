import pytest
from unittest.mock import AsyncMock

from usecases.delete_card_from_mark import DeleteCardFromMarkUseCase
from entity.models import Mark, Card
from config.errors import MarkNotFoundError

class TestDeleteCardFromMarkUseCase:
    async def test_delete_card_from_mark(self):
        """Test deleting a card from mark successfully"""
        mock_repo = AsyncMock()
        card = Card("ВТБ", 730)
        mark = Mark("Машина", card.get_value(), cards=[card])
        mock_repo.get_by_name.return_value = mark

        use_case = DeleteCardFromMarkUseCase(mock_repo)
        result = await use_case.execute("Машина", card)
        assert result == mark
        assert card not in mark.get_cards()
        mock_repo.update.assert_called_once_with(mark)

    async def test_delete_card_from_mark_error(self):
        """Test deleting a card and raises custom error"""
        mock_repo = AsyncMock()
        mock_repo.get_by_name.return_value = None

        use_case = DeleteCardFromMarkUseCase(mock_repo)
        card = Card("ВТБ", 730)

        with pytest.raises(MarkNotFoundError):
            await use_case.execute("Машина", card)
