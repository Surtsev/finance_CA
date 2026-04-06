import pytest
from unittest.mock import AsyncMock

from usecases.add_card_to_mark import AddCardToMarkUseCase
from entity.models import Mark, Card
from config.errors import MarkNotFoundError, CardNotFoundError


class TestAddCardToMarkUseCase:
    async def test_add_card_to_mark(self):
        """Test adding a card to an existing mark"""
        mock_repo = AsyncMock()
        mark = Mark("Test Mark", 100)
        mock_repo.get_by_name.return_value = mark

        use_case = AddCardToMarkUseCase(mock_repo)
        card = Card("Test Card", 50)

        result = await use_case.execute("Test Mark", card)

        assert card in result.get_cards()
        mock_repo.update.assert_called_once_with(mark)

    async def test_add_card_to_mark_error(self):
        """Test that adding card to nonexistent mark raises MarkNotFoundError"""
        mock_repo = AsyncMock()
        mock_repo.get_by_name.return_value = None

        use_case = AddCardToMarkUseCase(mock_repo)
        card = Card("Test Card", 50)

        with pytest.raises(MarkNotFoundError):
            await use_case.execute("Nonexistent Mark", card)
