from typing import Any, Protocol

from fluree_py.http.protocol.mixin import SupportsCommit, SupportsContext, SupportsRequestCreation


class SupportsHistory(Protocol):
    def history(self) -> "HistoryBuilder": ...


class HistoryBuilder(
    SupportsContext, SupportsRequestCreation, SupportsCommit, Protocol
):
    def with_history(self, history: list[str | None]) -> "HistoryBuilder": ...
    def with_t(self, t: dict[str, Any]) -> "HistoryBuilder": ...
    def with_commit_details(self, commit_details: bool) -> "HistoryBuilder": ...
