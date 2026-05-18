"""Shared helpers for property-analysis modules (separation, compactness, connectedness).

These four small utilities are used identically across all three property modules.
They are kept here to avoid triple-maintenance.
"""

from __future__ import annotations

from typing import Any


def _representation_of(space: Any) -> str:
    """Return the lowercase representation key from space metadata."""
    metadata = getattr(space, "metadata", {}) or {}
    return str(metadata.get("representation", "symbolic_general")).strip().lower()


def _extract_tags(space: Any) -> set[str]:
    """Return a normalised set of lowercase tags from a space object."""
    tags: set[str] = set()
    raw_tags: set[Any] = getattr(space, "tags", set())
    tags.update(str(tag).strip().lower() for tag in raw_tags if str(tag).strip())
    metadata = getattr(space, "metadata", {}) or {}
    for tag in metadata.get("tags", []):
        text = str(tag).strip().lower()
        if text:
            tags.add(text)
    return tags


def _matches_any(tags: set[str], candidates: list[str]) -> bool:
    """Return True iff at least one candidate string is in *tags*."""
    return any(candidate in tags for candidate in candidates)


def _mode_from_support(support: str) -> str:
    """Map a CapabilityRegistry support level to a Result mode string."""
    return {
        "exact": "exact",
        "theorem": "theorem",
        "symbolic": "symbolic",
        "mixed": "mixed",
        "none": "symbolic",
    }.get(support, "symbolic")


__all__ = [
    "_representation_of",
    "_extract_tags",
    "_matches_any",
    "_mode_from_support",
]
