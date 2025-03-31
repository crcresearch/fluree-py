from typing import Any, Generic, TypeVar, cast
from fluree_py.ledger.mixin.utils import resolve_base_class_reference
from fluree_py.ledger.protocol.mixin import HasContextData


T = TypeVar("T", bound="HasContextData")


def print_special_vars(obj: Any) -> None:
    all_attributes = dir(obj)
    special_vars = [
        attr for attr in all_attributes if attr.startswith("__") and attr.endswith("__")
    ]
    print(f"Special vars: {special_vars}")
    for var in special_vars:
        print(f"\t{var}: {getattr(obj, var)}")


class WithContextMixin(Generic[T]):
    def with_context(self, context: dict[str, Any]) -> T:
        print_special_vars(self.__class__)
        resolved_type = resolve_base_class_reference(self.__class__, "WithContextMixin")
        print(resolved_type)

        # Manually create a new instance with updated context
        updated_fields = self.__dict__.copy()
        updated_fields["context"] = context
        return cast(T, resolved_type(**updated_fields))
