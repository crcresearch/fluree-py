from typing import Any, Protocol


from fluree_py.ledger.protocol.commit import SupportsCommitable
from fluree_py.ledger.protocol.context import SupportsContext
from fluree_py.ledger.protocol.request import SupportsRequestCreation


class QueryBuilder(
    SupportsContext, SupportsRequestCreation, SupportsCommitable, Protocol
):
    def with_where(self, conditions: dict[str, Any]) -> "QueryBuilder": ...
    def with_group_by(self, fields: list[str]) -> "QueryBuilder": ...
    def with_having(self, condition: dict[str, Any]) -> "QueryBuilder": ...
    def with_order_by(self, fields: list[str]) -> "QueryBuilder": ...
    def with_opts(self, opts: dict[str, Any]) -> "QueryBuilder": ...
    def select(self, fields: dict[str, Any] | list[str]) -> "QueryBuilder": ...
