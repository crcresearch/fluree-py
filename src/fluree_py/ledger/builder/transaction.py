from dataclasses import dataclass, replace
from typing import Any

from fluree_py.ledger.mixin import CommitableMixin, RequestMixin, WithContextMixin
from fluree_py.ledger.mixin.where import WithWhereMixin
from fluree_py.query.where.types import WhereClause
from fluree_py.types import JsonArray, JsonObject


@dataclass(frozen=True, kw_only=True)
class TransactionBuilderImpl(WithContextMixin, WithWhereMixin):
    endpoint: str
    ledger: str
    insert_data: JsonObject | JsonArray | None = None
    delete_data: JsonObject | JsonArray | None = None

    def with_insert(
        self, data: JsonObject | JsonArray
    ) -> "TransactionReadyToCommitImpl":
        return TransactionReadyToCommitImpl(
            endpoint=self.endpoint,
            ledger=self.ledger,
            insert_data=data,
            delete_data=self.delete_data,
            where=self.where,
            context=self.context,
        )

    def with_delete(self, data: JsonObject | JsonArray) -> "TransactionReadyToCommitImpl":
        return TransactionReadyToCommitImpl(
            endpoint=self.endpoint,
            ledger=self.ledger,
            insert_data=self.insert_data,
            delete_data=data,
            where=self.where,
            context=self.context,
        )

@dataclass(frozen=True, kw_only=True)
class TransactionReadyToCommitImpl(RequestMixin, WithContextMixin, WithWhereMixin, CommitableMixin):
    endpoint: str
    ledger: str
    insert_data: JsonObject | JsonArray | None = None
    delete_data: JsonObject | JsonArray | None = None   
    
    def with_insert(
        self, data: JsonObject | JsonArray
    ) -> "TransactionReadyToCommitImpl":
        return replace(self, insert_data=data)

    def with_delete(self, data: JsonObject | JsonArray) -> "TransactionReadyToCommitImpl":
        return replace(self, delete_data=data)

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger}
        if self.insert_data:
            result["insert"] = self.insert_data
        if self.delete_data:
            result["delete"] = self.delete_data
        if self.where:
            result["where"] = self.where
        return result
