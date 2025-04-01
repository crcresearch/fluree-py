"""Base mixin for HTTP request handling in Fluree operations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from httpx import Request

from fluree_py.ledger.protocol.mixin.request import SupportsRequestCreation
from fluree_py.types import JsonObject


@dataclass(frozen=True, kw_only=True)
class RequestMixin(ABC, SupportsRequestCreation):
    """Base class for creating and managing HTTP requests."""

    def get_request(self) -> Request:
        """Constructs an HTTP request with the operation's data.

        Exceptions:
            NotImplementedError: If get_url() or build_request_payload() are not implemented.
        """
        return Request(
            method="POST",
            url=self.get_url(),
            json=self.build_request_payload(),
        )

    @abstractmethod
    def get_url(self) -> str:
        """Returns the endpoint URL for the request.

        Exceptions:
            NotImplementedError: If not implemented by subclass.
        """
        ...

    @abstractmethod
    def build_request_payload(self) -> JsonObject:
        """Constructs the JSON payload for the request.

        Exceptions:
            NotImplementedError: If not implemented by subclass.
        """
        ...
