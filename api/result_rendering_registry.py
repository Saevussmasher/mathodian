import importlib
import pkgutil
from typing import Dict, Type

class ResultRenderingRegistry:
    def __init__(self):
        self.renderings: Dict[str, Type] = {}

    def register(self, rendering_cls):
        op_id = rendering_cls.operation_id
        if op_id in self.renderings:
            raise ValueError(f"Duplicate operation_id: {op_id}")
        self.renderings[op_id] = rendering_cls

    def get_rendering(self, op_id):
        return self.renderings.get(op_id)

    def list_renderings(self):
        return [rendering_cls.metadata() for rendering_cls in self.renderings.values()]

    def load_renderings(self, package):
        # Auto-import all modules in the renderings package
        for _, modname, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package.__name__}.{modname}")
            # Each module must call registry.register() for its rendering class

# Singleton registry
rendering_registry = ResultRenderingRegistry()