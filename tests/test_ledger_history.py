import json

from fluree_py import FlureeClient


def test_ledger_history(dummy_client: FlureeClient):
    request = (
        dummy_client.with_ledger("cookbook/base")
        .history()
        .with_context({"schema": "http://schema.org/"})
        .with_history([None, "schema:name"])
        .with_t({"from": 1})
        .request()
    )

    assert request.method == "POST"
    assert request.url == dummy_client.base_url + "/fluree/history"
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.content) == {
        "@context": {"schema": "http://schema.org/"},
        "from": "cookbook/base",
        "history": [None, "schema:name"],
        "t": {"from": 1},
    }
