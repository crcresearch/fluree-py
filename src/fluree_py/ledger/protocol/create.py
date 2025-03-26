from typing import Any, Protocol

from fluree_py.ledger.protocol.base import BaseBuilder, BaseReadyToCommit


class CreateBuilder(BaseBuilder, Protocol):
    """Protocol for create builders."""

    def with_insert(
        self, data: list[dict[str, Any]] | dict[str, Any]
    ) -> "CreateReadyToCommit": ...


class CreateReadyToCommit(BaseReadyToCommit, Protocol):
    """Protocol for create builders that are ready to commit."""

    pass
