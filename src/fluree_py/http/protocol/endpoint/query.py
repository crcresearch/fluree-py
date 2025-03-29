from typing import (
    Any,
    Protocol,
    Self,
    TypeAlias,
    TypedDict,
)

from fluree_py.http.protocol.endpoint.base import BaseBuilder, BaseReadyToCommit
from fluree_py.types.query.select import SelectArray, SelectObject
from fluree_py.types.query.where import WhereClause

Role: TypeAlias = str
DecentralizedIdentifier: TypeAlias = str

ActiveIdentity = TypedDict("ActiveIdentity", {"did": DecentralizedIdentifier, "role": Role}, total=False)

class QueryBuilder(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for query builders."""

    def with_where(self, conditions: WhereClause) -> Self: ...
    def with_order_by(self, fields: list[str]) -> Self: ...
    def with_opts(self, opts: ActiveIdentity) -> Self: ...
    def with_select(self, fields: SelectObject | SelectArray) -> Self: ...
    def with_group_by(self, fields: list[str]) -> Self: ...

class QueryBuilderGrouped(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for query builders."""

    def with_where(self, conditions: WhereClause) -> Self: ...
    def with_having(self, condition: dict[str, Any]) -> Self: ...
    def with_order_by(self, fields: list[str]) -> Self: ...
    def with_opts(self, opts: ActiveIdentity) -> Self: ...
    def with_select(self, fields: SelectObject | SelectArray) -> Self: ...
