from dataclasses import dataclass, replace
from typing import Any, Dict, Optional, Protocol, Self


class SupportsContext(Protocol):
    def with_context(self, context: Dict[str, Any]) -> Self: ...


@dataclass(frozen=True, kw_only=True)
class WithContextMixin:
    context: Optional[Dict[str, Any]] = None

    def with_context(self, context: Dict[str, Any]) -> Self:
        return replace(self, context=context)

    @property
    def context_json(self) -> Dict[str, Any]:
        return {"@context": self.context} if self.context else {}
