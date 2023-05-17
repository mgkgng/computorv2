from computor import Computor
from parser import Lexer, Parser, AST_TYPE
from interpreter import Interpreter
from utils import print_tokens
import sys
import traceback


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
            # print(ast)
            print('interpreter begins')
            interpreter = Interpreter(ast.root, ast.type)
            left, right = interpreter.run()
            print('computor begins')
            if ast.type == AST_TYPE.ASSIGN:
                res = computor.assign(left, right)
                print(res)
            elif ast.type == AST_TYPE.COMPUTE_VAL:
                computor.compute_val(left)
            elif ast.type == AST_TYPE.COMPUTE_SOL:
                computor.compute_sol(left, right)
            print(computor)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            break
        except EOFError:
            print("\nEOFError")
            break
        except Exception as e:
            print("Error:", e)
            traceback_info = traceback.format_exc()
            print(traceback_info)


