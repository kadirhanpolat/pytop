"""Combinatorial topology: simplicial complexes, CW complexes, Euler characteristic,
simplicial homology, nerve theorem, and collapsibility.

Key theorems implemented
------------------------
- Euler's formula (1758 / Poincaré generalization): for a finite simplicial complex K
  the Euler characteristic is chi(K) = sum_{k>=0} (-1)^k f_k where f_k is the number
  of k-simplices. For a convex polyhedron: V - E + F = 2. Euler characteristic is a
  homotopy invariant: homeomorphic spaces have equal chi.
- Simplicial homology: for a finite simplicial complex K with an orientation, the
  k-th chain group C_k(K) is the free abelian group on k-simplices. The boundary
  map partial_k: C_k -> C_{k-1} satisfies partial_{k-1} circ partial_k = 0. The
  k-th homology group is H_k(K) = ker(partial_k) / im(partial_{k+1}). Key invariant:
  the Betti numbers beta_k = rank(H_k) and torsion subgroups.
- CW complexes: a CW complex X is built inductively — start with a discrete set X^0
  (0-cells), attach 1-cells via maps S^0 -> X^0 to get X^1, then 2-cells via maps
  S^1 -> X^1, etc. The k-th cellular chain group is C_k^{CW} = H_k(X^k, X^{k-1})
  and the cellular boundary maps give the same homology as simplicial. CW complexes
  are far more efficient than triangulations: S^n needs only two cells (one 0-cell,
  one n-cell).
- Nerve theorem (Borsuk 1948, Leray 1945): let U = {U_i} be a finite open cover of
  a paracompact space X where every nonempty finite intersection U_{i_1} cap ... cap
  U_{i_k} is contractible (a 'good cover'). Then the geometric realization |N(U)| of
  the nerve N(U) is homotopy equivalent to X. This connects open covers to combinatorial
  topology and is the foundation of Cech cohomology.
- Collapsibility and simple homotopy theory (Whitehead 1939): a simplicial complex K
  is collapsible if it can be reduced to a point by a sequence of elementary collapses.
  An elementary collapse removes a free face: a (k-1)-simplex sigma that is a face of
  exactly one k-simplex tau. Collapsible implies contractible; the converse fails
  (Zeeman's dunce hat: contractible but not collapsible). Contractible but non-collapsible
  complexes detect a subtle homotopy-vs-combinatorial distinction.
- Alexander duality (1915, simplicial form): for a simplicial complex K triangulating
  S^n and a subcomplex L ⊆ K, there is an isomorphism (with appropriate coefficients)
  H_q(L) ≅ H^{n-q-1}(S^n \\ |L|). This is the simplicial version of Alexander's
  classical theorem linking the topology of a subspace to its complement.
- Künneth formula: for simplicial complexes K, L with coefficients in a field F,
  H_n(K * L; F) ≅ ⊕_{i+j=n} H_i(K; F) ⊗ H_j(L; F). For the join K * L:
  H_k(K * L) ≅ ⊕_{i+j=k-1} H_i(K) ⊗ H_j(L)  (in the reduced sense).
- Simplicial approximation theorem: for any continuous map f: |K| -> |L| between
  geometric realizations of finite simplicial complexes, there exists a subdivision K'
  of K and a simplicial map g: K' -> L such that |g| is homotopic to f. This allows
  homotopy theory to be computed combinatorially.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class CombinatorialProfile:
    """A curated combinatorial topology example."""

    key: str
    display_name: str
    complex_type: str
    euler_characteristic: int | None
    is_contractible: bool
    is_acyclic: bool
    has_torsion_in_homology: bool
    is_collapsible: bool
    betti_numbers: tuple[int, ...]
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

SIMPLICIAL_COMPLEX_TAGS: frozenset[str] = frozenset({
    "simplicial_complex",
    "abstract_simplicial_complex",
    "geometric_simplicial_complex",
    "triangulated_space",
    "flag_complex",
    "clique_complex",
    "čech_complex",
    "vietoris_rips_complex",
    "nerve_complex",
    "independence_complex",
    "order_complex",
    "matching_complex",
    "chessboard_complex",
})

CW_COMPLEX_TAGS: frozenset[str] = frozenset({
    "cw_complex",
    "cw_structure",
    "cellular_complex",
    "delta_complex",
    "regular_cw_complex",
    "minimal_cell_structure",
})

CONTRACTIBLE_TAGS: frozenset[str] = frozenset({
    "contractible",
    "contractible_complex",
    "collapsible",
    "cone",
    "star",
    "convex_body",
    "tree_complex",
    "simply_connected_acyclic",
    "npc_complex",
})

ACYCLIC_TAGS: frozenset[str] = frozenset({
    "acyclic_complex",
    "acyclic_homology",
    "trivial_reduced_homology",
    "contractible",
    "contractible_complex",
    "collapsible",
    "homology_sphere_acyclic",
})

TORSION_TAGS: frozenset[str] = frozenset({
    "torsion_homology",
    "torsion_in_h1",
    "z2_torsion",
    "non_orientable",
    "non_orientable_closed",
    "projective_space_complex",
    "lens_space_complex",
    "klein_bottle_complex",
})

EULER_CHARACTERISTIC_TAGS: frozenset[str] = frozenset({
    "euler_characteristic_positive",
    "euler_characteristic_negative",
    "euler_characteristic_zero",
    "euler_characteristic_two",
    "euler_characteristic_one",
    "polyhedron",
    "manifold_complex",
    "surface_triangulation",
})

NERVE_THEOREM_TAGS: frozenset[str] = frozenset({
    "nerve_complex",
    "good_cover",
    "čech_complex",
    "nerve_of_cover",
    "leray_nerve",
    "borsuk_nerve",
})

COLLAPSIBLE_TAGS: frozenset[str] = frozenset({
    "collapsible",
    "shellable",
    "cone",
    "star",
    "tree_complex",
    "convex_polytope_boundary",
})

NOT_COLLAPSIBLE_TAGS: frozenset[str] = frozenset({
    "not_collapsible",
    "contractible_not_collapsible",
    "dunce_hat",
    "non_shellable",
    "bing_house",
    "contractible_non_trivial_whitehead",
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


def _matches_any(tags: set[str], candidates: set[str]) -> bool:
    return bool(tags & candidates)


# ---------------------------------------------------------------------------
# Named example registry
# ---------------------------------------------------------------------------

def get_named_combinatorial_profiles() -> tuple[CombinatorialProfile, ...]:
    """Return the registry of canonical combinatorial topology examples."""
    return (
        CombinatorialProfile(
            key="standard_simplex",
            display_name="Δ^n — the standard n-simplex",
            complex_type="simplicial_complex",
            euler_characteristic=1,
            is_contractible=True,
            is_acyclic=True,
            has_torsion_in_homology=False,
            is_collapsible=True,
            betti_numbers=(1,),
            presentation_layer="main_text",
            focus=(
                "The standard n-simplex Δ^n is the convex hull of n+1 affinely independent "
                "points {e_0, e_1, ..., e_n} in R^{n+1} (the standard basis vectors). As an "
                "abstract simplicial complex, Δ^n consists of all subsets of {0,1,...,n} — it "
                "is the full simplex: every subset is a face. "
                "Δ^n is contractible: the straight-line homotopy H(x,t) = (1-t)x + t·e_0 "
                "contracts Δ^n to the vertex e_0. In particular, all homology groups vanish: "
                "H_k(Δ^n) = 0 for k >= 1, and H_0(Δ^n) = Z (connected). "
                "Δ^n is collapsible: collapse the unique free face e_n in the maximal simplex "
                "{e_0,...,e_n} (any vertex is free), reducing dimension until a point remains. "
                "Euler characteristic: chi(Δ^n) = sum_{k=0}^{n} (-1)^k C(n+1, k+1) = 1 "
                "(alternating sum of binomial coefficients). "
                "Δ^n serves as the building block: every simplicial complex is built from "
                "simplices, and every topological space is a retract of a CW complex built "
                "from simplices (via the singular complex functor)."
            ),
            chapter_targets=("7", "17", "31"),
        ),
        CombinatorialProfile(
            key="sphere_triangulation",
            display_name="S^n — the n-sphere as a simplicial complex",
            complex_type="simplicial_complex",
            euler_characteristic=2,
            is_contractible=False,
            is_acyclic=False,
            has_torsion_in_homology=False,
            is_collapsible=False,
            betti_numbers=(1, 0, 1),
            presentation_layer="main_text",
            focus=(
                "The n-sphere S^n can be triangulated as the boundary of the (n+1)-simplex "
                "∂Δ^{n+1} — the simplicial complex consisting of all proper faces of Δ^{n+1}. "
                "For n=1: boundary of a triangle (3 vertices, 3 edges). "
                "For n=2: boundary of a tetrahedron (4 vertices, 6 edges, 4 faces). "
                "Simplicial homology: H_k(S^n) = Z for k=0,n and 0 otherwise. "
                "The Betti numbers are beta_0 = beta_n = 1, all others 0. "
                "Euler characteristic: chi(S^n) = 1 + (-1)^n (equal to 2 for even n, 0 for odd n). "
                "For n=2: V=4, E=6, F=4 → chi = 4-6+4 = 2 (Euler's formula for polyhedra). "
                "CW structure: S^n has a minimal CW decomposition with two cells — one 0-cell "
                "(the south pole) and one n-cell (the rest), attached via the constant map. "
                "Non-contractible: the identity map id: S^n -> S^n has degree 1 ≠ 0, so it "
                "cannot be homotopic to a constant (which has degree 0). Equivalently, "
                "pi_n(S^n) = Z (generated by the identity map). "
                "Not collapsible: any collapse of ∂Δ^{n+1} would have to free a face, but "
                "every (n-1)-face is contained in exactly two n-faces, so no free face exists."
            ),
            chapter_targets=("7", "17", "31"),
        ),
        CombinatorialProfile(
            key="torus_triangulation",
            display_name="T² — the torus as a triangulated surface",
            complex_type="simplicial_complex",
            euler_characteristic=0,
            is_contractible=False,
            is_acyclic=False,
            has_torsion_in_homology=False,
            is_collapsible=False,
            betti_numbers=(1, 2, 1),
            presentation_layer="main_text",
            focus=(
                "The torus T² = S¹ × S¹ can be triangulated with a minimum of 7 vertices. "
                "The minimal triangulation uses 7 vertices, 21 edges, and 14 triangles: "
                "chi(T²) = 7 - 21 + 14 = 0. "
                "Simplicial homology (Z coefficients): "
                "  H_0(T²) = Z (connected), "
                "  H_1(T²) = Z ⊕ Z (two generators: the longitude and meridian circles), "
                "  H_2(T²) = Z (orientable closed surface, fundamental class [T²]). "
                "Betti numbers: beta_0 = 1, beta_1 = 2, beta_2 = 1. No torsion. "
                "The torus satisfies Poincaré duality: H_k(T²; Z) ≅ H^{2-k}(T²; Z) — "
                "the torus is a compact orientable manifold without boundary. "
                "Classification: T² is the unique (up to homeomorphism) compact orientable "
                "surface of genus g=1 (one handle). The surface classification theorem "
                "states every compact orientable surface is a connected sum of tori. "
                "CW structure: T² has a CW decomposition with 1 zero-cell, 2 one-cells "
                "(a and b), and 1 two-cell (attached via the word aba^{-1}b^{-1}), giving "
                "chi = 1 - 2 + 1 = 0."
            ),
            chapter_targets=("7", "17", "31"),
        ),
        CombinatorialProfile(
            key="real_projective_plane",
            display_name="RP² — real projective plane (triangulated)",
            complex_type="simplicial_complex",
            euler_characteristic=1,
            is_contractible=False,
            is_acyclic=False,
            has_torsion_in_homology=True,
            is_collapsible=False,
            betti_numbers=(1, 0, 0),
            presentation_layer="main_text",
            focus=(
                "The real projective plane RP² = S²/(x ~ -x) is a compact non-orientable "
                "surface triangulated with a minimum of 6 vertices (Möbius-Kantor-type). "
                "The standard triangulation uses 6 vertices, 15 edges, 10 triangles: "
                "chi(RP²) = 6 - 15 + 10 = 1. "
                "Simplicial homology (Z coefficients): "
                "  H_0(RP²) = Z (connected), "
                "  H_1(RP²) = Z/2Z (torsion — the antipodal loop has order 2), "
                "  H_2(RP²) = 0 (non-orientable: no fundamental class over Z). "
                "With Z/2Z coefficients: H_k(RP²; Z/2Z) = Z/2Z for k = 0, 1, 2. "
                "The Z/2Z torsion in H_1 is detected by the first Stiefel-Whitney class "
                "w_1 ≠ 0 (obstruction to orientability). "
                "Universal covering: S² -> RP² is a 2-sheeted covering, compatible with "
                "the antipodal action of Z/2Z on S². The fundamental group pi_1(RP²) = Z/2Z. "
                "Euler characteristic is a homotopy invariant but NOT a homeomorphism "
                "invariant among non-orientable surfaces (chi distinguishes genus but "
                "not orientability when chi is the same). "
                "chi(RP²) = 1: for surfaces chi = 2 - 2g (orientable genus g) or "
                "2 - k (non-orientable genus k connected sums RP²). RP² has k=1, chi=1."
            ),
            chapter_targets=("7", "17", "31"),
        ),
        CombinatorialProfile(
            key="dunce_hat",
            display_name="Dunce hat — contractible but not collapsible",
            complex_type="simplicial_complex",
            euler_characteristic=1,
            is_contractible=True,
            is_acyclic=True,
            has_torsion_in_homology=False,
            is_collapsible=False,
            betti_numbers=(1,),
            presentation_layer="selected_block",
            focus=(
                "The dunce hat D is obtained from a triangle by identifying all three edges "
                "in the cyclic order: the three edges are identified so that they form a "
                "single edge with winding number 3 (the attaching word aba is used where "
                "a, b, a represent the three edges). "
                "D is contractible: pi_1(D) = 1 (trivial fundamental group), and all "
                "higher homotopy groups vanish. All reduced homology groups are zero. "
                "Euler characteristic: chi(D) = 1 (one vertex, one edge, one face after "
                "identification — 1 - 1 + 1 = 1). "
                "D is NOT collapsible (Zeeman 1963, correcting an error of Whitehead): "
                "every triangulation of D has no free face — in the minimal triangulation "
                "every edge is shared by at least two triangles. This shows that "
                "'contractible' does not imply 'collapsible' in the combinatorial sense. "
                "Significance for simple homotopy theory: Whitehead's simple homotopy "
                "equivalence (generated by collapses and expansions) is strictly finer than "
                "homotopy equivalence. The Whitehead group Wh(pi_1) detects this difference "
                "for spaces with non-trivial fundamental group. For D (trivial pi_1), "
                "collapsibility is the obstruction. "
                "The dunce hat is contractible (homotopy equivalent to a point) but not "
                "combinatorially simple — it cannot be dismantled vertex by vertex. This "
                "distinction matters in computational topology (persistent homology, "
                "discrete Morse theory, and topological data analysis)."
            ),
            chapter_targets=("7", "17"),
        ),
        CombinatorialProfile(
            key="nerve_good_cover",
            display_name="Nerve of a good cover — Nerve theorem",
            complex_type="simplicial_complex",
            euler_characteristic=None,
            is_contractible=False,
            is_acyclic=False,
            has_torsion_in_homology=False,
            is_collapsible=False,
            betti_numbers=(),
            presentation_layer="selected_block",
            focus=(
                "Given a finite open cover U = {U_1, ..., U_m} of a topological space X, "
                "the nerve N(U) is the abstract simplicial complex whose vertices are the "
                "sets U_i and whose simplices are finite subcollections with nonempty "
                "intersection: {U_{i_0}, ..., U_{i_k}} is a simplex iff "
                "U_{i_0} ∩ ... ∩ U_{i_k} ≠ ∅. "
                "Nerve theorem (Borsuk 1948 / Leray 1945): if U is a good cover — every "
                "nonempty finite intersection U_{i_0} ∩ ... ∩ U_{i_k} is contractible — "
                "then the geometric realization |N(U)| is homotopy equivalent to X. "
                "In particular, H_k(X) ≅ H_k(N(U)) for all k, and pi_1(X) ≅ pi_1(N(U)). "
                "Applications: "
                "(1) Čech cohomology: the Čech complex Č(U) for a good cover computes "
                "the actual cohomology of X — this is the basis of Čech cohomology. "
                "(2) Topological data analysis (TDA): the Vietoris-Rips and Čech complexes "
                "of a finite point cloud P ⊂ R^n approximate the topology of the underlying "
                "space. Persistent homology tracks how H_k changes as the radius grows. "
                "(3) Sensor networks: the nerve models coverage regions — whether a region "
                "is fully covered corresponds to contractibility of the nerve. "
                "Good cover existence: every compact Riemannian manifold has a good cover "
                "(convex neighborhoods from the injectivity radius). In R^n, all intersections "
                "of convex sets are convex hence contractible — so convex covers are good. "
                "The nerve theorem requires paracompactness and good cover; without the "
                "good cover condition the nerve may fail to capture the homotopy type."
            ),
            chapter_targets=("7", "17", "31"),
        ),
        CombinatorialProfile(
            key="klein_bottle_complex",
            display_name="K — Klein bottle as a triangulated complex",
            complex_type="simplicial_complex",
            euler_characteristic=0,
            is_contractible=False,
            is_acyclic=False,
            has_torsion_in_homology=True,
            is_collapsible=False,
            betti_numbers=(1, 1, 0),
            presentation_layer="selected_block",
            focus=(
                "The Klein bottle K is a compact non-orientable surface without boundary, "
                "obtained from a square by identifying opposite edges as ab a^{-1} b. "
                "Minimal triangulation: 8 vertices, 24 edges, 16 triangles — "
                "chi(K) = 8 - 24 + 16 = 0. "
                "Simplicial homology (Z coefficients): "
                "  H_0(K) = Z (connected), "
                "  H_1(K) = Z ⊕ Z/2Z (one free generator from b, one Z/2Z from 2a = 0), "
                "  H_2(K) = 0 (non-orientable: no Z fundamental class). "
                "With Z/2Z coefficients: H_k(K; Z/2Z) = Z/2Z for all k = 0, 1, 2. "
                "The Z/2Z torsion arises from the non-orientable identification: the "
                "boundary of 2[K] = 0 in the simplicial chain group, but [K] ≠ 0. "
                "Fundamental group: pi_1(K) = <a, b | abab^{-1} = 1> (non-abelian, "
                "infinite, with center Z). pi_1(K) / [pi_1(K), pi_1(K)] ≅ Z ⊕ Z/2Z "
                "matching H_1(K) by the Hurewicz theorem. "
                "K cannot be embedded in R³ without self-intersection (it can be immersed). "
                "It embeds in R^4 cleanly. The Klein bottle is the connected sum RP² # RP² "
                "— the simplest non-orientable surface with genus 2. "
                "Euler characteristic of non-orientable surfaces: chi = 2 - k where k is "
                "the number of crosscaps (connected summands of RP²). For K: k=2, chi=0."
            ),
            chapter_targets=("7", "17"),
        ),
    )


def combinatorial_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_combinatorial_profiles()
    ))


def combinatorial_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_combinatorial_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def combinatorial_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from complex_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_combinatorial_profiles():
        index.setdefault(p.complex_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_contractible_complex(space: Any) -> Result:
    """Check whether the space is contractible (homotopy equivalent to a point).

    A simplicial complex K is contractible if it is homotopy equivalent to a
    one-point space: all homotopy groups vanish (pi_k(K) = 0 for all k >= 0).
    Equivalently, the identity map id: K -> K is homotopic to a constant map.
    Key examples:
    - The standard n-simplex Δ^n and any cone are contractible.
    - Trees (connected, no cycles) are contractible.
    - The dunce hat is contractible but NOT collapsible.
    - Spheres S^n (n >= 1) are NOT contractible.

    Decision layers
    ---------------
    1. Explicit 'contractible' or cone/star/tree tag -> true.
    2. Not-contractible tags (sphere, manifold, torus) -> false.
    3. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, CONTRACTIBLE_TAGS):
        witness = next(t for t in tags if t in CONTRACTIBLE_TAGS)
        return Result.true(
            mode="theorem",
            value="contractible_complex",
            justification=[
                f"Tag {witness!r}: the complex is contractible — homotopy equivalent "
                "to a point. All reduced homology groups vanish and every homotopy group "
                "is trivial. A straight-line contraction exists (cone or collapse).",
            ],
            metadata={**base, "criterion": "explicit_contractible", "witness": witness},
        )

    not_contractible = {
        "sphere", "sphere_triangulation", "torus", "torus_triangulation",
        "surface_positive_genus", "projective_space_complex",
        "closed_orientable_manifold", "klein_bottle_complex",
        "non_contractible", "non_trivial_fundamental_group",
    }
    if _matches_any(tags, not_contractible):
        blocking = next(t for t in tags if t in not_contractible)
        return Result.false(
            mode="theorem",
            value="contractible_complex",
            justification=[
                f"Tag {blocking!r}: the complex is NOT contractible. "
                "Spheres S^n (n>=1) have H_n(S^n) = Z ≠ 0; tori and projective spaces "
                "have nontrivial fundamental groups or homology.",
            ],
            metadata={**base, "criterion": "not_contractible"},
        )

    return Result.unknown(
        mode="symbolic",
        value="contractible_complex",
        justification=[
            "Insufficient tags to determine contractibility. "
            "Supply tags such as 'contractible', 'cone', 'star', 'tree_complex', "
            "'sphere', 'torus', 'non_contractible', or 'collapsible'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_acyclic_complex(space: Any) -> Result:
    """Check whether the space is acyclic (trivial reduced homology).

    A space X is acyclic if its reduced homology vanishes: H_k(X) = 0 for all k >= 0.
    Equivalently, the augmented chain complex is exact. Key examples:
    - All contractible spaces are acyclic (but not vice versa: homology spheres
      that are acyclic exist — e.g., the Poincaré homology sphere with pi_1 = I* but
      H_k = H_k(S^3) — but this is not acyclic).
    - Acyclic but non-contractible: the Whitehead manifold (open 3-manifold).
    - Spheres S^n are NOT acyclic: H_n(S^n) = Z.

    Decision layers
    ---------------
    1. Explicit 'acyclic_homology' or 'trivial_reduced_homology' tag -> true.
    2. Contractible tags -> true (contractible implies acyclic).
    3. Sphere / closed manifold with known nonzero homology -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"acyclic_complex", "acyclic_homology",
                            "trivial_reduced_homology"}):
        witness = next(t for t in tags if t in {"acyclic_complex", "acyclic_homology",
                                                    "trivial_reduced_homology"})
        return Result.true(
            mode="theorem",
            value="acyclic_complex",
            justification=[
                f"Tag {witness!r}: the complex is acyclic — all reduced homology groups "
                "H_k vanish. The augmented chain complex is exact.",
            ],
            metadata={**base, "criterion": "explicit_acyclic", "witness": witness},
        )

    if _matches_any(tags, CONTRACTIBLE_TAGS):
        witness = next(t for t in tags if t in CONTRACTIBLE_TAGS)
        return Result.true(
            mode="theorem",
            value="acyclic_complex",
            justification=[
                f"Tag {witness!r}: contractible implies acyclic — homotopy equivalence "
                "to a point gives H_k = 0 for k >= 1 and H_0 = Z (reduced H_0 = 0).",
            ],
            metadata={**base, "criterion": "contractible_implies_acyclic", "witness": witness},
        )

    not_acyclic = {
        "sphere", "sphere_triangulation", "torus", "torus_triangulation",
        "projective_space_complex", "klein_bottle_complex",
        "non_acyclic", "nontrivial_homology",
    }
    if _matches_any(tags, not_acyclic):
        blocking = next(t for t in tags if t in not_acyclic)
        return Result.false(
            mode="theorem",
            value="acyclic_complex",
            justification=[
                f"Tag {blocking!r}: the complex is NOT acyclic. "
                "Spheres have H_n = Z; tori have H_1 = Z^2, H_2 = Z; projective "
                "spaces have torsion in odd dimensions.",
            ],
            metadata={**base, "criterion": "not_acyclic"},
        )

    return Result.unknown(
        mode="symbolic",
        value="acyclic_complex",
        justification=[
            "Insufficient tags to determine acyclicity. "
            "Supply tags such as 'acyclic_complex', 'contractible', 'sphere', "
            "'torus', or 'non_acyclic'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_torsion_homology(space: Any) -> Result:
    """Check whether the homology groups contain torsion elements.

    A simplicial complex K has torsion in homology if some H_k(K; Z) has a
    non-free part: H_k(K; Z) ≅ Z^{b_k} ⊕ (torsion subgroup). Key examples:
    - RP^n: H_k(RP^n; Z) has Z/2Z torsion in odd dimensions 0 < k < n.
    - The Klein bottle: H_1(K; Z) = Z ⊕ Z/2Z.
    - Lens spaces L(p,q): H_1 = Z/pZ.
    - Orientable manifolds: H_n = Z (no torsion in top degree for orientable).
    - Spheres and tori (over Z): no torsion.

    Decision layers
    ---------------
    1. Explicit 'torsion_homology' or 'z2_torsion' tag -> true.
    2. Non-orientable closed surface or projective space -> true.
    3. Sphere / orientable surface (torus etc.) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, TORSION_TAGS):
        witness = next(t for t in tags if t in TORSION_TAGS)
        return Result.true(
            mode="theorem",
            value="torsion_homology",
            justification=[
                f"Tag {witness!r}: the complex has torsion in homology. "
                "Non-orientable surfaces (RP², Klein bottle) carry Z/2Z torsion in H_1. "
                "Lens spaces L(p,q) have Z/pZ torsion in H_1.",
            ],
            metadata={**base, "criterion": "explicit_torsion", "witness": witness},
        )

    torsion_free = {
        "sphere", "sphere_triangulation",
        "torus", "torus_triangulation",
        "orientable_closed_surface",
        "contractible", "contractible_complex",
        "torsion_free_homology",
    }
    if _matches_any(tags, torsion_free):
        witness = next(t for t in tags if t in torsion_free)
        return Result.false(
            mode="theorem",
            value="torsion_homology",
            justification=[
                f"Tag {witness!r}: the complex has torsion-free homology. "
                "Spheres S^n have homology Z in dimensions 0 and n (no torsion). "
                "Orientable surfaces (torus, genus-g surface) have free homology groups.",
            ],
            metadata={**base, "criterion": "torsion_free"},
        )

    return Result.unknown(
        mode="symbolic",
        value="torsion_homology",
        justification=[
            "Insufficient tags to determine torsion in homology. "
            "Supply tags such as 'torsion_homology', 'z2_torsion', 'non_orientable', "
            "'sphere', 'torus', or 'torsion_free_homology'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_collapsible_complex(space: Any) -> Result:
    """Check whether the complex is collapsible (reducible to a point by elementary collapses).

    A simplicial complex K is collapsible if there exists a sequence of elementary collapses
    reducing K to a single vertex. An elementary collapse removes a free face: a (k-1)-simplex
    sigma contained in exactly one k-simplex tau. Both sigma and tau are removed together.
    Key facts:
    - Collapsible implies contractible (each collapse is a homotopy equivalence).
    - The converse fails: the dunce hat is contractible but not collapsible.
    - Cones are collapsible: cone(L) collapses to the cone point.
    - Shellable complexes are collapsible.
    - The Bing house with two rooms is contractible but non-collapsible.

    Decision layers
    ---------------
    1. Explicit 'collapsible' or 'shellable' or cone/star tag -> true.
    2. Not-collapsible tags (dunce_hat, bing_house) -> false.
    3. Non-contractible -> false (collapsible implies contractible).
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, COLLAPSIBLE_TAGS):
        witness = next(t for t in tags if t in COLLAPSIBLE_TAGS)
        return Result.true(
            mode="theorem",
            value="collapsible_complex",
            justification=[
                f"Tag {witness!r}: the complex is collapsible — it can be reduced to a "
                "point by elementary collapses (removing free face-maximal simplex pairs). "
                "Cones, stars, and shellable complexes are collapsible.",
            ],
            metadata={**base, "criterion": "explicit_collapsible", "witness": witness},
        )

    if _matches_any(tags, NOT_COLLAPSIBLE_TAGS):
        blocking = next(t for t in tags if t in NOT_COLLAPSIBLE_TAGS)
        return Result.false(
            mode="theorem",
            value="collapsible_complex",
            justification=[
                f"Tag {blocking!r}: the complex is NOT collapsible. "
                "The dunce hat (Zeeman 1963) and the Bing house with two rooms are "
                "contractible but have no free faces in any triangulation — no elementary "
                "collapse is possible. Collapsibility is strictly stronger than contractibility.",
            ],
            metadata={**base, "criterion": "not_collapsible"},
        )

    not_contractible = {
        "sphere", "sphere_triangulation", "torus", "torus_triangulation",
        "projective_space_complex", "non_contractible",
        "closed_orientable_manifold", "klein_bottle_complex",
    }
    if _matches_any(tags, not_contractible):
        blocking = next(t for t in tags if t in not_contractible)
        return Result.false(
            mode="theorem",
            value="collapsible_complex",
            justification=[
                f"Tag {blocking!r}: not contractible implies not collapsible. "
                "Every collapsible complex is contractible, so the contrapositive applies.",
            ],
            metadata={**base, "criterion": "not_contractible_not_collapsible"},
        )

    return Result.unknown(
        mode="symbolic",
        value="collapsible_complex",
        justification=[
            "Insufficient tags to determine collapsibility. "
            "Supply tags such as 'collapsible', 'shellable', 'cone', 'dunce_hat', "
            "'bing_house', 'not_collapsible', or 'sphere'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_combinatorial(space: Any) -> dict[str, Any]:
    """Classify the combinatorial topology type of space.

    Keys
    ----
    combinatorial_class : str
        One of ``"contractible_collapsible"``, ``"contractible_not_collapsible"``,
        ``"acyclic"``, ``"torsion"``, ``"free_homology"``, ``"unknown"``.
    is_contractible : Result
    is_acyclic : Result
    has_torsion : Result
    is_collapsible : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    contr_r = is_contractible_complex(space)
    acyclic_r = is_acyclic_complex(space)
    torsion_r = has_torsion_homology(space)
    collaps_r = is_collapsible_complex(space)

    if contr_r.is_true and collaps_r.is_true:
        combinatorial_class = "contractible_collapsible"
    elif contr_r.is_true and collaps_r.is_false:
        combinatorial_class = "contractible_not_collapsible"
    elif acyclic_r.is_true:
        combinatorial_class = "acyclic"
    elif torsion_r.is_true:
        combinatorial_class = "torsion"
    elif torsion_r.is_false and not acyclic_r.is_true:
        combinatorial_class = "free_homology"
    else:
        combinatorial_class = "unknown"

    key_properties: list[str] = []
    if contr_r.is_true:
        key_properties.append("contractible")
    if contr_r.is_false:
        key_properties.append("not_contractible")
    if acyclic_r.is_true:
        key_properties.append("acyclic")
    if torsion_r.is_true:
        key_properties.append("torsion_homology")
    if torsion_r.is_false:
        key_properties.append("torsion_free")
    if collaps_r.is_true:
        key_properties.append("collapsible")
    if collaps_r.is_false:
        key_properties.append("not_collapsible")
    if _matches_any(tags, NERVE_THEOREM_TAGS):
        key_properties.append("nerve_theorem_applicable")
    if _matches_any(tags, CW_COMPLEX_TAGS):
        key_properties.append("cw_structure")

    return {
        "combinatorial_class": combinatorial_class,
        "is_contractible": contr_r,
        "is_acyclic": acyclic_r,
        "has_torsion": torsion_r,
        "is_collapsible": collaps_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def combinatorial_profile(space: Any) -> dict[str, Any]:
    """Full combinatorial topology profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_combinatorial`.
    named_profiles : tuple[CombinatorialProfile, ...]
        Registry of canonical combinatorial topology examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_combinatorial(space),
        "named_profiles": get_named_combinatorial_profiles(),
        "layer_summary": combinatorial_layer_summary(),
    }


__all__ = [
    "CombinatorialProfile",
    "SIMPLICIAL_COMPLEX_TAGS",
    "CW_COMPLEX_TAGS",
    "CONTRACTIBLE_TAGS",
    "ACYCLIC_TAGS",
    "TORSION_TAGS",
    "EULER_CHARACTERISTIC_TAGS",
    "NERVE_THEOREM_TAGS",
    "COLLAPSIBLE_TAGS",
    "NOT_COLLAPSIBLE_TAGS",
    "get_named_combinatorial_profiles",
    "combinatorial_layer_summary",
    "combinatorial_chapter_index",
    "combinatorial_type_index",
    "is_contractible_complex",
    "is_acyclic_complex",
    "has_torsion_homology",
    "is_collapsible_complex",
    "classify_combinatorial",
    "combinatorial_profile",
]
