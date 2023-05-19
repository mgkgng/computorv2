from .token import TokenType
from .ast import ASTWrapper, AST_TYPE
from .node import Equation, BinaryOperator, Number, VariableNode, MatrixNode, FunctionNode, UnaryOperator, MatrixRow, Factorial

class Parser:
    def run(self, tokens):
        self.validate_lexer_tokens(tokens)
        if tokens[-1].type == TokenType.SOLUTION:
            self.ast_type = AST_TYPE.COMPUTE_VAL if tokens[-2].type == TokenType.EQUAL else AST_TYPE.COMPUTE_SOL
            self.tokens = tokens[:-1]
        else:
            self.ast_type = AST_TYPE.ASSIGN
            self.tokens = tokens
        self.pos = 0
        self.ast = None
        return self.parse()

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        if self.pos < len(self.tokens):
            self.pos += 1

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

    def parse(self):
        equation = self.parse_equation()
        self.ast = ASTWrapper(equation, self.ast_type)
        return self.ast

    def parse_equation(self):
        left = self.parse_expression()
        self.expect(TokenType.EQUAL)
        right = self.parse_expression() if self.ast_type != AST_TYPE.COMPUTE_VAL else None
        return Equation(left, right)

    def parse_expression(self):
        left = self.parse_term()
        while self.peek() is not None and self.peek().type == TokenType.OPERATOR and self.peek().value in "+-":
            print('expression: ', self.peek())
            operator_token = self.peek()
            self.consume()
            print('expression: ', self.peek())
            right = self.parse_term()
            left = BinaryOperator(left, operator_token.value, right)
        return left

    def parse_term(self):
        left_factor = self.parse_exponent()

        while self.peek() is not None and self.peek().type == TokenType.OPERATOR and self.peek().value in ['*', '/', '^', '%', '**']:
            print("term: ", self.peek())
            op = self.peek_and_consume()
            right_factor = self.parse_exponent()
            left_factor = BinaryOperator(left_factor, op.value, right_factor)
        return left_factor

    def parse_exponent(self):
        base = self.parse_factor()
        if self.peek() is not None and self.peek().type == TokenType.OPERATOR and self.peek().value == '^':
            print("exponent: ", self.peek())
            self.consume()
            self.rejects([TokenType.OPERATOR, TokenType.FUNCTION, TokenType.MATRIX_OPEN])
            exponent = self.parse_factor()
            return BinaryOperator(base, '^', exponent)
        return base

    def parse_factor(self):
        token = self.peek()
        print("factor: ", token)

        if token.type == TokenType.OPERATOR and token.value in '+-':
            self.consume()
            next_token = self.peek()
            if next_token is None or next_token.type in [TokenType.OPERATOR, TokenType.FUNCTION]:
                raise ValueError(f"Expected token not of type {token.type}, but got {token.type if token else None}")
            factor = self.parse_factor()
            return UnaryOperator(token.value, factor)

        elif token.type == TokenType.NUMBER:
            self.consume()
            if self.peek() is not None and self.peek().type == TokenType.IMAGINARY_UNIT:
                self.consume()
                return Number(float(token.value), False)
            if self.peek() is not None and self.peek().type == TokenType.FACTORIAL:
                self.consume()
                return Factorial(float(token.value))
            return Number(float(token.value))

        elif token.type == TokenType.VARIABLE:
            self.consume()
            res = VariableNode(token.value)
            if self.peek() is not None and self.peek().type == TokenType.FACTORIAL:
                self.consume()
                return Factorial(res)
            return res

        elif token.type == TokenType.PAREN_L:
            self.consume()
            expression = self.parse_expression()
            self.expect(TokenType.PAREN_R)
            if self.peek() is not None and self.peek().type == TokenType.FACTORIAL:
                self.consume()
                return Factorial(expression)
            return expression

        elif token.type == TokenType.FUNCTION:
            self.consume()
            self.expect(TokenType.PAREN_L)
            expression = self.parse_expression()
            self.expect(TokenType.PAREN_R)
            return FunctionNode(token.value, expression)
        
        elif token.type == TokenType.MATRIX_OPEN:
            self.consume()

            vec = []
            vec.append(self.parse_expression())

            delim = None
            if self.peek() is not None and self.peek().type == TokenType.MATRIX_ELEM_DELIM:
                delim = TokenType.MATRIX_ELEM_DELIM
            elif self.peek() is not None and self.peek().type == TokenType.MATRIX_ROW_DELIM:
                delim = TokenType.MATRIX_ROW_DELIM

            while self.peek() is not None and delim and self.peek().type == delim:
                self.consume()
                vec.append(self.parse_expression())

            self.expect(TokenType.MATRIX_CLOSE)

            if delim == TokenType.MATRIX_ELEM_DELIM:
                return MatrixRow(vec)
            return MatrixNode(vec)
        
        elif token.type == TokenType.IMAGINARY_UNIT:
            self.consume()
            return Number(1, False)

        else:
            raise ValueError(f"Unexpected token: {token}")


    def validate_lexer_tokens(self, tokens):
        equal_tokens = [i for i, token in enumerate(tokens) if token.type == TokenType.EQUAL]
        solution_tokens = [i for i, token in enumerate(tokens) if token.type == TokenType.SOLUTION]

        if len(equal_tokens) != 1 or len(solution_tokens) > 1:
            raise ValueError("Invalid number of equal or solution tokens")
        if equal_tokens[0] == 0 or equal_tokens[0] == len(tokens) - 1 \
            or (len(solution_tokens) and solution_tokens[0] != len(tokens) - 1):
            raise ValueError("Invalid position of equal or solution tokens")
