from typing import Protocol

from fluree_py.ledger.protocol.endpoint import (
    CreateBuilder,
    HistoryBuilder,
    QueryBuilder,
    TransactionBuilder,
)


class SupportsLedgerOperations(Protocol):
    def create(self) -> CreateBuilder: ...
    def transaction(self) -> TransactionBuilder: ...
    def query(self) -> QueryBuilder: ...
    def history(self) -> HistoryBuilder: ...
