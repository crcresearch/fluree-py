from typing import Any, Protocol


class SupportsCommit(Protocol):
    def commit(self) -> dict[str, Any]: ...
