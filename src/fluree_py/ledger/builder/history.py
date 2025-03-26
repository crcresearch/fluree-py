from dataclasses import dataclass, replace
from typing import Any


from fluree_py.ledger.mixin import CommitableMixin, WithContextMixin, RequestMixin


@dataclass(frozen=True, kw_only=True)
class HistoryBuilderImpl(RequestMixin, WithContextMixin, CommitableMixin):
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
