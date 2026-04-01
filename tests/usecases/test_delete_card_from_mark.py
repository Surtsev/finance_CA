import pytest
from unittest.mock import Mock

from src.usecases.delete_card_from_mark import DeleteCardFromMarkUseCase
from src.entity.models import Mark, Card
from src.config.errors import MarkNotFoundError

class TestDeleteCardFromMarkUseCase:
    def test_delete_card_from_mark(self):
        """Test deleting a card from mark successfully"""
        mock_repo = Mock()
        card = Card("ВТБ", 730)
        mark = Mark("Машина", card.get_value(), cards=[card])
        mock_repo.get_by_name.return_value = mark

        use_case = DeleteCardFromMarkUseCase(mock_repo)
        result = use_case.execute("Машина", card)
        assert result == mark
        assert card not in mark.get_cards()
        mock_repo.update.assert_called_once_with(mark)

    def test_delete_card_from_mark_error(self):
        """Test deleting a card and raises custom error"""
        mock_repo = Mock()
        mock_repo.get_by_name.return_value = None

        use_case = DeleteCardFromMarkUseCase(mock_repo)
        card = Card("ВТБ", 730)

        with pytest.raises(MarkNotFoundError):
            use_case.execute("Машина", card)