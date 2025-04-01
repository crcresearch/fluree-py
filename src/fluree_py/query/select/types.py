"""
FlureeQL Select Clause Grammar

The select clause in FlureeQL determines the structure and content of query results.
It can be either a select object or a select array.

This grammar defines the syntax for FlureeQL select clauses. The types defined below
in this file implement this grammar in Python.

Grammar (EBNF):
``` ebnf
    (* Main select clause structure *)
    SelectClause = SelectObject | SelectArray

    (* Select object maps logic variables to expressions *)
    SelectObject = "{" LogicVariable ":" SelectExpressionList "}"
    SelectExpressionList = [SelectExpression {"," SelectExpression}]

    (* Select array contains variables or objects *)
    SelectArray = "[" SelectArrayElement {"," SelectArrayElement} "]"
    SelectArrayElement = LogicVariable | SelectObject

    (* Expression types *)
    SelectExpression = Wildcard | Predicate | NodeObjectTemplate
    NodeObjectTemplate = "{" Predicate ":" SelectExpressionList "}"

    (* Basic elements *)
    LogicVariable = "?" (letter | digit | "-" | "_") {letter | digit | "-" | "_"}
    Predicate = string
    Wildcard = "*"

    (* Character sets *)
    letter = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
    digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
    string = '"' {character} '"'
    character = letter | digit | "-" | "_" | ":" | "."
```

Example Queries:
    # Select object - get name and all predicates of best friend
    - { "?s": [ "name", { "bestFriend": ["*"] } ] }

    # Select array - get multiple variables and objects
    - ["?s", "?name", "?friend"]
    - [ { "?s": ["*"] }, { "?friend": ["*"] } ]

    # Node object template - nested data structures
    - { "schema:address": ["*"] }                    # Get all address predicates
    - { "bestFriend": ["*"] }                        # Get all best friend predicates
    - { "bestFriend": [ { "address": ["*"] } ] }     # Get address of best friend

    # Logic variable examples
    - "?firstname"
    - "?first-name"
    - "?first_name"
    - "?address-1"
"""

import re
from typing import Any, Dict, List, TypeAlias, TypeGuard, Union

from fluree_py.query.types import Predicate, Wildcard

# Regex pattern to match valid logic variables.
# Starts with ? and is followed by alphanumeric characters, hyphens, or underscores.
LOGIC_VARIABLE_PATTERN = re.compile(r"^\?[a-zA-Z0-9_-]+$")

LogicVariable: TypeAlias = str
"""
A logic variable name in a FlureeQL query.
Logic variables are strings that begin with a question mark, ?, followed by
alphanumeric characters, hyphens, and underscores. They are used to bind
subjects to variables in the query.

Example Queries:
    "?firstname"
    "?first-name"
    "?first_name"
    "?address-1"
"""


def is_logic_variable(var: str) -> TypeGuard[LogicVariable]:
    """
    Type guard to check if a string is a valid logic variable.
    """
    if not all(c.isprintable() for c in var):
        return False
    return LOGIC_VARIABLE_PATTERN.search(var) is not None


SelectExpression: TypeAlias = Union[Wildcard, Predicate, "NodeObjectTemplate"]
"""
A select expression in a FlureeQL query.
Select expressions define what data to include in the query results.
They can be:
1. A predicate (e.g., "schema:name") - includes the value of that predicate
2. The wildcard "*" - includes all predicates of the subject
3. A node object template - traverses nested predicate values

Example Queries:
    ["name", { "bestFriend": ["*"] }]
"""

SelectExpressionList: TypeAlias = List[SelectExpression]
"""
A list of select expressions in a FlureeQL query.
Used in both select objects and node templates to specify multiple expressions.

Example Queries:
    ["name", "*", { "bestFriend": ["*"] }]
"""

NodeObjectTemplate: TypeAlias = Dict[Predicate, "SelectExpressionList"]
"""
A node object template in a FlureeQL query.
Node object templates define how to traverse nested predicate values.
They are objects where the keys are predicates, and the values are arrays of
select expressions. This allows for recursive querying of nested data structures.

Example Queries:
    { "schema:address": ["*"] }

    # Return an object that has all predicates for the node that "bestFriend" refers to
    { "bestFriend": ["*"] }

    # Multi-level nested object
    { "bestFriend": [ { "address": ["*"] } ] }
"""


def is_node_object_template(var: Any) -> TypeGuard[NodeObjectTemplate]:
    """
    Type guard to check if a value is a valid node object template.
    """
    if not isinstance(var, dict):
        return False
    return all(isinstance(k, str) and isinstance(v, list) for (k, v) in var.items())  # type: ignore


SelectObject: TypeAlias = Dict[LogicVariable, SelectExpressionList]
"""
A select object in a FlureeQL query.
A select object maps logic variables to arrays of select expressions.
Each logic variable corresponds to a set of subjects, and for each subject,
a JSON object is constructed based on the select expressions.

Example Queries:
    { "?s": [ "name", { "bestFriend": ["*"] } ] }
"""


def is_select_object(var: Any) -> TypeGuard[SelectObject]:
    """
    Type guard to check if a value is a valid select object.
    """
    if not isinstance(var, dict):
        return False
    return all(is_logic_variable(k) and isinstance(v, list) for k, v in var.items())  # type: ignore


SelectArrayElement: TypeAlias = Union[LogicVariable, SelectObject]
"""
An element in a select array in a FlureeQL query.
An element in a select array can be either a logic variable or a select object.

Example Queries:
    "?s"
    { "?s": ["*"] }
"""


def is_select_array_element(var: Any) -> TypeGuard[SelectArrayElement]:
    """
    Type guard to check if a value is a valid select array element.
    """
    return is_logic_variable(var) if isinstance(var, str) else is_select_object(var)


SelectArray: TypeAlias = List[SelectArrayElement]
"""
A select array in a FlureeQL query.
A select array is a list containing logic variables or select objects.
When using a select array, each element of the query results will be an array
containing the values for each element in the select array.

Example Queries:
    ["?s", "?name", "?friend"]
    [ { "?s": ["*"] }, { "?friend": ["*"] } ]
"""


def is_select_array(var: Any) -> TypeGuard[SelectArray]:
    """
    Type guard to check if a value is a valid select array.
    """
    if not isinstance(var, list):
        return False

    return all(is_select_array_element(v) for v in var)  # type: ignore


SelectClause: TypeAlias = Union[SelectObject, SelectArray]
"""
A select clause in a FlureeQL query.
A select clause can be either a select object or a select array.

Example Queries:
    - { "?s": [ "name", { "bestFriend": ["*"] } ] }
    - ["?s", "?name", "?friend"]
"""

__all__ = [
    "LogicVariable",
    "Predicate",
    "Wildcard",
    "SelectExpression",
    "SelectExpressionList",
    "NodeObjectTemplate",
    "SelectObject",
    "SelectArrayElement",
    "SelectArray",
    "is_logic_variable",
    "is_node_object_template",
    "is_select_object",
    "is_select_array_element",
    "is_select_array",
]
