import pytest
from api.operations.combinatorics import CombinatoricsOperation

class TestCombinatoricsOperation:
    
    def test_permutations_without_repetition_valid(self):
        params = {"n": 5, "k": 3, "problem_type": 1}
        result = CombinatoricsOperation.calculate(params)
        assert result["result"] == 60
        assert result["problem_type"] == "Permutations without repetition"

    def test_permutations_with_repetition_valid(self):
        params = {"n": 5, "k": 3, "problem_type": 2}
        result = CombinatoricsOperation.calculate(params)
        assert result["result"] == 125
        assert result["problem_type"] == "Permutations with repetition"

    def test_combinations_without_repetition_valid(self):
        params = {"n": 5, "k": 3, "problem_type": 3}
        result = CombinatoricsOperation.calculate(params)
        assert result["result"] == 10
        assert result["problem_type"] == "Combinations without repetition"

    def test_permutations_without_repetition_k_greater_than_n(self):
        params = {"n": 3, "k": 5, "problem_type": 1}
        with pytest.raises(ValueError, match="k cannot be greater than n for permutations without repetition."):
            CombinatoricsOperation.calculate(params)

    def test_negative_n_or_k_values(self):
        params = {"n": -5, "k": 3, "problem_type": 1}
        with pytest.raises(ValueError, match="n and k must be non-negative integers."):
            CombinatoricsOperation.calculate(params)

    def test_invalid_problem_type(self):
        params = {"n": 5, "k": 3, "problem_type": 5}
        with pytest.raises(ValueError, match="Invalid problem type."):
            CombinatoricsOperation.calculate(params)