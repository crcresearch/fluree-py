"""Mixin for handling where clause operations in Fluree queries."""

from typing import Generic, Protocol, TypeVar, cast

from fluree_py.http.mixin.utils import resolve_base_class_reference
from fluree_py.types.query.where import WhereClause


# Protocol definitions for where mixin
class HasWhereData(Protocol):
    """Protocol for objects that have where clause data."""

    where: WhereClause | None


T_co = TypeVar("T_co", bound="HasWhereData", covariant=True)


class SupportsWhere(Generic[T_co], Protocol):
    """Protocol for objects that support where clause operations."""

    where: WhereClause | None = None

    def with_where(self, clause: WhereClause) -> T_co:
        """Set the where clause for the operation."""
        ...


class WithWhereMixin(Generic[T_co]):
    """Provide where clause capabilities for Fluree queries."""

    def with_where(self, clause: WhereClause) -> T_co:
        """
        Update the query with a new where clause.

        Exceptions:
            TypeError: If the type parameter cannot be resolved.
        """
        resolved_type = resolve_base_class_reference(self.__class__, "WithWhereMixin")

        # Create a new instance of the resolved type
        updated_fields = self.__dict__.copy()
        updated_fields["where"] = clause
        return cast("T_co", resolved_type(**updated_fields))
