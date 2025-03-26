import json

from fluree_py import FlureeClient


def test_ledger_query(dummy_client: FlureeClient):
    request = (
        dummy_client.with_ledger("cookbook/base")
        .query()
        .with_context({"ex": "http://example.org/", "schema": "http://schema.org/"})
        .with_where({"@id": "?s", "schema:name": "?name"})
        .select({"?s": ["*"]})
        .get_request()
    )

    assert request.method == "POST"
    assert request.url == dummy_client.base_url + "/fluree/query"
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.content) == {
        "@context": {"ex": "http://example.org/", "schema": "http://schema.org/"},
        "from": "cookbook/base",
        "where": {"@id": "?s", "schema:name": "?name"},
        "select": {"?s": ["*"]},
    }
