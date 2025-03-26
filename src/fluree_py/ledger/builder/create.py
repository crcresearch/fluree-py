from dataclasses import dataclass, replace
from typing import Any

import httpx

from fluree_py.ledger.mixin.context import WithContextMixin
from fluree_py.ledger.mixin.request_builder import WithRequestMixin


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
class CreateReadyToCommitImpl(WithRequestMixin, WithContextMixin):
    endpoint: str
    ledger: str
    data: list[dict[str, Any]] | dict[str, Any]

    def get_url(self) -> str:
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        result = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger, "insert": self.data}
        return result

    def commit(self) -> dict[str, Any]:
        request = self.get_request()
        with httpx.Client() as client:
            response = client.send(request)
        response.raise_for_status()
        return response.json()
