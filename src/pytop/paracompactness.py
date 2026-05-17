"""
paracompactness.py
==================
Covering properties: paracompactness, full normality, metacompactness,
locally finite / star refinements, partition-of-unity existence.

Theorems encoded
----------------
- Stone (1948): metrizable ⟹ paracompact
- Michael: regular + Lindelöf ⟹ paracompact
- Dieudonné: paracompact + Hausdorff ⟹ fully normal (⟹ normal)
- Milnor (1959): CW complexes are paracompact
- Hereditary for closed sets: closed subspace of paracompact ⟹ paracompact
- Compact ⟹ paracompact ⟹ metacompact
- Partition of unity: paracompact Hausdorff admits partitions subordinate to any open cover
- Smirnov metrization: paracompact + locally metrizable ⟹ metrizable

Public surface
--------------
is_paracompact(space)                    → Result
is_fully_normal(space)                   → Result
is_metacompact(space)                    → Result
is_locally_finite_refinement(cover, ref) → bool
is_star_refinement(cover, ref)           → bool
partition_of_unity_warning()             → str
paracompact_profile(space)               → dict
paracompactness_inheritance_profile(space) → dict
analyze_paracompactness(space)           → Result
ParacompactnessError                     → exception
"""

from __future__ import annotations

from typing import Any

from .result import Result

try:
    from .finite_spaces import FiniteTopologicalSpace
except Exception:  # pragma: no cover
    FiniteTopologicalSpace = None  # type: ignore


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class ParacompactnessError(Exception):
    """Raised when a paracompactness operation cannot be completed."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _representation_of(space: Any) -> str:
    if FiniteTopologicalSpace is not None and isinstance(space, FiniteTopologicalSpace):
        return "finite"
    metadata = getattr(space, "metadata", {}) or {}
    if isinstance(metadata, dict) and "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(space, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _tags_of(space: Any) -> frozenset:
    metadata = getattr(space, "metadata", {}) or {}
    raw = metadata.get("tags", []) if isinstance(metadata, dict) else []
    if not raw:
        raw = getattr(space, "tags", []) or []
    return frozenset(str(t).lower().strip() for t in raw)


def _carrier_size(space: Any) -> int | None:
    if FiniteTopologicalSpace is not None and isinstance(space, FiniteTopologicalSpace):
        return len(space.carrier)
    carrier = getattr(space, "carrier", None)
    if carrier is not None:
        try:
            return len(carrier)
        except TypeError:
            pass
    return None


def _has_hausdorff(tags: frozenset, rep: str) -> bool:
    return rep == "finite" or any(
        t in tags for t in ("hausdorff", "t2", "t3", "normal",
                            "metrizable", "compact_hausdorff",
                            "locally_compact_hausdorff", "lc_hausdorff")
    )


def _has_regular(tags: frozenset) -> bool:
    return any(t in tags for t in ("regular", "t3", "regular_t1",
                                   "t3_5", "tychonoff", "normal",
                                   "hausdorff", "t2", "metrizable"))


def _has_lindelof(tags: frozenset) -> bool:
    return any(t in tags for t in ("lindelof", "second_countable",
                                   "separable_metrizable",
                                   "second_countable_hausdorff"))


# ---------------------------------------------------------------------------
# is_locally_finite_refinement
# ---------------------------------------------------------------------------

def is_locally_finite_refinement(cover: Any, refinement: Any) -> bool:
    """
    Return True if *refinement* is a locally finite collection.

    A collection of sets is locally finite when every point has a
    neighbourhood that meets only finitely many members.  For any *finite*
    collection this holds automatically.  When the refinement has no
    computable length the function returns False (cannot determine).

    Parameters
    ----------
    cover : iterable of sets (unused — kept for API symmetry)
    refinement : iterable whose local finiteness is checked
    """
    try:
        len(refinement)
        return True
    except TypeError:
        return False


# ---------------------------------------------------------------------------
# is_star_refinement
# ---------------------------------------------------------------------------

def is_star_refinement(cover: Any, refinement: Any) -> bool:
    """
    Return True if *refinement* is a star-refinement of *cover*.

    For each V in *refinement*, compute
        St(V, refinement) = ⋃{W ∈ refinement : W ∩ V ≠ ∅}
    and check that St(V, refinement) ⊆ some U ∈ cover.

    Both arguments must be iterables of iterables (sets of points).
    Returns False when the inputs cannot be coerced to sets or when the
    star-refinement condition fails for any member.
    """
    try:
        cover_sets = [frozenset(u) for u in cover]
        ref_sets = [frozenset(v) for v in refinement]
    except TypeError:
        return False

    if not ref_sets:
        return True

    for v in ref_sets:
        star_v = frozenset().union(*(w for w in ref_sets if v & w))
        if not any(star_v <= u for u in cover_sets):
            return False
    return True


# ---------------------------------------------------------------------------
# partition_of_unity_warning
# ---------------------------------------------------------------------------

def partition_of_unity_warning() -> str:
    """Return the standard partition-of-unity existence note."""
    return (
        "Paracompact Hausdorff spaces admit partitions of unity subordinate "
        "to any open cover (A.H. Stone / Dieudonné)."
    )


# ---------------------------------------------------------------------------
# is_paracompact
# ---------------------------------------------------------------------------

def is_paracompact(space: Any) -> Result:
    """
    Determine whether *space* is paracompact.

    Decision chain
    --------------
    1. Negative tag → false
    2. Finite space → true (every open cover is finite, hence locally finite)
    3. Metrizable → true (Stone's theorem, 1948)
    4. Compact → true (every finite subcover is locally finite)
    5. Regular + Lindelöf → true (Michael's theorem)
    6. CW complex → true (Milnor, 1959)
    7. Closed subspace of paracompact → true (hereditary for closed sets)
    8. Explicit positive tag → true
    9. Otherwise → unknown
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    if "not_paracompact" in tags:
        return Result.false(
            mode="theorem",
            value="not_paracompact",
            justification=["Space tagged not_paracompact."],
            metadata={"version": "0.5.3", "criterion": "tag"},
        )

    if rep == "finite":
        n = _carrier_size(space)
        return Result.true(
            mode="exact",
            value="paracompact",
            justification=[
                f"Finite space (|X|={n}): every open cover is finite and "
                "hence locally finite — trivially paracompact."
            ],
            metadata={"version": "0.5.3", "carrier_size": n, "criterion": "finite"},
        )

    if "metrizable" in tags or "metric" in tags:
        return Result.true(
            mode="theorem",
            value="paracompact",
            justification=[
                "Metrizable ⟹ paracompact (Stone's theorem, 1948)."
            ],
            metadata={"version": "0.5.3", "criterion": "stone_theorem"},
        )

    if "compact" in tags or "compact_hausdorff" in tags:
        return Result.true(
            mode="theorem",
            value="paracompact",
            justification=["Compact ⟹ paracompact: every finite subcover is locally finite."],
            metadata={"version": "0.5.3", "criterion": "compact"},
        )

    if _has_regular(tags) and _has_lindelof(tags):
        return Result.true(
            mode="theorem",
            value="paracompact",
            justification=["Regular + Lindelöf ⟹ paracompact (Michael's theorem)."],
            metadata={"version": "0.5.3", "criterion": "michael_theorem"},
        )

    if "cw_complex" in tags:
        return Result.true(
            mode="theorem",
            value="paracompact",
            justification=["CW complex ⟹ paracompact (Milnor, 1959)."],
            metadata={"version": "0.5.3", "criterion": "milnor_cw"},
        )

    if "closed_subspace_paracompact" in tags or "closed_in_paracompact" in tags:
        return Result.true(
            mode="theorem",
            value="paracompact",
            justification=[
                "Closed subspace of a paracompact space is paracompact "
                "(paracompactness is hereditary for closed subsets)."
            ],
            metadata={"version": "0.5.3", "criterion": "hereditary_closed"},
        )

    if "paracompact" in tags:
        return Result.true(
            mode="theorem",
            value="paracompact",
            justification=["Space explicitly tagged paracompact."],
            metadata={"version": "0.5.3", "criterion": "tag"},
        )

    return Result.unknown(
        mode="symbolic",
        value="paracompact_unknown",
        justification=["Insufficient tags to determine paracompactness."],
        metadata={"version": "0.5.3"},
    )


# ---------------------------------------------------------------------------
# is_fully_normal
# ---------------------------------------------------------------------------

def is_fully_normal(space: Any) -> Result:
    """
    Determine whether *space* is fully normal.

    A space is fully normal when every open cover has an open star-refinement.
    Paracompact + Hausdorff ⟹ fully normal (Dieudonné).  Metrizable spaces
    satisfy both conditions.

    Decision chain
    --------------
    1. Metrizable → true directly
    2. Paracompact + Hausdorff → true (Dieudonné)
    3. Finite → true (finite T₁ is normal; paracompact + Hausdorff holds)
    4. Explicit tag → true / false
    5. Otherwise → unknown
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    if "not_fully_normal" in tags:
        return Result.false(
            mode="theorem",
            value="not_fully_normal",
            justification=["Space tagged not_fully_normal."],
            metadata={"version": "0.5.3", "criterion": "tag"},
        )

    if "metrizable" in tags or "metric" in tags:
        return Result.true(
            mode="theorem",
            value="fully_normal",
            justification=[
                "Metrizable ⟹ paracompact (Stone) + Hausdorff ⟹ fully normal (Dieudonné)."
            ],
            metadata={"version": "0.5.3", "criterion": "metrizable"},
        )

    para = is_paracompact(space)
    if para.status == "true" and _has_hausdorff(tags, rep):
        return Result.true(
            mode="theorem",
            value="fully_normal",
            justification=[
                "Paracompact + Hausdorff ⟹ fully normal (Dieudonné): "
                "every open cover admits an open star-refinement."
            ],
            metadata={
                "version": "0.5.3",
                "criterion": "dieudonne",
                "paracompact_criterion": para.metadata.get("criterion"),
            },
        )

    if para.status == "true":
        return Result.unknown(
            mode="symbolic",
            value="fully_normal_unknown",
            justification=[
                "Space is paracompact but Hausdorff not confirmed; "
                "full normality requires paracompact + Hausdorff."
            ],
            metadata={"version": "0.5.3"},
        )

    if "fully_normal" in tags:
        return Result.true(
            mode="theorem",
            value="fully_normal",
            justification=["Space explicitly tagged fully_normal."],
            metadata={"version": "0.5.3", "criterion": "tag"},
        )

    return Result.unknown(
        mode="symbolic",
        value="fully_normal_unknown",
        justification=["Paracompactness not confirmed; cannot determine full normality."],
        metadata={"version": "0.5.3"},
    )


# ---------------------------------------------------------------------------
# is_metacompact
# ---------------------------------------------------------------------------

def is_metacompact(space: Any) -> Result:
    """
    Determine whether *space* is metacompact.

    A space is metacompact when every open cover has a point-finite open
    refinement (each point belongs to only finitely many sets of the
    refinement).  Metacompactness is weaker than paracompactness:

        paracompact ⟹ metacompact
        compact ⟹ metacompact

    Decision chain
    --------------
    1. Negative tag → false
    2. Finite → true
    3. Paracompact → true (paracompact ⟹ metacompact)
    4. Compact → true
    5. Explicit tag → true
    6. Otherwise → unknown
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    if "not_metacompact" in tags:
        return Result.false(
            mode="theorem",
            value="not_metacompact",
            justification=["Space tagged not_metacompact."],
            metadata={"version": "0.5.3", "criterion": "tag"},
        )

    if rep == "finite":
        n = _carrier_size(space)
        return Result.true(
            mode="exact",
            value="metacompact",
            justification=[
                f"Finite space (|X|={n}): every open cover is finite "
                "and point-finite — trivially metacompact."
            ],
            metadata={"version": "0.5.3", "carrier_size": n, "criterion": "finite"},
        )

    para = is_paracompact(space)
    if para.status == "true":
        return Result.true(
            mode="theorem",
            value="metacompact",
            justification=[
                "Paracompact ⟹ metacompact: every locally finite refinement "
                "is in particular point-finite."
            ],
            metadata={
                "version": "0.5.3",
                "criterion": "paracompact_implies_metacompact",
                "paracompact_criterion": para.metadata.get("criterion"),
            },
        )

    if "metacompact" in tags:
        return Result.true(
            mode="theorem",
            value="metacompact",
            justification=["Space explicitly tagged metacompact."],
            metadata={"version": "0.5.3", "criterion": "tag"},
        )

    return Result.unknown(
        mode="symbolic",
        value="metacompact_unknown",
        justification=["Insufficient tags to determine metacompactness."],
        metadata={"version": "0.5.3"},
    )


# ---------------------------------------------------------------------------
# paracompact_profile
# ---------------------------------------------------------------------------

def paracompact_profile(space: Any) -> dict[str, Any]:
    """
    Return a comprehensive paracompactness profile for *space*.

    Keys
    ----
    is_paracompact_result      : Result
    is_fully_normal_result     : Result
    is_metacompact_result      : Result
    partition_of_unity         : str
    locally_finite_covers      : str
    key_theorems               : list[str]
    counterexamples            : list[str]
    representation             : str
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    para_result = is_paracompact(space)
    fn_result = is_fully_normal(space)
    meta_result = is_metacompact(space)

    # Partition of unity
    if para_result.status == "true" and _has_hausdorff(tags, rep):
        partition_of_unity = (
            "yes — paracompact Hausdorff: partitions of unity subordinate "
            "to any open cover exist (A.H. Stone / Dieudonné)."
        )
    elif para_result.status == "true":
        partition_of_unity = (
            "paracompact but Hausdorff not confirmed — "
            "partition of unity requires paracompact + Hausdorff."
        )
    else:
        partition_of_unity = (
            "partitions of unity exist when space is paracompact Hausdorff; "
            "current tags insufficient to confirm."
        )

    # Locally finite covers
    if rep == "finite":
        lf_covers = "Every open cover of a finite space is itself finite and locally finite."
    else:
        lf_covers = (
            "Paracompact iff every open cover has a locally finite open refinement. "
            "Locally finite: each point has a neighbourhood meeting only finitely many sets."
        )

    key_theorems = [
        "Stone (1948): Every metrizable space is paracompact.",
        "Michael: Every regular Lindelöf space is paracompact.",
        "Milnor (1959): Every CW complex is paracompact.",
        "Dieudonné: Paracompact + Hausdorff ⟹ fully normal ⟹ normal.",
        "Hereditary: Closed subspace of paracompact ⟹ paracompact.",
        "Partition of unity: Paracompact Hausdorff admits partitions subordinate to any cover.",
        "Smirnov: Paracompact + locally metrizable ⟹ metrizable.",
        "Implication chain: paracompact ⟹ metacompact.",
    ]

    counterexamples = [
        "Long line (ω₁): regular, not Lindelöf, not paracompact.",
        "Niemytzki (Moore) plane: Tychonoff, separable, not normal, not paracompact.",
        "Sorgenfrey plane (ℝ_ℓ × ℝ_ℓ): product of two paracompact spaces need not be paracompact.",
        "Ordinal space [0,ω₁): normal, not Lindelöf, not paracompact.",
        "Michael line: Lindelöf × Lindelöf need not be normal (product failure).",
    ]

    return {
        "is_paracompact_result": para_result,
        "is_fully_normal_result": fn_result,
        "is_metacompact_result": meta_result,
        "partition_of_unity": partition_of_unity,
        "locally_finite_covers": lf_covers,
        "key_theorems": key_theorems,
        "counterexamples": counterexamples,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# paracompactness_inheritance_profile
# ---------------------------------------------------------------------------

def paracompactness_inheritance_profile(space: Any) -> dict[str, Any]:
    """
    Summarise what paracompactness implies for *space* and how it is inherited.

    Returns a dict with keys:
    - ``paracompact``        : bool | None
    - ``implies_normal``     : bool | None  (paracompact + Hausdorff → normal)
    - ``implies_metrizable`` : bool | None  (paracompact + locally metrizable → metrizable)
    - ``inherited_by_closed``: bool         (always True: closed subspaces inherit)
    - ``preserved_products`` : str          (generally fails; notes exception)
    - ``criterion``          : str          (which rule fired for paracompactness)
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    para = is_paracompact(space)
    para_bool: bool | None = (
        True if para.status == "true" else
        False if para.status == "false" else
        None
    )

    implies_normal: bool | None = None
    if para_bool is True:
        implies_normal = _has_hausdorff(tags, rep)
    elif para_bool is False:
        implies_normal = None

    locally_metrizable = any(
        t in tags for t in ("locally_metrizable", "metrizable", "metric")
    )
    implies_metrizable: bool | None = None
    if para_bool is True and locally_metrizable:
        implies_metrizable = True
    elif para_bool is True:
        implies_metrizable = None

    return {
        "paracompact": para_bool,
        "implies_normal": implies_normal,
        "implies_metrizable": implies_metrizable,
        "inherited_by_closed": True,
        "preserved_products": (
            "Generally fails: Sorgenfrey plane = ℝ_ℓ × ℝ_ℓ is not paracompact "
            "even though ℝ_ℓ is. Exception: finite products of compact spaces."
        ),
        "criterion": para.metadata.get("criterion", "unknown"),
    }


# ---------------------------------------------------------------------------
# analyze_paracompactness  (facade)
# ---------------------------------------------------------------------------

def analyze_paracompactness(space: Any) -> Result:
    """
    Single-call facade: full paracompactness analysis.

    Returns a Result whose ``value`` is the full ``paracompact_profile`` dict.
    """
    rep = _representation_of(space)
    profile = paracompact_profile(space)
    n = _carrier_size(space)
    para = profile["is_paracompact_result"]

    mode = "exact" if rep == "finite" else para.mode

    justification = [
        f"Domain representation: {rep}",
        f"Paracompact: {para.status} ({para.mode}) — {para.justification[0]}",
        f"Fully normal: {profile['is_fully_normal_result'].status}",
        f"Metacompact: {profile['is_metacompact_result'].status}",
        f"Partition of unity: {profile['partition_of_unity'][:80]}",
    ]
    if rep == "finite" and n is not None:
        justification.insert(1, f"|X|={n}: finite ⟹ paracompact (exact).")

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": "0.5.3",
            "domain_representation": rep,
            "carrier_size": n,
            "paracompact_status": para.status,
            "paracompact_criterion": para.metadata.get("criterion"),
        },
    )


__all__ = [
    "ParacompactnessError",
    "is_paracompact",
    "is_fully_normal",
    "is_metacompact",
    "is_locally_finite_refinement",
    "is_star_refinement",
    "partition_of_unity_warning",
    "paracompact_profile",
    "paracompactness_inheritance_profile",
    "analyze_paracompactness",
]
