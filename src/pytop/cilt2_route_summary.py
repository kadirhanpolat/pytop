"""Cilt II undergraduate route summary — v0.1.50 close-out corridor.

This module provides a single entry-point function that summarises the three
v0.1.47–v0.1.49 corridors (metric completeness, basic preservation tables,
basic counterexample atlas) as a coordinated Result object, closing out the
Cilt II (v0.1.41–v0.1.50) advanced undergraduate topology corridor.

Roadmap reference:
  v0.1.50 — Add undergraduate worksheet/notebook route (Cilt II close-out)
"""

from __future__ import annotations

from .result import Result
from .metric_completeness import analyze_metric_completeness
from .preservation_tables import analyze_preservation_table
from .counterexample_atlas import analyze_counterexample_atlas


# ---------------------------------------------------------------------------
# Corridor inventory
# ---------------------------------------------------------------------------

_CILT2_CORRIDORS: dict[str, dict] = {
    "v0.1.47": {
        "title": "Metric completeness corridor",
        "api": [
            "is_complete",
            "is_totally_bounded",
            "metric_compactness_check",
            "analyze_metric_completeness",
        ],
        "chapter": 15,
        "summary": (
            "Every finite metric space is complete and totally bounded; "
            "complete + totally bounded <=> compact (metric)."
        ),
    },
    "v0.1.48": {
        "title": "Basic preservation table corridor",
        "api": [
            "preservation_table_lookup",
            "preservation_table_row",
            "preservation_table_column",
            "analyze_preservation_table",
        ],
        "chapter": 10,
        "summary": (
            "5x5 preservation table: connectedness, compactness, Hausdorff, T1, "
            "second_countability x subspace, finite_product, countable_product, "
            "quotient, continuous_image."
        ),
    },
    "v0.1.49": {
        "title": "Basic counterexample atlas corridor",
        "api": [
            "counterexample_lookup",
            "counterexample_atlas_by_layer",
            "counterexample_atlas_by_property",
            "counterexample_atlas_by_construction",
            "analyze_counterexample_atlas",
            "ATLAS_IDS",
        ],
        "chapter": 10,
        "summary": (
            "CE-S-01...CE-S-06 (separation axioms) + CE-P-01...CE-P-10 "
            "(preservation failures). 16 atlas entries total."
        ),
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def cilt2_route_summary(include_sublookups: bool = False) -> Result:
    """Return a structured summary of the complete Cilt II corridor (v0.1.47–v0.1.50).

    Parameters
    ----------
    include_sublookups:
        If True, embed the full sub-corridor Result values in metadata.
        Defaults to False (lightweight mode).
    """
    corridor_summaries = {
        ver: {
            "title": data["title"],
            "api": data["api"],
            "chapter": data["chapter"],
            "summary": data["summary"],
        }
        for ver, data in _CILT2_CORRIDORS.items()
    }

    meta: dict = {
        "operator": "cilt2_route_summary",
        "cilt": "II",
        "phase": "v0.1.41--v0.1.50",
        "close_out_version": "v0.1.50",
        "corridors": corridor_summaries,
        "total_corridors": len(_CILT2_CORRIDORS),
        "chapters_covered": list(range(10, 17)),
        "worksheet": "manuscript/volume_1/worksheets/08_cilt2_undergraduate_route.md",
        "quick_check": "manuscript/volume_1/quick_checks/08_cilt2_undergraduate_route.tex",
        "notebook": "notebooks/teaching/cilt2_undergraduate_route.ipynb",
        "cilt_ii_close_out": True,
        "v0_1_50_corridor_record": True,
    }

    if include_sublookups:
        meta["metric_completeness_report"] = analyze_metric_completeness(
            carrier=["a"], metric={(("a", "a"), 0)}
        ).metadata
        meta["preservation_table_report"] = analyze_preservation_table().metadata
        meta["counterexample_atlas_report"] = analyze_counterexample_atlas().metadata

    return Result.true(
        mode="exact",
        value="cilt_ii_close_out",
        justification=[
            "Cilt II (v0.1.41--v0.1.50) undergraduate route is complete. "
            "Three corridors (v0.1.47 metric completeness, v0.1.48 preservation tables, "
            "v0.1.49 counterexample atlas) are coordinated with worksheet, "
            "quick-check, and notebook surfaces."
        ],
        metadata=meta,
    )


def cilt2_corridor_lookup(version: str) -> Result:
    """Return the corridor record for a specific Cilt II version.

    Parameters
    ----------
    version:
        A version string such as 'v0.1.47', 'v0.1.48', or 'v0.1.49'.
    """
    key = str(version).strip()
    if key not in _CILT2_CORRIDORS:
        return Result.unknown(
            mode="symbolic",
            value="cilt2_corridor_lookup",
            justification=[
                f"No Cilt II corridor record for {version!r}. "
                f"Available: {', '.join(sorted(_CILT2_CORRIDORS))}."
            ],
            metadata={"operator": "cilt2_corridor_lookup", "version": version},
        )
    data = _CILT2_CORRIDORS[key]
    return Result.true(
        mode="exact",
        value=key,
        justification=[data["summary"]],
        metadata={
            "operator": "cilt2_corridor_lookup",
            "version": key,
            "title": data["title"],
            "api": data["api"],
            "chapter": data["chapter"],
            "cilt_ii_close_out": True,
            "v0_1_50_corridor_record": True,
        },
    )
