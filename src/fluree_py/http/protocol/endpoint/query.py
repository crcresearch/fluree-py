"""Protocols and types for building and executing queries in the Fluree ledger."""

from typing import (
    Protocol,
    Self,
)

from fluree_py.http.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsRequestCreation,
    SupportsWhere,
)
from fluree_py.types.query.select import SelectArray, SelectObject
from fluree_py.types.query.query import (
    OrderByClause,
    ActiveIdentity,
    GroupByClause,
    HavingClause,
)


class QueryBuilder(
    SupportsContext["QueryBuilder"],
    SupportsWhere["QueryBuilder"],
    SupportsRequestCreation,
    SupportsCommitable,
    Protocol,
):
    """Protocol for building query operations."""

    def with_order_by(self, fields: OrderByClause) -> Self: ...
    def with_opts(self, opts: ActiveIdentity) -> Self: ...
    def with_select(self, fields: SelectObject | SelectArray) -> Self: ...
    def with_group_by(self, fields: GroupByClause) -> Self: ...
    def with_having(self, condition: HavingClause) -> Self: ...
