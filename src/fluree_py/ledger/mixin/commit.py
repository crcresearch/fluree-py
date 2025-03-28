from typing import Any, Generic, TypeVar

import httpx

from fluree_py.ledger.protocol.commit import SupportsAsyncCommit, SupportsCommit
from fluree_py.ledger.protocol.request import SupportsRequestCreation

T = TypeVar("T", bound=SupportsRequestCreation)


class CommitMixin(SupportsCommit, Generic[T]):
    def commit(self: T) -> dict[str, Any]:
        request = self.get_request()
        with httpx.Client() as client:
            response = client.send(request)
        response.raise_for_status()
        return response.json()


class AsyncCommitMixin(SupportsAsyncCommit, Generic[T]):
    async def acommit(self: T) -> dict[str, Any]:
        request = self.get_request()
        async with httpx.AsyncClient() as client:
            response = await client.send(request)
        response.raise_for_status()
        return response.json()


class CommitableMixin(CommitMixin[T], AsyncCommitMixin[T], Generic[T]):
    pass
