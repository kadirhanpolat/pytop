"""Comparison table for sequences, nets, and filters.

This module is a small durable API surface for the v0.1.54 Cilt III
convergence-language bridge.  It does not attempt to automate arbitrary
infinite convergence.  Its role is pedagogical: expose the standard comparison
between sequences, nets, and filters in a machine-readable table that can be
used by notebooks, manuscript examples, and lightweight tests.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConvergenceComparisonRow:
    """One row in the sequence--net--filter comparison table."""

    key: str
    tool: str
    typical_indexing: str
    convergence_test: str
    cluster_test: str
    pedagogical_role: str
    pytop_helpers: tuple[str, ...]
    strength_note: str


_ROWS: tuple[ConvergenceComparisonRow, ...] = (
    ConvergenceComparisonRow(
        key="sequence",
        tool="Sequences",
        typical_indexing="Natural numbers or a countable tail order",
        convergence_test="Every open neighborhood eventually contains all sequence terms.",
        cluster_test="Every open neighborhood is visited by the observed tail/terms.",
        pedagogical_role="Undergraduate entry point; strongest in metric and first-countable spaces.",
        pytop_helpers=(
            "sequence_converges_to",
            "sequence_cluster_point",
            "sequential_closure",
            "analyze_sequences",
        ),
        strength_note="Concrete and computationally friendly, but not sufficient for all topological spaces.",
    ),
    ConvergenceComparisonRow(
        key="net",
        tool="Nets",
        typical_indexing="Arbitrary directed sets",
        convergence_test="Every open neighborhood eventually contains the net.",
        cluster_test="Every open neighborhood is frequently visited by the net.",
        pedagogical_role="General-space convergence language; close to sequence intuition but index-flexible.",
        pytop_helpers=(
            "is_directed_set",
            "is_eventually_in",
            "is_frequently_in",
            "net_converges_to",
            "net_cluster_points",
            "analyze_net",
        ),
        strength_note="Captures closure and continuity in arbitrary topological spaces.",
    ),
    ConvergenceComparisonRow(
        key="filter",
        tool="Filters",
        typical_indexing="Upward-closed families of subsets closed under finite intersections",
        convergence_test="Every open neighborhood of the point belongs to the filter.",
        cluster_test="Every open neighborhood meets every filter member.",
        pedagogical_role="Set-family language suited to compactness, refinement, and adherence arguments.",
        pytop_helpers=(
            "is_filter_base",
            "generated_filter",
            "is_filter",
            "neighborhood_filter_base",
            "filter_converges_to",
            "is_finer_filter",
            "filter_clusters_at",
            "filter_cluster_points",
            "analyze_filter",
        ),
        strength_note="Equivalent in power to nets for many general-topology convergence tasks.",
    ),
)

_ALIASES = {
    "seq": "sequence",
    "sequences": "sequence",
    "sequence": "sequence",
    "net": "net",
    "nets": "net",
    "filter": "filter",
    "filters": "filter",
    "süzgeç": "filter",
    "ag": "net",
    "ağ": "net",
    "dizi": "sequence",
}


def convergence_comparison_table() -> tuple[ConvergenceComparisonRow, ...]:
    """Return the canonical sequence--net--filter comparison rows."""

    return _ROWS


def convergence_comparison_row(key: str) -> ConvergenceComparisonRow:
    """Return one comparison row by key or common alias.

    Parameters
    ----------
    key:
        One of ``sequence``, ``net``, ``filter`` or a common alias such as
        ``seq``, ``nets``, ``filters``, ``dizi``, ``ağ``, or ``süzgeç``.
    """

    normalized = _ALIASES.get(str(key).strip().lower())
    if normalized is None:
        known = ", ".join(sorted(_ALIASES))
        raise KeyError(f"Unknown convergence comparison key {key!r}. Known keys/aliases: {known}")
    for row in _ROWS:
        if row.key == normalized:
            return row
    raise KeyError(normalized)  # defensive; aliases and rows should remain synchronized.


def render_convergence_comparison_table(*, include_helpers: bool = True) -> str:
    """Render the comparison table as Markdown.

    The rendering is intentionally simple so it can be pasted into notebooks,
    manuscript planning notes, or teaching handouts without depending on a rich
    display framework.
    """

    headers = ["Tool", "Indexing / object", "Convergence test", "Cluster test", "Role"]
    if include_helpers:
        headers.append("pytop helpers")
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in _ROWS:
        cells = [
            row.tool,
            row.typical_indexing,
            row.convergence_test,
            row.cluster_test,
            row.pedagogical_role,
        ]
        if include_helpers:
            cells.append(", ".join(f"`{helper}`" for helper in row.pytop_helpers))
        lines.append("| " + " | ".join(_escape_cell(cell) for cell in cells) + " |")
    return "\n".join(lines)


def _escape_cell(value: str) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


__all__ = [
    "ConvergenceComparisonRow",
    "convergence_comparison_table",
    "convergence_comparison_row",
    "render_convergence_comparison_table",
]
