import warnings
from types import UnionType
from typing import Any, List, Tuple, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel


class ListOrderWarning(RuntimeWarning):
    pass


class PossibleEmptyModelWarning(RuntimeWarning):
    pass


def _check_model_has_id(model: type[BaseModel]) -> bool:
    """Check if a model has an id field in its type hints."""
    fields = get_type_hints(model, include_extras=True)
    return "id" in fields


def _check_model_requires_id(model: type[BaseModel]) -> bool:
    """Check if a model requires an id field based on its configuration."""
    # Get the model's config
    config = getattr(model, "model_config", None)
    if not config:
        return True  # Default to requiring id if no config

    # If config is a dict, get the extra setting
    if isinstance(config, dict):
        extra = config.get("extra", "ignore")
    else:
        # If config is a ConfigDict, get the extra setting
        extra = getattr(config, "extra", "ignore")

    # If extra is 'forbid' or not set (default), require id
    return extra in ("forbid", None)


def _get_real_type(field_type: Any) -> Any:
    """Get the real type from a potentially optional/union type."""
    origin = get_origin(field_type)
    if origin is Union:
        # Get non-None types from Union
        types = [t for t in get_args(field_type) if t is not type(None)]  # noqa: E721
        if types:
            # If we have a list type in the Union, use that
            for t in types:
                if hasattr(t, "__origin__") and t.__origin__ is list:
                    return t
            return types[0]
    return field_type


def _process_nested_model(
    field_name: str,
    field_type: type[BaseModel],
    warnings_list: List[Tuple[Warning, str]],
) -> dict[str, Any]:
    """Process a nested model and return its select structure."""
    # Check if the nested model requires an id field
    if _check_model_requires_id(field_type) and not _check_model_has_id(field_type):
        raise ValueError(
            f"Nested model '{field_type.__name__}' must have an 'id' field"
        )

    # Get all fields and their types
    fields = get_type_hints(field_type, include_extras=True)

    # Initialize select structure
    select = ["*"]

    # Process each field
    for nested_field_name, nested_field_type in fields.items():
        # Skip the id field as it's handled by the root select
        if nested_field_name == "id":
            continue

        # Get real type (handle Optional/Union)
        real_type = _get_real_type(nested_field_type)

        # Handle list types
        if hasattr(real_type, "__origin__") and real_type.__origin__ is list:
            warnings_list.append(
                (
                    ListOrderWarning,
                    f"Field '{nested_field_name}' is a list type. Order will be non-deterministic.",
                )
            )
            # Get the type argument of the list
            args = get_args(real_type)
            if args:
                inner_type = _get_real_type(args[0])
                # Add nested select for complex types (BaseModel, dict)
                if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
                    select.append(
                        _process_nested_model(
                            nested_field_name, inner_type, warnings_list
                        )
                    )
                elif (
                    hasattr(inner_type, "__origin__") and inner_type.__origin__ is dict
                ):
                    select.append({nested_field_name: ["*"]})
            continue

        # Handle nested models
        if isinstance(real_type, type) and issubclass(real_type, BaseModel):
            select.append(
                _process_nested_model(nested_field_name, real_type, warnings_list)
            )
            continue

        # Handle nested dictionaries
        if hasattr(real_type, "__origin__") and real_type.__origin__ is dict:
            select.append({nested_field_name: ["*"]})
            continue

    return {field_name: select}


def from_pydantic(pydantic_model: BaseModel) -> list[Any]:
    # Get all fields and their types
    fields = get_type_hints(
        pydantic_model if isinstance(pydantic_model, type) else type(pydantic_model),
        include_extras=True,
    )

    # Early validation checks
    if "id" not in fields:
        raise ValueError("Model must have an 'id' field")

    # Check for deeply nested dictionaries early
    for field_name, field_type in fields.items():
        if hasattr(field_type, "__origin__") and field_type.__origin__ is dict:
            if str(field_type).count("dict") > 1:
                raise ValueError("Deeply nested dictionaries are not supported")

        # Check list types for deeply nested structures
        if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
            args = get_args(field_type)
            if args:
                inner_type = args[0]
                if str(inner_type).startswith("tuple"):
                    raise ValueError("Tuples are not supported")
                if hasattr(inner_type, "__origin__") and inner_type.__origin__ is dict:
                    if str(inner_type).count("dict") > 1:
                        raise ValueError("Deeply nested dictionaries are not supported")

    # Initialize warnings list
    warnings_list: List[Tuple[Warning, str]] = []

    # Check for optional fields
    non_id_fields = [f for f in fields if f != "id"]
    if non_id_fields:
        # Check if all non-id fields are optional
        all_optional = True
        for field_name in non_id_fields:
            field_type = fields[field_name]
            origin = get_origin(field_type)
            if origin is UnionType:
                types = [t for t in get_args(field_type) if t is not type(None)]  # noqa: E721
                if not types:
                    continue
                field_type = types[0]

            # Skip warning for list types since empty lists are valid
            if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
                all_optional = False
                break

            # Skip warning for nested models since they have their own validation
            if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                all_optional = False
                break

            all_optional = False
            break

        if all_optional:
            warnings_list.append(
                (
                    PossibleEmptyModelWarning,
                    "Model has only optional fields. This may result in an empty model when inserting.",
                )
            )
        elif len(non_id_fields) == 1:
            field_name = non_id_fields[0]
            field_type = fields[field_name]
            # Skip warning for list types and nested models since they have their own validation
            if not (
                (hasattr(field_type, "__origin__") and field_type.__origin__ is list)
                or (isinstance(field_type, type) and issubclass(field_type, BaseModel))
            ):
                warnings_list.append(
                    (
                        PossibleEmptyModelWarning,
                        f"Model has a single optional field '{field_name}'. This may result in an empty model when inserting.",
                    )
                )

    # Initialize select structure
    select = ["*"]

    # Process each field
    for field_name, field_type in fields.items():
        # Skip the id field as it's handled by the root select
        if field_name == "id":
            continue

        # Handle Union types first
        origin = get_origin(field_type)
        if origin is UnionType:
            # Get non-None types from Union
            types = [t for t in get_args(field_type) if t is not type(None)]  # noqa: E721
            if types:
                field_type = types[0]

        # Handle list types
        if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
            warnings_list.append(
                (
                    ListOrderWarning,
                    f"Field '{field_name}' is a list type. Order will be non-deterministic.",
                )
            )
            # Get the type argument of the list
            args = get_args(field_type)
            if args:
                inner_type = args[0]
                # Add nested select for complex types (BaseModel, dict)
                if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
                    select.append(
                        _process_nested_model(field_name, inner_type, warnings_list)
                    )
                elif (
                    hasattr(inner_type, "__origin__") and inner_type.__origin__ is dict
                ):
                    select.append({field_name: ["*"]})
            continue

        # Handle nested models
        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            select.append(_process_nested_model(field_name, field_type, warnings_list))
            continue

        # Handle nested dictionaries
        if hasattr(field_type, "__origin__") and field_type.__origin__ is dict:
            select.append({field_name: ["*"]})
            continue

    # Emit all collected warnings at the end
    for warning_type, message in warnings_list:
        warnings.warn(message, warning_type)

    return select
