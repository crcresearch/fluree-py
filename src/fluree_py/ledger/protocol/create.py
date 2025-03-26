from typing import Any, Protocol

import httpx

from fluree_py.ledger.protocol.context import SupportsContext


class SupportsCreate(Protocol):
    def create(self) -> "CreateBuilder": ...


class CreateBuilder(SupportsContext, Protocol):
    def with_insert(
        self, data: list[dict[str, Any]] | dict[str, Any]
    ) -> "CreateReadyToCommit": ...


class CreateReadyToCommit(Protocol):
    def request(self) -> httpx.Request: ...
    def commit(self) -> dict[str, Any]: ...
