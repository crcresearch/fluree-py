from collections.abc import Generator
from http import HTTPStatus

import pytest
import respx
from httpx import Response
from respx import MockRouter

from fluree_py import FlureeClient
from fluree_py.http.endpoint import CreateReadyToCommitImpl


@pytest.fixture
def mocked_api(test_name: str) -> Generator[MockRouter, None, None]:
    with respx.mock(base_url="http://localhost:8090", assert_all_called=False) as respx_mock:
        create_route = respx_mock.post("/fluree/create", name="create")
        create_route.return_value = Response(
            HTTPStatus.CREATED,
            headers={"Content-Type": "application/json;charset=utf-8"},
            json={
                "commit": f"fluree:file://{test_name}/commit/bylyfvz5kexxf6l3tdzbobuz6eooxtgfxg3xqnp3pep7zfwxspkp.json",
                "ledger": test_name,
                "t": 1,
                "tx-id": "790b9747063d7878af67428ac92b37d2ff82971dee3ea533c053e44403a026de",
            },
        )

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
    create_route = mocked_api["create"]
    assert create_route.call_count == 1
    assert create_route.calls.last.request.url == "http://localhost:8090/fluree/create"
    assert create_route.calls.last.request.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_create_ledger_async(
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

    with_insert = fluree_client.with_ledger(test_name).create().with_context(context).with_insert(data)
    assert isinstance(with_insert, CreateReadyToCommitImpl)

    resp = await with_insert.acommit()

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
