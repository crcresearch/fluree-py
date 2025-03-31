from dataclasses import dataclass, replace
from typing import Any, Self

from fluree_py.ledger.mixin import CommitableMixin, RequestMixin, WithContextMixin
from fluree_py.ledger.mixin.where import WithWhereMixin
from fluree_py.ledger.protocol.endpoint.query import (
    GroupByClause,
    HavingClause,
    OrderByClause,
    QueryBuilder,
    ActiveIdentity,
)
from fluree_py.query.select.types import SelectArray, SelectObject
from fluree_py.query.where.types import WhereClause


@dataclass(frozen=True, kw_only=True)
class QueryBuilderImpl(
    WithContextMixin["QueryBuilderImpl"],
    WithWhereMixin["QueryBuilderImpl"],
    RequestMixin,
    CommitableMixin["QueryBuilderImpl"],
    QueryBuilder,
):
    endpoint: str
    ledger: str
    context: dict[str, Any] | None = None
    where: WhereClause | None = None
    group_by: GroupByClause | None = None
    having: HavingClause | None = None
    order_by: OrderByClause | None = None
    opts: ActiveIdentity | None = None
    select_fields: dict[str, Any] | list[str] | None = None

    def with_group_by(self, fields: GroupByClause) -> Self:
        return replace(self, group_by=fields)

    def with_having(self, condition: HavingClause) -> Self:
        return replace(self, having=condition)

    def with_order_by(self, fields: OrderByClause) -> Self:
        return replace(self, order_by=fields)

    def with_opts(self, opts: ActiveIdentity) -> Self:
        return replace(self, opts=opts)

    def with_select(self, fields: SelectObject | SelectArray) -> Self:
        return replace(self, select_fields=fields)

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.context:
            result["@context"] = self.context
        result |= {"from": self.ledger}
        if self.where:
            result["where"] = self.where
        if self.group_by:
            result["groupBy"] = self.group_by
        if self.having:
            result["having"] = self.having
        if self.order_by:
            result["orderBy"] = self.order_by
        if self.opts:
            result["opts"] = self.opts
        if self.select_fields:
            result["select"] = self.select_fields
        return result
