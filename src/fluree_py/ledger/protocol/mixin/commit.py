from typing import Protocol

from fluree_py.response import FlureeResponse


class SupportsCommit(Protocol):
    """Protocol for objects that support synchronous commit operations."""

    def commit(self) -> FlureeResponse:
        """Executes the transaction synchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        ...


class SupportsAsyncCommit(Protocol):
    """Protocol for objects that support asynchronous commit operations."""

    async def acommit(self) -> FlureeResponse:
        """Executes the transaction asynchronously.

        Exceptions:
            httpx.RequestError: If the HTTP request fails.
            TypeError: If the type parameter cannot be resolved.
        """
        ...


class SupportsCommitable(SupportsCommit, SupportsAsyncCommit, Protocol):
    """Protocol for objects that support both sync and async commit operations."""

    pass
