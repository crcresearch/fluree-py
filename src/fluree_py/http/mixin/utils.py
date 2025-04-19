"""
Utility functions for resolving generic type parameters in mixins.

This module provides helpers for dynamic builder patterns, especially for dataclasses and mixins that use immutable state transitions. The main utility is `make_setter`, which generates setter methods that return new instances (not in-place mutation), optionally transitioning to a new dataclass type for builder chaining.
"""

from collections.abc import Callable
from dataclasses import replace
from typing import Any, ClassVar, Protocol, TypeVar


class DataclassLike(Protocol):
    """Protocol for dataclass like types."""

    __dataclass_fields__: ClassVar[dict[str, Any]]


S = TypeVar("S", bound=DataclassLike)
U = TypeVar("U", bound=DataclassLike)


def make_setter(
    name: str,
    field: str,
    next_cls: type[U] | None = None,
) -> Callable[..., Any]:
    """Dynamically create a setter method for a dataclass field that returns a new instance of the current class (or `next_cls` when provided)."""

    def setter(self: S, value: object) -> S | U:
        updated = replace(self, **{field: value})
        if next_cls is None:
            return updated

        payload = {k: getattr(updated, k) for k in next_cls.__dataclass_fields__ if hasattr(updated, k)}
        return next_cls(**payload)

    setter.__name__ = name
    return setter
