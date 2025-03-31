from dataclasses import dataclass, replace
from typing import Any

from fluree_py.http.mixin import CommitableMixin, RequestMixin, WithContextMixin
from fluree_py.http.mixin.insert import WithInsertMixin
from fluree_py.http.mixin.where import WithWhereMixin
from fluree_py.http.protocol.endpoint import (
    TransactionBuilder,
    TransactionReadyToCommit,
)
from fluree_py.types.common import JsonArray, JsonObject
from fluree_py.types.query.where import WhereClause


@dataclass(frozen=True, kw_only=True)
class TransactionBuilderImpl(
    WithContextMixin["TransactionBuilderImpl"],
    WithInsertMixin["TransactionReadyToCommitImpl"],
    WithWhereMixin["TransactionBuilderImpl"],
    TransactionBuilder,
):
    endpoint: str
    ledger: str
    context: dict[str, Any] | None = None
    where: WhereClause | None = None
    data: JsonObject | JsonArray | None = None
    delete_data: JsonObject | JsonArray | None = None

    def with_delete(
        self, data: JsonObject | JsonArray
    ) -> "TransactionReadyToCommitImpl":
        updated_fields = self.__dict__.copy()
        updated_fields["delete_data"] = data
        return TransactionReadyToCommitImpl(**updated_fields)


@dataclass(frozen=True, kw_only=True)
class TransactionReadyToCommitImpl(
    RequestMixin,
    WithContextMixin["TransactionReadyToCommitImpl"],
    WithWhereMixin["TransactionReadyToCommitImpl"],
    CommitableMixin["TransactionReadyToCommitImpl"],
    TransactionReadyToCommit,
):
    endpoint: str
    ledger: str
    context: dict[str, Any] | None
    where: WhereClause | None
    data: JsonObject | JsonArray | None
    delete_data: JsonObject | JsonArray | None

    def with_delete(
        self, data: JsonObject | JsonArray
    ) -> "TransactionReadyToCommitImpl":
        return replace(self, delete_data=data)

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger}
        if self.data:
            result["insert"] = self.data
        if self.delete_data:
            result["delete"] = self.delete_data
        if self.where:
            result["where"] = self.where
        return result
