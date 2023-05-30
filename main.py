from computor import Computor
from parser import Lexer, Parser, AST_TYPE
from interpreter import Interpreter
from utils import print_tokens
import traceback
import readline


if __name__ == "__main__":
    computor = Computor()
    lexer = Lexer()
    parser = Parser()
    debug = False
    while True:
        try:
            s = input(">>> ")
            readline.add_history(s)
            if s == "DEBUG_ON":
                debug = True
                continue
            elif s == "DEBUG_OFF":
                debug = False
                continue
            tokens = lexer.run(s)
            if debug:
                print_tokens(tokens)
                print('parser begins')
            ast = parser.run(tokens)
            if debug:
                print(ast)
                print('interpreter begins')
            interpreter = Interpreter(ast.root, ast.type)
            left, right = interpreter.run()
            print('computor begins')
            if ast.type == AST_TYPE.ASSIGN:
                res = computor.assign(left, right)
            elif ast.type == AST_TYPE.COMPUTE_VAL:
                res = computor.compute_val(left)
            elif ast.type == AST_TYPE.COMPUTE_SOL:
                res = computor.compute_sol(left, right)
            # TODO1 : if fraction, print float value
            print(res)
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


