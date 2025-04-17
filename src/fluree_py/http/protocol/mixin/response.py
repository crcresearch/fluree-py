from typing import Protocol, TypeVar

from httpx import Response

T_co = TypeVar("T_co", covariant=True)


class SupportsFromResponse(Protocol[T_co]):
    """Protocol for objects that support a successful response."""

    @classmethod
    def from_response(cls, response: Response) -> T_co:
        """Handle a response."""
        ...


class SupportsRaisingFromResponse(Protocol):
    """Protocol for objects that support a response error."""

    @classmethod
    def raise_from_response(cls, response: Response) -> None:
        """Raise an exception from a response."""
        ...


T_Success_co = TypeVar("T_Success_co", bound=SupportsFromResponse, covariant=True)
T_Failure_co = TypeVar("T_Failure_co", bound=SupportsRaisingFromResponse, covariant=True)


class SupportsResponseHandling(Protocol[T_Success_co, T_Failure_co]):
    """Protocol for objects that support response handling."""

    def handle_response(self, response: Response) -> T_Success_co:
        """Handle a response."""
        ...
