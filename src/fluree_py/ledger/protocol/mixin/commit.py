from typing import Protocol

from fluree_py.response import FlureeResponse


class SupportsCommit(Protocol):
    def commit(self) -> FlureeResponse: ...


class SupportsAsyncCommit(Protocol):
    async def acommit(self) -> FlureeResponse: ...


class SupportsCommitable(SupportsCommit, SupportsAsyncCommit, Protocol):
    pass
