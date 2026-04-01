import pytest
from unittest.mock import Mock

from src.usecases.create_mark import CreateMarkUseCase
from src.entity.models import Mark

from src.config.errors import MarkAlreadyExistsError

class TestCreateMarkUseCase:
    def test_create_mark(self):
        """Test creating a new mark"""
        mock_repo = Mock()
        mock_repo.get_by_name.return_value = None

        use_case = CreateMarkUseCase(mock_repo)
        result = use_case.execute("На еду")

        assert isinstance(result, Mark)
        assert result.get_name() == "На еду"
        mock_repo.add.assert_called_once_with(result)

    def test_create_mark_error(self):
        """Test creating a mark that already exists and raises custom error"""
        mock_repo = Mock()
        mark = Mark("На еду", 100)
        mock_repo.get_by_name.return_value = mark

        use_case = CreateMarkUseCase(mock_repo)

        with pytest.raises(MarkAlreadyExistsError):
            use_case.execute("На еду")
