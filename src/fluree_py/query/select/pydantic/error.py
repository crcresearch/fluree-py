"""Errors for the FlureeQL select query builder."""


class FlureeSelectError(Exception):
    """Base exception for Fluree select query building errors."""


class MissingIdFieldError(FlureeSelectError):
    """Exception raised when a model is missing a required 'id' field."""


class DeeplyNestedStructureError(FlureeSelectError):
    """Exception raised when encountering unsupported deeply nested structures."""


class InvalidFieldTypeError(FlureeSelectError):
    """Exception raised when encountering an invalid field type."""


class ModelConfigError(FlureeSelectError):
    """Exception raised when there's an issue with the model configuration."""


class TypeProcessingError(FlureeSelectError):
    """Exception raised when there's an error processing a type."""
