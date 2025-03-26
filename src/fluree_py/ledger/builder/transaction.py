from dataclasses import dataclass, replace
from typing import Any


from fluree_py.ledger.mixin.commit import CommitMixin
from fluree_py.ledger.mixin.context import WithContextMixin
from fluree_py.ledger.mixin.request_builder import WithRequestMixin


@dataclass(frozen=True, kw_only=True)
class TransactionBuilderImpl(WithRequestMixin, WithContextMixin, CommitMixin):
    endpoint: str
    ledger: str
    insert_data: dict[str, Any] | None = None
    delete_data: dict[str, Any] | None = None
    where_clause: dict[str, Any] | None = None

    def with_insert(self, data: dict[str, Any]) -> "TransactionBuilderImpl":
        return replace(self, insert_data=data)

    def with_delete(self, data: dict[str, Any]) -> "TransactionBuilderImpl":
        return replace(self, delete_data=data)

    def with_where(self, clause: dict[str, Any]) -> "TransactionBuilderImpl":
        return replace(self, where_clause=clause)

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        if not self.insert_data and not self.delete_data:
            raise ValueError(
                "TransactBuilder: You must provide at least one of insert or delete before calling commit()."
            )

        result = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger}
        if self.insert_data:
            result["insert"] = self.insert_data
        if self.delete_data:
            result["delete"] = self.delete_data
        if self.where_clause:
            result["where"] = self.where_clause
        return result
