"""Base mixin for HTTP request handling in Fluree operations."""

from httpx import Request

from fluree_py.http.protocol.mixin.request import HasEndpointURL, HasRequestPayload


class WithRequestMixin(HasEndpointURL, HasRequestPayload):
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
