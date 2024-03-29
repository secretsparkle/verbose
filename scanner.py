from tokentype import TokenType
from token import Token

class Scanner:
    def __init__(self, source) -> None:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "add" : TokenType.ADD,
            "and" : TokenType.AND,
            "as" : TokenType.AS,
            "becomes" : TokenType.BECOMES,
            "break" : TokenType.BREAK,
            "class" : TokenType.CLASS,
            "comment" : TokenType.COMMENT,
            "define" : TokenType.DEFINE,
            "else" : TokenType.ELSE,
            "end" : TokenType.END,
            "false" : TokenType.FALSE,
            "for" : TokenType.FOR,
            "greater" : TokenType.GREATER,
            "if" : TokenType.IF,
            "import" : TokenType.IMPORT,
            "in" : TokenType.IN,
            "is" : TokenType.IS,
            "lambda" : TokenType.LAMBDA,
            "leave" : TokenType.LEAVE,
            "less" : TokenType.LESS,
            "loop" : TokenType.LOOP,
            "mod" : TokenType.MOD,
            "null" : TokenType.NULL,
            "or" : TokenType.OR,
            "otherwise" : TokenType.OTHERWISE,
            "out" : TokenType.OUT,
            "print" : TokenType.PRINT,
            "return" : TokenType.RETURN,
            "set" : TokenType.SET,
            "super" : TokenType.SUPER,
            "takes" : TokenType.TAKES,
            "than" : TokenType.THAN,
            "then" : TokenType.THEN,
            "this" : TokenType.THIS,
            "through" : TokenType.THROUGH,
            "to" : TokenType.TO,
            "true" : TokenType.TRUE,
            "var" : TokenType.VAR,
            "while" : TokenType.WHILE
        }

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == '[':
            self.add_token(TokenType.LEFT_BRACKET)
        elif c == ']':
            self.add_token(TokenType.RIGHT_BRACKET)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            if (self.match('=')):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif c == '=':
            if (self.match('=')):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c == '>':
            if (self.match('=')):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c == '<':
            if (self.match('=')):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c == '/':
            if (self.match('/')):
                while ((self.peek() != '\n') and (self.is_at_end() == False)):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == '\n':
            self.line += 1
            self.add_token(TokenType.NEWLINE)
        elif c == ' ':
            self.add_token(TokenType.SPACE)
        elif c == '\t':
            self.add_token(TokenType.TAB)
        elif c == '\r':
            pass
        elif c == '"':
            self.string()
        else:
            if (c.isdigit()):
                self.number()
            elif (c.isalpha()):
                self.identifier()
            else:
                raise ValueError("Unexpected character.")

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type):
        self.add_token_main(token_type, None)

    def add_token_main(self, token_type, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, expected):
        if (self.is_at_end()):
            return False
        if (self.source[self.current] != expected):
            return False
        self.current += 1
        return True

    def peek(self):
        if (self.is_at_end()):
            return '\0'
        return self.source[self.current]

    def string(self):
        while (self.peek() != '"' and not self.is_at_end()):
            if (self.peek() == '\n'):
                self.line += 1
            self.advance()
        if (self.is_at_end()):
            raise ValueError("Unterminated string.")
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token_main(TokenType.STRING, value)

    def number(self):
        while (self.peek().isdigit()):
            self.advance()
        if (self.peek() == '.' and self.peek_next().isdigit()):
            self.advance()
            while (self.peek().isdigit()):
                self.advance()
        self.add_token_main(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def peek_next(self):
        if (self.current + 1 >= len(self.source)):
            return '\0'
        return self.source[self.current + 1]

    def identifier(self):
        while (self.peek().isalnum() or self.peek() == '-'):
            self.advance()
        text = self.source[self.start:self.current]
        type = self.keywords.get(text)
        if (type is None):
            type = TokenType.IDENTIFIER
        self.add_token(type)
