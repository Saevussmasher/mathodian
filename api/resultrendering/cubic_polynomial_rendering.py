from api.result_rendering_registry import rendering_registry

class CubicPolynomialRendering:
    operation_id = "cubic_polynomial"

    @classmethod
    def metadata(cls):
        return {
            "operation_id": cls.operation_id,
            "name": "Cubic Polynomial Result Rendering",
            "description": "Renders the roots of the cubic polynomial."
        }

    @classmethod
    def render(cls, result):
        # Render only the roots of the cubic polynomial with HTML line breaks
        rendered_result = "Roots:<br>"
        for root in result["roots"]:
            if root["type"] == "real":
                rendered_result += f"Real Root: {root['value']}<br>"
            else:
                rendered_result += f"Complex Root: {root['value'][0]} + {root['value'][1]}i<br>"
        return rendered_result

# Register rendering
rendering_registry.register(CubicPolynomialRendering)
