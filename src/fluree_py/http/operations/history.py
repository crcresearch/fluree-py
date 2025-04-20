"""History operation protocols and implementations."""

from dataclasses import dataclass, replace
from typing import Any, ClassVar, Protocol, Self

from fluree_py.http.mixin.commit import CommitableMixin, SupportsCommitable
from fluree_py.http.mixin.context import HasContextData, SupportsContext
from fluree_py.http.mixin.response import SupportsFromResponse, SupportsRaisingFromResponse
from fluree_py.http.mixin.utils import make_setter
from fluree_py.http.response import FlureeResponse, MissingTransactionError
from fluree_py.logging import logger
from fluree_py.types.common import TimeClause
from fluree_py.types.http.history import HistoryClause


# Protocol definitions for history operations
class HistoryBuilder(
    SupportsCommitable[FlureeResponse],
    HasContextData,
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


# Implementation of history operations
@dataclass(frozen=True, kw_only=True)
class HistoryBuilderImpl(CommitableMixin[FlureeResponse], HistoryBuilder):
    """Implementation of a history query builder."""

    __response_errors__: ClassVar[list[type[SupportsRaisingFromResponse]]] = [MissingTransactionError]
    __response_payload__: ClassVar[type[SupportsFromResponse]] = FlureeResponse

    endpoint: str
    ledger: str
    context: dict[str, Any] | None = None
    history: HistoryClause | None = None
    t: TimeClause | None = None
    commit_details: bool | None = None

    def __post_init__(self) -> None:
        """Log the initialization of the history builder."""
        logger.info(
            "history_builder_initialized",
            endpoint=self.endpoint,
            ledger=self.ledger,
            context=self.context,
            history=self.history,
            t=self.t,
            commit_details=self.commit_details,
        )

    with_context = make_setter("with_context", "context")

    def with_history(self, history: HistoryClause) -> "HistoryBuilderImpl":
        """Set the history clause for the operation."""
        return replace(self, history=history)

    def with_t(self, t: TimeClause) -> "HistoryBuilderImpl":
        """Set the time clause for the operation."""
        return replace(self, t=t)

    def with_commit_details(self, commit_details: bool) -> "HistoryBuilderImpl":
        """Set the commit details for the operation."""
        return replace(self, commit_details=commit_details)

    def get_url(self) -> str:
        """Get the endpoint URL for the history operation."""
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        """Build the request payload for the history operation."""
        result: dict[str, Any] = {}
        if self.context:
            result["@context"] = self.context
        result |= {"from": self.ledger, "history": self.history, "t": self.t}
        if self.commit_details:
            result["commitDetails"] = self.commit_details
        return result
