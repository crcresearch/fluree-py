# Error Tests
import pytest
from pydantic import BaseModel, ConfigDict

from fluree_py.query.select.pydantic import from_pydantic


def test_no_root_id():
    class Model(BaseModel):
        name: str  # Model without id field

    with pytest.raises(ValueError):
        from_pydantic(Model)


# Should raise a error if a nested model doesn't have an id field and model config doesn't allow extra fields
def test_nested_model_no_id():
    class NestedModel(BaseModel):
        name: str

    class Model(BaseModel):
        id: str
        nested: NestedModel

    with pytest.raises(ValueError):
        from_pydantic(Model)


# Should raise a error if a nested model doesn't have an id field and model config forbids extra fields
def test_nested_model_no_id_forbid_extra():
    class NestedModel(BaseModel):
        name: str
        model_config = ConfigDict(extra="forbid")

    class Model(BaseModel):
        id: str
        nested: NestedModel

    with pytest.raises(ValueError):
        from_pydantic(Model)
