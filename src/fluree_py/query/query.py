from typing import TypeAlias, TypedDict

from fluree_py.types import JsonObject
from fluree_py.query.select.types import LogicVariable, SelectClause
from fluree_py.query.where import WhereClause, WhereFilterExpression
from fluree_py.query.history import TimeClause

Context: TypeAlias = JsonObject
"""
A W3C JSON-LD context for a FlureeQL request.
"""

Role: TypeAlias = str
DecentralizedIdentifier: TypeAlias = str

ActiveIdentity = TypedDict(
    "ActiveIdentity", {"did": DecentralizedIdentifier, "role": Role}, total=False
)

OrderByClause: TypeAlias = LogicVariable | list[LogicVariable]

HavingClause: TypeAlias = WhereFilterExpression | list[WhereFilterExpression]
GroupByClause: TypeAlias = LogicVariable | list[LogicVariable]


QuerySchema = TypedDict(
    "QuerySchema",
    {
        "@context": Context,
        "from": str | list[str],
        "where": WhereClause,
        "select": SelectClause,
        "t": TimeClause,
        "groupBy": GroupByClause,
        "having": HavingClause,
        "orderBy": OrderByClause,
    },
)
"""
A schema for a FlureeQL query.
"""
