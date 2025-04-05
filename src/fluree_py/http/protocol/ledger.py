"""Protocols for interacting with a Fluree ledger."""

from typing import Protocol

from fluree_py.http.protocol.endpoint import (
    CreateBuilder,
    HistoryBuilder,
    QueryBuilder,
    TransactionBuilder,
)


class SupportsLedgerOperations(Protocol):
    """Protocol defining core ledger operations."""

    def create(self) -> CreateBuilder:
        """Create a new builder for create operations."""
        ...

    def transaction(self) -> TransactionBuilder:
        """Create a new builder for transaction operations."""
        ...

    def query(self) -> QueryBuilder:
        """Create a new builder for query operations."""
        ...

    def history(self) -> HistoryBuilder:
        """Create a new builder for history operations."""
        ...
