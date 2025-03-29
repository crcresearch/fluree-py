from dataclasses import dataclass
from typing import Any

from fluree_py.ledger.mixin import CommitableMixin, RequestMixin, WithContextMixin
from fluree_py.types import JsonArray, JsonObject


@dataclass(frozen=True, kw_only=True)
class CreateBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str

    def with_insert(self, data: JsonObject | JsonArray) -> "CreateReadyToCommitImpl":
        return CreateReadyToCommitImpl(
            endpoint=self.endpoint,
            ledger=self.ledger,
            data=data,
            context=self.context,
        )


@dataclass(frozen=True, kw_only=True)
class CreateReadyToCommitImpl(RequestMixin, WithContextMixin, CommitableMixin):
    endpoint: str
    ledger: str
    data: JsonObject | JsonArray

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger, "insert": self.data}
        return result
