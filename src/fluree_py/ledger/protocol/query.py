from typing import (
    Any,
    Protocol,
    Self,
    TypeAlias,
    TypedDict,
)

from fluree_py.ledger.protocol.base import BaseBuilder, BaseReadyToCommit
from fluree_py.query.select.types import LogicVariable, SelectArray, SelectObject
from fluree_py.query.where.types import WhereClause, WhereFilterExpression

Role: TypeAlias = str
DecentralizedIdentifier: TypeAlias = str

ActiveIdentity = TypedDict("ActiveIdentity", {"did": DecentralizedIdentifier, "role": Role}, total=False)

OrderByClause: TypeAlias = LogicVariable | list[LogicVariable]

HavingClause: TypeAlias = WhereFilterExpression | list[WhereFilterExpression]
GroupByClause: TypeAlias = LogicVariable | list[LogicVariable]

class QueryBuilder(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for query builders."""

    def with_where(self, conditions: WhereClause) -> Self: ...
    def with_order_by(self, fields: OrderByClause) -> Self: ...
    def with_opts(self, opts: ActiveIdentity) -> Self: ...
    def with_select(self, fields: SelectObject | SelectArray) -> Self: ...
    def with_group_by(self, fields: GroupByClause) -> Self: ...

class QueryBuilderGrouped(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for query builders."""

    def with_where(self, conditions: WhereClause) -> Self: ...
    def with_having(self, condition: HavingClause) -> Self: ...
    def with_order_by(self, fields: OrderByClause) -> Self: ...
    def with_opts(self, opts: ActiveIdentity) -> Self: ...
    def with_select(self, fields: SelectObject | SelectArray) -> Self: ...
