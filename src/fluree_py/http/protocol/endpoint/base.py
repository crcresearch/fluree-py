from typing import Protocol

from fluree_py.http.protocol.mixin import SupportsCommitable, SupportsContext, SupportsRequestCreation


class BaseBuilder(SupportsContext, Protocol):
    """Base protocol for all builders that support context."""

    pass


class BaseReadyToCommit(SupportsRequestCreation, SupportsCommitable, Protocol):
    """Base protocol for all builders that are ready to commit."""

    pass
