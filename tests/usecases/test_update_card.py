import pytest
from unittest.mock import Mock

from src.usecases.update_card import UpdateCardUseCase
from src.entity.models import Mark, Card
from src.config.errors import MarkNotFoundError


class TestUpdateCardUseCase:
    def test_update_card(self):
        """Test updating a card in an existing mark"""
        mock_repo = Mock()
        card = Card("ВТБ", 500)
        mark = Mark("Машина", 1000, cards=[card])
        mock_repo.get_by_name.return_value = mark

        use_case = UpdateCardUseCase(mock_repo)
        result = use_case.execute("Машина", "ВТБ", 200)

        assert result == mark
        assert card.get_value() == 700

    def test_update_card_error(self):
        """Test that updating card in nonexistent mark raises MarkNotFoundError"""
        mock_repo = Mock()
        mock_repo.get_by_name.return_value = None

        use_case = UpdateCardUseCase(mock_repo)

        with pytest.raises(MarkNotFoundError):
            use_case.execute("Nonexistent Mark", "ВТБ", 200)
