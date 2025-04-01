from typing import Any, Literal, TypeAlias, TypeGuard, TypedDict


# Type alias for JSON-serializable data that can be either a single dict or a list of dicts
JsonObject: TypeAlias = dict[str, Any]
JsonArray: TypeAlias = list[Any]

LedgerName: TypeAlias = str
"""A textal name for the ledger."""


Subject: TypeAlias = str
"""A textual identifier for a subject."""

Context: TypeAlias = JsonObject
"""
A W3C JSON-LD context for a FlureeQL request.
"""

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

### Time Types
TimeCommit: TypeAlias = int


def is_time_commit(t: Any) -> TypeGuard[TimeCommit]:
    """Checks if a value is a valid time commit."""
    return isinstance(t, int) and t >= 0


LatestTimeConstraint = Literal["latest"]

TimeConstraint = TypedDict(
    "TimeConstraint",
    {
        "at": TimeCommit | LatestTimeConstraint,
        "from": TimeCommit | LatestTimeConstraint,
        "to": TimeCommit | LatestTimeConstraint,
    },
    total=False,
)


def is_time_constraint(t: Any) -> TypeGuard[TimeConstraint]:
    """Checks if a value is a valid time constraint."""
    return isinstance(t, dict) and all(
        is_time_commit(v) or v == "latest"
        for v in t.values()  # type: ignore
    )


TimeClause: TypeAlias = TimeConstraint | TimeCommit
"""
A time clause for a FlureeQL query. It is either a commit number or a constraint on the commit.

Examples:
    - {"t": {"at": 123}}
    - {"t": {"from": 123, "to": 456}}
    - {"t": 123}
"""
