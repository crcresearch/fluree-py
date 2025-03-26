from typing import Any, Protocol

from fluree_py.ledger.protocol.context import SupportsContext
from fluree_py.ledger.protocol.request import SupportsRequestCreation


class SupportsCreate(Protocol):
    def create(self) -> "CreateBuilder": ...


class CreateBuilder(SupportsContext, Protocol):
    def with_insert(
        self, data: list[dict[str, Any]] | dict[str, Any]
    ) -> "CreateReadyToCommit": ...


class CreateReadyToCommit(SupportsRequestCreation, Protocol):
    def commit(self) -> dict[str, Any]: ...
