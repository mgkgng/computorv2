import re
from fractions import Fraction


def check(str):
    variable_pattern = re.compile(r'^[a-zA-Z]+$')
    function_pattern = re.compile(r'\b[a-zA-Z]+\([a-zA-Z]+\)')

    if variable_pattern.match(str):
        return "Variable"
    elif function_pattern.match(str):
        return "Function"
    else:
        return "Invalid"

def is_valid_num(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


# Test cases
test_cases = [
    "toto",
    "tata",
    "x",
    "y",
    "varA",
    "varB",
    "cos(x)",
    "funcA(y)",
    "toto(B)",
    "titi(D)",
    "whataboutthis(blaba)"
]

print(Fraction(0.2142312).denominator)