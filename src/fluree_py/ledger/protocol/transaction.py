from typing import Protocol, Self

from fluree_py.ledger.protocol.base import BaseBuilder, BaseReadyToCommit
from fluree_py.ledger.protocol.where import SupportsWhere
from fluree_py.query.where.types import WhereClause
from fluree_py.types import JsonArray, JsonObject


class TransactionBuilder(BaseBuilder, Protocol):
    """Protocol for transaction builders."""

    def with_insert(
        self, data: JsonObject | JsonArray
    ) -> "TransactionReadyToCommit": ...
    def with_delete(self, data: JsonObject | JsonArray) -> "TransactionReadyToCommit": ...


class TransactionReadyToCommit(BaseBuilder, BaseReadyToCommit, SupportsWhere, Protocol):
    """Protocol for transaction builders that are ready to commit."""

    def with_insert(self, data: JsonObject | JsonArray) -> Self: ...
    def with_delete(self, data: JsonObject | JsonArray) -> Self: ...
