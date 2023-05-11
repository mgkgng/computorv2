from computor import Computor
from parser import Lexer, Parser, AST_TYPE
from interpreter import Interpreter
from utils import print_tokens
import sys

if __name__ == "__main__":
    computor = Computor()
    lexer = Lexer()
    parser = Parser()
    while True:
        try:
            s = input(">>> ")
            if s == "exit":
                sys.exit('Bye')
            print('lexer begins')
            tokens = lexer.run(s)
            print_tokens(tokens)
            print('parser begins')
            ast = parser.run(tokens)
            print('interpreter begins')
            interpreter = Interpreter(ast.root, ast.type)
            left, right = interpreter.visit()
            print('computor begins')
            if ast.type == AST_TYPE.ASSIGN:
                res = computor.assign(left, right)
            elif ast.type == AST_TYPE.COMPUTE_VAL:
                res = computor.compute(left, right)
            elif ast.type == AST_TYPE.COMPUTE_SOL:
                res = computor.compute(left, right)
            print(res)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            break
        except EOFError:
            print("\nEOFError")
            break
        except Exception as e:
            print("Error:", e)
