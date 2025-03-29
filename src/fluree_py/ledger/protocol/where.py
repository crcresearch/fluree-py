from typing import Protocol, Self

from fluree_py.query.where.types import WhereClause

class SupportsWhere(Protocol):
    def with_where(self, clause: WhereClause) -> Self: ...
