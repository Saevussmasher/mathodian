import pytest
import numpy as np
from api.operations.linear_system import LinearSystemOperation

class TestLinearSystemOperation:
    def test_unique_solution(self):
        params = {
            "A": [[3, 2], [1, 2]],
            "b": [5, 5]
        }
        result = LinearSystemOperation.calculate(params)
        expected_solution = np.linalg.solve(np.array(params["A"]), np.array(params["b"])).tolist()
        assert result["solution_type"] == "unique"
        assert result["solution"] == expected_solution
        assert result["message"] == "Unique solution found."