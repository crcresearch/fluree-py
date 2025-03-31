from typing import Any, Generic, Protocol, TypeVar


class HasContextData(Protocol):
    """Protocol for objects that have context data."""

    context: dict[str, Any] | None


T = TypeVar("T", bound="HasContextData", covariant=True)


class SupportsContext(Generic[T], Protocol):
    """Protocol for objects that support context operations."""

    context: dict[str, Any] | None

    def with_context(self, context: dict[str, Any]) -> T: ...
