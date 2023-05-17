from type import Polynomial, Rational, Complex, Matrix, Function
import numpy as np

class Computor:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def assign(self, left, right):
        if isinstance(left, Polynomial):
            if not isinstance(right, Rational) and not isinstance(right, Complex) and not isinstance(right, Matrix):
                raise TypeError("Cannot assign a polynomial or a function to a variable")
            if not left.coeffs == [0, 1]:
                raise TypeError("Wrong variable format")
            self.vars[left.variable] = right
        elif isinstance(left, Function):
            if isinstance(right, Function):
                raise TypeError("Cannot assign a function to another function")
            if isinstance(right, Polynomial) and right.variable != left.arg.variable and right.variable not in self.vars:
                raise TypeError("Cannot assign a polynomial to a function with a different variable")
            self.funcs[left.name] = right
        else:
            raise ValueError(f"Unexpected node type: {type(left)}")
        return right

    def compute_val(self, left):
        if isinstance(left, Polynomial):
            left.substitute(self.vars)
            if left.variable not in self.vars:
                raise ValueError(f"Variable {left.variable} is not defined")
            return left(self.vars[left.variable])

        elif isinstance(left, Function): # TODO chain of functions, variable in function ...
            if left.name in self.funcs:
                return self.funcs[left.name](left.arg)
            raise ValueError(f"Function {left.name} is not defined")

        else:
            return left

    def compute_sol(self, left, right):
        if isinstance(right, Function):
            raise TypeError("Cannot put a function on the right side of an equation")

        if isinstance(left, Function):
            if not left.name in self.funcs:
                raise ValueError(f"Function {left.name} is not defined")
            left = self.funcs[left.name](left.arg)
            left.substitute(self.vars)

        if isinstance(left, Polynomial):
            left = left.substitute(self.vars)
        if isinstance(right, Polynomial):
            right = right.substitute(self.vars)

        if not isinstance(left, Polynomial):
            left = Polynomial([left])
        if not isinstance(right, Polynomial):
            right = Polynomial([right])
        if left.variable != right.variable:
            raise TypeError("Cannot compare a polynomial with a different variable")
                        
        # TODO maybe plot both sides of the equation here

        new_poly = left - right
        if new_poly.degree == 0:
            self.solve_constant(new_poly.coeffs)
        elif new_poly.degree == 1:
            self.solve_linear(new_poly.coeffs)
        elif new_poly.degree == 2:
            self.solve_quadratic(new_poly.coeffs)
        elif new_poly.degree == 3:
            self.solve_cubic(new_poly.coeffs)
        else:
            print('The polynomial degree is stricly greater than 2, I can\'t solve.')

    @staticmethod    
    def solve_constant(coef):
        print('All real numbers are solution' if coef[0] == 0 else 'There is no solution')

    @staticmethod
    def solve_linear(coefs):
        print('The solution is:')
        print(-coefs[0] / coefs[1])

    @staticmethod
    def solve_quadratic(coefs):
        a = coefs[2]
        b = coefs[1]
        c = coefs[0]
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            print('Discriminant is strictly negative, the two complex solutions are:')
            print(f'({-b / 2 * a} - i * {-discriminant ** 0.5 / 2 * a}')
            print(f'({-b / 2 * a} + i * {-discriminant ** 0.5 / 2 * a}')
        elif discriminant == 0:
            print('Discriminant is equal to zero, the solution is:')
            print(-b / (2 * a))
        else:
            print('Discriminant is strictly positive, the two real solutions are:')
            print(f'{(-b - discriminant ** 0.5) / (2 * a)}')
            print(f'{(-b + discriminant ** 0.5) / (2 * a)}')
    
    @staticmethod
    def solve_cubic(coefs):
        roots = np.roots(coefs[::-1])

        print('The solutions are:')
        for root in roots:
            print(root)

    def __str__(self):
        return f"vars: {self.vars}\nfuncs: {self.funcs}"