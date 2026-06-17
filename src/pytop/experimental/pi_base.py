"""Deductive topological-property inference backed by the pi-Base dataset.

This module turns the curated pi-Base database (243 properties, 902 implication
theorems, 222 spaces with 2099 asserted traits) into a real **deductive engine**:
given some known traits of a space it computes their logical closure under the
implication theorems (forward chaining *and* contrapositive), and it detects
contradictory trait sets.

This complements pytop's hand-written, tag-based theorem inference with a large,
referenced implication graph. The data is loaded from a compact JSON blob
(stdlib ``json`` only -- no third-party runtime dependency); regenerate it with
``pytop._internal.pi_base_compile``.

Attribution
-----------
The underlying facts come from pi-Base (https://topology.pi-base.org), Copyright
2014-2025 Steven Clontz and James Dabbs, licensed CC BY 4.0. See
:data:`PI_BASE_ATTRIBUTION`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

_DATA_PATH = Path(__file__).with_name("_pi_base_data.json")


class InconsistentTraitsError(ValueError):
    """Raised when a set of traits is contradictory under the pi-Base theorems."""


class UnknownPropertyError(KeyError):
    """Raised when a property name or uid cannot be resolved."""


@lru_cache(maxsize=1)
def _load() -> dict[str, Any]:
    return json.loads(_DATA_PATH.read_text(encoding="utf-8"))


PI_BASE_ATTRIBUTION: str = _load()["_attribution"]


def dataset_counts() -> dict[str, int]:
    """Return the number of properties, theorems, spaces and traits loaded."""

    return dict(_load()["_counts"])


def properties() -> dict[str, dict[str, Any]]:
    """Return the property registry keyed by uid (``{uid: {name, aliases}}``)."""

    return _load()["properties"]


def theorems() -> list[dict[str, Any]]:
    """Return the implication theorems (``[{uid, if: {...}, then: {...}}, ...]``)."""

    return _load()["theorems"]


def spaces() -> dict[str, dict[str, Any]]:
    """Return the space registry keyed by uid."""

    return _load()["spaces"]


@lru_cache(maxsize=1)
def _name_index() -> dict[str, str]:
    index: dict[str, str] = {}
    for uid, record in properties().items():
        for label in [uid, record["name"], *record["aliases"]]:
            index[_normalize(label)] = uid
    return index


def _normalize(label: str) -> str:
    return label.replace("$", "").replace("\\", "").strip().lower()


def property_uid(name_or_uid: str) -> str:
    """Resolve a property name, alias, or uid to its canonical uid."""

    key = _normalize(name_or_uid)
    index = _name_index()
    if key in index:
        return index[key]
    raise UnknownPropertyError(f"Unknown pi-Base property: {name_or_uid!r}")


def property_name(uid: str) -> str:
    """Return the display name of a property uid."""

    try:
        return properties()[uid]["name"]
    except KeyError as exc:
        raise UnknownPropertyError(f"Unknown pi-Base property uid: {uid!r}") from exc


@lru_cache(maxsize=1)
def _space_traits() -> dict[str, dict[str, bool]]:
    result: dict[str, dict[str, bool]] = {}
    for space_uid, property_uid_, value in _load()["traits"]:
        result.setdefault(space_uid, {})[property_uid_] = value
    return result


def asserted_traits(space_uid: str) -> dict[str, bool]:
    """Return the explicitly asserted traits of a space (``{property_uid: bool}``)."""

    return dict(_space_traits().get(space_uid, {}))


def _evaluate(formula: dict[str, Any], state: dict[str, bool]) -> bool | None:
    """Evaluate a property formula against ``state``.

    Returns ``True`` / ``False`` if determined, or ``None`` if the truth value
    cannot yet be decided from the known traits.
    """

    if "and" in formula:
        values = [_evaluate(child, state) for child in formula["and"]]
        if False in values:
            return False
        return None if None in values else True
    if "or" in formula:
        values = [_evaluate(child, state) for child in formula["or"]]
        if True in values:
            return True
        return None if None in values else False
    if "not" in formula:
        inner = _evaluate(formula["not"], state)
        return None if inner is None else not inner
    # atom map: a conjunction of atoms
    result: bool | None = True
    for prop, required in formula.items():
        current = state.get(prop)
        if current is None:
            result = None
        elif current != required:
            return False
    return result


def _atoms(formula: dict[str, Any]) -> list[tuple[str, bool]] | None:
    """Flatten a pure conjunction of atoms to a list, or None if it is not one."""

    if "and" in formula:
        collected: list[tuple[str, bool]] = []
        for child in formula["and"]:
            child_atoms = _atoms(child)
            if child_atoms is None:
                return None
            collected.extend(child_atoms)
        return collected
    if "or" in formula or "not" in formula:
        return None
    return list(formula.items())


def deduce(known: dict[str, bool]) -> dict[str, bool]:
    """Return the deductive closure of ``known`` under the pi-Base theorems.

    Applies each implication ``if FORMULA then FORMULA`` by forward chaining
    (asserting a conjunctive conclusion when the hypothesis holds), and applies
    contrapositive reasoning for implications between conjunctions of atoms.
    Raises :class:`InconsistentTraitsError` if a property is forced both ways.
    """

    state: dict[str, bool] = dict(known)
    all_theorems = theorems()

    def assign(prop: str, value: bool) -> bool:
        if prop in state:
            if state[prop] != value:
                raise InconsistentTraitsError(
                    f"Property {prop} forced to both {state[prop]} and {value}."
                )
            return False
        state[prop] = value
        return True

    def assert_conclusion(formula: dict[str, Any]) -> bool:
        # Only conjunctions of atoms (possibly negated singletons) are assertable.
        if "or" in formula:
            return False
        if "not" in formula:
            inner = formula["not"]
            inner_atoms = _atoms(inner)
            if inner_atoms is not None and len(inner_atoms) == 1:
                prop, value = inner_atoms[0]
                return assign(prop, not value)
            return False
        atoms = _atoms(formula)
        if atoms is None:
            return False
        changed_here = False
        for prop, value in atoms:
            changed_here |= assign(prop, value)
        return changed_here

    changed = True
    while changed:
        changed = False
        for theorem in all_theorems:
            hypothesis = theorem["if"]
            conclusion = theorem["then"]

            if _evaluate(hypothesis, state) is True:
                changed |= assert_conclusion(conclusion)

            # Contrapositive for atom-conjunction -> single-atom implications.
            conclusion_atoms = _atoms(conclusion)
            hypothesis_atoms = _atoms(hypothesis)
            if (
                conclusion_atoms is not None
                and len(conclusion_atoms) == 1
                and hypothesis_atoms is not None
            ):
                concl_prop, concl_value = conclusion_atoms[0]
                if state.get(concl_prop) == (not concl_value):
                    unsatisfied = [
                        (p, v) for p, v in hypothesis_atoms if state.get(p) != v
                    ]
                    if len(unsatisfied) == 1 and unsatisfied[0][0] not in state:
                        prop, value = unsatisfied[0]
                        changed |= assign(prop, not value)
    return state


def is_consistent(known: dict[str, bool]) -> bool:
    """Return whether ``known`` is consistent under the pi-Base theorems."""

    try:
        deduce(known)
    except InconsistentTraitsError:
        return False
    return True


def consequences(name_or_uid: str, value: bool = True) -> dict[str, bool]:
    """Return the closure implied by a single trait, keyed by property uid."""

    return deduce({property_uid(name_or_uid): value})


def deduced_space_traits(space_uid: str) -> dict[str, bool]:
    """Return the deductive closure of a space's asserted traits."""

    return deduce(asserted_traits(space_uid))


@dataclass(frozen=True)
class TraitConflict:
    """A disagreement between an external trait set and pi-Base deductions."""

    property_uid: str
    expected: bool
    deduced: bool


def compare_traits(known: dict[str, bool], claims: dict[str, bool]) -> tuple[TraitConflict, ...]:
    """Deduce from ``known`` and report where ``claims`` disagree with the closure.

    Useful for cross-validating an external library's property judgements against
    pi-Base: ``known`` seeds the deduction, ``claims`` are the values to check.
    """

    closure = deduce(known)
    conflicts = []
    for prop, claimed in claims.items():
        if prop in closure and closure[prop] != claimed:
            conflicts.append(TraitConflict(prop, claimed, closure[prop]))
    return tuple(conflicts)


__all__ = [
    "PI_BASE_ATTRIBUTION",
    "InconsistentTraitsError",
    "UnknownPropertyError",
    "TraitConflict",
    "dataset_counts",
    "properties",
    "theorems",
    "spaces",
    "property_uid",
    "property_name",
    "asserted_traits",
    "deduce",
    "is_consistent",
    "consequences",
    "deduced_space_traits",
    "compare_traits",
]
