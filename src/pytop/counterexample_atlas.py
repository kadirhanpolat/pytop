"""Basic counterexample atlas for the topology book ecosystem.

This module provides the v0.1.49 Cilt II corridor: a structured, queryable
atlas of canonical counterexamples.  Each entry corresponds to a known
failure of a topological property (or a failure of preservation under a
standard construction) that undergraduate students routinely need.

The atlas is organized into two layers:

  1. Separation-axiom atlas  (CE-S-01 ... CE-S-06)
     Canonical witnesses for the T0/T1/T2 implication chain failures.
     (These first appeared as CA-1...CA-6 in v0.1.42; the atlas is here
     given stable identifiers and structured Result objects.)

  2. Preservation-failure atlas  (CE-P-01 ... CE-P-10)
     One canonical counterexample for each "H" (not-preserved) cell in
     the v0.1.48 basic preservation table.

Each entry returns a Result with:
  - value: the atlas entry identifier (e.g. "CE-S-01")
  - justification: what the counterexample demonstrates
  - metadata: space description, property, construction (where relevant),
    and a classroom-safe description string

Roadmap reference:
  v0.1.49 — Organize a basic counterexample atlas (Cilt II, Chapter 10/11)
"""

from __future__ import annotations

from typing import Any

from .result import Result


# ---------------------------------------------------------------------------
# Atlas data
# ---------------------------------------------------------------------------

_ATLAS: dict[str, dict[str, Any]] = {

    # ── Separation-axiom atlas ───────────────────────────────────────────────

    "CE-S-01": {
        "layer": "separation",
        "space": "Indiscrete space on {a, b}",
        "property_failed": "t0",
        "construction": None,
        "statement": "An indiscrete space on more than one point fails T0: no open set separates any two points.",
        "counterexample_class": "not_t0",
        "chapter": 11,
    },
    "CE-S-02": {
        "layer": "separation",
        "space": "Sierpiński space {0, 1} with topology {∅, {1}, {0,1}}",
        "property_failed": "t1",
        "construction": None,
        "statement": "The Sierpiński space is T0 but not T1: the point 0 cannot be separated from 1 by an open set containing 0 but not 1.",
        "counterexample_class": "t0_not_t1",
        "chapter": 11,
    },
    "CE-S-03": {
        "layer": "separation",
        "space": "Cofinite topology on an infinite set",
        "property_failed": "hausdorff",
        "construction": None,
        "statement": "The cofinite topology on an infinite set is T1 but not Hausdorff: any two non-empty open sets intersect.",
        "counterexample_class": "t1_not_hausdorff",
        "chapter": 11,
    },
    "CE-S-04": {
        "layer": "separation",
        "space": "Cocountable topology on an uncountable set",
        "property_failed": "hausdorff",
        "construction": None,
        "statement": "The cocountable topology is T1 but not Hausdorff.",
        "counterexample_class": "t1_not_hausdorff",
        "chapter": 11,
    },
    "CE-S-05": {
        "layer": "separation",
        "space": "Finite T1 space with more than one point",
        "property_failed": "non_discrete_t1",
        "construction": None,
        "statement": "A finite T1 space must be discrete; a finite non-discrete space cannot be T1.",
        "counterexample_class": "finite_t1_forces_discrete",
        "chapter": 11,
    },
    "CE-S-06": {
        "layer": "separation",
        "space": "Metric space (e.g. R with standard metric)",
        "property_failed": None,
        "construction": None,
        "statement": "Every metric space is Hausdorff. This positive example anchors the implication chain: metric => T2 => T1 => T0.",
        "counterexample_class": "metric_hausdorff_anchor",
        "chapter": 11,
    },

    # ── Preservation-failure atlas ───────────────────────────────────────────

    "CE-P-01": {
        "layer": "preservation",
        "space": "R (real line) with standard topology",
        "property_failed": "connectedness",
        "construction": "subspace",
        "statement": "R is connected but (0,1)∪(2,3) is a disconnected open subspace.",
        "counterexample_class": "connectedness_not_subspace",
        "chapter": 13,
    },
    "CE-P-02": {
        "layer": "preservation",
        "space": "[0,1] with subspace (0,1)",
        "property_failed": "compactness",
        "construction": "subspace",
        "statement": "[0,1] is compact but (0,1) is an open subspace that is not compact.",
        "counterexample_class": "compactness_not_subspace",
        "chapter": 14,
    },
    "CE-P-03": {
        "layer": "preservation",
        "space": "R with identification of two points",
        "property_failed": "hausdorff",
        "construction": "quotient",
        "statement": "Identifying two distinct points in R (Hausdorff) can produce a non-Hausdorff quotient.",
        "counterexample_class": "hausdorff_not_quotient",
        "chapter": 11,
    },
    "CE-P-04": {
        "layer": "preservation",
        "space": "Continuous surjection from a Hausdorff space onto an indiscrete space",
        "property_failed": "hausdorff",
        "construction": "continuous_image",
        "statement": "A continuous surjection can collapse Hausdorff separation: the image may be indiscrete (not Hausdorff).",
        "counterexample_class": "hausdorff_not_continuous_image",
        "chapter": 11,
    },
    "CE-P-05": {
        "layer": "preservation",
        "space": "T1 space with identification of a sequence to its limit",
        "property_failed": "t1",
        "construction": "quotient",
        "statement": "A quotient of a T1 space can fail T1 if the equivalence relation is not compatible with the T1 structure.",
        "counterexample_class": "t1_not_quotient",
        "chapter": 11,
    },
    "CE-P-06": {
        "layer": "preservation",
        "space": "Continuous surjection onto an indiscrete space",
        "property_failed": "t1",
        "construction": "continuous_image",
        "statement": "The continuous image of a T1 space need not be T1: a surjection onto a two-point indiscrete space provides a witness.",
        "counterexample_class": "t1_not_continuous_image",
        "chapter": 11,
    },
    "CE-P-07": {
        "layer": "preservation",
        "space": "R (second countable) with large quotient",
        "property_failed": "second_countability",
        "construction": "quotient",
        "statement": "A quotient of a second-countable space can fail second countability when the equivalence classes are too numerous.",
        "counterexample_class": "second_countability_not_quotient",
        "chapter": 12,
    },
    "CE-P-08": {
        "layer": "preservation",
        "space": "Continuous surjection onto an uncountable discrete space",
        "property_failed": "second_countability",
        "construction": "continuous_image",
        "statement": "The continuous image of a second-countable space need not be second countable.",
        "counterexample_class": "second_countability_not_continuous_image",
        "chapter": 12,
    },
    "CE-P-09": {
        "layer": "preservation",
        "space": "Product of uncountably many second-countable spaces",
        "property_failed": "second_countability",
        "construction": "countable_product",
        "statement": "An uncountable product of second-countable spaces fails second countability; the countable case is preserved.",
        "counterexample_class": "second_countability_uncountable_product",
        "chapter": 12,
    },
    "CE-P-10": {
        "layer": "preservation",
        "space": "Topologist's sine curve",
        "property_failed": "path_connectedness",
        "construction": "subspace",
        "statement": "The topologist's sine curve is connected but not path-connected, showing connectedness does not imply path-connectedness.",
        "counterexample_class": "connected_not_path_connected",
        "chapter": 13,
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def counterexample_lookup(atlas_id: str) -> Result:
    """Return the structured atlas entry for the given identifier.

    Parameters
    ----------
    atlas_id:
        An atlas identifier such as 'CE-S-01' or 'CE-P-03'.
    """
    key = str(atlas_id).strip().upper()
    if key not in _ATLAS:
        return Result.unknown(
            mode="symbolic",
            value="counterexample_lookup",
            justification=[
                f"No atlas entry for {atlas_id!r}. "
                f"Available IDs: {', '.join(sorted(_ATLAS))}."
            ],
            metadata={"operator": "counterexample_lookup", "atlas_id": atlas_id},
        )
    entry = _ATLAS[key]
    return Result.true(
        mode="exact",
        value=key,
        justification=[entry["statement"]],
        metadata={
            "operator": "counterexample_lookup",
            "atlas_id": key,
            "layer": entry["layer"],
            "space": entry["space"],
            "property_failed": entry["property_failed"],
            "construction": entry["construction"],
            "counterexample_class": entry["counterexample_class"],
            "chapter": entry["chapter"],
            "cilt_ii_corridor": "basic-counterexample-atlas",
            "v0_1_49_corridor_record": True,
        },
    )


def counterexample_atlas_by_layer(layer: str) -> Result:
    """Return all atlas entries for a given layer ('separation' or 'preservation')."""
    layer_norm = str(layer).strip().lower()
    if layer_norm not in {"separation", "preservation"}:
        return Result.unknown(
            mode="symbolic",
            value="counterexample_atlas_by_layer",
            justification=["layer must be 'separation' or 'preservation'."],
            metadata={"operator": "counterexample_atlas_by_layer", "layer": layer},
        )
    entries = {k: v["statement"] for k, v in _ATLAS.items() if v["layer"] == layer_norm}
    return Result.true(
        mode="exact",
        value=entries,
        justification=[f"All atlas entries for layer '{layer_norm}'."],
        metadata={
            "operator": "counterexample_atlas_by_layer",
            "layer": layer_norm,
            "entry_count": len(entries),
            "cilt_ii_corridor": "basic-counterexample-atlas",
            "v0_1_49_corridor_record": True,
        },
    )


def counterexample_atlas_by_property(property_name: str) -> Result:
    """Return all atlas entries where the given property fails."""
    prop = str(property_name).strip().lower().replace("-", "_").replace(" ", "_")
    entries = {k: v["statement"] for k, v in _ATLAS.items()
               if v.get("property_failed") == prop}
    if not entries:
        return Result.unknown(
            mode="symbolic",
            value="counterexample_atlas_by_property",
            justification=[f"No atlas entries found for property {property_name!r}."],
            metadata={"operator": "counterexample_atlas_by_property", "property": prop},
        )
    return Result.true(
        mode="exact",
        value=entries,
        justification=[f"All atlas entries where '{prop}' fails."],
        metadata={
            "operator": "counterexample_atlas_by_property",
            "property": prop,
            "entry_count": len(entries),
            "cilt_ii_corridor": "basic-counterexample-atlas",
            "v0_1_49_corridor_record": True,
        },
    )


def counterexample_atlas_by_construction(construction: str) -> Result:
    """Return all preservation-failure entries for the given construction."""
    cons = str(construction).strip().lower().replace("-", "_").replace(" ", "_")
    entries = {k: v["statement"] for k, v in _ATLAS.items()
               if v.get("construction") == cons}
    if not entries:
        return Result.unknown(
            mode="symbolic",
            value="counterexample_atlas_by_construction",
            justification=[f"No atlas entries found for construction {construction!r}."],
            metadata={"operator": "counterexample_atlas_by_construction", "construction": cons},
        )
    return Result.true(
        mode="exact",
        value=entries,
        justification=[f"All atlas entries for construction '{cons}'."],
        metadata={
            "operator": "counterexample_atlas_by_construction",
            "construction": cons,
            "entry_count": len(entries),
            "cilt_ii_corridor": "basic-counterexample-atlas",
            "v0_1_49_corridor_record": True,
        },
    )


def analyze_counterexample_atlas(
    atlas_id: str | None = None,
    layer: str | None = None,
    property_name: str | None = None,
    construction: str | None = None,
) -> Result:
    """Corridor entry-point for v0.1.49.

    - With atlas_id: single entry lookup.
    - With layer: all entries for that layer.
    - With property_name: all entries where that property fails.
    - With construction: all preservation-failure entries for that construction.
    - With none: full atlas summary (IDs and statements).
    """
    if atlas_id is not None:
        return counterexample_lookup(atlas_id)
    if layer is not None:
        return counterexample_atlas_by_layer(layer)
    if property_name is not None:
        return counterexample_atlas_by_property(property_name)
    if construction is not None:
        return counterexample_atlas_by_construction(construction)

    # Full summary
    summary = {k: v["statement"] for k, v in _ATLAS.items()}
    return Result.true(
        mode="exact",
        value=summary,
        justification=["Full basic counterexample atlas: separation + preservation layers."],
        metadata={
            "operator": "analyze_counterexample_atlas",
            "total_entries": len(_ATLAS),
            "separation_entries": sum(1 for v in _ATLAS.values() if v["layer"] == "separation"),
            "preservation_entries": sum(1 for v in _ATLAS.values() if v["layer"] == "preservation"),
            "cilt_ii_corridor": "basic-counterexample-atlas",
            "v0_1_49_corridor_record": True,
        },
    )


ATLAS_IDS = tuple(sorted(_ATLAS.keys()))
