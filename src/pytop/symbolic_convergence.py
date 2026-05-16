"""Symbolic convergence theory for infinite topological spaces.

Provides tag-based net and filter descriptors that work with infinite
(symbolic) spaces, complementing the finite exact layers in ``nets.py``
and ``filters.py``.

Key classes:
  ``SymbolicNetDescriptor``     — net on an infinite space via tags
  ``SymbolicFilterDescriptor``  — filter on an infinite space via tags

Key functions:
  ``net_converges_symbolically``    — convergence result from space/net tags
  ``filter_converges_symbolically`` — convergence result from space/filter tags
  ``ultrafilter_theorem_descriptor`` — ultrafilter / compactness link
  ``convergence_equivalence_profile`` — nets ↔ filters equivalence record
  ``analyze_symbolic_convergence``  — combined facade
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .result import Result

VERSION = "0.1.0"


# ---------------------------------------------------------------------------
# Tag helpers (local, no import cycle)
# ---------------------------------------------------------------------------

def _tags_of(obj: Any) -> set[str]:
    tags: set[str] = set()
    if isinstance(obj, dict):
        raw = obj.get("tags", [])
        if isinstance(raw, (list, tuple, set, frozenset)):
            tags.update(str(t).strip().lower() for t in raw)
        return tags
    raw = getattr(obj, "tags", set()) or set()
    if isinstance(raw, (set, frozenset, list, tuple)):
        tags.update(str(t).strip().lower() for t in raw)
    meta = getattr(obj, "metadata", {}) or {}
    if isinstance(meta, dict):
        for t in meta.get("tags", []):
            tags.add(str(t).strip().lower())
    return tags


# ---------------------------------------------------------------------------
# SymbolicNetDescriptor
# ---------------------------------------------------------------------------

@dataclass
class SymbolicNetDescriptor:
    """A symbolic net on an infinite topological space.

    Parameters
    ----------
    space:
        The infinite space (any object with tags or a dict).
    index_type:
        'chain' (e.g. ω), 'uncountable', or 'directed'.
    value_tags:
        Tags describing how the net's values relate to the space
        (e.g. 'dense_range', 'eventually_in_every_open').
    convergence_point_tag:
        Tag describing the limit point (e.g. 'limit_exists', or a point name).
    name:
        Optional human-readable name.
    """

    space: Any
    index_type: str = "chain"
    value_tags: set[str] = field(default_factory=set)
    convergence_point_tag: str = ""
    name: str = ""

    def __post_init__(self) -> None:
        if self.index_type not in ("chain", "uncountable", "directed"):
            self.index_type = "directed"
        self.value_tags = {str(t).strip().lower() for t in self.value_tags}

    @property
    def space_tags(self) -> set[str]:
        return _tags_of(self.space)

    def convergence_result(self) -> Result:
        """Compute a symbolic convergence result for this net."""
        return net_converges_symbolically(self)


# ---------------------------------------------------------------------------
# SymbolicFilterDescriptor
# ---------------------------------------------------------------------------

@dataclass
class SymbolicFilterDescriptor:
    """A symbolic filter on an infinite topological space.

    Parameters
    ----------
    space:
        The infinite space.
    filter_type:
        'neighborhood', 'ultrafilter', 'cofinite', 'principal', or 'general'.
    base_tags:
        Tags describing the filter base (e.g. 'closed_under_intersection').
    convergence_point_tag:
        Tag for the convergence/cluster point.
    name:
        Optional human-readable name.
    """

    space: Any
    filter_type: str = "general"
    base_tags: set[str] = field(default_factory=set)
    convergence_point_tag: str = ""
    name: str = ""

    def __post_init__(self) -> None:
        valid_types = {"neighborhood", "ultrafilter", "cofinite", "principal", "general"}
        if self.filter_type not in valid_types:
            self.filter_type = "general"
        self.base_tags = {str(t).strip().lower() for t in self.base_tags}

    @property
    def space_tags(self) -> set[str]:
        return _tags_of(self.space)

    def convergence_result(self) -> Result:
        """Compute a symbolic convergence result for this filter."""
        return filter_converges_symbolically(self)


# ---------------------------------------------------------------------------
# Convergence results
# ---------------------------------------------------------------------------

def net_converges_symbolically(net: SymbolicNetDescriptor) -> Result:
    """Determine convergence of a symbolic net.

    Rules applied (in order):
    1. Tag 'eventually_in_every_open' or 'convergent' → converges.
    2. 'dense_range' in compact Hausdorff → has cluster point (not necessarily convergent).
    3. Space is sequentially compact + index_type='chain' → cluster point exists.
    4. Space is indiscrete → every net converges to every point.
    5. Otherwise: unknown.
    """
    space_tags = net.space_tags
    value_tags = net.value_tags
    meta = {"version": VERSION, "index_type": net.index_type, "value_tags": sorted(value_tags)}

    # Explicit convergence witness
    if "convergent" in value_tags or "eventually_in_every_open" in value_tags:
        return Result.true(
            mode="theorem",
            value="net_converges",
            justification=["Net is tagged as convergent / eventually in every open set."],
            metadata=meta,
        )

    if "not_convergent" in value_tags:
        return Result.false(
            mode="theorem",
            value="net_not_convergent",
            justification=["Net is tagged not_convergent."],
            metadata=meta,
        )

    # Indiscrete space: every net converges to every point
    if "indiscrete" in space_tags:
        return Result.true(
            mode="theorem",
            value="net_converges",
            justification=["Indiscrete space: every net converges to every point (only open sets are ∅ and X)."],
            metadata=meta,
        )

    # Compact space: every net has a cluster point (but convergence needs Hausdorff)
    if "compact" in space_tags:
        if "hausdorff" in space_tags:
            if "dense_range" in value_tags or net.index_type in ("chain", "directed"):
                return Result.true(
                    mode="theorem",
                    value="net_has_cluster_point",
                    justification=[
                        "Compact Hausdorff space: every net has a convergent subnet "
                        "(universal nets converge; cluster points exist by compactness)."
                    ],
                    metadata={**meta, "note": "cluster point, not necessarily the net itself"},
                )
        else:
            return Result.true(
                mode="theorem",
                value="net_has_cluster_point",
                justification=["Compact space: every net has a cluster point."],
                metadata=meta,
            )

    # Sequential compactness + countable index → subsequence converges
    if "sequentially_compact" in space_tags and net.index_type == "chain":
        return Result.true(
            mode="theorem",
            value="net_has_convergent_subnet",
            justification=[
                "Sequentially compact space: every sequence (chain-indexed net) "
                "has a convergent subsequence."
            ],
            metadata=meta,
        )

    # First-countable: convergence via sequences suffices
    if "first_countable" in space_tags and net.index_type == "chain":
        return Result.unknown(
            mode="theorem",
            value="net_convergence_unknown",
            justification=[
                "First-countable space: sequential convergence characterizes topology, "
                "but no decisive tag on the net's behavior."
            ],
            metadata=meta,
        )

    return Result.unknown(
        mode="symbolic",
        value="net_convergence_unknown",
        justification=["Insufficient tags to determine symbolic net convergence."],
        metadata=meta,
    )


def filter_converges_symbolically(filt: SymbolicFilterDescriptor) -> Result:
    """Determine convergence of a symbolic filter.

    Rules applied (in order):
    1. filter_type='neighborhood' → the neighborhood filter converges to its base point.
    2. 'convergent' in base_tags → converges.
    3. filter_type='ultrafilter' in compact space → converges.
    4. Cofinite filter in T1 compact space → converges.
    5. Space is indiscrete → every filter converges to every point.
    6. Otherwise: unknown.
    """
    space_tags = filt.space_tags
    base_tags = filt.base_tags
    meta = {
        "version": VERSION,
        "filter_type": filt.filter_type,
        "base_tags": sorted(base_tags),
    }

    # Neighborhood filter always converges to its base point
    if filt.filter_type == "neighborhood":
        return Result.true(
            mode="theorem",
            value="filter_converges",
            justification=[
                "The neighborhood filter of a point converges to that point "
                "(by definition of the neighborhood filter)."
            ],
            metadata=meta,
        )

    # Explicit convergence tag
    if "convergent" in base_tags:
        return Result.true(
            mode="theorem",
            value="filter_converges",
            justification=["Filter is tagged convergent."],
            metadata=meta,
        )

    if "not_convergent" in base_tags:
        return Result.false(
            mode="theorem",
            value="filter_not_convergent",
            justification=["Filter is tagged not_convergent."],
            metadata=meta,
        )

    # Indiscrete space
    if "indiscrete" in space_tags:
        return Result.true(
            mode="theorem",
            value="filter_converges",
            justification=["Indiscrete space: every filter converges to every point."],
            metadata=meta,
        )

    # Ultrafilter in compact space → converges
    if filt.filter_type == "ultrafilter":
        if "compact" in space_tags:
            return Result.true(
                mode="theorem",
                value="filter_converges",
                justification=[
                    "Ultrafilter theorem: every ultrafilter on a compact space converges. "
                    "(Tychonoff ↔ every ultrafilter converges.)"
                ],
                metadata=meta,
            )
        return Result.unknown(
            mode="theorem",
            value="ultrafilter_convergence_unknown",
            justification=[
                "Ultrafilter convergence in non-compact space depends on specific ultrafilter."
            ],
            metadata=meta,
        )

    # Cofinite filter in compact T1 → converges
    if filt.filter_type == "cofinite":
        if "compact" in space_tags and "t1" in space_tags:
            return Result.true(
                mode="theorem",
                value="filter_converges",
                justification=[
                    "Cofinite filter on a compact T1 space converges "
                    "(compact T1 → every ultrafilter converges → cofinite filter converges)."
                ],
                metadata=meta,
            )

    # General compact: every filter has a cluster point
    if "compact" in space_tags:
        return Result.true(
            mode="theorem",
            value="filter_has_cluster_point",
            justification=[
                "Compact space: every filter has a cluster point "
                "(equivalently: every filter can be extended to a convergent ultrafilter)."
            ],
            metadata=meta,
        )

    return Result.unknown(
        mode="symbolic",
        value="filter_convergence_unknown",
        justification=["Insufficient tags to determine symbolic filter convergence."],
        metadata=meta,
    )


# ---------------------------------------------------------------------------
# Ultrafilter theorem descriptor
# ---------------------------------------------------------------------------

def ultrafilter_theorem_descriptor() -> dict[str, Any]:
    """Return a descriptor for the ultrafilter theorem and its consequences.

    The ultrafilter theorem (equivalent to the Boolean prime ideal theorem,
    weaker than AC) states: every filter can be extended to an ultrafilter.

    Consequences:
    - Tychonoff's theorem (product of compact spaces is compact) is equivalent
      to AC; compactness via ultrafilters needs the ultrafilter theorem.
    - A space X is compact iff every ultrafilter converges.
    - A Hausdorff space X is compact iff every ultrafilter converges to exactly
      one point.
    """
    return {
        "theorem": "Ultrafilter theorem (Boolean prime ideal theorem)",
        "statement": "Every filter on a set can be extended to an ultrafilter.",
        "logical_strength": "Weaker than AC; independent of ZF.",
        "compactness_equivalence": (
            "X is compact ⟺ every ultrafilter on X converges. "
            "(Hausdorff case: X is compact ⟺ every ultrafilter converges to exactly one point.)"
        ),
        "tychonoff_connection": (
            "Tychonoff's theorem (∏ X_α compact ⟺ all X_α compact) is equivalent to AC. "
            "For Hausdorff factors, it follows from the ultrafilter theorem alone."
        ),
        "stone_cech_connection": (
            "The Stone-Čech compactification βX is the space of ultrafilters on X "
            "(for discrete X). Every filter on X extends to a point of βX."
        ),
        "net_filter_equivalence": (
            "x in cl(A) ⟺ ∃ net in A converging to x ⟺ ∃ filter containing A converging to x."
        ),
        "version": VERSION,
    }


# ---------------------------------------------------------------------------
# Nets ↔ Filters equivalence profile
# ---------------------------------------------------------------------------

def convergence_equivalence_profile(space: Any) -> dict[str, Any]:
    """Return a profile comparing net and filter convergence for *space*.

    Documents:
    - When nets and filters give equivalent convergence theories.
    - When sequential convergence suffices (first-countable spaces).
    - The ultrafilter/compactness link.
    """
    space_tags = _tags_of(space)
    meta: dict[str, Any] = {"version": VERSION, "space_tags": sorted(space_tags)}

    equivalences = [
        "x ∈ cl(A) ⟺ ∃ net in A converging to x ⟺ ∃ filter generated by {A} converging to x.",
        "f: X → Y continuous ⟺ f preserves net convergence ⟺ f preserves filter convergence.",
        "X compact ⟺ every net has a cluster point ⟺ every ultrafilter converges.",
    ]

    sequential_sufficiency = None
    if "first_countable" in space_tags or "second_countable" in space_tags or "metrizable" in space_tags:
        sequential_sufficiency = (
            "First-countable: sequences suffice — net/filter convergence ↔ sequential convergence. "
            "x ∈ cl(A) ⟺ ∃ sequence in A converging to x."
        )
        meta["sequential_sufficiency"] = True
    else:
        sequential_sufficiency = (
            "Not first-countable: sequences do NOT generally suffice. "
            "Need nets or filters for full convergence theory."
        )
        meta["sequential_sufficiency"] = False

    ultrafilter_note = None
    if "compact" in space_tags:
        ultrafilter_note = (
            "Compact space: every ultrafilter converges. "
            + ("Exactly one limit point per ultrafilter (Hausdorff)." if "hausdorff" in space_tags else "")
        )

    return {
        "equivalences": equivalences,
        "sequential_sufficiency": sequential_sufficiency,
        "ultrafilter_note": ultrafilter_note,
        "nets_advantage": "Nets generalize sequences; work in any topological space without restriction.",
        "filters_advantage": "Filters avoid index-set bookkeeping; natural for compactness proofs.",
        "metadata": meta,
    }


# ---------------------------------------------------------------------------
# Combined facade
# ---------------------------------------------------------------------------

def analyze_symbolic_convergence(
    space: Any,
    *,
    net: SymbolicNetDescriptor | None = None,
    filt: SymbolicFilterDescriptor | None = None,
) -> dict[str, Any]:
    """Analyze symbolic convergence for *space*, optionally with a net or filter.

    Returns a dict with keys:
        space_tags, net_result, filter_result, equivalence_profile,
        ultrafilter_descriptor, version
    """
    space_tags = _tags_of(space)
    net_result = net.convergence_result() if net else None
    filter_result = filt.convergence_result() if filt else None

    return {
        "space_tags": sorted(space_tags),
        "net_result": net_result,
        "filter_result": filter_result,
        "equivalence_profile": convergence_equivalence_profile(space),
        "ultrafilter_descriptor": ultrafilter_theorem_descriptor(),
        "version": VERSION,
    }


__all__ = [
    "SymbolicNetDescriptor",
    "SymbolicFilterDescriptor",
    "net_converges_symbolically",
    "filter_converges_symbolically",
    "ultrafilter_theorem_descriptor",
    "convergence_equivalence_profile",
    "analyze_symbolic_convergence",
]
