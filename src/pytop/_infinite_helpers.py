"""Shared carrier/cardinality helpers for infinite-space modules.

These utilities are used by :mod:`pytop.infinite_spaces` and any future
infinite-space sub-modules.  Keeping them here allows cardinality inference
to be tested and maintained independently of the space class hierarchy.
"""

from __future__ import annotations

from typing import Any

STANDARD_COUNTABLE_CARRIERS: frozenset[str] = frozenset({
    "n", "naturals", "natural_numbers", "z", "integers", "q", "rationals"
})
STANDARD_UNCOUNTABLE_CARRIERS: frozenset[str] = frozenset({
    "r", "reals", "real_line", "irrationals"
})
VALID_CARDINALITY_TOKENS: frozenset[str] = frozenset({
    "finite", "countable", "countably_infinite", "at_most_countable",
    "uncountable", "aleph_0", "aleph_1", "continuum", "beth_1",
})
_ALL_STANDARD_CARRIERS: frozenset[str] = STANDARD_COUNTABLE_CARRIERS | STANDARD_UNCOUNTABLE_CARRIERS


def _carrier_token(carrier: Any) -> str:
    return str(carrier).strip().lower() if isinstance(carrier, str) else ""


def _has_standard_countable_subset(carrier: Any, metadata: dict[str, Any]) -> bool:
    """Return True if the carrier is known to admit a countable dense subset.

    This intentionally returns True for uncountable standard carriers like "r"/"reals"
    because the cofinite topology on an uncountable space is still separable —
    every infinite (countable) subset is dense in the cofinite topology.
    """
    token = _carrier_token(carrier)
    if token in _ALL_STANDARD_CARRIERS:
        return True
    return bool(metadata.get("has_countable_subset", False) or metadata.get("countable_dense_subset", False))


def _infer_size_tags(carrier: Any, metadata: dict[str, Any]) -> set[str]:
    token = _carrier_token(carrier)
    tags: set[str] = set()
    cardinality = str(metadata.get("cardinality", "")).strip().lower()
    countability = str(metadata.get("countability", "")).strip().lower()
    if (
        token in STANDARD_COUNTABLE_CARRIERS
        or cardinality in {"countable", "aleph_0", "finite", "at_most_countable", "countably_infinite"}
        or countability in {"countable", "countably_infinite", "finite"}
    ):
        tags.add("countable")
    if token in STANDARD_UNCOUNTABLE_CARRIERS or cardinality == "uncountable" or countability == "uncountable":
        tags.add("uncountable")
    return tags


def _is_countable_family_size(value: Any) -> bool:
    token = str(value).strip().lower()
    return token in {"aleph_0", "countable", "finite", "at_most_countable", "countably_infinite"}


__all__ = [
    "STANDARD_COUNTABLE_CARRIERS",
    "STANDARD_UNCOUNTABLE_CARRIERS",
    "VALID_CARDINALITY_TOKENS",
]
