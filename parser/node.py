class Node:
    pass

class Equation(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self, level=0):
        ret = "\t"*level + "Equation:\n"
        ret += "left:" + self.left.__str__(level + 1)
        ret += "right:" + self.right.__str__(level + 1) if self.right else ""
        return ret


class Expression(Node):
    pass

class BinaryOperator(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __str__(self, level=0):
        ret = "\t"*level + f"BinaryOperator: {self.op}\n"
        ret += "left:" + self.left.__str__(level + 1)
        ret += "right:" + self.right.__str__(level + 1)
        return ret

class UnaryOperator(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    
    def __str__(self, level=0):
        ret = "\t"*level + f"UnaryOperator: {self.op}\n"
        ret += self.operand.__str__(level + 1)
        return ret


class FunctionNode(Expression):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def __str__(self, level=0):
        ret = "\t"*level + f"FunctionNode: {self.name}\n"
        for arg in self.args:
            ret += arg.__str__(level + 1)
        return ret


class VariableNode(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self, level=0):
        return "\t"*level + f"VariableNode: {self.name}\n"

class Number(Expression):
    def __init__(self, value, is_real=True):
        self.value = value
        self.is_real = is_real

    def __str__(self, level=0):
        return "\t"*level + f"Number: {self.value}\n"


class MatrixNode(Expression):
    def __init__(self, rows):
        if len(rows) == 0:
            raise Exception("Empty matrix")
        elem_count = len(rows[0].elem)
        for row in rows:
            if len(row.elem) != elem_count:
                raise Exception("Invalid matrix")
        self.rows = rows
        self.shape = (len(rows), elem_count)
    
    def __str__(self, level=0):
        ret = "\t"*level + f"MatrixNode: shape {self.shape}\n"
        for row in self.rows:
            ret += row.__str__(level + 1)
        return ret

class MatrixRow(Expression):
    def __init__(self, elems):
        if len(elems) == 0:
            raise Exception("Empty matrix row")
        self.elems = elems
    
    def __str__(self, level=0):
        ret = "\t"*level + "MatrixRow:\n"
        for elem in self.elems:
            ret += elem.__str__(level + 1)
        return ret