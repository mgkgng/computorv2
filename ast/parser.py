from node import Number, BinaryOperation, UnaryOperation, Function, Variable, Matrix, Equation, MatrixRow
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

    def peek_and_consume(self):
        token = self.peek()
        self.consume()
        return token

    def expect(self, token_type):
        token = self.peek()
        if token is None or token.type != token_type:
            raise ValueError(f"Expected token of type {token_type}, but got {token.type if token else None}")
        self.consume()

    def reject(self, token_type):
        token = self.peek()
        if token is None or token.type == token_type:
            raise ValueError(f"Expected token not of type {token_type}, but got {token.type if token else None}") #TODO
        self.consume()

    def rejects(self, token_types):
        token = self.peek()
        if token is None or token.type in token_types:
            raise ValueError(f"Expected token not of type {token.type}, but got {token.type if token else None}") # TODO
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
        while self.peek() is not None and self.peek().type == TokenType.OPERATOR and self.peek().value in "+-":
            operator_token = self.peek()
            self.consume()
            right = self.parse_term()
            left = BinaryOperation(left, operator_token.value, right)

    def parse_term(self):
        left_factor = self.parse_exponent()

        while self.peek() is not None and self.peek().type == TokenType.OPERATOR and self.peek().value in '*/^':
            op = self.peek_and_consume()
            right_factor = self.parse_exponent()
            left_factor = BinaryOperation(left_factor, op.value, right_factor)
        return left_factor

    def parse_exponent(self):
        base = self.parse_factor()
        if self.peek() is not None and self.peek().type == TokenType.OPERATOR and self.peek().value == '^':
            self.consume()
            self.rejects([TokenType.OPERATOR, TokenType.FUNCTION, TokenType.MATRIX])
            exponent = self.parse_factor()
            return BinaryOperation(base, '^', exponent)
        return base

    def parse_factor(self):
        token = self.peek()

        if token.type == TokenType.OPERATOR and token.value in '+-':
            self.consume()
            self.reject(TokenType.OPERATOR)
            factor = self.parse_factor()
            return UnaryOperation(token.value, factor)

        elif token.type == TokenType.NUMBER:
            self.consume()
            return Number(float(token.value))

        elif token.type == TokenType.VARIABLE:
            self.consume()
            return Variable(token.value)

        elif token.type == TokenType.OPEN_PAREN:
            self.consume()
            expression = self.parse_expression()
            self.expect(TokenType.CLOSE_PAREN)
            return expression

        elif token.type == TokenType.FUNCTION:
            self.consume()
            self.expect(TokenType.OPEN_PAREN)
            expression = self.parse_expression()
            self.expect(TokenType.CLOSE_PAREN)
            return Function(token.value, expression)
        
        elif token.type == TokenType.MATRIX_OPEN:
            self.consume()

            vec = []
            vec.append(self.parse_expression())

            if self.peek() is not None and self.peek().type == TokenType.MATRIX_ELEM_DELIM:
                delim = TokenType.MATRIX_ELEM_DELIM
            elif self.peek() is not None and self.peek().type == TokenType.MATRIX_ROW_DELIM:
                delim = TokenType.MATRIX_ROW_DELIM

            while self.peek() is not None and self.peek().type == delim:
                self.consume()
                vec.append(self.parse_expression())

            self.expect(TokenType.MATRIX_CLOSE)

            if delim == TokenType.MATRIX_ELEM_DELIM:
                return MatrixRow(vec)
            return Matrix(token.value, expression)

        else:
            raise ValueError(f"Unexpected token: {token}")


    def validate_lexer_tokens(self):
        equal_tokens = [i for i, token in enumerate(self.tokens) if token.type == TokenType.EQUAL]
        solution_tokens = [i for i, token in enumerate(self.tokens) if token.type == TokenType.SOLUTION]

        if len(equal_tokens) != 1 or len(solution_tokens) > 1:
            raise ValueError("Invalid number of equal or solution tokens")
        if equal_tokens[0] == 0 or equal_tokens[0] == len(self.tokens) - 1 or (len(solution_tokens) and solution_tokens[0] != len(self.tokens) - 1):
            raise ValueError("Invalid position of equal or solution tokens")
