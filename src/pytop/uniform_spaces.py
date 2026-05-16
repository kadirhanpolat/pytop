"""Uniform-space benchmark helpers.

This v0.1.104 surface replaces the placeholder values with a conservative
boolean API driven by explicit benchmark descriptors, tags, and metadata.
It does not attempt a full symbolic uniformity engine, but it now supports
honest positive/negative checks for the main roadmap corridor:

- uniform-space recognition
- entourage extraction
- uniform continuity
- Cauchy-filter recognition
- uniform completeness
"""

from __future__ import annotations

from typing import Any

VERSION = "0.1.104"

UNIFORM_TRUE_TAGS = {
    "uniform_space",
    "metric_uniformity",
    "discrete_uniformity",
    "metric",
    "metrizable",
    "complete_metric",
}
UNIFORM_COMPLETE_TRUE_TAGS = {
    "complete_metric",
    "discrete_uniformity",
    "finite_uniform_space",
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


def _explicit_bool(obj: Any, key: str) -> bool | None:
    if isinstance(obj, dict) and isinstance(obj.get(key), bool):
        return obj[key]
    metadata = _metadata_of(obj)
    if isinstance(metadata.get(key), bool):
        return metadata[key]
    value = getattr(obj, key, None)
    if isinstance(value, bool):
        return value
    return None


def _entourage_payload(space: Any):
    if isinstance(space, dict) and "entourages" in space:
        return space["entourages"]
    metadata = _metadata_of(space)
    if "entourages" in metadata:
        return metadata["entourages"]
    return getattr(space, "entourages", None)


def _entourage_list(space: Any) -> list[Any] | None:
    payload = _entourage_payload(space)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, tuple):
        return list(payload)
    return None


def is_uniform_space(space):
    """Check whether the input carries a usable uniform-space witness."""
    if _explicit_bool(space, "is_uniform_space") is not None:
        return bool(_explicit_bool(space, "is_uniform_space"))
    entourages = _entourage_list(space)
    if entourages:
        return True
    tags = _extract_tags(space)
    return bool(tags & UNIFORM_TRUE_TAGS)


def entourage_system(space):
    """Return the entourage list when a benchmark uniformity is available."""
    entourages = _entourage_list(space)
    if entourages is not None:
        return entourages
    tags = _extract_tags(space)
    if "discrete_uniformity" in tags:
        return ["diagonal_subset", "all_supersets_of_diagonal"]
    if "metric_uniformity" in tags or "metric" in tags or "complete_metric" in tags:
        return ["epsilon_ball_entourages"]
    if is_uniform_space(space):
        return ["symbolic_entourage_basis"]
    return None


def is_uniformly_continuous(mapping):
    """Check whether a mapping carries a benchmark uniform-continuity witness."""
    explicit = _explicit_bool(mapping, "is_uniformly_continuous")
    if explicit is not None:
        return explicit
    tags = _extract_tags(mapping)
    if "uniformly_continuous" in tags:
        return True
    if "not_uniformly_continuous" in tags:
        return False
    if isinstance(mapping, dict):
        if mapping.get("lipschitz_constant") is not None:
            return True
        if mapping.get("map_type") in {"identity", "constant"}:
            return True
    metadata = _metadata_of(mapping)
    if metadata.get("lipschitz_constant") is not None:
        return True
    if metadata.get("map_type") in {"identity", "constant"}:
        return True
    return False


def is_cauchy_filter(filter_obj, uniform_space):
    """Check whether a filter object carries a benchmark Cauchy witness."""
    explicit = _explicit_bool(filter_obj, "is_cauchy_filter")
    if explicit is not None:
        return explicit
    if not is_uniform_space(uniform_space):
        return False
    if isinstance(filter_obj, dict):
        if filter_obj.get("filter_type") == "principal":
            return True
        if filter_obj.get("meets_every_entourage") is True:
            return True
    metadata = _metadata_of(filter_obj)
    if metadata.get("filter_type") == "principal":
        return True
    if metadata.get("meets_every_entourage") is True:
        return True
    return False


def is_uniformly_complete(uniform_space):
    """Check completeness on the benchmark uniform-space corridor."""
    explicit = _explicit_bool(uniform_space, "is_uniformly_complete")
    if explicit is not None:
        return explicit
    if not is_uniform_space(uniform_space):
        return False
    tags = _extract_tags(uniform_space)
    if tags & UNIFORM_COMPLETE_TRUE_TAGS:
        return True
    if isinstance(uniform_space, dict):
        if uniform_space.get("space_type") == "Metric Uniformity":
            return True
        if uniform_space.get("space_type") == "Discrete Uniformity":
            return True
    metadata = _metadata_of(uniform_space)
    if metadata.get("space_type") == "Metric Uniformity":
        return True
    if metadata.get("space_type") == "Discrete Uniformity":
        return True
    return False


__all__ = [
    "is_uniform_space",
    "entourage_system",
    "is_uniformly_continuous",
    "is_cauchy_filter",
    "is_uniformly_complete",
]
