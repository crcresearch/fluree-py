from dataclasses import dataclass
from http import HTTPStatus
from typing import Self, TypeVar

from httpx import Headers, Response

from fluree_py.types.common import JsonArray, JsonObject

T = TypeVar("T")


@dataclass(frozen=True, kw_only=True)
class FlureeResponse:
    """A response from the Fluree ledger."""

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

    @classmethod
    def from_response(cls, response: Response) -> Self | None:
        return cls(response=response)


class MissingTransactionError(Exception):
    """Exception raised when a transaction is missing."""

    def __init__(self, ledger: str):
        self.message = f"Ledger {ledger} does not exist!"
        super().__init__(self.message)

    @classmethod
    def raise_from_response(cls, response: Response) -> None:
        if response.status_code == HTTPStatus.CONFLICT:
            json = response.json()
            if "error" in json:
                raise cls(json["error"])
