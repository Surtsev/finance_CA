class Card:
    """
    The entity of a bank card that will store the amount value for a Goal.
    """

    _id: int
    _name: str
    _value: int = 0

    def __init__(self, bid: int, name: str, value: int = 0):
        self._id = bid
        self._name = name
        self._value = value

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_value(self) -> int:
        return self._value

    def set_value(self, value):
        self._value += value
