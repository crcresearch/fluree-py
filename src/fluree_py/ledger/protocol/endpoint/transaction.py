from typing import Protocol, Self

from fluree_py.ledger.protocol.mixin import SupportsContext
from fluree_py.types import JsonArray, JsonObject


class TransactionBuilder(SupportsContext, Protocol):
    """Protocol for transaction builders."""

    def with_delete(
        self, data: JsonObject | JsonArray
    ) -> "TransactionReadyToCommit": ...


class TransactionReadyToCommit(SupportsContext, Protocol):
    """Protocol for transaction builders that are ready to commit."""

    def with_delete(self, data: JsonObject | JsonArray) -> Self: ...
