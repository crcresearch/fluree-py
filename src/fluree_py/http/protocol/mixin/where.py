from typing import Generic, Protocol, TypeVar

from fluree_py.types.query.where import WhereClause


class HasWhereData(Protocol):
    where: WhereClause | None


T = TypeVar("T", bound="HasWhereData", covariant=True)


class SupportsWhere(Generic[T], Protocol):
    where: WhereClause | None = None

    def with_where(self, clause: WhereClause) -> T: ...
