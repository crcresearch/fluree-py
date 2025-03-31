from typing import Protocol

from fluree_py.ledger.protocol.mixin.commit import SupportsCommitable
from fluree_py.ledger.protocol.mixin.context import SupportsContext
from fluree_py.ledger.protocol.mixin.request import SupportsRequestCreation


class BaseBuilder(SupportsContext, Protocol):
    """Base protocol for all builders that support context."""

    pass


class BaseReadyToCommit(SupportsRequestCreation, SupportsCommitable, Protocol):
    """Base protocol for all builders that are ready to commit."""

    pass
