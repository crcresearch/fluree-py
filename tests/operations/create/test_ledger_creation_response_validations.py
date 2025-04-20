from http import HTTPStatus

import pytest
from httpx import Response

from fluree_py.http.response import LedgerCreationResponse


def test_from_response_unsuccessful_status() -> None:
    # Define a valid JSON payload
    json_payload = {"ledger": "test-ledger", "commit": "test-commit", "t": 1, "tx-id": "test-tx-id"}
    # Create a response with an unsuccessful status code (e.g., 400 BAD REQUEST)
    response = Response(HTTPStatus.BAD_REQUEST, headers={"Content-Type": "application/json"}, json=json_payload)

    with pytest.raises(ValueError, match="Unsuccessful HTTP response"):
        LedgerCreationResponse.from_response(response)


def test_from_response_non_dict_json() -> None:
    # Provide a JSON payload that is not a dictionary
    json_payload = ["not", "a", "dict"]
    response = Response(HTTPStatus.CREATED, headers={"Content-Type": "application/json"}, json=json_payload)

    with pytest.raises(ValueError, match="Expected JSON object"):
        LedgerCreationResponse.from_response(response)


def test_from_response_missing_required_key() -> None:
    # Create a payload missing the 'ledger' key
    json_payload = {"commit": "test-commit", "t": 1, "tx-id": "test-tx-id"}
    response = Response(HTTPStatus.CREATED, headers={"Content-Type": "application/json"}, json=json_payload)

    with pytest.raises(ValueError, match="Missing required key"):
        LedgerCreationResponse.from_response(response)


def test_from_response_invalid_type_for_t() -> None:
    # Provide a payload where 't' is not an integer
    json_payload = {"ledger": "test-ledger", "commit": "test-commit", "t": "1", "tx-id": "test-tx-id"}
    response = Response(HTTPStatus.CREATED, headers={"Content-Type": "application/json"}, json=json_payload)

    with pytest.raises(ValueError, match="Invalid type for 't'"):
        LedgerCreationResponse.from_response(response)
