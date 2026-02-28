from enum import Enum

import models


class Types(Enum):
    MARK = 0
    GOAL = 1


class Mark:
    """
    A frequently used entity by the user is a financial goal,
    indicating the current/required amount of money,
    with the ability to specify which bank accounts and which amounts are part of this goal.
    """

    _name: str
    _type: Types
    _current: int
    _required: int
    _cards: list[models.Card]

    def __init__(
        self, name: str, current: int, cards: list[models.Card] = [], required: int = 0
    ):
        self._name = name
        self._current = current
        self._cards = cards
        self._required = required
        self._type = Types.GOAL if self._required > 0 else Types.MARK

    def is_goal(self):
        return self._type

    def get_name(self) -> str:
        return self._name

    def get_current(self) -> int:
        return self._current

    def get_required(self) -> int:
        return self._required

    def get_cards(self) -> list[models.Card]:
        return self._cards
