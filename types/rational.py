import math

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
        pass

    def __add__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator * other.denominator + other.numerator * self.denominator
            denominator = self.denominator * other.denominator
            return Rational(numerator, denominator)
        else:
            return Rational(self.numerator + other * self.denominator, self.denominator)

    def __sub__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator * other.denominator - other.numerator * self.denominator
            denominator = self.denominator * other.denominator
            return Rational(numerator, denominator)
        else:
            return Rational(self.numerator - other * self.denominator, self.denominator)

    def __mul__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator * other.numerator
            denominator = self.denominator * other.denominator
            return Rational(numerator, denominator)
        else:
            return Rational(self.numerator * other, self.denominator)

    def __truediv__(self, other):
        if isinstance(other, Rational):
            if other.numerator == 0:
                raise ZeroDivisionError("Division by zero")

            numerator = self.numerator * other.denominator
            denominator = self.denominator * other.numerator
            return Rational(numerator, denominator)
        else:
            if other == 0:
                raise ZeroDivisionError("Division by zero")
            return Rational(self.numerator, self.denominator * other)

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
        pass