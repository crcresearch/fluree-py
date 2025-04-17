from dataclasses import dataclass
from typing import Protocol

from fluree_py.http.operations import (
    CreateBuilder,
    CreateBuilderImpl,
    HistoryBuilder,
    HistoryBuilderImpl,
    QueryBuilder,
    QueryBuilderImpl,
    TransactionBuilder,
    TransactionBuilderImpl,
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


@dataclass(frozen=True, kw_only=True)
class LedgerSelected:
    """Selected ledger for operations."""

    base_url: str
    ledger: str

    def create(self) -> CreateBuilder:
        """Create a new ledger."""
        return CreateBuilderImpl(endpoint=f"{self.base_url}/fluree/create", ledger=self.ledger)

    def transaction(self) -> TransactionBuilder:
        """Execute ledger transactions."""
        return TransactionBuilderImpl(endpoint=f"{self.base_url}/fluree/transact", ledger=self.ledger)

    def query(self) -> QueryBuilder:
        """Query the ledger."""
        return QueryBuilderImpl(endpoint=f"{self.base_url}/fluree/query", ledger=self.ledger)

    def history(self) -> HistoryBuilder:
        """Query ledger history."""
        return HistoryBuilderImpl(endpoint=f"{self.base_url}/fluree/history", ledger=self.ledger)
