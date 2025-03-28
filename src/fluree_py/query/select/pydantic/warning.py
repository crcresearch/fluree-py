class ListOrderWarning(RuntimeWarning):
    """Warning raised when a field is a list type, indicating non-deterministic order."""

    pass


class PossibleEmptyModelWarning(RuntimeWarning):
    """Warning raised when a model has only optional fields."""

    pass
