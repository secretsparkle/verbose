import sys
from scanner import Scanner
from parser import Parser
from preprocessor import PreProcessor
from translator import Translator

def main():
    if len(sys.argv) > 2:
        print("The program currently only takes one argument")
    elif len(sys.argv) == 2:
        # take the file argument
        source = open(sys.argv[1], "r")
        source = source.read()
        print(source)
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        preprocessor = PreProcessor(tokens)
        processed_tokens = preprocessor.process()
        for token in processed_tokens:
            print(str(token))
        translator = Translator("output.py", processed_tokens)

    else:
        # no arguments, run the repl
        while True:
            query = input("> ")
            print(query)
            if query == 'q' or query == "exit" or query == "quit":
                break

if __name__ == '__main__':
    main()
