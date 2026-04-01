from src.config.types import Money, MarkTypes

from . import Card




class Mark:
    """
    A frequently used entity by the user is a financial goal,
    indicating the current/required amount of money,
    with the ability to specify which bank accounts and which amounts are part of this goal.
    """

    _name: str
    _type: MarkTypes
    _current: Money
    _required: int
    _cards: list[Card]

    def __init__(
        self,
        name: str,
        current: Money,
        cards: list[Card] = [],
        required: int = 0,
    ):
        self._name = name
        self._current = current
        self._cards = cards
        self._required = required
        self._type = MarkTypes.GOAL if self._required > 0 else MarkTypes.MARK

    def is_goal(self):
        return self._type == MarkTypes.GOAL

    def get_name(self) -> str:
        return self._name

    def get_current(self) -> Money:
        return self._current

    def get_required(self) -> int:
        return self._required

    def get_cards(self) -> list[Card]:
        return self._cards
        
    def get_card(self, card_name: str) -> Card:
        for card in self._cards:
            if card.get_name() == card_name:
                return card
        raise ValueError(f"Card '{card_name}' not found")

    def set_current(self, value: Money):
        self._current += value

    def add_card(self, card: Card):
        self._cards.append(card)

    def update_card(self, card: Card):
        for i, c in enumerate(self._cards):
            if c.get_name() == card.get_name():
                self._cards[i].set_value(card.get_value())
                return
        raise ValueError(f"Card '{card.get_name()}' not found")

    def delete_card(self, card: Card):
        self._cards = [c for c in self._cards if c.get_name() != card.get_name()]
