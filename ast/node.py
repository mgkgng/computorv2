class Node:
    pass

class Equation(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Expression(Node):
    pass

class BinaryOperator(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOperator(Expression):
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
        if len(rows) == 0:
            raise Exception("Empty matrix")
        elem_count = len(rows[0].elem)
        for row in rows:
            if len(row.elem) != elem_count:
                raise Exception("Invalid matrix")
        self.rows = rows
        self.shape = (len(rows), elem_count)

class MatrixRow(Expression):
    def __init__(self, elems):
        if len(elems) == 0:
            raise Exception("Empty matrix row")
        self.elems = elems