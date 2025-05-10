import pytest
import numpy as np

from api.operations.linear_system import LinearSystemOperation

class TestLinearSystemOperation:
    def test_unique_solution_returns_correct_result(self):
        # A is a 2x2 invertible matrix, b is a vector
        A = [[2, 1], [1, 3]]
        b = [8, 13]
        params = {"A": A, "b": b}
        result = LinearSystemOperation.calculate(params)
        assert result["solution_type"] == "unique"
        # The expected solution is x = [3, 2]
        expected_solution = np.linalg.solve(np.array(A), np.array(b)).tolist()
        np.testing.assert_allclose(result["solution"], expected_solution, rtol=1e-7, atol=1e-7)
        assert "Unique solution found." in result["message"]