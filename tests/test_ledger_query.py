from typing import Generator

import pytest
import respx
from httpx import Request, Response
from pytest import FixtureRequest
from respx import MockRouter

from fluree_py import FlureeClient


def query_side_effect(request: Request):
    return Response(
        200,
        headers={"Content-Type": "application/json;charset=utf-8"},
        json=[
            {
                "@type": "schema:Person",
                "schema:age": 35,
                "schema:follows": [
                    {"@id": "ex:betty"},
                    {"@id": "ex:freddy"},
                    {"@id": "ex:letty"},
                ],
                "schema:name": "Andrew Johnson",
                "@id": "ex:andrew",
            },
            {
                "@type": "ex:Yeti",
                "schema:age": 82,
                "schema:follows": {"@id": "ex:freddy"},
                "schema:name": "Betty",
                "@id": "ex:betty",
            },
            {
                "@type": "ex:Yeti",
                "schema:age": 4,
                "schema:name": "Freddy",
                "ex:verified": True,
                "@id": "ex:freddy",
            },
            {
                "@type": "ex:Yeti",
                "schema:age": 2,
                "schema:follows": {"@id": "ex:freddy"},
                "schema:name": "Leticia",
                "ex:nickname": "Letty",
                "@id": "ex:letty",
            },
        ],
    )


@pytest.fixture
def mocked_api() -> Generator[MockRouter, None, None]:
    with respx.mock(
        base_url="http://localhost:8090", assert_all_called=False
    ) as respx_mock:
        query_route = respx_mock.post("/fluree/query", name="query")
        query_route.side_effect = query_side_effect

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
    create_route = mocked_api["query"]
    assert create_route.call_count == 1
    assert create_route.calls.last.request.url == "http://localhost:8090/fluree/query"
    assert create_route.calls.last.request.headers["Content-Type"] == "application/json"


# https://developers.flur.ee/docs/reference/cookbook/#-wildcard
def test_ledger_query_wildcard_example(
    request: FixtureRequest, cookbook_client: FlureeClient
):
    resp = (
        cookbook_client.with_ledger(request.node.name)
        .query()
        .with_context({"ex": "http://example.org/", "schema": "http://schema.org/"})
        .with_where({"@id": "?s", "schema:name": "?name"})
        .with_select({"?s": ["*"]})
        .commit()
    )

    print(resp.json())
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json;charset=utf-8"

    assert resp.json() == [
        {
            "@type": "schema:Person",
            "schema:age": 35,
            "schema:follows": [
                {"@id": "ex:betty"},
                {"@id": "ex:freddy"},
                {"@id": "ex:letty"},
            ],
            "schema:name": "Andrew Johnson",
            "@id": "ex:andrew",
        },
        {
            "@type": "ex:Yeti",
            "schema:age": 82,
            "schema:follows": {"@id": "ex:freddy"},
            "schema:name": "Betty",
            "@id": "ex:betty",
        },
        {
            "@type": "ex:Yeti",
            "schema:age": 4,
            "schema:name": "Freddy",
            "ex:verified": True,
            "@id": "ex:freddy",
        },
        {
            "@type": "ex:Yeti",
            "schema:age": 2,
            "schema:follows": {"@id": "ex:freddy"},
            "schema:name": "Leticia",
            "ex:nickname": "Letty",
            "@id": "ex:letty",
        },
    ]
