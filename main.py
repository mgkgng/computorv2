from computor import computor
from parser import Lexer, Parser, AST_TYPE
from interpreter import Interpreter
from utils import print_tokens
import traceback
import readline

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser()
    debug = False
    while True:
        try:
            print("Please put your input here. Type 'HELP' to see the usage.")
            s = input(">>> ")
            if s == 'HELP':
                print('usage TODO')
                print()
                continue
            if s == 'VARS':
                computor.print_vars()
                continue
            if s == 'FUNCS':
                computor.print_funcs()
                continue
            if s.startswith('PLOT '):
                args = s.split(' ')
                if len(args) != 2:
                    print("Usage: PLOT <function name>")
                    continue
                if args[1] in computor.funcs:
                    computor.funcs[args[1]].plot()
                else:
                    print(f"Function {args[1]} is not defined")
                continue
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


