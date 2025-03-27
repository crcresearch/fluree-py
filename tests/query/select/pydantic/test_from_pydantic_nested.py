import warnings

import pytest
from pydantic import BaseModel, ConfigDict

from fluree_py.query.select.pydantic import from_pydantic


# Ignore all warnings in these tests
@pytest.fixture(scope="class", autouse=True)
def setup_class():
    warnings.filterwarnings("ignore")
    yield


# Config Dictionary Options
def test_model_config_allow_extra():
    class NestedModel(BaseModel):
        name: str
        model_config = ConfigDict(extra="allow")

    class Model(BaseModel):
        id: str
        nested: NestedModel

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]


def test_model_config_ignore_extra():
    class NestedModel(BaseModel):
        name: str
        model_config = ConfigDict(extra="ignore")

    class Model(BaseModel):
        id: str
        nested: NestedModel

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]


# Should handle nested models correctly
def test_nested_model_with_base_type():
    class NestedModel(BaseModel):
        id: str
        name: str

    class Model(BaseModel):
        id: str
        nested: NestedModel

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

def test_optional_nested_model_with_base_type():
    class NestedModel(BaseModel):
        id: str
        name: str

    class Model(BaseModel):
        id: str
        nested: NestedModel | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

# Should handle nested models with lists
def test_nested_model_with_list():
    class NestedModel(BaseModel):
        id: str
        entries: list[str]

    class Model(BaseModel):
        id: str
        nested: NestedModel

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]


# Should handle nested models with lists
def test_list_of_nested_models():
    class NestedModel(BaseModel):
        id: str
        entries: list[str]

    class Model(BaseModel):
        id: str
        nested: list[NestedModel]

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

# Should handle nested models with lists
def test_optional_list_of_nested_models():
    class NestedModel(BaseModel):
        id: str
        entries: list[str]

    class Model(BaseModel):
        id: str
        nested: list[NestedModel] | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]



# Should recursively handle nested models correctly
def test_nested_model_with_submodel():
    class SubNestedModel(BaseModel):
        id: str
        name: str

    class NestedModel(BaseModel):
        id: str
        subnested: SubNestedModel

    class Model(BaseModel):
        id: str
        nested: NestedModel

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*", {"subnested": ["*"]}]}]


def test_deeply_nested_dict():
    class Model(BaseModel):
        id: str
        level1: dict[str, dict[str, dict[str, str]]]

    select = from_pydantic(Model)
    assert select == ["*", {"level1": ["*"]}]

def test_circular_reference():
    class Model(BaseModel):
        id: str
        name: str

    class NestedModel(BaseModel):
        id: str
        parent: Model | None = None

    select = from_pydantic(NestedModel)
    assert select == ["*", {"parent": ["*"]}]