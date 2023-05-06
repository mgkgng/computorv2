class Lexer:
    def __init__(self, str):
        self.str = str.replace(' ', '')
        self.pos = 0

    def tokenize(self):
        tokens = []
        while self.pos < len(self.str):
            c = self.str[self.pos]
