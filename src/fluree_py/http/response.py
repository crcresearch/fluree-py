"""
Response handling utilities for Fluree HTTP interactions.

This module defines the FlureeResponse dataclass, which wraps HTTPX Response objects to provide
convenient access to response data, status, and headers, as well as logging for JSON parsing.
It also defines custom exceptions for Fluree-specific error handling, such as missing transactions.
"""

import re
from dataclasses import dataclass
from http import HTTPStatus
from typing import Self

from httpx import Headers, Response

from fluree_py.http.mixin.response import SupportsRaisingFromResponse
from fluree_py.logging import logger
from fluree_py.types.common import JsonArray, JsonObject


@dataclass(frozen=True, kw_only=True)
class FlureeResponse:
    """A response from the Fluree ledger."""

    response: Response

    def json(self) -> JsonObject | JsonArray:
        """Parse the response as JSON."""
        logger.debug(
            "parsing_response_json",
            status_code=self.response.status_code,
            text_snippet=self.response.text[:200],
        )
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
    def from_response(cls, response: Response) -> Self:
        """Create a FlureeResponse from an HTTP response."""
        return cls(response=response)


@dataclass(frozen=True, kw_only=True)
class LedgerCreationResponse(FlureeResponse):
    """A response from the Fluree ledger."""

    ledger: str
    commit: str
    t: int
    tx_id: str

    @classmethod
    def from_response(cls, response: Response) -> Self:
        """Create a LedgerCreationResponse from an HTTP response with validations."""
        if not response.is_success:
            raise ValueError("Unsuccessful HTTP response")

        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Expected JSON object")

        required_keys = ["ledger", "commit", "t", "tx-id"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")

        if not isinstance(data["t"], int):
            raise ValueError("Invalid type for 't'")

        return cls(response=response, ledger=data["ledger"], commit=data["commit"], t=data["t"], tx_id=data["tx-id"])  # type: ignore[arg-type]


@dataclass(frozen=True, kw_only=True)
class QueryResponse(FlureeResponse):
    """A response from the Fluree ledger."""

    objects: list[JsonObject]

    @classmethod
    def from_response(cls, response: Response) -> Self:
        """Create a QueryResponse from an HTTP response."""
        return cls(response=response, objects=response.json())


class MissingTransactionError(Exception, SupportsRaisingFromResponse):
    """Exception raised when a transaction is missing."""

    def __init__(self, ledger: str) -> None:
        """Initialize the based on the response from the ledger."""
        self.message = f"Ledger {ledger} does not exist!"
        super().__init__(self.message)

    @classmethod
    def raise_from_response(cls, response: Response) -> Exception | None:
        """Raise an exception from a response if the status code is a conflict."""
        if response.status_code != HTTPStatus.CONFLICT:
            return None

        data = response.json()
        if "error" not in data:
            return None

        return cls(data["error"])


class LedgerAlreadyExistsError(Exception, SupportsRaisingFromResponse):
    """Exception raised when a ledger already exists."""

    def __init__(self, ledger: str) -> None:
        """Initialize the based on the response from the ledger."""
        self.message = f"Ledger {ledger} already exists!"
        super().__init__(self.message)

    @classmethod
    def raise_from_response(cls, response: Response) -> Exception | None:
        """Raise an exception from a response if the status code is a conflict."""
        if response.status_code != HTTPStatus.CONFLICT:
            return None

        data = response.json()
        if "error" not in data:
            return None

        match = re.match(r"Ledger (\w+) already exists", data["error"])
        if not match:
            return None

        return cls(ledger=match.group(1))
