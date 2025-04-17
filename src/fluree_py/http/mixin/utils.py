"""Utility functions for resolving generic type parameters in mixins."""

import inspect
import sys
from typing import Any, ForwardRef, TypeVar, get_origin


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


def collect_types_for_base(cls: type[Any], base_name: str) -> list[type[Any]]:
    """Locate a base class by name in the class's original bases."""
    if not hasattr(cls, "__orig_bases__"):
        return []

    for base in cls.__orig_bases__:
        if base.__name__ == base_name:
            print("Base name matches")
            return list(base.__args__)

        if hasattr(base, "__origin__"):
            o_types = collect_types_for_base(get_origin(base), base_name)
            print("Origin types:", o_types)
            if o_types is not None:
                print("Origin name matches")
                return list(base.__args__)

    return []


def evaluate_forward_ref(
    type_arg: Any, global_namespace: dict[str, Any], local_namespace: dict[str, Any]
) -> type[Any] | None:
    try:
        if sys.version_info < (3, 13):
            return type_arg._evaluate(  # noqa: SLF001
                global_namespace,
                local_namespace,
                recursive_guard=frozenset(),
            )
        return type_arg._evaluate(  # noqa: SLF001
            global_namespace,
            local_namespace,
            type_params=(),
            recursive_guard=frozenset(),
        )
    except Exception:
        return None


def resolve_type_arg(cls: type[Any], type_arg: Any) -> type[Any]:  # noqa: ANN401
    if not isinstance(type_arg, ForwardRef):
        return type_arg

    global_namespace = sys.modules[cls.__module__].__dict__

    # Climb up the stack frames, starting from our caller
    frame = inspect.currentframe().f_back
    while frame is not None:
        local_namespace = {**frame.f_locals}

        maybe_resolved = evaluate_forward_ref(type_arg, global_namespace, local_namespace)
        if maybe_resolved is not None:
            # If it resolved properly, return it
            return maybe_resolved

        # Otherwise, go up one more frame
        frame = frame.f_back

    # If we exhaust all frames, we fail
    raise TypeResolutionError(f"Could not resolve forward reference {type_arg} in any caller's local scope")


def find_type_for_base(cls: type[Any], base_name: str) -> list[type[Any]]:
    """Locate a base class by name in the class's original bases."""
    return [resolve_type_arg(cls, type_arg) for type_arg in collect_types_for_base(cls, base_name)]


def find_type_for_base_arg(cls: type[Any], base_name: str, argument: TypeVar) -> list[type[Any]]:
    """Locate a base class by name in the class's original bases."""
    return [resolve_type_arg(cls, type_arg) for type_arg in collect_types_for_base(cls, base_name)]
