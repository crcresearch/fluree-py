"""Errors for the FlureeQL select query builder."""

class FlureeSelectError(Exception):
    """Base exception for Fluree select query building errors."""


class MissingIdFieldError(FlureeSelectError):
    """Exception raised when a model is missing a required 'id' field."""

    def __init__(self, model_name: str) -> None:
        super().__init__(f"{model_name} must have an 'id' field")


class NestingError(FlureeSelectError):
    """Exception raised when encountering unsupported nesting."""


class DeeplyNestedDictionaryError(NestingError):
    """Exception raised when encountering unsupported deeply nested dictionaries."""

    def __init__(self, field_name: str) -> None:
        super().__init__(f"Deeply nested dictionaries are not supported in field '{field_name}'")


class NestedTupleError(NestingError):
    """Exception raised when encountering unsupported nested tuples."""

    def __init__(self, field_name: str) -> None:
        super().__init__(f"Tuples are not supported in field '{field_name}'")


class InvalidFieldTypeError(FlureeSelectError):
    """Exception raised when encountering an invalid field type."""

    def __init__(self, field_name: str, field_type: type) -> None:
        super().__init__(f"Invalid field type for '{field_name}': {field_type}")


class ModelConfigError(FlureeSelectError):
    """Exception raised when there's an issue with the model configuration."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class TypeProcessingError(FlureeSelectError):
    """Exception raised when there's an error processing a type."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
