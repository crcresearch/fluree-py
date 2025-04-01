from typing import TypeAlias, TypedDict

from fluree_py.types.common import JsonObject
from fluree_py.types.query.select import LogicVariable, SelectClause
from fluree_py.types.query.where import WhereClause, WhereFilterExpression  
from fluree_py.types.history import TimeClause   

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
