from typing import Protocol

from httpx import Request


class SupportsRequestCreation(Protocol):
    """Protocol for objects that support HTTP request creation."""
    def get_request(self) -> Request: ...
