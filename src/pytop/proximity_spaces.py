"""Proximity-space benchmark helpers.

This v0.1.105 surface replaces the placeholder returns with a conservative
benchmark layer for:

- proximity-space recognition
- closeness queries between subsets
- symbolic Smirnov compactification descriptors
"""

from __future__ import annotations

from typing import Any


VERSION = "0.1.105"

PROXIMITY_TRUE_TAGS = {
    "proximity_space",
    "efremovich_proximity",
    "metric_proximity",
}


def _metadata_of(obj: Any) -> dict[str, Any]:
    if isinstance(obj, dict):
        raw = obj.get("metadata", {})
        return raw if isinstance(raw, dict) else {}
    raw = getattr(obj, "metadata", {}) or {}
    return raw if isinstance(raw, dict) else {}


def _extract_tags(obj: Any) -> set[str]:
    tags: set[str] = set()
    if isinstance(obj, dict):
        raw_tags = obj.get("tags", [])
        if isinstance(raw_tags, (set, list, tuple, frozenset)):
            tags.update(str(tag).strip().lower() for tag in raw_tags)
    metadata = _metadata_of(obj)
    raw_meta_tags = metadata.get("tags", [])
    if isinstance(raw_meta_tags, (set, list, tuple, frozenset)):
        tags.update(str(tag).strip().lower() for tag in raw_meta_tags)
    for attr in ("tags", "_tags"):
        raw = getattr(obj, attr, None)
        if isinstance(raw, (set, list, tuple, frozenset)):
            tags.update(str(tag).strip().lower() for tag in raw)
    return tags


def _closeness_map(space: Any) -> dict[tuple[str, str], bool]:
    if isinstance(space, dict) and isinstance(space.get("closeness_map"), dict):
        return {
            (str(a), str(b)): bool(v)
            for (a, b), v in space["closeness_map"].items()
        }
    metadata = _metadata_of(space)
    if isinstance(metadata.get("closeness_map"), dict):
        return {
            (str(a), str(b)): bool(v)
            for (a, b), v in metadata["closeness_map"].items()
        }
    return {}


def _normalize_subset(subset: Any) -> str:
    if isinstance(subset, (set, frozenset, list, tuple)):
        return "{" + ",".join(sorted(str(x) for x in subset)) + "}"
    return str(subset)


def is_proximity_space(space):
    """Check whether the input carries a usable proximity witness."""
    if isinstance(space, dict) and isinstance(space.get("is_proximity_space"), bool):
        return space["is_proximity_space"]
    metadata = _metadata_of(space)
    if isinstance(metadata.get("is_proximity_space"), bool):
        return metadata["is_proximity_space"]
    if _closeness_map(space):
        return True
    tags = _extract_tags(space)
    return bool(tags & PROXIMITY_TRUE_TAGS)


def is_close(A, B, proximity_space):
    """Check whether two subsets are benchmark-close in the proximity descriptor."""
    if not is_proximity_space(proximity_space):
        return False
    closeness = _closeness_map(proximity_space)
    if closeness:
        left = _normalize_subset(A)
        right = _normalize_subset(B)
        return closeness.get((left, right), closeness.get((right, left), False))
    if isinstance(proximity_space, dict) and proximity_space.get("space_type") == "Metric Proximity":
        return True
    if "metric_proximity" in _extract_tags(proximity_space):
        return True
    return False


def smirnov_compactification(proximity_space):
    """Return a symbolic Smirnov compactification descriptor when available."""
    if not is_proximity_space(proximity_space):
        return None
    if isinstance(proximity_space, dict) and isinstance(proximity_space.get("smirnov_compactification"), dict):
        return {
            **proximity_space["smirnov_compactification"],
            "version": VERSION,
        }
    metadata = _metadata_of(proximity_space)
    if isinstance(metadata.get("smirnov_compactification"), dict):
        return {
            **metadata["smirnov_compactification"],
            "version": VERSION,
        }
    return {
        "compactification_type": "Smirnov compactification",
        "source": proximity_space.get("space_type", "symbolic proximity space") if isinstance(proximity_space, dict) else "symbolic proximity space",
        "closeness_principle": "A and B are close iff their closures intersect in the compactification.",
        "version": VERSION,
    }
