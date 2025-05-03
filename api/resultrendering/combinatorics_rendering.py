from api.result_rendering_registry import rendering_registry

class CombinatoricsRendering:
    operation_id = "combinatorics"

    @classmethod
    def metadata(cls):
        return {
            "operation_id": cls.operation_id,
            "name": "Combinatorics Result Rendering",
            "description": "Renders the result of the combinatorics calculation."
        }

    @classmethod
    def render(cls, result):
        # Render only the combinatorial result
        rendered_result = f"Result: {result['result']}\n"
        return rendered_result

# Register rendering
rendering_registry.register(CombinatoricsRendering)