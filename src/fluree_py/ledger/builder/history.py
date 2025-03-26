from dataclasses import dataclass, replace
from typing import Any

import httpx

from fluree_py.ledger.mixin.context import WithContextMixin
from fluree_py.ledger.mixin.request_builder import WithRequestMixin


@dataclass(frozen=True, kw_only=True)
class HistoryBuilderImpl(WithRequestMixin, WithContextMixin):
    endpoint: str
    ledger: str
    history: list[str] | None = None
    t: dict[str, Any] | None = None
    commit_details: bool | None = None

    def with_history(self, history: list[str | None]) -> "HistoryBuilderImpl":
        return replace(self, history=history)

    def with_t(self, t: dict[str, Any]) -> "HistoryBuilderImpl":
        return replace(self, t=t)

    def with_commit_details(self, commit_details: bool) -> "HistoryBuilderImpl":
        return replace(self, commit_details=commit_details)

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result = {}
        if self.context:
            result["@context"] = self.context
        result |= {"from": self.ledger, "history": self.history, "t": self.t}
        if self.commit_details:
            result["commitDetails"] = self.commit_details
        return result

    def commit(self) -> dict[str, Any]:
        request = self.get_request()
        with httpx.Client() as client:
            response = client.send(request)
        response.raise_for_status()
        return response.json()
