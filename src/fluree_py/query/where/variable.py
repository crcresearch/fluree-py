from fluree_py.query.where.condition import Condition


class Var:
    def __init__(self, name: str):
        self.name = name

    def __gt__(self, other): return Condition(str(self.name), ">", other)
    def __lt__(self, other): return Condition(str(self.name), "<", other)
    def __ge__(self, other): return Condition(str(self.name), ">=", other)
    def __le__(self, other): return Condition(str(self.name), "<=", other)

    def __str__(self): return f"?{self.name}"
    def __repr__(self): return f"Var({self.name})"