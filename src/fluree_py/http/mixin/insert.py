"""Mixin for handling data insertion operations in Fluree."""

from typing import Protocol, TypeVar

from fluree_py.types.common import JsonArray, JsonObject


# Protocol definitions for insert mixin
class HasInsertData(Protocol):
    """Protocol for objects that have insert data."""

    data: JsonObject | JsonArray | None


T_co = TypeVar("T_co", bound=HasInsertData, covariant=True)


class SupportsInsert(Protocol[T_co]):
    """Protocol for objects that support insert operations."""

    def with_insert(self, value: JsonObject | JsonArray) -> T_co:
        """Set the insert data for the operation."""
        ...
