"""
Utility functions for resolving generic type parameters in mixins.

This module provides helpers for dynamic builder patterns, especially for dataclasses and mixins that use immutable state transitions. The main utility is `make_setter`, which generates setter methods that return new instances (not in-place mutation), optionally transitioning to a new dataclass type for builder chaining.
"""

from dataclasses import replace
from typing import Any


def make_setter(name: str, field: str, next_cls: type | None = None):  # noqa: ANN201
    """
    Dynamically create a setter method for a dataclass field that returns a new instance.

    Args:
        name (str): The name to assign to the generated setter function.
        field (str): The dataclass field to set.
        next_cls (type[U] | None): If provided, the setter will return an instance of this class,
            passing only the fields declared in `next_cls`. If None, returns an updated instance of the current class.

    Returns:
        Callable[[T, Any], T | U]: A setter function that takes (self, value) and returns a new instance.

    """

    def setter(self, value: Any):  # noqa: ANN001, ANN202, ANN401
        updated = replace(self, **{field: value})  # 🔄 NEW instance
        if next_cls is None:  # stay in builder
            return updated
        # hand only the attributes declared in `next_cls`
        payload = {k: getattr(updated, k) for k in next_cls.__dataclass_fields__ if hasattr(updated, k)}
        return next_cls(**payload)  # → new state

    setter.__name__ = name
    return setter
