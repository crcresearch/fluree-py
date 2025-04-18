"""Utility functions for resolving generic type parameters in mixins."""

import inspect
import sys
from typing import ForwardRef, TypeVar, get_origin


class InvalidArgumentCountError(TypeError):
    """Exception raised when a requested type has an invalid number of generic arguments."""

    def __init__(self, type_arg: str, base_name: str, resolved_type: list[type]) -> None:
        """Initialize the error with a fixed message."""
        super().__init__(f"Invalid number of generic arguments for {type_arg} in {base_name}: {resolved_type}")


class NonGenericBaseClassError(TypeError):
    """Exception raised when a base class is not generic."""

    def __init__(self, base_name: str) -> None:
        """Initialize the error with a fixed message."""
        super().__init__(f"Base class {base_name} does not have a generic argument")


class TypeResolutionError(TypeError):
    """Exception raised when a type cannot be resolved."""

    def __init__(self, type_arg: object) -> None:
        """Initialize the error with a fixed message."""
        super().__init__(f"Unable to resolve type argument {type_arg}")


class ForwardRefResolutionError(TypeError):
    """Exception raised when a ForwardRef cannot be resolved with detailed context."""

    def __init__(self, type_arg: ForwardRef | type, cls: type) -> None:
        """Initialize the error with a fixed message."""
        msg = (
            f"Could not resolve forward reference {type_arg!r} in any caller's local scope "
            f"for class '{cls.__name__}' in module '{cls.__module__}'. "
            f"ForwardRef details: {getattr(type_arg, '__forward_arg__', repr(type_arg))}"
        )
        super().__init__(msg)


def collect_types_for_base(cls: type, base_name: str) -> list[type]:
    """
    Locate and return the type arguments for a base class with the given name in the class's original bases.

    Args:
        cls: The class whose base's type arguments are to be collected.
        base_name: The name of the base class to search for.

    Returns:
        A list of type arguments for the specified base class, or an empty list if not found.

    """
    if not hasattr(cls, "__orig_bases__"):
        return []

    for base in cls.__orig_bases__:
        if base.__name__ == base_name:
            return list(base.__args__)

        if hasattr(base, "__origin__"):
            o_types = collect_types_for_base(get_origin(base), base_name)
            if o_types is not None:
                return list(base.__args__)

    return []


def evaluate_forward_ref(
    type_arg: ForwardRef | type,
    global_namespace: dict[str, object],
    local_namespace: dict[str, object],
) -> type | None:
    """
    Evaluate a ForwardRef type argument in the given namespaces.

    Args:
        type_arg: The type argument to evaluate (may be a ForwardRef).
        global_namespace: The global namespace for evaluation.
        local_namespace: The local namespace for evaluation.

    Returns:
        The resolved type if successful, or None if evaluation fails.

    """
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


def resolve_type_arg(cls: type, type_arg: ForwardRef | type) -> type:
    """
    Resolve a type argument, evaluating ForwardRefs if necessary, using the class's module and caller's local scope.

    Args:
        cls: The class context for resolution.
        type_arg: The type argument to resolve (may be a ForwardRef).

    Returns:
        The resolved type.

    Raises:
        TypeResolutionError: If the type argument cannot be resolved in any caller's local scope.

    """
    if not isinstance(type_arg, ForwardRef):
        return type_arg

    global_namespace = sys.modules[cls.__module__].__dict__

    # Climb up the stack frames, starting from our caller
    frame = inspect.currentframe()
    if frame is not None:
        frame = frame.f_back
    while frame is not None:
        local_namespace = {**frame.f_locals}

        maybe_resolved = evaluate_forward_ref(type_arg, global_namespace, local_namespace)
        if maybe_resolved is not None:
            # If it resolved properly, return it
            return maybe_resolved

        # Otherwise, go up one more frame
        frame = frame.f_back

    # If we exhaust all frames, we fail
    raise ForwardRefResolutionError(type_arg, cls)


def resolve_base_type_args(cls: type, base_name: str | type) -> list[type]:
    """
    Resolve all concrete type arguments for a given generic base class in the inheritance chain.

    Args:
        cls: The class whose base's type arguments are to be resolved.
        base_name: The name (str) or type of the base class.

    Returns:
        A list of resolved type arguments for the specified base class.

    """
    # Normalize base_name to a string
    base_name_str = base_name.__name__ if isinstance(base_name, type) else base_name
    return [resolve_type_arg(cls, type_arg) for type_arg in collect_types_for_base(cls, base_name_str)]


def resolve_base_type_arg(
    cls: type,
    base_name: str,
    argument: TypeVar | str,
) -> list[type]:
    """
    Resolve the concrete type for a specific type variable of a generic base class in the inheritance chain.

    Args:
        cls: The class whose base's type argument is to be resolved.
        base_name: The name of the base class.
        argument: The TypeVar or its name to resolve.

    Returns:
        A list containing the resolved type for the specified type variable, or an empty list if not found.

    """
    # Normalize argument to a name
    arg_name = argument.__name__ if isinstance(argument, TypeVar) else argument
    if not hasattr(cls, "__orig_bases__"):
        return []

    for base in cls.__orig_bases__:
        if base.__name__ == base_name:
            params = getattr(base, "__parameters__", None)
            args = getattr(base, "__args__", None)
            # If not found, try the origin
            if (params is None or not any(p.__name__ == arg_name for p in params)) and hasattr(base, "__origin__"):
                origin = get_origin(base)
                params = getattr(origin, "__parameters__", None)
            if params is not None and args is not None:
                for idx, param in enumerate(params):
                    if param.__name__ == arg_name:
                        return [resolve_type_arg(cls, args[idx])]
            return [resolve_type_arg(cls, type_arg) for type_arg in args] if args else []
        if hasattr(base, "__origin__"):
            result = resolve_base_type_arg(get_origin(base), base_name, argument)
            if result:
                return result
    return []
