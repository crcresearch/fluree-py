"""Protocols and types for building and executing queries in the Fluree ledger."""

from typing import (
    Protocol,
    Self,
)

from fluree_py.http.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsWhere,
)
from fluree_py.types.query.query import (
    ActiveIdentity,
    GroupByClause,
    HavingClause,
    OrderByClause,
)
from fluree_py.types.query.select import SelectArray, SelectObject


class QueryBuilder(
    SupportsContext["QueryBuilder"],
    SupportsWhere["QueryBuilder"],
    SupportsCommitable,
    Protocol,
):
    """Protocol for building query operations."""

    def with_order_by(self, fields: OrderByClause) -> Self:
        """Set the order by clause for the operation."""
        ...

    def with_opts(self, opts: ActiveIdentity) -> Self:
        """Set the active identity for the operation."""
        ...

    def with_select(self, fields: SelectObject | SelectArray) -> Self:
        """Set the select clause for the operation."""
        ...

    def with_group_by(self, fields: GroupByClause) -> Self:
        """Set the group by clause for the operation."""
        ...

    def with_having(self, condition: HavingClause) -> Self:
        """Set the having clause for the operation."""
        ...
