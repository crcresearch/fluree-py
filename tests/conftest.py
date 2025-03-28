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
def fluree_url(request) -> Generator[str | None, None, None]:
    if not request.config.getoption("--use-fluree-server"):
        yield None
        return
    
    container = ServerContainer(port=8090, image="fluree/server")
    container.start()

    # Wait for the container to be ready
    wait_for_logs(container, "Starting Fluree server with profile")

    yield container._create_connection_url()

    (out, err) = container.get_logs()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))

    # Cleanup
    container.stop()


@pytest.fixture(scope="session")
def fluree_client(fluree_url) -> FlureeClient | None:
    if fluree_url is None:
        return None
    return FlureeClient(base_url=fluree_url)


@pytest.fixture(scope="session")
def dummy_client():
    return FlureeClient(base_url="http://localhost:8090")
