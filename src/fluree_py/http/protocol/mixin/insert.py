from typing import Generic, Protocol, TypeVar

from fluree_py.types.common import JsonArray, JsonObject


class HasInsertData(Protocol):
    """Protocol for objects that have insert data."""

    data: JsonObject | JsonArray | None


T = TypeVar("T", bound="HasInsertData", covariant=True)


class SupportsInsert(Generic[T], Protocol):
    """Protocol for objects that support insert operations."""

    data: JsonObject | JsonArray | None

    def with_insert(self, data: JsonObject | JsonArray) -> T: ...
