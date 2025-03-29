from typing import Any, Literal, Protocol, Self, TypeAlias, TypeGuard, TypedDict, Union

from fluree_py.ledger.protocol.base import BaseBuilder, BaseReadyToCommit

TimeCommit: TypeAlias = int

def is_time_commit(t: Any) -> TypeGuard[TimeCommit]:
    return isinstance(t, int) and t >= 0

LatestTimeConstraint = Literal["latest"]

TimeConstraint = TypedDict('TimeConstraint', {
    'at': TimeCommit | LatestTimeConstraint,
    'from': TimeCommit | LatestTimeConstraint,
    'to': TimeCommit | LatestTimeConstraint
}, total=False)

def is_time_constraint(t: Any) -> TypeGuard[TimeConstraint]:
    return isinstance(t, dict) and all(is_time_commit(v) or v == "latest" for v in t.values())

TimeClause = Union[TimeConstraint, TimeCommit]

def is_time_clause(t: Any) -> TypeGuard[TimeClause]:
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


class HistoryBuilder(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for history builders."""

    def with_history(self, history: HistoryClause) -> Self: ...
    def with_t(self, t: TimeClause) -> Self: ...
    def with_commit_details(self, commit_details: bool) -> Self: ...
