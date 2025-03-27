import pytest

from fluree_py.client import FlureeClient


@pytest.fixture(scope="session")
def client_with_cookbook(fluree_client: FlureeClient) -> FlureeClient:
    fluree_client.with_ledger(ledger="cookbook/base").create().with_context(
        {"ex": "http://example.org/", "schema": "http://schema.org/"}
    ).with_insert(
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
    ).commit()

    return fluree_client
