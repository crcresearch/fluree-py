from dataclasses import dataclass

from fluree_py.create import CreateBuilder, CreateBuilderImpl
from fluree_py.history import HistoryBuilder, HistoryBuilderImpl
from fluree_py.query import QueryBuilder, QueryBuilderImpl
from fluree_py.transaction import TransactionBuilder, TransactionBuilderImpl


@dataclass(frozen=True, kw_only=True)
class LedgerSelected:
    base_url: str
    ledger: str

    def create(self) -> "CreateBuilder":
        return CreateBuilderImpl(
            endpoint=f"{self.base_url}/fluree/create", ledger=self.ledger
        )

    def transaction(self) -> "TransactionBuilder":
        return TransactionBuilderImpl(
            endpoint=f"{self.base_url}/fluree/transact", ledger=self.ledger
        )

    def query(self) -> "QueryBuilder":
        return QueryBuilderImpl(
            endpoint=f"{self.base_url}/fluree/query", ledger=self.ledger
        )

    def history(self) -> "HistoryBuilder":
        return HistoryBuilderImpl(
            endpoint=f"{self.base_url}/fluree/history", ledger=self.ledger
        )
