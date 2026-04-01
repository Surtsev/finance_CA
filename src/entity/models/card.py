from src.config.types import Money

class Card:
    """
    The entity of a bank card that will store the amount value for a Goal.
    """

    _name: str
    _value: Money = 0

    def __init__(self, name: str, value: Money = 0):
        self._name = name
        self._value = value


    def get_name(self) -> str:
        return self._name

    def get_value(self) -> Money:
        return self._value

    def set_value(self, value):
        self._value += value
