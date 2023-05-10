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
        else:
            return Complex(self.real + other, self.imaginary)

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imaginary - other.imaginary)
        else:
            return Complex(self.real - other, self.imaginary)

    def __mul__(self, other):
        if isinstance(other, Complex):
            real = self.real * other.real - self.imaginary * other.imaginary
            imaginary = self.imaginary * other.real + self.real * other.imaginary
            return Complex(real, imaginary)
        else:
            return Complex(self.real * other, self.imaginary * other)

    def __truediv__(self, other):
        if isinstance(other, Complex):
            denom = other.real ** 2 + other.imaginary ** 2
            real = (self.real * other.real + self.imaginary * other.imaginary) / denom
            imaginary = (self.imaginary * other.real - self.real * other.imaginary) / denom
            return Complex(real, imaginary)
        else:
            return Complex(self.real / other, self.imaginary / other)

    def conjugate(self):
        return Complex(self.real, -self.imaginary)

    def __str__(self):
        if self.imaginary >= 0:
            return f"{self.real} + {self.imaginary}i"
        else:
            return f"{self.real} - {-self.imaginary}i"

    def __eq__(self, other):
        pass