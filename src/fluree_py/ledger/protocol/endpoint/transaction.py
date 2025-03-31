"""Protocols for building and executing transactions in the Fluree ledger."""

from typing import Protocol, Self

from fluree_py.ledger.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsRequestCreation,
)
from fluree_py.ledger.protocol.mixin.insert import HasInsertData, SupportsInsert
from fluree_py.ledger.protocol.mixin.where import SupportsWhere
from fluree_py.types import JsonArray, JsonObject


class TransactionBuilder(
    SupportsContext["TransactionBuilder"],
    SupportsInsert["TransactionReadyToCommit"],
    SupportsWhere["TransactionBuilder"],
    Protocol,
):
    """Protocol for building transaction operations.
    """

    def with_delete(
        self, data: JsonObject | JsonArray
    ) -> "TransactionReadyToCommit": ...


class TransactionReadyToCommit(
    SupportsRequestCreation,
    SupportsCommitable,
    SupportsContext["TransactionReadyToCommit"],
    SupportsWhere["TransactionReadyToCommit"],
    HasInsertData,
    Protocol,
):
    """Protocol for transaction operations ready to be committed.
    """

    def with_delete(self, data: JsonObject | JsonArray) -> Self: ...
