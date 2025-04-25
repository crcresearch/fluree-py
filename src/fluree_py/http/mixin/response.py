"""
Response handling mixins and protocols for HTTPX-based API clients.

This module provides a set of protocols and mixins to standardize the handling of HTTP responses in a type-safe and extensible way. It defines interfaces for extracting payloads and errors from HTTPX responses, as well as a reusable mixin for implementing response handling logic in client classes.

Key Concepts:
- SupportsFromResponse: Protocol for types that can be constructed from an httpx.Response.
- SupportsRaisingFromResponse: Protocol for types that can raise exceptions from an httpx.Response.
- HasResponsePayload/HasResponseErrors: Protocols for declaring payload and error types.
- ResponseHandlingMixin: Mixin providing a handle_response method for consistent response processing.
"""

from typing import ClassVar, Generic, Protocol, Self, TypeVar, cast, runtime_checkable

import httpx

from fluree_py.logging import logger

T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class SupportsFromResponse(Protocol):
    """Protocol for types constructible from an httpx.Response."""

    @classmethod
    def from_response(cls, response: httpx.Response) -> Self:
        """Handle a response."""
        ...


@runtime_checkable
class SupportsRaisingFromResponse(Protocol):
    """Protocol for types that can raise exceptions from an httpx.Response."""

    @classmethod
    def raise_from_response(cls, response: httpx.Response) -> Exception | None:
        """Raise an exception from a response."""
        ...


T_Success_co = TypeVar("T_Success_co", bound=SupportsFromResponse, covariant=True)


class HasResponsePayload(Protocol):
    """Protocol for classes with a response payload type."""

    __response_payload__: ClassVar[type[SupportsFromResponse]]


class HasResponseErrors(Protocol):
    """Protocol for classes with response error types."""

    __response_errors__: ClassVar[list[type[SupportsRaisingFromResponse]]]


class SupportsResponseHandling(HasResponsePayload, HasResponseErrors, Protocol):
    """Protocol for objects supporting response handling via handle_response."""

    def handle_response(self, response: httpx.Response) -> SupportsFromResponse:
        """Handle a response."""
        ...


class ResponseHandlingMixin(HasResponsePayload, HasResponseErrors, Generic[T_Success_co]):
    """Mixin for handling HTTPX responses: raises errors or returns a payload instance."""

    def handle_response(self, response: httpx.Response) -> T_Success_co:
        """
        Process an HTTPX response, raising an error if detected or returning the payload.

        This method iterates through the error types defined in __response_errors__, calling their
        raise_from_response method. If any error type returns an exception, it is raised immediately.
        If no errors are detected, the method constructs and returns the payload using the type
        specified in __response_payload__ via its from_response method.

        Args:
            response (httpx.Response): The HTTP response to process.

        Returns:
            SupportsFromResponse[T_Success_co]: An instance of the payload type, constructed from the response.

        Raises:
            Exception: If any error type in __response_errors__ returns an exception.

        """
        logger.debug(
            "handle_response",
            status_code=response.status_code,
            data=response.text,
        )

        for exception_type in self.__response_errors__:
            logger.info("handle_response", cls=self.__class__.__name__)
            exception = exception_type.raise_from_response(response)
            if exception is not None:
                raise exception

        return cast("type[T_Success_co]", self.__response_payload__).from_response(response)
