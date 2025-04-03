"""Query grammar package."""

from typing import TypeAlias, TypedDict

from fluree_py.types.common import Context, TimeClause
from fluree_py.types.query.select import LogicVariable, SelectClause
from fluree_py.types.query.where import WhereClause, WhereFilterExpression

Role: TypeAlias = str
DecentralizedIdentifier: TypeAlias = str


class ActiveIdentity(TypedDict, total=False):
    did: DecentralizedIdentifier
    role: Role


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
""" A schema for a FlureeQL query. """
