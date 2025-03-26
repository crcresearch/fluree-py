from typing import Any, Protocol, Self

from fluree_py.ledger.protocol.base import BaseBuilder, BaseReadyToCommit


class HistoryBuilder(BaseBuilder, BaseReadyToCommit, Protocol):
    """Protocol for history builders."""

    def with_history(self, history: list[str | None]) -> Self: ...
    def with_t(self, t: dict[str, Any]) -> Self: ...
    def with_commit_details(self, commit_details: bool) -> Self: ...
