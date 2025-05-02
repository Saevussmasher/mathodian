from models.parameters import ScalarParameter
from api.operation_registry import registry
import numpy as np

class CubicPolynomialOperation:
    operation_id = "cubic_polynomial"
    name = "Cubic Polynomial Solver"
    description = "Finds the real and complex roots of a cubic polynomial: ax³ + bx² + cx + d = 0"

    @classmethod
    def parameters(cls):
        return [
            ScalarParameter("a", "Coefficient a"),
            ScalarParameter("b", "Coefficient b"),
            ScalarParameter("c", "Coefficient c"),
            ScalarParameter("d", "Coefficient d"),
        ]

    @classmethod
    def metadata(cls):
        return {
            "operation_id": cls.operation_id,
            "name": cls.name,
            "description": cls.description,
            "parameters": [p.to_dict() for p in cls.parameters()]
        }

    @classmethod
    def calculate(cls, params):
        a = float(params["a"])
        b = float(params["b"])
        c = float(params["c"])
        d = float(params["d"])
        if a == 0:
            raise ValueError("Coefficient a must not be zero for a cubic equation.")
        coeffs = [a, b, c, d]
        roots = np.roots(coeffs)
        result = []
        for r in roots:
            if abs(r.imag) < 1e-10:
                result.append({"type": "real", "value": r.real})
            else:
                result.append({"type": "complex", "value": [r.real, r.imag]})
        return {"roots": result}

# Register operation
registry.register(CubicPolynomialOperation)