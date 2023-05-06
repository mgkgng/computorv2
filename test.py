import re

def check(str):
    variable_pattern = re.compile(r'^[a-zA-Z]+$')
    function_pattern = re.compile(r'\b[a-zA-Z]+\([a-zA-Z]+\)')

    if variable_pattern.match(str):
        return "Variable"
    elif function_pattern.match(str):
        return "Function"
    else:
        return "Invalid"

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

for test_case in test_cases:
    print(f"{test_case}: {check(test_case)}")
