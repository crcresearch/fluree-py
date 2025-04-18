"""Utility functions for resolving generic type parameters in mixins."""

import inspect
import sys
from typing import ForwardRef, TypeVar, get_origin

from fluree_py.logging import logger


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

        # Log the available classes in the local and global namespaces
        logger.info(
            "forwardref_resolution_attempt",
            frame=frame.f_code.co_name,
            local_classes=[k for k, v in local_namespace.items() if isinstance(v, type)],
            global_classes=[k for k, v in global_namespace.items() if isinstance(v, type)],
            forwardref=str(type_arg),
        )

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


def _get_typevar_mapping(cls):
    """
    Walk the MRO and accumulate a mapping of typevars to their concrete types.
    Returns a dict mapping TypeVar to its resolved value.
    """
    mapping = {}
    mro = inspect.getmro(cls)
    for current_cls in mro:
        if hasattr(current_cls, "__orig_bases__"):
            for base in current_cls.__orig_bases__:
                origin = get_origin(base)
                if origin is None:
                    continue
                params = getattr(origin, "__parameters__", ())
                args = getattr(base, "__args__", ())
                # Log the mapping process
                logger.info(
                    "typevar_mapping_step",
                    current_cls=current_cls.__name__,
                    base=str(base),
                    origin=str(origin),
                    params=[getattr(p, "__name__", str(p)) for p in params],
                    args=[str(a) for a in args],
                    mapping={getattr(k, "__name__", str(k)): str(v) for k, v in mapping.items()},
                )
                for param, arg in zip(params, args, strict=False):
                    # Substitute any typevars in arg using the current map
                    resolved_arg = mapping.get(arg, arg)
                    mapping[param] = resolved_arg
    return mapping


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
    logger.info("resolve_base_type_arg", cls=cls.__name__, base_name=base_name, arg_name=arg_name)
    # Find the target base in the MRO
    mro = inspect.getmro(cls)
    for current_cls in mro:
        if hasattr(current_cls, "__orig_bases__"):
            for base in current_cls.__orig_bases__:
                origin = get_origin(base)
                if origin is None:
                    continue
                if origin.__name__ == base_name or getattr(origin, "__name__", None) == base_name:
                    params = getattr(origin, "__parameters__", ())
                    args = getattr(base, "__args__", ())
                    # Build the typevar mapping up to this point
                    mapping = _get_typevar_mapping(cls)
                    for idx, param in enumerate(params):
                        if param.__name__ == arg_name:
                            resolved = mapping.get(param, param)
                            # If still a TypeVar, try to resolve recursively
                            while (
                                isinstance(resolved, TypeVar) and resolved in mapping and mapping[resolved] != resolved
                            ):
                                resolved = mapping[resolved]
                            if isinstance(resolved, TypeVar):
                                raise TypeResolutionError(resolved)
                            if not isinstance(resolved, type):
                                raise TypeResolutionError(resolved)
                            return [resolved]
    return []
