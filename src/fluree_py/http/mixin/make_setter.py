from dataclasses import is_dataclass, replace
from types import new_class
from typing import Any, Protocol, TypeVar, cast, runtime_checkable


# ---------------------------------------------------------------------------
# Helper: minimal Protocol demanding that `self.<attr>` exists
# ---------------------------------------------------------------------------
def _attr_protocol(attr: str) -> type:
    """Return a `Protocol` subclass requiring `self.<attr>`."""
    return runtime_checkable(
        new_class(
            f"_Has_{attr}",
            (Protocol,),
            exec_body=lambda ns: ns.update({attr: None}),  # attribute marker
        )
    )


# ---------------------------------------------------------------------------
# Generic factory - now USES the protocol at run-time AND in annotations
# ---------------------------------------------------------------------------
SelfT = TypeVar("SelfT")  # builder *before* the call
NextT = TypeVar("NextT")  # builder returned by the call


def make_setter(
    *,
    method_name: str,
    field: str,
    next_state: type | None = None,
    protocol: type | None = None,
) -> type:
    """
    Build a mixin that works on *frozen* dataclasses:

      mixin.<method_name>(value)

    ① replaces `self._payload`   with `dataclasses.replace(...)`
    ② returns `self` *or* an instance of `next_state`.

    Parameters
    ----------
    method_name : str
        Name of the fluent setter (e.g. ``"with_context"``).
    field : str
        Field inside the dataclass to update.
    next_state : type | None
        Builder class to transition to. Omit to stay in the same state.
    protocol : type | None
        Structural contract `self` must satisfy.  If ``None`` a minimal
        one is generated on‑the‑fly that only asserts the existence of
        ``self._payload``.

    """
    Proto = protocol or _attr_protocol("_payload")

    # -- craft the method body ------------------------------------------------
    # Annotate `self` with the structural protocol (`Proto`) so that mypy /
    # Pyright know it has at least the required attribute(s).
    def _setter(self: Proto, value: Any) -> SelfT | NextT:  # type: ignore[name-defined]
        # 1⃣  Confirm at run‑time that the object really conforms
        if not isinstance(self, Proto):  # runtime structural check
            raise TypeError(f"{type(self).__name__} does not satisfy required protocol")

        payload = self._payload

        # 2⃣  Only dataclasses are supported
        if not is_dataclass(payload):
            raise TypeError(f"_payload must be a dataclass, got {type(payload)!r}")

        # 3⃣  Build *new* payload (safe for frozen=True)
        new_payload = replace(payload, **{field: value})
        self._payload = new_payload

        # 4⃣  Decide what to return
        if next_state is None:
            return cast("SelfT", self)  # stay put

        # If next_state expects extra args, forward `self` after payload
        try:
            return cast("NextT", next_state(new_payload))
        except TypeError:
            return cast("NextT", next_state(new_payload, self))

    _setter.__name__ = method_name

    # -- generate the mixin class --------------------------------------------
    return new_class(
        f"Mixin_{method_name}",
        (),  # no base classes
        exec_body=lambda ns: ns.update({method_name: _setter}),
    )
