import importlib
import pkgutil
from typing import Dict, Type

class OperationRegistry:
    def __init__(self):
        self.operations: Dict[str, Type] = {}

    def register(self, operation_cls):
        op_id = operation_cls.operation_id
        if op_id in self.operations:
            raise ValueError(f"Duplicate operation_id: {op_id}")
        self.operations[op_id] = operation_cls

    def get_operation(self, op_id):
        return self.operations.get(op_id)

    def list_operations(self):
        return [op_cls.metadata() for op_cls in self.operations.values()]

    def load_operations(self, package):
        # Auto-import all modules in the operations package
        for _, modname, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package.__name__}.{modname}")
            # Each module must call registry.register() for its operation class

# Singleton registry
registry = OperationRegistry()