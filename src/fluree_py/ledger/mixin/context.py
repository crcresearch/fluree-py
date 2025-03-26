from dataclasses import dataclass, replace
from typing import Any, Self


@dataclass(frozen=True, kw_only=True)
class WithContextMixin:
    context: dict[str, Any] | None = None

    def with_context(self, context: dict[str, Any]) -> Self:
        return replace(self, context=context)
