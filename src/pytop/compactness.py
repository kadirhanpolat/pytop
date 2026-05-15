"""Compactness support layered over result, capabilities, and theorem inference.

The goal is not to promise a universal decision procedure for arbitrary infinite
spaces. Instead, this module reports whether a conclusion is exact,
theorem-based, symbolic, or currently unknown.
"""

from __future__ import annotations

from typing import Any

from .capabilities import DEFAULT_REGISTRY, normalize_feature_name
from .result import Result
from .theorem_engine import infer_feature


TRUE_TAGS = {
    "compact": ["compact", "marked_compact"],
    "countably_compact": ["countably_compact"],
    "sequentially_compact": ["sequentially_compact"],
    "limit_point_compact": ["limit_point_compact"],
    "lindelof": ["lindelof"],
}

FALSE_TAGS = {
    "compact": ["noncompact", "not_compact"],
    "countably_compact": ["not_countably_compact"],
    "sequentially_compact": ["not_sequentially_compact"],
    "limit_point_compact": ["not_limit_point_compact"],
    "lindelof": ["not_lindelof"],
}


class CompactnessError(ValueError):
    """Raised when an invalid compactness property is requested."""


def normalize_compactness_property(name: str) -> str:
    normalized = normalize_feature_name(name)
    aliases = {
        "compactness": "compact",
        "countablycompact": "countably_compact",
        "countably_compactness": "countably_compact",
        "sequentialcompactness": "sequentially_compact",
        "limit_point_compactness": "limit_point_compact",
    }
    normalized = aliases.get(normalized, normalized)
    valid = set(TRUE_TAGS)
    if normalized not in valid:
        raise CompactnessError(
            f"Unsupported compactness property {name!r}. Expected one of {sorted(valid)}."
        )
    return normalized


def analyze_compactness(space: Any, property_name: str = "compact") -> Result:
    """Return a structured result for a compactness-style query."""

    property_name = normalize_compactness_property(property_name)
    tags = _extract_tags(space)
    representation = _representation_of(space)
    capability = DEFAULT_REGISTRY.support_for(representation, property_name)

    if _matches_any(tags, FALSE_TAGS[property_name]):
        return Result.false(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=[
                f"The space carries an explicit negative tag for {property_name}."
            ],
            metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
        )

    if representation == "finite":
        return _finite_compactness_result(property_name, representation, tags)

    if property_name == "compact":
        theorem_result = infer_feature("compact", space)
        if not theorem_result.is_unknown:
            theorem_result.metadata.setdefault("property", property_name)
            return theorem_result

    if _matches_any(tags, TRUE_TAGS[property_name]):
        return Result.true(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=[
                f"The space carries an explicit positive tag for {property_name}."
            ],
            metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
        )

    if property_name == "lindelof" and "second_countable" in tags:
        return Result.true(
            mode="theorem",
            value=property_name,
            assumptions=["Second countability is interpreted via tags or metadata."],
            justification=["Every second-countable space is Lindelöf."],
            proof_outline=[
                "Use a countable base.",
                "From any open cover choose one cover element for each basis element it contains.",
            ],
            metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
        )

    return Result.unknown(
        mode=_mode_from_support(capability.support),
        value=property_name,
        justification=[capability.notes or f"No decisive compactness information available for {representation}."],
        metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
    )


def is_compact(space: Any) -> Result:
    return analyze_compactness(space, "compact")


def is_countably_compact(space: Any) -> Result:
    return analyze_compactness(space, "countably_compact")


def is_sequentially_compact(space: Any) -> Result:
    return analyze_compactness(space, "sequentially_compact")


def is_limit_point_compact(space: Any) -> Result:
    return analyze_compactness(space, "limit_point_compact")


def is_lindelof(space: Any) -> Result:
    return analyze_compactness(space, "lindelof")


def _finite_compactness_result(property_name: str, representation: str, tags: set[str]) -> Result:
    return Result.true(
        mode="exact",
        value=property_name,
        justification=[
            f"Every finite topological space is {property_name.replace('_', ' ')}."
        ],
        proof_outline=[
            "Any relevant open-cover or sequence-based requirement reduces to finitely many cases on a finite carrier."
        ],
        metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
    )


def _representation_of(space: Any) -> str:
    metadata = getattr(space, "metadata", {}) or {}
    return str(metadata.get("representation", "symbolic_general")).strip().lower()



def _extract_tags(space: Any) -> set[str]:
    tags: set[str] = set()
    raw_tags = getattr(space, "tags", set())
    tags.update(str(tag).strip().lower() for tag in raw_tags if str(tag).strip())
    metadata = getattr(space, "metadata", {}) or {}
    for tag in metadata.get("tags", []):
        text = str(tag).strip().lower()
        if text:
            tags.add(text)
    return tags



def _matches_any(tags: set[str], candidates: list[str]) -> bool:
    return any(candidate in tags for candidate in candidates)



def _mode_from_support(support: str) -> str:
    return {
        "exact": "exact",
        "theorem": "theorem",
        "symbolic": "symbolic",
        "mixed": "mixed",
        "none": "symbolic",
    }[support]


__all__ = [
    "CompactnessError",
    "normalize_compactness_property",
    "analyze_compactness",
    "is_compact",
    "is_countably_compact",
    "is_sequentially_compact",
    "is_limit_point_compact",
    "is_lindelof",
]
