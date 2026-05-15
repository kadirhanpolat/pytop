"""research_bridge_inventory

Structured export surface for curated manuscript/example-bank/experimental research bridges.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .research_bridge_profiles import get_named_research_bridge_profiles


@dataclass(frozen=True)
class ResearchBridgeInventoryEntry:
    """A joined record connecting a bridge route to a broader research-facing family."""

    key: str
    display_name: str
    path_family: str
    writing_layer: str
    starting_benchmark: str
    example_bank_file: str
    experimental_note: str
    experimental_module: str
    chapter_targets: tuple[str, ...]


_ROUTE_TO_PATH_FAMILY = {
    "safe_zone_sharpness_route": "inequality_sharpness",
    "compactification_upgrade_route": "compactness_comparison",
    "hereditary_local_warning_route": "warning_examples",
    "counterexample_search_route": "counterexample_search",
    "future_threshold_release_route": "project_alignment",
}


def build_research_bridge_inventory() -> tuple[ResearchBridgeInventoryEntry, ...]:
    """Return the joined inventory used by the v0.7.5 export/report surfaces."""

    entries = []
    for route in get_named_research_bridge_profiles():
        entries.append(
            ResearchBridgeInventoryEntry(
                key=route.key,
                display_name=route.display_name,
                path_family=_ROUTE_TO_PATH_FAMILY[route.key],
                writing_layer=route.writing_layer,
                starting_benchmark=route.starting_benchmark,
                example_bank_file=route.example_bank_file,
                experimental_note=route.experimental_note,
                experimental_module=route.experimental_module,
                chapter_targets=route.chapter_targets,
            )
        )
    return tuple(entries)


def inventory_layer_summary() -> dict[str, int]:
    """Return a compact count of routes by manuscript presentation layer."""

    counts = Counter(entry.writing_layer for entry in build_research_bridge_inventory())
    return dict(counts)
