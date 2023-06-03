from computor import computor
from parser import Lexer, Parser, AST_TYPE
from interpreter import Interpreter
import traceback
import readline

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser()
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
        DEL <variable/function name>: delete variable/function''')
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
            if s.startswith('DEL '):
                args = s.split(' ')
                if len(args) != 2 or not len(args[1]):
                    print("Usage: DEL <variable/function name>")
                    continue
                if args[1] in computor.vars:
                    del computor.vars[args[1]]
                elif args[1] in computor.funcs:
                    del computor.funcs[args[1]]
                else:
                    print(f"Variable or function {args[1]} is not defined")
                continue
        
            readline.add_history(s)
            tokens = lexer.run(s)
            ast = parser.run(tokens)
            interpreter = Interpreter(ast.root, ast.type)
            left, right = interpreter.run()
            if ast.type == AST_TYPE.ASSIGN:
                res = computor.assign(left, right)
            elif ast.type == AST_TYPE.COMPUTE_VAL:
                res = computor.compute_val(left)
            elif ast.type == AST_TYPE.COMPUTE_SOL:
                res = computor.compute_sol(left, right)
            if res is not None:
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


