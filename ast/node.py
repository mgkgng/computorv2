class Node:
    pass

class Expression(Node):
    pass

class BinaryOperation(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOperation(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Function(Expression):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Variable(Expression):
    def __init__(self, name):
        self.name = name

class Number(Expression):
    def __init__(self, value):
        self.value = value

class Parenthesis(Expression):
    def __init__(self, exp):
        self.exp = exp

class Matrix(Expression):
    def __init__(self, rows):
        self.rows = rows