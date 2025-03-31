from typing import Generic, TypeVar, cast

from fluree_py.ledger.mixin.utils import resolve_base_class_reference
from fluree_py.ledger.protocol.mixin.where import HasWhereData
from fluree_py.query.where.types import WhereClause

T = TypeVar("T", bound="HasWhereData")


class WithWhereMixin(Generic[T]):
    def with_where(self: T, clause: WhereClause) -> T:
        resolved_type = resolve_base_class_reference(self.__class__, "WithWhereMixin")

        # Create a new instance of the resolved type
        updated_fields = self.__dict__.copy()
        updated_fields["where"] = clause
        return cast(T, resolved_type(**updated_fields))
