from typing import Any, List, Dict

class Parameter:
    def __init__(self, name: str, label: str, param_type: str, **kwargs):
        self.name = name
        self.label = label
        self.type = param_type
        self.extra = kwargs

    def to_dict(self):
        return {
            "name": self.name,
            "label": self.label,
            "type": self.type,
            **self.extra
        }

    def validate(self, value: Any):
        raise NotImplementedError

class ScalarParameter(Parameter):
    def __init__(self, name, label, dtype="float", **kwargs):
        super().__init__(name, label, "scalar", dtype=dtype, **kwargs)

    def validate(self, value):
        try:
            if self.extra.get("dtype") == "int":
                return int(value)
            else:
                return float(value)
        except Exception:
            raise ValueError(f"Invalid scalar value for {self.name}")

class VectorParameter(Parameter):
    def __init__(self, name, label, length=None, dtype="float", **kwargs):
        super().__init__(name, label, "vector", length=length, dtype=dtype, **kwargs)

    def validate(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected list for {self.name}")
        if self.extra.get("length") and len(value) != self.extra["length"]:
            raise ValueError(f"Expected vector of length {self.extra['length']} for {self.name}")
        dtype = self.extra.get("dtype", "float")
        if dtype == "int":
            return [int(x) for x in value]
        else:
            return [float(x) for x in value]

class MatrixParameter(Parameter):
    def __init__(self, name, label, rows=None, cols=None, dtype="float", **kwargs):
        super().__init__(name, label, "matrix", rows=rows, cols=cols, dtype=dtype, **kwargs)

    def validate(self, value):
        if not isinstance(value, list) or not all(isinstance(row, list) for row in value):
            raise ValueError(f"Expected matrix (list of lists) for {self.name}")
        if self.extra.get("rows") and len(value) != self.extra["rows"]:
            raise ValueError(f"Expected {self.extra['rows']} rows for {self.name}")
        if self.extra.get("cols") and any(len(row) != self.extra["cols"] for row in value):
            raise ValueError(f"Expected {self.extra['cols']} columns for {self.name}")
        dtype = self.extra.get("dtype", "float")
        if dtype == "int":
            return [[int(x) for x in row] for row in value]
        else:
            return [[float(x) for x in row] for row in value]