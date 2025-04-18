"""Mixins for committing transactions to the Fluree ledger."""

from typing import Protocol, TypeVar

from httpx import AsyncClient, Client

from fluree_py.http.mixin.request import WithRequestMixin
from fluree_py.http.mixin.response import (
    ResponseHandlingMixin,
    SupportsFromResponse,
    SupportsResponseHandling,
)
from fluree_py.logging import logger

T_Success = TypeVar("T_Success", bound=SupportsFromResponse)


class SupportsCommit(SupportsResponseHandling, Protocol):
    """Protocol for objects that support synchronous commit operations."""

    def commit(self) -> SupportsFromResponse:
        """
        Execute the transaction synchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        ...


class SupportsAsyncCommit(SupportsResponseHandling, Protocol):
    """Protocol for objects that support asynchronous commit operations."""

    async def acommit(self) -> SupportsFromResponse:
        """
        Execute the transaction asynchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        ...


class SupportsCommitable(
    SupportsCommit,
    SupportsAsyncCommit,
    Protocol,
):
    """Protocol for objects that support both sync and async commit operations."""


class CommitMixin(WithRequestMixin, ResponseHandlingMixin[T_Success], SupportsCommit):
    """Synchronous commit functionality for Fluree transactions."""

    def commit(self) -> T_Success:
        """
        Execute the transaction synchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        request = self.get_request()
        logger.info("commit_request", method=request.method, url=str(request.url))
        with Client() as client:
            response = client.send(request)
        logger.info("commit_response", status_code=response.status_code, elapsed=response.elapsed)

        return self.handle_response(response)


class AsyncCommitMixin(WithRequestMixin, ResponseHandlingMixin[T_Success], SupportsAsyncCommit):
    """Asynchronous commit functionality for Fluree transactions."""

    async def acommit(self) -> T_Success:
        """
        Execute the transaction asynchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        request = self.get_request()
        logger.info("async_commit_request", method=request.method, url=str(request.url))
        async with AsyncClient() as client:
            response = await client.send(request)
        logger.info("async_commit_response", status_code=response.status_code, elapsed=response.elapsed)

        return self.handle_response(response)


class CommitableMixin(CommitMixin[T_Success], AsyncCommitMixin[T_Success]):
    """Combines synchronous and asynchronous commit capabilities."""
