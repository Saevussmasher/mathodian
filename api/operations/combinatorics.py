from models.parameters import ScalarParameter
from api.operation_registry import registry
import math

class CombinatoricsOperation:
    operation_id = "combinatorics"
    name = "Combinatorics Calculator"
    description = "Solves the four basic combinatorial problems: permutations/combinations with/without repetition."

    @classmethod
    def parameters(cls):
        return [
            ScalarParameter("n", "Number of Elements (n)", dtype="int"),
            ScalarParameter("k", "Number of Choices (k)", dtype="int"),
            # Problem type: 1=perm no rep, 2=perm rep, 3=comb no rep, 4=comb rep
            ScalarParameter("problem_type", "Problem Type (1=Permutations w/o rep, 2=Permutations w/ rep, 3=Combinations w/o rep, 4=Combinations w/ rep)", dtype="int"),
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
        n = int(params["n"])
        k = int(params["k"])
        pt = int(params["problem_type"])
        if n < 0 or k < 0:
            raise ValueError("n and k must be non-negative integers.")
        if pt == 1:
            # Permutations without repetition: n! / (n-k)!
            if k > n:
                raise ValueError("k cannot be greater than n for permutations without repetition.")
            result = math.factorial(n) // math.factorial(n - k)
            desc = "Permutations without repetition"
        elif pt == 2:
            # Permutations with repetition: n^k
            result = n ** k
            desc = "Permutations with repetition"
        elif pt == 3:
            # Combinations without repetition: n! / (k! * (n-k)!)
            if k > n:
                raise ValueError("k cannot be greater than n for combinations without repetition.")
            result = math.comb(n, k)
            desc = "Combinations without repetition"
        elif pt == 4:
            # Combinations with repetition: (n+k-1)! / (k! * (n-1)!)
            result = math.comb(n + k - 1, k)
            desc = "Combinations with repetition"
        else:
            raise ValueError("Invalid problem type.")
        return {
            "problem_type": desc,
            "n": n,
            "k": k,
            "result": result
        }

# Register operation
registry.register(CombinatoricsOperation)