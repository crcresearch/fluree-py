"""Mixins for committing transactions to the Fluree ledger."""

from typing import Protocol

from httpx import AsyncClient, Client

from fluree_py.http.mixin.request import WithRequestMixin
from fluree_py.http.response import FlureeResponse


# Protocol definitions for commit mixin
class SupportsCommit(Protocol):
    """Protocol for objects that support synchronous commit operations."""

    def commit(self) -> FlureeResponse: ...


class SupportsAsyncCommit(Protocol):
    """Protocol for objects that support asynchronous commit operations."""

    async def acommit(self) -> FlureeResponse: ...


class SupportsCommitable(SupportsCommit, SupportsAsyncCommit, Protocol):
    """Protocol for objects that support both sync and async commit operations."""


class CommitMixin(WithRequestMixin, SupportsCommit):
    """Synchronous commit functionality for Fluree transactions."""

    def commit(self) -> FlureeResponse:
        """
        Execute the transaction synchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        request = self.get_request()
        with Client() as client:
            response = client.send(request)
        return FlureeResponse(response=response)


class AsyncCommitMixin(WithRequestMixin, SupportsAsyncCommit):
    """Asynchronous commit functionality for Fluree transactions."""

    async def acommit(self) -> FlureeResponse:
        """
        Execute the transaction asynchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        request = self.get_request()
        async with AsyncClient() as client:
            response = await client.send(request)
        return FlureeResponse(response=response)


class CommitableMixin(CommitMixin, AsyncCommitMixin):
    """Combines synchronous and asynchronous commit capabilities."""
