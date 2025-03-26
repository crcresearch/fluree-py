from dataclasses import dataclass, replace
from typing import Any, Dict, Optional, Protocol

import httpx

from fluree_py.context import SupportsContext, WithContextMixin


class SupportsCreate(Protocol):
    def create(self) -> "CreateBuilder": ...


class CreateBuilder(SupportsContext, Protocol):
    def with_insert(self, data: Dict[str, Any]) -> "CreateReadyToCommit": ...


class CreateReadyToCommit(Protocol):
    def request(self) -> httpx.Request: ...
    def commit(self) -> Dict[str, Any]: ...


@dataclass(frozen=True, kw_only=True)
class CreateBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str

    def with_context(self, context: Dict[str, Any]) -> "CreateBuilderImpl":
        return replace(self, context=context)

    def with_insert(self, data: Dict[str, Any]) -> "CreateReadyToCommitImpl":
        return CreateReadyToCommitImpl(
            endpoint=self.endpoint,
            ledger=self.ledger,
            data=data,
            context=self.context,
        )


@dataclass(frozen=True, kw_only=True)
class CreateReadyToCommitImpl:
    endpoint: str
    ledger: str
    data: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

    @property
    def json(self) -> Dict[str, Any]:
        return (
            {"ledger": self.ledger, "insert": self.data} | {"@context": self.context}
            if self.context
            else {}
        )

    def request(self) -> httpx.Request:
        return httpx.Request(
            "POST",
            self.endpoint,
            json=self.json,
        )

    def commit(self) -> Dict[str, Any]:
        response = httpx.post(self.endpoint, json=self.json)
        response.raise_for_status()
        return response.json()
