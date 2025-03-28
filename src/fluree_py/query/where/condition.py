from typing import Any

from fluree_py.query.where.variable import Var


class Condition:
    def __init__(self, field: str, op: str, value: Any):
        self.field = field
        self.op = op
        self.value = value

    def to_expr(self) -> str:
        return f"({self.op} {self.field} {self._format_value(self.value)})"

    def _format_value(self, val):
        if isinstance(val, Var):
            return str(val)
        elif isinstance(val, str) and not val.startswith("?"):
            return f'"{val}"'
        return val

    def to_fluree(self) -> dict:
        if self.op == "=":
            return {self.field: self.value}
        else:
            return {self.field: {f"${self.op}": self.value}}
