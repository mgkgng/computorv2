class Polynomial:
    def __init__(self, coefficients, variable):
        if not coefficients or not isinstance(coefficients, list):
            raise ValueError("Polynomial coefficients should be a list")
        
        # Remove leading zeros, if any
        while len(coefficients) > 1 and coefficients[0] == 0:
            coefficients.pop(0)

        self.coefficients = coefficients

    def __pos__(self):
        return self

    def __neg__(self):
        pass


    def __str__(self):
        if len(self.coefficients) == 1 and self.coefficients[0] == 0:
            return "0"
        
        terms = []
        for i, coef in enumerate(reversed(self.coefficients)):
            if coef == 0:
                continue
            
            term = str(coef) if i == 0 or abs(coef) != 1 else "-" if coef < 0 else ""
            if i > 0:
                term += "x"
                if i > 1:
                    term += f"^{i}"
            
            terms.append(term)
        
        return " + ".join(terms).replace("+ -", "- ")

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Both operands should be of Polynomial type")

        coeffs1 = self.coefficients[::-1]
        coeffs2 = other.coefficients[::-1]
        min_len = min(len(coeffs1), len(coeffs2))
        max_len = max(len(coeffs1), len(coeffs2))

        result_coeffs = [coeffs1[i] + coeffs2[i] for i in range(min_len)] + \
                        [coeffs1[i] for i in range(min_len, max_len)] + \
                        [coeffs2[i] for i in range(min_len, max_len)]

        return Polynomial(result_coeffs[::-1])

    def __sub__(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Both operands should be of Polynomial type")

        coeffs1 = self.coefficients[::-1]
        coeffs2 = other.coefficients[::-1]
        min_len = min(len(coeffs1), len(coeffs2))
        max_len = max(len(coeffs1), len(coeffs2))

        result_coeffs = [coeffs1[i] - coeffs2[i] for i in range(min_len)] + \
                        [coeffs1[i] for i in range(min_len, max_len)] + \
                        [-coeffs2[i] for i in range(min_len, max_len)]

        return Polynomial(result_coeffs[::-1])

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Both operands should be of Polynomial type")

        coeffs1 = self.coefficients[::-1]
        coeffs2 = other.coefficients[::-1]
        result_coeffs = [0] * (len(coeffs1) + len(coeffs2) - 1)

        for i, coef1 in enumerate(coeffs1):
            for j, coef2 in enumerate(coeffs2):
                result_coeffs[i + j] += coef1 * coef2

        return Polynomial(result_coeffs[::-1])

    def __call__(self, x):
        return sum(coef * (x ** i) for i, coef in enumerate(reversed(self.coefficients)))

    def degree(self):
        return len(self.coefficients) - 1