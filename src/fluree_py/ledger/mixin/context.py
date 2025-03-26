from dataclasses import dataclass, replace
from typing import Any, Self


@dataclass(frozen=True, kw_only=True)
class WithContextMixin:
    context: dict[str, Any] | None = None

    def with_context(self, context: dict[str, Any]) -> Self:
        return replace(self, context=context)

    @property
    def context_json(self) -> dict[str, Any]:
        return {"@context": self.context} if self.context else {}
