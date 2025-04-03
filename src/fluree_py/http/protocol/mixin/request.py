from typing import Protocol

from httpx import Request

from fluree_py.types.common import JsonObject


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
