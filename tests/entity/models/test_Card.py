import pytest

from src.entity.models import Card


def test_card_create():
    card = Card(name="ВТБ", value=13420)
    assert card._name == "ВТБ"
    assert card._value == 13420

def test_name_getter():
    card = Card(name="ВТБ", value=100)
    assert card.get_name() == "ВТБ"


def test_value_getter():
    card = Card(name="ВТБ", value=100)
    assert card.get_value() == 100


def test_positive_value_setter():
    card = Card(name="ВТБ", value=100)
    card.set_value(20)
    assert card.get_value() == 120


def test_negative_value_setter():
    card = Card(name="ВТБ", value=100)
    card.set_value(-75)
    assert card.get_value() == 25
