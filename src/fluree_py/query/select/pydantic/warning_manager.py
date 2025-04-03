"""Warning management for the FlureeQL select query builder."""

import warnings
from dataclasses import dataclass, field


@dataclass
class WarningManager:
    """
    Manages warnings for the Pydantic model processing.

    Example:
        >>> manager = WarningManager()
        >>> manager.add_warning(ListOrderWarning, "Field 'items' is a list")
        >>> manager.emit_warnings()

    """

    warnings_list: list[tuple[type[Warning], str]] = field(default_factory=list)

    def add_warning(self, warning_type: type[Warning], message: str) -> None:
        """Add a warning to the list."""
        self.warnings_list.append((warning_type, message))

    def emit_warnings(self) -> None:
        """Emit all collected warnings."""
        for warning_type, message in self.warnings_list:
            warnings.warn(message, warning_type)
