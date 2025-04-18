"""
Tests for find_type_for_base_arg utility.
"""

from typing import Generic, TypeVar

import pytest

from fluree_py.http.mixin.commit import CommitableMixin
from fluree_py.http.mixin.context import WithContextMixin
from fluree_py.http.mixin.insert import WithInsertMixin
from fluree_py.http.mixin.utils import resolve_base_type_arg
from fluree_py.http.response import FlureeResponse, MissingTransactionError
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


# --- Realistic production-like test for mixin/generic chain ---
def test_realistic_commit_chain_type_resolution():
    class RealisticTestImpl(
        CommitableMixin[FlureeResponse, MissingTransactionError],
        WithContextMixin["RealisticTestImpl"],
        WithInsertMixin["RealisticTestImpl"],
    ):
        pass

    # Should resolve to the real types, not TypeVar
    success_types = resolve_base_type_arg(RealisticTestImpl, "ResponseHandlingMixin", "T_Success_co")
    failure_types = resolve_base_type_arg(RealisticTestImpl, "ResponseHandlingMixin", "T_Failure_co")

    assert success_types == [FlureeResponse], f"Expected FlureeResponse, got {success_types}"
    assert failure_types == [MissingTransactionError], f"Expected MissingTransactionError, got {failure_types}"
    assert all(not hasattr(t, "__name__") or not t.__name__.startswith("T_") for t in success_types + failure_types), (
        "TypeVars should not leak into runtime resolution"
    )


# --- Minimal mock tests for multi-level generic propagation ---
from typing import Generic, TypeVar


def test_typevar_leakage_simple_chain():
    T = TypeVar("T")
    U = TypeVar("U")

    class Base(Generic[T, U]):
        pass

    class Mid(Base[T, U]):
        pass

    class Concrete(Mid[int, str]):
        pass

    # This should resolve to int and str, but will likely leak TypeVar in current utility
    from fluree_py.http.mixin.utils import resolve_base_type_arg

    assert resolve_base_type_arg(Concrete, "Base", "T") == [int], "Should resolve T to int"
    assert resolve_base_type_arg(Concrete, "Base", "U") == [str], "Should resolve U to str"


def test_typevar_leakage_with_mixin():
    T = TypeVar("T")

    class Base(Generic[T]):
        pass

    class Mixin(Base[T]):
        pass

    class Concrete(Mixin[int]):
        pass

    from fluree_py.http.mixin.utils import resolve_base_type_arg

    assert resolve_base_type_arg(Concrete, "Base", "T") == [int], "Should resolve T to int"
