from dataclasses import dataclass, replace
from typing import Any, Dict, List, Optional, Protocol

import httpx

from fluree_py.context import SupportsContext, WithContextMixin


class QueryBuilder(SupportsContext, Protocol):
    def with_where(self, conditions: Dict[str, Any]) -> "QueryBuilder": ...
    def with_group_by(self, fields: List[str]) -> "QueryBuilder": ...
    def with_having(self, condition: Dict[str, Any]) -> "QueryBuilder": ...
    def with_order_by(self, fields: List[str]) -> "QueryBuilder": ...
    def with_opts(self, opts: Dict[str, Any]) -> "QueryBuilder": ...
    def select(self, fields: List[str]) -> "QueryBuilder": ...
    def request(self) -> httpx.Request: ...
    def commit(self) -> Dict[str, Any]: ...


@dataclass(frozen=True, kw_only=True)
class QueryBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str
    where: Optional[Dict[str, Any]] = None
    group_by: Optional[List[str]] = None
    having: Optional[Dict[str, Any]] = None
    order_by: Optional[List[str]] = None
    opts: Optional[Dict[str, Any]] = None
    select_fields: Optional[List[str]] = None

    def with_where(self, conditions: Dict[str, Any]) -> "QueryBuilderImpl":
        return replace(self, where=conditions)

    @property
    def where_json(self) -> Dict[str, Any]:
        return {"where": self.where} if self.where else {}

    def with_group_by(self, fields: List[str]) -> "QueryBuilderImpl":
        return replace(self, group_by=fields)

    @property
    def group_by_json(self) -> Dict[str, Any]:
        return {"groupBy": self.group_by} if self.group_by else {}

    def with_having(self, condition: Dict[str, Any]) -> "QueryBuilderImpl":
        return replace(self, having=condition)

    @property
    def having_json(self) -> Dict[str, Any]:
        return {"having": self.having} if self.having else {}

    def with_order_by(self, fields: List[str]) -> "QueryBuilderImpl":
        return replace(self, order_by=fields)

    @property
    def order_by_json(self) -> Dict[str, Any]:
        return {"orderBy": self.order_by} if self.order_by else {}

    def with_opts(self, opts: Dict[str, Any]) -> "QueryBuilderImpl":
        return replace(self, opts=opts)

    @property
    def opts_json(self) -> Dict[str, Any]:
        return {"opts": self.opts} if self.opts else {}

    def select(self, fields: List[str]) -> "QueryBuilderImpl":
        return replace(self, select_fields=fields)

    @property
    def select_json(self) -> Dict[str, Any]:
        return {"select": self.select_fields} if self.select_fields else {}

    @property
    def json(self) -> Dict[str, Any]:
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

    def commit(self) -> Dict[str, Any]:
        response = httpx.post(self.endpoint, json=self.json)
        response.raise_for_status()
        return response.json()
