"""Shape theory: ANR/FANR classification, movability, and Čech invariants.

Key theorems implemented
------------------------
- Borsuk's ANR theorem: a compact metrizable space X is an ANR iff it is
  locally contractible (every point has a contractible neighbourhood in X).
- Every compact AR is an ANR; every ANR is an FANR; every FANR is movable.
- Compact polyhedra and compact manifolds (without boundary) are ANRs.
- The Warsaw circle is compact, connected, and metrizable, but NOT locally
  contractible at the limit arc, hence not an ANR, not an FANR, and not movable.
- The dyadic solenoid is compact, connected, metrizable, and not locally
  path-connected, hence not an ANR, not an FANR, and not movable.
- The Hawaiian earring is a Peano continuum (compact, connected, locally
  path-connected), hence movable by Borsuk's theorem, but NOT an ANR (local
  contractibility fails at the origin) and NOT an FANR (Čech H_1 is not
  finitely generated — the FANR condition requires shape domination by a
  compact ANR, which forces finitely generated Čech homology).
- Čech cohomology is a shape invariant: shape equivalent spaces have
  isomorphic Čech cohomology groups in every degree.
- For compact ANRs, Čech cohomology coincides with singular cohomology.
- Whitehead's theorem fails in shape theory: a shape morphism inducing
  isomorphisms on all Čech cohomology groups need not be a shape equivalence
  (the Warsaw circle and the circle share Čech cohomology but differ in shape).
- A compact metrizable space has trivial shape iff it is a compact AR
  (i.e., contractible and ANR), equivalently iff it is contractible and
  locally contractible.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from typing import Any

from .result import Result


@dataclass(frozen=True)
class ShapeProfile:
    """A curated shape-theory example."""

    key: str
    display_name: str
    shape_type: str
    is_anr: bool
    is_fanr: bool
    is_movable: bool
    is_shape_trivial: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

ANR_POSITIVE_TAGS: frozenset[str] = frozenset({
    "anr", "absolute_neighborhood_retract",
    "ar", "absolute_retract",
    "compact_manifold", "compact_manifold_no_boundary",
    "finite_cw_complex", "compact_polyhedron",
    "locally_contractible", "locally_contractible_compact",
    "compact_lie_group",
    "sphere", "torus", "projective_space",
    "compact_surface",
})

FANR_POSITIVE_TAGS: frozenset[str] = frozenset({
    "fanr", "fundamental_absolute_neighborhood_retract",
    "anr", "absolute_neighborhood_retract",
    "ar", "absolute_retract",
    "compact_polyhedron", "finite_cw_complex",
    "compact_manifold", "compact_lie_group",
})

MOVABLE_POSITIVE_TAGS: frozenset[str] = frozenset({
    "movable", "shape_movable",
    "fanr", "anr", "ar",
    "compact_polyhedron", "finite_cw_complex",
    "compact_manifold",
    "peano_continuum",
    "hawaiian_earring",
    "locally_path_connected_compact",
    "compact_surface",
    "compact_lie_group",
})

SHAPE_TRIVIAL_TAGS: frozenset[str] = frozenset({
    "contractible", "shape_trivial",
    "ar", "absolute_retract",
    "single_point", "point",
    "closed_ball", "convex_compact",
    "compact_contractible_anr",
    "hilbert_cube",
    "contractible_compact",
})

CECH_COMPUTABLE_TAGS: frozenset[str] = frozenset({
    "compact_metrizable", "compact_metric",
    "compact_hausdorff",
    "compact_polyhedron", "finite_cw_complex",
    "compact_manifold",
    "paracompact_hausdorff",
    "locally_compact_hausdorff",
    "locally_compact_metrizable",
})

NOT_ANR_TAGS: frozenset[str] = frozenset({
    "not_anr", "not_locally_contractible",
    "warsaw_circle",
    "solenoid", "dyadic_solenoid",
    "topologists_sine_curve",
    "hawaiian_earring",
    "not_locally_contractible_at_limit",
    "totally_path_disconnected_locally",
})

NOT_FANR_TAGS: frozenset[str] = frozenset({
    "not_fanr",
    "solenoid", "dyadic_solenoid",
    "warsaw_circle",
    "hawaiian_earring",
    "infinite_cech_homology",
    "not_shape_dominated_by_polyhedron",
})

NOT_MOVABLE_TAGS: frozenset[str] = frozenset({
    "not_movable",
    "warsaw_circle",
    "solenoid", "dyadic_solenoid",
    "pro_homotopy_nontrivial",
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


def _matches_any(tags: set[str], candidates: set[str] | frozenset[str]) -> bool:
    return bool(tags & candidates)


# ---------------------------------------------------------------------------
# Named example registry
# ---------------------------------------------------------------------------

def get_named_shape_profiles() -> tuple[ShapeProfile, ...]:
    """Return the registry of canonical shape-theory examples."""
    return (
        ShapeProfile(
            key="compact_polyhedron",
            display_name="P — compact polyhedron / finite CW complex",
            shape_type="anr",
            is_anr=True,
            is_fanr=True,
            is_movable=True,
            is_shape_trivial=False,
            presentation_layer="main_text",
            focus=(
                "A compact polyhedron (finite simplicial complex, or equivalently a "
                "finite CW complex) is the foundational object of classical homotopy "
                "theory. Every point in a finite CW complex lies in an open cell, "
                "which is homeomorphic to R^n and hence contractible; this makes "
                "finite CW complexes locally contractible. By Borsuk's ANR theorem "
                "(compact metrizable X is ANR iff locally contractible), every compact "
                "polyhedron is an ANR. Being an ANR, it is automatically an FANR "
                "and movable (the chain ANR ⊃ FANR ⊃ movable). For compact ANRs, "
                "shape theory coincides with homotopy theory: two compact ANRs are "
                "shape equivalent iff they are homotopy equivalent. "
                "Čech cohomology coincides with singular cohomology for ANRs. "
                "Examples: spheres S^n, tori T^n, projective spaces RP^n and CP^n, "
                "and all compact surfaces."
            ),
            chapter_targets=("6", "23", "48"),
        ),
        ShapeProfile(
            key="compact_ar",
            display_name="D^n — compact AR (closed ball / contractible ANR)",
            shape_type="shape_trivial",
            is_anr=True,
            is_fanr=True,
            is_movable=True,
            is_shape_trivial=True,
            presentation_layer="main_text",
            focus=(
                "A compact absolute retract (AR) is a compact metrizable space X that "
                "is a retract of every compact metrizable space in which it embeds. "
                "Equivalently, by Dugundji's theorem, every convex compact subset of a "
                "locally convex topological vector space is a compact AR. "
                "A compact AR is always an ANR (the retraction condition is stronger) "
                "and is contractible (the retraction contracts X to any point). "
                "Compact ARs therefore have trivial shape (shape equivalent to a point): "
                "a compact metrizable X has trivial shape iff X is a compact AR. "
                "Examples: closed balls D^n, the Hilbert cube [0,1]^omega, tree-like "
                "continua that are locally contractible. The fixed-point theorem of "
                "Brouwer (for D^n) and Schauder (for convex compact subsets of Banach spaces) "
                "applies to compact ARs."
            ),
            chapter_targets=("6", "23"),
        ),
        ShapeProfile(
            key="compact_manifold",
            display_name="M^n — closed compact manifold",
            shape_type="anr",
            is_anr=True,
            is_fanr=True,
            is_movable=True,
            is_shape_trivial=False,
            presentation_layer="main_text",
            focus=(
                "A closed compact manifold M^n (compact without boundary) is locally "
                "homeomorphic to R^n, hence locally contractible at every point. "
                "By Borsuk's ANR theorem, M^n is an ANR, and therefore an FANR and movable. "
                "Its shape equals its homotopy type. The shape classification of "
                "compact manifolds is thus equivalent to their homotopy classification. "
                "Key results: Poincaré duality holds for closed orientable manifolds; "
                "the h-cobordism theorem (Smale, dim ≥ 5) classifies manifolds with "
                "trivial Whitehead group; in dimension 3, Perelman's geometrisation "
                "theorem classifies all closed 3-manifolds. "
                "Examples: spheres S^n, tori T^n, real and complex projective spaces, "
                "compact Lie groups, and hyperbolic manifolds."
            ),
            chapter_targets=("6", "23", "48"),
        ),
        ShapeProfile(
            key="warsaw_circle",
            display_name="W — Warsaw circle",
            shape_type="not_movable",
            is_anr=False,
            is_fanr=False,
            is_movable=False,
            is_shape_trivial=False,
            presentation_layer="main_text",
            focus=(
                "The Warsaw circle W is constructed by taking the topologist's sine "
                "curve {(x, sin(1/x)) : 0 < x ≤ 1} and adding the segment {0} × [-1,1] "
                "together with an arc that connects the two 'ends' of the space. "
                "W is compact, connected, and metrizable, but NOT locally contractible "
                "at any point of the limit arc {0} × [-1,1]: every neighbourhood of "
                "such a point contains oscillating sine-curve arcs that cannot be "
                "simultaneously contracted. Hence W is NOT an ANR (by Borsuk's theorem). "
                "W is NOT movable: the pro-fundamental group of W is non-stable and "
                "detects a non-trivial obstruction. "
                "Crucially, the Čech cohomology of W equals that of the circle S^1 "
                "(Ȟ^1(W;Z) ≅ Z), yet W and S^1 are NOT shape equivalent — "
                "illustrating that Čech cohomology alone does not determine shape "
                "(Whitehead's theorem fails in shape theory)."
            ),
            chapter_targets=("6", "23", "48"),
        ),
        ShapeProfile(
            key="solenoid",
            display_name="Σ — dyadic solenoid",
            shape_type="not_movable",
            is_anr=False,
            is_fanr=False,
            is_movable=False,
            is_shape_trivial=False,
            presentation_layer="selected_block",
            focus=(
                "The dyadic solenoid Σ is the inverse limit of the system "
                "S^1 ← S^1 ← S^1 ← ··· where each bonding map is the degree-2 "
                "covering map z → z^2. Σ is compact, connected, and metrizable. "
                "Locally, Σ is homeomorphic to the product (Cantor set) × (open arc), "
                "so it is totally path-disconnected transversally — in particular NOT "
                "locally path-connected at most points. Consequently Σ is NOT locally "
                "contractible and NOT an ANR. "
                "Σ is NOT movable: the pro-homotopy system of Σ is the inverse system "
                "Z ← Z ← Z ← ··· (multiplication by 2 at each step), which does not "
                "stabilise. The Čech cohomology of Σ is: "
                "Ȟ^0(Σ;Z) ≅ Z, Ȟ^1(Σ;Z) ≅ Z[1/2] (the dyadic rationals). "
                "Solenoids appear as strange attractors in dynamical systems "
                "(Smale's horseshoe) and as universal covers of certain foliations."
            ),
            chapter_targets=("23", "48"),
        ),
        ShapeProfile(
            key="hawaiian_earring",
            display_name="H — Hawaiian earring",
            shape_type="movable",
            is_anr=False,
            is_fanr=False,
            is_movable=True,
            is_shape_trivial=False,
            presentation_layer="selected_block",
            focus=(
                "The Hawaiian earring H is the union of circles C_n of radius 1/n "
                "centered at (1/n, 0) in R^2 for n = 1, 2, 3, .... "
                "H is compact, connected, and locally path-connected (Peano continuum): "
                "every neighbourhood of the origin contains arcs of arbitrarily small "
                "circles, providing local path-connectivity. By Borsuk's theorem, "
                "every Peano continuum is movable, so H is movable. "
                "However, H is NOT locally contractible at the origin: no neighbourhood "
                "of (0,0) in H can be contracted to a point (the larger circles escape "
                "any such neighbourhood). By Borsuk's ANR theorem, H is NOT an ANR. "
                "H is NOT an FANR: its first Čech homology group Ȟ_1(H;Z) is not "
                "finitely generated (it contains a copy of the countable product Z^omega), "
                "while every FANR must have finitely generated Čech homology groups "
                "(since FANR spaces are shape dominated by compact polyhedra). "
                "The fundamental group π_1(H, 0) is the 'Hawaiian earring group', "
                "which properly contains the free group on countably many generators."
            ),
            chapter_targets=("23", "48"),
        ),
    )


def shape_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_shape_profiles()))


def shape_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_shape_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def shape_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from shape_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_shape_profiles():
        index.setdefault(p.shape_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_anr(space: Any) -> Result:
    """Check whether space is an absolute neighbourhood retract (ANR).

    A compact metrizable space X is an ANR iff it is locally contractible:
    every point x has a neighbourhood U such that the inclusion U → X is
    null-homotopic (i.e., U contracts to a point within X). Key facts:
    - Compact manifolds, compact polyhedra, and finite CW complexes are ANRs.
    - Every compact AR is an ANR (but not every ANR is an AR).
    - The Warsaw circle is NOT an ANR (not locally contractible at limit arc).
    - The solenoid is NOT an ANR (locally like Cantor × arc, not contractible).
    - The Hawaiian earring is NOT an ANR (not locally contractible at origin).
    - Being an ANR implies being an FANR, which implies being movable.
    - Two compact ANRs are shape equivalent iff they are homotopy equivalent.

    Decision layers
    ---------------
    1. Explicit ANR / AR tag -> true.
    2. Compact manifold (locally Euclidean, hence locally contractible) -> true.
    3. Finite CW complex / compact polyhedron -> true.
    4. Locally contractible compact metrizable tag -> true.
    5. Not-locally-contractible / Warsaw circle / solenoid / Hawaiian earring -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"anr", "absolute_neighborhood_retract",
                            "ar", "absolute_retract"}):
        witness = next(t for t in tags if t in {"anr", "absolute_neighborhood_retract",
                                                  "ar", "absolute_retract"})
        return Result.true(
            mode="theorem",
            value="anr",
            justification=[
                f"Tag {witness!r}: the space is an absolute neighbourhood retract — "
                "a compact metrizable space that is a neighbourhood retract of every "
                "compact metrizable space in which it embeds.",
            ],
            metadata={**base, "criterion": "explicit_anr_tag", "witness": witness},
        )

    if _matches_any(tags, {"compact_manifold", "compact_manifold_no_boundary",
                            "compact_surface", "compact_lie_group",
                            "sphere", "torus", "projective_space"}):
        witness = next(t for t in tags if t in {"compact_manifold",
                                                   "compact_manifold_no_boundary",
                                                   "compact_surface", "compact_lie_group",
                                                   "sphere", "torus", "projective_space"})
        return Result.true(
            mode="theorem",
            value="anr",
            justification=[
                f"Tag {witness!r}: compact manifolds are locally Euclidean (locally "
                "homeomorphic to R^n), hence locally contractible at every point. "
                "By Borsuk's ANR theorem, every locally contractible compact metrizable "
                "space is an ANR.",
            ],
            metadata={**base, "criterion": "compact_manifold_anr", "witness": witness},
        )

    if _matches_any(tags, {"finite_cw_complex", "compact_polyhedron"}):
        witness = next(t for t in tags if t in {"finite_cw_complex", "compact_polyhedron"})
        return Result.true(
            mode="theorem",
            value="anr",
            justification=[
                f"Tag {witness!r}: every compact polyhedron (finite CW complex) is an ANR. "
                "Each point lies in an open cell homeomorphic to R^n, which provides "
                "the local contractibility required by Borsuk's ANR theorem.",
            ],
            metadata={**base, "criterion": "compact_polyhedron_anr", "witness": witness},
        )

    if _matches_any(tags, {"locally_contractible", "locally_contractible_compact"}):
        witness = next(t for t in tags if t in {"locally_contractible",
                                                   "locally_contractible_compact"})
        return Result.true(
            mode="theorem",
            value="anr",
            justification=[
                f"Tag {witness!r}: Borsuk's ANR theorem — a compact metrizable space is "
                "an ANR if and only if it is locally contractible. Local contractibility "
                "is the necessary and sufficient condition.",
            ],
            metadata={**base, "criterion": "locally_contractible_borsuk", "witness": witness},
        )

    if _matches_any(tags, NOT_ANR_TAGS):
        blocking = next(t for t in tags if t in NOT_ANR_TAGS)
        return Result.false(
            mode="theorem",
            value="anr",
            justification=[
                f"Tag {blocking!r}: the space is not locally contractible and therefore "
                "not an ANR. Classic examples include the Warsaw circle (not locally "
                "contractible at the limit arc), the solenoid (locally Cantor × arc), "
                "and the Hawaiian earring (not locally contractible at the origin).",
            ],
            metadata={**base, "criterion": "not_locally_contractible", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="anr",
        justification=[
            "Insufficient tags to determine ANR status. "
            "Supply tags such as 'anr', 'compact_manifold', 'finite_cw_complex', "
            "'locally_contractible', 'warsaw_circle', 'solenoid', or 'hawaiian_earring'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_fanr(space: Any) -> Result:
    """Check whether space is a fundamental absolute neighbourhood retract (FANR).

    A compact metrizable space X is an FANR if it is shape dominated by a compact
    ANR: there exist shape morphisms f: X → P (P a compact ANR) and g: P → X
    with g ∘ f shape-homotopic to id_X. Key facts:
    - Every ANR is an FANR (take P = X in the definition).
    - Every FANR is movable (domination by an ANR implies movability).
    - An FANR must have finitely generated Čech cohomology and homology groups.
    - The Hawaiian earring is movable but NOT an FANR (Ȟ_1 is not finitely generated).
    - The Warsaw circle and solenoid are neither FANR nor movable.

    Decision layers
    ---------------
    1. Explicit FANR / ANR / AR tag -> true.
    2. Compact polyhedron or compact manifold (ANRs) -> true.
    3. FANR tag -> true.
    4. Hawaiian earring, solenoid, Warsaw circle (not FANR) -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, FANR_POSITIVE_TAGS):
        witness = next(t for t in tags if t in FANR_POSITIVE_TAGS)
        return Result.true(
            mode="theorem",
            value="fanr",
            justification=[
                f"Tag {witness!r}: the space is an FANR (fundamental absolute neighbourhood "
                "retract). It is shape dominated by a compact ANR — there exist shape "
                "morphisms f: X → P and g: P → X with g ∘ f ≃ id_X in the shape category.",
            ],
            metadata={**base, "criterion": "fanr_positive_tag", "witness": witness},
        )

    if _matches_any(tags, NOT_FANR_TAGS):
        blocking = next(t for t in tags if t in NOT_FANR_TAGS)
        return Result.false(
            mode="theorem",
            value="fanr",
            justification=[
                f"Tag {blocking!r}: the space is not an FANR. Either its Čech homology "
                "groups are not finitely generated (Hawaiian earring: Ȟ_1 contains Z^omega), "
                "or its pro-homotopy system does not stabilise (solenoid, Warsaw circle), "
                "preventing shape domination by any compact polyhedron.",
            ],
            metadata={**base, "criterion": "not_fanr_tag", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="fanr",
        justification=[
            "Insufficient tags to determine FANR status. "
            "Supply tags such as 'fanr', 'anr', 'compact_polyhedron', 'compact_manifold', "
            "'hawaiian_earring', 'solenoid', or 'warsaw_circle'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_movable(space: Any) -> Result:
    """Check whether space is movable in the sense of Borsuk.

    A compact metrizable space X (embedded in the Hilbert cube Q) is movable if
    for every open neighbourhood U of X in Q there exists an open neighbourhood V
    of X in Q such that the inclusion V → U is null-homotopic in U. Key facts:
    - ANR ⊂ FANR ⊂ movable (the implications are strict).
    - Every Peano continuum (compact connected locally path-connected metrizable space)
      is movable (Borsuk's theorem).
    - The Hawaiian earring is a Peano continuum, hence movable.
    - The Warsaw circle is NOT movable (pro-fundamental group does not stabilise).
    - The dyadic solenoid is NOT movable (pro-homotopy obstruction).
    - Movability is a shape invariant.

    Decision layers
    ---------------
    1. Explicit movable / FANR / ANR / AR tag -> true.
    2. Compact polyhedron / manifold / Lie group (ANRs) -> true.
    3. Peano continuum (locally path-connected compact metrizable) -> true.
    4. Hawaiian earring (Peano continuum, movable but not ANR/FANR) -> true.
    5. Warsaw circle / solenoid (not movable) -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"movable", "shape_movable", "fanr", "anr",
                            "ar", "absolute_retract", "absolute_neighborhood_retract"}):
        witness = next(t for t in tags if t in {"movable", "shape_movable", "fanr",
                                                   "anr", "ar", "absolute_retract",
                                                   "absolute_neighborhood_retract"})
        return Result.true(
            mode="theorem",
            value="movable",
            justification=[
                f"Tag {witness!r}: the space is movable. Every FANR and ANR is movable; "
                "an explicit movable tag confirms this property directly.",
            ],
            metadata={**base, "criterion": "explicit_movable_tag", "witness": witness},
        )

    if _matches_any(tags, {"compact_polyhedron", "finite_cw_complex",
                            "compact_manifold", "compact_lie_group",
                            "sphere", "torus", "compact_surface"}):
        witness = next(t for t in tags if t in {"compact_polyhedron", "finite_cw_complex",
                                                   "compact_manifold", "compact_lie_group",
                                                   "sphere", "torus", "compact_surface"})
        return Result.true(
            mode="theorem",
            value="movable",
            justification=[
                f"Tag {witness!r}: compact polyhedra and manifolds are ANRs (locally "
                "contractible), hence FANRs, hence movable. "
                "The chain ANR ⊂ FANR ⊂ movable applies.",
            ],
            metadata={**base, "criterion": "compact_polyhedron_movable", "witness": witness},
        )

    if _matches_any(tags, {"peano_continuum", "locally_path_connected_compact",
                            "hawaiian_earring"}):
        witness = next(t for t in tags if t in {"peano_continuum",
                                                   "locally_path_connected_compact",
                                                   "hawaiian_earring"})
        return Result.true(
            mode="theorem",
            value="movable",
            justification=[
                f"Tag {witness!r}: Borsuk's theorem — every Peano continuum (compact, "
                "connected, locally path-connected, metrizable) is movable. The Hawaiian "
                "earring is a Peano continuum: it is locally path-connected everywhere, "
                "including at the origin where arcs of small circles provide local paths.",
            ],
            metadata={**base, "criterion": "peano_continuum_movable", "witness": witness},
        )

    if _matches_any(tags, NOT_MOVABLE_TAGS):
        blocking = next(t for t in tags if t in NOT_MOVABLE_TAGS)
        return Result.false(
            mode="theorem",
            value="movable",
            justification=[
                f"Tag {blocking!r}: the space is NOT movable. The Warsaw circle and the "
                "dyadic solenoid have non-stable pro-fundamental groups — the inverse "
                "system of fundamental groups of their neighbourhoods does not stabilise, "
                "providing an obstruction to movability.",
            ],
            metadata={**base, "criterion": "not_movable_tag", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="movable",
        justification=[
            "Insufficient tags to determine movability. "
            "Supply tags such as 'movable', 'peano_continuum', 'fanr', 'anr', "
            "'compact_polyhedron', 'hawaiian_earring', 'warsaw_circle', or 'solenoid'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_trivial_shape(space: Any) -> Result:
    """Check whether space has trivial shape (shape equivalent to a point).

    A compact metrizable space X has trivial shape iff X is a compact AR
    (absolute retract), equivalently iff X is contractible and an ANR.
    Key facts:
    - Closed balls D^n, the Hilbert cube [0,1]^omega, and contractible compact
      polyhedra are compact ARs and have trivial shape.
    - A contractible compact polyhedron is an AR (Whitehead's theorem applies:
      contractible ANR ⟹ AR).
    - The circle S^1 does NOT have trivial shape (Ȟ^1(S^1;Z) ≅ Z ≠ 0).
    - The Warsaw circle has non-trivial shape (same Čech cohomology as S^1).
    - Trivial shape implies all Čech cohomology groups vanish in positive degrees.

    Decision layers
    ---------------
    1. Explicit AR / contractible AR / single point tag -> true.
    2. Convex compact subset of locally convex TVS (Dugundji: compact AR) -> true.
    3. Non-trivial Čech cohomology / known non-contractible space -> false.
    4. Not locally contractible (not ANR) -> false (non-ANR cannot be AR).
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, SHAPE_TRIVIAL_TAGS):
        witness = next(t for t in tags if t in SHAPE_TRIVIAL_TAGS)
        return Result.true(
            mode="theorem",
            value="trivial_shape",
            justification=[
                f"Tag {witness!r}: the space has trivial shape — it is a compact AR "
                "(absolute retract), contractible and locally contractible. "
                "Its shape is the same as that of a single point.",
            ],
            metadata={**base, "criterion": "compact_ar_trivial_shape", "witness": witness},
        )

    if _matches_any(tags, {"nontrivial_cech_cohomology", "nonzero_cech_h1",
                            "sphere", "torus", "projective_space",
                            "compact_surface_positive_genus",
                            "warsaw_circle", "solenoid", "hawaiian_earring",
                            "not_contractible"}):
        blocking = next(t for t in tags if t in {
            "nontrivial_cech_cohomology", "nonzero_cech_h1",
            "sphere", "torus", "projective_space",
            "compact_surface_positive_genus",
            "warsaw_circle", "solenoid", "hawaiian_earring",
            "not_contractible",
        })
        return Result.false(
            mode="theorem",
            value="trivial_shape",
            justification=[
                f"Tag {blocking!r}: the space does not have trivial shape. "
                "Non-trivial Čech cohomology or known non-contractibility obstructs "
                "shape equivalence with a point. For example, S^1 has Ȟ^1 ≅ Z, "
                "and the Warsaw circle shares this despite not being homotopy equivalent "
                "to S^1.",
            ],
            metadata={**base, "criterion": "nontrivial_shape", "witness": blocking},
        )

    if _matches_any(tags, NOT_ANR_TAGS):
        blocking = next(t for t in tags if t in NOT_ANR_TAGS)
        return Result.false(
            mode="theorem",
            value="trivial_shape",
            justification=[
                f"Tag {blocking!r}: the space is not locally contractible, hence not an "
                "ANR. A compact AR must be locally contractible (it is in particular an ANR). "
                "Spaces that fail local contractibility cannot have trivial shape.",
            ],
            metadata={**base, "criterion": "not_anr_not_ar"},
        )

    return Result.unknown(
        mode="symbolic",
        value="trivial_shape",
        justification=[
            "Insufficient tags to determine whether the shape is trivial. "
            "Supply tags such as 'ar', 'contractible', 'closed_ball', 'hilbert_cube', "
            "'single_point', 'sphere', 'torus', 'warsaw_circle', or 'not_contractible'.",
        ],
        metadata={**base, "criterion": None},
    )


def cech_cohomology_applicable(space: Any) -> Result:
    """Check whether Čech cohomology is the appropriate cohomology theory.

    Čech cohomology Ȟ^*(X; G) is defined for any topological space X via the
    direct limit of Čech cochains over open covers. Key facts:
    - Čech cohomology is a shape invariant: shape equivalent spaces have
      isomorphic Čech cohomology groups.
    - For compact ANRs, Čech cohomology coincides with singular cohomology.
    - For compact metrizable spaces, Čech cohomology is computed via an
      inverse system of polyhedra (Čech nerve construction).
    - For paracompact Hausdorff spaces, Čech cohomology agrees with sheaf
      cohomology (with constant coefficients).
    - Čech cohomology distinguishes the Warsaw circle from the circle in
      pro-homotopy, but NOT in Čech cohomology (both have Ȟ^1 ≅ Z).

    Decision layers
    ---------------
    1. Compact polyhedron / manifold (ANR: Čech = singular) -> true.
    2. Compact metrizable / compact Hausdorff -> true.
    3. Paracompact Hausdorff / locally compact Hausdorff -> true.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"compact_polyhedron", "finite_cw_complex",
                            "compact_manifold", "anr", "ar"}):
        witness = next(t for t in tags if t in {"compact_polyhedron", "finite_cw_complex",
                                                   "compact_manifold", "anr", "ar"})
        return Result.true(
            mode="theorem",
            value="cech_applicable",
            justification=[
                f"Tag {witness!r}: compact ANR. Čech cohomology is applicable and, "
                "for compact ANRs, coincides with singular cohomology. "
                "The Čech nerve construction gives a direct limit of finite polyhedra "
                "whose cohomology stabilises to the singular cohomology of the space.",
            ],
            metadata={**base, "criterion": "compact_anr_cech_equals_singular",
                       "witness": witness},
        )

    if _matches_any(tags, {"compact_metrizable", "compact_metric", "compact_hausdorff"}):
        witness = next(t for t in tags if t in {"compact_metrizable", "compact_metric",
                                                   "compact_hausdorff"})
        return Result.true(
            mode="theorem",
            value="cech_applicable",
            justification=[
                f"Tag {witness!r}: compact metrizable (or Hausdorff) space. "
                "Čech cohomology is well-defined and is the correct shape-invariant "
                "cohomology theory. The Warsaw circle and solenoid are computed this way.",
            ],
            metadata={**base, "criterion": "compact_metrizable_cech", "witness": witness},
        )

    if _matches_any(tags, {"paracompact_hausdorff", "locally_compact_hausdorff",
                            "locally_compact_metrizable"}):
        witness = next(t for t in tags if t in {"paracompact_hausdorff",
                                                   "locally_compact_hausdorff",
                                                   "locally_compact_metrizable"})
        return Result.true(
            mode="theorem",
            value="cech_applicable",
            justification=[
                f"Tag {witness!r}: paracompact or locally compact Hausdorff space. "
                "Čech cohomology is applicable and agrees with sheaf cohomology "
                "(with constant coefficients) for paracompact Hausdorff spaces.",
            ],
            metadata={**base, "criterion": "paracompact_cech", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="cech_applicable",
        justification=[
            "Insufficient tags to determine Čech cohomology applicability. "
            "Supply tags such as 'compact_metrizable', 'compact_hausdorff', "
            "'compact_polyhedron', 'paracompact_hausdorff', or 'locally_compact_hausdorff'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_shape(space: Any) -> dict[str, Any]:
    """Classify the shape-theoretic properties of space.

    Keys
    ----
    shape_class : str
        One of ``"shape_trivial"``, ``"anr"``, ``"fanr"``, ``"movable"``,
        ``"not_movable"``, ``"unknown"``.
    is_anr : Result
    is_fanr : Result
    is_movable : Result
    has_trivial_shape : Result
    cech_applicable : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    anr_r = is_anr(space)
    fanr_r = is_fanr(space)
    mov_r = is_movable(space)
    trivial_r = has_trivial_shape(space)
    cech_r = cech_cohomology_applicable(space)

    if trivial_r.is_true:
        shape_class = "shape_trivial"
    elif anr_r.is_true:
        shape_class = "anr"
    elif fanr_r.is_true:
        shape_class = "fanr"
    elif mov_r.is_true:
        shape_class = "movable"
    elif mov_r.is_false:
        shape_class = "not_movable"
    else:
        shape_class = "unknown"

    key_properties: list[str] = []
    if trivial_r.is_true:
        key_properties.append("trivial_shape")
    if anr_r.is_true:
        key_properties.append("anr")
    if fanr_r.is_true:
        key_properties.append("fanr")
    if mov_r.is_true:
        key_properties.append("movable")
    if mov_r.is_false:
        key_properties.append("not_movable")
    if cech_r.is_true:
        key_properties.append("cech_cohomology_applicable")
    if anr_r.is_false:
        key_properties.append("not_anr")
    if fanr_r.is_false:
        key_properties.append("not_fanr")

    return {
        "shape_class": shape_class,
        "is_anr": anr_r,
        "is_fanr": fanr_r,
        "is_movable": mov_r,
        "has_trivial_shape": trivial_r,
        "cech_applicable": cech_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def shape_profile(space: Any) -> dict[str, Any]:
    """Full shape-theory profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_shape`.
    named_profiles : tuple[ShapeProfile, ...]
        Registry of canonical shape-theory examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_shape(space),
        "named_profiles": get_named_shape_profiles(),
        "layer_summary": shape_layer_summary(),
    }


# ---------------------------------------------------------------------------
# Computational engines (from raw simplicial data)
# ---------------------------------------------------------------------------

def _face_close_shape(simplices: list[list[Any]]) -> list[list[Any]]:
    seen: set[frozenset[Any]] = set()
    result: list[list[Any]] = []
    for s in simplices:
        for r in range(1, len(s) + 1):
            for face in combinations(s, r):
                fs = frozenset(face)
                if fs not in seen:
                    seen.add(fs)
                    result.append(list(face))
    return result


def link_complex(simplices: list[list[Any]], vertex: Any) -> list[list[Any]]:
    """Return the link of ``vertex`` in the simplicial complex.

    lk(K, v) = {σ \\ {v} : σ ∈ K, v ∈ σ, |σ| ≥ 2}.

    The result is face-closed.

    Parameters
    ----------
    simplices:
        List of simplices as vertex lists.
    vertex:
        The vertex whose link is computed.

    Returns
    -------
    list[list[Any]]
        Face-closed simplices of lk(K, v).

    Examples
    --------
    Link of vertex 0 in a filled triangle:

    >>> link_complex([[0,1,2],[0,1],[0,2],[1,2],[0],[1],[2]], 0)
    [[1], [2], [1, 2]]
    """
    link_faces: set[frozenset[Any]] = set()
    for s in simplices:
        vs = frozenset(s)
        if vertex in vs and len(vs) >= 2:
            link_faces.add(vs - {vertex})
    if not link_faces:
        return []
    seen: set[frozenset[Any]] = set()
    result: list[list[Any]] = []
    for face in link_faces:
        for r in range(1, len(face) + 1):
            for sub in combinations(sorted(face, key=repr), r):
                fs = frozenset(sub)
                if fs not in seen:
                    seen.add(fs)
                    result.append(list(sub))
    return result


def is_manifold_triangulation(simplices: list[list[Any]], n: int) -> bool:
    """Check whether K is a triangulation of a closed n-manifold.

    A compact simplicial complex K triangulates a closed n-manifold iff
    every vertex link lk(K, v) has the homology of S^{n-1}:
    H_{n-1}(lk(v); ℤ) = ℤ and H_k(lk(v); ℤ) = 0 for k ≠ n-1.

    Parameters
    ----------
    simplices:
        List of simplices as vertex lists.
    n:
        Expected manifold dimension (≥ 1).

    Returns
    -------
    bool

    Examples
    --------
    The boundary of a tetrahedron triangulates S²:

    >>> bdry = [[0,1,2],[0,1,3],[0,2,3],[1,2,3],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3],[0],[1],[2],[3]]
    >>> is_manifold_triangulation(bdry, 2)
    True
    """
    if n < 1:
        raise ValueError(f"Manifold dimension must be ≥ 1, got {n!r}")
    from .homotopy import has_sphere_homology

    closed = _face_close_shape(simplices)
    vertices: set[Any] = set()
    for s in closed:
        vertices.update(s)

    for v in vertices:
        lk = link_complex(closed, v)
        if not lk:
            return False
        if not has_sphere_homology(lk, n - 1):
            return False
    return True


def has_trivial_shape_sc(simplices: list[list[Any]]) -> bool:
    """Check whether a finite simplicial complex has trivial shape.

    A compact polyhedron K has trivial shape iff it is contractible:
    H₀(K; ℤ) = ℤ and H_k(K; ℤ) = 0 for k ≥ 1.
    For compact polyhedra (always ANRs), trivial shape equals compact AR.

    Parameters
    ----------
    simplices:
        List of simplices as vertex lists.

    Returns
    -------
    bool

    Examples
    --------
    A filled triangle is contractible:

    >>> has_trivial_shape_sc([[0,1,2],[0,1],[0,2],[1,2],[0],[1],[2]])
    True

    The circle (boundary of triangle) is not contractible:

    >>> has_trivial_shape_sc([[0,1],[1,2],[2,0]])
    False
    """
    from .homotopy import is_contractible_simplicial
    return is_contractible_simplicial(simplices)


def shape_anr_check_sc(simplices: list[list[Any]]) -> dict[str, Any]:
    """Shape-theoretic classification of a finite simplicial complex.

    Every finite simplicial complex is a compact polyhedron, hence always
    an ANR, FANR, and movable.  The key computed quantity is whether K has
    trivial shape (= K is contractible = K is a compact AR).

    Parameters
    ----------
    simplices:
        List of simplices as vertex lists.

    Returns
    -------
    dict with keys:
        ``is_anr`` : bool — always True
        ``is_fanr`` : bool — always True
        ``is_movable`` : bool — always True
        ``has_trivial_shape`` : bool — True iff K is contractible
        ``shape_class`` : str — ``"compact_ar"`` or ``"anr"``
        ``vertex_count`` : int
        ``max_simplex_dim`` : int

    Examples
    --------
    A cone is contractible (compact AR):

    >>> r = shape_anr_check_sc([[0,1],[1,2],[0,2],[0],[1],[2]])
    >>> r['is_anr'], r['shape_class']
    (True, 'anr')
    """
    closed = _face_close_shape(simplices)
    trivial = has_trivial_shape_sc(closed)
    vertices: set[Any] = set()
    max_dim = 0
    for s in closed:
        vertices.update(s)
        if s:
            max_dim = max(max_dim, len(s) - 1)

    return {
        "is_anr": True,
        "is_fanr": True,
        "is_movable": True,
        "has_trivial_shape": trivial,
        "shape_class": "compact_ar" if trivial else "anr",
        "vertex_count": len(vertices),
        "max_simplex_dim": max_dim,
    }


__all__ = [
    "ShapeProfile",
    "ANR_POSITIVE_TAGS",
    "FANR_POSITIVE_TAGS",
    "MOVABLE_POSITIVE_TAGS",
    "SHAPE_TRIVIAL_TAGS",
    "CECH_COMPUTABLE_TAGS",
    "NOT_ANR_TAGS",
    "NOT_FANR_TAGS",
    "NOT_MOVABLE_TAGS",
    "get_named_shape_profiles",
    "shape_layer_summary",
    "shape_chapter_index",
    "shape_type_index",
    "is_anr",
    "is_fanr",
    "is_movable",
    "has_trivial_shape",
    "cech_cohomology_applicable",
    "classify_shape",
    "shape_profile",
    "link_complex",
    "is_manifold_triangulation",
    "has_trivial_shape_sc",
    "shape_anr_check_sc",
]
