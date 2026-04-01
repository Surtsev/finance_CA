import pytest
from unittest.mock import Mock

from src.usecases.delete_mark import DeleteMarkUseCase
from src.entity.models import Mark
from src.config.errors import MarkNotFoundError


class TestDeleteMarkUseCase:
    def test_delete_mark(self):
        """Test deleting an existing mark"""
        mock_repo = Mock()
        mark = Mark("Test Mark", 100)
        mock_repo.get_by_name.return_value = mark

        use_case = DeleteMarkUseCase(mock_repo)
        use_case.execute("Test Mark")

        mock_repo.delete.assert_called_once_with(mark)

    def test_delete_mark_error(self):
        """Test that deleting nonexistent mark raises MarkNotFoundError"""
        mock_repo = Mock()
        mock_repo.get_by_name.return_value = None

        use_case = DeleteMarkUseCase(mock_repo)

        with pytest.raises(MarkNotFoundError):
            use_case.execute("Nonexistent Mark")
