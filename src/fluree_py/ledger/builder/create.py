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
    RequestMixin,
    WithContextMixin["CreateReadyToCommitImpl"],
    WithInsertMixin["CreateReadyToCommitImpl"],
    CommitableMixin["CreateReadyToCommitImpl"],
    CreateReadyToCommit,
):
    endpoint: str
    ledger: str
    data: JsonObject | JsonArray | None
    context: dict[str, Any] | None = None

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger, "insert": self.data}
        return result


@dataclass(frozen=True, kw_only=True)
class CreateBuilderImpl(
    WithContextMixin["CreateBuilderImpl"],
    WithInsertMixin[CreateReadyToCommitImpl],
    CreateBuilder,
):
    endpoint: str
    ledger: str
    data: JsonObject | JsonArray | None = None
    context: dict[str, Any] | None = None
