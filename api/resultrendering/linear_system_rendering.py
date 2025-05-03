from api.result_rendering_registry import rendering_registry

class LinearSystemRendering:
    operation_id = "linear_system"

    @classmethod
    def metadata(cls):
        return {
            "operation_id": cls.operation_id,
            "name": "Linear System Result Rendering",
            "description": "Renders the solution of the linear equation system."
        }

    @classmethod
    def render(cls, result):
        # Render only the solution of the linear system
        if result["solution_type"] == "unique":
            rendered_result = f"Unique Solution: {result['solution']}\n"
        elif result["solution_type"] == "infinite":
            rendered_result = f"Infinite Solutions: One particular solution is {result['particular_solution']}\n"
        else:
            rendered_result = "No solution exists.\n"
        return rendered_result

# Register rendering
rendering_registry.register(LinearSystemRendering)