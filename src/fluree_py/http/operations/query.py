"""Query operation protocols and implementations."""

from dataclasses import dataclass, replace
from typing import Any, ClassVar, Protocol, Self

from fluree_py.http.mixin.commit import CommitableMixin, SupportsCommitable
from fluree_py.http.mixin.context import HasContextData, SupportsContext
from fluree_py.http.mixin.response import SupportsFromResponse, SupportsRaisingFromResponse
from fluree_py.http.mixin.utils import make_setter
from fluree_py.http.mixin.where import HasWhereData, SupportsWhere
from fluree_py.http.response import MissingTransactionError, QueryResponse
from fluree_py.logging import logger
from fluree_py.types.query.query import ActiveIdentity, GroupByClause, HavingClause, OrderByClause
from fluree_py.types.query.select import SelectArray, SelectObject
from fluree_py.types.query.where import WhereClause


# Protocol definitions for query operations
class QueryBuilder(
    HasContextData,
    SupportsContext["QueryBuilder"],
    HasWhereData,
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


# Implementation of query operations
@dataclass(frozen=True, kw_only=True)
class QueryBuilderImpl(
    CommitableMixin[QueryResponse],
    QueryBuilder,
):
    """Implementation of a query operation builder."""

    __response_errors__: ClassVar[list[type[SupportsRaisingFromResponse]]] = [MissingTransactionError]
    __response_payload__: ClassVar[type[SupportsFromResponse]] = QueryResponse

    endpoint: str
    ledger: str
    context: dict[str, Any] | None = None
    where: WhereClause | None = None
    group_by: GroupByClause | None = None
    having: HavingClause | None = None
    order_by: OrderByClause | None = None
    opts: ActiveIdentity | None = None
    select_fields: SelectObject | SelectArray | None = None

    def __post_init__(self) -> None:
        """Log the initialization of the query builder."""
        logger.info(
            "query_builder_initialized",
            endpoint=self.endpoint,
            ledger=self.ledger,
            context=self.context,
            where=self.where,
            group_by=self.group_by,
            having=self.having,
            order_by=self.order_by,
            opts=self.opts,
            select_fields=self.select_fields,
        )

    with_context = make_setter("with_context", "context")
    with_where = make_setter("with_where", "where")

    def with_group_by(self, fields: GroupByClause) -> Self:
        """Set the group by clause for the operation."""
        return replace(self, group_by=fields)

    def with_having(self, condition: HavingClause) -> Self:
        """Set the having clause for the operation."""
        return replace(self, having=condition)

    def with_order_by(self, fields: OrderByClause) -> Self:
        """Set the order by clause for the operation."""
        return replace(self, order_by=fields)

    def with_opts(self, opts: ActiveIdentity) -> Self:
        """Set the active identity for the operation."""
        return replace(self, opts=opts)

    def with_select(self, fields: SelectObject | SelectArray) -> Self:
        """Set the select clause for the operation."""
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
        logger.debug("building_query_payload", payload=result)
        return result
