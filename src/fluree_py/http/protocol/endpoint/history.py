"""Protocols and types for querying historical data in the Fluree ledger."""

from typing import Protocol, Self

from fluree_py.http.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsRequestCreation,
)
from fluree_py.types.common import TimeClause
from fluree_py.types.http.history import HistoryClause


class HistoryBuilder(
    SupportsContext["HistoryBuilder"],
    SupportsRequestCreation,
    SupportsCommitable,
    Protocol,
):
    """Protocol for history builders."""

    def with_history(self, history: HistoryClause) -> Self: ...
    def with_t(self, t: TimeClause) -> Self: ...
    def with_commit_details(self, commit_details: bool) -> Self: ...
