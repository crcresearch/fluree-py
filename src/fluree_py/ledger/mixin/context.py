"""Mixin for managing context data in Fluree operations."""

from typing import Any, Generic, TypeVar, cast
from fluree_py.ledger.mixin.utils import resolve_base_class_reference
from fluree_py.ledger.protocol.mixin import HasContextData


T = TypeVar("T", bound="HasContextData")
"""Ensure that the type we are trying to create has a context attribute."""


class WithContextMixin(Generic[T]):
    """Provides context management for Fluree operations."""

    def with_context(self, context: dict[str, Any]) -> T:
        """Updates the operation's context with new data.

        Exceptions:
            TypeError: If the type parameter cannot be resolved.
        """
        resolved_type = resolve_base_class_reference(self.__class__, "WithContextMixin")

        # Manually create a new instance with updated context
        updated_fields = self.__dict__.copy()
        updated_fields["context"] = context
        return cast(T, resolved_type(**updated_fields))
