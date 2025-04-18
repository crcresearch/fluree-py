"""Create operation protocols and implementations."""

from dataclasses import dataclass
from typing import Any, Protocol

from fluree_py.http.mixin import (
    WithContextMixin,
    WithInsertMixin,
)
from fluree_py.http.mixin.commit import CommitableMixin, SupportsCommitable
from fluree_py.http.mixin.context import HasContextData, SupportsContext
from fluree_py.http.mixin.insert import HasInsertData, SupportsInsert
from fluree_py.http.response import FlureeResponse, MissingTransactionError
from fluree_py.logging import logger
from fluree_py.types.common import JsonArray, JsonObject


# Protocol definitions for create operations
class CreateReadyToCommit(
    SupportsCommitable[FlureeResponse, MissingTransactionError], HasInsertData, HasContextData, Protocol
):
    """Protocol for create operations ready to be committed."""


class CreateBuilder(SupportsContext["CreateBuilder"], SupportsInsert[CreateReadyToCommit], Protocol):
    """Protocol for building create operations."""


# Implementation of create operations
@dataclass(frozen=True, kw_only=True)
class CreateReadyToCommitImpl(
    CommitableMixin[FlureeResponse, MissingTransactionError],
    WithContextMixin["CreateReadyToCommitImpl"],
    WithInsertMixin["CreateReadyToCommitImpl"],
    CreateReadyToCommit,
):
    """Implementation of a create operation ready to be committed."""

    endpoint: str
    ledger: str
    data: JsonObject | JsonArray | None
    context: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        logger.info("create_ready", endpoint=self.endpoint, ledger=self.ledger, data=self.data)

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
class CreateBuilderImpl(
    WithContextMixin["CreateBuilderImpl"],
    WithInsertMixin[CreateReadyToCommitImpl],
    CreateBuilder,
):
    """Implementation of a create operation builder."""

    endpoint: str
    ledger: str
    data: JsonObject | JsonArray | None = None
    context: dict[str, Any] | None = None
