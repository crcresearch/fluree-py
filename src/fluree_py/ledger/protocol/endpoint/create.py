from typing import Protocol

from fluree_py.ledger.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsInsert,
    SupportsRequestCreation,
)
from fluree_py.ledger.protocol.mixin.context import HasContextData
from fluree_py.ledger.protocol.mixin.insert import HasInsertData


class CreateBuilder(SupportsContext, SupportsInsert, Protocol):
    """Protocol for create builders."""

    pass


class CreateReadyToCommit(
    SupportsRequestCreation, SupportsCommitable, HasInsertData, HasContextData, Protocol
):
    """Protocol for create builders that are ready to commit."""

    pass
