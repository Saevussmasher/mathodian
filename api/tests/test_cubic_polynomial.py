import pytest
from api.operations.cubic_polynomial import CubicPolynomialOperation

class TestCubicPolynomialOperation:
    def test_cubic_polynomial_three_real_roots(self):
        # Equation: x^3 - 6x^2 + 11x - 6 = 0 has roots 1, 2, 3
        params = {"a": 1, "b": -6, "c": 11, "d": -6}
        result = CubicPolynomialOperation.calculate(params)
        roots = [r for r in result["roots"] if r["type"] == "real"]
        root_values = sorted([round(r["value"], 8) for r in roots])
        assert len(roots) == 3
        assert root_values == [1.0, 2.0, 3.0]
        # Ensure no complex roots
        assert all(r["type"] == "real" for r in result["roots"])