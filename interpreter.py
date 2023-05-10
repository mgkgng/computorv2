from ast import Number, BinaryOperator, UnaryOperator, Variable, Function, MatrixNode, Equation
from ast import AST_TYPE
from types import Complex, Rational, Matrix, Polynomial

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
        # Handle Number nodes
        pass

    def visit_unary_operator(self, node):
        # Handle UnaryOperator nodes
        pass

    def visit_binary_operator(self, node):
        # Handle BinaryOperator nodes
        pass

    def visit_function(self, node):
        # Handle Function nodes
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
