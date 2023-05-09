from token import Token, TokenType
import re

class Lexer:
    def __init__(self, str):
        self.str = str.replace(' ', '')
        self.pos = 0

    def tokenize(self):
        tokens = []
        while self.pos < len(self.str):
            c = self.str[self.pos]

            if c in '+*-/^':
                tokens.append(Token(c, TokenType.OPERATOR, c))      
                self.pos += 1
            elif c in '()':
                tokens.append(Token(c, TokenType.PAREN_L if c == '(' else TokenType.PAREN_R, c))
                self.pos += 1
            elif c.isdigit():
                num = self.get_num_str(self.str[self.pos:])
                tokens.append(Token(c, TokenType.NUMBER, num))
                self.pos += len(num)
            elif c.isalpha():
                name, token_type = self.get_var_or_func_str(self.str[self.pos:])
                if token_type == TokenType.VARIABLE:
                    tokens.append(Token(c, TokenType.VARIABLE, name.lower()))
                elif token_type == TokenType.IMAGINARY_UNIT:
                    tokens.append(Token(c, TokenType.IMAGINARY_UNIT, name.lower()))
                else:
                    tokens.append(Token(c, TokenType.FUNCTION, name.lower()))
                self.pos += len(name)
            elif c == '[]':
                tokens.append(Token(c, TokenType.MATRIX_OPEN if c == '[' else TokenType.MATRIX_CLOSE, c))
                self.pos += 1
            elif c == ',':
                tokens.append(Token(c, TokenType.MATRIX_ELEM_DELIM, c))
                self.pos += 1
            elif c == ';':
                tokens.append(Token(c, TokenType.MATRIX_ROW_DELIM, c))
                self.pos += 1
            elif c == '?':
                tokens.append(Token(c, TokenType.SOLUTION, c))
                self.pos += 1
            elif c == '=':
                tokens.append(Token(c, TokenType.EQUAL, c))
                self.pos += 1
            else:
                raise Exception("Invalid character")
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
        token_type = TokenType.FUNCTION if i < len(str) and str[i] == '(' else TokenType.VARIABLE
        if token_type == TokenType.VARIABLE and str[:i].lower() == 'i':
            token_type = TokenType.IMAGINARY_UNIT
        elif token_type == TokenType.FUNCTION and str[:i].lower() == 'i':
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