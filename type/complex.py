from .rational import Rational
from decimal import Decimal

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
        return other + self

    def __radd__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Complex(self.real + other, self.imaginary)
        return self + other

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imaginary - other.imaginary)
        elif isinstance(other, Rational):
            return Complex(self.real - other.numerator / other.denominator, self.imaginary)
        else:
            return -other + self

    def __mul__(self, other):
        if isinstance(other, Complex):
            real = self.real * other.real - self.imaginary * other.imaginary
            imaginary = self.imaginary * other.real + self.real * other.imaginary
            return Complex(real, imaginary)
        elif isinstance(other, Rational):
            return Complex(self.real * other.numerator / other.denominator, self.imaginary * other.numerator / other.denominator)
        elif isinstance(other, int) or isinstance(other, float):
            return Complex(self.real * other, self.imaginary * other)
        else:
            return other * self

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Complex):
            denom = other.real ** 2 + other.imaginary ** 2
            real = (self.real * other.real + self.imaginary * other.imaginary) / denom
            imaginary = (self.imaginary * other.real - self.real * other.imaginary) / denom
            return Complex(real, imaginary)
        elif isinstance(other, Rational):
            return Complex(self.real / other.numerator * other.denominator, self.imaginary / other.numerator * other.denominator)
        else:
            return other ** -1 * self

    def __xor__(self, power):
        if isinstance(power, Rational) and power.denominator == 1 and power.numerator >= 0:
            if power == 0:
                return Rational(1)
            elif power == 1:
                return self
            elif power == 2:
                return self * self
            else:
                return self * (self ^ (power - 1))
        else:
            raise TypeError("Power must be an integer greater than or equal to 0")

    def __str__(self):
        if self.imaginary >= 0:
            return f"{int(self.real) if self.real.is_integer() else self.real} + {int(self.imaginary) if self.imaginary.is_integer() else self.imaginary}i"
        else:
            return f"{int(self.real) if self.real.is_integer() else self.real} - {int(-self.imaginary) if self.imaginary.is_integer() else -self.imaginary}i"

    def __eq__(self, other):
        return self.real == other.real and self.imaginary == other.imaginary

    def __pow__(self, power):
        if power < 0:
            raise TypeError("Power of complex number must be an integer greater than or equal to 0")
        if power == 0:
            return Rational(1)
        elif power == 1:
            return self
        else:
            while power > 1:
                self = self * self
                power -= 1