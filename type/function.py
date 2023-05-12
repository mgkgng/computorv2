class Function:
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

    def __add__(self):
        raise TypeError("Cannot add to a function")

    def __radd__(self):
        raise TypeError("Cannot add to a function")

    def __sub__(self):
        raise TypeError("Cannot subtract from a function")

    def __rsub__(self):
        raise TypeError("Cannot subtract from a function")

    def __mul__(self):
        raise TypeError("Cannot multiply a function")

    def __rmul__(self):
        raise TypeError("Cannot multiply a function")

    def __truediv__(self):
        raise TypeError("Cannot divide a function")

    def __rtruediv__(self):
        raise TypeError("Cannot divide a function")

    def __pow__(self):
        raise TypeError("Cannot raise a function to a power")

    def __rpow__(self):
        raise TypeError("Cannot raise a function to a power")

    def __mod__(self):
        raise TypeError("Cannot mod a function")

    def __rmod__(self):
        raise TypeError("Cannot mod a function")