"""Mixins for committing transactions to the Fluree ledger."""

from typing import TypeVar

from httpx import AsyncClient, Client

from fluree_py.http.mixin.request import WithRequestMixin
from fluree_py.http.mixin.response import ResponseHandlingMixin
from fluree_py.http.protocol.mixin.commit import SupportsAsyncCommit, SupportsCommit
from fluree_py.http.protocol.mixin.response import SupportsFromResponse, SupportsRaisingFromResponse

T_Success = TypeVar("T_Success", bound=SupportsFromResponse)
T_Failure = TypeVar("T_Failure", bound=SupportsRaisingFromResponse)


class CommitMixin(WithRequestMixin, ResponseHandlingMixin[T_Success, T_Failure], SupportsCommit[T_Success, T_Failure]):
    """Synchronous commit functionality for Fluree transactions."""

    def commit(self) -> T_Success:
        """
        Execute the transaction synchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        request = self.get_request()
        with Client() as client:
            response = client.send(request)

        return self.handle_response(response)


class AsyncCommitMixin(
    WithRequestMixin, ResponseHandlingMixin[T_Success, T_Failure], SupportsAsyncCommit[T_Success, T_Failure]
):
    """Asynchronous commit functionality for Fluree transactions."""

    async def acommit(self) -> T_Success:
        """
        Execute the transaction asynchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        request = self.get_request()
        async with AsyncClient() as client:
            response = await client.send(request)

        return self.handle_response(response)


class CommitableMixin(CommitMixin[T_Success, T_Failure], AsyncCommitMixin[T_Success, T_Failure]):
    """Combines synchronous and asynchronous commit capabilities."""
