"""Mixin for handling data insertion operations in Fluree."""

from typing import Generic, Protocol, TypeVar, cast

from fluree_py.http.mixin.utils import resolve_base_class_reference
from fluree_py.logging import logger
from fluree_py.types.common import JsonArray, JsonObject


# Protocol definitions for insert mixin
class HasInsertData(Protocol):
    """Protocol for objects that have insert data."""

    data: JsonObject | JsonArray | None


T_co = TypeVar("T_co", bound="HasInsertData", covariant=True)


class SupportsInsert(Generic[T_co], Protocol):
    """Protocol for objects that support insert operations."""

    data: JsonObject | JsonArray | None

    def with_insert(self, data: JsonObject | JsonArray) -> T_co:
        """Set the insert data for the operation."""
        ...


class WithInsertMixin(Generic[T_co]):
    """Provides data insertion capabilities for Fluree operations."""

    def with_insert(self, data: JsonObject | JsonArray) -> T_co:
        """
        Update the operation with new data to be inserted.

        Exceptions:
            TypeError: If the type parameter cannot be resolved.
        """
        logger.debug("with_insert", data=data)
        resolved_type = resolve_base_class_reference(self.__class__, "WithInsertMixin")

        # Create a new instance of the resolved type
        updated_fields = self.__dict__.copy()
        updated_fields["data"] = data
        return cast("T_co", resolved_type(**updated_fields))
