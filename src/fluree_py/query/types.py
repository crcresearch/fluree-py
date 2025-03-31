from typing import Literal, TypeAlias

# A predicate identifier in a FlureeQL query.
# A predicate is a string that identifies a property or relationship in the database.
#
# Examples:
#     "schema:name"
#     "schema:age"
#     "schema:friend"
Predicate: TypeAlias = str


# The wildcard symbol in a FlureeQL query.
# The wildcard symbol, "*", represents all predicates of a subject.
Wildcard: TypeAlias = Literal["*"]
