from typing import Generator

import pytest
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.generic import ServerContainer

from fluree_py import FlureeClient


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--use-fluree-server",
        action="store_true",
        default=False,
        help="Run tests against a real Fluree server container",
    )


@pytest.fixture(scope="session")
def fluree_url(request) -> Generator[str, None, None]:
    # Return dummy address if --use-fluree-server is not set
    if not request.config.getoption("--use-fluree-server"):
        yield "http://localhost:8090"
        return

    # Start a new Fluree server container
    container = ServerContainer(port=8090, image="fluree/server")
    container.start()

    # Wait for the container to be ready
    wait_for_logs(container, "Starting Fluree server with profile")

    # Return the container's connection URL
    yield container._create_connection_url()

    # Print the container's logs
    (out, err) = container.get_logs()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))

    # Cleanup
    container.stop()


@pytest.fixture(scope="session")
def fluree_client(fluree_url: str) -> FlureeClient:
    return FlureeClient(base_url=fluree_url)


@pytest.fixture
def cookbook_client(
    request: pytest.FixtureRequest, fluree_client: FlureeClient
) -> Generator[FlureeClient, None, None]:
    if not request.config.getoption("--use-fluree-server"):
        yield fluree_client
        return

    # Only setup the ledger if we're using a real Fluree server
    resp = (
        fluree_client.with_ledger(ledger=request.node.name)
        .create()
        .with_context({"ex": "http://example.org/", "schema": "http://schema.org/"})
        .with_insert(
            [
                {
                    "@id": "ex:freddy",
                    "@type": "ex:Yeti",
                    "schema:age": 4,
                    "schema:name": "Freddy",
                    "ex:verified": True,
                },
                {
                    "@id": "ex:letty",
                    "@type": "ex:Yeti",
                    "schema:age": 2,
                    "ex:nickname": "Letty",
                    "schema:name": "Leticia",
                    "schema:follows": [{"@id": "ex:freddy"}],
                },
                {
                    "@id": "ex:betty",
                    "@type": "ex:Yeti",
                    "schema:age": 82,
                    "schema:name": "Betty",
                    "schema:follows": [{"@id": "ex:freddy"}],
                },
                {
                    "@id": "ex:andrew",
                    "@type": "schema:Person",
                    "schema:age": 35,
                    "schema:name": "Andrew Johnson",
                    "schema:follows": [
                        {"@id": "ex:freddy"},
                        {"@id": "ex:letty"},
                        {"@id": "ex:betty"},
                    ],
                },
            ]
        )
        .commit()
    )

    assert resp.status_code == 201

    yield fluree_client
