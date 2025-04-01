from typing import Any, Literal, TypeAlias, TypeGuard, TypedDict, Union


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


TimeClause = Union[TimeConstraint, TimeCommit]


def is_time_clause(t: Any) -> TypeGuard[TimeClause]:
    """Checks if a value is a valid time clause."""
    return is_time_constraint(t) or is_time_commit(t)


# History Clause
SubjectConstraint: TypeAlias = str

PropertyConstraint: TypeAlias = str
PropertyConstraintClause: TypeAlias = tuple[
    SubjectConstraint | None, PropertyConstraint
]

ObjectConstraint: TypeAlias = str
ObjectConstraintClause: TypeAlias = tuple[
    SubjectConstraint | None, PropertyConstraint, ObjectConstraint
]

HistoryClause: TypeAlias = (
    SubjectConstraint | PropertyConstraintClause | ObjectConstraintClause
)
