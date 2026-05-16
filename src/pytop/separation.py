"""Separation-axiom support with exact, theorem-based, and symbolic answers.

The module starts with the undergraduate ``T0/T1/T2`` layer and then exposes
finite, pedagogical helpers for the Cilt III advanced-separation corridor:
regularity, normality, T3/T4, complete regularity, and Tychonoff status.  The
advanced helpers are deliberately conservative outside exact finite data and
well-known theorem/tag cases.
"""

from __future__ import annotations

from typing import Any

from .capabilities import DEFAULT_REGISTRY
from .result import Result

BASIC_PROPERTIES = {"t0", "t1", "hausdorff"}
ADVANCED_PROPERTIES = {
    "regular",
    "t3",
    "normal",
    "t4",
    "completely_regular",
    "tychonoff",
}
SUPPORTED_PROPERTIES = BASIC_PROPERTIES | ADVANCED_PROPERTIES
DEFAULT_PROFILE_PROPERTIES = (
    "t0",
    "t1",
    "hausdorff",
    "regular",
    "t3",
    "completely_regular",
    "tychonoff",
    "normal",
    "t4",
)

TRUE_TAGS = {
    "t0": ["t0", "kolmogorov"],
    "t1": ["t1"],
    "hausdorff": ["hausdorff", "t2"],
    "regular": ["regular"],
    "t3": ["t3", "regular_t1"],
    "completely_regular": ["completely_regular", "functionally_regular"],
    "tychonoff": ["tychonoff", "t3_5", "t3½"],
    "normal": ["normal"],
    "t4": ["t4", "normal_t1"],
}
FALSE_TAGS = {
    "t0": ["not_t0"],
    "t1": ["not_t1"],
    "hausdorff": ["not_hausdorff", "not_t2"],
    "regular": ["not_regular"],
    "t3": ["not_t3", "not_regular_t1"],
    "completely_regular": ["not_completely_regular", "not_functionally_regular"],
    "tychonoff": ["not_tychonoff", "not_t3_5"],
    "normal": ["not_normal"],
    "t4": ["not_t4", "not_normal_t1"],
}


class SeparationError(ValueError):
    pass


def normalize_separation_property(name: str) -> str:
    normalized = str(name).strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "separation": "hausdorff",
        "t2": "hausdorff",
        "t_2": "hausdorff",
        "hausdorffness": "hausdorff",
        "kolmogorov": "t0",
        "t_0": "t0",
        "t_1": "t1",
        "regular_t1": "t3",
        "t_3": "t3",
        "normal_t1": "t4",
        "t_4": "t4",
        "complete_regular": "completely_regular",
        "functionally_regular": "completely_regular",
        "completely_regular_t1": "tychonoff",
        "t3_5": "tychonoff",
        "t3½": "tychonoff",
        "t_3_5": "tychonoff",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_PROPERTIES:
        raise SeparationError(
            "Expected one of 't0', 't1', 'hausdorff', 'regular', 't3', "
            "'completely_regular', 'tychonoff', 'normal', or 't4'."
        )
    return normalized


def analyze_separation(space: Any, property_name: str = "hausdorff") -> Result:
    property_name = normalize_separation_property(property_name)
    tags = _extract_tags(space)
    representation = _representation_of(space)
    capability = DEFAULT_REGISTRY.support_for(representation, property_name)

    if _matches_any(tags, FALSE_TAGS[property_name]):
        return Result.false(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=[f"The space carries an explicit negative tag for {property_name}."],
            metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
        )

    if representation == "finite" and hasattr(space, "topology"):
        exact = _finite_separation(space, property_name)
        if exact is not None:
            return _finite_result(exact, representation, property_name, tags)

    theorem_result = _theorem_level_separation(space, property_name, tags, representation)
    if theorem_result is not None:
        return theorem_result

    if _matches_any(tags, TRUE_TAGS[property_name]) or _positive_tag_implies(tags, property_name):
        return Result.true(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=[f"The space carries a positive tag or implication for {property_name}."],
            metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
        )

    negative_implication = _negative_tag_implication(tags, property_name)
    if negative_implication:
        return Result.false(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=[negative_implication],
            metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
        )

    return Result.unknown(
        mode=_mode_from_support(capability.support),
        value=property_name,
        justification=[capability.notes or f"No decisive separation information available for {representation}."],
        metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
    )


def separation_profile(space: Any, properties: tuple[str, ...] | None = None) -> dict[str, Result]:
    """Return a conservative profile of basic and advanced separation properties."""

    selected = properties or DEFAULT_PROFILE_PROPERTIES
    return {normalize_separation_property(name): analyze_separation(space, name) for name in selected}


def advanced_separation_report(space: Any) -> dict[str, Result]:
    """Alias for the Cilt III advanced-separation profile used by notebooks."""

    return separation_profile(space)


def is_t0(space: Any) -> Result:
    return analyze_separation(space, "t0")


def is_t1(space: Any) -> Result:
    return analyze_separation(space, "t1")


def is_hausdorff(space: Any) -> Result:
    return analyze_separation(space, "hausdorff")


def is_t2(space: Any) -> Result:
    return analyze_separation(space, "hausdorff")


def is_regular(space: Any) -> Result:
    return analyze_separation(space, "regular")


def is_t3(space: Any) -> Result:
    return analyze_separation(space, "t3")


def is_completely_regular(space: Any) -> Result:
    return analyze_separation(space, "completely_regular")


def is_tychonoff(space: Any) -> Result:
    return analyze_separation(space, "tychonoff")


def is_normal(space: Any) -> Result:
    return analyze_separation(space, "normal")


def is_t4(space: Any) -> Result:
    return analyze_separation(space, "t4")


def _finite_result(exact: bool, representation: str, property_name: str, tags: set[str]) -> Result:
    metadata = {"representation": representation, "property": property_name, "tags": sorted(tags)}
    if exact:
        return Result.true(
            mode="exact",
            value=property_name,
            justification=[f"The explicit finite topology satisfies {property_name}."],
            proof_outline=[_finite_proof_hint(property_name)],
            metadata=metadata,
        )
    return Result.false(
        mode="exact",
        value=property_name,
        justification=[f"The explicit finite topology fails {property_name}."],
        metadata=metadata,
    )


def _finite_proof_hint(property_name: str) -> str:
    if property_name in BASIC_PROPERTIES:
        return "Check all distinct pairs of points against the defining open-set criterion."
    if property_name in {"regular", "t3"}:
        return "Check every point and closed set not containing it for disjoint open neighbourhoods."
    if property_name in {"normal", "t4"}:
        return "Check every pair of disjoint closed sets for disjoint open neighbourhoods."
    return "Use the finite exact separation classification available for this property."


def _finite_separation(space: Any, property_name: str) -> bool | None:
    topology = getattr(space, "topology", None)
    carrier = getattr(space, "carrier", None)
    if not topology or carrier is None:
        return None
    opens, points = _finite_open_sets(space)
    if not opens:
        return None

    if property_name in {"t0", "t1", "hausdorff"}:
        return _finite_basic_separation(opens, points, property_name)
    if property_name == "regular":
        return _finite_regular(opens, points)
    if property_name == "t3":
        return _finite_basic_separation(opens, points, "t1") and _finite_regular(opens, points)
    if property_name == "normal":
        return _finite_normal(opens, points)
    if property_name == "t4":
        return _finite_basic_separation(opens, points, "t1") and _finite_normal(opens, points)
    if property_name == "completely_regular":
        # For finite T1 spaces, the topology is discrete, hence completely regular.
        # For non-T1 finite spaces, the general functional question is left symbolic.
        if _finite_basic_separation(opens, points, "t1"):
            return True
        return None
    if property_name == "tychonoff":
        return _finite_basic_separation(opens, points, "t1")
    return None


def _finite_open_sets(space: Any) -> tuple[list[set[Any]], list[Any]]:
    opens = [set(open_set) for open_set in getattr(space, "topology")]
    points = list(getattr(space, "carrier"))
    return opens, points


def _finite_closed_sets(opens: list[set[Any]], points: list[Any]) -> list[set[Any]]:
    carrier = set(points)
    return [carrier - open_set for open_set in opens]


def _finite_basic_separation(opens: list[set[Any]], points: list[Any], property_name: str) -> bool:
    for i, x in enumerate(points):
        for y in points[i + 1 :]:
            if property_name == "t0":
                if not any((x in U) ^ (y in U) for U in opens):
                    return False
            elif property_name == "t1":
                has_x_not_y = any(x in U and y not in U for U in opens)
                has_y_not_x = any(y in U and x not in U for U in opens)
                if not (has_x_not_y and has_y_not_x):
                    return False
            elif property_name == "hausdorff":
                found = False
                for U in opens:
                    if x not in U:
                        continue
                    for V in opens:
                        if y in V and U.isdisjoint(V):
                            found = True
                            break
                    if found:
                        break
                if not found:
                    return False
    return True


def _finite_regular(opens: list[set[Any]], points: list[Any]) -> bool:
    closed_sets = _finite_closed_sets(opens, points)
    for x in points:
        for closed in closed_sets:
            if x in closed:
                continue
            if not _separate_point_and_closed_set(opens, x, closed):
                return False
    return True


def _finite_normal(opens: list[set[Any]], points: list[Any]) -> bool:
    closed_sets = _finite_closed_sets(opens, points)
    for i, first in enumerate(closed_sets):
        for second in closed_sets[i:]:
            if first.isdisjoint(second) and not _separate_closed_sets(opens, first, second):
                return False
    return True


def _separate_point_and_closed_set(opens: list[set[Any]], point: Any, closed: set[Any]) -> bool:
    for point_neighborhood in opens:
        if point not in point_neighborhood:
            continue
        for closed_neighborhood in opens:
            if closed <= closed_neighborhood and point_neighborhood.isdisjoint(closed_neighborhood):
                return True
    return False


def _separate_closed_sets(opens: list[set[Any]], first: set[Any], second: set[Any]) -> bool:
    for first_neighborhood in opens:
        if not first <= first_neighborhood:
            continue
        for second_neighborhood in opens:
            if second <= second_neighborhood and first_neighborhood.isdisjoint(second_neighborhood):
                return True
    return False


def _theorem_level_separation(space: Any, property_name: str, tags: set[str], representation: str) -> Result | None:
    capability = DEFAULT_REGISTRY.support_for(representation, property_name)
    metadata = {"representation": representation, "property": property_name, "tags": sorted(tags)}

    if "metric" in tags:
        metric_properties = {
            "t0",
            "t1",
            "hausdorff",
            "regular",
            "t3",
            "completely_regular",
            "tychonoff",
            "normal",
            "t4",
        }
        if property_name in metric_properties:
            return Result.true(
                mode="theorem",
                value=property_name,
                justification=[_metric_justification(property_name)],
                proof_outline=["Use metric balls or distance-to-closed-set functions to obtain the requested separation."],
                metadata=metadata,
            )

    if property_name == "t1" and _positive_tag_implies(tags, "t1"):
        return Result.true(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=["The supplied stronger separation information implies T1."],
            metadata=metadata,
        )

    if property_name == "t0" and _positive_tag_implies(tags, "t0"):
        return Result.true(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=["The supplied stronger separation information implies T0."],
            metadata=metadata,
        )

    if property_name == "hausdorff" and _positive_tag_implies(tags, "hausdorff"):
        return Result.true(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=["The supplied stronger separation information implies Hausdorffness."],
            metadata=metadata,
        )

    if property_name == "completely_regular" and _positive_tag_implies(tags, "completely_regular"):
        return Result.true(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=["Tychonoff or normal T1 information gives complete regularity."],
            metadata=metadata,
        )

    return None


def _metric_justification(property_name: str) -> str:
    if property_name == "hausdorff":
        return "Every metric space is Hausdorff."
    if property_name == "t1":
        return "Every metric space is Hausdorff, hence T1."
    if property_name == "t0":
        return "Every metric space is Hausdorff, hence T1 and T0."
    if property_name in {"regular", "t3", "completely_regular", "tychonoff"}:
        return "Distance-to-a-closed-set functions make every metric space completely regular, hence regular."
    if property_name in {"normal", "t4"}:
        return "Every metric space is normal; with T1 this gives the T4 separation level."
    return "Metric structure supplies the requested separation property."


def _positive_tag_implies(tags: set[str], property_name: str) -> bool:
    stronger_tags = {
        "t0": {"t1", "hausdorff", "t2", "t3", "tychonoff", "t3_5", "t4"},
        "t1": {"hausdorff", "t2", "t3", "tychonoff", "t3_5", "t4"},
        "hausdorff": {"t3", "tychonoff", "t3_5", "t4"},
        "regular": {"t3", "t4"},
        "t3": {"t3", "t4"},
        "completely_regular": {"tychonoff", "t3_5", "t4"},
        "tychonoff": {"tychonoff", "t3_5", "t4"},
        "normal": {"t4"},
        "t4": {"t4"},
    }
    return bool(tags & stronger_tags.get(property_name, set()))


def _negative_tag_implication(tags: set[str], property_name: str) -> str:
    if property_name in {"t3", "tychonoff", "t4"} and "not_t1" in tags:
        return f"The property {property_name} includes T1, but the space is tagged not_t1."
    if property_name in {"regular", "normal"} and {"t1", "not_hausdorff"} <= tags:
        return f"A T1 {property_name} space would be Hausdorff; the tags record T1 and not_hausdorff."
    if property_name == "t3" and "not_regular" in tags:
        return "T3 requires regularity, but the space is tagged not_regular."
    if property_name == "t4" and "not_normal" in tags:
        return "T4 requires normality, but the space is tagged not_normal."
    if property_name == "tychonoff" and "not_completely_regular" in tags:
        return "Tychonoff requires complete regularity, but the space is tagged not_completely_regular."
    return ""


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
    "SeparationError",
    "normalize_separation_property",
    "analyze_separation",
    "separation_profile",
    "advanced_separation_report",
    "is_t0",
    "is_t1",
    "is_hausdorff",
    "is_t2",
    "is_regular",
    "is_t3",
    "is_completely_regular",
    "is_tychonoff",
    "is_normal",
    "is_t4",
]
