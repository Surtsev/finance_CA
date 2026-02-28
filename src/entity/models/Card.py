class Card:
    """
    The entity of a bank card that will store the amount value for a Goal.
    """

    def __init__(self, name: str, value: int):
        self._name = name
        self._value = value
