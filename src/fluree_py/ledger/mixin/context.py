from dataclasses import dataclass, replace
from typing import Any, Self

from fluree_py.ledger.protocol.context import SupportsContext


@dataclass(frozen=True, kw_only=True)
class WithContextMixin(SupportsContext):
    context: dict[str, Any] | None = None

    def with_context(self, context: dict[str, Any]) -> Self:
        return replace(self, context=context)
