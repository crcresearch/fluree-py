import logging
from collections.abc import Iterable

import structlog
from structlog.stdlib import LoggerFactory
from structlog.types import BindableLogger, Processor

# Default structlog configuration for the fluree_py library
_DEFAULT_PROCESSORS: list[Processor] = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
]

_DEFAULT_WRAPPER_CLASS = structlog.stdlib.BoundLogger
_DEFAULT_LOGGER_FACTORY = structlog.stdlib.LoggerFactory()


def configure_logging(
    level: int = logging.INFO,
    processors: Iterable[Processor] | None = None,
    wrapper_class: type[BindableLogger] | None = None,
    logger_factory: type[LoggerFactory] | None = None,
    cache_logger_on_first_use: bool = True,
) -> None:
    """
    Configure structured logging for fluree_py.

    Args:
        level: Logging level for the standard library logger.
        processors: A list of structlog processors.
        wrapper_class: The structlog wrapper_class.
        logger_factory: The structlog logger_factory.
        cache_logger_on_first_use: Whether to cache the logger on first use.

    """
    logging.basicConfig(level=level)
    structlog.configure(
        processors=processors or _DEFAULT_PROCESSORS,
        wrapper_class=wrapper_class or _DEFAULT_WRAPPER_CLASS,
        logger_factory=logger_factory or _DEFAULT_LOGGER_FACTORY,
        cache_logger_on_first_use=cache_logger_on_first_use,
    )


# Apply default configuration
configure_logging()

# Export a library-wide logger
logger = structlog.get_logger("fluree_py")
