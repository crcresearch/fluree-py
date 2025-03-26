from dataclasses import dataclass
from typing import Any


from fluree_py.ledger.mixin import CommitableMixin, WithContextMixin, RequestMixin


@dataclass(frozen=True, kw_only=True)
class CreateBuilderImpl(WithContextMixin):
    endpoint: str
    ledger: str

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
class CreateReadyToCommitImpl(RequestMixin, WithContextMixin, CommitableMixin):
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
