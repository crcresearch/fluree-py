from dataclasses import dataclass, replace
from typing import Any, Dict, List, Optional, Protocol

import httpx

from fluree_py.context import SupportsContext, WithContextMixin


class SupportsHistory(Protocol):
    def history(self) -> "HistoryBuilder": ...


class HistoryBuilder(SupportsContext, Protocol):
    def with_history(self, history: List[str]) -> "HistoryBuilder": ...
    def with_t(self, t: int) -> "HistoryBuilder": ...
    def with_commit_details(self, commit_details: bool) -> "HistoryBuilder": ...
    def request(self) -> httpx.Request: ...
    def commit(self) -> Dict[str, Any]: ...


@dataclass(frozen=True, kw_only=True)
class HistoryBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str
    history: Optional[List[str]] = None
    t: Optional[int] = None
    commit_details: Optional[bool] = None

    def with_context(self, context: Dict[str, Any]) -> "HistoryBuilderImpl":
        return replace(self, context=context)

    def with_history(self, history: List[str]) -> "HistoryBuilderImpl":
        return replace(self, history=history)

    def with_t(self, t: int) -> "HistoryBuilderImpl":
        return replace(self, t=t)

    @property
    def commit_details_json(self) -> Dict[str, Any]:
        return {"commitDetails": self.commit_details} if self.commit_details else {}

    @property
    def json(self) -> Dict[str, Any]:
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

    def commit(self) -> Dict[str, Any]:
        response = httpx.post(self.endpoint, json=self.json)
        response.raise_for_status()
        return response.json()
