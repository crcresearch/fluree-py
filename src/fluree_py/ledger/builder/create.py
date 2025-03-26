from dataclasses import dataclass, replace
from typing import Any

import httpx

from fluree_py.ledger.mixin.context import WithContextMixin


@dataclass(frozen=True, kw_only=True)
class CreateBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str

    def with_context(self, context: dict[str, Any]) -> "CreateBuilderImpl":
        return replace(self, context=context)

    def with_insert(
        self, data: list[dict[str, Any]] | dict[str, Any]
    ) -> "CreateReadyToCommitImpl":
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
    data: list[dict[str, Any]] | dict[str, Any]
    context: dict[str, Any] | None = None

    @property
    def json(self) -> dict[str, Any]:
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

    def commit(self) -> dict[str, Any]:
        response = httpx.post(self.endpoint, json=self.json)
        response.raise_for_status()
        return response.json()
