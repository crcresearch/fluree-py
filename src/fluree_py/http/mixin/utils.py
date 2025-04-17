"""Utility functions for resolving generic type parameters in mixins."""

import sys
from typing import Any, ForwardRef

from fluree_py.logging import logger


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
    logger.debug("resolve_base_class_reference", class_name=cls.__name__, base_name=base_name)
    base_class = find_base_class(cls, base_name)
    logger.debug("find_base_class", base_class=base_class.__name__)

    if not hasattr(base_class, "__args__"):
        logger.debug("no_generic_args", returning=cls.__name__)
        return cls

    type_arg = base_class.__args__[0]
    logger.debug("type_arg", type_arg=repr(type_arg))
    if not type_arg:
        logger.debug("no_type_arg", base_name=base_name)
        raise NonGenericBaseClassError(base_name)

    if not isinstance(type_arg, ForwardRef):
        logger.debug("type_arg_not_forward_ref", returning=repr(type_arg))
        return type_arg

    if sys.version_info < (3, 13):
        resolved_type = type_arg._evaluate(  # noqa: SLF001
            sys.modules[cls.__module__].__dict__,
            locals(),
            recursive_guard=frozenset(),
        )
    else:
        resolved_type = type_arg._evaluate(  # noqa: SLF001
            sys.modules[cls.__module__].__dict__,
            locals(),
            type_params=(),
            recursive_guard=frozenset(),
        )

    logger.debug("forward_ref_resolved", resolved_type=resolved_type)
    if not resolved_type:
        logger.debug("forward_ref_resolution_failed", type_arg=repr(type_arg))
        raise TypeResolutionError(type_arg)

    logger.debug("returning_resolved_type", resolved_type=resolved_type.__name__)
    return resolved_type
