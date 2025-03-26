from typing import Any, Protocol

from fluree_py.http.protocol.mixin import SupportsCommit, SupportsContext, SupportsRequestCreation


class SupportsTransaction(Protocol):
    def transaction(self) -> "TransactionBuilder": ...


class TransactionBuilder(
    SupportsContext, SupportsRequestCreation, SupportsCommit, Protocol
):
    def with_insert(self, data: dict[str, Any]) -> "TransactionBuilder": ...
    def with_delete(self, data: dict[str, Any]) -> "TransactionBuilder": ...
    def with_where(self, clause: dict[str, Any]) -> "TransactionBuilder": ...
