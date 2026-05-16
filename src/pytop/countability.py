"""Countability-style support with exact, theorem-based, and symbolic answers."""

from __future__ import annotations

from typing import Any

from .capabilities import DEFAULT_REGISTRY
from .result import Result

TRUE_TAGS = {
    "first_countable": ["first_countable"],
    "second_countable": ["second_countable"],
    "separable": ["separable"],
    "lindelof": ["lindelof"],
}

FALSE_TAGS = {
    "first_countable": ["not_first_countable"],
    "second_countable": ["not_second_countable"],
    "separable": ["not_separable"],
    "lindelof": ["not_lindelof"],
}

REPORT_PROPERTIES = ("first_countable", "second_countable", "separable", "lindelof")


class CountabilityError(ValueError):
    pass


def normalize_countability_property(name: str) -> str:
    normalized = str(name).strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "countability": "first_countable",
        "first": "first_countable",
        "second": "second_countable",
        "lindelof_property": "lindelof",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in set(TRUE_TAGS):
        raise CountabilityError(
            f"Unsupported countability property {name!r}. Expected one of {sorted(TRUE_TAGS)}."
        )
    return normalized


def analyze_countability(space: Any, property_name: str = "first_countable") -> Result:
    property_name = normalize_countability_property(property_name)
    tags = _extract_tags(space)
    representation = _representation_of(space)
    capability = DEFAULT_REGISTRY.support_for(representation, property_name)

    if _matches_any(tags, FALSE_TAGS[property_name]):
        return Result.false(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=[f"The space carries an explicit negative tag for {property_name}."],
            metadata={
                "representation": representation,
                "property": property_name,
                "tags": sorted(tags),
                "source": "explicit_negative_tag",
            },
        )

    if representation == "finite":
        return Result.true(
            mode="exact",
            value=property_name,
            justification=[f"Every finite topological space is {property_name.replace('_', ' ')}."],
            proof_outline=["A finite topology has a finite base, hence every standard countability consequence follows."],
            metadata={
                "representation": representation,
                "property": property_name,
                "tags": sorted(tags),
                "source": "finite_space",
            },
        )

    if property_name == "first_countable" and "metric" in tags:
        return Result.true(
            mode="theorem",
            value=property_name,
            justification=["Every metric space is first countable."],
            proof_outline=["Use the countable local base of open balls B(x,1/n)."],
            metadata={
                "representation": representation,
                "property": property_name,
                "tags": sorted(tags),
                "source": "theorem",
                "inference_rule": "metric_implies_first_countable",
            },
        )

    if property_name == "first_countable" and "second_countable" in tags:
        return Result.true(
            mode="theorem",
            value=property_name,
            assumptions=["Second countability is provided by tags or metadata."],
            justification=["Every second-countable space is first countable."],
            proof_outline=["Restrict the countable global base to the members containing the chosen point."],
            metadata={
                "representation": representation,
                "property": property_name,
                "tags": sorted(tags),
                "source": "theorem",
                "inference_rule": "second_countable_implies_first_countable",
            },
        )

    if property_name == "second_countable" and {"metric", "separable"}.issubset(tags):
        return Result.true(
            mode="theorem",
            value=property_name,
            assumptions=["The space is metric and separable."],
            justification=["Every separable metric space is second countable."],
            proof_outline=[
                "Choose a countable dense subset.",
                "Use open balls with centers in that dense subset and positive rational radii.",
            ],
            metadata={
                "representation": representation,
                "property": property_name,
                "tags": sorted(tags),
                "source": "theorem",
                "inference_rule": "separable_metric_implies_second_countable",
            },
        )

    if property_name in {"separable", "lindelof"}:
        second_countable_reason = _second_countable_reason(space, tags)
        if second_countable_reason:
            conclusion = "Every second-countable space is separable and Lindelöf."
            rule = (
                "second_countable_implies_separable"
                if property_name == "separable"
                else "second_countable_implies_lindelof"
            )
            return Result.true(
                mode="theorem",
                value=property_name,
                assumptions=[second_countable_reason],
                justification=[conclusion],
                proof_outline=[
                    "For separability, choose one point from each nonempty basic open set.",
                    "For Lindelöfness, thin any open cover using a countable base.",
                ],
                metadata={
                    "representation": representation,
                    "property": property_name,
                    "tags": sorted(tags),
                    "source": "theorem",
                    "inference_rule": rule,
                },
            )

    if _matches_any(tags, TRUE_TAGS[property_name]):
        return Result.true(
            mode=_mode_from_support(capability.support),
            value=property_name,
            justification=[f"The space carries an explicit positive tag for {property_name}."],
            metadata={
                "representation": representation,
                "property": property_name,
                "tags": sorted(tags),
                "source": "explicit_positive_tag",
            },
        )

    return Result.unknown(
        mode=_mode_from_support(capability.support),
        value=property_name,
        justification=[capability.notes or f"No decisive countability information available for {representation}."],
        metadata={"representation": representation, "property": property_name, "tags": sorted(tags)},
    )


def is_first_countable(space: Any) -> Result:
    return analyze_countability(space, "first_countable")


def is_second_countable(space: Any) -> Result:
    return analyze_countability(space, "second_countable")


def is_separable(space: Any) -> Result:
    return analyze_countability(space, "separable")


def is_lindelof(space: Any) -> Result:
    return analyze_countability(space, "lindelof")


def countability_report(space: Any) -> dict[str, Result]:
    return {name: analyze_countability(space, name) for name in REPORT_PROPERTIES}


def render_countability_report(space: Any) -> str:
    report = countability_report(space)
    space_name = _space_name(space)
    lines = [f"Countability report for {space_name}", ""]
    for key in REPORT_PROPERTIES:
        result = report[key]
        status = _status_label(result)
        line = f"- {key}: {status} ({result.mode})"
        rule = str(result.metadata.get("inference_rule", "")).strip()
        if rule:
            line += f" [{rule}]"
        lines.append(line)
    theorem_lines = [
        result.metadata.get("inference_rule")
        for result in report.values()
        if result.metadata.get("inference_rule")
    ]
    if theorem_lines:
        lines.append("")
        lines.append("Theorem corridor:")
        for rule in theorem_lines:
            lines.append(f"- {rule}")
    negative_properties = [key for key, result in report.items() if result.is_false]
    if negative_properties:
        lines.append("")
        lines.append(
            "Warning-line: not every countability property follows from the currently visible family data."
        )
    return "\n".join(lines)



def _second_countable_reason(space: Any, tags: set[str]) -> str | None:
    if "second_countable" in tags:
        return "Second countability is provided by tags or metadata."
    if {"metric", "separable"}.issubset(tags):
        return "Second countability follows from the separable-metric theorem."
    return None

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


def _status_label(result: Result) -> str:
    if result.is_true:
        return "yes"
    if result.is_false:
        return "no"
    if result.is_conditional:
        return "conditional"
    return "unknown"


def _space_name(space: Any) -> str:
    metadata = getattr(space, "metadata", {}) or {}
    for key in ("name", "label", "title"):
        value = str(metadata.get(key, "")).strip()
        if value:
            return value
    return space.__class__.__name__


__all__ = [
    "CountabilityError",
    "normalize_countability_property",
    "analyze_countability",
    "is_first_countable",
    "is_second_countable",
    "is_separable",
    "is_lindelof",
    "countability_report",
    "render_countability_report",
]
