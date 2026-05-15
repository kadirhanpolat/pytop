"""Advanced compactification bridge helpers.

This v0.1.102 surface replaces the old placeholders with a conservative but
genuinely usable theorem/symbolic layer for three related notions:

- Cech-completeness
- realcompactness
- perfect mappings

The goal is not a full decision procedure for arbitrary spaces; instead the
module reads explicit tags/metadata and a few stable theorem corridors, then
returns structured ``Result`` objects that distinguish exact, theorem-level,
conditional, and unknown outcomes.
"""

from __future__ import annotations

from typing import Any

from .result import Result


VERSION = "0.1.102"

CECH_TRUE_TAGS = {
    "cech_complete",
    "cech-complete",
    "complete_metric",
    "completely_metrizable",
    "polish",
    "compact_hausdorff",
}
CECH_FALSE_TAGS = {
    "not_cech_complete",
    "not_cech-complete",
}
REALCOMPACT_TRUE_TAGS = {
    "realcompact",
    "hewitt_realcompact",
    "complete_metric",
    "completely_metrizable",
    "polish",
    "compact_hausdorff",
    "discrete",
    "countable_discrete",
    "finite_discrete",
}
REALCOMPACT_FALSE_TAGS = {
    "not_realcompact",
}
PERFECT_TRUE_TAGS = {
    "perfect_map",
}
PERFECT_FALSE_TAGS = {
    "not_perfect_map",
}
TYCHONOFF_TAGS = {
    "tychonoff",
    "tikhonov",
    "completely_regular_t1",
    "compact_hausdorff",
    "polish",
    "realcompact",
    "cech_complete",
}
HAUSDORFF_TAGS = {
    "hausdorff",
    "t2",
    "compact_hausdorff",
    "finite_hausdorff",
}
METRIC_LIKE_TAGS = {
    "metric",
    "metrizable",
    "complete_metric",
    "completely_metrizable",
    "polish",
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


def _representation_of(obj: Any) -> str:
    if isinstance(obj, dict) and "representation" in obj:
        return str(obj["representation"]).strip().lower()
    metadata = _metadata_of(obj)
    if "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(obj, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _name_of(obj: Any, fallback: str) -> str:
    if isinstance(obj, dict):
        value = obj.get("name")
        if value:
            return str(value)
    metadata = _metadata_of(obj)
    if metadata.get("name"):
        return str(metadata["name"])
    value = getattr(obj, "name", None)
    if value:
        return str(value)
    return fallback


def _has_any(tags: set[str], candidates: set[str]) -> bool:
    return bool(tags & candidates)


def _bool_field(obj: Any, key: str) -> bool | None:
    if isinstance(obj, dict) and key in obj and isinstance(obj[key], bool):
        return obj[key]
    metadata = _metadata_of(obj)
    if key in metadata and isinstance(metadata[key], bool):
        return metadata[key]
    value = getattr(obj, key, None)
    if isinstance(value, bool):
        return value
    return None


def _space_metadata(space: Any, tags: set[str]) -> dict[str, Any]:
    return {
        "version": VERSION,
        "representation": _representation_of(space),
        "space_name": _name_of(space, "anonymous_space"),
        "tags": sorted(tags),
    }


def is_cech_complete(space: Any) -> Result:
    """Conservatively assess Cech-completeness.

    Positive theorem corridors:
    - explicit ``cech_complete`` tag,
    - complete/completely metrizable tags,
    - compact Hausdorff tag.
    """
    tags = _extract_tags(space)
    metadata = _space_metadata(space, tags)

    if _has_any(tags, CECH_FALSE_TAGS):
        return Result.false(
            mode="theorem",
            value="cech_complete",
            justification=["The space carries an explicit negative Cech-completeness tag."],
            metadata=metadata,
        )

    if _has_any(tags, {"finite_discrete", "finite_hausdorff"}):
        return Result.true(
            mode="theorem",
            value="cech_complete",
            justification=[
                "Finite Hausdorff spaces are compact Hausdorff.",
                "Compact Hausdorff spaces are Cech-complete.",
            ],
            metadata=metadata,
        )

    if _has_any(tags, CECH_TRUE_TAGS):
        return Result.true(
            mode="theorem",
            value="cech_complete",
            justification=[
                "The space lies in a standard positive corridor for Cech-completeness.",
                "Complete metrizable and compact Hausdorff spaces are classical examples.",
            ],
            metadata=metadata,
        )

    if _has_any(tags, METRIC_LIKE_TAGS):
        return Result.conditional(
            mode="theorem",
            value="cech_complete",
            justification=[
                "Metrizability alone does not imply Cech-completeness.",
                "A completeness witness or an explicit positive tag is still required.",
            ],
            metadata=metadata,
        )

    return Result.unknown(
        mode="symbolic",
        value="cech_complete",
        justification=["Insufficient structural information for a conservative Cech-completeness decision."],
        metadata=metadata,
    )


def is_realcompact(space: Any) -> Result:
    """Conservatively assess realcompactness.

    Positive theorem corridors:
    - explicit ``realcompact`` tag,
    - complete/completely metrizable tags,
    - compact Hausdorff tag,
    - discrete benchmark tags.
    """
    tags = _extract_tags(space)
    metadata = _space_metadata(space, tags)

    if _has_any(tags, REALCOMPACT_FALSE_TAGS):
        return Result.false(
            mode="theorem",
            value="realcompact",
            justification=["The space carries an explicit negative realcompactness tag."],
            metadata=metadata,
        )

    if _has_any(tags, REALCOMPACT_TRUE_TAGS):
        return Result.true(
            mode="theorem",
            value="realcompact",
            justification=[
                "The space lies in a standard positive corridor for realcompactness.",
                "Complete metrizable, compact Hausdorff, and discrete benchmark cases are realcompact.",
            ],
            metadata=metadata,
        )

    if _has_any(tags, {"finite_hausdorff", "finite_discrete"}):
        return Result.true(
            mode="theorem",
            value="realcompact",
            justification=[
                "Finite Hausdorff spaces are compact Hausdorff.",
                "Compact Hausdorff spaces are realcompact.",
            ],
            metadata=metadata,
        )

    if _has_any(tags, TYCHONOFF_TAGS):
        return Result.conditional(
            mode="theorem",
            value="realcompact",
            justification=[
                "Tychonoff-type information is necessary but not by itself sufficient here.",
                "Add an explicit realcompactness witness or a stronger benchmark tag.",
            ],
            metadata=metadata,
        )

    return Result.unknown(
        mode="symbolic",
        value="realcompact",
        justification=["Insufficient structural information for a conservative realcompactness decision."],
        metadata=metadata,
    )


def is_perfect_map(mapping: Any) -> Result:
    """Assess whether a mapping satisfies the perfect-map corridor.

    A perfect map is treated here as a continuous, closed, surjective map with
    compact fibers. Exact boolean data is respected when provided explicitly.
    """
    tags = _extract_tags(mapping)
    metadata = {
        "version": VERSION,
        "mapping_name": _name_of(mapping, "anonymous_mapping"),
        "representation": _representation_of(mapping),
        "tags": sorted(tags),
    }

    if _has_any(tags, PERFECT_FALSE_TAGS):
        return Result.false(
            mode="theorem",
            value="perfect_map",
            justification=["The mapping carries an explicit negative perfect-map tag."],
            metadata=metadata,
        )

    if _has_any(tags, PERFECT_TRUE_TAGS):
        return Result.true(
            mode="theorem",
            value="perfect_map",
            justification=["The mapping carries an explicit perfect-map tag."],
            metadata=metadata,
        )

    feature_map = {
        "continuous": _bool_field(mapping, "continuous"),
        "closed": _bool_field(mapping, "closed"),
        "compact_fibers": _bool_field(mapping, "compact_fibers"),
        "surjective": _bool_field(mapping, "surjective"),
    }
    metadata["feature_map"] = dict(feature_map)

    if all(value is True for value in feature_map.values()):
        return Result.true(
            mode="exact",
            value="perfect_map",
            justification=[
                "The mapping explicitly records continuity, closedness, surjectivity, and compact fibers.",
            ],
            metadata=metadata,
        )

    failed = [name for name, value in feature_map.items() if value is False]
    if failed:
        return Result.false(
            mode="exact",
            value="perfect_map",
            justification=[f"The mapping explicitly fails the required feature(s): {', '.join(failed)}."],
            metadata=metadata,
        )

    present = [name for name, value in feature_map.items() if value is True]
    if present:
        return Result.conditional(
            mode="symbolic",
            value="perfect_map",
            justification=[
                f"Only part of the perfect-map corridor is witnessed explicitly: {', '.join(present)}.",
                "Closedness, surjectivity, continuity, and compact-fiber data must all be known.",
            ],
            metadata=metadata,
        )

    return Result.unknown(
        mode="symbolic",
        value="perfect_map",
        justification=["No explicit perfect-map witness data was supplied."],
        metadata=metadata,
    )


def advanced_compactness_profile(space: Any) -> dict[str, Any]:
    """Return a compact profile for the advanced compactification bridge."""
    cech = is_cech_complete(space)
    realcompact = is_realcompact(space)
    tags = _extract_tags(space)
    return {
        "version": VERSION,
        "representation": _representation_of(space),
        "space_name": _name_of(space, "anonymous_space"),
        "tags": sorted(tags),
        "cech_complete": cech.status == "true",
        "realcompact": realcompact.status == "true",
        "cech_complete_result": cech,
        "realcompact_result": realcompact,
        "benchmark_summary": {
            "cech_status": cech.status,
            "realcompact_status": realcompact.status,
            "shares_positive_corridor": cech.status == "true" and realcompact.status == "true",
        },
    }
