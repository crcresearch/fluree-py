import json
from collections.abc import Generator
from http import HTTPStatus

import pytest
import respx
from httpx import Request, Response
from respx import MockRouter, Route

from fluree_py import FlureeClient
from fluree_py.http.response import LedgerAlreadyExistsError, LedgerCreationResponse


def create_side_effect(request: Request, route: Route) -> Response:
    ledger = json.loads(request.content)["ledger"]

    # First call returns success
    if route.call_count == 0:
        return Response(
            HTTPStatus.CREATED,
            headers={"Content-Type": "application/json;charset=utf-8"},
            json={
                "commit": f"fluree:file://{ledger}/commit/bylyfvz5kexxf6l3tdzbobuz6eooxtgfxg3xqnp3pep7zfwxspkp.json",
                "ledger": ledger,
                "t": 1,
                "tx-id": "790b9747063d7878af67428ac92b37d2ff82971dee3ea533c053e44403a026de",
            },
        )

    # Second call returns conflict as we have already created the ledger
    return Response(
        HTTPStatus.CONFLICT,
        headers={"Content-Type": "application/json;charset=utf-8"},
        json={"error": f"Ledger {ledger} already exists"},
    )


@pytest.fixture
def mocked_api() -> Generator[MockRouter, None, None]:
    with respx.mock(base_url="http://localhost:8090", assert_all_called=False) as respx_mock:
        create_route = respx_mock.post("/fluree/create", name="create")
        create_route.side_effect = create_side_effect

        yield respx_mock


@pytest.fixture
def fluree_client(request: pytest.FixtureRequest, fluree_client: FlureeClient) -> Generator[FlureeClient, None, None]:
    # If we're using a real Fluree server, yield the client and ignore the mocked API
    if request.config.getoption("--use-fluree-server"):
        yield fluree_client
        return

    # If we're not using a real Fluree server, mock the API
    mocked_api: MockRouter = request.getfixturevalue("mocked_api")
    yield fluree_client

    # Assert that the mocked API was called
    mocked_api.assert_all_called()


def test_create_ledger(
    test_name: str,
    fluree_client: FlureeClient,
) -> None:
    context = {
        "ex": "http://example.org/",
        "schema": "http://schema.org/",
    }

    data = [
        {
            "@id": "ex:freddy",
            "@type": "ex:Yeti",
            "schema:age": 4,
            "schema:name": "Freddy",
        },
    ]

    resp = fluree_client.with_ledger(test_name).create().with_context(context).with_insert(data).commit()

    assert resp.status_code == HTTPStatus.CREATED
    assert resp.headers["Content-Type"] == "application/json;charset=utf-8"

    resp_json = resp.json()
    assert isinstance(resp_json, dict)

    assert "ledger" in resp_json
    assert resp_json["ledger"] == test_name

    assert "t" in resp_json
    assert resp_json["t"] == 1

    assert "commit" in resp_json
    assert resp_json["commit"].startswith(f"fluree:file://{test_name}/commit/")

    assert "tx-id" in resp_json

    # Additional assertions to verify that resp is a LedgerCreationResponse with correct attributes
    assert isinstance(resp, LedgerCreationResponse)
    assert resp.ledger == test_name
    assert resp.commit.startswith(f"fluree:file://{test_name}/commit/")
    assert resp.t == 1
    assert isinstance(resp.tx_id, str)


def test_create_ledger_already_exists(
    test_name: str,
    fluree_client: FlureeClient,
) -> None:
    context = {
        "ex": "http://example.org/",
        "schema": "http://schema.org/",
    }

    data = [
        {
            "@id": "ex:freddy",
            "@type": "ex:Yeti",
            "schema:age": 4,
            "schema:name": "Freddy",
        },
    ]

    request = fluree_client.with_ledger(test_name).create().with_context(context).with_insert(data)

    # First commit should succeed
    resp = request.commit()
    assert resp.status_code == HTTPStatus.CREATED

    # Second commit should raise a LedgerAlreadyExistsError
    with pytest.raises(LedgerAlreadyExistsError):
        resp = request.commit()
