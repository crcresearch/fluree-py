from typing import Any, Protocol

from fluree_py.ledger.protocol.commit import SupportsCommitable
from fluree_py.ledger.protocol.context import SupportsContext
from fluree_py.ledger.protocol.request import SupportsRequestCreation


class HistoryBuilder(
    SupportsContext, SupportsRequestCreation, SupportsCommitable, Protocol
):
    def with_history(self, history: list[str | None]) -> "HistoryBuilder": ...
    def with_t(self, t: dict[str, Any]) -> "HistoryBuilder": ...
    def with_commit_details(self, commit_details: bool) -> "HistoryBuilder": ...
