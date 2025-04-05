"""Protocols and types for querying historical data in the Fluree ledger."""

from typing import Protocol, Self

from fluree_py.http.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
)
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
