import json

from fluree_py import FlureeClient


def test_create_ledger(dummy_client: FlureeClient):
    request = (
        dummy_client.with_ledger("cookbook/base")
        .create()
        .with_context(
            {
                "ex": "http://example.org/",
                "schema": "http://schema.org/",
            }
        )
        .with_insert(
            [
                {
                    "@id": "ex:freddy",
                    "@type": "ex:Yeti",
                    "schema:age": 4,
                    "schema:name": "Freddy",
                    "ex:verified": True,
                }
            ]
        )
        .request()
    )

    assert request.method == "POST"
    assert request.url == dummy_client.base_url + "/fluree/create"
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.content) == {
        "@context": {"ex": "http://example.org/", "schema": "http://schema.org/"},
        "ledger": "cookbook/base",
        "insert": [
            {
                "@id": "ex:freddy",
                "@type": "ex:Yeti",
                "schema:age": 4,
                "schema:name": "Freddy",
                "ex:verified": True,
            }
        ],
    }
