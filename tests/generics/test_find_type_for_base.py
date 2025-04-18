"""
Tests for find_type_for_base utility.
"""

from collections.abc import Callable
from types import new_class
from typing import Generic

import pytest

from fluree_py.http.mixin.utils import resolve_base_type_args
from tests.generics.conftest import (
    ConcreteFailure,
    ConcreteSuccess,
    T_Failure,
    T_Success,
)

# --- Generics and Mixins for testing ---


class MixinOne(Generic[T_Success]):
    pass


class MixinTwo(Generic[T_Success]):
    pass


class MixinOneMulti(Generic[T_Success, T_Failure]):
    pass


class MixinTwoMulti(Generic[T_Success, T_Failure], MixinOneMulti[T_Success, T_Failure]):
    pass


# --- Test class factories ---
def make_inherited_base_class() -> type:
    class MixinTwoInherited(MixinOne[T_Success]):
        pass

    class ConcreteMixinTwoInherited(MixinTwoInherited[ConcreteSuccess]):
        pass

    return ConcreteMixinTwoInherited


def make_inherited_generic_args_class() -> type:
    class MixinTwoInherited(MixinOne[T_Success]):
        pass

    class ConcreteMixinTwoInherited(MixinTwoInherited[ConcreteSuccess]):
        pass

    return ConcreteMixinTwoInherited


def make_forward_ref_class() -> type:
    class ForwardRef(MixinOne["ConcreteSuccess"]):
        pass

    return ForwardRef


# --- Parametrized tests ---
@pytest.mark.parametrize(
    ("class_factory", "base_name", "expected"),
    [
        (
            lambda: new_class("SingleGeneric", (MixinOne[ConcreteSuccess],), {}),
            "MixinOne",
            [ConcreteSuccess],
        ),
        (
            make_forward_ref_class,
            "MixinOne",
            [ConcreteSuccess],
        ),
        (
            lambda: new_class("MultipleBases", (MixinOne[ConcreteSuccess], MixinTwo[ConcreteSuccess]), {}),
            "MixinOne",
            [ConcreteSuccess],
        ),
        (
            make_inherited_base_class,
            "MixinTwoInherited",
            [ConcreteSuccess],
        ),
        (
            make_inherited_generic_args_class,
            "MixinOne",
            [ConcreteSuccess],
        ),
        (
            lambda: new_class("MultipleGenerics", (MixinOneMulti[ConcreteSuccess, ConcreteFailure],), {}),
            "MixinOneMulti",
            [ConcreteSuccess, ConcreteFailure],
        ),
        (
            lambda: new_class("InheritedArgs", (MixinTwoMulti[ConcreteSuccess, ConcreteFailure],), {}),
            "MixinTwoMulti",
            [ConcreteSuccess, ConcreteFailure],
        ),
        (
            lambda: new_class("InheritedBaseArgs", (MixinTwoMulti[ConcreteSuccess, ConcreteFailure],), {}),
            "MixinOneMulti",
            [ConcreteSuccess, ConcreteFailure],
        ),
    ],
    ids=[
        "single_generic",
        "forward_ref",
        "multiple_bases",
        "inherited_base",
        "inherited_generic_args",
        "multiple_generics",
        "inherited_args",
        "inherited_base_args",
    ],
)
def test_find_type_for_base(class_factory: Callable[[], type], base_name: str, expected: list[type]) -> None:
    cls = class_factory()
    assert resolve_base_type_args(cls, base_name) == expected, f"Failed for {cls.__name__} and base {base_name}"


@pytest.mark.parametrize(
    "base_name",
    [
        "MixinOne",
        MixinOne,
    ],
    ids=["base_name_str", "base_name_class"],
)
def test_find_type_for_base_str_and_class_name(base_name: str | type) -> None:
    DynamicClass = new_class("DynamicClass", (MixinOne[ConcreteSuccess],), {})  # noqa: N806
    assert resolve_base_type_args(DynamicClass, base_name) == [ConcreteSuccess]
