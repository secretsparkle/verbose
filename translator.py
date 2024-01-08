from tokentype import TokenType
from token import Token

class Translator:
    def __init__(self, python_file, tokens):
        self.current = 0
        self.tokens = tokens
        self.identifiers = {"first": "function",
                            "rest": "function"}
        self.imported = dict()
        self.python_file = python_file
        self.output_file = open(self.python_file, "w")
        self.prepend_library_functions()
        self.translate()

    def prepend_library_functions(self):
        self.output_file.write("\ndef first(sequence):\n")
        self.output_file.write("\treturn sequence[0]\n")
        self.output_file.write("\ndef rest(sequence):\n")
        self.output_file.write("\treturn sequence[1:]\n")
        self.output_file.write("\ndef last(sequence):\n")
        self.output_file.write("\treturn sequence[-1]\n")
        self.output_file.write("\ndef prepend(atom, sequence):\n")
        self.output_file.write("\tsequence.insert(0, atom)\n")
        self.output_file.write("\ndef append(atom, sequence):\n")
        self.output_file.write("\tsequence.append(atom)\n")

    def peek(self):
        return self.tokens[self.current + 1]

    def double_peek(self):
        return self.tokens[self.current + 2]

    def advance(self):
        self.current += 1

    def match(self, token):
        return self.tokens[self.current].token_type == token

    def write_current_token(self):
        self.output_file.write(self.tokens[self.current].lexeme)

    def translate(self):
        while True:
            if self.match(TokenType.NEWLINE):
                self.current += 1
            self.expression()
            self.statement()
            if self.match(TokenType.EOF):
                return

    def expression(self):
        if self.match(TokenType.IDENTIFIER):
            self.function_call()
        elif self.match(TokenType.ADD):
            self.add_expression()

    def statement(self):
        if self.match(TokenType.SET):
            self.set_statement()
        elif self.match(TokenType.PRINT):
            self.print_statement()
        elif self.match(TokenType.IF):
            self.if_statement()
        elif self.match(TokenType.OTHERWISE):
            self.otherwise_statement()
        elif self.match(TokenType.RETURN):
            self.return_statement()
        elif self.match(TokenType.IMPORT):
            self.import_statement()
        elif self.match(TokenType.LOOP):
            self.loop_statement()
        elif self.match(TokenType.LEAVE):
            self.leave_statement()

    def function_call(self):
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1
        self.output_file.write("(")
        self.process_arguments()
        self.output_file.write(")")
        # print newline
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1

    def add_expression(self):
        # skip add keyword
        self.current += 1
        add_list = []
        was_right_paren = False
        while True:
            if self.tokens[self.current].token_type == TokenType.NEWLINE:
                break
            elif self.tokens[self.current].token_type == TokenType.RIGHT_PAREN:
                was_right_paren = True
                self.current += 1
                break
            else:
                add_list.append(self.tokens[self.current].lexeme)
                self.current += 1
        added = " + ".join(add_list)
        self.output_file.write("(")
        self.output_file.write(added)
        self.output_file.write(")")
        if was_right_paren:
            self.output_file.write(")")
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1
        self.process_tabs()

    def set_statement(self):
        if self.double_peek().token_type == TokenType.LAMBDA:
            # is function definition
            self.output_file.write("def ")
            self.current += 1
            self.output_file.write(self.tokens[self.current].lexeme)
            self.identifiers[self.tokens[self.current].lexeme] = "function"
            self.current += 2
            self.output_file.write("(")
            self.process_arguments()
            self.output_file.write("):")
            self.output_file.write(self.tokens[self.current].lexeme)
            self.current += 1
            self.process_tabs()
        else:
            # is variable defintion
            self.current += 1
            self.output_file.write(self.tokens[self.current].lexeme)
            self.identifiers[self.tokens[self.current].lexeme] = "variable"
            self.output_file.write(" = ")
            self.current += 1
            while True:
                if self.tokens[self.current].token_type == TokenType.NEWLINE:
                    self.output_file.write(self.tokens[self.current].lexeme)
                    self.current += 1
                    break
                elif self.match(TokenType.LEFT_BRACKET):
                    self.output_file.write(self.tokens[self.current].lexeme)
                    self.current += 1
                    while True:
                        if self.match(TokenType.RIGHT_BRACKET):
                            self.output_file.write(self.tokens[self.current].lexeme)
                            self.current += 1
                            break
                        else:
                            self.write_current_token()
                            if self.peek().token_type != TokenType.RIGHT_BRACKET:
                                self.output_file.write(", ")
                            self.advance()
                elif self.identifiers.get(self.tokens[self.current].lexeme) == "function":
                    self.process_arguments()
                elif self.match(TokenType.ADD):
                    self.add_expression()
                else:
                    self.output_file.write(self.tokens[self.current].lexeme)
                    self.output_file.write(" ")
                    self.current += 1
            self.process_tabs()

    def print_statement(self):
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1
        self.output_file.write("(")
        self.process_arguments()
        self.output_file.write(")")
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1
        self.process_tabs()

    def if_statement(self):
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1
        self.output_file.write(" ")
        while True:
            if self.tokens[self.current].token_type == TokenType.THEN:
                self.output_file.write(": ")
                self.current += 1
                if self.tokens[self.current].token_type == TokenType.PRINT:
                    self.print_statement()
                    break
                self.process_statement_body()
                break
            elif self.tokens[self.current].token_type == TokenType.NEWLINE:
                self.output_file.write(":")
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
                break
            elif self.identifiers.get(self.tokens[self.current].lexeme) == "function":
                self.process_arguments()
            elif self.tokens[self.current].token_type == TokenType.MOD:
                self.output_file.write(" % ")
                self.current += 1
            elif self.tokens[self.current].token_type == TokenType.IS:
                self.output_file.write(" == ")
                self.current += 1
            elif self.tokens[self.current].token_type == TokenType.TRUE:
                self.output_file.write("True")
                self.current += 1
            elif self.tokens[self.current].token_type == TokenType.FALSE:
                self.output_file.write("False")
                self.current += 1
            else:
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
        self.process_tabs()

    def otherwise_statement(self):
        if self.peek().token_type == TokenType.IF:
            self.output_file.write("elif ")
            self.current += 1
            # call if_statement?
        else:
            self.output_file.write("else: ")
            self.current += 1
            if self.tokens[self.current].token_type == TokenType.PRINT:
                self.print_statement()
                return
            self.process_statement_body()
            self.process_tabs()
            return

        while True:
            if self.tokens[self.current].token_type == TokenType.NEWLINE:
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
                break
            else:
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1

    def return_statement(self):
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1
        self.output_file.write(" ")
        while True:
            if self.tokens[self.current].token_type == TokenType.TRUE:
                self.output_file.write("True")
                self.current += 1
            elif self.tokens[self.current].token_type == TokenType.FALSE:
                self.output_file.write("False")
                self.current += 1
            elif self.tokens[self.current].token_type != TokenType.NEWLINE:
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
                self.output_file.write(" ")
            else:
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
                break
        self.process_tabs()

    def import_statement(self):
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1
        self.output_file.write(" ")
        self.imported[self.tokens[self.current].lexeme] = True
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1
        # print newline
        self.output_file.write(self.tokens[self.current].lexeme)
        self.current += 1

    def loop_statement(self):
        # skip the loop keyword
        self.current += 1
        if self.match(TokenType.THROUGH):
            # skip through
            self.current += 1
            self.output_file.write("for ")
            self.output_file.write(self.double_peek().lexeme)
            self.output_file.write(" in ")
            self.output_file.write(self.tokens[self.current].lexeme)
            self.current += 3
            self.output_file.write(":")
            #write the newline
            self.output_file.write(self.tokens[self.current].lexeme)
            self.current += 1
        elif self.match(TokenType.WHILE):
            self.output_file.write("while ")
            self.current += 1
            while True:
                if self.tokens[self.current].token_type == TokenType.NEWLINE:
                    self.output_file.write(":")
                    self.output_file.write(self.tokens[self.current].lexeme)
                    self.current += 1
                    break
                elif self.identifiers.get(self.tokens[self.current].lexeme) == "function":
                    self.process_arguments()
                elif self.tokens[self.current].token_type == TokenType.MOD:
                    self.output_file.write(" % ")
                    self.current += 1
                elif self.tokens[self.current].token_type == TokenType.IS:
                    self.output_file.write(" == ")
                    self.current += 1
                elif self.tokens[self.current].token_type == TokenType.TRUE:
                    self.output_file.write("True")
                    self.current += 1
                elif self.tokens[self.current].token_type == TokenType.FALSE:
                    self.output_file.write("False")
                    self.current += 1
                else:
                    self.output_file.write(self.tokens[self.current].lexeme)
                    self.current += 1
        self.process_tabs()

    def leave_statement(self):
        self.output_file.write("break\n")
        self.current += 2
        self.process_tabs()

    def process_statement_body(self):
        while True:
            if self.tokens[self.current].token_type == TokenType.NEWLINE:
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
                break
            elif self.tokens[self.current].token_type == TokenType.TRUE:
                self.output_file.write("True")
                self.current += 1
            elif self.tokens[self.current].token_type == TokenType.FALSE:
                self.output_file.write("False")
                self.current += 1
            else:
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
                self.output_file.write(" ")

    def process_tabs(self):
        while True:
            if self.tokens[self.current].token_type == TokenType.TAB:
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
            else:
                break

    def process_arguments(self):
        while True:
            if self.tokens[self.current].token_type == TokenType.LEFT_PAREN:
                while self.tokens[self.current].token_type != TokenType.RIGHT_PAREN:
                    self.output_file.write(self.tokens[self.current].lexeme)
                    self.current += 1
            elif self.imported.get(self.tokens[self.current].lexeme):
                # write the library
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
                # check for the dot operator
                if self.tokens[self.current].token_type == TokenType.DOT:
                    print("MADE IT HERE")
                    self.output_file.write(self.tokens[self.current].lexeme)
                    self.current += 1
                    # write the function
                    self.output_file.write(self.tokens[self.current].lexeme)
                    self.current += 1
                    self.output_file.write("(")
                    if self.identifiers.get(self.tokens[self.current].lexeme) == "function":
                        self.process_arguments()
                    while True:
                        if self.tokens[self.current].token_type == TokenType.THEN:
                            self.output_file.write(")")
                            return
                        elif self.tokens[self.current].token_type != TokenType.NEWLINE:
                            self.output_file.write(self.tokens[self.current].lexeme)
                            if self.peek().token_type == TokenType.NEWLINE:
                                self.current += 1
                                break
                            self.output_file.write(", ")
                            self.current += 1
                        else:
                            break
                    self.output_file.write(")")
                    break

            elif self.tokens[self.current].token_type == TokenType.ADD:
                self.add_expression()
            elif self.identifiers.get(self.tokens[self.current].lexeme) == "function":
                self.output_file.write(self.tokens[self.current].lexeme)
                self.current += 1
                self.output_file.write("(")
                if self.identifiers.get(self.tokens[self.current].lexeme) == "function":
                    self.process_arguments()
                while True:
                    if self.tokens[self.current].token_type == TokenType.THEN:
                        self.output_file.write(")")
                        return
                    elif self.tokens[self.current].token_type != TokenType.NEWLINE:
                        self.output_file.write(self.tokens[self.current].lexeme)
                        self.current += 1
                    else:
                        break
                self.output_file.write(")")
                break
            elif self.identifiers.get(self.tokens[self.current].lexeme) == "variable":
                if self.tokens[self.current].lexeme == "arguments":
                    self.output_file.write("*arguments")
            self.output_file.write(self.tokens[self.current].lexeme)
            self.current += 1
            if self.tokens[self.current].token_type == TokenType.NEWLINE:
                break
            else:
                self.output_file.write(", ")
