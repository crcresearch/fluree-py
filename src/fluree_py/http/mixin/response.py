from typing import Any, TypeVar

import httpx

from fluree_py.http.mixin.utils import find_type_for_base
from fluree_py.http.protocol.mixin.response import (
    SupportsFromResponse,
    SupportsRaisingFromResponse,
    SupportsResponseHandling,
)

T_Success = TypeVar("T_Success", bound=SupportsFromResponse)
T_Failure = TypeVar("T_Failure", bound=SupportsRaisingFromResponse)


class ResponseHandlingMixin(SupportsResponseHandling[T_Success, T_Failure]):
    def handle_response(self, response: httpx.Response) -> T_Success:
        target_types = find_type_for_base(self.__class__, "ResponseHandlingMixin")

        if not target_types:
            raise TypeError(f"{self.__class__.__name__} must be parameterized with a target type")

        print("target_types", target_types)

        # For each target type, try different conversion methods
        for target_type in target_types:
            # Skip TypeVar or non-concrete types
            if isinstance(target_type, TypeVar) or target_type is Any:
                continue

            converted = target_type.from_response(response)
            if converted is not None:
                return converted

        # If we get here, no conversion method worked
        raise ValueError(f"Could not convert response to any of the target types: {target_types}")
