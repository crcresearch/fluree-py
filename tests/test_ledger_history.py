from typing import Generator

import pytest
import respx
from httpx import Response
from pytest import FixtureRequest
from respx import MockRouter

from fluree_py import FlureeClient


@pytest.fixture
def mocked_api() -> Generator[MockRouter, None, None]:
    with respx.mock(
        base_url="http://localhost:8090", assert_all_called=False
    ) as respx_mock:
        history_route = respx_mock.post("/fluree/history", name="history")
        history_route.return_value = Response(
            200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            json=[
                {
                    "f:assert": [
                        {"@id": "ex:andrew", "schema:name": "Andrew Johnson"},
                        {"@id": "ex:betty", "schema:name": "Betty"},
                        {"@id": "ex:freddy", "schema:name": "Freddy"},
                        {"@id": "ex:letty", "schema:name": "Leticia"},
                    ],
                    "f:retract": [],
                    "f:t": 1,
                }
            ],
        )

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
    create_route = mocked_api["history"]
    assert create_route.call_count == 1
    assert create_route.calls.last.request.url == "http://localhost:8090/fluree/history"
    assert create_route.calls.last.request.headers["Content-Type"] == "application/json"


def test_ledger_history(test_name: str, cookbook_client: FlureeClient):
    context = {
        "ex": "http://example.org/",
        "schema": "http://schema.org/",
        "f": "https://ns.flur.ee/ledger#",
    }

    resp = (
        cookbook_client.with_ledger(test_name)
        .history()
        .with_context(context)
        .with_history((None, "schema:name"))
        .with_t({"from": 1})
        .commit()
    )

    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json;charset=utf-8"

    assert resp.json() == [
        {
            "f:assert": [
                {"@id": "ex:andrew", "schema:name": "Andrew Johnson"},
                {"@id": "ex:betty", "schema:name": "Betty"},
                {"@id": "ex:freddy", "schema:name": "Freddy"},
                {"@id": "ex:letty", "schema:name": "Leticia"},
            ],
            "f:retract": [],
            "f:t": 1,
        }
    ]
