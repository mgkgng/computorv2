from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    VARIABLE = auto()
    FUNCTION = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_MAT = auto()
    RIGHT_MAT = auto()
    COMMA = auto()
    pass

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value