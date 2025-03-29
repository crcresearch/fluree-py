from typing import Protocol, Self

from fluree_py.ledger.protocol.base import BaseBuilder, BaseReadyToCommit
from fluree_py.types import JsonObject


class HistoryBuilder(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for history builders."""

    def with_history(self, history: JsonObject) -> Self: ...
    def with_t(self, t: JsonObject) -> Self: ...
    def with_commit_details(self, commit_details: bool) -> Self: ...
