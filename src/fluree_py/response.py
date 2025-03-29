from dataclasses import dataclass
from typing import TypeVar, cast

from httpx import Headers, Response

from fluree_py.types import JsonArray, JsonObject

T = TypeVar("T")


@dataclass(frozen=True, kw_only=True)
class FlureeResponse:
    response: Response

    def json(self) -> JsonObject | JsonArray:
        """Parse the response as JSON."""
        return self.response.json()
    
    @property
    def text(self) -> str:
        """Get the response text."""
        return self.response.text

    @property
    def bytes(self) -> bytes:
        """Get the response bytes."""
        return self.response.content

    @property
    def headers(self) -> Headers:
        """Get the response headers."""
        return self.response.headers

    @property
    def status_code(self) -> int:
        """Get the response status code."""
        return self.response.status_code

    @property
    def is_success(self) -> bool:
        """Check if the response was successful."""
        return self.response.is_success

    def cast(self, type_: type[T]) -> T:
        """Cast the JSON response to a specific type."""
        return cast(T, self.json())