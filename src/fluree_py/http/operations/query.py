"""Query operation protocols and implementations."""

from dataclasses import dataclass, replace
from typing import Any, Protocol, Self

from fluree_py.http.mixin import WithContextMixin, WithWhereMixin
from fluree_py.http.mixin.commit import CommitableMixin, SupportsCommitable
from fluree_py.http.mixin.context import SupportsContext
from fluree_py.http.mixin.where import SupportsWhere
from fluree_py.types.query.query import ActiveIdentity, GroupByClause, HavingClause, OrderByClause
from fluree_py.types.query.select import SelectArray, SelectObject
from fluree_py.types.query.where import WhereClause


class QueryBuilder(
    SupportsContext["QueryBuilder"],
    SupportsWhere["QueryBuilder"],
    SupportsCommitable,
    Protocol,
):
    """Protocol for building query operations."""

    def with_order_by(self, fields: OrderByClause) -> Self: ...

    def with_opts(self, opts: ActiveIdentity) -> Self: ...

    def with_select(self, fields: SelectObject | SelectArray) -> Self: ...

    def with_group_by(self, fields: GroupByClause) -> Self: ...

    def with_having(self, condition: HavingClause) -> Self: ...


@dataclass(frozen=True, kw_only=True)
class QueryBuilderImpl(
    CommitableMixin,
    WithContextMixin["QueryBuilderImpl"],
    WithWhereMixin["QueryBuilderImpl"],
    QueryBuilder,
):
    """Implementation of a query operation builder."""

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
