import logging
from collections.abc import Generator

import pytest
from testcontainers.core.waiting_utils import wait_for_logs  # type: ignore
from testcontainers.generic import ServerContainer  # type: ignore

from fluree_py import FlureeClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--use-fluree-server",
        action="store_true",
        default=False,
        help="Run tests against a real Fluree server container",
    )


@pytest.fixture(scope="session")
def fluree_url(request: pytest.FixtureRequest) -> Generator[str, None, None]:
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
    yield container._create_connection_url()  # type: ignore # noqa: SLF001

    # Print the container's logs
    (out, err) = container.get_logs()
    logger.info("Container logs:\n%s", out.decode("utf-8"))
    if err:
        logger.error("Container error logs:\n%s", err.decode("utf-8"))

    # Cleanup
    container.stop()


@pytest.fixture(scope="session")
def fluree_client(fluree_url: str) -> FlureeClient:
    return FlureeClient(base_url=fluree_url)


@pytest.fixture
def using_fluree_server(request: pytest.FixtureRequest) -> bool:
    is_using_fluree_server = request.config.getoption("--use-fluree-server")
    assert isinstance(is_using_fluree_server, bool)
    return is_using_fluree_server


@pytest.fixture
def test_name(request: pytest.FixtureRequest) -> str:
    node_name: str = request.node.name  # type: ignore
    assert isinstance(node_name, str)
    return node_name


@pytest.fixture
def cookbook_client(
    using_fluree_server: bool,
    test_name: str,
    fluree_client: FlureeClient,
) -> Generator[FlureeClient, None, None]:
    if not using_fluree_server:
        yield fluree_client
        return

    # Only setup the ledger if we're using a real Fluree server
    resp = (
        fluree_client.with_ledger(ledger=test_name)
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
            ],
        )
        .commit()
    )

    assert resp.status_code == 201

    yield fluree_client
