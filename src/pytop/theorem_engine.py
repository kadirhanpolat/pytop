"""A small theorem-backed inference engine for `pytop`.

This engine is intentionally modest. It does not attempt universal automated
proof search. Instead, it provides a traceable registry of theorem rules that
can yield exact-looking mathematical conclusions in well-described settings.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from .capabilities import DEFAULT_REGISTRY, normalize_feature_name
from .result import Result
from .theorem_profile_alignment import get_promoted_theorem_profile_alignments


@dataclass(slots=True)
class TheoremRule:
    name: str
    feature: str
    conclusion: bool = True
    result_value: Any | None = None
    requires_all: set[str] = field(default_factory=set)
    assumptions: list[str] = field(default_factory=list)
    justification: list[str] = field(default_factory=list)
    proof_outline: list[str] = field(default_factory=list)
    profile_family: str | None = None
    profile_keys: tuple[str, ...] = ()
    chapter_targets: tuple[str, ...] = ()

    def applies_to(self, tags: set[str]) -> bool:
        return self.requires_all.issubset(tags)


class TheoremEngine:
    """Registry-driven theorem support.

    The engine reads tags from a space-like object or a plain mapping. A rule
    applies when all of its required tags are present.
    """

    def __init__(self, rules: Iterable[TheoremRule] = ()) -> None:
        self._rules: dict[str, list[TheoremRule]] = {}
        for rule in rules:
            self.register(rule)

    def register(self, rule: TheoremRule) -> None:
        feature = normalize_feature_name(rule.feature)
        self._rules.setdefault(feature, []).append(rule)

    def rules_for(self, feature: str) -> list[TheoremRule]:
        return list(self._rules.get(normalize_feature_name(feature), []))

    def infer(self, feature: str, obj: Any) -> Result:
        feature = normalize_feature_name(feature)
        tags = extract_tags(obj)
        representation = extract_representation(obj)
        matched = [rule for rule in self.rules_for(feature) if rule.applies_to(tags)]

        if not matched:
            capability = DEFAULT_REGISTRY.support_for(representation, feature)
            return Result.unknown(
                mode="symbolic" if capability.support in {"symbolic", "none"} else "mixed",
                value=feature,
                justification=[
                    f"No theorem rule matched feature={feature!r} for representation={representation!r}.",
                    f"Capability fallback: {capability.support}.",
                ],
                proof_outline=[
                    "Add more tags or assumptions to the space metadata.",
                    "Register a suitable theorem rule for this representation class.",
                ],
                metadata={
                    "representation": representation,
                    "feature": feature,
                    "matched_rules": [],
                    "matched_profile_families": [],
                    "matched_profile_keys": [],
                    "matched_chapter_targets": [],
                },
            )

        if all(rule.conclusion for rule in matched):
            status = "true"
        elif all(not rule.conclusion for rule in matched):
            status = "false"
        else:
            status = "conditional"

        mode = "theorem"
        assumptions = unique_in_order(item for rule in matched for item in rule.assumptions)
        justification = unique_in_order(item for rule in matched for item in rule.justification)
        proof_outline = unique_in_order(item for rule in matched for item in rule.proof_outline)
        justification.insert(0, f"Matched theorem rules: {', '.join(rule.name for rule in matched)}.")

        value_payload = _merged_rule_value(matched, default=feature)
        matched_profile_families = unique_in_order(rule.profile_family for rule in matched if rule.profile_family)
        matched_profile_keys = unique_in_order(key for rule in matched for key in rule.profile_keys)
        matched_chapter_targets = unique_in_order(chapter for rule in matched for chapter in rule.chapter_targets)

        if status == "true":
            return Result.true(
                mode=mode,
                value=value_payload,
                assumptions=assumptions,
                justification=justification,
                proof_outline=proof_outline,
                metadata={
                    "representation": representation,
                    "feature": feature,
                    "matched_rules": [rule.name for rule in matched],
                    "tags": sorted(tags),
                    "matched_profile_families": matched_profile_families,
                    "matched_profile_keys": matched_profile_keys,
                    "matched_chapter_targets": matched_chapter_targets,
                },
            )

        if status == "false":
            return Result.false(
                mode=mode,
                value=value_payload,
                assumptions=assumptions,
                justification=justification,
                proof_outline=proof_outline,
                metadata={
                    "representation": representation,
                    "feature": feature,
                    "matched_rules": [rule.name for rule in matched],
                    "tags": sorted(tags),
                },
            )

        return Result.conditional(
            mode=mode,
            value=value_payload,
            assumptions=assumptions,
            justification=justification,
            proof_outline=proof_outline,
            metadata={
                "representation": representation,
                "feature": feature,
                "matched_rules": [rule.name for rule in matched],
                "tags": sorted(tags),
            },
        )




def _profile_alignment_rules() -> list[TheoremRule]:
    rules: list[TheoremRule] = []
    for alignment in get_promoted_theorem_profile_alignments():
        rules.append(
            TheoremRule(
                name=alignment.theorem_rule_name,
                feature=alignment.feature,
                result_value=alignment.result_value,
                requires_all=set(alignment.required_tags),
                assumptions=list(alignment.assumptions),
                justification=list(alignment.justification),
                proof_outline=list(alignment.proof_outline),
                profile_family=alignment.profile_family,
                profile_keys=alignment.profile_keys,
                chapter_targets=alignment.chapter_targets,
            )
        )
    return rules


DEFAULT_THEOREM_ENGINE = TheoremEngine(
    [
        TheoremRule(
            name="finite_spaces_are_compact",
            feature="compact",
            requires_all={"finite"},
            justification=["Every finite topological space is compact."],
            proof_outline=[
                "Take any open cover of the space.",
                "Because the carrier has only finitely many points, finitely many cover elements suffice.",
            ],
        ),
        TheoremRule(
            name="path_connected_implies_connected",
            feature="connected",
            requires_all={"path_connected"},
            justification=["Every path-connected space is connected."],
            proof_outline=[
                "Assume the space were disconnected.",
                "A path joining points from different components would contradict the disconnection.",
            ],
        ),
        TheoremRule(
            name="metric_spaces_are_hausdorff",
            feature="separation",
            requires_all={"metric"},
            assumptions=["Interpret the queried separation feature at least at the Hausdorff level."],
            justification=["Every metric space is Hausdorff."],
            proof_outline=[
                "Let x != y in the metric space.",
                "Choose disjoint open balls of radius d(x,y)/3 around x and y.",
            ],
        ),
        TheoremRule(
            name="metric_spaces_are_first_countable",
            feature="countability",
            requires_all={"metric"},
            assumptions=["Interpret the queried countability feature at least at the first-countable level."],
            justification=["Every metric space is first countable."],
            proof_outline=[
                "For each point x, the sequence of open balls B(x,1/n) forms a countable local base.",
            ],
        ),
        TheoremRule(
            name="second_countable_implies_separable_and_lindelof",
            feature="countability",
            requires_all={"second_countable"},
            assumptions=[
                "Interpret the query as asking for a standard countability consequence such as separability or Lindelöfness."
            ],
            justification=["Every second-countable space is separable and Lindelöf."],
            proof_outline=[
                "Choose one point from each nonempty basic open set to obtain a countable dense set.",
                "Use a countable base to thin any open cover to a countable subcover.",
            ],
        ),
        TheoremRule(
            name="closed_subspace_of_compact_is_compact",
            feature="compact",
            requires_all={"closed_subspace", "ambient_compact"},
            justification=["A closed subspace of a compact space is compact."],
            proof_outline=[
                "Lift an open cover of the subspace to an open cover of the ambient compact space.",
                "Use compactness of the ambient space and closedness of the subspace.",
            ],
        ),
        TheoremRule(
            name="continuous_image_of_compact_is_compact",
            feature="compact",
            requires_all={"continuous_image", "domain_compact"},
            justification=["The continuous image of a compact space is compact."],
            proof_outline=[
                "Pull back an open cover of the image along the continuous map.",
                "Use compactness of the domain and push the finite subcover forward.",
            ],
        ),
        TheoremRule(
            name="metric_spaces_have_countable_character",
            feature="character",
            result_value="aleph_0",
            requires_all={"metric"},
            justification=["Every metric space has countable local character at each point."],
            proof_outline=[
                "For each point x, the balls B(x,1/n) form a countable local base.",
                "Hence the global character is at most countable.",
            ],
        ),
        TheoremRule(
            name="second_countable_implies_countable_weight",
            feature="weight",
            result_value="aleph_0",
            requires_all={"second_countable"},
            justification=["A second-countable space has a countable base, so its weight is countable."],
            proof_outline=["Take the given countable base as a witness for the weight bound."],
        ),
        TheoremRule(
            name="second_countable_implies_countable_density",
            feature="density",
            result_value="aleph_0",
            requires_all={"second_countable"},
            justification=["Every second-countable space is separable."],
            proof_outline=["Choose one point from each nonempty basis element."],
        ),
        TheoremRule(
            name="separable_tag_implies_countable_density",
            feature="density",
            result_value="aleph_0",
            requires_all={"separable"},
            justification=["A separable space has a countable dense subset."],
            proof_outline=["Interpret the separable tag as providing a countable dense witness."],
        ),
        TheoremRule(
            name="second_countable_implies_countable_lindelof_number",
            feature="lindelof_number",
            result_value="aleph_0",
            requires_all={"second_countable"},
            justification=["Every second-countable space is Lindelöf, so the Lindelöf number is countable."],
            proof_outline=["Use a countable base to reduce each open cover to a countable subcover."],
        ),
    ] + _profile_alignment_rules()
)


def theorem_result(statement: str, assumptions: list[str] | None = None) -> Result:
    """Backward-compatible helper kept from the v0.5 scaffold."""
    return Result.true(
        mode="theorem",
        value=statement,
        assumptions=assumptions or [],
        justification=["Derived from a theorem-level helper result."],
        proof_outline=["Use the registered theorem rules for richer inference traces when available."],
    )


def infer_feature(feature: str, obj: Any) -> Result:
    """Convenience wrapper around the default theorem engine."""
    return DEFAULT_THEOREM_ENGINE.infer(feature, obj)



def extract_tags(obj: Any) -> set[str]:
    tags: set[str] = set()

    if hasattr(obj, "tags"):
        raw = getattr(obj, "tags")
        if raw is not None:
            tags.update(str(tag).strip().lower() for tag in raw if str(tag).strip())

    metadata = getattr(obj, "metadata", None)
    if isinstance(metadata, dict):
        meta_tags = metadata.get("tags", [])
        tags.update(str(tag).strip().lower() for tag in meta_tags if str(tag).strip())
        if metadata.get("representation"):
            tags.add(str(metadata["representation"]).strip().lower())

    if isinstance(obj, dict):
        raw_tags = obj.get("tags", [])
        tags.update(str(tag).strip().lower() for tag in raw_tags if str(tag).strip())
        if obj.get("representation"):
            tags.add(str(obj["representation"]).strip().lower())

    if hasattr(obj, "is_finite"):
        try:
            if obj.is_finite():
                tags.add("finite")
        except Exception:
            pass

    return tags



def extract_representation(obj: Any) -> str:
    metadata = getattr(obj, "metadata", None)
    if isinstance(metadata, dict) and metadata.get("representation"):
        return str(metadata["representation"])
    if isinstance(obj, dict) and obj.get("representation"):
        return str(obj["representation"])
    if "finite" in extract_tags(obj):
        return "finite"
    return "symbolic_general"



def unique_in_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        text = str(item).strip()
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def _merged_rule_value(rules: Iterable[TheoremRule], default: Any) -> Any:
    values = [rule.result_value for rule in rules if rule.result_value is not None]
    if not values:
        return default
    first = values[0]
    if all(value == first for value in values):
        return first
    return values


__all__ = [
    "TheoremRule",
    "TheoremEngine",
    "DEFAULT_THEOREM_ENGINE",
    "theorem_result",
    "infer_feature",
    "extract_tags",
    "extract_representation",
    "unique_in_order",
]
