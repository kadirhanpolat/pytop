"""Comparison utilities for spaces and structures.

The module offers small but concrete comparison helpers. Exact finite
homeomorphism detection is included for small explicit finite spaces, while
broader space comparison is profile-based and uses already available analyzers.
"""

from __future__ import annotations

from itertools import permutations
from typing import Any

from .compactness import is_compact
from .connectedness import is_connected
from .countability import is_first_countable, is_second_countable, is_separable
from .invariants import cellularity, character, density, lindelof_number, weight
from .result import Result
from .separation import is_hausdorff, is_t0, is_t1



def compare_spaces(left: Any, right: Any) -> dict[str, Any]:
    return {
        "same_representation": _representation_of(left) == _representation_of(right),
        "same_cardinality": _carrier_size(left) == _carrier_size(right),
        "left_profile": invariant_profile(left),
        "right_profile": invariant_profile(right),
        "basic_property_match": _basic_property_match(left, right),
        "tag_overlap": sorted(_extract_tags(left) & _extract_tags(right)),
    }



def invariant_profile(space: Any) -> dict[str, Any]:
    profile = {
        "weight": weight(space).value,
        "density": density(space).value,
        "character": character(space).value,
        "lindelof_number": lindelof_number(space).value,
        "cellularity": cellularity(space).value,
        "compact": is_compact(space).status,
        "connected": is_connected(space).status,
        "t0": is_t0(space).status,
        "t1": is_t1(space).status,
        "hausdorff": is_hausdorff(space).status,
        "first_countable": is_first_countable(space).status,
        "second_countable": is_second_countable(space).status,
        "separable": is_separable(space).status,
    }
    return profile



def finite_homeomorphism_result(left: Any, right: Any) -> Result:
    if not (_space_is_finite(left) and _space_is_finite(right) and hasattr(left, "topology") and hasattr(right, "topology")):
        return Result.unknown(
            mode="symbolic",
            value="homeomorphic",
            justification=["Exact finite homeomorphism detection requires two explicit finite spaces."],
            metadata={"comparison": "finite_homeomorphism"},
        )

    left_points = tuple(getattr(left, "carrier", ()))
    right_points = tuple(getattr(right, "carrier", ()))
    if len(left_points) != len(right_points):
        return Result.false(
            mode="exact",
            value="homeomorphic",
            justification=["Finite spaces with different cardinalities cannot be homeomorphic."],
            metadata={"comparison": "finite_homeomorphism"},
        )

    left_topology = {frozenset(U) for U in getattr(left, "topology", ())}
    right_topology = {frozenset(U) for U in getattr(right, "topology", ())}

    for perm in permutations(right_points):
        mapping = dict(zip(left_points, perm))
        if _is_homeomorphism_mapping(mapping, left_topology, right_topology):
            return Result.true(
                mode="exact",
                value="homeomorphic",
                justification=["A bijection preserving the topology in both directions was found."],
                proof_outline=[
                    "Enumerate bijections between the two finite carriers.",
                    "Check whether direct images of open sets are open and whether the inverse also preserves openness.",
                ],
                metadata={"comparison": "finite_homeomorphism", "witness": mapping},
            )

    return Result.false(
        mode="exact",
        value="homeomorphic",
        justification=["No topology-preserving bijection exists between the two finite spaces."],
        metadata={"comparison": "finite_homeomorphism"},
    )



def compare_invariants(left: Any, right: Any) -> dict[str, tuple[Any, Any]]:
    left_profile = invariant_profile(left)
    right_profile = invariant_profile(right)
    return {key: (left_profile.get(key), right_profile.get(key)) for key in sorted(left_profile)}



def _basic_property_match(left: Any, right: Any) -> bool:
    keys = ["compact", "connected", "t0", "t1", "hausdorff", "first_countable", "second_countable", "separable"]
    left_profile = invariant_profile(left)
    right_profile = invariant_profile(right)
    return all(left_profile.get(key) == right_profile.get(key) for key in keys)



def _is_homeomorphism_mapping(mapping: dict[Any, Any], left_topology: set[frozenset[Any]], right_topology: set[frozenset[Any]]) -> bool:
    image_of_left_opens = {
        frozenset(mapping[x] for x in open_set)
        for open_set in left_topology
    }
    if image_of_left_opens != right_topology:
        return False
    inverse = {v: k for k, v in mapping.items()}
    image_of_right_opens = {
        frozenset(inverse[y] for y in open_set)
        for open_set in right_topology
    }
    return image_of_right_opens == left_topology



def _space_is_finite(space: Any) -> bool:
    try:
        return bool(space.is_finite())
    except Exception:
        return False



def _carrier_size(space: Any) -> int | None:
    carrier = getattr(space, "carrier", None)
    if carrier is None or isinstance(carrier, (str, bytes)):
        return None
    try:
        return len(carrier)
    except Exception:
        return None



def _representation_of(space: Any) -> str:
    metadata = getattr(space, "metadata", None)
    if isinstance(metadata, dict) and metadata.get("representation"):
        return str(metadata["representation"]).strip().lower()
    return "finite" if _space_is_finite(space) else "symbolic_general"



def _extract_tags(space: Any) -> set[str]:
    tags: set[str] = set()
    raw = getattr(space, "tags", None)
    if raw is not None:
        tags.update(str(tag).strip().lower() for tag in raw if str(tag).strip())
    metadata = getattr(space, "metadata", None)
    if isinstance(metadata, dict):
        tags.update(str(tag).strip().lower() for tag in metadata.get("tags", []) if str(tag).strip())
    return tags


__all__ = [
    "compare_spaces",
    "compare_invariants",
    "invariant_profile",
    "finite_homeomorphism_result",
]
