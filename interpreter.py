from parser import AST_TYPE
from parser import Number, BinaryOperator, UnaryOperator, FunctionNode, VariableNode, MatrixNode, Equation, MatrixRow
from type import Complex, Rational, Matrix, Polynomial, Function
from fractions import Fraction

class Interpreter:
    def __init__(self, root, ast_type):
        self.root = root
        self.ast_type = ast_type

    def run(self):
        return self.visit(self.root)

    def visit(self, node):
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, UnaryOperator):
            return self.visit_unary_operator(node)
        elif isinstance(node, BinaryOperator):
            return self.visit_binary_operator(node)
        elif isinstance(node, VariableNode):
            return self.visit_variable(node)
        elif isinstance(node, FunctionNode):
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

        print('type: ', type(left), type(right))

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
            if isinstance(right, Matrix) or isinstance(right, Function) or isinstance(right, Polynomial):
                raise TypeError("Cannot exponentiate a matrix, a function or a variable")
            return left ** right
        elif node.op == '%':
            if isinstance(right, (Rational, Complex)) and right == 0:
                raise ZeroDivisionError("Modulo by zero")
            return left % right
        elif node.op == '**':
            if not isinstance(left, Matrix) or not isinstance(right, Matrix):
                raise TypeError("Both operands should be matrices for vector multiplication")
            return left ** right
        else:
            raise ValueError(f"Unknown operator: {node.op}")            

    def visit_imaginary(self, node):
        return Complex(0, 1)

    def visit_variable(self, node):
        return Polynomial([0, 1], node.name)

    def visit_function(self, node):
        arg = self.visit(node.arg)
        return Function(node.name, arg)

    def visit_matrix(self, node):
        rows = []
        for row in node.rows:
            rows.append([self.visit(element) for element in row])
        return Matrix(rows)

    def visit_equation(self, node):
        if self.ast_type == AST_TYPE.ASSIGN and not isinstance(node.left, VariableNode) and not isinstance(node.left, FunctionNode): # TODO function declaration
            raise ValueError("The left side of the equation must declare a variable or function when it is an assignment")
        left = self.visit(node.left)
        right = self.visit(node.right) if self.ast_type != AST_TYPE.COMPUTE_VAL else None
        return left, right
