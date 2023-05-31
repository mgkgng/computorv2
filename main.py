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
    print("Please put your input here. Type 'HELP' to see the usage and 'EXIT' to exit.")
    while True:
        try:
            s = input(">>> ")
            if s == 'EXIT':
                break
            if s == 'HELP':
                print('''usage:
    Assignment: <variable> = <expression>
    Computation: <expression> = ?
    Solve: <expression> = <expression> ? (supported only for polynomials of degree <= 3)
                
    Special commands:
        HELP: show help
        VARS: show variables
        FUNCS: show functions
        PLOT <function name>: plot function
        DEBUG_ON: turn on debug mode
        DEBUG_OFF: turn off debug mode''')
                continue
            if s == 'VARS':
                computor.print_vars()
                continue
            if s == 'FUNCS':
                computor.print_funcs()
                continue
            if s.startswith('PLOT '):
                args = s.split(' ')
                if len(args) != 2 or not len(args[1]):
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
            if ast.type == AST_TYPE.ASSIGN:
                res = computor.assign(left, right)
            elif ast.type == AST_TYPE.COMPUTE_VAL:
                res = computor.compute_val(left)
            elif ast.type == AST_TYPE.COMPUTE_SOL:
                res = computor.compute_sol(left, right)
            # TODO1 : if fraction, print float value
            print(res)
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


