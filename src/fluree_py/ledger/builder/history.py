from dataclasses import dataclass, replace
from typing import Any

from fluree_py.ledger.mixin import CommitableMixin, RequestMixin, WithContextMixin
from fluree_py.ledger.protocol.endpoint import HistoryBuilder
from fluree_py.query.history import HistoryClause, TimeClause


@dataclass(frozen=True, kw_only=True)
class HistoryBuilderImpl(
    RequestMixin,
    WithContextMixin["HistoryBuilderImpl"],
    CommitableMixin["HistoryBuilderImpl"],
    HistoryBuilder,
):
    """Implementation of a history query builder."""

    endpoint: str
    ledger: str
    context: dict[str, Any] | None = None
    history: HistoryClause | None = None
    t: TimeClause | None = None
    commit_details: bool | None = None

    def with_history(self, history: HistoryClause) -> "HistoryBuilderImpl":
        """Add history clause to the query."""
        return replace(self, history=history)

    def with_t(self, t: TimeClause) -> "HistoryBuilderImpl":
        """Add time clause to the query."""
        return replace(self, t=t)

    def with_commit_details(self, commit_details: bool) -> "HistoryBuilderImpl":
        """Add commit details flag to the query."""
        return replace(self, commit_details=commit_details)

    def get_url(self) -> str:
        """Get the endpoint URL for the history query operation."""
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        """Build the request payload for the history query operation."""
        result: dict[str, Any] = {}
        if self.context:
            result["@context"] = self.context
        result |= {"from": self.ledger, "history": self.history, "t": self.t}
        if self.commit_details:
            result["commitDetails"] = self.commit_details
        return result
