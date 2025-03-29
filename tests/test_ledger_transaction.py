import json
from typing import Generator

import pytest
import respx
from httpx import Request, Response
from pytest import FixtureRequest
from respx import MockRouter

from fluree_py import FlureeClient


def transact_side_effect(request: Request):
    ledger = json.loads(request.content)["ledger"]
    if ledger == "test_ledger_transaction_single_record":
        return Response(
            200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            json={
                "ledger": ledger,
                "commit": f"fluree:file://{ledger}/commit/bjuov2y7ovapwqrjza2mgaul4v5ge4faae2n42wifslfap6wvppo.json",
                "t": 2,
                "tx-id": "2a3e5896f19dbf9db70c2ee025a08964ae1ca5858e13d2dac7b5edeee730c370",
            },
        )
    elif ledger == "test_ledger_transaction_multiple_records":
        return Response(
            200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            json={
                "ledger": "test_ledger_transaction_multiple_records",
                "commit": "fluree:file://test_ledger_transaction_multiple_records/commit/qjgxryeobnyfxjczjszcwywyhp7iwwwtsqnidocw6rax3og2wuu.json",
                "t": 2,
                "tx-id": "48c46259a0912fb95d5266fbccf52f828670fb9fc5d60432b741a3e7e73302c3",
            },
        )
    return Response(404)


@pytest.fixture
def mocked_api() -> Generator[MockRouter, None, None]:
    with respx.mock(
        base_url="http://localhost:8090", assert_all_called=False
    ) as respx_mock:
        transact_route = respx_mock.post("/fluree/transact", name="transact")
        transact_route.side_effect = transact_side_effect

        yield respx_mock


@pytest.fixture
def cookbook_client(
    request: FixtureRequest, cookbook_client: FlureeClient
) -> Generator[FlureeClient, None, None]:
    # If we're using a real Fluree server, yield the client and ignore the mocked API
    if request.config.getoption("--use-fluree-server"):
        yield cookbook_client
        return

    # If we're not using a real Fluree server, mock the API
    mocked_api: MockRouter = request.getfixturevalue("mocked_api")
    yield cookbook_client

    # Assert that the mocked API was called
    create_route = mocked_api["transact"]
    assert create_route.call_count == 1
    assert (
        create_route.calls.last.request.url == "http://localhost:8090/fluree/transact"
    )
    assert create_route.calls.last.request.headers["Content-Type"] == "application/json"


# https://developers.flur.ee/docs/reference/cookbook/#inserting-a-single-record
def test_ledger_transaction_single_record(
    request: FixtureRequest, cookbook_client: FlureeClient
):
    resp = (
        cookbook_client.with_ledger(request.node.name)
        .transaction()
        .with_context({"ex": "http://example.org/", "schema": "http://schema.org/"})
        .with_insert(
            {
                "@id": "ex:fluree",
                "@type": "schema:Organization",
                "schema:description": "We ❤️ Data",
            }
        )
        .commit()
    )

    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json;charset=utf-8"

    resp_json = resp.json()
    assert isinstance(resp_json, dict)
    
    assert "ledger" in resp_json
    assert resp_json["ledger"] == request.node.name

    assert "t" in resp_json
    assert resp_json["t"] == 2

    assert "commit" in resp_json
    assert resp_json["commit"].startswith(f"fluree:file://{request.node.name}/commit/")

    assert "tx-id" in resp_json


# https://developers.flur.ee/docs/reference/cookbook/#inserting-multiple-records
def test_ledger_transaction_multiple_records(
    request: FixtureRequest, cookbook_client: FlureeClient
):
    resp = (
        cookbook_client.with_ledger(request.node.name)
        .transaction()
        .with_context({"ex": "http://example.org/", "schema": "http://schema.org/"})
        .with_insert(
            [
                {
                    "@id": "ex:w3c",
                    "@type": "schema:Organization",
                    "schema:description": "We ❤️ Internet",
                },
                {
                    "@id": "ex:mosquitos",
                    "@type": "ex:Monster",
                    "schema:description": "We ❤️ Human Blood",
                },
            ]
        )
        .commit()
    )

    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json;charset=utf-8"

    resp_json = resp.json()
    assert isinstance(resp_json, dict)

    assert "ledger" in resp_json
    assert resp_json["ledger"] == request.node.name

    assert "t" in resp_json
    assert resp_json["t"] == 2

    assert "commit" in resp_json
    assert resp_json["commit"].startswith(f"fluree:file://{request.node.name}/commit/")

    assert "tx-id" in resp_json


# Transaction Errors
def test_transaction_on_missing_ledger(
    request: FixtureRequest, fluree_client: FlureeClient
):
    resp = (
        fluree_client.with_ledger(request.node.name)
        .transaction()
        .with_context({"ex": "http://example.org/", "schema": "http://schema.org/"})
        .with_insert(
            {
                "@id": "ex:fluree",
                "@type": "schema:Organization",
                "schema:description": "We ❤️ Data",
            }
        )
        .commit()
    )

    assert resp.status_code == 409
    assert resp.json() == {"error": f"Ledger {request.node.name} does not exist!"}
