from typing import Dict
from .interface import VerificationMethod

# registry of method_name -> instance
_registry: Dict[str, VerificationMethod] = {}

def register_method(method: VerificationMethod):
    _registry[method.name] = method

def get_method(name: str) -> VerificationMethod | None:
    return _registry.get(name)

def list_methods() -> list[str]:
    return list(_registry.keys())
