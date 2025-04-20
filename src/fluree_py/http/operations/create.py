"""Create operation protocols and implementations."""

from dataclasses import dataclass
from typing import Any, ClassVar, Protocol

from fluree_py.http.mixin.commit import CommitableMixin, SupportsCommitable
from fluree_py.http.mixin.context import HasContextData, SupportsContext
from fluree_py.http.mixin.insert import HasInsertData, SupportsInsert
from fluree_py.http.mixin.response import SupportsFromResponse, SupportsRaisingFromResponse
from fluree_py.http.mixin.utils import make_setter
from fluree_py.http.response import LedgerCreationResponse, MissingTransactionError
from fluree_py.logging import logger
from fluree_py.types.common import JsonArray, JsonObject


# Protocol definitions for create operations
class CreateReadyToCommit(SupportsCommitable, HasInsertData, HasContextData, Protocol):
    """Protocol for create operations ready to be committed."""


class CreateBuilder(
    HasContextData, SupportsContext["CreateBuilder"], HasInsertData, SupportsInsert[CreateReadyToCommit], Protocol
):
    """Protocol for building create operations."""


# Implementation of create operations
@dataclass(frozen=True, kw_only=True)
class CreateReadyToCommitImpl(CommitableMixin[LedgerCreationResponse], CreateReadyToCommit):
    """Implementation of a create operation ready to be committed."""

    __response_errors__: ClassVar[list[type[SupportsRaisingFromResponse]]] = [MissingTransactionError]
    __response_payload__: ClassVar[type[SupportsFromResponse]] = LedgerCreationResponse

    endpoint: str
    ledger: str
    data: JsonObject | JsonArray | None
    context: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        """Log the transition to a ready to commit state."""
        logger.info("create_ready", endpoint=self.endpoint, ledger=self.ledger, data=self.data)

    with_insert = make_setter("with_insert", "data")
    with_context = make_setter("with_context", "context")

    def get_url(self) -> str:
        """Get the endpoint URL for the create operation."""
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        """Build the request payload for the create operation."""
        result: dict[str, Any] = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger, "insert": self.data}
        return result


@dataclass(frozen=True, kw_only=True)
class CreateBuilderImpl(CreateBuilder):
    """Implementation of a create operation builder."""

    endpoint: str
    ledger: str

    context: dict[str, Any] | None = None
    with_context = make_setter("with_context", "context")

    data: JsonObject | JsonArray | None = None
    with_insert = make_setter("with_insert", "data", next_cls=CreateReadyToCommitImpl)
