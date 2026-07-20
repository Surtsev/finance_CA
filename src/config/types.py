from typing import TypeAlias
from enum import Enum

Money: TypeAlias = int | float

class MarkTypes(Enum):
    MARK = 0
    GOAL = 1
