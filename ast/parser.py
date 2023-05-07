from node import Number, BinaryOperation, UnaryOperation, Function, Variable, Matrix, Parenthesis, Equation, Expression
from token import TokenType
from ast import AST, AST_TYPE

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = None
    
    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def consume(self):
        if self.position < len(self.tokens):
            self.position += 1

    def expect(self, token_type):
        token = self.peek()
        if token is None or token.type != token_type:
            raise ValueError(f"Expected token of type {token_type}, but got {token.type if token else None}")
        self.consume()

    def parse(self):
        self.validate_lexer_tokens()
        equation, input_type = self.parse_equation()
        self.ast = AST(equation, input_type)
        return self.ast

    def parse_equation(self):
        left, _ = self.parse_expression()
        self.expect(TokenType.EQUAL)
        right, input_type = self.parse_expression()
        return Equation(left, right), input_type

    def parse_expression(self):
        left = self.parse_term()
        pass

    def parse_term(self):
        left = self.parse_factor()
        # while self.peek() and self.peek().type == TokenType.OPERATOR and self.peek().value in "*/":
        #     operator_token = self.peek()
        #     self.consume()
        #     right = self.parse_factor()
        #     left = BinaryOperation(left, operator_token.value, right)
        # return left
        pass

    def parse_factor(self):
        # token = self.peek()
        # if token is None:
        #     raise ValueError("Unexpected end of input")

        # if token.type == TokenType.NUMBER:
        #     self.consume()
        #     return Number(token.value)

        # if token.type == TokenType.VARIABLE:
        #     self.consume()
        #     return Variable(token.value)

        # if token.type == TokenType.PAREN_L:
        #     self.consume()
        #     expression = self.parse_expression()
        #     self.expect(TokenType.PAREN_R)
        #     return expression

        # raise ValueError(f"Unexpected token at position {self.pos}: {token.type}")
        pass

    def validate_lexer_tokens(self):
        equal_tokens = [i for i, token in enumerate(self.tokens) if token.type == TokenType.EQUAL]
        solution_tokens = [i for i, token in enumerate(self.tokens) if token.type == TokenType.SOLUTION]

        if len(equal_tokens) != 1 or len(solution_tokens) > 1:
            raise ValueError("Invalid number of equal or solution tokens")
        if equal_tokens[0] == 0 or equal_tokens[0] == len(self.tokens) - 1 or (len(solution_tokens) and solution_tokens[0] != len(self.tokens) - 1):
            raise ValueError("Invalid position of equal or solution tokens")

        pass
