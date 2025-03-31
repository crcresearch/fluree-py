from typing import Generic, TypeVar, cast

from fluree_py.ledger.mixin.utils import resolve_base_class_reference
from fluree_py.ledger.protocol.mixin import HasInsertData
from fluree_py.types import JsonArray, JsonObject


T = TypeVar("T", bound="HasInsertData")


class WithInsertMixin(Generic[T]):
    def with_insert(self, data: JsonObject | JsonArray) -> T:
        resolved_type = resolve_base_class_reference(self.__class__, "WithInsertMixin")

        # Create a new instance of the resolved type
        updated_fields = self.__dict__.copy()
        updated_fields["data"] = data
        return cast(T, resolved_type(**updated_fields))
