"""Structured separation analysis for supported infinite space families."""

from __future__ import annotations

from typing import Any

from .infinite_spaces import (
    CocountableSpace,
    CofiniteSpace,
    DiscreteInfiniteSpace,
    IndiscreteInfiniteSpace,
    InfiniteTopologicalSpace,
)
from .result import Result
from .separation import analyze_separation, normalize_separation_property, separation_profile


KNOWN_TRUE = {
    DiscreteInfiniteSpace: {
        "t0",
        "t1",
        "hausdorff",
        "regular",
        "t3",
        "completely_regular",
        "tychonoff",
        "normal",
        "t4",
    },
    IndiscreteInfiniteSpace: {"regular", "normal"},
    CofiniteSpace: {"t0", "t1"},
    CocountableSpace: {"t0", "t1"},
}

KNOWN_FALSE = {
    IndiscreteInfiniteSpace: {"t0", "t1", "hausdorff", "t3", "tychonoff", "t4"},
    CofiniteSpace: {
        "hausdorff",
        "regular",
        "t3",
        "completely_regular",
        "tychonoff",
        "normal",
        "t4",
    },
    CocountableSpace: {
        "hausdorff",
        "regular",
        "t3",
        "completely_regular",
        "tychonoff",
        "normal",
        "t4",
    },
}


def analyze_infinite_separation(space: Any, property_name: str = "hausdorff") -> Result:
    if not isinstance(space, InfiniteTopologicalSpace):
        return analyze_separation(space, property_name)
    property_name = normalize_separation_property(property_name)
    for cls, features in KNOWN_TRUE.items():
        if isinstance(space, cls) and property_name in features:
            return Result.true(
                mode="exact",
                value=property_name,
                justification=[f"{cls.__name__} has a class-level exact separation classification for {property_name}."],
                metadata={"representation": space.metadata.get("representation"), "property": property_name, "source": cls.__name__},
            )
    for cls, features in KNOWN_FALSE.items():
        if isinstance(space, cls) and property_name in features:
            return Result.false(
                mode="exact",
                value=property_name,
                justification=[f"{cls.__name__} has a class-level exact separation classification for {property_name}."],
                metadata={"representation": space.metadata.get("representation"), "property": property_name, "source": cls.__name__},
            )
    return analyze_separation(space, property_name)


def is_t0_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "t0")


def is_t1_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "t1")


def is_hausdorff_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "hausdorff")


def is_regular_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "regular")


def is_t3_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "t3")


def is_completely_regular_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "completely_regular")


def is_tychonoff_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "tychonoff")


def is_normal_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "normal")


def is_t4_infinite(space: Any) -> Result:
    return analyze_infinite_separation(space, "t4")


def infinite_separation_report(space: Any) -> dict[str, Result]:
    if isinstance(space, InfiniteTopologicalSpace):
        return {
            "t0": is_t0_infinite(space),
            "t1": is_t1_infinite(space),
            "hausdorff": is_hausdorff_infinite(space),
            "regular": is_regular_infinite(space),
            "t3": is_t3_infinite(space),
            "completely_regular": is_completely_regular_infinite(space),
            "tychonoff": is_tychonoff_infinite(space),
            "normal": is_normal_infinite(space),
            "t4": is_t4_infinite(space),
        }
    return separation_profile(space)
