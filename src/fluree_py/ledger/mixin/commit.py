from dataclasses import dataclass
from typing import Any, Generic, TypeVar

import httpx

from fluree_py.ledger.protocol.request import SupportsRequestCreation

T = TypeVar("T", bound=SupportsRequestCreation)


@dataclass(frozen=True, kw_only=True)
class CommitMixin(Generic[T]):
    def commit(self: T) -> dict[str, Any]:
        request = self.get_request()
        with httpx.Client() as client:
            response = client.send(request)
        response.raise_for_status()
        return response.json()
