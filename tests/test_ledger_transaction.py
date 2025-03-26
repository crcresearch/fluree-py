import json


from fluree_py import FlureeClient


def test_ledger_transaction(dummy_client: FlureeClient):
    request = (
        dummy_client.with_ledger("cookbook/base")
        .transaction()
        .with_context({"schema": "http://schema.org/"})
        .with_where({"@id": "?s", "schema:description": "We ❤️ All Blood"})
        .with_delete({"@id": "?s", "schema:description": "We ❤️ All Blood"})
        .with_insert(
            {
                "@id": "?s",
                "schema:description": ["We ❤️ Human Blood", "We ❤️ Animal Blood"],
            }
        )
        .get_request()
    )

    assert request.method == "POST"
    assert request.url == dummy_client.base_url + "/fluree/transact"
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.content) == {
        "@context": {"schema": "http://schema.org/"},
        "ledger": "cookbook/base",
        "where": {"@id": "?s", "schema:description": "We ❤️ All Blood"},
        "delete": {"@id": "?s", "schema:description": "We ❤️ All Blood"},
        "insert": {
            "@id": "?s",
            "schema:description": ["We ❤️ Human Blood", "We ❤️ Animal Blood"],
        },
    }


def test_ledger_transaction_no_context(dummy_client: FlureeClient):
    request = (
        dummy_client.with_ledger("cookbook/base")
        .transaction()
        .with_where({"@id": "?s", "schema:description": "We ❤️ All Blood"})
        .with_delete({"@id": "?s", "schema:description": "We ❤️ All Blood"})
        .with_insert(
            {
                "@id": "?s",
                "schema:description": ["We ❤️ Human Blood", "We ❤️ Animal Blood"],
            }
        )
        .get_request()
    )

    assert request.method == "POST"
    assert request.url == dummy_client.base_url + "/fluree/transact"
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.content) == {
        "ledger": "cookbook/base",
        "where": {"@id": "?s", "schema:description": "We ❤️ All Blood"},
        "delete": {"@id": "?s", "schema:description": "We ❤️ All Blood"},
        "insert": {
            "@id": "?s",
            "schema:description": ["We ❤️ Human Blood", "We ❤️ Animal Blood"],
        },
    }
