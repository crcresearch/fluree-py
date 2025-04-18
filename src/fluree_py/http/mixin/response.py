from typing import Any, Generic, Protocol, TypeVar, cast

import httpx

from fluree_py.http.mixin.utils import resolve_base_type_arg
from fluree_py.logging import logger

T_co = TypeVar("T_co", covariant=True)


class SupportsFromResponse(Protocol[T_co]):
    """Protocol for objects that support a successful response."""

    @classmethod
    def from_response(cls, response: httpx.Response) -> T_co:
        """Handle a response."""
        ...


class SupportsRaisingFromResponse(Protocol):
    """Protocol for objects that support a response error."""

    def raise_from_response(cls, response: httpx.Response) -> None:
        """Raise an exception from a response."""
        ...


T_Success_co = TypeVar("T_Success_co", bound="SupportsFromResponse", covariant=True)
T_Failure_co = TypeVar("T_Failure_co", bound="SupportsRaisingFromResponse", covariant=True)


class SupportsResponseHandling(Protocol[T_Success_co, T_Failure_co]):
    """Protocol for objects that support response handling."""

    def handle_response(self, response: httpx.Response) -> T_Success_co:
        """Handle a response."""
        ...


class ResponseHandlingMixin(Generic[T_Success_co, T_Failure_co]):
    def handle_response(self, response: httpx.Response) -> T_Success_co:
        logger.info("handle_response", cls=self.__class__.__name__)
        exception_types = resolve_base_type_arg(self.__class__, "ResponseHandlingMixin", "T_Failure_co")
        logger.info("exception_types", exception_types)
        for exception_type in exception_types:
            logger.info("exception_type", exception_type.__class__.__name__)
            cast("T_Failure_co", exception_type).raise_from_response(response)

        target_types = resolve_base_type_arg(self.__class__, "ResponseHandlingMixin", T_Success_co)
        if not target_types:
            raise TypeError(f"{self.__class__.__name__} must be parameterized with a target type")

        logger.info("target_types", target_types)

        # For each target type, try different conversion methods
        for target_type in target_types:
            # Skip TypeVar or non-concrete types
            if isinstance(target_type, TypeVar) or target_type is Any:
                continue

            converted = target_type.from_response(response)
            if converted is not None:
                return converted

        # If we get here, no conversion method worked
        raise ValueError(f"Could not convert response to any of the target types: {target_types}")
