class Matrix:
    def __init__(self, elements):
        if not elements or not isinstance(elements, list):
            raise ValueError("Matrix elements should be a list of lists")
        
        row_length = len(elements[0])
        for row in elements:
            if len(row) != row_length:
                raise ValueError("All rows should have the same length")
        
        self.elements = elements
        self.num_rows = len(elements)
        self.num_cols = row_length

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.elements])

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Both operands should be of Matrix type")
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices should have the same dimensions")

        result = [[self.elements[i][j] + other.elements[i][j] for j in range(self.num_cols)] for i in range(self.num_rows)]
        return Matrix(result)

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Both operands should be of Matrix type")
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices should have the same dimensions")

        result = [[self.elements[i][j] - other.elements[i][j] for j in range(self.num_cols)] for i in range(self.num_rows)]
        return Matrix(result)

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Both operands should be of Matrix type")
        if self.num_cols != other.num_rows:
            raise ValueError("The number of columns of the first matrix should be equal to the number of rows of the second matrix")

        result = [[sum(self.elements[i][k] * other.elements[k][j] for k in range(self.num_cols)) for j in range(other.num_cols)] for i in range(self.num_rows)]
        return Matrix(result)

    def transpose(self):
        transposed_elements = [[self.elements[j][i] for j in range(self.num_rows)] for i in range(self.num_cols)]
        return Matrix(transposed_elements)

    @staticmethod
    def identity(n):
        elements = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return Matrix(elements)