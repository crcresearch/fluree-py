"""Mixin for handling where clause operations in Fluree queries."""

from typing import Generic, TypeVar, cast

from fluree_py.http.mixin.utils import resolve_base_class_reference
from fluree_py.http.protocol.mixin.where import HasWhereData
from fluree_py.types.query.where import WhereClause

T = TypeVar("T", bound="HasWhereData")


class WithWhereMixin(Generic[T]):
    """Provide where clause capabilities for Fluree queries."""

    def with_where(self, clause: WhereClause) -> T:
        """
        Update the query with a new where clause.

        Exceptions:
            TypeError: If the type parameter cannot be resolved.
        """
        resolved_type = resolve_base_class_reference(self.__class__, "WithWhereMixin")

        # Create a new instance of the resolved type
        updated_fields = self.__dict__.copy()
        updated_fields["where"] = clause
        return cast("T", resolved_type(**updated_fields))
