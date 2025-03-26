import pytest
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.generic import ServerContainer

from fluree_py import FlureeClient


@pytest.fixture(scope="session")
def fluree_url():
    """
    Fixture that starts a Fluree server container and returns its URL.
    The container will be stopped after all tests are completed.
    """
    container = ServerContainer(port=8090, image="fluree/server")
    container.start()

    # Wait for the container to be ready
    wait_for_logs(container, "Starting Fluree server with profile")

    yield container._create_connection_url()

    # Cleanup
    container.stop()


@pytest.fixture(scope="session")
def fluree_client(fluree_url):
    return FlureeClient(base_url=fluree_url)


@pytest.fixture(scope="session")
def dummy_client():
    return FlureeClient(base_url="http://localhost:8090")
