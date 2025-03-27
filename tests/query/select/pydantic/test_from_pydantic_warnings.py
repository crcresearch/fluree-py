# Warning Tests
import pytest
from pydantic import BaseModel

from fluree_py.query.select.pydantic import (
    ListOrderWarning,
    PossibleEmptyModelWarning,
    from_pydantic,
)


def test_list_of_base_types():
    class Model(BaseModel):
        id: str
        entries: list[str]

    with pytest.warns(ListOrderWarning):
        from_pydantic(Model)


def test_list_of_dictionaries():
    class Model(BaseModel):
        id: str
        entries: list[dict[str, str]]

    with pytest.warns(ListOrderWarning):
        from_pydantic(Model)


def test_inside_nested_model():
    class NestedModel(BaseModel):
        id: str
        nested_entries: list[str]

    class Model(BaseModel):
        id: str
        entries: NestedModel

    with pytest.warns(ListOrderWarning):
        from_pydantic(Model)


def test_inside_nested_model_list():
    class NestedModel(BaseModel):
        id: str
        nested_entries: list[str]

    class Model(BaseModel):
        id: str
        entries: list[NestedModel]

    with pytest.warns(ListOrderWarning):
        from_pydantic(Model)


# Should warn if a model has a single optional field as fluree won't accept an insert with just an ID field
def test_single_optional_field():
    class Model(BaseModel):
        id: str
        name: str | None = None

    with pytest.warns(PossibleEmptyModelWarning):
        from_pydantic(Model)


# Should warn if a model has only optional fields as fluree won't accept an insert with just an ID field
def test_only_optional_fields():
    class Model(BaseModel):
        id: str
        name: str | None = None

    with pytest.warns(PossibleEmptyModelWarning):
        from_pydantic(Model)
