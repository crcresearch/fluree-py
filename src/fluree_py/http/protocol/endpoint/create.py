"""Protocols for creating new entities in the Fluree ledger."""

from typing import Protocol

from fluree_py.http.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsInsert,
)
from fluree_py.http.protocol.mixin.context import HasContextData
from fluree_py.http.protocol.mixin.insert import HasInsertData


class CreateBuilder(SupportsContext["CreateBuilder"], SupportsInsert["CreateReadyToCommit"], Protocol):
    """Protocol for building create operations."""


class CreateReadyToCommit(SupportsCommitable, HasInsertData, HasContextData, Protocol):
    """Protocol for create operations ready to be committed."""
