from computor import computor
from parser import AST_TYPE
from parser import Number, BinaryOperator, UnaryOperator, FunctionNode, VariableNode, MatrixNode, Equation, MatrixRow
from type import Complex, Rational, Matrix, Polynomial, Function
from fractions import Fraction
from decimal import Decimal

class Interpreter:
    def __init__(self, root, ast_type):
        self.root = root
        self.ast_type = ast_type

    def run(self):
        return self.visit(self.root)

    def visit(self, node, on_left=None):
        # print(f"Visiting {type(node)}, left: {on_left}")
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, UnaryOperator):
            return self.visit_unary_operator(node, on_left)
        elif isinstance(node, BinaryOperator):
            return self.visit_binary_operator(node, on_left)
        elif isinstance(node, VariableNode):
            return self.visit_variable(node, on_left)
        elif isinstance(node, FunctionNode):
            return self.visit_function(node, on_left)
        elif isinstance(node, MatrixNode):
            return self.visit_matrix(node, on_left)
        elif isinstance(node, Equation):
            return self.visit_equation(node)
        else:
            raise ValueError(f"Unexpected node type: {type(node)}")

    def visit_number(self, node):
        if node.is_real is True:
            decimal_value = Decimal(str(node.value))
            fraction = Fraction(decimal_value)
            return Rational(fraction.numerator, fraction.denominator)
        return Complex(0, node.value)

    def visit_unary_operator(self, node, on_left=None):
        operand = self.visit(node.operand, on_left)
        return -operand if node.op == "-" else operand

    def visit_binary_operator(self, node, on_left=None):
        left = self.visit(node.left, on_left)
        right = self.visit(node.right, on_left)

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

    def visit_variable(self, node, on_left=None):
        if node.name in computor.vars and (self.ast_type != AST_TYPE.ASSIGN or on_left is False):
            return computor.vars[node.name]
        return Polynomial([0, 1], node.name)

    def visit_function(self, node, on_left=None):
        arg = self.visit(node.arg, on_left)
        if node.name in computor.funcs and (self.ast_type != AST_TYPE.ASSIGN or on_left is False):
            return computor.funcs[node.name](arg)
        if self.ast_type == AST_TYPE.ASSIGN:
            if not isinstance(arg, Polynomial):
                raise ValueError("The left side of the equation must declare a variable when it is an assignment")
            if node.name == arg.variable:
                raise ValueError("Function name and variable name cannot be the same")
            if node.arg.name in computor.vars:
                raise ValueError("The variable name is already used")
        return Function(node.name, arg)

    def visit_matrix(self, node, on_left=None):
        rows = []
        for row in node.rows:
            rows.append([self.visit(element, on_left) for element in row.elems])
        return Matrix(rows)
    
    def visit_equation(self, node):
        if self.ast_type == AST_TYPE.ASSIGN and not isinstance(node.left, VariableNode) and not isinstance(node.left, FunctionNode): # TODO function declaration
            raise ValueError("The left side of the equation must declare a variable or function when it is an assignment")
        left = self.visit(node.left, True)
        right = self.visit(node.right, False) if self.ast_type != AST_TYPE.COMPUTE_VAL else None
        return left, right
