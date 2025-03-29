from dataclasses import dataclass, replace
from typing import Self

from fluree_py.ledger.protocol.context import SupportsContext
from fluree_py.types import JsonObject


@dataclass(frozen=True, kw_only=True)
class WithContextMixin(SupportsContext):
    context: JsonObject | None = None

    def with_context(self, context: JsonObject) -> Self:
        return replace(self, context=context)
