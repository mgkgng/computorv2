from computor import Computor
from parser import lexer, parser, AST_TYPE
from interpreter import Interpreter
import sys

if __name__ == "__main__":
    computor = Computor()
    while True:
        try:
            s = input(">>> ")
            if s == "exit":
                sys.exit('Bye')
            tokens = lexer(s)
            ast = parser(tokens)
            interpreter = Interpreter(ast.root, ast.type)
            left, right = interpreter.visit()
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
            break