from typing import Protocol, Self

from fluree_py.http.protocol.endpoint.base import BaseBuilder, BaseReadyToCommit
from fluree_py.types.query.where import WhereClause
from fluree_py.types.common import JsonArray, JsonObject


class TransactionBuilder(BaseBuilder, Protocol):
    """Protocol for transaction builders."""

    def with_insert(
        self, data: JsonObject | JsonArray
    ) -> "TransactionReadyToCommit": ...
    def with_delete(self, data: JsonObject | JsonArray) -> "TransactionReadyToCommit": ...
    def with_where(self, clause: WhereClause) -> Self: ...


class TransactionReadyToCommit(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for transaction builders that are ready to commit."""

    def with_insert(self, data: JsonObject | JsonArray) -> Self: ...
    def with_delete(self, data: JsonObject | JsonArray) -> Self: ...
    def with_where(self, clause: WhereClause) -> Self: ...
