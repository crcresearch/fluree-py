from typing import TypeVar

# Shared TypeVars
T_Success = TypeVar("T_Success")
T_Failure = TypeVar("T_Failure")
T = TypeVar("T")


# Shared base classes
class ConcreteSuccess:
    pass


class ConcreteFailure:
    pass


class Concrete:
    pass
