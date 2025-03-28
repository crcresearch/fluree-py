from typing import Protocol

from httpx import Response


class SupportsCommit(Protocol):
    def commit(self) -> Response: ...


class SupportsAsyncCommit(Protocol):
    async def acommit(self) -> Response: ...


class SupportsCommitable(SupportsCommit, SupportsAsyncCommit, Protocol):
    pass
