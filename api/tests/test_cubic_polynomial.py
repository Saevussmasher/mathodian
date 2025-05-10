import pytest
import numpy as np
from api.operations.cubic_polynomial import CubicPolynomialOperation

class TestCubicPolynomialOperation:
    def test_cubic_polynomial_valid_roots(self):
        params = {
            "a": 1,
            "b": -6,
            "c": 11,
            "d": -6
        }
        expected_roots = [
            {"type": "real", "value": 1.0},
            {"type": "real", "value": 2.0},
            {"type": "real", "value": 3.0}
        ]
        result = CubicPolynomialOperation.calculate(params)
        assert result["roots"] == expected_roots