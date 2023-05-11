from rational import Rational
from function import Function

class Polynomial:
    def __init__(self, coeffs, variable):
        if not coeffs or not isinstance(coeffs, list) or len():
            raise ValueError("Polynomial coefficients should be a non-empty list")
        
        # coefficients index: 0 -> x^0, 1 -> x^1, 2 -> x^2, ...
        self.coeffs = coeffs
        self.variable = variable

    def __pos__(self):
        return self

    def __neg__(self):
        return Polynomial([-coef for coef in self.coeffs], self.variable)

    def __str__(self):
        if len(self.coeffs) == 1 and self.coeffs[0] == 0:
            return "0"
        
        terms = []
        for i, coef in enumerate(self.coeffs):
            if coef == 0:
                continue
            
            term = str(coef) if i == 0 or abs(coef) != 1 else "-" if coef < 0 else ""
            if i > 0:
                term += self.variable
                if i > 1:
                    term += f"^{i}"
            
            terms.append(term)
        
        return " + ".join(terms).replace(" + -", " - ")

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                # if variables are different, I will treat them as constants
                coeffs1 = self.coeffs
                coeffs1[0] += other
                return Polynomial(coeffs1, self.variable)

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
            return self + Polynomial([other], self.variable)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                # if variables are different, treat them as constants
                coeffs1 = self.coeffs
                for i in range(len(coeffs1)):
                    coeffs1[i] *= other
                return Polynomial(coeffs1, self.variable)
            deg = len(self.coeffs) + len(other.coeffs) - 1
            res = [0] * deg
            for i, coef1 in enumerate(self.coeffs):
                for j, coef2 in enumerate(other.coeffs):
                    res[i + j] += coef1 * coef2
            return Polynomial(res, self.variable)
        elif isinstance(other, Function):
            raise TypeError("Cannot multiply a polynomial by a function")
        else:
            return self * Polynomial([other], self.variable)

    def __call__(self, x):
        return sum([coef * x ** i for i, coef in enumerate(self.coeffs)])
    
    def degree(self):
        return len(self.coeffs) - 1

    def __pow__(self, power):
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