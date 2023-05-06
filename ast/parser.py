from node import Number, BinaryOperation, UnaryOperation, Function, Variable, Matrix, Parenthesis
from token import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = None
    
    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self):
        if self.position < len(self.tokens):
            self.position += 1

    def expect(self, token_type):
        token = self.peek()
        if token is None or token.type != token_type:
            raise ValueError(f"Expected token of type {token_type}, but got {token.type if token else None}")
        self.consume()

    def parse_expression(self):
        left = self.parse_term()

        while self.peek() and self.peek().type == TokenType.OPERATOR and self.peek().value in "+-":
            operator_token = self.peek()
            self.consume()
            right = self.parse_term()
            left = BinaryOperation(left, operator_token.value, right)
        return left

    def parse_term(self):
        left = self.parse_factor()

        while self.peek() and self.peek().type == TokenType.OPERATOR and self.peek().value in "*/":
            operator_token = self.peek()
            self.consume()
            right = self.parse_factor()
            left = BinaryOperation(left, operator_token.value, right)
        return left

    def parse_factor(self):
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of input")

        if token.type == TokenType.NUMBER:
            self.consume()
            return Number(token.value)

        if token.type == TokenType.VARIABLE:
            self.consume()
            return Variable(token.value)

        if token.type == TokenType.PAREN_LEFT:
            self.consume()
            expression = self.parse_expression()
            self.expect(TokenType.PAREN_RIGHT)
            return expression

        raise ValueError(f"Unexpected token at position {self.pos}: {token.type}")

