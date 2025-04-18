"""Mixin for handling where clause operations in Fluree queries."""

from typing import Generic, TypeVar, cast

from fluree_py.http.mixin.utils import resolve_base_type_arg
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
        resolved_type = resolve_base_type_arg(self.__class__, "WithWhereMixin", T)
        if resolved_type is None or len(resolved_type) != 1:
            raise TypeError("Cannot resolve type for WithWhereMixin")

        # Create a new instance of the resolved type
        updated_fields = self.__dict__.copy()
        updated_fields["where"] = clause
        return cast("T", resolved_type[0](**updated_fields))
