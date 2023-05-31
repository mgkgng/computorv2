import math
from decimal import Decimal
from fractions import Fraction

class Rational:
    def __init__(self, numerator, denominator=1):
        # print(numerator, denominator)

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
            return Rational(self.numerator * other.denominator + other.numerator * self.denominator, \
                self.denominator * other.denominator)
        elif isinstance(other, int):
            return Rational(self.numerator + other * self.denominator, self.denominator)
        elif isinstance(other, float):
            decimal_value = Decimal(str(other))
            fraction = Fraction(decimal_value)
            return Rational(self.numerator * fraction.denominator + fraction.numerator * self.denominator, \
                self.denominator * fraction.denominator)

        else:
            return other + self
    
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator * other.denominator - other.numerator * self.denominator
            denominator = self.denominator * other.denominator
            return Rational(numerator, denominator)
        else:
            return -other + self

    def __mul__(self, other):
        if isinstance(other, Rational):
            return Rational(self.numerator * other.numerator, self.denominator * other.denominator)
        elif isinstance(other, int):
            return Rational(self.numerator * other, self.denominator)
        elif isinstance(other, float):
            decimal_value = Decimal(str(other))
            fraction = Fraction(decimal_value)
            return Rational(self.numerator * fraction.numerator, self.denominator * fraction.denominator)
        else:
            return other * self

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Rational):
            if other.numerator == 0:
                raise ZeroDivisionError("Division by zero")

            numerator = self.numerator * other.denominator
            denominator = self.denominator * other.numerator
            return Rational(numerator, denominator)
        else:
            return other ** -1 * self
    
    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return str(self.to_float())

    def __repr__(self):
        return self.__str__()

    def to_float(self):
        res = float(self.numerator) / float(self.denominator)
        return int(res) if res.is_integer() else res

    def __eq__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.to_float() == other
        return self.to_float() == other.to_float()

    def __pow__(self, power):
        if isinstance(power, int) and power >= 0:
            return Rational(self.numerator ** power, self.denominator ** power)
        else:
            return self.to_float() ** power
    
    def __mod__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.to_float() % other
        return self.to_float() % other.to_float()

    def __rpow__(self, other):
        return other ** self.to_float()

    def __abs__(self):
        return abs(self.to_float())

    def __lt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.to_float() < other
        return self.to_float() < other.to_float()

    def __le__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.to_float() <= other
        return self.to_float() <= other.to_float()

    def __gt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.to_float() > other
        return self.to_float() > other.to_float()

    def __ge__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.to_float() >= other
        return self.to_float() >= other.to_float()

    def __float__(self):
        return float(self.to_float())