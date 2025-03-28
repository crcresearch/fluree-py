import warnings

import pytest
from pydantic import BaseModel, ConfigDict

from fluree_py.client import FlureeClient
from fluree_py.query.select.pydantic import from_pydantic
from tests.utils import create_and_retrieve_random_model


# Ignore all warnings in these tests
@pytest.fixture(scope="class", autouse=True)
def setup_class():
    warnings.filterwarnings("ignore")
    yield


# Config Dictionary Options
def test_model_config_allow_extra(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
):
    class NestedModel(BaseModel):
        name: str
        model_config = ConfigDict(extra="allow")

    class Model(BaseModel):
        id: str
        nested: NestedModel

    assert from_pydantic(Model) == ["*", {"nested": ["*"]}]

    if request.config.getoption("--use-fluree-server"):
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, request.node.name
        )

        # Remove id field from nested models as it is added by Fluree
        delattr(result_model.nested, "id")

        assert model == result_model


def test_model_config_ignore_extra(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
):
    class NestedModel(BaseModel):
        name: str
        model_config = ConfigDict(extra="ignore")

    class Model(BaseModel):
        id: str
        nested: NestedModel

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if request.config.getoption("--use-fluree-server"):
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, request.node.name
        )
        assert model == result_model


# Should handle nested models correctly
def test_nested_model_with_base_type(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
):
    class NestedModel(BaseModel):
        id: str
        name: str

    class Model(BaseModel):
        id: str
        nested: NestedModel

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if request.config.getoption("--use-fluree-server"):
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, request.node.name
        )
        assert model == result_model


def test_optional_nested_model_with_base_type(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
):
    class NestedModel(BaseModel):
        id: str
        name: str

    class Model(BaseModel):
        id: str
        nested: NestedModel | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if request.config.getoption("--use-fluree-server"):
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, request.node.name
        )
        assert model == result_model


# Should handle nested models with lists
def test_nested_model_with_list(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
):
    class NestedModel(BaseModel):
        id: str
        entries: list[str]

    class Model(BaseModel):
        id: str
        nested: NestedModel

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if request.config.getoption("--use-fluree-server"):
        model, result_model = create_and_retrieve_random_model(
            Model,
            fluree_client,
            request.node.name,
            {"entries": {"@container": "@list"}},
        )
        assert model == result_model


# Should handle nested models with lists
def test_list_of_nested_models(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
):
    class NestedModel(BaseModel):
        id: str
        entries: list[str]

    class Model(BaseModel):
        id: str
        nested: list[NestedModel]

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if request.config.getoption("--use-fluree-server"):
        model, result_model = create_and_retrieve_random_model(
            Model,
            fluree_client,
            request.node.name,
            {"nested": {"@container": "@list"}, "entries": {"@container": "@list"}},
        )
        assert model == result_model


# Should handle nested models with lists
def test_optional_list_of_nested_models(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
):
    class NestedModel(BaseModel):
        id: str
        entries: list[str]

    class Model(BaseModel):
        id: str
        nested: list[NestedModel] | None = None

    select = from_pydantic(Model)
    assert select == ["*", {"nested": ["*"]}]

    if request.config.getoption("--use-fluree-server"):
        model, result_model = create_and_retrieve_random_model(
            Model,
            fluree_client,
            request.node.name,
            {"nested": {"@container": "@list"}, "entries": {"@container": "@list"}},
        )
        assert model == result_model


# Should recursively handle nested models correctly
def test_nested_model_with_submodel(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
):
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

    if request.config.getoption("--use-fluree-server"):
        model, result_model = create_and_retrieve_random_model(
            Model, fluree_client, request.node.name
        )
        assert model == result_model


# def test_circular_reference():
#     class Model(BaseModel):
#         id: str
#         name: str

#     class NestedModel(BaseModel):
#         id: str
#         parent: Model | None = None

#     select = from_pydantic(NestedModel)
#     assert select == ["*", {"parent": ["*"]}]
