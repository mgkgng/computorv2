from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    VARIABLE = auto()
    FUNCTION = auto()
    IMAGINARY_UNIT = auto()
    PAREN_L = auto()
    PAREN_R = auto()
    SOLUTION = auto()
    EQUAL = auto()
    MATRIX_OPEN = auto()
    MATRIX_CLOSE = auto()
    MATRIX_ELEM_DELIM = auto()
    MATRIX_ROW_DELIM = auto()
    FACTORIAL = auto()

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    @staticmethod
    def convert_num_str(str):
        if '.' in str:
            index = str.find('.')
            if index == 0 or index == len(str) - 1 or str.count(".") > 1: 
                raise Exception("Invalid number")
            return float(str)
        return int(str)

    def __str__(self):
        return f"Token({self.type}, {self.value})"
