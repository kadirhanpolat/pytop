"""Topological vector spaces: locally convex, Fréchet, Banach, and key theorems.

Key theorems implemented
------------------------
- Hahn-Banach theorem: every continuous linear functional on a subspace of a
  locally convex space extends to a continuous linear functional on the whole space.
- Open Mapping theorem: a continuous surjective linear map between Fréchet spaces
  (in particular between Banach spaces) is an open map.
- Closed Graph theorem: a linear map between Fréchet spaces whose graph is closed
  is continuous.
- Uniform Boundedness Principle (Banach-Steinhaus): if a family of continuous
  linear functionals on a Banach space is pointwise bounded, it is uniformly bounded.
- Hierarchy: Hilbert ⊊ Banach ⊊ Fréchet ⊊ locally convex TVS ⊊ TVS.
- A TVS is Hausdorff iff {0} is closed (equivalently, iff it is T1).
- L^p(μ) for 0 < p < 1 is a TVS that is NOT locally convex.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class TVSProfile:
    """A curated topological vector space example."""

    key: str
    display_name: str
    tvs_type: str
    is_locally_convex: bool
    is_complete: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

TVS_POSITIVE_TAGS: set[str] = {
    "tvs", "topological_vector_space",
    "banach_space", "banach",
    "hilbert_space", "hilbert",
    "frechet_space", "frechet",
    "locally_convex", "locally_convex_space",
    "normed_space", "seminormed_space",
    "nuclear_space", "lf_space",
    "sobolev_space", "schwartz_space",
    "distribution_space", "lp_space",
    "lp_space_0_p_1", "lp_quasi_banach",
    "hardy_space_p_less_1",
}
TVS_NEGATIVE_TAGS: set[str] = {
    "not_tvs", "not_topological_vector_space",
    "topological_group_not_vector",
}
LOCALLY_CONVEX_TAGS: set[str] = {
    "locally_convex", "locally_convex_space",
    "banach_space", "banach",
    "hilbert_space", "hilbert",
    "frechet_space", "frechet",
    "normed_space", "seminormed_space",
    "nuclear_space", "lf_space",
    "sobolev_space", "schwartz_space",
    "distribution_space",
}
NOT_LOCALLY_CONVEX_TAGS: set[str] = {
    "not_locally_convex", "quasi_normed",
    "lp_space_0_p_1", "lp_quasi_banach",
    "hardy_space_p_less_1",
}
FRECHET_TAGS: set[str] = {
    "frechet_space", "frechet",
    "banach_space", "banach",
    "hilbert_space", "hilbert",
    "l2_space", "l2",
    "lp_space", "l_infinity", "c_zero",
    "sobolev_space",
    "smooth_functions_space", "c_infty_space",
    "schwartz_space",
}
BANACH_TAGS: set[str] = {
    "banach_space", "banach",
    "hilbert_space", "hilbert",
    "l2_space", "l2",
    "lp_space", "l_infinity", "c_zero",
    "sobolev_space",
}
HILBERT_TAGS: set[str] = {
    "hilbert_space", "hilbert",
    "l2_space", "l2",
}
HAHN_BANACH_TAGS: set[str] = {
    "locally_convex", "locally_convex_space",
    "banach_space", "banach",
    "hilbert_space", "hilbert",
    "frechet_space", "frechet",
    "normed_space", "seminormed_space",
    "nuclear_space", "sobolev_space",
}
OPEN_MAPPING_TAGS: set[str] = {
    "banach_space", "banach",
    "hilbert_space", "hilbert",
    "frechet_space", "frechet",
}


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


def _matches_any(tags: set[str], candidates: set[str]) -> bool:
    return bool(tags & candidates)


# ---------------------------------------------------------------------------
# Named example registry
# ---------------------------------------------------------------------------

def get_named_tvs_profiles() -> tuple[TVSProfile, ...]:
    """Return the registry of canonical TVS examples."""
    return (
        TVSProfile(
            key="hilbert_l2",
            display_name="L²[0,1] — Hilbert space",
            tvs_type="hilbert",
            is_locally_convex=True,
            is_complete=True,
            presentation_layer="main_text",
            focus=(
                "L²[0,1] with inner product <f,g> = integral f·g is the prototype Hilbert "
                "space. It is a Banach space (complete normed), Fréchet space, and locally "
                "convex TVS. The Hahn-Banach theorem applies; every continuous linear "
                "functional is of the form f ↦ <f, g> for some fixed g (Riesz representation). "
                "The Open Mapping and Closed Graph theorems hold for operators on L²."
            ),
            chapter_targets=("5", "28"),
        ),
        TVSProfile(
            key="banach_lp",
            display_name="L^p(μ) for 1 ≤ p < ∞ — Banach space",
            tvs_type="banach",
            is_locally_convex=True,
            is_complete=True,
            presentation_layer="main_text",
            focus=(
                "For 1 ≤ p < ∞, L^p(μ) is a Banach space (complete normed linear space). "
                "It is locally convex (the norm topology has a convex neighborhood basis). "
                "The Hahn-Banach theorem extends linear functionals from subspaces. "
                "The dual of L^p is L^q where 1/p + 1/q = 1 (for 1 < p < ∞). "
                "The Banach-Steinhaus principle guarantees uniform boundedness of "
                "pointwise-bounded families of linear operators."
            ),
            chapter_targets=("5", "28"),
        ),
        TVSProfile(
            key="frechet_smooth",
            display_name="C^∞(R) — Fréchet space of smooth functions",
            tvs_type="frechet",
            is_locally_convex=True,
            is_complete=True,
            presentation_layer="selected_block",
            focus=(
                "C^∞(R) with the topology of uniform convergence on compact subsets of "
                "all derivatives is a Fréchet space: completely metrizable locally convex "
                "TVS. It is NOT a Banach space (no compatible norm). The Open Mapping and "
                "Closed Graph theorems hold for linear maps between Fréchet spaces. "
                "The Schwartz space S(R) ⊂ C^∞(R) is also a Fréchet space, and its dual "
                "S'(R) (tempered distributions) is a locally convex space."
            ),
            chapter_targets=("5", "28"),
        ),
        TVSProfile(
            key="locally_convex_distributions",
            display_name="D'(R) — distributions (locally convex, not metrizable)",
            tvs_type="locally_convex",
            is_locally_convex=True,
            is_complete=True,
            presentation_layer="advanced_note",
            focus=(
                "The space D'(R) of Schwartz distributions (dual of C^∞_c(R) with the "
                "strict inductive limit topology) is locally convex and complete but NOT "
                "metrizable — hence not Fréchet. The Hahn-Banach theorem still applies. "
                "Its topology is given by a family of seminorms indexed by test functions. "
                "This space is the natural home of delta functions and distributional "
                "derivatives, and is a key example of a non-metrizable locally convex space."
            ),
            chapter_targets=("5", "28"),
        ),
        TVSProfile(
            key="quasi_banach_lp",
            display_name="L^p(0,1) for 0 < p < 1 — quasi-Banach (NOT locally convex)",
            tvs_type="tvs",
            is_locally_convex=False,
            is_complete=True,
            presentation_layer="advanced_note",
            focus=(
                "For 0 < p < 1, L^p(0,1) is a complete TVS with a translation-invariant "
                "metric d(f,g) = integral |f-g|^p. However, it is NOT locally convex: "
                "the only convex open sets are ∅ and the whole space. Therefore the "
                "Hahn-Banach theorem FAILS: the only continuous linear functional is "
                "identically zero. The Open Mapping theorem requires Fréchet spaces; "
                "it does not directly apply to L^p for p < 1."
            ),
            chapter_targets=("5", "28"),
        ),
    )


def tvs_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_tvs_profiles()))


def tvs_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_tvs_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def tvs_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from tvs_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_tvs_profiles():
        index.setdefault(p.tvs_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_locally_convex(space: Any) -> Result:
    """Check whether the TVS has a convex neighborhood basis at zero.

    A topological vector space is locally convex iff its topology has a basis
    of convex sets, equivalently if it is defined by a family of seminorms.
    Key facts:
    - All Banach, Hilbert, and Fréchet spaces are locally convex.
    - L^p for 0 < p < 1 is a complete TVS that is NOT locally convex.
    - The Hahn-Banach theorem requires local convexity.

    Decision layers
    ---------------
    1. Explicit not-locally-convex tags → false.
    2. Hilbert → true (inner product space has norm, norm defines convex balls).
    3. Banach → true (normed space: balls are convex).
    4. Fréchet → true (Fréchet spaces are locally convex by definition).
    5. Direct locally-convex / normed / seminormed tags → true.
    6. General TVS tag without local convexity info → unknown.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, NOT_LOCALLY_CONVEX_TAGS):
        blocking = next(t for t in tags if t in NOT_LOCALLY_CONVEX_TAGS)
        return Result.false(
            mode="theorem",
            value="locally_convex",
            justification=[
                f"Tag {blocking!r}: the space is explicitly not locally convex. "
                "For 0 < p < 1, L^p has no nonzero continuous linear functionals; "
                "the only convex open sets are ∅ and the whole space.",
            ],
            metadata={**base, "criterion": "not_locally_convex"},
        )

    if _matches_any(tags, HILBERT_TAGS):
        witness = next(t for t in tags if t in HILBERT_TAGS)
        return Result.true(
            mode="theorem",
            value="locally_convex",
            justification=[
                f"Tag {witness!r}: every Hilbert space is locally convex — "
                "the norm topology (from the inner product) has open balls as a "
                "convex neighborhood basis.",
            ],
            metadata={**base, "criterion": "hilbert", "witness": witness},
        )

    if _matches_any(tags, BANACH_TAGS):
        witness = next(t for t in tags if t in BANACH_TAGS)
        return Result.true(
            mode="theorem",
            value="locally_convex",
            justification=[
                f"Tag {witness!r}: every Banach space is locally convex — "
                "the open balls B(0, r) form a convex neighborhood basis at zero.",
            ],
            metadata={**base, "criterion": "banach", "witness": witness},
        )

    if _matches_any(tags, FRECHET_TAGS):
        witness = next(t for t in tags if t in FRECHET_TAGS)
        return Result.true(
            mode="theorem",
            value="locally_convex",
            justification=[
                f"Tag {witness!r}: every Fréchet space is locally convex by definition — "
                "it is a completely metrizable locally convex TVS.",
            ],
            metadata={**base, "criterion": "frechet", "witness": witness},
        )

    if _matches_any(tags, LOCALLY_CONVEX_TAGS):
        witness = next(t for t in tags if t in LOCALLY_CONVEX_TAGS)
        return Result.true(
            mode="theorem",
            value="locally_convex",
            justification=[
                f"Tag {witness!r}: the space is directly tagged as locally convex or "
                "as a type (normed, seminormed, nuclear) that implies local convexity.",
            ],
            metadata={**base, "criterion": "direct_tag", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="locally_convex",
        justification=[
            "Insufficient tags to determine local convexity. "
            "Supply tags such as 'locally_convex', 'banach_space', 'hilbert_space', "
            "'frechet_space', 'normed_space', or 'not_locally_convex'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_frechet_space(space: Any) -> Result:
    """Check whether the TVS is a Fréchet space.

    A Fréchet space is a completely metrizable locally convex topological vector
    space. Equivalently, it is a TVS whose topology is defined by a countable
    family of seminorms and is complete under the induced metric. Key facts:
    - Every Banach space is Fréchet (the norm gives one seminorm, completeness is inherited).
    - C^∞(R) and the Schwartz space S(R) are Fréchet but not Banach.
    - D'(R) (distributions) is locally convex and complete but NOT Fréchet (not metrizable).
    - The Open Mapping and Closed Graph theorems hold between Fréchet spaces.

    Decision layers
    ---------------
    1. Not-locally-convex → false (Fréchet requires local convexity).
    2. Hilbert → true (Hilbert ⊊ Banach ⊊ Fréchet).
    3. Banach → true.
    4. Direct Fréchet tags → true.
    5. Locally convex + not complete or not metrizable → false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, NOT_LOCALLY_CONVEX_TAGS):
        blocking = next(t for t in tags if t in NOT_LOCALLY_CONVEX_TAGS)
        return Result.false(
            mode="theorem",
            value="frechet_space",
            justification=[
                f"Tag {blocking!r}: Fréchet spaces must be locally convex; "
                "this space is not locally convex, so it cannot be Fréchet.",
            ],
            metadata={**base, "criterion": "not_locally_convex"},
        )

    if _matches_any(tags, HILBERT_TAGS):
        witness = next(t for t in tags if t in HILBERT_TAGS)
        return Result.true(
            mode="theorem",
            value="frechet_space",
            justification=[
                f"Tag {witness!r}: every Hilbert space is a Fréchet space "
                "(Hilbert ⊊ Banach ⊊ Fréchet in the TVS hierarchy).",
            ],
            metadata={**base, "criterion": "hilbert", "witness": witness},
        )

    if _matches_any(tags, BANACH_TAGS):
        witness = next(t for t in tags if t in BANACH_TAGS)
        return Result.true(
            mode="theorem",
            value="frechet_space",
            justification=[
                f"Tag {witness!r}: every Banach space is a Fréchet space — "
                "complete normed implies completely metrizable locally convex.",
            ],
            metadata={**base, "criterion": "banach", "witness": witness},
        )

    if _matches_any(tags, FRECHET_TAGS):
        witness = next(t for t in tags if t in FRECHET_TAGS)
        return Result.true(
            mode="theorem",
            value="frechet_space",
            justification=[f"Tag {witness!r}: the space is directly tagged as a Fréchet space."],
            metadata={**base, "criterion": "direct_tag", "witness": witness},
        )

    if _matches_any(tags, {"not_metrizable", "not_first_countable", "distribution_space", "lf_space"}):
        blocking = next(t for t in tags if t in {"not_metrizable", "not_first_countable", "distribution_space", "lf_space"})
        return Result.false(
            mode="theorem",
            value="frechet_space",
            justification=[
                f"Tag {blocking!r}: Fréchet spaces are metrizable (completely metrizable); "
                "a non-metrizable locally convex space such as D'(R) or an LF-space "
                "cannot be Fréchet.",
            ],
            metadata={**base, "criterion": "not_metrizable"},
        )

    return Result.unknown(
        mode="symbolic",
        value="frechet_space",
        justification=[
            "Insufficient tags to determine whether the space is Fréchet. "
            "Supply tags such as 'frechet_space', 'banach_space', 'hilbert_space', "
            "'smooth_functions_space', or 'not_locally_convex'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_banach_space(space: Any) -> Result:
    """Check whether the TVS is a Banach space.

    A Banach space is a complete normed linear space. It is Fréchet and locally
    convex. Key facts:
    - Every Hilbert space is Banach (the inner product gives a norm).
    - C^∞(R) is Fréchet but NOT Banach (no compatible norm).
    - The Hahn-Banach, Open Mapping, Closed Graph, and Banach-Steinhaus theorems
      all hold for Banach spaces.
    - A Fréchet space is Banach iff its topology is defined by a single norm.

    Decision layers
    ---------------
    1. Explicitly not Banach (Fréchet but not normed) → false.
    2. Hilbert → true.
    3. Direct Banach tags → true.
    4. Fréchet but not normed (C^∞, Schwartz) → false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"not_banach", "not_normable", "not_normed"}):
        blocking = next(t for t in tags if t in {"not_banach", "not_normable", "not_normed"})
        return Result.false(
            mode="theorem",
            value="banach_space",
            justification=[
                f"Tag {blocking!r}: the space is explicitly tagged as not a Banach space. "
                "A Fréchet space whose topology is not generated by any single norm "
                "cannot be a Banach space.",
            ],
            metadata={**base, "criterion": "not_banach"},
        )

    if _matches_any(tags, HILBERT_TAGS):
        witness = next(t for t in tags if t in HILBERT_TAGS)
        return Result.true(
            mode="theorem",
            value="banach_space",
            justification=[
                f"Tag {witness!r}: every Hilbert space is a Banach space — "
                "the inner product norm ||x|| = sqrt(<x,x>) makes it a complete normed space.",
            ],
            metadata={**base, "criterion": "hilbert", "witness": witness},
        )

    if _matches_any(tags, BANACH_TAGS):
        witness = next(t for t in tags if t in BANACH_TAGS)
        return Result.true(
            mode="theorem",
            value="banach_space",
            justification=[f"Tag {witness!r}: the space is directly tagged as a Banach space."],
            metadata={**base, "criterion": "direct_tag", "witness": witness},
        )

    if _matches_any(tags, {"smooth_functions_space", "c_infty_space", "schwartz_space",
                            "not_locally_convex", "not_normable"}):
        blocking = next(t for t in tags if t in {"smooth_functions_space", "c_infty_space",
                                                   "schwartz_space", "not_locally_convex", "not_normable"})
        return Result.false(
            mode="theorem",
            value="banach_space",
            justification=[
                f"Tag {blocking!r}: spaces like C^∞(R) or the Schwartz space are "
                "Fréchet but NOT Banach — their topologies are not generated by any norm.",
            ],
            metadata={**base, "criterion": "frechet_not_banach"},
        )

    return Result.unknown(
        mode="symbolic",
        value="banach_space",
        justification=[
            "Insufficient tags to determine whether the space is a Banach space. "
            "Supply tags such as 'banach_space', 'hilbert_space', 'lp_space', "
            "or 'not_normable'.",
        ],
        metadata={**base, "criterion": None},
    )


def hahn_banach_applicable(space: Any) -> Result:
    """Check whether the Hahn-Banach theorem applies to the space.

    The Hahn-Banach theorem states: if X is a locally convex TVS and f is a
    continuous linear functional on a subspace Y ⊆ X, then f extends to a
    continuous linear functional F on all of X with the same norm. Key facts:
    - Requires local convexity (fails for L^p, 0 < p < 1).
    - Geometric Hahn-Banach: in a locally convex space, a closed convex set
      and a disjoint compact convex set can be separated by a hyperplane.
    - Corollary: in a locally convex Hausdorff TVS, continuous linear functionals
      separate points.

    Decision layers
    ---------------
    1. Not locally convex → false (theorem explicitly fails).
    2. Hilbert → true (Riesz representation gives all functionals explicitly).
    3. Banach → true.
    4. Fréchet → true.
    5. Locally convex tags → true.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, NOT_LOCALLY_CONVEX_TAGS):
        blocking = next(t for t in tags if t in NOT_LOCALLY_CONVEX_TAGS)
        return Result.false(
            mode="theorem",
            value="hahn_banach_applicable",
            justification=[
                f"Tag {blocking!r}: the Hahn-Banach theorem requires local convexity. "
                "In L^p (0 < p < 1), the only continuous linear functional is identically "
                "zero — no nontrivial extensions exist.",
            ],
            metadata={**base, "criterion": "not_locally_convex"},
        )

    if _matches_any(tags, HILBERT_TAGS):
        witness = next(t for t in tags if t in HILBERT_TAGS)
        return Result.true(
            mode="theorem",
            value="hahn_banach_applicable",
            justification=[
                f"Tag {witness!r}: Hahn-Banach applies to all Hilbert spaces. "
                "Moreover, the Riesz representation theorem gives every continuous "
                "linear functional explicitly as f(x) = <x, y> for some y.",
            ],
            metadata={**base, "criterion": "hilbert", "witness": witness},
        )

    if _matches_any(tags, BANACH_TAGS | FRECHET_TAGS | HAHN_BANACH_TAGS):
        witness = next(t for t in tags if t in (BANACH_TAGS | FRECHET_TAGS | HAHN_BANACH_TAGS))
        return Result.true(
            mode="theorem",
            value="hahn_banach_applicable",
            justification=[
                f"Tag {witness!r}: the Hahn-Banach theorem applies to all locally convex "
                "TVS (including Banach and Fréchet spaces). Every continuous linear "
                "functional on a subspace extends to the whole space.",
            ],
            metadata={**base, "criterion": "locally_convex", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="hahn_banach_applicable",
        justification=[
            "Insufficient tags to determine Hahn-Banach applicability. "
            "Supply tags such as 'locally_convex', 'banach_space', 'frechet_space', "
            "or 'not_locally_convex'.",
        ],
        metadata={**base, "criterion": None},
    )


def open_mapping_theorem_holds(space: Any) -> Result:
    """Check whether the Open Mapping theorem applies to the space.

    The Open Mapping theorem: a continuous surjective linear map T: X → Y
    between Fréchet spaces (in particular Banach spaces) is an open map.
    The Closed Graph theorem is a consequence: a linear map T: X → Y between
    Fréchet spaces with closed graph is continuous. Key facts:
    - Both require the domain and codomain to be Fréchet (the Baire category
      theorem plays a key role in the proof).
    - Fails in general for locally convex spaces that are not Fréchet.
    - Corollary: a bijective continuous linear map between Fréchet spaces is
      a homeomorphism (its inverse is automatically continuous).

    Decision layers
    ---------------
    1. Not Fréchet (locally convex but not complete or not metrizable) → false.
    2. Hilbert → true.
    3. Banach → true.
    4. Fréchet tags → true.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"not_metrizable", "not_first_countable", "distribution_space",
                            "lf_space", "not_locally_convex", "not_banach"}):
        blocking = next(t for t in tags if t in {"not_metrizable", "not_first_countable",
                                                   "distribution_space", "lf_space",
                                                   "not_locally_convex", "not_banach"})
        return Result.false(
            mode="theorem",
            value="open_mapping_theorem_holds",
            justification=[
                f"Tag {blocking!r}: the Open Mapping theorem requires both domain and "
                "codomain to be Fréchet spaces. A non-metrizable locally convex space "
                "(e.g., D'(R)) or a non-locally-convex TVS does not support it in general.",
            ],
            metadata={**base, "criterion": "not_frechet"},
        )

    if _matches_any(tags, HILBERT_TAGS):
        witness = next(t for t in tags if t in HILBERT_TAGS)
        return Result.true(
            mode="theorem",
            value="open_mapping_theorem_holds",
            justification=[
                f"Tag {witness!r}: the Open Mapping theorem holds for all Hilbert spaces — "
                "a continuous surjective linear operator T: H₁ → H₂ is open. "
                "The Closed Graph theorem also holds: a linear T with closed graph is continuous.",
            ],
            metadata={**base, "criterion": "hilbert", "witness": witness},
        )

    if _matches_any(tags, BANACH_TAGS):
        witness = next(t for t in tags if t in BANACH_TAGS)
        return Result.true(
            mode="theorem",
            value="open_mapping_theorem_holds",
            justification=[
                f"Tag {witness!r}: the Open Mapping theorem holds for Banach spaces — "
                "the proof uses the Baire Category theorem applied to the complete metric "
                "space structure. Every continuous surjective linear map is open.",
            ],
            metadata={**base, "criterion": "banach", "witness": witness},
        )

    if _matches_any(tags, OPEN_MAPPING_TAGS | FRECHET_TAGS):
        witness = next(t for t in tags if t in (OPEN_MAPPING_TAGS | FRECHET_TAGS))
        return Result.true(
            mode="theorem",
            value="open_mapping_theorem_holds",
            justification=[
                f"Tag {witness!r}: the Open Mapping theorem (and its consequence, the "
                "Closed Graph theorem) holds for Fréchet spaces — the Baire Category "
                "theorem applies since Fréchet spaces are completely metrizable.",
            ],
            metadata={**base, "criterion": "frechet", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="open_mapping_theorem_holds",
        justification=[
            "Insufficient tags to determine Open Mapping theorem applicability. "
            "Supply tags such as 'banach_space', 'hilbert_space', 'frechet_space', "
            "or 'distribution_space'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_tvs(space: Any) -> dict[str, Any]:
    """Classify a topological vector space by its type in the TVS hierarchy.

    Keys
    ----
    tvs_type : str
        One of ``"hilbert"``, ``"banach"``, ``"frechet"``,
        ``"locally_convex"``, ``"tvs"``, ``"unknown"``.
    is_locally_convex : Result
    is_frechet : Result
    is_banach : Result
    hahn_banach : Result
    open_mapping : Result
    key_properties : list[str]
    representation : str
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    lc_r = is_locally_convex(space)
    fr_r = is_frechet_space(space)
    ba_r = is_banach_space(space)
    hb_r = hahn_banach_applicable(space)
    om_r = open_mapping_theorem_holds(space)

    if _matches_any(tags, HILBERT_TAGS):
        tvs_type = "hilbert"
    elif ba_r.is_true:
        tvs_type = "banach"
    elif fr_r.is_true:
        tvs_type = "frechet"
    elif lc_r.is_true:
        tvs_type = "locally_convex"
    elif _matches_any(tags, TVS_POSITIVE_TAGS):
        tvs_type = "tvs"
    else:
        tvs_type = "unknown"

    key_properties: list[str] = []
    if lc_r.is_true:
        key_properties.append("locally_convex")
    if fr_r.is_true:
        key_properties.append("frechet")
    if ba_r.is_true:
        key_properties.append("banach")
    if _matches_any(tags, HILBERT_TAGS):
        key_properties.append("hilbert")
    if hb_r.is_true:
        key_properties.append("hahn_banach")
    if om_r.is_true:
        key_properties.append("open_mapping")
    if _matches_any(tags, NOT_LOCALLY_CONVEX_TAGS):
        key_properties.append("not_locally_convex")

    return {
        "tvs_type": tvs_type,
        "is_locally_convex": lc_r,
        "is_frechet": fr_r,
        "is_banach": ba_r,
        "hahn_banach": hb_r,
        "open_mapping": om_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def tvs_profile(space: Any) -> dict[str, Any]:
    """Full TVS profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_tvs`.
    named_profiles : tuple[TVSProfile, ...]
        Registry of canonical TVS examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_tvs(space),
        "named_profiles": get_named_tvs_profiles(),
        "layer_summary": tvs_layer_summary(),
    }


__all__ = [
    "TVSProfile",
    "TVS_POSITIVE_TAGS",
    "TVS_NEGATIVE_TAGS",
    "LOCALLY_CONVEX_TAGS",
    "NOT_LOCALLY_CONVEX_TAGS",
    "FRECHET_TAGS",
    "BANACH_TAGS",
    "HILBERT_TAGS",
    "HAHN_BANACH_TAGS",
    "OPEN_MAPPING_TAGS",
    "get_named_tvs_profiles",
    "tvs_layer_summary",
    "tvs_chapter_index",
    "tvs_type_index",
    "is_locally_convex",
    "is_frechet_space",
    "is_banach_space",
    "hahn_banach_applicable",
    "open_mapping_theorem_holds",
    "classify_tvs",
    "tvs_profile",
]
