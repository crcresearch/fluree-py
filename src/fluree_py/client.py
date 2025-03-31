from dataclasses import dataclass

from fluree_py.ledger.ledger import LedgerSelected
from fluree_py.ledger.protocol.ledger import SupportsLedgerOperations


@dataclass(frozen=True, kw_only=True)
class FlureeClient:
    """Client for interacting with Fluree databases."""
    base_url: str

    def with_ledger(self, ledger: str) -> SupportsLedgerOperations:
        """Select a ledger to operate on."""
        return LedgerSelected(base_url=self.base_url, ledger=ledger)
