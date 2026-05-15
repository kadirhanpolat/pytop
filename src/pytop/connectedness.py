"""Connectedness support layered over result, capabilities, and theorem inference."""

from __future__ import annotations

from typing import Any

from .capabilities import DEFAULT_REGISTRY, normalize_feature_name
from .result import Result
from .theorem_engine import infer_feature


TRUE_TAGS = {
    "connected": ["connected", "marked_connected"],
    "path_connected": ["path_connected"],
    "locally_connected": ["locally_connected"],
}

FALSE_TAGS = {
    "connected": ["disconnected", "not_connected"],
    "path_connected": ["not_path_connected"],
    "locally_connected": ["not_locally_connected"],
}


class ConnectednessError(ValueError):
    pass


def normalize_connectedness_property(name: str) -> str:
    normalized = normalize_feature_name(name)
    aliases = {
        "connectedness": "connected",
        "pathconnected": "path_connected",
        "local_connectedness": "locally_connected",
    }
    normalized = aliases.get(normalized, normalized)
    valid = set(TRUE_TAGS)
    if normalized not in valid:
        raise ConnectednessError(
            f"Unsupported connectedness property {name!r}. Expected one of {sorted(valid)}."
        )
    return normalized



def analyze_connectedness(space: Any, property_name: str = "connected") -> Result:
    property_name = normalize_connectedness_property(property_name)
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

    if property_name == "connected":
        theorem_result = infer_feature("connected", space)
        if not theorem_result.is_unknown:
            theorem_result.metadata.setdefault("property", property_name)
            return theorem_result

    if representation == "finite" and property_name == "connected" and hasattr(space, "topology"):
        exact = _finite_connected_from_topology(space)
        if exact is not None:
            return Result.true(
                mode="exact",
                value=property_name,
                justification=["The finite topology admits no nontrivial clopen partition."],
                proof_outline=[
                    "Enumerate clopen subsets from the explicit topology.",
                    "Check whether a nontrivial clopen subset exists.",
                ],
                metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
            ) if exact else Result.false(
                mode="exact",
                value=property_name,
                justification=["A nontrivial clopen subset exists in the explicit finite topology."],
                metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
            )

    if _matches_any(tags, TRUE_TAGS[property_name]):
        return Result.true(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=[
                f"The space carries an explicit positive tag for {property_name}."
            ],
            metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
        )

    return Result.unknown(
        mode=_mode_from_support(capability.support),
        value=property_name,
        justification=[capability.notes or f"No decisive connectedness information available for {representation}."],
        metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
    )



def is_connected(space: Any) -> Result:
    return analyze_connectedness(space, "connected")



def is_path_connected(space: Any) -> Result:
    return analyze_connectedness(space, "path_connected")



def is_locally_connected(space: Any) -> Result:
    return analyze_connectedness(space, "locally_connected")



def _finite_connected_from_topology(space: Any) -> bool | None:
    topology = getattr(space, "topology", None)
    carrier = getattr(space, "carrier", None)
    if not topology or carrier is None:
        return None
    all_points = set(carrier)
    opens = {_as_frozenset(open_set) for open_set in topology}
    for open_set in opens:
        subset = set(open_set)
        if not subset or subset == all_points:
            continue
        if frozenset(all_points - subset) in opens:
            return False
    return True



def _as_frozenset(obj: Any) -> frozenset[Any]:
    return frozenset(obj)



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
    "ConnectednessError",
    "normalize_connectedness_property",
    "analyze_connectedness",
    "is_connected",
    "is_path_connected",
    "is_locally_connected",
]
