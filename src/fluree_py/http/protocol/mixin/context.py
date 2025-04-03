from typing import Any, Generic, Protocol, TypeVar


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
