"""
Tests for find_type_for_base_arg utility.
"""

from typing import Generic, TypeVar

import pytest

from fluree_py.http.mixin.utils import resolve_base_type_arg
from tests.generics.conftest import ConcreteFailure, ConcreteSuccess, T_Failure, T_Success

# --- Generics and Mixins for testing ---


class MixinOneMulti(Generic[T_Success, T_Failure]):
    pass


class ConcreteMixin(MixinOneMulti[ConcreteSuccess, ConcreteFailure]):
    pass


# --- Parametrized tests ---
@pytest.mark.parametrize(
    ("typevar", "expected_cls"),
    [
        (T_Success, ConcreteSuccess),
        (T_Failure, ConcreteFailure),
    ],
)
def test_with_typevar(typevar: TypeVar, expected_cls: type) -> None:
    """Should find the correct type for a given TypeVar argument."""
    assert resolve_base_type_arg(ConcreteMixin, "MixinOneMulti", typevar) == [expected_cls]


@pytest.mark.parametrize(
    ("typevar_name", "expected_cls"),
    [
        ("T_Success", ConcreteSuccess),
        ("T_Failure", ConcreteFailure),
    ],
)
def test_with_str(typevar_name: str, expected_cls: type) -> None:
    """Should find the correct type for a given TypeVar argument as a string."""
    assert resolve_base_type_arg(ConcreteMixin, "MixinOneMulti", typevar_name) == [expected_cls]
