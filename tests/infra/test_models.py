import pytest
from sqlalchemy import inspect

from src.infra.models import Base, Mark as MarkModel, Card as CardModel
from src.config.types import MarkTypes


class TestMarkModel:
    def test_table_name(self):
        assert MarkModel.__tablename__ == "marks"

    def test_columns(self):
        columns = {c.name: c for c in MarkModel.__table__.columns}
        assert "name" in columns
        assert "type" in columns
        assert "current" in columns
        assert "required" in columns

    def test_name_is_primary_key(self):
        pk = MarkModel.__table__.primary_key.columns.keys()
        assert "name" in pk

    def test_cards_relationship(self):
        assert hasattr(MarkModel, "cards")

    def test_create_mark_model(self):
        mark = MarkModel(name="Test Mark", current=100, required=200)
        assert mark.name == "Test Mark"
        assert mark.current == 100
        assert mark.required == 200
        assert mark.cards == []


class TestCardModel:
    def test_table_name(self):
        assert CardModel.__tablename__ == "cards"

    def test_columns(self):
        columns = {c.name: c for c in CardModel.__table__.columns}
        assert "id" in columns
        assert "name" in columns
        assert "value" in columns
        assert "mark_name" in columns

    def test_id_is_primary_key(self):
        pk = CardModel.__table__.primary_key.columns.keys()
        assert "id" in pk

    def test_id_is_autoincrement(self):
        col = CardModel.__table__.columns["id"]
        assert col.autoincrement is True

    def test_mark_name_is_foreign_key(self):
        fks = list(CardModel.__table__.columns["mark_name"].foreign_keys)
        assert len(fks) == 1
        assert "marks.name" in str(fks[0].target_fullname)

    def test_mark_relationship(self):
        assert hasattr(CardModel, "mark")

    def test_create_card_model(self):
        card = CardModel(name="Card1", value=50, mark_name="Test Mark")
        assert card.name == "Card1"
        assert card.value == 50
        assert card.mark_name == "Test Mark"


class TestBase:
    def test_base_is_declarative(self):
        assert hasattr(Base, "metadata")

    def test_registered_models(self):
        tables = Base.metadata.tables.keys()
        assert "marks" in tables
        assert "cards" in tables
