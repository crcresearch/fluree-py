"""Base mixin for HTTP request handling in Fluree operations."""

from typing import Protocol

from httpx import Request

from fluree_py.types.common import JsonObject


# Protocol definitions for request mixin
class SupportsRequestCreation(Protocol):
    """Protocol for objects that support HTTP request creation."""

    def get_request(self) -> Request:
        """Create a HTTP request for this operation."""
        ...


class HasEndpointURL(Protocol):
    """Protocol for objects that have an endpoint URL."""

    def get_url(self) -> str:
        """Return the endpoint URL for the request."""
        ...


class HasRequestPayload(Protocol):
    """Protocol for objects that have a request payload."""

    def build_request_payload(self) -> JsonObject:
        """Construct the JSON payload for the request."""
        ...


class WithRequestMixin(SupportsRequestCreation, HasEndpointURL, HasRequestPayload):
    """Mixin for creating and managing HTTP requests."""

    def get_request(self) -> Request:
        """
        Construct a HTTP request with the operation's data.

        Exceptions:
            NotImplementedError: If get_url() or build_request_payload() are not implemented.
        """
        return Request(
            method="POST",
            url=self.get_url(),
            json=self.build_request_payload(),
        )
