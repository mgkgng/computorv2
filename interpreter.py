from ast import Number, BinaryOperator, UnaryOperator, Variable, Function, MatrixNode, Equation
from ast import AST_TYPE
from types import Complex, Rational, Matrix, Polynomial
from fractions import Fraction

class Interpreter:
    def __init__(self, root, type):
        self.root = root
        self.type = type

    def visit(self, node):
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, UnaryOperator):
            return self.visit_unary_operator(node)
        elif isinstance(node, BinaryOperator):
            return self.visit_binary_operator(node)
        elif isinstance(node, Function):
            return self.visit_function(node)
        elif isinstance(node, MatrixNode):
            return self.visit_matrix(node)
        elif isinstance(node, Equation):
            return self.visit_equation(node)
        else:
            raise ValueError(f"Unexpected node type: {type(node)}")

    def visit_number(self, node):
        fraction = Fraction(node.value)
        return Rational(fraction.numerator, fraction.denominator)

    def visit_unary_operator(self, node):
        operand = self.visit(node.operand)
        return -operand if node.op == "-" else operand

    def visit_binary_operator(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if isinstance(right, (Rational, Complex)) and right == 0:
                raise ZeroDivisionError("Division by zero")
            if isinstance(right, Matrix):
                raise TypeError("Cannot divide by a matrix")
            return left / right
        elif node.op == '^':
            if isinstance(right, Matrix) or isinstance(right, Function) or isinstance(right, Variable): #TODO maybe with variable it could be ok
                raise TypeError("Cannot exponentiate a matrix, a function or a variable")
            return left ** right
        elif node.op == '%':
            if isinstance(right, (Rational, Complex)) and right == 0:
                raise ZeroDivisionError("Modulo by zero")
            return left % right
        elif node.op == '**':
            if not isinstance(left, Matrix) or not isinstance(right, Matrix):
                raise TypeError("Both operands should be matrices for vector multiplication")
            return left @ right
        else:
            raise ValueError(f"Unknown operator: {node.op}")            

    def visit_imaginary(self, node):
        return Complex(0, 1)

    def visit_function(self, node):
        pass

    def visit_matrix(self, node):
        # Handle Matrix nodes
        pass

    def visit_equation(self, node):
        left = self.visit(node.left)
        if self.ast_type == AST_TYPE.ASSIGN and not isinstance(left, Variable) and not isinstance(left, Function): # TODO function declaration
            raise ValueError("The left side of the equation must declare a variable or function when it is an assignment")
        right = self.visit(node.right)
        
        return left, right
