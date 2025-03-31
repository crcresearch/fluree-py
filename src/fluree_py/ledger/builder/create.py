from dataclasses import dataclass
from typing import Any

from fluree_py.ledger.mixin import (
    CommitableMixin,
    RequestMixin,
    WithContextMixin,
    WithInsertMixin,
)
from fluree_py.ledger.protocol.endpoint.create import CreateBuilder, CreateReadyToCommit
from fluree_py.types import JsonArray, JsonObject


@dataclass(frozen=True, kw_only=True)
class CreateReadyToCommitImpl(
    RequestMixin, WithContextMixin, CommitableMixin, CreateReadyToCommit
):
    endpoint: str
    ledger: str
    data: JsonObject | JsonArray | None = None
    context: dict[str, Any] | None = None

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger, "insert": self.data}
        return result


@dataclass(frozen=True, kw_only=True)
class CreateBuilderImpl(
    WithContextMixin,
    WithInsertMixin["CreateReadyToCommitImpl"],
    CreateBuilder,
):
    endpoint: str
    ledger: str
    data: JsonObject | JsonArray | None = None
    context: dict[str, Any] | None = None
