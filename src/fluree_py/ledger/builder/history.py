from dataclasses import dataclass, replace
from typing import Any

from fluree_py.ledger.mixin import CommitableMixin, RequestMixin, WithContextMixin
from fluree_py.ledger.protocol.endpoint import HistoryClause, TimeClause, HistoryBuilder


@dataclass(frozen=True, kw_only=True)
class HistoryBuilderImpl(
    RequestMixin, WithContextMixin, CommitableMixin, HistoryBuilder
):
    endpoint: str
    ledger: str
    context: dict[str, Any] | None = None
    history: HistoryClause | None = None
    t: TimeClause | None = None
    commit_details: bool | None = None

    def with_history(self, history: HistoryClause) -> "HistoryBuilderImpl":
        return replace(self, history=history)

    def with_t(self, t: TimeClause) -> "HistoryBuilderImpl":
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
