from tokentype import TokenType
from token import Token

# parser error codes
SUCCESS = 0
ERROR = 1

class ParseError(RuntimeError):
    """An error has occurred"""

class Parser:
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def parse(self):
        print(len(self.tokens))
        return self.body()

    def body(self):
        print("body")
        while True:
            if self.expression() or self.statement():
                continue
            elif self.match(TokenType.EOF):
                break
            else:
                return False
        return True

    def binary(self):
        print("binary")
        if not (self.literal() or self.grouping() or self.function_call()):
            return False
        if not (self.is_statement() or self.match(TokenType.AND) or self.match(TokenType.OR)):
            return False
        if not (self.literal() or self.grouping() or self.function_call()):
            return False
        else:
            return True

    def grouping(self):
        print("grouping")
        if not self.match(TokenType.LEFT_PAREN):
            return False
        if not (self.literal() or self.function_call() or self.lambda_expression()):
            return False
        if not self.match(TokenType.RIGHT_PAREN):
            return False
        return True

    def statement(self):
        print("statement")
        if self.return_statement() or self.if_statement() or self.set_statement() or self.print_statement():
            return True
        else:
            return False

    def expression(self):
        print("expression")
        if self.literal() or self.function_call() or self.lambda_expression() or self.grouping() or self.binary() or self.match(TokenType.IDENTIFIER):
            return True
        else:
            return False

    def function_call(self):
        print("function call")
        if self.match(TokenType.IDENTIFIER):
            while True:
                if not self.expression():
                    self.current -= 1
                    return False
        return True

    def lambda_expression(self):
        print("lambda")
        if not self.match(TokenType.LAMBDA):
            return False
        while self.expression():
            continue
        return self.function_body()

    def function_body(self):
        print("function body")
        if self.expression() or self.statement():
            while True:
                if not (self.expression() or self.statement()):
                    return False
        else:
            return False

    def if_statement(self):
        print("if statement")
        if not self.match(TokenType.IF):
            return False
        if not self.expression():
            return False
        if not self.statement():
            return False
        while self.otherwise_if():
            continue
        if self.match(TokenType.OTHERWISE) and self.statement():
            return True
        else:
            return True

    def otherwise_if(self):
        print("otherwise if")
        if not self.match(TokenType.OTHERWISE):
            return False
        if not self.match(TokenType.IF):
            return False
        if not self.statement():
            return False
        return True

    def set_statement(self):
        print("set statement")
        if self.match(TokenType.SET):
            if self.match(TokenType.IDENTIFIER):
                if self.expression():
                    return True
            else:
                self.current -= 1

    def print_statement(self):
        print("print statement")
        if self.match(TokenType.PRINT):
            if self.expression():
                return True
            else:
                self.current -= 1
                return False
        else:
            return False

    def return_statement(self):
        print("return statement")
        if self.match(TokenType.RETURN):
            if self.expression():
                return True
            else:
                self.current -= 1
                return False

    def is_statement(self):
        print("is statement")
        if self.tokens[self.current].token_type == TokenType.IS:
            # IS
            if self.match(TokenType.LESS) or self.match(TokenType.GREATER):
                # IS GREATER or IS LESS
                if self.match(TokenType.THAN):
                    # IS GREATER THAN or IS LESS THAN
                    return True
                else:
                    # IS GREATER WRONG
                    # IS LESS WRONG
                    return ParseError("Invalid IS Statement")
            elif self.match(TokenType.NOT):
                # IS NOT
                return True
            else:
                # only IS matched
                return True
        else:
            # no match at all
            self.current -= 1
            return False

    def literal(self):
        print("literal")
        if self.match(TokenType.STRING, TokenType.NUMBER, TokenType.TRUE,
                      TokenType.FALSE, TokenType.NULL):
            return True
        else:
            return False

    def match(self, *types):
        print("Token: ", self.tokens[self.current])
        print("Index: ", self.current)
        for t in types:
            if self.tokens[self.current].token_type == t:
                self.advance()
                return True
        return False

    def advance(self):
        self.current += 1

    def previous(self):
        self.current -= 1

    def peek(self):
        return self.tokens[self.current + 1]

    def double_peek(self):
        return self.tokens[self.current + 2]

    def is_at_end(self):
        return self.peek().type == TokenType.EOF
