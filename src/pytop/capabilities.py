"""Capability descriptions for supported space classes and reasoning modes.

The package distinguishes exact support, theorem-based support, symbolic support,
and mixed support. This module provides a small registry that can be queried by
representation class and feature name.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

SUPPORT_LEVELS = {"exact", "theorem", "symbolic", "mixed", "none"}


@dataclass(slots=True)
class FeatureCapability:
    feature: str
    support: str
    notes: str = ""

    def __post_init__(self) -> None:
        if self.support not in SUPPORT_LEVELS:
            raise ValueError(
                f"Invalid support level {self.support!r}. Expected one of {sorted(SUPPORT_LEVELS)}."
            )


@dataclass(slots=True)
class CapabilityProfile:
    representation: str
    summary_support: str
    notes: str = ""
    features: dict[str, FeatureCapability] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.summary_support not in SUPPORT_LEVELS:
            raise ValueError(
                f"Invalid summary support {self.summary_support!r}. Expected one of {sorted(SUPPORT_LEVELS)}."
            )

    def support_for(self, feature: str) -> FeatureCapability:
        feature = normalize_feature_name(feature)
        if feature in self.features:
            return self.features[feature]
        return FeatureCapability(
            feature=feature,
            support=self.summary_support,
            notes="No feature-specific entry. Falling back to representation summary support.",
        )

    def explain(self, feature: str) -> str:
        entry = self.support_for(feature)
        return f"{self.representation}: {entry.feature} -> {entry.support}. {entry.notes}".strip()


class CapabilityRegistry:
    def __init__(self, profiles: Iterable[CapabilityProfile] = ()) -> None:
        self._profiles: dict[str, CapabilityProfile] = {
            profile.representation: profile for profile in profiles
        }

    def register(self, profile: CapabilityProfile) -> None:
        self._profiles[profile.representation] = profile

    def get(self, representation: str) -> CapabilityProfile:
        try:
            return self._profiles[representation]
        except KeyError as exc:
            raise KeyError(f"Unknown representation {representation!r}.") from exc

    def support_for(self, representation: str, feature: str) -> FeatureCapability:
        return self.get(representation).support_for(feature)

    def explain(self, representation: str, feature: str) -> str:
        return self.get(representation).explain(feature)

    def as_dict(self) -> dict[str, dict[str, str]]:
        return {
            representation: {
                feature: capability.support
                for feature, capability in profile.features.items()
            }
            for representation, profile in self._profiles.items()
        }


DEFAULT_REGISTRY = CapabilityRegistry(
    [
        CapabilityProfile(
            representation="finite",
            summary_support="exact",
            notes="Finite spaces are the strongest exact-computation layer in the project.",
            features={
                "compact": FeatureCapability("compact", "exact", "Every finite topological space is compact; feature-level checks may also be computed directly."),
                "countably_compact": FeatureCapability("countably_compact", "exact", "Finite spaces are automatically countably compact."),
                "sequentially_compact": FeatureCapability("sequentially_compact", "exact", "Finite spaces are sequentially compact."),
                "lindelof": FeatureCapability("lindelof", "exact", "Finite spaces are Lindelöf."),
                "connected": FeatureCapability("connected", "exact", "Finite connectedness is decidable from explicit topology data when available."),
                "path_connected": FeatureCapability("path_connected", "exact", "Finite path-connectedness support may depend on additional path data; tags remain exact if supplied."),
                "t0": FeatureCapability("t0", "exact", "T0 can be checked from explicit finite topology data."),
                "t1": FeatureCapability("t1", "exact", "T1 can be checked from explicit finite topology data."),
                "hausdorff": FeatureCapability("hausdorff", "exact", "Hausdorffness can be checked from explicit finite topology data."),
                "regular": FeatureCapability("regular", "exact", "Regularity can be checked by separating points from closed sets in an explicit finite topology."),
                "t3": FeatureCapability("t3", "exact", "T3 is checked as T1 plus regularity in explicit finite topology data."),
                "completely_regular": FeatureCapability("completely_regular", "mixed", "Finite T1 spaces are discrete and hence completely regular; non-T1 cases are kept conservative."),
                "tychonoff": FeatureCapability("tychonoff", "exact", "Finite Tychonoff status is checked through the finite T1/discrete route."),
                "normal": FeatureCapability("normal", "exact", "Normality can be checked by separating disjoint closed sets in an explicit finite topology."),
                "t4": FeatureCapability("t4", "exact", "T4 is checked as T1 plus normality in explicit finite topology data."),
                "first_countable": FeatureCapability("first_countable", "exact", "Finite spaces are first countable."),
                "second_countable": FeatureCapability("second_countable", "exact", "Finite spaces are second countable."),
                "separable": FeatureCapability("separable", "exact", "Finite spaces are separable."),
                "invariants": FeatureCapability("invariants", "exact", "Basic invariants can be computed from explicit finite representations."),
                "weight": FeatureCapability("weight", "exact", "Weight is exactly computable from an explicit finite topology."),
                "density": FeatureCapability("density", "exact", "Density is exactly computable from an explicit finite topology."),
                "character": FeatureCapability("character", "exact", "Character is exactly computable from an explicit finite topology."),
                "lindelof_number": FeatureCapability("lindelof_number", "exact", "The Lindelöf number is exactly computable from an explicit finite topology."),
                "cellularity": FeatureCapability("cellularity", "exact", "Cellularity is exactly computable from an explicit finite topology."),
            },
        ),
        CapabilityProfile(
            representation="infinite_discrete",
            summary_support="mixed",
            notes="Infinite discrete spaces admit exact family-level answers, with countability-sensitive distinctions.",
            features={
                "compact": FeatureCapability("compact", "exact", "Infinite discrete spaces are not compact."),
                "connected": FeatureCapability("connected", "exact", "Infinite discrete spaces are disconnected."),
                "path_connected": FeatureCapability("path_connected", "exact", "Infinite discrete spaces are not path connected unless they have at most one point."),
                "t0": FeatureCapability("t0", "exact", "Discrete spaces are T0."),
                "t1": FeatureCapability("t1", "exact", "Discrete spaces are T1."),
                "hausdorff": FeatureCapability("hausdorff", "exact", "Discrete spaces are Hausdorff."),
                "regular": FeatureCapability("regular", "exact", "Discrete spaces are regular."),
                "t3": FeatureCapability("t3", "exact", "Discrete spaces are T3."),
                "completely_regular": FeatureCapability("completely_regular", "exact", "Discrete spaces are completely regular."),
                "tychonoff": FeatureCapability("tychonoff", "exact", "Discrete spaces are Tychonoff."),
                "normal": FeatureCapability("normal", "exact", "Discrete spaces are normal."),
                "t4": FeatureCapability("t4", "exact", "Discrete spaces are T4."),
                "first_countable": FeatureCapability("first_countable", "exact", "Discrete spaces are first countable."),
                "second_countable": FeatureCapability("second_countable", "mixed", "Second countability is exact once countability of the carrier is known."),
                "separable": FeatureCapability("separable", "mixed", "Separability is exact once countability of the carrier is known."),
                "lindelof": FeatureCapability("lindelof", "mixed", "Lindelöfness is exact once countability of the carrier is known."),
            },
        ),
        CapabilityProfile(
            representation="infinite_indiscrete",
            summary_support="exact",
            notes="Infinite indiscrete spaces have a simple exact family-level theory.",
            features={
                "compact": FeatureCapability("compact", "exact", "Indiscrete spaces are compact."),
                "connected": FeatureCapability("connected", "exact", "Indiscrete spaces are connected."),
                "path_connected": FeatureCapability("path_connected", "exact", "Indiscrete spaces are path connected whenever they are nonempty."),
                "t0": FeatureCapability("t0", "exact", "Infinite indiscrete spaces fail T0."),
                "t1": FeatureCapability("t1", "exact", "Infinite indiscrete spaces fail T1."),
                "hausdorff": FeatureCapability("hausdorff", "exact", "Infinite indiscrete spaces are not Hausdorff."),
                "regular": FeatureCapability("regular", "exact", "Indiscrete spaces satisfy the non-T1 regular condition vacuously."),
                "t3": FeatureCapability("t3", "exact", "Infinite indiscrete spaces fail T3 because they fail T1."),
                "completely_regular": FeatureCapability("completely_regular", "symbolic", "Complete regularity is not used as a positive Tychonoff conclusion without T1."),
                "tychonoff": FeatureCapability("tychonoff", "exact", "Infinite indiscrete spaces fail Tychonoff because they fail T1."),
                "normal": FeatureCapability("normal", "exact", "Indiscrete spaces satisfy the non-T1 normal condition vacuously."),
                "t4": FeatureCapability("t4", "exact", "Infinite indiscrete spaces fail T4 because they fail T1."),
                "first_countable": FeatureCapability("first_countable", "exact", "The one-set neighbourhood system gives first countability."),
                "second_countable": FeatureCapability("second_countable", "exact", "The topology has a finite base."),
                "separable": FeatureCapability("separable", "exact", "Any nonempty countable subset is dense; in standard examples a singleton already suffices."),
                "lindelof": FeatureCapability("lindelof", "exact", "Compactness implies Lindelöfness."),
            },
        ),
        CapabilityProfile(
            representation="infinite_cofinite",
            summary_support="mixed",
            notes="Cofinite spaces have several exact family-level properties, with countability-sensitive local behaviour.",
            features={
                "compact": FeatureCapability("compact", "exact", "Every cofinite space is compact."),
                "connected": FeatureCapability("connected", "exact", "Infinite cofinite spaces are connected."),
                "t0": FeatureCapability("t0", "exact", "Infinite cofinite spaces are T0."),
                "t1": FeatureCapability("t1", "exact", "Infinite cofinite spaces are T1."),
                "hausdorff": FeatureCapability("hausdorff", "exact", "Infinite cofinite spaces are not Hausdorff."),
                "regular": FeatureCapability("regular", "exact", "Infinite cofinite T1 spaces are not regular because T1 regularity would imply Hausdorffness."),
                "t3": FeatureCapability("t3", "exact", "Infinite cofinite spaces are not T3."),
                "completely_regular": FeatureCapability("completely_regular", "exact", "Infinite cofinite T1 spaces are not completely regular/Tychonoff."),
                "tychonoff": FeatureCapability("tychonoff", "exact", "Infinite cofinite spaces are not Tychonoff."),
                "normal": FeatureCapability("normal", "exact", "Infinite cofinite T1 spaces are not normal because normal T1 implies Hausdorffness."),
                "t4": FeatureCapability("t4", "exact", "Infinite cofinite spaces are not T4."),
                "first_countable": FeatureCapability("first_countable", "mixed", "Exact once countability of the carrier is known."),
                "second_countable": FeatureCapability("second_countable", "mixed", "Exact once countability of the carrier is known."),
                "separable": FeatureCapability("separable", "mixed", "Supported exactly for standard carriers with known countable dense subsets."),
            },
        ),
        CapabilityProfile(
            representation="infinite_cocountable",
            summary_support="mixed",
            notes="Cocountable spaces are handled exactly for the standard uncountable-family semantics used by the examples layer.",
            features={
                "compact": FeatureCapability("compact", "exact", "Standard uncountable cocountable spaces are not compact."),
                "connected": FeatureCapability("connected", "exact", "Standard uncountable cocountable spaces are connected."),
                "t0": FeatureCapability("t0", "exact", "Cocountable spaces are T0."),
                "t1": FeatureCapability("t1", "exact", "Cocountable spaces are T1."),
                "hausdorff": FeatureCapability("hausdorff", "exact", "Standard uncountable cocountable spaces are not Hausdorff."),
                "regular": FeatureCapability("regular", "exact", "Standard uncountable cocountable T1 spaces are not regular because T1 regularity would imply Hausdorffness."),
                "t3": FeatureCapability("t3", "exact", "Standard uncountable cocountable spaces are not T3."),
                "completely_regular": FeatureCapability("completely_regular", "exact", "Standard uncountable cocountable T1 spaces are not completely regular/Tychonoff."),
                "tychonoff": FeatureCapability("tychonoff", "exact", "Standard uncountable cocountable spaces are not Tychonoff."),
                "normal": FeatureCapability("normal", "exact", "Standard uncountable cocountable T1 spaces are not normal because normal T1 implies Hausdorffness."),
                "t4": FeatureCapability("t4", "exact", "Standard uncountable cocountable spaces are not T4."),
                "first_countable": FeatureCapability("first_countable", "exact", "Standard uncountable cocountable spaces are not first countable."),
                "second_countable": FeatureCapability("second_countable", "exact", "Standard uncountable cocountable spaces are not second countable."),
                "separable": FeatureCapability("separable", "exact", "Standard uncountable cocountable spaces are not separable."),
                "lindelof": FeatureCapability("lindelof", "exact", "Standard uncountable cocountable spaces are Lindelöf."),
            },
        ),
        CapabilityProfile(
            representation="infinite_metric",
            summary_support="theorem",
            notes="Infinite metric spaces are handled by a mix of direct structure and theorem-level reasoning.",
            features={
                "compact": FeatureCapability("compact", "theorem", "Compactness is often supported through metric-space theorems or supplied hypotheses."),
                "connected": FeatureCapability("connected", "theorem", "Connectedness and path-connectedness relations may be theorem-backed."),
                "path_connected": FeatureCapability("path_connected", "theorem", "Path-connectedness may be tag-driven or theorem-backed in metric settings."),
                "hausdorff": FeatureCapability("hausdorff", "theorem", "Every metric space is Hausdorff."),
                "regular": FeatureCapability("regular", "theorem", "Every metric space is regular."),
                "t3": FeatureCapability("t3", "theorem", "Every metric space is T3."),
                "completely_regular": FeatureCapability("completely_regular", "theorem", "Distance-to-closed-set functions make metric spaces completely regular."),
                "tychonoff": FeatureCapability("tychonoff", "theorem", "Every metric space is Tychonoff."),
                "normal": FeatureCapability("normal", "theorem", "Every metric space is normal."),
                "t4": FeatureCapability("t4", "theorem", "Every metric space is T4."),
                "t1": FeatureCapability("t1", "theorem", "Every metric space is T1 through Hausdorffness."),
                "t0": FeatureCapability("t0", "theorem", "Every metric space is T0 through T1."),
                "first_countable": FeatureCapability("first_countable", "theorem", "Every metric space is first countable."),
                "second_countable": FeatureCapability("second_countable", "theorem", "Second countability usually needs extra assumptions such as separability or explicit basis data."),
                "separable": FeatureCapability("separable", "theorem", "Separable metric spaces may be inferred from stronger hypotheses such as second countability tags."),
                "lindelof": FeatureCapability("lindelof", "theorem", "Lindelöfness may be theorem-backed when second countability is known."),
                "invariants": FeatureCapability("invariants", "symbolic", "Invariant support may be partial or assumption-sensitive in the infinite metric setting."),
                "weight": FeatureCapability("weight", "theorem", "Weight becomes theorem-backed when second countability or explicit countable basis data is available."),
                "density": FeatureCapability("density", "theorem", "Density becomes theorem-backed when separability or second countability is known."),
                "character": FeatureCapability("character", "theorem", "Every metric space has countable character."),
                "lindelof_number": FeatureCapability("lindelof_number", "theorem", "The Lindelöf number becomes theorem-backed when second countability is known."),
                "cellularity": FeatureCapability("cellularity", "symbolic", "Cellularity usually needs additional structure or assumptions in infinite metric settings."),
            },
        ),
        CapabilityProfile(
            representation="basis_defined",
            summary_support="mixed",
            notes="Basis-defined spaces may permit exact local checks and theorem-backed global deductions.",
            features={
                "compact": FeatureCapability("compact", "symbolic", "Compactness usually needs extra hypotheses or theorem support."),
                "connected": FeatureCapability("connected", "mixed", "Connectedness may be detected from tags or from explicit clopen data."),
                "hausdorff": FeatureCapability("hausdorff", "mixed", "Some separation checks may be structural; others remain theorem-backed."),
                "regular": FeatureCapability("regular", "symbolic", "Regularity usually needs explicit base/closed-set data or hypotheses."),
                "t3": FeatureCapability("t3", "symbolic", "T3 usually needs T1 plus regularity hypotheses."),
                "completely_regular": FeatureCapability("completely_regular", "symbolic", "Complete regularity usually needs functional separation data or hypotheses."),
                "tychonoff": FeatureCapability("tychonoff", "symbolic", "Tychonoff status usually needs T1 plus complete regularity hypotheses."),
                "normal": FeatureCapability("normal", "symbolic", "Normality usually needs closed-set separation data or hypotheses."),
                "t4": FeatureCapability("t4", "symbolic", "T4 usually needs T1 plus normality hypotheses."),
                "t1": FeatureCapability("t1", "mixed", "T1 may be read from basis behavior in some structured settings."),
                "t0": FeatureCapability("t0", "mixed", "T0 may be read from basis behavior in some structured settings."),
                "first_countable": FeatureCapability("first_countable", "mixed", "Local basis data may give direct first-countability information."),
                "second_countable": FeatureCapability("second_countable", "mixed", "Basis size may directly determine second countability."),
                "separable": FeatureCapability("separable", "symbolic", "Separability generally needs additional information."),
                "lindelof": FeatureCapability("lindelof", "symbolic", "Lindelöfness usually needs extra hypotheses or theorem support."),
                "weight": FeatureCapability("weight", "mixed", "Weight may be read exactly from explicit basis-size metadata."),
                "density": FeatureCapability("density", "symbolic", "Density needs explicit dense-set data or theorem support."),
                "character": FeatureCapability("character", "mixed", "Character may be read from local-basis metadata."),
                "lindelof_number": FeatureCapability("lindelof_number", "symbolic", "Lindelöf number usually needs extra structure or metadata."),
                "cellularity": FeatureCapability("cellularity", "symbolic", "Cellularity usually needs explicit open-set or basis information."),
            },
        ),
        CapabilityProfile(
            representation="symbolic_general",
            summary_support="symbolic",
            notes="General symbolic spaces support traceable reasoning but not universal decision procedures.",
            features={
                "compact": FeatureCapability("compact", "symbolic", "Requires theorem registration or explicit assumptions."),
                "countably_compact": FeatureCapability("countably_compact", "symbolic", "Requires explicit assumptions or theorem support."),
                "sequentially_compact": FeatureCapability("sequentially_compact", "symbolic", "Requires explicit assumptions or theorem support."),
                "connected": FeatureCapability("connected", "symbolic", "Requires theorem registration or explicit assumptions."),
                "path_connected": FeatureCapability("path_connected", "symbolic", "Requires theorem registration or explicit assumptions."),
                "hausdorff": FeatureCapability("hausdorff", "symbolic", "Requires theorem registration or explicit assumptions."),
                "regular": FeatureCapability("regular", "symbolic", "Requires explicit assumptions or finite closed-set data."),
                "t3": FeatureCapability("t3", "symbolic", "Requires T1 plus regularity assumptions or exact finite data."),
                "completely_regular": FeatureCapability("completely_regular", "symbolic", "Requires functional separation assumptions or theorem support."),
                "tychonoff": FeatureCapability("tychonoff", "symbolic", "Requires T1 plus complete regularity assumptions or theorem support."),
                "normal": FeatureCapability("normal", "symbolic", "Requires closed-set separation assumptions or exact finite data."),
                "t4": FeatureCapability("t4", "symbolic", "Requires T1 plus normality assumptions or theorem support."),
                "t1": FeatureCapability("t1", "symbolic", "Requires theorem registration or explicit assumptions."),
                "t0": FeatureCapability("t0", "symbolic", "Requires theorem registration or explicit assumptions."),
                "first_countable": FeatureCapability("first_countable", "symbolic", "Requires theorem registration or explicit assumptions."),
                "second_countable": FeatureCapability("second_countable", "symbolic", "Requires theorem registration or explicit assumptions."),
                "separable": FeatureCapability("separable", "symbolic", "Requires theorem registration or explicit assumptions."),
                "lindelof": FeatureCapability("lindelof", "symbolic", "Requires theorem registration or explicit assumptions."),
                "invariants": FeatureCapability("invariants", "symbolic", "Invariant output is generally explanatory rather than decision-complete."),
                "weight": FeatureCapability("weight", "symbolic", "Weight needs explicit basis data or theorem support."),
                "density": FeatureCapability("density", "symbolic", "Density needs explicit dense-set data or theorem support."),
                "character": FeatureCapability("character", "symbolic", "Character needs explicit local-base data or theorem support."),
                "lindelof_number": FeatureCapability("lindelof_number", "symbolic", "Lindelöf number needs explicit data or theorem support."),
                "cellularity": FeatureCapability("cellularity", "symbolic", "Cellularity needs explicit structural data."),
            },
        ),
    ]
)


def normalize_feature_name(feature: str) -> str:
    feature = feature.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "compactness": "compact",
        "connectedness": "connected",
        "pathconnected": "path_connected",
        "locallyconnected": "locally_connected",
        "separation_axioms": "hausdorff",
        "countability_axioms": "first_countable",
        "cardinal_functions": "invariants",
        "topological_invariants": "invariants",
        "w": "weight",
        "d": "density",
        "chi": "character",
        "lindelofnumber": "lindelof_number",
        "t2": "hausdorff",
        "kolmogorov": "t0",
    }
    return aliases.get(feature, feature)


def explain_capability(representation: str, feature: str) -> str:
    return DEFAULT_REGISTRY.explain(representation, feature)


__all__ = [
    "SUPPORT_LEVELS",
    "FeatureCapability",
    "CapabilityProfile",
    "CapabilityRegistry",
    "DEFAULT_REGISTRY",
    "normalize_feature_name",
    "explain_capability",
]
