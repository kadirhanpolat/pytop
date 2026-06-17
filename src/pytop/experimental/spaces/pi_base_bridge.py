"""Bridge: expose pi-Base atlas spaces as protocol :class:`Space` objects.

This connects pytop's two strongest point-set pieces — the curated pi-Base atlas
(222 famous spaces with deduced trait matrices) and the reasoning engine — by
wrapping each pi-Base space as a :class:`Space` whose property certificates come
from pi-Base's **deductive closure** of that space's traits.

So the engine's predicates and :func:`~pytop.experimental.spaces.reasoning.derive`
work directly on famous spaces (the long line, the Cantor set, Stone–Čech
remainders, …), and those spaces can be fed into the construction wrappers
(``ProductSpace([pi_base_space("Cantor set"), …])``) for compositional reasoning.

The wrapper is *opaque*: it does not model the underlying point set (membership is
not decidable here), it answers property questions from pi-Base. Cardinality is
reported as non-finite so predicates take the certificate path.
"""

from __future__ import annotations

from functools import cache
from typing import Any

from ..pi_base import deduced_space_traits, property_uid
from ..pi_base_atlas import space_name, space_uid
from .core import CarrierKind, Space, Verdict
from .reasoning import _PI_NAME


@cache
def _closure(uid: str) -> dict[str, bool]:
    return deduced_space_traits(uid)


class PiBaseSpace(Space):
    """A pi-Base atlas space presented through the computable-space protocol.

    Property certificates are looked up from pi-Base's deductive closure of the
    space's asserted traits.
    """

    def __init__(self, uid: str) -> None:
        self._uid = uid
        self.name = space_name(uid)
        self.carrier_kind = CarrierKind.UNCOUNTABLE  # opaque; always uses certificates

    def contains(self, point: Any) -> bool:  # pragma: no cover - opaque point set
        raise NotImplementedError("pi-Base spaces are opaque; membership is not modelled.")

    def certificate(self, prop: str) -> Verdict | None:
        pi_name = _PI_NAME.get(prop)
        if pi_name is None:
            return None
        try:
            uid = property_uid(pi_name)
        except KeyError:
            return None
        traits = _closure(self._uid)
        if uid not in traits:
            return None
        value = traits[uid]
        reason = f"pi-Base: {self.name} is {'' if value else 'not '}{prop}"
        return Verdict.true(reason=reason) if value else Verdict.false(reason=reason)


def pi_base_space(name_or_uid: str) -> PiBaseSpace:
    """Build a :class:`PiBaseSpace` from a pi-Base space name, alias, or uid."""

    return PiBaseSpace(space_uid(name_or_uid))


def analyze_pi_base_space(name_or_uid: str) -> dict[str, Verdict]:
    """Return every reasoning-engine property verdict for a famous pi-Base space."""

    from .reasoning import PROPERTY_KEYS, derive

    space = pi_base_space(name_or_uid)
    return {prop: derive(space, prop).verdict for prop in PROPERTY_KEYS}


__all__ = [
    "PiBaseSpace",
    "pi_base_space",
    "analyze_pi_base_space",
]
