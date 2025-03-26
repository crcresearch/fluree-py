from typing import Any, Protocol

from fluree_py.http.protocol.mixin import SupportsCommit, SupportsContext, SupportsRequestCreation


class SupportsCreate(Protocol):
    def create(self) -> "CreateBuilder": ...


class CreateBuilder(SupportsContext, Protocol):
    def with_insert(
        self, data: list[dict[str, Any]] | dict[str, Any]
    ) -> "CreateReadyToCommit": ...


class CreateReadyToCommit(SupportsRequestCreation, SupportsCommit, Protocol):
    pass
