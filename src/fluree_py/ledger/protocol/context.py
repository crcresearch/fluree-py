from typing import Any, Protocol, Self


class SupportsContext(Protocol):
    def with_context(self, context: dict[str, Any]) -> Self: ...
