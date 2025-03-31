from typing import Any, Generic, Protocol, TypeVar


class HasContextData(Protocol):
    context: dict[str, Any] | None


T = TypeVar("T", bound="HasContextData", covariant=True)


class SupportsContext(Generic[T], Protocol):
    context: dict[str, Any] | None

    def with_context(self, context: dict[str, Any]) -> T: ...
