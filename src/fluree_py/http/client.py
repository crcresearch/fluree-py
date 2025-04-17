from dataclasses import dataclass

from fluree_py.http.ledger import LedgerSelected, SupportsLedgerOperations
from fluree_py.logging import logger
from fluree_py.types.common import LedgerName


@dataclass(frozen=True, kw_only=True)
class FlureeClient:
    """Client for interacting with Fluree databases."""

    base_url: str

    def with_ledger(self, ledger: LedgerName) -> SupportsLedgerOperations:
        """Select a ledger to operate on."""
        logger.debug("selecting_ledger", base_url=self.base_url, ledger=ledger)
        return LedgerSelected(base_url=self.base_url, ledger=ledger)
