import warnings
from typing import Any, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel


class ListOrderWarning(RuntimeWarning):
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
            return types[0]
    return field_type

def _process_nested_model(field_name: str, field_type: type[BaseModel]) -> dict[str, Any]:
    """Process a nested model and return its select structure."""
    # Check if the nested model requires an id field
    if _check_model_requires_id(field_type) and not _check_model_has_id(field_type):
        raise ValueError(f"Nested model '{field_type.__name__}' must have an 'id' field")
        
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
            warnings.warn(
                f"Field '{nested_field_name}' is a list type. Order will be non-deterministic.",
                ListOrderWarning
            )
            # Get the type argument of the list
            args = get_args(real_type)
            if args:
                inner_type = _get_real_type(args[0])
                # Add nested select for complex types (BaseModel, dict)
                if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
                    select.append(_process_nested_model(nested_field_name, inner_type))
                elif hasattr(inner_type, "__origin__") and inner_type.__origin__ is dict:
                    select.append({nested_field_name: ["*"]})
            continue
            
        # Handle nested models
        if isinstance(real_type, type) and issubclass(real_type, BaseModel):
            select.append(_process_nested_model(nested_field_name, real_type))
            continue
            
        # Handle nested dictionaries
        if hasattr(real_type, "__origin__") and real_type.__origin__ is dict:
            select.append({nested_field_name: ["*"]})
            continue
            
    return {field_name: select}

def from_pydantic(pydantic_model: BaseModel) -> list[Any]:
    # Get all fields and their types
    fields = get_type_hints(pydantic_model if isinstance(pydantic_model, type) else type(pydantic_model), include_extras=True)
    
    # Check for root ID field
    if "id" not in fields:
        raise ValueError("Model must have an 'id' field")
    
    # Initialize select structure
    select = ["*"]
    
    # Process each field
    for field_name, field_type in fields.items():
        # Skip the id field as it's handled by the root select
        if field_name == "id":
            continue
            
        # Get real type (handle Optional/Union)
        real_type = _get_real_type(field_type)
            
        # Handle list types
        if hasattr(real_type, "__origin__") and real_type.__origin__ is list:
            warnings.warn(
                f"Field '{field_name}' is a list type. Order will be non-deterministic.",
                ListOrderWarning
            )
            # Get the type argument of the list
            args = get_args(real_type)
            if args:
                inner_type = _get_real_type(args[0])
                # Add nested select for complex types (BaseModel, dict)
                if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
                    # Process nested model in list
                    select.append(_process_nested_model(field_name, inner_type))
                elif hasattr(inner_type, "__origin__") and inner_type.__origin__ is dict:
                    select.append({field_name: ["*"]})
            continue
            
        # Handle nested models
        if isinstance(real_type, type) and issubclass(real_type, BaseModel):
            select.append(_process_nested_model(field_name, real_type))
            continue
            
        # Handle nested dictionaries
        if hasattr(real_type, "__origin__") and real_type.__origin__ is dict:
            select.append({field_name: ["*"]})
            continue
            
    return select