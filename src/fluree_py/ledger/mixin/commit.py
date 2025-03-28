from typing import Generic, TypeVar

from httpx import AsyncClient, Client, Response

from fluree_py.ledger.protocol.commit import SupportsAsyncCommit, SupportsCommit
from fluree_py.ledger.protocol.request import SupportsRequestCreation

T = TypeVar("T", bound=SupportsRequestCreation)


class CommitMixin(SupportsCommit, Generic[T]):
    def commit(self) -> Response:
        request = self.get_request()
        with Client() as client:
            response = client.send(request)
        response.raise_for_status()
        return response


class AsyncCommitMixin(SupportsAsyncCommit, Generic[T]):
    async def acommit(self) -> Response:
        request = self.get_request()
        async with AsyncClient() as client:
            response = await client.send(request)
        response.raise_for_status()
        return response


class CommitableMixin(CommitMixin[T], AsyncCommitMixin[T], Generic[T]):
    pass
