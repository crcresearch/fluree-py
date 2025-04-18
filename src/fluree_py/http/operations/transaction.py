"""Transaction operation protocols and implementations."""

from dataclasses import dataclass
from typing import Any, ClassVar, Protocol, Self

from fluree_py.http.mixin.commit import CommitableMixin, SupportsCommitable
from fluree_py.http.mixin.context import SupportsContext
from fluree_py.http.mixin.insert import HasInsertData, SupportsInsert
from fluree_py.http.mixin.response import SupportsFromResponse, SupportsRaisingFromResponse
from fluree_py.http.mixin.utils import make_setter
from fluree_py.http.mixin.where import SupportsWhere
from fluree_py.http.response import FlureeResponse, MissingTransactionError
from fluree_py.logging import logger
from fluree_py.types.common import JsonArray, JsonObject
from fluree_py.types.query.where import WhereClause


# Protocol definitions for transaction operations
class TransactionReadyToCommit(
    SupportsCommitable,
    SupportsContext["TransactionReadyToCommit"],
    SupportsWhere["TransactionReadyToCommit"],
    HasInsertData,
    Protocol,
):
    """Protocol for transaction operations ready to be committed."""

    def with_delete(self, value: JsonObject | JsonArray) -> Self:
        """Set the delete data for the operation."""
        ...


class TransactionBuilder(
    SupportsContext["TransactionBuilder"],
    SupportsInsert[TransactionReadyToCommit],
    SupportsWhere["TransactionBuilder"],
    Protocol,
):
    """Protocol for building transaction operations."""

    def with_delete(self, value: JsonObject | JsonArray) -> TransactionReadyToCommit:
        """Set the delete data for the operation."""
        ...


# Implementation of transaction operations


@dataclass(frozen=True, kw_only=True)
class TransactionReadyToCommitImpl(
    CommitableMixin[FlureeResponse],
    TransactionReadyToCommit,
):
    """Implementation of a transaction operation ready to be committed."""

    __response_errors__: ClassVar[list[type[SupportsRaisingFromResponse]]] = [MissingTransactionError]
    __response_payload__: ClassVar[type[SupportsFromResponse]] = FlureeResponse

    endpoint: str
    ledger: str

    context: dict[str, Any] | None
    with_context = make_setter("with_context", "context")

    where: WhereClause | None
    with_where = make_setter("with_where", "where")

    # data is defined in the HasInsertData protocol
    data: JsonObject | JsonArray | None

    delete_data: JsonObject | JsonArray | None
    with_delete = make_setter("with_delete", "delete_data")

    def __post_init__(self) -> None:
        """Log the transition to a ready to commit state."""
        logger.info(
            "transaction_ready",
            endpoint=self.endpoint,
            ledger=self.ledger,
            data=self.data,
            delete_data=self.delete_data,
            where=self.where,
        )

    def get_url(self) -> str:
        """Get the endpoint URL for the transaction operation."""
        return self.endpoint

    def build_request_payload(self) -> dict[str, Any]:
        """Build the request payload for the transaction operation."""
        result: dict[str, Any] = {}
        if self.context:
            result["@context"] = self.context
        result |= {"ledger": self.ledger}
        if self.data:
            result["insert"] = self.data
        if self.delete_data:
            result["delete"] = self.delete_data
        if self.where:
            result["where"] = self.where
        logger.debug("building_transaction_payload", payload=result)
        return result


@dataclass(frozen=True, kw_only=True)
class TransactionBuilderImpl(TransactionBuilder):
    """Implementation of a transaction operation builder."""

    endpoint: str
    ledger: str

    context: dict[str, Any] | None = None
    with_context = make_setter("with_context", "context")

    data: JsonObject | JsonArray | None = None
    with_insert = make_setter("with_insert", "data", next_cls=TransactionReadyToCommitImpl)

    where: WhereClause | None = None
    with_where = make_setter("with_where", "where")

    delete_data: JsonObject | JsonArray | None = None
    with_delete = make_setter("with_delete", "delete_data", next_cls=TransactionReadyToCommitImpl)
