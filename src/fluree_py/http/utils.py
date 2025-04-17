import logging
from typing import Any

logger = logging.getLogger(__name__)


def resolve_base_class_reference(cls: type, mixin_name: str) -> type[Any]:
    # Traverse the MRO to find the first class that has the mixin
    for base in cls.__mro__:
        logger.debug("resolve_type", class_name=cls.__name__, checking=base.__name__)
        if base.__name__.endswith(mixin_name) and base is not mixin_class:
            logger.debug("resolved_type", base=base.__name__)
            return base
