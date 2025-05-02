from models.parameters import MatrixParameter, VectorParameter
from api.operation_registry import registry
import numpy as np

class LinearSystemOperation:
    operation_id = "linear_system"
    name = "Linear Equation System Solver"
    description = "Solves a linear system Ax = b. Handles unique, infinite, or no solutions."

    @classmethod
    def parameters(cls):
        return [
            MatrixParameter("A", "Coefficient Matrix (A)", dtype="float"),
            VectorParameter("b", "Right-hand Side Vector (b)", dtype="float"),
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
        A = np.array(params["A"], dtype=float)
        b = np.array(params["b"], dtype=float)
        m, n = A.shape
        if b.shape[0] != m:
            raise ValueError("Dimension mismatch between A and b.")
        # Use numpy.linalg.lstsq for general solution
        x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        # Check for solution type
        if rank < n:
            # Infinite solutions or no solution
            # Check if b is in the column space of A
            if np.allclose(A @ x, b):
                return {
                    "solution_type": "infinite",
                    "particular_solution": x.tolist(),
                    "message": "Infinite solutions exist. One particular solution is shown."
                }
            else:
                return {
                    "solution_type": "none",
                    "message": "No solution exists for this system."
                }
        else:
            # Unique solution
            return {
                "solution_type": "unique",
                "solution": x.tolist(),
                "message": "Unique solution found."
            }

# Register operation
registry.register(LinearSystemOperation)