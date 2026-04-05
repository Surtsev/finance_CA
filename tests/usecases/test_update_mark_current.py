import pytest
from unittest.mock import AsyncMock

from src.usecases.update_mark_current import UpdateMarkCurrentUseCase
from src.entity.models import Mark
from src.config.errors import MarkNotFoundError


class TestUpdateMarkCurrentUseCase:
    async def test_update_mark_current(self):
        """Test updating current value of an existing mark"""
        mock_repo = AsyncMock()
        mark = Mark("Машина", 1000)
        mock_repo.get_by_name.return_value = mark

        use_case = UpdateMarkCurrentUseCase(mock_repo)
        result = await use_case.execute("Машина", 500)

        assert result == mark
        assert mark.get_current() == 1500

    async def test_update_mark_current_negative(self):
        """Test that updating current to negative value raises ValueError"""
        mock_repo = AsyncMock()
        mark = Mark("Машина", 100)
        mock_repo.get_by_name.return_value = mark

        use_case = UpdateMarkCurrentUseCase(mock_repo)

        with pytest.raises(ValueError, match="Current's result cannot be negative"):
            await use_case.execute("Машина", -200)

    async def test_update_mark_current_error(self):
        """Test that updating nonexistent mark raises MarkNotFoundError"""
        mock_repo = AsyncMock()
        mock_repo.get_by_name.return_value = None

        use_case = UpdateMarkCurrentUseCase(mock_repo)

        with pytest.raises(MarkNotFoundError):
            await use_case.execute("Nonexistent Mark", 500)
