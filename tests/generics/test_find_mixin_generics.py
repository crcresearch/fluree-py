from typing import Generic, TypeVar

from fluree_py.http.mixin.utils import find_type_for_base, find_type_for_base_arg


def test_find_single_base_simple():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    class MixinOne(Generic[T_Success]):
        pass

    class ConcreteMixinOne(MixinOne[ConcreteSuccess]):
        pass

    assert find_type_for_base(ConcreteMixinOne, "MixinOne") == [ConcreteSuccess]


def test_find_single_base_simple_forward_ref():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    class MixinOne(Generic[T_Success]):
        pass

    class ConcreteMixinOne(MixinOne["ConcreteSuccess"]):
        pass

    assert find_type_for_base(ConcreteMixinOne, "MixinOne") == [ConcreteSuccess]


def test_find_single_base_simple_multiple():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    class MixinOne(Generic[T_Success]):
        pass

    class MixinTwo(Generic[T_Success]):
        pass

    class ConcreteMixinOne(MixinOne[ConcreteSuccess], MixinTwo[ConcreteSuccess]):
        pass

    assert find_type_for_base(ConcreteMixinOne, "MixinOne") == [ConcreteSuccess]


def test_find_single_base_simple_inherited():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    class MixinOne(Generic[T_Success]):
        pass

    class MixinTwo(MixinOne[T_Success]):
        pass

    class ConcreteMixinTwo(MixinTwo[ConcreteSuccess]):
        pass

    assert find_type_for_base(ConcreteMixinTwo, "MixinTwo") == [ConcreteSuccess]


def test_find_single_base_simple_inherited_with_generic_args():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    class MixinOne(Generic[T_Success]):
        pass

    class MixinTwo(MixinOne[T_Success]):
        pass

    class ConcreteMixinTwo(MixinTwo[ConcreteSuccess]):
        pass

    assert find_type_for_base(ConcreteMixinTwo, "MixinOne") == [ConcreteSuccess]


def test_find_multiple_base_simple():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    T_Failure = TypeVar("T_Failure")

    class ConcreteFailure:
        pass

    class MixinOne(Generic[T_Success, T_Failure]):
        pass

    class ConcreteMixinOne(MixinOne[ConcreteSuccess, ConcreteFailure]):
        pass

    assert find_type_for_base(ConcreteMixinOne, "MixinOne") == [ConcreteSuccess, ConcreteFailure]


def test_find_args_inherited():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    T_Failure = TypeVar("T_Failure")

    class ConcreteFailure:
        pass

    class MixinOne(Generic[T_Success, T_Failure]):
        pass

    class MixinTwo(Generic[T_Success, T_Failure], MixinOne[T_Success, T_Failure]):
        pass

    class ConcreteMixinTwo(MixinTwo[ConcreteSuccess, ConcreteFailure]):
        pass

    assert find_type_for_base(ConcreteMixinTwo, "MixinTwo") == [ConcreteSuccess, ConcreteFailure]


def test_find_base_args_inherited():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    T_Failure = TypeVar("T_Failure")

    class ConcreteFailure:
        pass

    class MixinOne(Generic[T_Success, T_Failure]):
        pass

    class MixinTwo(Generic[T_Success, T_Failure], MixinOne[T_Success, T_Failure]):
        pass

    class ConcreteMixinTwo(MixinTwo[ConcreteSuccess, ConcreteFailure]):
        pass

    assert find_type_for_base(ConcreteMixinTwo, "MixinOne") == [ConcreteSuccess, ConcreteFailure]


def test_find_type_for_base_argument():
    T_Success = TypeVar("T_Success")

    class ConcreteSuccess:
        pass

    T_Failure = TypeVar("T_Failure")

    class ConcreteFailure:
        pass

    class Mixin(Generic[T_Success, T_Failure]):
        pass

    class ConcreteMixin(Mixin[ConcreteSuccess, ConcreteFailure]):
        pass

    assert find_type_for_base_arg(ConcreteMixin, "Mixin", T_Success) == [ConcreteSuccess]
    assert find_type_for_base_arg(ConcreteMixin, "Mixin", T_Failure) == [ConcreteFailure]
