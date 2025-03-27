# Warning Tests
import pytest
from pydantic import BaseModel

from fluree_py.query.select.pydantic import ListOrderWarning, from_pydantic


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
        entries: list[str]

    class Model(BaseModel):
        id: str
        entries: NestedModel

    with pytest.warns(ListOrderWarning):
        from_pydantic(Model)

def test_inside_nested_model_list():
    class NestedModel(BaseModel):
        id: str
        entries: list[str]

    class Model(BaseModel):
        id: str
        entries: list[NestedModel]

    with pytest.warns(ListOrderWarning):
        from_pydantic(Model)