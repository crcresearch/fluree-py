"""Utility functions for resolving generic type parameters in mixins."""

import sys
from typing import Any, ForwardRef


class NonGenericBaseClassError(TypeError):
    """Exception raised when a base class is not generic."""

    def __init__(self, base_name: str) -> None:
        """Initialize the error with a fixed message."""
        super().__init__(f"Base class {base_name} does not have a generic argument")

class TypeResolutionError(TypeError):
    """Exception raised when a type cannot be resolved."""

    def __init__(self, type_arg: Any) -> None:  # noqa: ANN401
        """Initialize the error with a fixed message."""
        super().__init__(f"Unable to resolve type argument {type_arg}")

def find_base_class(cls: type[Any], base_name: str) -> type[Any]:
    """Locate a base class by name in the class's original bases."""
    for base in cls.__orig_bases__:
        if base.__name__ == base_name:
            return base
    return cls

def resolve_base_class_reference(cls: type[Any], base_name: str) -> type[Any]:
    """
    Resolve the type parameter from a generic base class.

    Exceptions:
        NonGenericBaseClassError: If the base class is not generic.
        TypeResolutionError: If the type cannot be resolved.
    """
    base_class = find_base_class(cls, base_name)

    if not hasattr(base_class, "__args__"):
        return cls

    type_arg = base_class.__args__[0]
    if not type_arg:
        raise NonGenericBaseClassError(base_name)

    if not isinstance(type_arg, ForwardRef):
        return type_arg

    if sys.version_info < (3, 13):
        resolved_type = type_arg._evaluate( # noqa: SLF001
            sys.modules[cls.__module__].__dict__,
            locals(),
            recursive_guard=frozenset(),
        )
    else:
        resolved_type = type_arg._evaluate( # noqa: SLF001
            sys.modules[cls.__module__].__dict__,
            locals(),
            type_params=(),
            recursive_guard=frozenset(),
        )

    if not resolved_type:
        raise TypeResolutionError(type_arg)

    return resolved_type
