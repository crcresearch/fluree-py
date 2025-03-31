from typing import Generic, Protocol, TypeVar

from fluree_py.types import JsonArray, JsonObject


class HasInsertData(Protocol):
    data: JsonObject | JsonArray | None


T = TypeVar("T", bound="HasInsertData", covariant=True)


class SupportsInsert(Generic[T], Protocol):
    data: JsonObject | JsonArray | None

    def with_insert(self, data: JsonObject | JsonArray) -> T: ...
