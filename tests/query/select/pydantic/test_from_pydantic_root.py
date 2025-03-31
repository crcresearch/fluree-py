import warnings

import pytest
from pydantic import BaseModel, Field

from fluree_py.client import FlureeClient
from fluree_py.query.select.pydantic import from_pydantic
from tests.utils import create_and_retrieve_random_model


# Ignore all warnings in these tests
@pytest.fixture(scope="class", autouse=True)
def setup_class():
    warnings.filterwarnings("ignore")
    yield


# Base Types
def test_base_type(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        name: str

    select = from_pydantic(Model)
    assert select == ["*"]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name
        )
        assert model == result_model


# List of Base Types
def test_list_of_base_type(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        name: list[str]

    select = from_pydantic(Model)
    assert select == ["*"]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name, {"name": {"@container": "@list"}}
        )
        assert model == result_model


def test_optional_list_of_base_type(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        name: list[str] | None = None

    select = from_pydantic(Model)
    assert select == ["*"]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name, {"name": {"@container": "@list"}}
        )
        assert model == result_model


def test_optional_list_of_base_type_with_initializer(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        name: list[str] | None = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*"]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name, {"name": {"@container": "@list"}}
        )
        assert model == result_model


# Dictionaries
def test_dict(using_fluree_server: bool, test_name: str, fluree_client: FlureeClient):
    class Model(BaseModel):
        id: str
        nested: dict[str, str]

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name
        )

        # Remove id field from nested dictionary as it is added by Fluree
        del result_model.nested["id"]

        assert model == result_model


def test_optional_dict(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        nested: dict[str, str] | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name
        )

        # Remove id field from nested dictionary as it is added by Fluree
        if result_model.nested and "id" in result_model.nested:
            del result_model.nested["id"]

        assert model == result_model


def test_dict_with_initializer(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        nested: dict[str, str] = Field(default_factory=dict)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name
        )

        # Remove id field from nested dictionary as it is added by Fluree
        if result_model.nested and "id" in result_model.nested:
            del result_model.nested["id"]

        assert model == result_model


def test_optional_dict_with_initializer(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        nested: dict[str, str] | None = Field(default_factory=dict)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name
        )

        # Remove id field from nested dictionary as it is added by Fluree
        if result_model.nested and "id" in result_model.nested:
            del result_model.nested["id"]

        assert model == result_model


# List of Dictionaries
def test_list_of_dict(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        nested: list[dict[str, str]]

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name, {"nested": {"@container": "@list"}}
        )

        # Remove id field from nested models as it is added by Fluree
        for m in result_model.nested:
            del m["id"]

        assert model == result_model


def test_optional_list_of_dict(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        nested: list[dict[str, str]] | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name, {"nested": {"@container": "@list"}}
        )

        # Remove id field from nested models as it is added by Fluree
        if result_model.nested:
            for m in result_model.nested:
                del m["id"]

        assert model == result_model


def test_list_of_dict_with_initializer(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        nested: list[dict[str, str]] = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name, {"nested": {"@container": "@list"}}
        )

        # Remove id field from nested models as it is added by Fluree
        for m in result_model.nested:
            del m["id"]

        assert model == result_model


def test_optional_list_of_dict_with_initializer(
    using_fluree_server: bool, test_name: str, fluree_client: FlureeClient
):
    class Model(BaseModel):
        id: str
        nested: list[dict[str, str]] | None = Field(default_factory=list)

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if using_fluree_server:
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, test_name, {"nested": {"@container": "@list"}}
        )

        # Remove id field from nested models as it is added by Fluree
        if result_model.nested:
            for m in result_model.nested:
                del m["id"]

        assert model == result_model
