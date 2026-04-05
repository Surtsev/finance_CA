import pytest
from unittest.mock import AsyncMock

from src.usecases.update_card import UpdateCardUseCase
from src.entity.models import Mark, Card
from src.config.errors import MarkNotFoundError


class TestUpdateCardUseCase:
    async def test_update_card(self):
        """Test updating a card in an existing mark"""
        mock_repo = AsyncMock()
        card = Card("ВТБ", 500)
        mark = Mark("Машина", 1000, cards=[card])
        mock_repo.get_by_name.return_value = mark

        use_case = UpdateCardUseCase(mock_repo)
        result = await use_case.execute("Машина", "ВТБ", 200)

        assert result == mark
        assert card.get_value() == 700

    async def test_update_card_error(self):
        """Test that updating card in nonexistent mark raises MarkNotFoundError"""
        mock_repo = AsyncMock()
        mock_repo.get_by_name.return_value = None

        use_case = UpdateCardUseCase(mock_repo)

        with pytest.raises(MarkNotFoundError):
            await use_case.execute("Nonexistent Mark", "ВТБ", 200)
