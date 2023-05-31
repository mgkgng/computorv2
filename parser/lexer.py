from .token import Token, TokenType

class Lexer:
    def run(self, str):
        self.str = str.replace(' ', '')
        self.pos = 0
        return self.tokenize()

    def tokenize(self):
        tokens = []
        while self.pos < len(self.str):
            c = self.str[self.pos]

            if c in '+*-/^%':
                if len(self.str[self.pos:]) > 2 and self.str[self.pos:self.pos + 2] == '**':
                    tokens.append(Token(TokenType.OPERATOR, '**'))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.OPERATOR, c))
                    self.pos += 1
            elif c in '()':
                tokens.append(Token(TokenType.PAREN_L if c == '(' else TokenType.PAREN_R, c))
                self.pos += 1
            elif c.isdigit():
                num = self.get_num_str(self.str[self.pos:])
                tokens.append(Token(TokenType.NUMBER, num))
                self.pos += len(num)
            elif c.isalpha():
                name, token_type = self.get_var_or_func_str(self.str[self.pos:])
                if len(tokens) > 0 and tokens[-1].type == TokenType.NUMBER:
                    tokens.append(Token(TokenType.OPERATOR, '*'))
                if token_type == TokenType.VARIABLE:
                    tokens.append(Token(TokenType.VARIABLE, name.lower()))
                elif token_type == TokenType.IMAGINARY_UNIT:
                    tokens.append(Token(TokenType.IMAGINARY_UNIT, name.lower()))
                else:
                    tokens.append(Token(TokenType.FUNCTION, name.lower()))
                self.pos += len(name)
            elif c in '[]':
                tokens.append(Token(TokenType.MATRIX_OPEN if c == '[' else TokenType.MATRIX_CLOSE, c))
                self.pos += 1
            elif c == ',':
                tokens.append(Token(TokenType.MATRIX_ELEM_DELIM, c))
                self.pos += 1
            elif c == ';':
                tokens.append(Token(TokenType.MATRIX_ROW_DELIM, c))
                self.pos += 1
            elif c == '?':
                tokens.append(Token(TokenType.SOLUTION, c))
                self.pos += 1
            elif c == '=':
                tokens.append(Token(TokenType.EQUAL, c))
                self.pos += 1
            else:
                raise Exception("Invalid character", c)
        return tokens

    @staticmethod
    def get_num_str(str):
        i = 0
        while i < len(str) and (str[i].isdigit() or str[i] == '.'):
            i += 1
        return str[:i]

    @staticmethod
    def get_var_or_func_str(str):
        i = 0
        while i < len(str) and str[i].isalpha():
            i += 1

        name = str[:i].lower()
        token_type = TokenType.FUNCTION if i < len(str) and str[i] == '(' else TokenType.VARIABLE
        if token_type == TokenType.VARIABLE and name in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'log', 'ln', 'sqrt', 'abs', 'exp']:
            raise Exception(f"You cannot use '{name}' as a variable name")
        if token_type == TokenType.VARIABLE and name == 'i':
            token_type = TokenType.IMAGINARY_UNIT
        elif token_type == TokenType.FUNCTION and name == 'i':
            raise Exception("Invalid function name")
        return str[:i], token_type

    @staticmethod
    def get_mat_str(str):
        i = 0
        open = 1
        while i < len(str) and open > 0:
            open += 1 if str[i] == '[' else -1 if str[i] == ']' else 0
            i += 1
        if open > 0:
            raise Exception("Invalid matrix")
        return str[:i]        