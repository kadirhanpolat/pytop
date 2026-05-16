"""Stone-Čech compactification: existence, embeddings, and function-extension theorems.

Key theorems implemented
------------------------
- βX exists iff X is Tychonoff (T3.5).
- X embeds as a dense subspace of βX iff X is Tychonoff.
- Every bounded continuous f: X → R extends uniquely to f̃: βX → R (universal property).
- X is compact Hausdorff iff the embedding X ↪ βX is a homeomorphism (X = βX).
- For discrete X, βX = ultrafilter space on X; |βN| = 2^c.
- βX is the largest compactification of X (universality among Tychonoff compactifications).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class StoneCechDescriptor:
    """A named Stone-Čech compactification example."""

    key: str
    display_name: str
    base_space: str
    beta_space_description: str
    embedding_type: str     # "homeomorphism" or "proper_dense"
    remainder_note: str     # description of βX \\ X
    cardinality_note: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

STONE_CECH_TYCHONOFF_TAGS: set[str] = {
    # Direct Tychonoff / T3.5
    "tychonoff", "t3_5", "t3½", "completely_regular_t1",
    # T4 / normal T1 → Tychonoff
    "t4", "normal_t1", "perfectly_normal",
    # Metric/metrizable → completely regular → Tychonoff
    "metric", "metrizable", "completely_metrizable",
    "second_countable_regular", "second_countable_t3", "urysohn_metrizable",
    # Special classes that are always Tychonoff
    "lie_group", "lie", "profinite", "profinite_group",
    # Compact Hausdorff → T4 → Tychonoff
    "compact_hausdorff", "compact_t2",
}

COMPACT_HAUSDORFF_TAGS: set[str] = {
    "compact_hausdorff", "compact_t2",
}

STONE_CECH_BLOCKING_TAGS: set[str] = {
    "not_tychonoff", "not_t3_5", "not_completely_regular", "not_t1", "not_hausdorff",
}

# Tags for detecting compact + Hausdorff from separate tags
_COMPACT_POSITIVE: frozenset[str] = frozenset({
    "compact", "compact_hausdorff", "compact_t2", "profinite",
})
_HAUSDORFF_POSITIVE: frozenset[str] = frozenset({
    "hausdorff", "t2", "t3", "tychonoff", "t3_5", "t4",
    "metric", "metrizable", "compact_hausdorff",
})


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_tags(space: Any) -> set[str]:
    raw = getattr(space, "tags", None) or getattr(space, "_tags", None)
    if isinstance(raw, (set, list, tuple, frozenset)):
        return {str(t).strip().lower() for t in raw}
    return set()


def _representation_of(space: Any) -> str:
    metadata = getattr(space, "metadata", {}) or {}
    if isinstance(metadata, dict) and "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(space, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _is_compact_hausdorff(tags: set[str]) -> bool:
    """True if tags confirm compact + Hausdorff (= X is its own Stone-Čech compactification)."""
    if bool(tags & COMPACT_HAUSDORFF_TAGS):
        return True
    return bool(tags & _COMPACT_POSITIVE) and bool(tags & _HAUSDORFF_POSITIVE)


# ---------------------------------------------------------------------------
# Named examples registry
# ---------------------------------------------------------------------------

def get_named_stone_cech_examples() -> tuple[StoneCechDescriptor, ...]:
    """Return canonical Stone-Čech compactification examples."""
    return (
        StoneCechDescriptor(
            key="beta_n",
            display_name="βN — Stone-Čech compactification of N",
            base_space="N (natural numbers with discrete topology)",
            beta_space_description=(
                "Space of ultrafilters on N; compact Hausdorff and extremally disconnected. "
                "Principal ultrafilters correspond to isolated points of N inside βN."
            ),
            embedding_type="proper_dense",
            remainder_note=(
                "βN \\ N (the corona or Stone-Čech remainder) is a compact Hausdorff space "
                "of cardinality 2^c; it is non-metrizable and has no isolated points."
            ),
            cardinality_note="|βN| = 2^c = 2^{2^{ℵ₀}}",
            chapter_targets=("21", "38"),
        ),
        StoneCechDescriptor(
            key="beta_r",
            display_name="βR — Stone-Čech compactification of R",
            base_space="R (real line with standard topology)",
            beta_space_description=(
                "A non-metrizable compact Hausdorff space containing R as a dense subspace; "
                "properly extends the one-point compactification R ∪ {∞}."
            ),
            embedding_type="proper_dense",
            remainder_note=(
                "βR \\ R is non-metrizable; the one-point compactification circle S¹ is a "
                "quotient of βR but βR is much larger."
            ),
            cardinality_note="|βR| = 2^c",
            chapter_targets=("21", "38"),
        ),
        StoneCechDescriptor(
            key="beta_compact_hausdorff",
            display_name="βX = X — compact Hausdorff self-compactification",
            base_space="X compact Hausdorff",
            beta_space_description=(
                "A compact Hausdorff space is already its own Stone-Čech compactification: "
                "every bounded continuous function on X extends trivially (it is already defined on βX = X)."
            ),
            embedding_type="homeomorphism",
            remainder_note="Remainder βX \\ X = ∅ (no new points added).",
            cardinality_note="|βX| = |X|",
            chapter_targets=("21",),
        ),
        StoneCechDescriptor(
            key="beta_q",
            display_name="βQ — Stone-Čech compactification of Q",
            base_space="Q (rationals as subspace of R)",
            beta_space_description=(
                "A separable compact Hausdorff space; βQ ≠ βR since Q is not Čech-complete. "
                "The inclusion Q ↪ R does not extend to a homeomorphism βQ ≅ βR."
            ),
            embedding_type="proper_dense",
            remainder_note=(
                "βQ \\ Q is a compact non-metrizable space; Q is not Čech-complete, "
                "so the remainder is non-empty and complicated."
            ),
            cardinality_note="|βQ| = 2^c",
            chapter_targets=("21", "38"),
        ),
        StoneCechDescriptor(
            key="beta_discrete",
            display_name="βX — Stone-Čech of a discrete space",
            base_space="X with discrete topology (infinite)",
            beta_space_description=(
                "βX = space of ultrafilters on X; points of X correspond to principal ultrafilters. "
                "βX is extremally disconnected and compact Hausdorff."
            ),
            embedding_type="proper_dense",
            remainder_note=(
                "Non-principal ultrafilters form the remainder βX \\ X; "
                "isolated points of βX are exactly the points of X."
            ),
            cardinality_note="|βX| = 2^{2^{|X|}} for infinite discrete X",
            chapter_targets=("21", "38"),
        ),
    )


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_stone_cech_compactifiable(space: Any) -> Result:
    """Determine whether the Stone-Čech compactification βX exists for the space.

    The Stone-Čech compactification exists (and embeds X densely) if and only if
    X is Tychonoff (T3.5 / completely regular Hausdorff).

    Decision layers
    ---------------
    1. Explicit blocking tags (not_tychonoff, not_t1, not_hausdorff, ...) → false.
    2. Compact Hausdorff (explicit tag or compact + Hausdorff) → true (X = βX).
    3. Direct Tychonoff positive tags → true.
    4. T4 / normal T1 / perfectly normal → true.
    5. Metric / metrizable → true (metrizable → Tychonoff).
    6. Lie group / profinite → true (both are Tychonoff).
    7. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    # Layer 1: explicit blocking tags
    if tags & STONE_CECH_BLOCKING_TAGS:
        blocking = next(t for t in tags if t in STONE_CECH_BLOCKING_TAGS)
        return Result.false(
            mode="theorem",
            value="stone_cech_compactifiable",
            justification=[
                f"The space carries blocking tag {blocking!r}.",
                "The Stone-Čech compactification βX exists only for Tychonoff (T3.5) spaces.",
            ],
            metadata={**base, "criterion": None},
        )

    # Layer 2: compact Hausdorff → X = βX
    if _is_compact_hausdorff(tags):
        return Result.true(
            mode="theorem",
            value="stone_cech_compactifiable",
            justification=[
                "Compact Hausdorff spaces are Tychonoff; moreover X is already compact so βX = X.",
                "The Stone-Čech compactification exists and is homeomorphic to X itself.",
            ],
            metadata={**base, "criterion": "compact_hausdorff", "self_compact": True},
        )

    # Layer 3: direct Tychonoff tags
    direct = {"tychonoff", "t3_5", "t3½", "completely_regular_t1"}
    if bool(tags & direct):
        return Result.true(
            mode="theorem",
            value="stone_cech_compactifiable",
            justification=[
                "The space is Tychonoff (T3.5); the Stone-Čech compactification βX exists.",
                "X embeds as a dense subspace of the compact Hausdorff space βX.",
            ],
            metadata={**base, "criterion": "tychonoff", "self_compact": None},
        )

    # Layer 4: T4 / normal T1 → Tychonoff
    t4_tags = {"t4", "normal_t1", "perfectly_normal"}
    if bool(tags & t4_tags):
        return Result.true(
            mode="theorem",
            value="stone_cech_compactifiable",
            justification=[
                "T4 (normal T1) implies Tychonoff by Urysohn's Lemma; βX therefore exists.",
            ],
            metadata={**base, "criterion": "t4_implies_tychonoff", "self_compact": None},
        )

    # Layer 5: metric / metrizable → Tychonoff
    metric_tags = {"metric", "metrizable", "completely_metrizable",
                   "second_countable_regular", "second_countable_t3", "urysohn_metrizable"}
    if bool(tags & metric_tags):
        return Result.true(
            mode="theorem",
            value="stone_cech_compactifiable",
            justification=[
                "Metrizable spaces are Tychonoff (metric structure supplies complete regularity); βX exists.",
            ],
            metadata={**base, "criterion": "metrizable_implies_tychonoff", "self_compact": None},
        )

    # Layer 6: Lie group / profinite → Tychonoff
    lie_profinite = {"lie_group", "lie", "smooth_manifold_group", "profinite", "profinite_group"}
    if bool(tags & lie_profinite):
        return Result.true(
            mode="theorem",
            value="stone_cech_compactifiable",
            justification=[
                "Lie groups (smooth manifolds) and profinite groups are both Tychonoff; βX exists.",
            ],
            metadata={**base, "criterion": "special_class_tychonoff", "self_compact": None},
        )

    return Result.unknown(
        mode="symbolic",
        value="stone_cech_compactifiable",
        justification=[
            "Insufficient information to confirm Tychonoff (T3.5) status.",
            "Tag with 'tychonoff'/'t3_5', or 'metric', or 't4', or 'compact_hausdorff' to determine βX existence.",
        ],
        metadata={**base, "criterion": None},
    )


def stone_cech_embedding(space: Any) -> Result:
    """Determine the embedding type of X into its Stone-Čech compactification βX.

    Possible outcomes:
    - **homeomorphism**: X is compact Hausdorff, so X = βX (no proper extension).
    - **proper dense**: X is Tychonoff but not compact; X embeds densely and properly into βX.
    - **false**: X is not Tychonoff; no Stone-Čech embedding exists.
    - **unknown**: Insufficient information.

    The embedding type is recorded in ``metadata["embedding_type"]``.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    comp_r = is_stone_cech_compactifiable(space)

    if comp_r.is_false:
        return Result.false(
            mode="theorem",
            value="stone_cech_embedding",
            justification=[
                "No Stone-Čech embedding exists: the space is not Tychonoff.",
                "Dense embeddings into compact Hausdorff spaces characterise Tychonoff spaces.",
            ],
            metadata={**base, "embedding_type": None},
        )

    if comp_r.is_true:
        is_ch = _is_compact_hausdorff(tags)
        if is_ch:
            return Result.true(
                mode="theorem",
                value="stone_cech_embedding",
                justification=[
                    "X is compact Hausdorff, so the embedding X ↪ βX is a homeomorphism (X = βX).",
                    "No proper compactification is needed; the space is already compact.",
                ],
                metadata={**base, "embedding_type": "homeomorphism"},
            )
        return Result.true(
            mode="theorem",
            value="stone_cech_embedding",
            justification=[
                "X is Tychonoff, so X embeds as a dense subspace of the compact Hausdorff space βX.",
                "The embedding is proper (X ≇ βX) because X is not compact Hausdorff.",
            ],
            metadata={**base, "embedding_type": "proper_dense"},
        )

    return Result.unknown(
        mode="symbolic",
        value="stone_cech_embedding",
        justification=[
            "Cannot determine embedding type: Tychonoff status is unknown.",
        ],
        metadata={**base, "embedding_type": None},
    )


def stone_cech_extension(space: Any) -> Result:
    """Determine whether the Stone-Čech function-extension property holds.

    Universal property: X is Tychonoff iff for every compact Hausdorff space K
    and every continuous f: X → K there exists a unique continuous extension
    f̃: βX → K.  The key special case is K = [0,1]: X is Tychonoff iff every
    bounded continuous f: X → R extends to f̃: βX → R.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    comp_r = is_stone_cech_compactifiable(space)

    if comp_r.is_true:
        return Result.true(
            mode="theorem",
            value="stone_cech_extension",
            justification=[
                "X is Tychonoff; the Stone-Čech universal property holds.",
                "Every bounded continuous f: X → R extends uniquely to f̃: βX → R.",
                "More generally, every continuous f: X → K (K compact Hausdorff) extends uniquely to βX.",
            ],
            metadata={**base, "criterion": comp_r.metadata.get("criterion")},
        )

    if comp_r.is_false:
        return Result.false(
            mode="theorem",
            value="stone_cech_extension",
            justification=[
                "The space is not Tychonoff; the Stone-Čech extension property fails.",
                "Continuous functions need not separate points from closed sets, blocking extension.",
            ],
            metadata={**base, "criterion": None},
        )

    return Result.unknown(
        mode="symbolic",
        value="stone_cech_extension",
        justification=[
            "Cannot determine extension property: Tychonoff status is unknown.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_stone_cech(space: Any) -> dict[str, Any]:
    """Classify the relationship between X and its Stone-Čech compactification βX.

    Keys
    ----
    relationship : str
        One of ``"homeomorphism"``, ``"proper_compactification"``,
        ``"non_existent"``, ``"unknown"``.
    is_compactifiable : Result
        Whether βX exists.
    is_self_compact : bool or None
        True if X = βX (compact Hausdorff); False if X is Tychonoff but not compact;
        None if unknown.
    criterion : str or None
        The criterion used to determine compactifiability.
    note : str
        Human-readable summary.
    """
    tags = _extract_tags(space)
    comp_r = is_stone_cech_compactifiable(space)
    criterion = comp_r.metadata.get("criterion") if isinstance(comp_r.metadata, dict) else None

    # Determine self-compact status
    is_ch = _is_compact_hausdorff(tags)
    not_compact = "not_compact" in tags
    if is_ch:
        is_self_compact: bool | None = True
    elif comp_r.is_true and not_compact:
        is_self_compact = False
    elif comp_r.is_true and not is_ch:
        is_self_compact = None  # Tychonoff but compactness unknown
    else:
        is_self_compact = None

    if comp_r.is_false:
        relationship = "non_existent"
        note = "βX does not exist: the space is not Tychonoff."
    elif comp_r.is_true:
        if is_ch:
            relationship = "homeomorphism"
            note = "X is compact Hausdorff, so βX = X (homeomorphism)."
        elif not_compact:
            relationship = "proper_compactification"
            note = "X is Tychonoff but not compact; βX is a proper compactification."
        else:
            relationship = "proper_compactification"
            note = "X is Tychonoff; βX exists as a compactification (compactness status unknown)."
    else:
        relationship = "unknown"
        note = "Tychonoff status is undetermined; cannot classify X → βX."

    return {
        "relationship": relationship,
        "is_compactifiable": comp_r,
        "is_self_compact": is_self_compact,
        "criterion": criterion,
        "note": note,
    }


def stone_cech_profile(space: Any) -> dict[str, Any]:
    """Full Stone-Čech profile combining all analyses and the named example registry.

    Keys
    ----
    is_compactifiable : Result
    embedding : Result
    extension : Result
    classification : dict
    named_examples : tuple[StoneCechDescriptor, ...]
    """
    return {
        "is_compactifiable": is_stone_cech_compactifiable(space),
        "embedding": stone_cech_embedding(space),
        "extension": stone_cech_extension(space),
        "classification": classify_stone_cech(space),
        "named_examples": get_named_stone_cech_examples(),
    }


__all__ = [
    "StoneCechDescriptor",
    "STONE_CECH_TYCHONOFF_TAGS",
    "COMPACT_HAUSDORFF_TAGS",
    "STONE_CECH_BLOCKING_TAGS",
    "get_named_stone_cech_examples",
    "is_stone_cech_compactifiable",
    "stone_cech_embedding",
    "stone_cech_extension",
    "classify_stone_cech",
    "stone_cech_profile",
]
