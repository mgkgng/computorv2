from .rational import Rational
from .complex import Complex

class Matrix:
    def __init__(self, elements):        
        row_length = len(elements[0])
        for row in elements:
            if len(row) != row_length:
                raise ValueError("All rows should have the same length")
        
        self.elements = elements
        self.shape = (len(elements), row_length)

    def __pos__(self):
        return self

    def __neg__(self):
        return self * -1

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.elements])

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Both operands should be of Matrix type")
        if self.shape != other.shape:
            raise ValueError("Matrices should have the same shape")

        result = [[self.elements[i][j] + other.elements[i][j] for j in range(self.num_cols)] for i in range(self.num_rows)]
        return Matrix(result)

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Both operands should be of Matrix type")
        if self.shape != other.shape:
            raise ValueError("Matrices should have the same shape")

        result = [[self.elements[i][j] - other.elements[i][j] for j in range(self.num_cols)] for i in range(self.num_rows)]
        return Matrix(result)

    # Scalar multiplication
    def __mul__(self, other):
        if not isinstance(other, Rational) and not isinstance(other, Complex):
            raise TypeError("Second operand should be of Rational or Complex type")
        result = [[other * self.elements[i][j] for j in range(self.num_cols)] for i in range(self.num_rows)]
        return Matrix(result)

    # Scalar division
    def __truediv__(self, other):
        if not isinstance(other, Rational) and not isinstance(other, Complex):
            raise TypeError("Second operand should be of Rational or Complex type")
        result = [[self.elements[i][j] / other for j in range(self.num_cols)] for i in range(self.num_rows)]
        return Matrix(result)

    def transpose(self):
        transposed_elements = [[self.elements[j][i] for j in range(self.num_rows)] for i in range(self.num_cols)]
        return Matrix(transposed_elements)

    @staticmethod
    def identity(n):
        elements = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return Matrix(elements)

    def __pow__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Both operands should be of Matrix type")
        if self.shape[1] != other.shape[0]:
            raise ValueError("The number of columns of the first matrix should be equal to the number of rows of the second matrix")

        result = [[sum(self.elements[i][k] * other.elements[k][j] for k in range(self.num_cols)) for j in range(other.num_cols)] for i in range(self.num_rows)]
        return Matrix(result)