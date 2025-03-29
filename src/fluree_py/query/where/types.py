# You can think of a FlureeQL query executing in two phases: the where phase and the select phase. The where phase filters and returns sets of bound values that the select phase can use to construct JSON objects. The where clause may return node subject ?bindings that we then use with select expressions like "*" to perform graph crawls from those subject nodes.
# The where clause may also retrieve all the bindings we need, and we simply instruct the select clause that we want those bindings returned directly as query results.
# In any case, in addition to establishing logic variables for bound values, we use the where clause to establish various data constraints for the data we are interested in querying (e.g. filtering by a particular predicate value, or expressing optional and outer-join data conditions).
# When a where clause is an array, it can combine a series of where conditions and where operations.

# Define Condition as a dictionary with flexible key-value pairs
from typing import Dict, List, Literal, TypeAlias, TypeGuard, Union

from fluree_py.query.select.types import LogicVariable
from fluree_py.query.types import Predicate

WhereResultSet: TypeAlias = Dict[Union[Predicate, LogicVariable], LogicVariable]
WhereRelationship: TypeAlias = Dict[Union[Predicate, LogicVariable], Predicate]

# A where condition describes relationships between nodes that must be satisfied for the nodes to be included in result sets, and it names those sets.
#
# Examples:
# { "@id": "?s", "schema:name": "Sheil" }
# { "@id": "?s", "schema:name": "?name" }
# { "@id": "?s", "schema:name": "Freddie", "schema:familyName": "Mercury" }
# { "@id": "http://example.org/jack", "?p": "?o" }
WhereCondition = Dict[WhereResultSet, WhereRelationship]

# Examples:
# [ 
#    {
#        "@id": "?s",
#        "bestFriend": "?friend"
#     },
#     {
#       "@id": "?friend",
#       "schema:name": "?name"
#     }
#   ]
SuccessiveWhereCondition: TypeAlias = List[WhereCondition]


# Examples:
# [
#   "optional",
#     { "@id": "?s", "schema:name": "?name" },
#     { "@id": "?s", "schema:age": "?age" }
# ]
WhereOperationOptional: TypeAlias = List[Union[Literal["optional"], WhereCondition]]


# Examples:
# "(> ?age 45)"
# "(< ?age 50)"
# (! (strStarts ?url \"http\"))
WhereFilterExpression: TypeAlias = str

# A filter expression is a string that starts and ends with a parenthesis.
# It starts with a function, followed by a space
# It then contains a list of arguments.
# Each argument may be a logic variable, a predicate, or a nested filter expression.
# Examples:
# "(> ?age 45)"
# "(< ?age 50)"
# (! (strStarts ?url \"http\"))
def is_filter_expression(var: str) -> TypeGuard[WhereFilterExpression]:
    """
    Type guard to check if a string is a valid filter expression.
    """
    if not all(c.isprintable() for c in var):
        return False
    
    # Check if the string starts and ends with a parenthesis
    if not (var.startswith("(") and var.endswith(")")):
        return False
    
    # Get internal string
    internal = var[1:-1]
    
    # Check if the internal string is balanced
    if internal.count("(") != internal.count(")") or internal.count("\"") % 2 != 0:
        return False
    
    # The internal string may have multiple arguments
    # Each argument can be a nested filter expression, a logic variable, or a predicate
    # There must be at least one logic variable or nested filter expression
    
    return True

# Examples:
# ["filter", "(> ?age 45)", "(< ?age 50)"]
WhereOperationFilter: TypeAlias = List[Union[Literal["optional"], WhereFilterExpression]]


# Examples:
# [
#   "union",
#   { "@id": "?s", "schema:email": "?email" },
#   { "@id": "?s", "ex:email": "?email" }
# ]
WhereOperationUnion: TypeAlias = List[Union[Literal["union"], WhereCondition]]

# Examples:
# ["bind", "?canVote", "(>= ?age 18)"]
WhereOperationBind: TypeAlias = List[Union[Literal["bind"], LogicVariable, WhereFilterExpression]]

WhereOperation = Union[WhereOperationOptional, WhereOperationFilter, WhereOperationUnion, WhereOperationBind]



WhereClauseEntry: TypeAlias = Union[WhereCondition, WhereOperation]

WhereClause: TypeAlias = List[WhereClauseEntry]