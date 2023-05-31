from .function import Function
from .rational import Rational
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce

class Polynomial:
    def __init__(self, coeffs, variable=None, divisor=None):
        if not coeffs or not isinstance(coeffs, list) or len(coeffs) == 0:
            raise ValueError("Polynomial coefficients should be a non-empty list")
        
        # coefficients index: 0 -> x^0, 1 -> x^1, 2 -> x^2, ...
        self.coeffs = coeffs
        self.variable = variable
        self.degree = len(coeffs) - 1

    def __pos__(self):
        return self

    def __neg__(self):
        return Polynomial([-coef for coef in self.coeffs], self.variable)

    def __str__(self):
        if len(self.coeffs) == 1 and self.coeffs[0] == 0:
            return "0"

        variable = self.variable if self.variable else "x"
        
        terms = []
        for i, coef in enumerate(self.coeffs):
            if coef == 0:
                continue
            
            term = str(coef) if i == 0 or ((isinstance(coef, int) or isinstance(coef, Rational)) and abs(coef) != 1) else "-" if (isinstance(coef, int) or isinstance(coef, Rational)) and coef < 0 else ""
            if i > 0:
                term += variable
                if i > 1:
                    term += f"^{i}"
            
            terms.append(term)
        
        return " + ".join(terms).replace(" + -", " - ")

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                raise ValueError("Polynomials should have the same variable")
            deg = max(len(self.coeffs), len(other.coeffs))
            res = [0] * deg
            i = 0
            while i < len(self.coeffs):
                res[i] = self.coeffs[i] + other.coeffs[i] if i < len(other.coeffs) else self.coeffs[i]
                i += 1
            while i < len(other.coeffs):
                res[i] = other.coeffs[i]
                i += 1
            return Polynomial(res, self.variable)  
        elif isinstance(other, Function):
            raise TypeError("Cannot add a polynomial to a function")
        else:
            new_coeffs = self.coeffs.copy()
            new_coeffs[0] = new_coeffs[0] + other
            return Polynomial(new_coeffs, self.variable)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, Rational):
            return Polynomial([coef * other for coef in self.coeffs], self.variable)
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                # if variables are different, treat them as constants
                coeffs = self.coeffs
                for i in range(len(coeffs)):
                    coeffs[i] *= other
                return Polynomial(coeffs, self.variable)
            deg = len(self.coeffs) + len(other.coeffs) - 1
            res = [0] * deg
            for i, coef1 in enumerate(self.coeffs):
                for j, coef2 in enumerate(other.coeffs):
                    res[i + j] += coef1 * coef2
            return Polynomial(res, self.variable)
        elif isinstance(other, Function):
            raise TypeError("Cannot multiply a polynomial by a function")
        else:
            return self * Polynomial([other])

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other,float) or isinstance(other, Rational):
            return Polynomial([coef / other for coef in self.coeffs], self.variable)
        if isinstance(other, Polynomial) or isinstance(other, PolynomialWrapper):
            if self.variable != other.variable :
                raise ValueError("Polynomials should have the same variable")
            return PolynomialWrapper(self, other, self.variable)
        raise TypeError("Cannot divide a polynomial by this type")

    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Rational):
            return PolynomialWrapper(other, self, self.variable)
        raise TypeError("Cannot divide this type by a polynomial")

    def __call__(self, x):
        # if isinstance(x, Polynomial):
        #     raise TypeError("Cannot call a polynomial with a polynomial")
        return sum([coef * x ** i for i, coef in enumerate(self.coeffs)])
    
    def __pow__(self, power):
        if isinstance(power, Rational) and power.denominator == 1:
            power = power.numerator
        if not isinstance(power, int):
            raise TypeError("Power should be an integer")

        if power < 0:
            raise ValueError("Negative powers are not supported")

        if power == 0:
            return Rational(1)

        res = self
        for _ in range(power - 1):
            res *= self

        return res

    def modify_var(self, new_var):
        self.variable = new_var

    def plot(self):
        x = np.linspace(-15, 15, 100)
        apply_func = np.vectorize(lambda x: reduce(lambda sum, coeff : sum + coeff[1] * (x ** coeff[0]), enumerate(self.coeffs), 0))
        y = apply_func(x)

        plt.axhline(0, color='black')  # Add horizontal x-axis at y=0
        plt.axvline(0, color='black')  # Add vertical y-axis at x=0
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.xlim(-15, 15)
        plt.plot(x, y)
        plt.grid(True)
        plt.show()

    def __float__(self):
        return float(self.coeffs[0])

class PolynomialWrapper:
    def __init__(self, dividend, divisor, variable):
        self.dividend = dividend
        self.divisor = divisor
        self.variable = variable

    def __str__(self):
        return f"{self.dividend} / {self.divisor}"
    
    def __repr__(self):
        return self.__str__()
    
    def __call__(self, x):

        return self.dividend(x) if isinstance(self.dividend, Polynomial) else self.dividend / self.divisor(x)
    
    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, Rational):
            return PolynomialWrapper(self.dividend + other * self.divisor, self.divisor, self.variable)
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                raise ValueError("Polynomials should have the same variable")
            return PolynomialWrapper(self.dividend + other * self.divisor, self.divisor, self.variable)
        else:
            raise TypeError("Operation too complex")
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return (-self) + other
    
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, Rational):
            return PolynomialWrapper(self.dividend * other, self.divisor, self.variable)
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                raise ValueError("Polynomials should have the same variable")
            return PolynomialWrapper(self.dividend * other, self.divisor, self.variable)
        else:
            raise TypeError("Operation too complex")
        
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, Rational):
            return PolynomialWrapper(self.dividend, self.divisor * other, self.variable)
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                raise ValueError("Polynomials should have the same variable")
            return PolynomialWrapper(self.dividend, self.divisor * other, self.variable)
        else:
            raise TypeError("Operation too complex")
    
    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, Rational):
            return PolynomialWrapper(self.divisor * other, self.dividend, self.variable)
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                raise ValueError("Polynomials should have the same variable")
            return PolynomialWrapper(self.divisor * other, self.dividend, self.variable)
        else:
            raise TypeError("Operation too complex")
    
    def plot(self):
        x = np.linspace(-15, 15, 100)
        apply_func = np.vectorize(lambda x: self(x))
        y = apply_func(x)

        plt.axhline(0, color='black')
        plt.axvline(0, color='black')  # Add vertical y-axis at x=0
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.xlim(-15, 15)
        plt.plot(x, y)
        plt.grid(True)
        plt.show()
