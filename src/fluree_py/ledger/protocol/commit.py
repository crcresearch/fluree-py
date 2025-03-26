from typing import Any, Protocol


class SupportsCommit(Protocol):
    def commit(self) -> dict[str, Any]: ...


class SupportsAsyncCommit(Protocol):
    async def acommit(self) -> dict[str, Any]: ...


class SupportsCommitable(SupportsCommit, SupportsAsyncCommit, Protocol):
    pass
