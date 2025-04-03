"""Mixin for handling data insertion operations in Fluree."""

from typing import Generic, TypeVar, cast

from fluree_py.http.mixin.utils import resolve_base_class_reference
from fluree_py.http.protocol.mixin import HasInsertData
from fluree_py.types.common import JsonArray, JsonObject

T = TypeVar("T", bound="HasInsertData")


class WithInsertMixin(Generic[T]):
    """Provides data insertion capabilities for Fluree operations."""

    def with_insert(self, data: JsonObject | JsonArray) -> T:
        """
        Update the operation with new data to be inserted.

        Exceptions:
            TypeError: If the type parameter cannot be resolved.
        """
        resolved_type = resolve_base_class_reference(self.__class__, "WithInsertMixin")

        # Create a new instance of the resolved type
        updated_fields = self.__dict__.copy()
        updated_fields["data"] = data
        return cast("T", resolved_type(**updated_fields))
