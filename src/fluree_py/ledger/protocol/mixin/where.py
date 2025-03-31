from typing import Generic, Protocol, TypeVar

from fluree_py.query.where import WhereClause


class HasWhereData(Protocol):
    """Protocol for objects that have where clause data."""
    where: WhereClause | None


T = TypeVar("T", bound="HasWhereData", covariant=True)


class SupportsWhere(Generic[T], Protocol):
    """Protocol for objects that support where clause operations."""
    where: WhereClause | None = None

    def with_where(self, clause: WhereClause) -> T: ...
