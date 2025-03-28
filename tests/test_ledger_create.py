import json
from typing import Generator

from httpx import Response
import pytest
from respx import MockRouter
import respx

from fluree_py import FlureeClient


@pytest.fixture
def leger_creation_data() -> tuple[dict, list[dict]]:
    return (
        {
            "ex": "http://example.org/",
            "schema": "http://schema.org/",
        },
        [
            {
                "@id": "ex:freddy",
                "@type": "ex:Yeti",
                "schema:age": 4,
                "schema:name": "Freddy",
                "ex:verified": True,
            }
        ],
    )


@pytest.fixture
def mocked_api(request) -> Generator[MockRouter, None, None]:
    with respx.mock(
        base_url="http://localhost:8090", assert_all_called=False
    ) as respx_mock:
        create_route = respx_mock.post("/fluree/create", name="create")
        create_route.return_value = Response(
            201,
            headers={"Content-Type": "application/json;charset=utf-8"},
            json={
                "commit": f"fluree:file://{request.node.name}/commit/bylyfvz5kexxf6l3tdzbobuz6eooxtgfxg3xqnp3pep7zfwxspkp.json",
                "ledger": request.node.name,
                "t": 1,
                "tx-id": "790b9747063d7878af67428ac92b37d2ff82971dee3ea533c053e44403a026de",
            },
        )

        yield respx_mock


@pytest.fixture
def fluree_client_create(
    request, fluree_client: FlureeClient
) -> Generator[FlureeClient, None, None]:
    if request.config.getoption("--use-fluree-server"):
        yield fluree_client
        return

    # If we're not using a real Fluree server, mock the API
    mocked_api: MockRouter = request.getfixturevalue("mocked_api")
    print(mocked_api.routes)
    yield fluree_client

    # Assert that the mocked API was called
    create_route = mocked_api["create"]
    assert create_route.call_count == 1
    assert create_route.calls.last.request.url == "http://localhost:8090/fluree/create"
    assert create_route.calls.last.request.headers["Content-Type"] == "application/json"


def test_create_ledger(
    request,
    fluree_client_create: FlureeClient,
    leger_creation_data: tuple[dict, list[dict]],
):
    resp = (
        fluree_client_create.with_ledger(request.node.name)
        .create()
        .with_context(leger_creation_data[0])
        .with_insert(leger_creation_data[1])
        .commit()
    )

    assert resp.status_code == 201
    assert resp.headers["Content-Type"] == "application/json;charset=utf-8"

    resp_json = resp.json()
    assert "ledger" in resp_json
    assert resp_json["ledger"] == request.node.name

    assert "t" in resp_json
    assert resp_json["t"] == 1

    assert "commit" in resp_json
    assert resp_json["commit"].startswith(f"fluree:file://{request.node.name}/commit/")

    assert "tx-id" in resp_json
