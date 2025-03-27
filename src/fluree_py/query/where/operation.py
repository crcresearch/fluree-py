from dataclasses import dataclass

from fluree_py.query.where.condition import Condition
from fluree_py.query.where.variable import Var


@dataclass
class UnionClause:
    conditions: list[Condition]

    def to_expr(self) -> list[str]:
        return ["union"] + list(map(lambda c: c.to_expr(), self.conditions))


@dataclass
class FilterClause:
    expressions: list[Condition]

    def to_expr(self) -> list[str]:
        return ["filter"] + list(map(lambda e: e.to_expr(), self.expressions))


@dataclass
class BindClause:
    variable: Var
    expression: Condition

    def to_expr(self) -> list[str]:
        return ["bind", str(self.variable), str(self.expression)]


@dataclass
class OptionalClause:
    conditions: list[Condition]

    def to_expr(self) -> list[str]:
        return ["optional"] + list(map(lambda c: c.to_expr(), self.conditions))
