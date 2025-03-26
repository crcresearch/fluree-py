from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from httpx import Request


@dataclass(frozen=True, kw_only=True)
class WithRequestMixin(ABC):
    def get_request(self) -> Request:
        return Request(
            method="POST",
            url=self.get_url(),
            json=self.build_request_payload(),
        )

    @abstractmethod
    def get_url(self) -> str: ...

    @abstractmethod
    def build_request_payload(self) -> dict[str, Any]: ...
