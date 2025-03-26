from typing import Protocol
from httpx import Request


class SupportsRequestCreation(Protocol):
    def get_request(self) -> Request: ...
