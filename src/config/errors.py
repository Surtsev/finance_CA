class MarkNotFoundError(Exception):
    """Исключение, когда марка не найдена"""

    pass


class CardNotFoundError(Exception):
    """Исключение, когда карта не найдена"""

    pass


class MarkAlreadyExistsError(Exception):
    """Исключение, когда марка уже существует"""

    pass


class CardAlreadyExistsError(Exception):
    """Исключение, когда карта уже существует"""

    pass

