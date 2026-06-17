"""Atlas and counterexample search over the pi-Base space database.

Built on :mod:`pytop.experimental.pi_base`, this module exposes the 222 pi-Base
spaces as a searchable atlas: look a space up by name, read its full deduced
property matrix, search for spaces satisfying property constraints, and -- the
signature pi-Base operation -- **find counterexamples** ("a space that is
compact but not Hausdorff").

Each space's property matrix is the deductive closure of its asserted traits
under the implication theorems, so searches see derived properties, not only the
handful explicitly recorded.

Attribution: see :data:`pytop.experimental.pi_base.PI_BASE_ATTRIBUTION`.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache
from typing import Any

from . import pi_base


class UnknownSpaceError(KeyError):
    """Raised when a space name or uid cannot be resolved."""


@lru_cache(maxsize=1)
def _space_name_index() -> dict[str, str]:
    index: dict[str, str] = {}
    for uid, record in pi_base.spaces().items():
        labels = [uid, record["name"], *record.get("aliases", [])]
        for label in labels:
            index[pi_base._normalize(label)] = uid
    return index


def space_uid(name_or_uid: str) -> str:
    """Resolve a space name, alias, or uid to its canonical uid."""

    key = pi_base._normalize(name_or_uid)
    index = _space_name_index()
    if key in index:
        return index[key]
    raise UnknownSpaceError(f"Unknown pi-Base space: {name_or_uid!r}")


def space_name(uid: str) -> str:
    try:
        return pi_base.spaces()[uid]["name"]
    except KeyError as exc:
        raise UnknownSpaceError(f"Unknown pi-Base space uid: {uid!r}") from exc


def space_record(uid: str) -> dict[str, Any]:
    try:
        return dict(pi_base.spaces()[uid])
    except KeyError as exc:
        raise UnknownSpaceError(f"Unknown pi-Base space uid: {uid!r}") from exc


@lru_cache(maxsize=1)
def _all_closures() -> dict[str, dict[str, bool]]:
    """Deductive closure of every space's asserted traits, cached."""

    return {uid: pi_base.deduced_space_traits(uid) for uid in pi_base.spaces()}


def property_matrix(space_uid_: str, *, names: bool = False) -> dict[str, bool]:
    """Return the full deduced property matrix of a space (``{property: bool}``).

    With ``names=True`` the keys are human-readable property names instead of
    uids.
    """

    if space_uid_ not in pi_base.spaces():
        raise UnknownSpaceError(f"Unknown pi-Base space uid: {space_uid_!r}")
    closure = _all_closures()[space_uid_]
    if not names:
        return dict(closure)
    return {pi_base.property_name(p): v for p, v in closure.items()}


def _resolve_constraints(constraints: dict[str, bool]) -> dict[str, bool]:
    return {pi_base.property_uid(name): value for name, value in constraints.items()}


def search_spaces(constraints: dict[str, bool]) -> tuple[str, ...]:
    """Return uids of spaces whose deduced matrix satisfies every constraint.

    ``constraints`` maps property names/uids to required boolean values.
    """

    resolved = _resolve_constraints(constraints)
    matches = []
    for uid, closure in _all_closures().items():
        if all(closure.get(prop) == value for prop, value in resolved.items()):
            matches.append(uid)
    return tuple(sorted(matches))


def find_counterexamples(
    has: Iterable[str] = (),
    lacks: Iterable[str] = (),
) -> tuple[str, ...]:
    """Find spaces that *have* every property in ``has`` and *lack* every one in ``lacks``.

    This is the classic counterexample query, e.g.
    ``find_counterexamples(has=["Compact"], lacks=["Hausdorff"])``.
    """

    constraints = {name: True for name in has}
    constraints.update({name: False for name in lacks})
    return search_spaces(constraints)


@lru_cache(maxsize=1)
def steen_seebach_index() -> dict[int, str]:
    """Map *Counterexamples in Topology* numbers to pi-Base space uids."""

    index: dict[int, str] = {}
    for uid, record in pi_base.spaces().items():
        ce_id = record.get("counterexamples_id")
        if ce_id is not None:
            index[int(ce_id)] = uid
    return index


__all__ = [
    "UnknownSpaceError",
    "space_uid",
    "space_name",
    "space_record",
    "property_matrix",
    "search_spaces",
    "find_counterexamples",
    "steen_seebach_index",
]
