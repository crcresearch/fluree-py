from typing import Any, Generic, TypeVar, cast
from fluree_py.ledger.mixin.utils import resolve_base_class_reference
from fluree_py.ledger.protocol.mixin import HasContextData


T = TypeVar("T", bound="HasContextData")


class WithContextMixin(Generic[T]):
    def with_context(self, context: dict[str, Any]) -> T:
        resolved_type = resolve_base_class_reference(self.__class__, "WithContextMixin")

        # Manually create a new instance with updated context
        updated_fields = self.__dict__.copy()
        updated_fields["context"] = context
        return cast(T, resolved_type(**updated_fields))
