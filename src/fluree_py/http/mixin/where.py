"""Mixin for handling where clause operations in Fluree queries."""

from typing import Protocol, TypeVar

from fluree_py.types.query.where import WhereClause


# Protocol definitions for where mixin
class HasWhereData(Protocol):
    """Protocol for objects that have where clause data."""

    where: WhereClause | None


T_co = TypeVar("T_co", bound=HasWhereData, covariant=True)


class SupportsWhere(Protocol[T_co]):
    """Protocol for objects that support where clause operations."""

    def with_where(self, value: WhereClause) -> T_co:
        """Set the where clause for the operation."""
        ...
