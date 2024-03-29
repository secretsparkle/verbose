class Token:
    def __init__(self, _type, lexeme, literal, line):
        self.token_type = _type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    # def __str__(self): returns the string for str(Token). Pretty cool
    def __str__(self):
        return f'{self.token_type} {self.lexeme} {self.literal};'
