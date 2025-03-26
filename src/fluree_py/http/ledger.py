from dataclasses import dataclass

from fluree_py.http.endpoint.create import CreateBuilderImpl
from fluree_py.http.endpoint.history import HistoryBuilderImpl
from fluree_py.http.endpoint.query import QueryBuilderImpl
from fluree_py.http.endpoint.transact import TransactionBuilderImpl
from fluree_py.http.protocol.endpoint.create import CreateBuilder
from fluree_py.http.protocol.endpoint.history import HistoryBuilder
from fluree_py.http.protocol.endpoint.query import QueryBuilder
from fluree_py.http.protocol.endpoint.transaction import TransactionBuilder


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
