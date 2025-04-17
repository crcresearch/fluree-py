from typing import Protocol, TypeVar

from fluree_py.http.protocol.mixin.response import (
    SupportsFromResponse,
    SupportsRaisingFromResponse,
    SupportsResponseHandling,
)

T_Success_co = TypeVar("T_Success_co", bound=SupportsFromResponse, covariant=True)
T_Failure_co = TypeVar("T_Failure_co", bound=SupportsRaisingFromResponse, covariant=True)


class SupportsCommit(SupportsResponseHandling[T_Success_co, T_Failure_co], Protocol[T_Success_co, T_Failure_co]):
    """Protocol for objects that support synchronous commit operations."""

    def commit(self) -> T_Success_co:
        """
        Execute the transaction synchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        ...


class SupportsAsyncCommit(SupportsResponseHandling[T_Success_co, T_Failure_co], Protocol[T_Success_co, T_Failure_co]):
    """Protocol for objects that support asynchronous commit operations."""

    async def acommit(self) -> T_Success_co:
        """
        Execute the transaction asynchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        ...


class SupportsCommitable(
    SupportsCommit[T_Success_co, T_Failure_co],
    SupportsAsyncCommit[T_Success_co, T_Failure_co],
    Protocol[T_Success_co, T_Failure_co],
):
    """Protocol for objects that support both sync and async commit operations."""
