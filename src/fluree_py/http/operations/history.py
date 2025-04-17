"""History operation protocols and implementations."""

from dataclasses import dataclass, replace
from typing import Any, Protocol, Self

from fluree_py.http.mixin import WithContextMixin
from fluree_py.http.mixin.commit import CommitableMixin, SupportsCommitable
from fluree_py.http.mixin.context import SupportsContext
from fluree_py.logging import logger
from fluree_py.types.common import TimeClause
from fluree_py.types.http.history import HistoryClause


class HistoryBuilder(
    SupportsCommitable,
    SupportsContext["HistoryBuilder"],
    Protocol,
):
    """Protocol for history builders."""

    def with_history(self, history: HistoryClause) -> Self:
        """Set the history clause for the operation."""
        ...

    def with_t(self, t: TimeClause) -> Self:
        """Set the time clause for the operation."""
        ...

    def with_commit_details(self, commit_details: bool) -> Self:
        """Include commit details in the response."""
        ...


@dataclass(frozen=True, kw_only=True)
class HistoryBuilderImpl(
    CommitableMixin,
    WithContextMixin["HistoryBuilderImpl"],
    HistoryBuilder,
):
    """Implementation of a history query builder."""

    endpoint: str
    ledger: str
    context: dict[str, Any] | None = None
    history: HistoryClause | None = None
    t: TimeClause | None = None
    commit_details: bool | None = None

    def __post_init__(self) -> None:
        logger.info(
            "history_builder_initialized",
            endpoint=self.endpoint,
            ledger=self.ledger,
            context=self.context,
            history=self.history,
            t=self.t,
            commit_details=self.commit_details,
        )

    def with_history(self, history: HistoryClause) -> "HistoryBuilderImpl":
        return replace(self, history=history)

    def with_t(self, t: TimeClause) -> "HistoryBuilderImpl":
        return replace(self, t=t)

    def with_commit_details(self, commit_details: bool) -> "HistoryBuilderImpl":
        return replace(self, commit_details=commit_details)

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.context:
            result["@context"] = self.context
        result |= {"from": self.ledger, "history": self.history, "t": self.t}
        if self.commit_details:
            result["commitDetails"] = self.commit_details
        return result
