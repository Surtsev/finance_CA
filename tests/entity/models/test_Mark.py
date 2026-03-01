import pytest

from src.entity.models import Card, Mark, Types


def test_goal_create():
    card = Card(bid=2, name="ВТБ", value=100)
    mark = Mark(mid=1, name="Машина", current=100, cards=[card], required=775000)
    assert mark.get_name() == "Машина"
    assert mark.get_current() == 100
    assert mark.get_cards() == [card]
    assert mark.get_required() == 775000
    assert mark.get_id() == 1
    assert mark.is_goal() == Types.GOAL


def test_mark_create():
    card = Card(bid=2, name="ВТБ", value=100)
    mark = Mark(mid=1, name="Машина", current=100, cards=[card])
    assert mark.get_name() == "Машина"
    assert mark.get_current() == 100
    assert mark.get_cards() == [card]
    assert mark.get_id() == 1
    assert mark.is_goal() == Types.MARK


def test_current_setter():
    card = Card(bid=3, name="ВТБ", value=100)
    mark = Mark(mid=2, name="Машина", current=100, cards=[card])
    mark.set_current(270)
    assert mark.get_current() == 370


def test_add_card():
    card = Card(bid=3, name="ВТБ", value=100)
    mark = Mark(mid=2, name="Машина", current=100)
    mark.add_card(card)
    assert mark.get_cards() == [card]


def test_delete_card():
    card = Card(bid=3, name="ВТБ", value=100)
    card2 = Card(bid=4, name="Альфа", value=230)
    mark = Mark(mid=2, name="Машина", current=100, cards=[card, card2])
    mark.delete_card(card2)
    assert mark.get_cards() == [card]
