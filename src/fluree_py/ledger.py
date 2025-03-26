from dataclasses import dataclass

from fluree_py.create import CreateBuilderImpl
from fluree_py.history import HistoryBuilderImpl
from fluree_py.query import QueryBuilderImpl
from fluree_py.transaction import TransactionBuilderImpl


@dataclass(frozen=True, kw_only=True)
class LedgerSelected:
    base_url: str
    ledger: str

    def create(self) -> "CreateBuilderImpl":
        return CreateBuilderImpl(
            endpoint=f"{self.base_url}/fluree/create", ledger=self.ledger
        )

    def transaction(self) -> "TransactionBuilderImpl":
        return TransactionBuilderImpl(
            endpoint=f"{self.base_url}/fluree/transact", ledger=self.ledger
        )

    def query(self) -> "QueryBuilderImpl":
        return QueryBuilderImpl(
            endpoint=f"{self.base_url}/fluree/query", ledger=self.ledger
        )

    def history(self) -> "HistoryBuilderImpl":
        return HistoryBuilderImpl(
            endpoint=f"{self.base_url}/fluree/history", ledger=self.ledger
        )
