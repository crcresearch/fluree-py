from typing import Any, Protocol

from fluree_py.ledger.protocol.base import BaseBuilder, BaseReadyToCommit


class TransactionBuilder(BaseBuilder, Protocol):
    """Protocol for transaction builders."""

    def with_insert(
        self, data: list[dict[str, Any]] | dict[str, Any]
    ) -> "TransactionReadyToCommit": ...
    def with_delete(self, data: dict[str, Any]) -> "TransactionReadyToCommit": ...
    def with_where(self, clause: dict[str, Any]) -> "TransactionBuilder": ...


class TransactionReadyToCommit(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for transaction builders that are ready to commit."""

    def with_insert(
        self, data: list[dict[str, Any]] | dict[str, Any]
    ) -> "TransactionReadyToCommit": ...
    def with_delete(self, data: dict[str, Any]) -> "TransactionReadyToCommit": ...
    def with_where(self, clause: dict[str, Any]) -> "TransactionReadyToCommit": ...
