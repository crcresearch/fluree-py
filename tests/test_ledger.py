from dataclasses import FrozenInstanceError

import pytest

from fluree_py import FlureeClient


def test_ledger_is_immutable(dummy_client: FlureeClient):
    ledger = dummy_client.with_ledger("test")
    with pytest.raises(FrozenInstanceError):
        ledger.name = "test2"
