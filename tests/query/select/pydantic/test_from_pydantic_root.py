import warnings

import pytest
from pydantic import BaseModel, Field

from fluree_py.query.select.pydantic import from_pydantic


# Ignore all warnings in these tests
@pytest.fixture(scope="class", autouse=True)
def setup_class():
    warnings.filterwarnings("ignore")
    yield


# Base Types
def test_base_type():
    class Model(BaseModel):
        id: str
        name: str

    select = from_pydantic(Model)
    assert select == ["*"]

# List of Base Types
def test_list_of_base_type():
    class Model(BaseModel):
        id: str
        name: list[str]

    select = from_pydantic(Model)
    assert select == ["*"]

def test_optional_list_of_base_type():
    class Model(BaseModel):
        id: str
        name: list[str] | None = None

    select = from_pydantic(Model)
    assert select == ["*"]

def test_optional_list_of_base_type_with_initializer():
    class Model(BaseModel):
        id: str
        name: list[str] | None = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*"]

# Set of Base Types
def test_set_of_base_type():
    class Model(BaseModel):
        id: str
        name: set[str]

    select = from_pydantic(Model)
    assert select == ["*"]

def test_optional_set_of_base_type():
    class Model(BaseModel):
        id: str
        name: set[str] | None = None

    select = from_pydantic(Model)
    assert select == ["*"]

def test_optional_set_of_base_type_with_initializer():
    class Model(BaseModel):
        id: str
        name: set[str] | None = Field(default_factory=set)

    select = from_pydantic(Model)
    assert select == ["*"]

# Dictionaries
def test_dict():
    class Model(BaseModel):
        id: str
        nested: dict[str, str]

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

def test_optional_dict():
    class Model(BaseModel):
        id: str
        nested: dict[str, str] | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

def test_dict_with_initializer():
    class Model(BaseModel):
        id: str
        nested: dict[str, str] = Field(default_factory=dict)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

def test_optional_dict_with_initializer():
    class Model(BaseModel):
        id: str
        nested: dict[str, str] | None = Field(default_factory=dict)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

# List of Dictionaries
def test_list_of_dict():
    class Model(BaseModel):
        id: str
        nested: list[dict[str, str]]

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

def test_optional_list_of_dict():
    class Model(BaseModel):
        id: str
        nested: list[dict[str, str]] | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]


def test_list_of_dict_with_initializer():
    class Model(BaseModel):
        id: str
        nested: list[dict[str, str]] = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

def test_optional_list_of_dict_with_initializer():
    class Model(BaseModel):
        id: str
        nested: list[dict[str, str]] | None = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

# List of Sets
def test_list_of_set():
    class Model(BaseModel):
        id: str
        nested: list[set[str]]

    select = from_pydantic(Model)
    assert select == ["*"]

def test_optional_list_of_set():
    class Model(BaseModel):
        id: str
        nested: list[set[str]] | None = None

    select = from_pydantic(Model)
    assert select == ["*"]


def test_list_of_set_with_initializer():
    class Model(BaseModel):
        id: str
        nested: list[set[str]] = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*"]

def test_optional_list_of_set_with_initializer():
    class Model(BaseModel):
        id: str
        nested: list[set[str]] | None = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*"]

# List of Tuples
def test_list_of_tuple():
    class Model(BaseModel):
        id: str
        nested: list[tuple[str, str]]

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

def test_optional_list_of_tuple():
    class Model(BaseModel):
        id: str
        nested: list[tuple[str, str]] | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]


def test_list_of_tuple_with_initializer():
    class Model(BaseModel):
        id: str
        nested: list[tuple[str, str]] = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

def test_optional_list_of_tuple_with_initializer():
    class Model(BaseModel):
        id: str
        nested: list[tuple[str, str]] | None = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]