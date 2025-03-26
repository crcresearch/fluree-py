from typing import Protocol

from fluree_py.ledger.protocol.commit import SupportsCommitable
from fluree_py.ledger.protocol.context import SupportsContext
from fluree_py.ledger.protocol.request import SupportsRequestCreation


class BaseBuilder(SupportsContext, Protocol):
    """Base protocol for all builders that support context."""

    pass


class BaseReadyToCommit(SupportsRequestCreation, SupportsCommitable, Protocol):
    """Base protocol for all builders that are ready to commit."""

    pass
