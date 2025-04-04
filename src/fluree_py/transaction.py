from dataclasses import dataclass, replace
from typing import Any, Protocol

import httpx

from fluree_py.context import SupportsContext, WithContextMixin


class SupportsTransaction(Protocol):
    def transaction(self) -> "TransactionBuilder": ...


class TransactionBuilder(SupportsContext, Protocol):
    def with_insert(self, data: list[dict[str, Any]] | dict[str, Any]) -> "TransactionBuilder": ...
    def with_delete(self, data: list[dict[str, Any]] | dict[str, Any]) -> "TransactionBuilder": ...
    def with_where(self, clause: dict[str, Any]) -> "TransactionBuilder": ...
    def request(self) -> httpx.Request: ...
    def commit(self) -> dict[str, Any]: ...


@dataclass(frozen=True, kw_only=True)
class TransactionBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str
    insert_data: list[dict[str, Any]] | dict[str, Any] | None = None
    delete_data: list[dict[str, Any]] | dict[str, Any] | None = None
    where_clause: dict[str, Any] | None = None

    def with_insert(self, data: list[dict[str, Any]] | dict[str, Any]) -> "TransactionBuilderImpl":
        return replace(self, insert_data=data)

    @property
    def insert_json(self) -> dict[str, Any]:
        return {"insert": self.insert_data} if self.insert_data else {}

    @property
    def delete_json(self) -> dict[str, Any]:
        return {"delete": self.delete_data} if self.delete_data else {}

    @property
    def where_json(self) -> dict[str, Any]:
        return {"where": self.where_clause} if self.where_clause else {}

    def with_delete(self, data: list[dict[str, Any]] | dict[str, Any]) -> "TransactionBuilderImpl":
        return replace(self, delete_data=data)

    def with_where(self, clause: dict[str, Any]) -> "TransactionBuilderImpl":
        return replace(self, where_clause=clause)

    @property
    def json(self) -> dict[str, Any]:
        return self.context_json | {"ledger": self.ledger} | self.where_json | self.delete_json | self.insert_json

    def request(self) -> httpx.Request:
        if not self.insert_data and not self.delete_data:
            raise ValueError(
                "TransactBuilder: You must provide at least one of insert or delete before calling commit()."
            )

        return httpx.Request(
            "POST",
            self.endpoint,
            json=self.json,
        )

    def commit(self) -> dict[str, Any]:
        if not self.insert_data and not self.delete_data:
            raise ValueError(
                "TransactBuilder: You must provide at least one of insert or delete before calling commit()."
            )

        response = httpx.post(self.endpoint, json=self.json)
        response.raise_for_status()
        return response.json()
