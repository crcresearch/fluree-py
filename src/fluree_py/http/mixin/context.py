"""Mixin for managing context data in Fluree operations."""

from typing import Any, Generic, TypeVar, cast

from fluree_py.http.mixin.utils import resolve_base_type_arg
from fluree_py.http.protocol.mixin import HasContextData

T = TypeVar("T", bound="HasContextData")
"""Ensure that the type we are trying to create has a context attribute."""


class WithContextMixin(Generic[T]):
    """Provides context management for Fluree operations."""

    def with_context(self, context: dict[str, Any]) -> T:
        """
        Update the operation's context with new data.

        Exceptions:
            TypeError: If the type parameter cannot be resolved.
        """
        resolved_type = resolve_base_type_arg(self.__class__, "WithContextMixin", T)
        if resolved_type is None or len(resolved_type) != 1:
            raise TypeError("Cannot resolve type for WithContextMixin")

        # Manually create a new instance with updated context
        updated_fields = self.__dict__.copy()
        updated_fields["context"] = context
        return cast("T", resolved_type[0](**updated_fields))
