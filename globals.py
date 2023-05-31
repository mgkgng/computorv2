from math import sin, cos, tan, log, sqrt, exp

DEBUGGING = False

built_in_funcs = {
    'sin': lambda x: sin(x),
    'cos': lambda x: cos(x),
    'tan': lambda x: tan(x),
    'cot': lambda x: 1 / tan(x),
    'sec': lambda x: 1 / cos(x),
    'csc': lambda x: 1 / sin(x),
    'ln': lambda x: log(x),
    'sqrt': lambda x: sqrt(x),
    'abs': lambda x: abs(x),
    'exp': lambda x: exp(x),
}