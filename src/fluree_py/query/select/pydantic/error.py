class FlureeSelectError(Exception):
    """Base exception for Fluree select query building errors."""

    pass


class MissingIdFieldError(FlureeSelectError):
    """Exception raised when a model is missing a required 'id' field."""

    pass


class DeeplyNestedStructureError(FlureeSelectError):
    """Exception raised when encountering unsupported deeply nested structures."""

    pass


class InvalidFieldTypeError(FlureeSelectError):
    """Exception raised when encountering an invalid field type."""

    pass


class ModelConfigError(FlureeSelectError):
    """Exception raised when there's an issue with the model configuration."""

    pass


class TypeProcessingError(FlureeSelectError):
    """Exception raised when there's an error processing a type."""

    pass
