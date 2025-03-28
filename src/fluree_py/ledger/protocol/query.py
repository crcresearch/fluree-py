from typing import (
    Any,
    Dict,
    List,
    Protocol,
    Self,
)

from fluree_py.ledger.protocol.base import BaseBuilder, BaseReadyToCommit


# Define Condition as a dictionary with flexible key-value pairs
WhereCondition = Dict[str, Any]

# Define Operation as a list that represents operations like union or filter
WhereOperation = List[str | Any]

# Define QueryList as a list that can contain Conditions or Operations
WhereQueryList = List[WhereCondition | WhereOperation]


class QueryBuilder(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for query builders."""

    def with_where(self, conditions: WhereCondition | WhereQueryList) -> Self: ...
    def with_group_by(self, fields: list[str]) -> Self: ...
    def with_having(self, condition: dict[str, Any]) -> Self: ...
    def with_order_by(self, fields: list[str]) -> Self: ...
    def with_opts(self, opts: dict[str, Any]) -> Self: ...
    def with_select(self, fields: dict[str, Any] | list[str]) -> Self: ...
