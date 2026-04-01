import pytest
from unittest.mock import Mock

from src.usecases.add_card_to_mark import AddCardToMarkUseCase
from src.entity.models import Mark, Card
from src.config.errors import MarkNotFoundError


class TestAddCardToMarkUseCase:
    def test_add_card_to_mark(self):
        """Test adding a card to an existing mark"""
        mock_repo = Mock()
        mark = Mark("Test Mark", 100)
        mock_repo.get_by_name.return_value = mark
        
        use_case = AddCardToMarkUseCase(mock_repo)
        card = Card("Test Card", 50)
        
        result = use_case.execute("Test Mark", card)
        
        assert result == mark
        assert card in mark.get_cards()
        mock_repo.update.assert_called_once_with(mark)
    
    def test_add_card_to_mark_error(self):
        """Test that adding card to nonexistent mark raises MarkNotFoundError"""
        mock_repo = Mock()
        mock_repo.get_by_name.return_value = None
        
        use_case = AddCardToMarkUseCase(mock_repo)
        card = Card("Test Card", 50)
        
        with pytest.raises(MarkNotFoundError):
            use_case.execute("Nonexistent Mark", card)
