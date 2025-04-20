from http import HTTPStatus

from httpx import Response

from fluree_py.http.response import LedgerCreationResponse


def test_ledger_creation_response_from_response() -> None:
    # Define a JSON payload similar to what a ledger creation might return
    json_payload = {"ledger": "test-ledger", "commit": "test-commit", "t": 1, "tx-id": "test-tx-id"}

    # Create a simulated HTTP response with the JSON payload
    response = Response(HTTPStatus.CREATED, headers={"Content-Type": "application/json"}, json=json_payload)

    # Use LedgerCreationResponse.from_response to wrap the HTTP response
    ledger_response = LedgerCreationResponse.from_response(response)

    # Validate that the LedgerCreationResponse contains the correct data
    assert ledger_response.response.status_code == HTTPStatus.CREATED

    # The json() method of LedgerCreationResponse should return our payload
    assert ledger_response.json() == json_payload

    # Ensure the returned type is indeed LedgerCreationResponse
    assert isinstance(ledger_response, LedgerCreationResponse)

    # Verify that the attributes are accessible and correct
    assert ledger_response.ledger == "test-ledger"
    assert ledger_response.commit == "test-commit"
    assert ledger_response.t == 1
    assert ledger_response.tx_id == "test-tx-id"
