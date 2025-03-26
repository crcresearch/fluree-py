from dataclasses import dataclass, replace
from typing import Any

import httpx

from fluree_py.ledger.mixin.context import WithContextMixin


@dataclass(frozen=True, kw_only=True)
class HistoryBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str
    history: list[str] | None = None
    t: dict[str, Any] | None = None
    commit_details: bool | None = None

    def with_context(self, context: dict[str, Any]) -> "HistoryBuilderImpl":
        return replace(self, context=context)

    def with_history(self, history: list[str | None]) -> "HistoryBuilderImpl":
        return replace(self, history=history)

    def with_t(self, t: dict[str, Any]) -> "HistoryBuilderImpl":
        return replace(self, t=t)

    def with_commit_details(self, commit_details: bool) -> "HistoryBuilderImpl":
        return replace(self, commit_details=commit_details)

    @property
    def commit_details_json(self) -> dict[str, Any]:
        return {"commitDetails": self.commit_details} if self.commit_details else {}

    @property
    def json(self) -> dict[str, Any]:
        return (
            self.context_json
            | {"from": self.ledger, "history": self.history, "t": self.t}
            | self.commit_details_json
        )

    def request(self) -> httpx.Request:
        return httpx.Request(
            "POST",
            self.endpoint,
            json=self.json,
        )

    def commit(self) -> dict[str, Any]:
        response = httpx.post(self.endpoint, json=self.json)
        response.raise_for_status()
        return response.json()
