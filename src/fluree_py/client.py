from dataclasses import dataclass

from fluree_py.ledger.ledger import LedgerSelected


@dataclass(frozen=True, kw_only=True)
class FlureeClient:
    base_url: str

    def with_ledger(self, ledger: str) -> "LedgerSelected":
        return LedgerSelected(base_url=self.base_url, ledger=ledger)
