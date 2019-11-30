from enum import Enum, auto

class Field(Enum):
    EMPTY = 0
    X = 1
    O = -1

    def __neg__(self):
        return Field(-self.value)

    def to_char(self):
        return {self.EMPTY: ' ', self.X: 'x', self.O: 'o'}[self]


class Mode(Enum):
    HUMAN = auto()
    RANDOM = auto()
    HEURISTIC = auto()
    Q = auto()
