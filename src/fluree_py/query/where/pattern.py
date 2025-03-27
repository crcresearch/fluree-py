from dataclasses import dataclass
from typing import Union

from fluree_py.query.where.variable import Var

@dataclass
class Pattern:
    field: str
    value: Union[str, int, float, bool, 'Var']

    def to_fluree(self) -> dict:
        val = str(self.value) if isinstance(self.value, Var) else self.value
        return {self.field: val}

    def __repr__(self):
        return str(self.to_fluree())