import pytest
from unittest.mock import AsyncMock

from usecases.delete_mark import DeleteMarkUseCase
from entity.models import Mark
from config.errors import MarkNotFoundError


class TestDeleteMarkUseCase:
    async def test_delete_mark(self):
        """Test deleting an existing mark"""
        mock_repo = AsyncMock()
        mark = Mark("Test Mark", 100)
        mock_repo.get_by_name.return_value = mark

        use_case = DeleteMarkUseCase(mock_repo)
        await use_case.execute("Test Mark")

        mock_repo.delete.assert_called_once_with(mark)

    async def test_delete_mark_error(self):
        """Test that deleting nonexistent mark raises MarkNotFoundError"""
        mock_repo = AsyncMock()
        mock_repo.get_by_name.return_value = None

        use_case = DeleteMarkUseCase(mock_repo)

        with pytest.raises(MarkNotFoundError):
            await use_case.execute("Nonexistent Mark")
