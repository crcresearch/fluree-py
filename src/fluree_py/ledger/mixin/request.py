from abc import ABC, abstractmethod
from dataclasses import dataclass

from httpx import Request

from fluree_py.ledger.protocol.request import SupportsRequestCreation
from fluree_py.types import JsonObject


@dataclass(frozen=True, kw_only=True)
class RequestMixin(ABC, SupportsRequestCreation):
    def get_request(self) -> Request:
        return Request(
            method="POST",
            url=self.get_url(),
            json=self.build_request_payload(),
        )

    @abstractmethod
    def get_url(self) -> str: ...

    @abstractmethod
    def build_request_payload(self) -> JsonObject: ...
