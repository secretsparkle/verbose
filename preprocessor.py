from tokentype import TokenType
from token import Token

class PreProcessor:
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def process(self):
        while self.tokens[self.current].token_type != TokenType.EOF:
            self.process_tokens()
        #self.tokens.insert(self.current-1, Token(TokenType.NEWLINE, '\n', None, 0))
        self.current = 0
        while self.tokens[self.current].token_type != TokenType.EOF:
            self.remove_spaces()
        self.current = 0
        while self.tokens[self.current].token_type != TokenType.EOF:
            self.remove_spaces()

        return self.tokens

    def process_tokens(self):
        # insert tabs for spaces after newline
        if self.tokens[self.current].token_type == TokenType.NEWLINE:
            num_spaces = self.count_spaces()
            index = 1
            while num_spaces > 0:
                self.tokens.insert(self.current + index, Token(TokenType.TAB, '\t', None, 0))
                index += 1
                num_spaces -= 4
        # perform changes to identifiers to make them pythonic and mask them
        elif self.tokens[self.current].token_type == TokenType.IDENTIFIER:
            self.tokens[self.current].lexeme = self.tokens[self.current].lexeme.replace('-', '_')
            if self.tokens[self.current].lexeme == "not":
                self.tokens[self.current].lexeme += "_"

        self.current += 1

    # too crazy, need to figure out this bug
    def remove_spaces(self):
        if self.tokens[self.current].token_type == TokenType.SPACE:
            self.tokens.pop(self.current)
            if self.tokens[self.current].token_type == TokenType.SPACE:
                self.tokens.pop(self.current)
                if self.tokens[self.current].token_type == TokenType.SPACE:
                    self.tokens.pop(self.current)
        self.current += 1

    def count_spaces(self):
        num_spaces = 0
        current_space = self.current + 1
        while self.tokens[current_space].token_type == TokenType.SPACE:
            num_spaces += 1
            current_space += 1
        return num_spaces
