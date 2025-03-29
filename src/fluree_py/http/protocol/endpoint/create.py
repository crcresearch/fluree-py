from typing import Protocol

from fluree_py.http.protocol.endpoint.base import BaseBuilder, BaseReadyToCommit
from fluree_py.types.common import JsonArray, JsonObject


class CreateBuilder(BaseBuilder, Protocol):
    """Protocol for create builders."""

    def with_insert(
        self, data: JsonObject | JsonArray
    ) -> "CreateReadyToCommit": ...


class CreateReadyToCommit(BaseReadyToCommit, Protocol):
    """Protocol for create builders that are ready to commit."""

    pass
