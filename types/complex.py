from rational import Rational
from polynomial import Polynomial
from matrix import Matrix
from function import Function

class Complex:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __pos__(self):
        return self

    def __neg__(self):
        return Complex(-self.real, -self.imaginary)

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imaginary + other.imaginary)
        elif isinstance(other, Rational):
            return Complex(self.real + other.numerator / other.denominator, self.imaginary)
        elif isinstance(other, Polynomial):
            coef = other.coefficients
            coef[0] += self.real
            return Polynomial(coef, other.variable)
        elif isinstance(other, Matrix):
            raise TypeError("Cannot add a complex number to a matrix")
        elif isinstance(other, Function):
            raise TypeError("Cannot add a complex number to a function")

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imaginary - other.imaginary)
        elif isinstance(other, Rational):
            return Complex(self.real - other.numerator / other.denominator, self.imaginary)
        elif isinstance(other, Polynomial):
            coef = other.coefficients
            coef[0] -= self.real
            return Polynomial(coef, other.variable)
        elif isinstance(other, Matrix):
            raise TypeError("Cannot subtract a complex number from a matrix")
        elif isinstance(other, Function):
            raise TypeError("Cannot subtract a complex number from a function")

    def __mul__(self, other):
        if isinstance(other, Complex):
            real = self.real * other.real - self.imaginary * other.imaginary
            imaginary = self.imaginary * other.real + self.real * other.imaginary
            return Complex(real, imaginary)
        elif isinstance(other, Rational):
            return Complex(self.real * other.numerator / other.denominator, self.imaginary * other.numerator / other.denominator)
        elif isinstance(other, Polynomial):
            coef = other.coefficients
            for i in range(len(coef)):
                coef[i] *= self.real
            return Polynomial(coef, other.variable)
        elif isinstance(other, Matrix):
            return other * self
        elif isinstance(other, Function):
            raise TypeError("Cannot multiply a complex number by a function")

    def __truediv__(self, other):
        if isinstance(other, Complex):
            denom = other.real ** 2 + other.imaginary ** 2
            real = (self.real * other.real + self.imaginary * other.imaginary) / denom
            imaginary = (self.imaginary * other.real - self.real * other.imaginary) / denom
            return Complex(real, imaginary)
        elif isinstance(other, Rational):
            return Complex(self.real / other.numerator * other.denominator, self.imaginary / other.numerator * other.denominator)
        elif isinstance(other, Polynomial):
            coef = other.coefficients
            for i in range(len(coef)):
                coef[i] /= self.real
            return Polynomial(coef, other.variable)
        elif isinstance(other, Matrix):
            raise TypeError("Cannot divide a complex number by a matrix")
        elif isinstance(other, Function):
            raise TypeError("Cannot divide a complex number by a function")

    def __xor__(self, power):
        if isinstance(power, int):
            if power == 0:
                return Complex(1, 0)
            elif power == 1:
                return self
            elif power == 2:
                return self * self
            else:
                return self * (self ^ (power - 1))
        elif isinstance(power, Rational):
            return (self ^ power.numerator) ** (1 / power.denominator)
        elif isinstance(power, Polynomial):
            raise TypeError("Cannot raise a complex number to a polynomial")
        elif isinstance(power, Matrix):
            raise TypeError("Cannot raise a complex number to a matrix")
        elif isinstance(power, Function):
            raise TypeError("Cannot raise a complex number to a function")

    def conjugate(self):
        return Complex(self.real, -self.imaginary)

    def __str__(self):
        if self.imaginary >= 0:
            return f"{self.real} + {self.imaginary}i"
        else:
            return f"{self.real} - {-self.imaginary}i"

    def __eq__(self, other):
        return self.real == other.real and self.imaginary == other.imaginary