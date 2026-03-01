from enum import Enum

from . import Card


class Types(Enum):
    MARK = 0
    GOAL = 1


class Mark:
    """
    A frequently used entity by the user is a financial goal,
    indicating the current/required amount of money,
    with the ability to specify which bank accounts and which amounts are part of this goal.
    """

    _id: int
    _name: str
    _type: Types
    _current: int
    _required: int
    _cards: list[Card]

    def __init__(
        self,
        mid: int,
        name: str,
        current: int,
        cards: list[Card] = [],
        required: int = 0,
    ):
        self._id = mid
        self._name = name
        self._current = current
        self._cards = cards
        self._required = required
        self._type = Types.GOAL if self._required > 0 else Types.MARK

    def is_goal(self):
        return self._type

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_current(self) -> int:
        return self._current

    def get_required(self) -> int:
        return self._required

    def get_cards(self) -> list[Card]:
        return self._cards

    def set_current(self, value):
        self._current += value

    def add_card(self, card: Card):
        self._cards.append(card)

    def delete_card(self, card: Card):
        self._cards = [c for c in self._cards if c.get_name() != card.get_name()]
