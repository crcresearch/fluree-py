from dataclasses import dataclass, replace
from typing import Self

from fluree_py.http.protocol.endpoint.where import SupportsWhere
from fluree_py.types.query.where import WhereClause


@dataclass(frozen=True, kw_only=True)
class WithWhereMixin(SupportsWhere):
    where: WhereClause | None = None

    def with_where(self, clause: WhereClause) -> Self:
        return replace(self, where=clause)
