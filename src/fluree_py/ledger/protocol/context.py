from typing import Protocol, Self

from fluree_py.types import JsonObject


class SupportsContext(Protocol):
    def with_context(self, context: JsonObject) -> Self: ...
