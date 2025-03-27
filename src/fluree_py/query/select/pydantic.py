import warnings
from dataclasses import dataclass, field
from types import UnionType
from typing import (
    Any,
    Generic,
    List,
    Protocol,
    Tuple,
    Type,
    TypeAlias,
    TypeGuard,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    runtime_checkable,
)

from pydantic import BaseModel, ConfigDict


class ListOrderWarning(RuntimeWarning):
    """Warning raised when a field is a list type, indicating non-deterministic order."""
    pass


class PossibleEmptyModelWarning(RuntimeWarning):
    """Warning raised when a model has only optional fields."""
    pass


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


T = TypeVar("T", bound=BaseModel)
FieldType: TypeAlias = Union[
    str,
    int,
    float,
    bool,
    list[Any],
    dict[str, Any],
    type[BaseModel],
    None,
]  # More specific type for field types in Pydantic models


@dataclass
class WarningManager:
    """Manages warnings for the Pydantic model processing.
    
    Example:
        >>> manager = WarningManager()
        >>> manager.add_warning(ListOrderWarning, "Field 'items' is a list")
        >>> manager.emit_warnings()
    """
    warnings_list: List[Tuple[Warning, str]] = field(default_factory=list)

    def add_warning(self, warning_type: type[Warning], message: str) -> None:
        """Add a warning to the list."""
        self.warnings_list.append((warning_type, message))

    def emit_warnings(self) -> None:
        """Emit all collected warnings."""
        for warning_type, message in self.warnings_list:
            warnings.warn(message, warning_type)


@runtime_checkable
class HasModelConfig(Protocol):
    """Protocol for objects that have a model_config attribute."""
    model_config: ConfigDict




class TypeChecker(Generic[T]):
    """Handles type checking and validation for Pydantic models.
    
    This class provides utility methods for checking various types that can appear
    in Pydantic models, such as lists, dictionaries, and nested models.
    """

    @classmethod
    def is_list_type(cls, field_type: Any) -> TypeGuard[Type[List[Any]]]:
        """Check if a type is a list type."""
        return hasattr(field_type, "__origin__") and field_type.__origin__ is list

    @classmethod
    def is_dict_type(cls, field_type: Any) -> TypeGuard[Type[dict[str, Any]]]:
        """Check if a type is a dict type."""
        return hasattr(field_type, "__origin__") and field_type.__origin__ is dict

    @classmethod
    def is_tuple_type(cls, field_type: Any) -> TypeGuard[Type[tuple[Any, ...]]]:
        """Check if a type is a tuple type."""
        return hasattr(field_type, "__origin__") and field_type.__origin__ is tuple

    @classmethod
    def is_union_type(cls, field_type: Any) -> TypeGuard[Type[Union[Any, ...]]]:
        """Check if a type is a Union type."""
        return hasattr(field_type, "__origin__") and field_type.__origin__ is Union

    @classmethod
    def is_optional_type(cls, field_type: Any) -> TypeGuard[Type[Union[Any, None]]]:
        """Check if a type is an Optional type (Union with None)."""
        if not cls.is_union_type(field_type):
            return False
        args = get_args(field_type)
        return type(None) in args  # noqa: E721

    @classmethod
    def is_primitive_type(cls, field_type: Any) -> TypeGuard[Type[str | int | float | bool]]:
        """Check if a type is a primitive type (str, int, float, bool)."""
        return field_type in (str, int, float, bool)

    @classmethod
    def is_id_field(cls, field_name: str) -> bool:
        """Check if a field name is the id field."""
        return field_name == "id"
    
    @classmethod
    def dict_max_depth(cls, field_type: Any, depth: int = 0) -> int:
        """Recursively count dictionary nesting depth."""
        if not TypeChecker.is_dict_type(field_type):
            return depth

        args = get_args(field_type)
        if not args:
            return depth
            
        # Check the value type of the dictionary
        value_type = args[1]
        if TypeChecker.is_dict_type(value_type):
            return cls.dict_max_depth(value_type, depth + 1)
        return depth

    @classmethod
    def is_base_model(cls, field_type: Any) -> TypeGuard[Type[T]]:
        """Check if a type is a BaseModel."""
        return isinstance(field_type, type) and issubclass(field_type, BaseModel)

    @classmethod
    def get_real_type(cls, field_type: Any) -> Any:
        """Get the real type from a potentially optional/union type."""
        origin = get_origin(field_type)
        if origin is Union:
            types = [t for t in get_args(field_type) if t is not type(None)]  # noqa: E721
            if types:
                for t in types:
                    if cls.is_list_type(t):
                        return t
                return types[0]
        return field_type

    @classmethod
    def check_model_has_id(cls, model: Type[T]) -> bool:
        """Check if a model has an id field in its type hints."""
        return "id" in get_type_hints(model, include_extras=True)
    
    @classmethod
    def has_model_config(cls, model: Type[T]) -> TypeGuard[Type[T]]:
        """Check if a model has a model_config attribute."""
        return hasattr(model, "model_config")

    @classmethod
    def check_model_requires_id(cls, model: Type[T]) -> bool:
        """Check if a model requires an id field based on its configuration."""
        if not cls.has_model_config(model):
            return True

        config = getattr(model, "model_config", None)
        if not config:
            return True

        match config:
            case dict() as d:
                extra = d.get("extra", "ignore")
            case _:
                extra = getattr(config, "extra", "ignore")

        return extra in ("forbid", None)


@dataclass
class FlureeSelectBuilder(Generic[T]):
    """Builds Fluree select queries from Pydantic models.
    
    Example:
        >>> class User(BaseModel):
        ...     id: str
        ...     name: str
        >>> builder = FlureeSelectBuilder[User]()
        >>> query = builder.build(User)
        >>> assert query == ["*"]
    """
    warning_manager: WarningManager = field(default_factory=WarningManager)
    select: list[Any] = field(default_factory=lambda: ["*"])
    _processed_models: set[Type[T]] = field(default_factory=set)

    def _validate_model_config(self, model: Type[T]) -> None:
        """Validate the model configuration.
        
        Raises:
            ModelConfigError: If the model configuration is invalid
        """
        if not TypeChecker.has_model_config(model):
            return
        
        try:
            extra = model.model_config.get("extra", "ignore")
            if extra not in ("allow", "ignore", "forbid"):
                raise ModelConfigError(
                    f"Invalid 'extra' configuration value: {extra}. "
                    "Must be one of: 'allow', 'ignore', 'forbid'"
                )
        except Exception as e:
            if not isinstance(e, FlureeSelectError):
                raise ModelConfigError(
                    f"Error validating model configuration for {model.__name__}: {str(e)}"
                ) from e
            raise

    def _process_nested_model(
        self,
        field_name: str,
        field_type: Type[BaseModel],
    ) -> dict[str, Any]:
        """Process a nested model and return its select structure.
        
        Raises:
            MissingIdFieldError: If the nested model requires an id field but doesn't have one
            ModelConfigError: If there's an issue with the model configuration
        """
        # Prevent infinite recursion
        if field_type in self._processed_models:
            return {field_name: ["*"]}
        self._processed_models.add(field_type)

        # Validate model configuration
        self._validate_model_config(field_type)

        if TypeChecker.check_model_requires_id(field_type) and not TypeChecker.check_model_has_id(field_type):
            raise MissingIdFieldError(f"Nested model '{field_type.__name__}' must have an 'id' field")

        fields = get_type_hints(field_type, include_extras=True)
        select = ["*"]

        for nested_field_name, nested_field_type in fields.items():
            if TypeChecker.is_id_field(nested_field_name):
                continue

            real_type = TypeChecker.get_real_type(nested_field_type)
            self._process_field(nested_field_name, real_type, select)

        return {field_name: select}

    def _process_field(self, field_name: str, field_type: Any, select: list[Any]) -> None:
        """Process a field and add its select structure to the result.
        
        Raises:
            InvalidFieldTypeError: If the field type is not supported
            TypeProcessingError: If there's an error processing the field type
        """
        try:
            match field_type:
                case t if TypeChecker.is_list_type(t):
                    self.warning_manager.add_warning(
                        ListOrderWarning,
                        f"Field '{field_name}' is a list type. Order will be non-deterministic.",
                    )
                    args = get_args(t)
                    if args:
                        inner_type = TypeChecker.get_real_type(args[0])
                        if TypeChecker.is_base_model(inner_type):
                            select.append(self._process_nested_model(field_name, inner_type))
                        elif TypeChecker.is_dict_type(inner_type):
                            select.append({field_name: ["*"]})
                    return

                case t if TypeChecker.is_base_model(t):
                    select.append(self._process_nested_model(field_name, t))
                    return

                case t if TypeChecker.is_dict_type(t):
                    select.append({field_name: ["*"]})
                    return

                case t if TypeChecker.is_primitive_type(t):
                    # Primitive types are included in "*" so we don't need to add them explicitly
                    return

                case _:
                    raise InvalidFieldTypeError(
                        f"Unsupported field type for '{field_name}': {field_type}"
                    )
        except Exception as e:
            if not isinstance(e, FlureeSelectError):
                raise TypeProcessingError(
                    f"Error processing field '{field_name}' of type {field_type}: {str(e)}"
                ) from e
            raise

    def _handle_union_type(self, field_type: Any) -> Any:
        """Handle Union types by extracting the first non-None type."""
        origin = get_origin(field_type)
        if origin is UnionType:
            types = [t for t in get_args(field_type) if t is not type(None)]  # noqa: E721
            if types:
                return types[0]
        return field_type

    def _check_deeply_nested_structures(self, fields: dict[str, Any]) -> None:
        """Check for deeply nested structures that are not supported.
        
        Raises:
            DeeplyNestedStructureError: If a deeply nested structure is found
        """
        for field_name, field_type in fields.items():
            try:
                match field_type:
                    case t if TypeChecker.is_dict_type(t):
                        if TypeChecker.dict_max_depth(t) > 1:
                            raise DeeplyNestedStructureError(
                                f"Deeply nested dictionaries are not supported in field '{field_name}'"
                            )

                    case t if TypeChecker.is_list_type(t):
                        args = get_args(t)
                        if args:
                            inner_type = args[0]
                            if TypeChecker.is_tuple_type(inner_type):
                                raise DeeplyNestedStructureError(
                                    f"Tuples are not supported in field '{field_name}'"
                                )
                            if TypeChecker.dict_max_depth(inner_type) > 1:
                                raise DeeplyNestedStructureError(
                                    f"Deeply nested dictionaries are not supported in field '{field_name}'"
                                )
            except Exception as e:
                if not isinstance(e, FlureeSelectError):
                    raise TypeProcessingError(
                        f"Error checking nested structure for field '{field_name}': {str(e)}"
                    ) from e
                raise

    def _check_optional_fields(self, fields: dict[str, Any]) -> None:
        """Check for optional fields and add appropriate warnings."""
        non_id_fields = [f for f in fields if not TypeChecker.is_id_field(f)]
        if not non_id_fields:
            return

        all_optional = True
        for field_name in non_id_fields:
            field_type = fields[field_name]
            real_type = TypeChecker.get_real_type(field_type)
            
            if TypeChecker.is_list_type(real_type) or TypeChecker.is_base_model(real_type):
                all_optional = False
                break

        if all_optional:
            self.warning_manager.add_warning(
                PossibleEmptyModelWarning,
                "Model has only optional fields. This may result in an empty model when inserting.",
            )
        elif len(non_id_fields) == 1:
            field_name = non_id_fields[0]
            field_type = fields[field_name]
            real_type = TypeChecker.get_real_type(field_type)
            if not (TypeChecker.is_list_type(real_type) or TypeChecker.is_base_model(real_type)):
                self.warning_manager.add_warning(
                    PossibleEmptyModelWarning,
                    f"Model has a single optional field '{field_name}'. This may result in an empty model when inserting.",
                )

    def build(self, pydantic_model: T) -> list[Any]:
        """Build a Fluree select query structure from a Pydantic model.
        
        Raises:
            MissingIdFieldError: If the model is missing a required 'id' field
            DeeplyNestedStructureError: If the model contains unsupported deeply nested structures
            ModelConfigError: If there's an issue with the model configuration
        """
        model_type = type(pydantic_model) if isinstance(pydantic_model, BaseModel) else pydantic_model
        fields = get_type_hints(model_type, include_extras=True)

        # Early validation checks
        if "id" not in fields:
            raise MissingIdFieldError("Model must have an 'id' field")

        # Validate model configuration
        self._validate_model_config(model_type)

        # Check for deeply nested structures
        self._check_deeply_nested_structures(fields)

        # Process each field
        for field_name, field_type in fields.items():
            if field_name == "id":
                continue

            field_type = self._handle_union_type(field_type)
            self._process_field(field_name, field_type, self.select)

        # Check for optional fields
        self._check_optional_fields(fields)

        # Emit all collected warnings
        self.warning_manager.emit_warnings()
        return self.select


def from_pydantic(model: T) -> list[Any]:
    """Convert a Pydantic model to a Fluree select query structure.
    
    Example:
        >>> class User(BaseModel):
        ...     id: str
        ...     name: str
        >>> query = from_pydantic(User)
        >>> assert query == ["*"]
    """
    builder = FlureeSelectBuilder[T]()
    return builder.build(model)
