"""Protocols for creating new entities in the Fluree ledger."""

from typing import Protocol

from fluree_py.ledger.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsInsert,
    SupportsRequestCreation,
)
from fluree_py.ledger.protocol.mixin.context import HasContextData
from fluree_py.ledger.protocol.mixin.insert import HasInsertData


class CreateBuilder(
    SupportsContext["CreateBuilder"], SupportsInsert["CreateReadyToCommit"], Protocol
):
    """Protocol for building create operations."""

    pass


class CreateReadyToCommit(
    SupportsRequestCreation, SupportsCommitable, HasInsertData, HasContextData, Protocol
):
    """Protocol for create operations ready to be committed."""

    pass
