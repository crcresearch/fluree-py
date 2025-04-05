"""Warnings for the FlureeQL select query builder."""


class ListOrderWarning(RuntimeWarning):
    """Warning raised when a field is a list type, indicating non-deterministic order."""


class PossibleEmptyModelWarning(RuntimeWarning):
    """Warning raised when a model has only optional fields."""

    def __init__(self, model_name: str):
        super().__init__(f"{model_name} has only optional fields. This may result in an empty model when inserting.")
