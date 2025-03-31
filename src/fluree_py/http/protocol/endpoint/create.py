from typing import Protocol

from fluree_py.http.protocol.mixin import (
    SupportsCommitable,
    SupportsContext,
    SupportsInsert,
    SupportsRequestCreation,
)
from fluree_py.http.protocol.mixin.context import HasContextData
from fluree_py.http.protocol.mixin.insert import HasInsertData


class CreateBuilder(
    SupportsContext["CreateBuilder"], SupportsInsert["CreateReadyToCommit"], Protocol
):
    """Protocol for create builders."""

    pass


class CreateReadyToCommit(
    SupportsRequestCreation, SupportsCommitable, HasInsertData, HasContextData, Protocol
):
    """Protocol for create builders that are ready to commit."""

    pass
