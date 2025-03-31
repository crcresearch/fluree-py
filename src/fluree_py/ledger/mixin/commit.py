from typing import Generic, TypeVar

from httpx import AsyncClient, Client

from fluree_py.ledger.protocol.mixin.commit import SupportsAsyncCommit, SupportsCommit
from fluree_py.ledger.protocol.mixin.request import SupportsRequestCreation
from fluree_py.response import FlureeResponse

T = TypeVar("T", bound=SupportsRequestCreation)


class CommitMixin(SupportsCommit, Generic[T]):
    def commit(self: T) -> FlureeResponse:
        request = self.get_request()
        with Client() as client:
            response = client.send(request)
        return FlureeResponse(response=response)


class AsyncCommitMixin(SupportsAsyncCommit, Generic[T]):
    async def acommit(self: T) -> FlureeResponse:
        request = self.get_request()
        async with AsyncClient() as client:
            response = await client.send(request)
        return FlureeResponse(response=response)


class CommitableMixin(CommitMixin[T], AsyncCommitMixin[T], Generic[T]):
    pass
