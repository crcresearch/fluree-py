from types import UnionType
from pydantic import BaseModel


from typing import Any, List, Type, TypeGuard, get_args, get_origin, get_type_hints


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
    def is_primitive_type(
        cls, field_type: Any
    ) -> TypeGuard[Type[str | int | float | bool]]:
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
    def is_base_model(cls, field_type: Any) -> TypeGuard[Type[BaseModel]]:
        """Check if a type is a BaseModel."""
        return isinstance(field_type, type) and issubclass(field_type, BaseModel)

    @classmethod
    def get_real_type(cls, field_type: Any) -> Any:
        """Get the real type from a potentially optional/union type."""
        origin = get_origin(field_type)
        if origin is UnionType:
            types = [t for t in get_args(field_type) if t is not type(None)]  # noqa: E721
            if types:
                for t in types:
                    if cls.is_list_type(t):
                        return t
                return types[0]
        return field_type

    @classmethod
    def check_model_has_id(cls, model: Type[BaseModel]) -> bool:
        """Check if a model has an id field in its type hints."""
        return "id" in get_type_hints(model, include_extras=True)

    @classmethod
    def has_model_config(cls, model: Type[BaseModel]) -> TypeGuard[Type[BaseModel]]:
        """Check if a model has a model_config attribute."""
        return hasattr(model, "model_config")

    @classmethod
    def check_model_requires_id(cls, model: Type[BaseModel]) -> bool:
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
