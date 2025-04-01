"""Types used in FlureeQL queries."""

from typing import Literal, TypeAlias


Predicate: TypeAlias = str
"""
 A predicate identifier in a FlureeQL query.
 A predicate is a string that identifies a property or relationship in the database.

 Examples:
     "schema:name"
     "schema:age"
     "schema:friend"
"""

Wildcard: TypeAlias = Literal["*"]
"""
A wildcard character in a FlureeQL query.
The wildcard character is used to select all predicates of a subject.

Examples:
    "*"
"""
