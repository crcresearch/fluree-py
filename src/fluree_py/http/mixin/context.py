"""Mixin for managing context data in Fluree operations."""

from typing import Any, Generic, Protocol, TypeVar, cast

from fluree_py.http.mixin.utils import InvalidArgumentCountError, resolve_base_type_arg
from fluree_py.logging import logger


# Protocol definitions for context mixin
class HasContextData(Protocol):
    """Protocol for objects that have context data."""

    context: dict[str, Any] | None


T_co = TypeVar("T_co", bound="HasContextData", covariant=True)


class SupportsContext(Generic[T_co], Protocol):
    """Protocol for objects that support context operations."""

    context: dict[str, Any] | None

    def with_context(self, context: dict[str, Any]) -> T_co:
        """Set the context for this operation."""
        ...


class WithContextMixin(Generic[T_co]):
    """Provides context management for Fluree operations."""

    def with_context(self, context: dict[str, Any]) -> T_co:
        """
        Update the operation's context with new data.

        Exceptions:
            TypeError: If the type parameter cannot be resolved.
        """
        logger.debug("with_context", context=context)
        resolved_type = resolve_base_type_arg(self.__class__, "WithContextMixin", T_co)
        if len(resolved_type) != 1:
            raise InvalidArgumentCountError(self.__class__.__name__, "WithContextMixin", resolved_type)

        # Manually create a new instance with updated context
        updated_fields = self.__dict__.copy()
        updated_fields["context"] = context
        return cast("T_co", resolved_type[0](**updated_fields))
