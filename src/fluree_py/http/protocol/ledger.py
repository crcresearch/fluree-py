from typing import Protocol

from fluree_py.http.protocol.endpoint import (
    CreateBuilder,
    HistoryBuilder,
    QueryBuilder,
    TransactionBuilder,
)


class SupportsLedgerOperations(Protocol):
    """Protocol defining core ledger operations."""

    def create(self) -> CreateBuilder: ...
    def transaction(self) -> TransactionBuilder: ...
    def query(self) -> QueryBuilder: ...
    def history(self) -> HistoryBuilder: ...
