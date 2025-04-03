from typing import Generic, Protocol, TypeVar

from fluree_py.types.query.where import WhereClause


class HasWhereData(Protocol):
    """Protocol for objects that have where clause data."""

    where: WhereClause | None


T_co = TypeVar("T_co", bound="HasWhereData", covariant=True)


class SupportsWhere(Generic[T_co], Protocol):
    """Protocol for objects that support where clause operations."""

    where: WhereClause | None = None

    def with_where(self, clause: WhereClause) -> T_co:
        """Set the where clause for the operation."""
        ...
