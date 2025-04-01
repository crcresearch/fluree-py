from typing import TypeAlias
from fluree_py.types.common import Subject

# History Clause
PropertyConstraint: TypeAlias = str
PropertyConstraintClause: TypeAlias = tuple[
    Subject | None, PropertyConstraint
]

ObjectConstraint: TypeAlias = str
ObjectConstraintClause: TypeAlias = tuple[
    Subject | None, PropertyConstraint, ObjectConstraint
]

HistoryClause: TypeAlias = (
    Subject | PropertyConstraintClause | ObjectConstraintClause
)
