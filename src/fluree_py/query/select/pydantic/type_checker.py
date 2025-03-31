from types import UnionType
from pydantic import BaseModel


from typing import (
    Any,
    List,
    Type,
    TypeGuard,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)


class TypeChecker:
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
    def is_primitive_type(cls, field_type: Any) -> bool:
        """Check if a type is a primitive type (str, int, float, bool)."""
        return isinstance(field_type, type) and field_type in {str, int, float, bool}

    @classmethod
    def is_id_field(cls, field_name: str) -> bool:
        """Check if a field name is the id field."""
        return field_name == "id"

    @classmethod
    def dict_max_depth(cls, field_type: Any, depth: int = 0) -> int:
        """Recursively count dictionary nesting depth."""
        while TypeChecker.is_dict_type(field_type):
            args = get_args(field_type)
            if not args or len(args) < 2:
                break
            field_type = args[1]  # Move to the value type
            depth += 1
        return depth

    @classmethod
    def is_base_model(cls, field_type: Any) -> TypeGuard[Type[BaseModel]]:
        """Check if a type is a BaseModel."""
        return isinstance(field_type, type) and issubclass(field_type, BaseModel)

    @classmethod
    def get_real_type(cls, field_type: Any) -> Any:
        """Get the real type from a potentially optional/union type."""
        origin = get_origin(field_type)
        if origin in {Union, UnionType}:
            types = [t for t in get_args(field_type) if t is not type(None)]
            if types:
                return next((t for t in types if cls.is_list_type(t)), types[0])
        return field_type

    @classmethod
    def check_model_has_id(cls, model: Type[BaseModel]) -> bool:
        """Check if a model has an id field in its type hints."""
        return "id" in get_type_hints(model, include_extras=True)

    @classmethod
    def has_model_config(cls, model: Type[BaseModel]) -> bool:
        """Check if a model has a model_config attribute."""
        return hasattr(model, "model_config")

    @classmethod
    def check_model_requires_id(cls, model: Type[BaseModel]) -> bool:
        """Check if a model requires an id field based on its configuration."""
        if not cls.has_model_config(model):
            return True

        config = model.model_config
        if not config:
            return True

        extra = config.get("extra", "ignore")
        return extra in ("forbid", None)
