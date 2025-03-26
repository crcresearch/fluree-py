from dataclasses import dataclass, replace
from typing import Any

import httpx
from fluree_py.ledger.mixin.context import WithContextMixin


@dataclass(frozen=True, kw_only=True)
class QueryBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str
    where: dict[str, Any] | None = None
    group_by: list[str] | None = None
    having: dict[str, Any] | None = None
    order_by: list[str] | None = None
    opts: dict[str, Any] | None = None
    select_fields: list[str] | None = None

    def with_where(self, conditions: dict[str, Any]) -> "QueryBuilderImpl":
        return replace(self, where=conditions)

    @property
    def where_json(self) -> dict[str, Any]:
        return {"where": self.where} if self.where else {}

    def with_group_by(self, fields: list[str]) -> "QueryBuilderImpl":
        return replace(self, group_by=fields)

    @property
    def group_by_json(self) -> dict[str, Any]:
        return {"groupBy": self.group_by} if self.group_by else {}

    def with_having(self, condition: dict[str, Any]) -> "QueryBuilderImpl":
        return replace(self, having=condition)

    @property
    def having_json(self) -> dict[str, Any]:
        return {"having": self.having} if self.having else {}

    def with_order_by(self, fields: list[str]) -> "QueryBuilderImpl":
        return replace(self, order_by=fields)

    @property
    def order_by_json(self) -> dict[str, Any]:
        return {"orderBy": self.order_by} if self.order_by else {}

    def with_opts(self, opts: dict[str, Any]) -> "QueryBuilderImpl":
        return replace(self, opts=opts)

    @property
    def opts_json(self) -> dict[str, Any]:
        return {"opts": self.opts} if self.opts else {}

    def select(self, fields: dict[str, Any] | list[str]) -> "QueryBuilderImpl":
        return replace(self, select_fields=fields)

    @property
    def select_json(self) -> dict[str, Any]:
        return {"select": self.select_fields} if self.select_fields else {}

    @property
    def json(self) -> dict[str, Any]:
        return (
            self.context_json
            | {"from": self.ledger}
            | self.where_json
            | self.group_by_json
            | self.having_json
            | self.order_by_json
            | self.opts_json
            | self.select_json
        )

    def request(self) -> httpx.Request:
        return httpx.Request(
            "POST",
            self.endpoint,
            json=self.json,
        )

    def commit(self) -> dict[str, Any]:
        response = httpx.post(self.endpoint, json=self.json)
        response.raise_for_status()
        return response.json()
