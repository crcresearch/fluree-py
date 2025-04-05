from dataclasses import dataclass, replace
from typing import Any, Self

from fluree_py.http.mixin import (
    CommitableMixin,
    WithContextMixin,
    WithWhereMixin,
)
from fluree_py.http.protocol.endpoint.query import (
    ActiveIdentity,
    GroupByClause,
    HavingClause,
    OrderByClause,
    QueryBuilder,
)
from fluree_py.types.query.select import SelectArray, SelectObject
from fluree_py.types.query.where import WhereClause


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
        """Add group by clause to the query."""
        return replace(self, group_by=fields)

    def with_having(self, condition: HavingClause) -> Self:
        """Add having clause to the query."""
        return replace(self, having=condition)

    def with_order_by(self, fields: OrderByClause) -> Self:
        """Add order by clause to the query."""
        return replace(self, order_by=fields)

    def with_opts(self, opts: ActiveIdentity) -> Self:
        """Add query options to the query."""
        return replace(self, opts=opts)

    def with_select(self, fields: SelectObject | SelectArray) -> Self:
        """Add select fields to the query."""
        return replace(self, select_fields=fields)

    def get_url(self) -> str:
        """Get the endpoint URL for the query operation."""
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        """Build the request payload for the query operation."""
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
