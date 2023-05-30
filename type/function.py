class Function:
    def __init__(self, name, arg, polynomials):
        self.name = name
        self.arg = arg
        self.polynomials = polynomials

    def __call__(self, x):
        return self.polynomials(x)

    def __str__(self):
        return f"{self.name}({self.arg}) = {self.polynomials.__str__()}"

    def __add__(self, other):
        if isinstance(self.arg, str):
            raise TypeError("Cannot add to a function declaration")
        return self.__call__(self.arg) + other

    def __radd__(self, other):
        if isinstance(self.arg, str):
            raise TypeError("Cannot add to a function declaration")
        return self.__call__(self.arg) + other