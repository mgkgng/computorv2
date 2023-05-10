import math
from complex import Complex
from polynomial import Polynomial
from matrix import Matrix
from function import Function

class Rational:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be 0")

        common_divisor = math.gcd(numerator, denominator)
        self.numerator = numerator // common_divisor
        self.denominator = denominator // common_divisor

    def __pos__(self):
        return self

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __add__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator * other.denominator + other.numerator * self.denominator
            denominator = self.denominator * other.denominator
            return Rational(numerator, denominator)
        elif isinstance(other, Complex):
            return other + self
        elif isinstance(other, Polynomial):
            coef = other.coefficients
            coef[0] += self.numerator / self.denominator
            return Polynomial(coef, other.variable)
        elif isinstance(other, Matrix):
            raise TypeError("Cannot add a rational number to a matrix")
        elif isinstance(other, Function):
            raise TypeError("Cannot add a rational number to a function")

    def __sub__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator * other.denominator - other.numerator * self.denominator
            denominator = self.denominator * other.denominator
            return Rational(numerator, denominator)
        elif isinstance(other, Complex):
            return Complex(self.numerator / self.denominator - other.real, -other.imaginary)
        elif isinstance(other, Polynomial):
            pass
        elif isinstance(other, Matrix):
            raise TypeError("Cannot subtract a rational number from a matrix")
        elif isinstance(other, Function):
            raise TypeError("Cannot subtract a rational number from a function")

    def __mul__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator * other.numerator
            denominator = self.denominator * other.denominator
            return Rational(numerator, denominator)
        elif isinstance(other, Complex):
            return other * self
        elif isinstance(other, Polynomial):
            coef = other.coefficients
            for i in range(len(coef)):
                coef[i] *= self.numerator / self.denominator
            return Polynomial(coef, other.variable)
        elif isinstance(other, Matrix):
            return other * self
        elif isinstance(other, Function):
            raise TypeError("Cannot multiply a rational number by a function")

    def __truediv__(self, other):
        if isinstance(other, Rational):
            if other.numerator == 0:
                raise ZeroDivisionError("Division by zero")

            numerator = self.numerator * other.denominator
            denominator = self.denominator * other.numerator
            return Rational(numerator, denominator)
        elif isinstance(other, Complex):   
            return Complex(self.numerator / self.denominator, 0) / other
        elif isinstance(other, Polynomial):
            pass
        elif isinstance(other, Matrix):
            raise TypeError("Cannot divide a rational number by a matrix")
        elif isinstance(other, Function):
            raise TypeError("Cannot divide a rational number by a function")
    
    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        return self.__str__()

    def to_float(self):
        return float(self.numerator) / float(self.denominator)

    def __eq__(self, other):
        return self.to_float() == other.to_float()