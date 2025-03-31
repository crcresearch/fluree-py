"""Utility functions for resolving generic type parameters in mixins."""

import sys
from typing import Any, ForwardRef


def find_base_class(cls: type[Any], base_name: str) -> type[Any]:
    """Locates a base class by name in the class's original bases.

    Exceptions:
        TypeError: If the base class cannot be found.
    """
    for base in cls.__orig_bases__:
        if base.__name__ == base_name:
            return base
    return cls


def resolve_base_class_reference(cls: type[Any], base_name: str) -> type[Any]:
    """Resolves the type parameter from a generic base class.

    Exceptions:
        TypeError: If no type argument is found or if the type cannot be resolved.
    """
    base_class = find_base_class(cls, base_name)

    if not hasattr(base_class, "__args__"):
        return cls

    type_arg = base_class.__args__[0]
    if not type_arg:
        raise TypeError(f"No argument found for {base_name}")

    if not isinstance(type_arg, ForwardRef):
        return type_arg

    resolved_type = type_arg._evaluate(
        sys.modules[cls.__module__].__dict__,
        locals(),
        type_params=(),
        recursive_guard=frozenset(),
    )
    if not resolved_type:
        raise TypeError(f"Unable to resolve type argument {type_arg}")

    return resolved_type
