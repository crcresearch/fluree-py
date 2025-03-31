from dataclasses import dataclass

from fluree_py.http.ledger import LedgerSelected
from fluree_py.http.protocol.ledger import SupportsLedgerOperations


@dataclass(frozen=True, kw_only=True)
class FlureeClient:
    base_url: str

    def with_ledger(self, ledger: str) -> SupportsLedgerOperations:
        return LedgerSelected(base_url=self.base_url, ledger=ledger)
