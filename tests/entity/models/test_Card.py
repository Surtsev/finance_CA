import pytest

from src.entity.models import Card


def test_card_create():
    card = Card(bid=1, name="ВТБ", value=13420)
    assert card._id == 1
    assert card._name == "ВТБ"
    assert card._value == 13420


def test_id_getter():
    card = Card(bid=2, name="ВТБ", value=100)
    assert card.get_id() == 2


def test_name_getter():
    card = Card(bid=2, name="ВТБ", value=100)
    assert card.get_name() == "ВТБ"


def test_value_getter():
    card = Card(bid=2, name="ВТБ", value=100)
    assert card.get_value() == 100


def test_positive_value_setter():
    card = Card(bid=2, name="ВТБ", value=100)
    card.set_value(20)
    assert card.get_value() == 120


def test_negative_value_setter():
    card = Card(bid=2, name="ВТБ", value=100)
    card.set_value(-75)
    assert card.get_value() == 25
