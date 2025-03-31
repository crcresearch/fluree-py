from typing import (
    Protocol,
    Self,
    TypeAlias,
    TypedDict,
)

from fluree_py.ledger.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsRequestCreation,
)
from fluree_py.ledger.protocol.mixin.where import SupportsWhere
from fluree_py.query.select.types import LogicVariable, SelectArray, SelectObject
from fluree_py.query.where.types import WhereFilterExpression

Role: TypeAlias = str
DecentralizedIdentifier: TypeAlias = str

ActiveIdentity = TypedDict(
    "ActiveIdentity", {"did": DecentralizedIdentifier, "role": Role}, total=False
)

OrderByClause: TypeAlias = LogicVariable | list[LogicVariable]

HavingClause: TypeAlias = WhereFilterExpression | list[WhereFilterExpression]
GroupByClause: TypeAlias = LogicVariable | list[LogicVariable]


class QueryBuilder(
    SupportsContext["QueryBuilder"],
    SupportsWhere["QueryBuilder"],
    SupportsRequestCreation,
    SupportsCommitable,
    Protocol,
):
    """Protocol for query builders."""

    def with_order_by(self, fields: OrderByClause) -> Self: ...
    def with_opts(self, opts: ActiveIdentity) -> Self: ...
    def with_select(self, fields: SelectObject | SelectArray) -> Self: ...
    def with_group_by(self, fields: GroupByClause) -> Self: ...
    def with_having(self, condition: HavingClause) -> Self: ...
