from types import Complex, Rational, Matrix, Polynomial, Function

class Computor:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def assign(self, left, right):
        if isinstance(left, Polynomial):
            if not isinstance(right, Rational) and not isinstance(right, Complex) and not isinstance(right, Matrix):
                raise TypeError("Cannot assign a polynomial or a function to a variable")
            self.vars[left.variable] = right
        elif isinstance(left, Function):
            if isinstance(right, Function):
                raise TypeError("Cannot assign a function to another function")
            if isinstance(right, Polynomial) and right.variable != left.arg:
                raise TypeError("Cannot assign a polynomial to a function with a different variable")
            self.funcs[left.name] = right
        else:
            raise ValueError(f"Unexpected node type: {type(left)}")
        return right

    def compute_val(self, left, right):
        if isinstance(left, Polynomial):
            if left.variable in self.vars:
                return left(self.vars[left.variable])
            else:
                raise ValueError(f"Variable {left.variable} is not defined")

        elif isinstance(left, Function): # TODO chain of functions, variable in function ...
            if left.name in self.funcs:
                return self.funcs[left.name](left.arg)
            else:
                raise ValueError(f"Function {left.name} is not defined")

        else:
            return left

    def compute_sol(self, left, right):
        pass
        
        
