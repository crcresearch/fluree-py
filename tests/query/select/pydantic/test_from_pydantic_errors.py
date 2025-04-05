# Error Tests
import pytest
from pydantic import BaseModel, ConfigDict

from fluree_py.query.select.pydantic import (
    MissingIdFieldError,
    from_pydantic,
)
from fluree_py.query.select.pydantic.error import (
    DeeplyNestedDictionaryError,
    NestedTupleError,
)


def test_no_root_id() -> None:
    class Model(BaseModel):
        name: str  # Model without id field

    with pytest.raises(MissingIdFieldError):
        from_pydantic(Model)


# Should raise a error if a nested model doesn't have an id field and model config doesn't allow extra fields
def test_nested_model_no_id() -> None:
    class NestedModel(BaseModel):
        name: str

    class Model(BaseModel):
        id: str
        nested: NestedModel

    with pytest.raises(MissingIdFieldError):
        from_pydantic(Model)


# Should raise a error if a nested model doesn't have an id field and model config forbids extra fields
def test_nested_model_no_id_forbid_extra() -> None:
    class NestedModel(BaseModel):
        name: str
        model_config = ConfigDict(extra="forbid")

    class Model(BaseModel):
        id: str
        nested: NestedModel

    with pytest.raises(MissingIdFieldError):
        from_pydantic(Model)


# Should raise a error if a deeply nested dict is used because we can't infer the names of the keys
def test_deeply_nested_dict() -> None:
    class Model(BaseModel):
        id: str
        level1: dict[str, dict[str, dict[str, str]]]

    with pytest.raises(DeeplyNestedDictionaryError):
        from_pydantic(Model)


# Should raise an error if a list of tuples are used as a field type
def test_list_of_tuple_field() -> None:
    class Model(BaseModel):
        id: str
        nested: list[tuple[str, str]]

    with pytest.raises(NestedTupleError):
        from_pydantic(Model)


# Should raise an error if we encounter a circular dependency
