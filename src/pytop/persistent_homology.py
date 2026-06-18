"""Persistent homology: topological data analysis, filtrations, persistence diagrams,
barcodes, stability theorem, and the algebraic structure of persistence modules.

Key theorems implemented
------------------------
- Filtration and persistent homology (Edelsbrunner-Letscher-Zomorodian 2002): given a
  nested sequence of simplicial complexes (a filtration) K_0 ⊆ K_1 ⊆ ... ⊆ K_n, the
  persistent homology H_k^{i,j} = im(H_k(K_i) -> H_k(K_j)) tracks which k-dimensional
  homology classes 'born' at K_i survive to K_j. Each class has a birth time b and
  death time d (or death = infty for essential classes), giving a persistence pair (b,d).
  The collection of all persistence pairs forms the persistence diagram Dgm_k.
- Vietoris-Rips complex (Rips, used by Vietoris 1927): for a finite metric space (X, d)
  and scale parameter r > 0, the Vietoris-Rips complex VR(X, r) has vertex set X and
  includes a simplex {x_0, ..., x_k} whenever d(x_i, x_j) <= r for all i, j (i.e.,
  when the diameter of the set is <= r). As r grows from 0 to infty, the VR complexes
  form a filtration VR(X, 0) ⊆ VR(X, r_1) ⊆ ... ⊆ VR(X, infty) = Δ^{|X|-1}.
  The persistent homology of this filtration captures the 'shape' of the point cloud X
  at all scales simultaneously.
- Čech complex: for X ⊆ R^n and r > 0, the Čech complex C(X, r) includes a simplex
  {x_0, ..., x_k} iff the balls B(x_i, r) have a common point (their intersection is
  nonempty). By the nerve theorem, |C(X,r)| is homotopy equivalent to the union of balls
  union B(x_i, r). The Čech complex is finer than VR: C(X, r) ⊆ VR(X, 2r) ⊆ C(X, 2r)
  (the 'sandwich' lemma). In practice VR is preferred as it is easier to compute.
- Structure theorem for persistence modules (Zomorodian-Carlsson 2005): a persistence
  module M = {M_i, phi_i: M_i -> M_{i+1}} over a field k (each M_i a finite-dimensional
  k-vector space) decomposes as a direct sum of interval modules k[b_j, d_j) — one for
  each persistence pair (b_j, d_j). This decomposition is unique (up to isomorphism),
  and the multiset of intervals is exactly the barcode. The proof uses the classification
  of finitely generated modules over k[t] (a PID) — the structure theorem for modules
  over PIDs applied to the graded module associated to the persistence module.
- Stability theorem (Cohen-Steiner, Edelsbrunner, Harer 2007): the bottleneck distance
  d_B(Dgm(f), Dgm(g)) between the persistence diagrams of two functions f, g: X -> R
  satisfies d_B(Dgm(f), Dgm(g)) <= ||f - g||_infty. Thus small perturbations of the
  input give small perturbations of the persistence diagram (in bottleneck distance).
  This is the key stability result: persistent homology is robust to noise. The
  Wasserstein version: d_W^q(Dgm(f), Dgm(g)) <= C · ||f - g||_infty^{1/q}.
- Bottleneck distance: for two persistence diagrams D_1, D_2 (multisets of points
  (b,d) in the extended plane with b < d), the bottleneck distance is
  d_B(D_1, D_2) = inf_{gamma bijection} sup_{x in D_1} ||x - gamma(x)||_infty
  where the bijection gamma: D_1 ∪ Δ -> D_2 ∪ Δ allows matching points to the
  diagonal Δ = {(x,x) : x in R} (representing trivial classes). A point (b,d)
  matched to the diagonal contributes persistence d - b to the cost.
- Wasserstein distance: the p-th Wasserstein distance is
  d_W^p(D_1, D_2) = inf_gamma (sum_{x in D_1} ||x - gamma(x)||_infty^p)^{1/p}.
  For p = infty, d_W^infty = d_B. The Wasserstein distance is more sensitive to
  small features than the bottleneck distance.
- Elder rule / pairing: in a filtration, each k-simplex sigma either (a) creates a new
  k-cycle (birth) or (b) kills a (k-1)-cycle (death, pairing with the oldest unmatched
  cycle, the 'elder'). The elder rule (or reduction algorithm) determines the pairing
  uniquely and gives the persistence diagram.
- Persistent homology over Z/2Z: computations are often done over the field Z/2Z = F_2
  to avoid sign issues. The boundary matrix is reduced by column operations over F_2
  (addition mod 2). The resulting pairing gives the same topological information as
  Z-coefficients for most point cloud applications (orientability does not affect the
  birth-death pairing in typical TDA pipelines).
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from typing import Any

from .result import Result


@dataclass(frozen=True)
class PersistenceProfile:
    """A curated persistent homology / TDA example."""

    key: str
    display_name: str
    complex_type: str
    filtration_type: str
    has_finite_barcode: bool
    is_stable: bool
    has_essential_classes: bool
    computable_over_field: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

VIETORIS_RIPS_TAGS: frozenset[str] = frozenset({
    "vietoris_rips",
    "rips_complex",
    "vr_filtration",
    "rips_filtration",
    "clique_filtration",
    "diameter_filtration",
})

CECH_COMPLEX_TAGS: frozenset[str] = frozenset({
    "cech_complex",
    "cech_filtration",
    "ball_cover_filtration",
    "nerve_of_balls",
    "alpha_complex",
    "weighted_alpha_complex",
})

PERSISTENCE_DIAGRAM_TAGS: frozenset[str] = frozenset({
    "persistence_diagram",
    "barcode",
    "persistence_barcode",
    "birth_death_pairs",
    "dgm",
    "persistence_pairs",
})

STABLE_FILTRATION_TAGS: frozenset[str] = frozenset({
    "stable_filtration",
    "stability_theorem",
    "bottleneck_stable",
    "sublevel_set_filtration",
    "morse_filtration",
    "function_filtration",
    "tame_function",
    "height_filtration",
})

UNSTABLE_OR_SENSITIVE_TAGS: frozenset[str] = frozenset({
    "not_stable",
    "sensitive_to_noise",
    "non_tame_function",
    "infinite_persistence",
})

ESSENTIAL_CLASS_TAGS: frozenset[str] = frozenset({
    "essential_homology",
    "infinite_bar",
    "essential_class",
    "non_contractible_component",
    "essential_cycle",
    "unbounded_persistence",
})

SUBLEVEL_SET_TAGS: frozenset[str] = frozenset({
    "sublevel_set_filtration",
    "morse_filtration",
    "function_filtration",
    "height_filtration",
    "distance_filtration",
    "rips_filtration",
    "cech_filtration",
    "vr_filtration",
})

FIELD_COEFFICIENTS_TAGS: frozenset[str] = frozenset({
    "field_coefficients",
    "z2_coefficients",
    "f2_coefficients",
    "rational_coefficients",
    "fp_coefficients",
    "persistent_homology_field",
})

STRUCTURE_THEOREM_TAGS: frozenset[str] = frozenset({
    "structure_theorem",
    "interval_decomposition",
    "persistence_module",
    "pid_decomposition",
    "zomorodian_carlsson",
    "graded_module_pid",
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

def get_named_persistence_profiles() -> tuple[PersistenceProfile, ...]:
    """Return the registry of canonical persistent homology examples."""
    return (
        PersistenceProfile(
            key="vietoris_rips_point_cloud",
            display_name="VR(X, r) — Vietoris-Rips filtration of a point cloud",
            complex_type="vietoris_rips",
            filtration_type="diameter_filtration",
            has_finite_barcode=True,
            is_stable=True,
            has_essential_classes=False,
            computable_over_field=True,
            presentation_layer="main_text",
            focus=(
                "The Vietoris-Rips filtration is the standard construction for persistent "
                "homology of finite metric spaces (point clouds). For X = {x_1, ..., x_n} "
                "with distances d_{ij} = d(x_i, x_j), VR(X, r) is the flag/clique complex "
                "on the graph G_r where {x_i, x_j} is an edge iff d_{ij} <= r. "
                "As r increases: r=0 gives n isolated vertices; r = d_{12}/2 gives the first "
                "edge; eventually VR(X, diam(X)) = the complete simplex Δ^{n-1}. "
                "The filtration VR(X, 0) ⊆ VR(X, r_1) ⊆ ... ⊆ Δ^{n-1} yields a finite "
                "sequence of simplicial complexes (since X is finite and distances are discrete). "
                "Persistent H_0 (connected components): components merge as r increases. "
                "A component 'born' at r = 0 (every point is its own component) and 'dies' "
                "when it merges with another component (the death time = distance to nearest "
                "neighbor for the older component, by the elder rule). "
                "Persistent H_1 (loops): 1-cycles appear when a triangle's interior is not "
                "filled. E.g., for points sampled from a circle S^1, H_1 has a long bar "
                "corresponding to the fundamental cycle. "
                "VR vs Čech: VR(X, r) ⊆ Čech(X, r) ⊆ VR(X, 2r) (sandwich). VR is purely "
                "combinatorial (no geometry needed beyond distances); Čech requires ambient space. "
                "Stability: the VR filtration is stable — the persistence diagram changes by "
                "at most ||delta_d||_infty under perturbation of distances (stability theorem)."
            ),
            chapter_targets=("9", "19", "33"),
        ),
        PersistenceProfile(
            key="sublevel_set_filtration",
            display_name="f^{-1}(-∞, t] — sublevel set filtration of a function",
            complex_type="simplicial_complex",
            filtration_type="sublevel_set",
            has_finite_barcode=True,
            is_stable=True,
            has_essential_classes=True,
            computable_over_field=True,
            presentation_layer="main_text",
            focus=(
                "For a continuous function f: X -> R on a triangulated space X, the sublevel "
                "set filtration is X_t = f^{-1}(-infty, t] for t in R. As t increases from "
                "-infty to +infty, X_t grows from the empty set to all of X. "
                "Persistent homology of the sublevel filtration captures the topology of "
                "X at all function values simultaneously — a 'multi-scale' Morse theory. "
                "Morse theory connection: for a Morse function f on a manifold, each critical "
                "point of index k either creates a new k-cycle (birth) or kills an existing "
                "(k-1)-cycle (death). The persistence pair (b, d) of a birth-death pair has "
                "persistence d - b = the 'lifetime' of the topological feature. "
                "Elder rule: when a k-cycle is killed, it is paired with the 'oldest' "
                "surviving (k-1)-cycle (the one born earliest). This determines the unique "
                "persistence diagram. "
                "Essential classes: classes that are born but never die (death = +infty) "
                "correspond to non-trivial classes in H_k(X). For a compact connected "
                "manifold: H_0 has one essential class (the connected component) and "
                "H_n has one essential class if X is orientable (the fundamental class). "
                "Stability theorem (Cohen-Steiner, Edelsbrunner, Harer 2007): "
                "d_B(Dgm(f), Dgm(g)) <= ||f - g||_infty for tame functions on the same space. "
                "Applications: terrain analysis (water flow, ridges = persistence pairs), "
                "brain imaging (fMRI sublevel sets of activation), shape analysis."
            ),
            chapter_targets=("9", "19", "33"),
        ),
        PersistenceProfile(
            key="persistence_diagram_bottleneck",
            display_name="Persistence diagram and bottleneck distance",
            complex_type="abstract",
            filtration_type="general",
            has_finite_barcode=True,
            is_stable=True,
            has_essential_classes=False,
            computable_over_field=True,
            presentation_layer="main_text",
            focus=(
                "A persistence diagram Dgm_k is a multiset of points (b, d) in the extended "
                "half-plane {(b,d) : b <= d <= +infty} — one point for each persistence pair "
                "(birth b, death d) in H_k of the filtration, plus all diagonal points "
                "(x, x) with infinite multiplicity (representing trivial classes). "
                "The bottleneck distance between two diagrams D_1, D_2 is: "
                "d_B(D_1, D_2) = inf_{gamma: D_1 -> D_2 bijection} sup_{p in D_1} ||p - gamma(p)||_infty "
                "where the bijection gamma sends points in D_1 to points in D_2 or to their "
                "nearest diagonal point (a point (b,d) matched to the diagonal contributes "
                "cost (d-b)/2 — its distance to the diagonal). "
                "Stability theorem: d_B(Dgm(f), Dgm(g)) <= ||f - g||_infty. "
                "This means: if two functions differ by at most epsilon in sup-norm, their "
                "persistence diagrams are at most epsilon apart in bottleneck distance. "
                "Consequence: persistent homology is stable under noise — adding Gaussian "
                "noise of magnitude epsilon to the input shifts the diagram by at most epsilon. "
                "Short bars (near the diagonal) represent topological noise; long bars represent "
                "genuine topological features. The stability theorem justifies this heuristic. "
                "Wasserstein distance d_W^p: more sensitive to small features than d_B. "
                "d_W^1 (total persistence cost) penalizes many small features more than d_B. "
                "The space of persistence diagrams with bottleneck distance is a complete "
                "metric space (Mileyko-Mukherjee-Harer). "
                "Frechet mean: the average of a set of persistence diagrams exists and is "
                "unique in the Wasserstein metric (for the squared 2-Wasserstein distance)."
            ),
            chapter_targets=("9", "19", "33"),
        ),
        PersistenceProfile(
            key="structure_theorem_persistence_modules",
            display_name="Structure theorem — persistence module decomposition",
            complex_type="algebraic",
            filtration_type="algebraic",
            has_finite_barcode=True,
            is_stable=True,
            has_essential_classes=False,
            computable_over_field=True,
            presentation_layer="main_text",
            focus=(
                "A persistence module M = (M_i, phi_i) over a field k consists of a sequence "
                "of k-vector spaces M_0, M_1, ..., M_n and linear maps phi_i: M_i -> M_{i+1}. "
                "Example: M_i = H_k(K_i; k) with phi_i = the map induced by the inclusion K_i -> K_{i+1}. "
                "Structure theorem (Zomorodian-Carlsson 2005): every finitely presented "
                "persistence module over a field k decomposes uniquely (up to isomorphism) "
                "as a direct sum of interval modules: "
                "M ≅ ⊕_j k[b_j, d_j) "
                "where k[b, d) is the persistence module that is k in positions b <= i < d "
                "and 0 otherwise, with identity maps within the interval and 0 maps outside. "
                "Proof: encode M as a finitely generated graded k[t]-module via the shift "
                "functor (t acts by phi_i). The structure theorem for finitely generated "
                "modules over k[t] (a PID) gives the decomposition. The graded version "
                "yields exactly the interval modules. "
                "The barcode: the multiset {[b_j, d_j)} is the barcode of M. Each interval "
                "corresponds to a bar in the barcode diagram: a bar starts at birth b_j and "
                "ends at death d_j (or extends to infinity for essential classes). "
                "Rank invariant: beta_k^{i,j} = rank(phi_j circ ... circ phi_i: M_i -> M_j) "
                "counts persistent k-cycles born at or before i surviving to j. "
                "The persistence diagram Dgm_k is equivalent to the barcode and to the rank "
                "invariant (they carry the same information for field coefficients)."
            ),
            chapter_targets=("9", "19"),
        ),
        PersistenceProfile(
            key="cech_alpha_complex",
            display_name="Čech / alpha complex filtration for point clouds in R^n",
            complex_type="cech_complex",
            filtration_type="ball_cover_filtration",
            has_finite_barcode=True,
            is_stable=True,
            has_essential_classes=False,
            computable_over_field=True,
            presentation_layer="selected_block",
            focus=(
                "The Čech complex C(X, r) for a finite X ⊆ R^n is the nerve of the ball cover "
                "{B(x, r) : x in X}: a simplex {x_0,...,x_k} is included iff "
                "B(x_0, r) ∩ ... ∩ B(x_k, r) ≠ ∅. By the nerve theorem (balls are convex, "
                "hence contractible, and all intersections of convex sets are convex), "
                "|C(X, r)| is homotopy equivalent to the union of balls B(X, r) = ∪ B(x, r). "
                "Sandwich lemma: VR(X, r) ⊆ C(X, r) ⊆ VR(X, 2r). The Čech filtration is "
                "homotopy equivalent to the union-of-balls filtration (geometric faithfulness), "
                "but VR is purely combinatorial and computationally preferred. "
                "Alpha complex: a subcomplex of the Delaunay triangulation — includes only "
                "the Čech simplices whose circumradius is <= r AND whose circumcenter is in "
                "the Voronoi cell. The alpha filtration has the same persistent homology as "
                "the Čech filtration but with far fewer simplices (linear in |X| for R^2). "
                "The alpha complex is the standard construction in practice for point clouds "
                "in R^2 or R^3 (used in GUDHI, Ripser, Dionysus). "
                "Stability: the Čech filtration is stable (it is a function filtration "
                "via the distance function d(·, X), so the stability theorem applies). "
                "The 1-parameter family C(X, r) for r > 0 is a sublevel filtration of the "
                "distance function d(·, X): R^n -> R, which is 1-Lipschitz."
            ),
            chapter_targets=("9", "19", "33"),
        ),
        PersistenceProfile(
            key="circle_point_cloud",
            display_name="Points sampled from S^1 — detecting a loop",
            complex_type="vietoris_rips",
            filtration_type="diameter_filtration",
            has_finite_barcode=True,
            is_stable=True,
            has_essential_classes=False,
            computable_over_field=True,
            presentation_layer="selected_block",
            focus=(
                "A canonical TDA example: n points X sampled (uniformly or with noise) from "
                "the unit circle S^1 ⊂ R^2. The Vietoris-Rips persistent homology recovers "
                "the topology of S^1: "
                "H_0 persistence: n components at r=0, all merging into one as r approaches "
                "the longest gap between adjacent points. The bar for H_0 that survives to "
                "r = infty (or the full complex) is the essential component. "
                "H_1 persistence: at a certain r (approximately the circumradius of three "
                "adjacent points), a 1-cycle (loop) is born. It dies when the full simplicial "
                "complex fills the interior. For a perfect circle, there is one long bar in "
                "H_1 corresponding to the fundamental class of S^1. "
                "Signal vs noise: short bars in H_1 are topological noise from the sampling. "
                "The long bar is the signal (the circle). The stability theorem guarantees "
                "that as the sample density increases, the persistence diagram converges to "
                "that of S^1 (one infinite H_0 bar, one long H_1 bar). "
                "This is the paradigmatic example demonstrating that persistent homology "
                "correctly identifies the 'shape' of noisy point cloud data. "
                "For points sampled from a torus T^2: H_0 has one essential bar, H_1 has two "
                "long bars (the two generators of H_1(T^2) = Z^2), H_2 has one long bar."
            ),
            chapter_targets=("9", "19", "33"),
        ),
        PersistenceProfile(
            key="mapper_algorithm",
            display_name="Mapper — topological summary graph of high-dimensional data",
            complex_type="abstract",
            filtration_type="cover_filtration",
            has_finite_barcode=False,
            is_stable=False,
            has_essential_classes=False,
            computable_over_field=False,
            presentation_layer="selected_block",
            focus=(
                "The Mapper algorithm (Singh-Mémoli-Carlsson 2007) produces a graph (1-complex) "
                "summarizing the topology of a high-dimensional dataset X ⊆ R^n. Steps: "
                "(1) Choose a filter function f: X -> R (e.g., a coordinate, density, eccentricity). "
                "(2) Cover the range f(X) by overlapping intervals U_1, ..., U_m (with overlap). "
                "(3) Pull back: compute the preimages f^{-1}(U_i) for each interval. "
                "(4) Cluster: within each f^{-1}(U_i), run a clustering algorithm (e.g., "
                "    single-linkage at a scale parameter r) to get clusters C_{i,1}, C_{i,2}, ... "
                "(5) Build the graph: one node per cluster; connect nodes sharing a data point "
                "    (arising from the overlap between U_i and U_{i+1}). "
                "The resulting graph is the Mapper graph — a 1-skeleton topological summary. "
                "Mapper generalizes Reeb graphs: for X a manifold and f a Morse function, "
                "the Mapper converges (in a suitable sense) to the Reeb graph of f as the "
                "cover and cluster parameters refine. "
                "Mapper is NOT a filtration and does NOT give persistence diagrams directly — "
                "it is a qualitative topological summary, not a quantitative one. "
                "Applications: cancer genomics (Nicolau-Levine-Carlsson 2011 — identified "
                "a new breast cancer subtype using Mapper on gene expression data), NBA player "
                "clustering, materials science. "
                "The Mapper graph is stable to perturbations of the filter function in a "
                "coarse sense (Carrière-Oudot 2018), but lacks the precise stability of "
                "persistence diagrams (no bottleneck distance theorem for Mapper)."
            ),
            chapter_targets=("9", "19"),
        ),
    )


def persistence_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_persistence_profiles()
    ))


def persistence_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_persistence_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def persistence_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from complex_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_persistence_profiles():
        index.setdefault(p.complex_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def has_finite_barcode(space: Any) -> Result:
    """Check whether the filtration yields a finite persistence barcode.

    A filtration has a finite barcode if the number of birth-death pairs is finite.
    This holds whenever the filtration is a finite sequence of finite simplicial
    complexes (e.g., Vietoris-Rips on a finite point cloud). Key facts:
    - All finite point cloud filtrations (VR, Čech, alpha) have finite barcodes.
    - Sublevel set filtrations of tame functions on compact spaces have finite barcodes.
    - Non-tame functions (e.g., with infinitely many critical values) may have infinite
      barcodes.

    Decision layers
    ---------------
    1. Explicit 'barcode' or 'persistence_diagram' tag -> true.
    2. VR / Čech / sublevel filtration tags -> true (finite point cloud / tame).
    3. Non-tame / infinite tags -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, PERSISTENCE_DIAGRAM_TAGS):
        witness = next(t for t in tags if t in PERSISTENCE_DIAGRAM_TAGS)
        return Result.true(
            mode="theorem",
            value="finite_barcode",
            justification=[
                f"Tag {witness!r}: the filtration has a finite persistence barcode — "
                "a finite multiset of birth-death pairs (b, d) with b <= d.",
            ],
            metadata={**base, "criterion": "explicit_barcode", "witness": witness},
        )

    if _matches_any(tags, VIETORIS_RIPS_TAGS | CECH_COMPLEX_TAGS | SUBLEVEL_SET_TAGS):
        witness = next(t for t in tags
                       if t in VIETORIS_RIPS_TAGS | CECH_COMPLEX_TAGS | SUBLEVEL_SET_TAGS)
        return Result.true(
            mode="theorem",
            value="finite_barcode",
            justification=[
                f"Tag {witness!r}: finite point cloud or tame function filtration — "
                "the barcode is finite (finitely many simplices, finitely many "
                "birth-death pairs by the structure theorem).",
            ],
            metadata={**base, "criterion": "finite_filtration", "witness": witness},
        )

    if _matches_any(tags, UNSTABLE_OR_SENSITIVE_TAGS | {"non_tame_function",
                                                          "infinite_filtration"}):
        blocking = next(t for t in tags
                        if t in UNSTABLE_OR_SENSITIVE_TAGS | {"non_tame_function",
                                                               "infinite_filtration"})
        return Result.false(
            mode="theorem",
            value="finite_barcode",
            justification=[
                f"Tag {blocking!r}: the barcode may be infinite — "
                "non-tame functions or infinite filtrations can produce infinitely "
                "many birth-death pairs.",
            ],
            metadata={**base, "criterion": "infinite_barcode"},
        )

    return Result.unknown(
        mode="symbolic",
        value="finite_barcode",
        justification=[
            "Insufficient tags to determine finiteness of barcode. "
            "Supply tags such as 'barcode', 'vietoris_rips', 'cech_complex', "
            "'sublevel_set_filtration', or 'non_tame_function'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_stable_filtration(space: Any) -> Result:
    """Check whether the persistence diagram is stable under perturbations.

    The stability theorem (Cohen-Steiner, Edelsbrunner, Harer 2007): for tame functions
    f, g: X -> R, d_B(Dgm(f), Dgm(g)) <= ||f - g||_infty. This means small changes
    in the input (noise) cause small changes in the diagram (bottleneck distance).
    Key stable filtrations: sublevel sets, VR/Čech (via distance functions), alpha.
    Key unstable: Mapper (no direct stability in bottleneck sense).

    Decision layers
    ---------------
    1. Explicit 'stability_theorem' or 'stable_filtration' tag -> true.
    2. VR / Čech / sublevel filtration -> true.
    3. Not-stable / sensitive-to-noise / Mapper tags -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, STABLE_FILTRATION_TAGS):
        witness = next(t for t in tags if t in STABLE_FILTRATION_TAGS)
        return Result.true(
            mode="theorem",
            value="stable_filtration",
            justification=[
                f"Tag {witness!r}: the filtration is stable — the stability theorem "
                "guarantees d_B(Dgm(f), Dgm(g)) <= ||f - g||_infty for tame functions. "
                "Small perturbations of the input give small perturbations of the diagram.",
            ],
            metadata={**base, "criterion": "explicit_stable", "witness": witness},
        )

    if _matches_any(tags, VIETORIS_RIPS_TAGS | CECH_COMPLEX_TAGS):
        witness = next(t for t in tags if t in VIETORIS_RIPS_TAGS | CECH_COMPLEX_TAGS)
        return Result.true(
            mode="theorem",
            value="stable_filtration",
            justification=[
                f"Tag {witness!r}: VR and Čech filtrations are stable — they arise as "
                "sublevel filtrations of the distance function d(·, X), which is 1-Lipschitz. "
                "The stability theorem applies.",
            ],
            metadata={**base, "criterion": "rips_cech_stable", "witness": witness},
        )

    if _matches_any(tags, UNSTABLE_OR_SENSITIVE_TAGS | {"mapper_graph",
                                                          "cover_filtration",
                                                          "not_stable"}):
        blocking = next(t for t in tags
                        if t in UNSTABLE_OR_SENSITIVE_TAGS | {"mapper_graph",
                                                               "cover_filtration",
                                                               "not_stable"})
        return Result.false(
            mode="theorem",
            value="stable_filtration",
            justification=[
                f"Tag {blocking!r}: the filtration is NOT stable in the bottleneck sense. "
                "The Mapper algorithm does not admit a persistence diagram and lacks "
                "the stability theorem guarantee.",
            ],
            metadata={**base, "criterion": "not_stable"},
        )

    return Result.unknown(
        mode="symbolic",
        value="stable_filtration",
        justification=[
            "Insufficient tags to determine stability. "
            "Supply tags such as 'stability_theorem', 'vietoris_rips', 'cech_filtration', "
            "'sublevel_set_filtration', 'not_stable', or 'mapper_graph'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_essential_classes(space: Any) -> Result:
    """Check whether the filtration has essential homology classes (infinite bars).

    Essential classes are persistence classes that are born but never die (death = +infty).
    They correspond to non-trivial homology classes of the underlying space. Key facts:
    - H_0 always has one essential class for each connected component of the full complex.
    - H_k (k >= 1) has essential classes iff H_k of the full complex is non-trivial.
    - For a point cloud sampled from S^1: one essential H_0 class, one essential H_1 class.
    - For sublevel sets of a Morse function on a closed manifold: essential classes in
      H_0 (one) and H_n (one, if orientable).

    Decision layers
    ---------------
    1. Explicit 'essential_homology' or 'infinite_bar' tag -> true.
    2. Non-contractible / known topology tags -> true.
    3. Contractible full complex (e.g., VR of convex set) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, ESSENTIAL_CLASS_TAGS):
        witness = next(t for t in tags if t in ESSENTIAL_CLASS_TAGS)
        return Result.true(
            mode="theorem",
            value="essential_classes",
            justification=[
                f"Tag {witness!r}: the filtration has essential homology classes — "
                "persistence pairs (b, +infty) corresponding to non-trivial homology "
                "of the underlying topological space.",
            ],
            metadata={**base, "criterion": "explicit_essential", "witness": witness},
        )

    non_contractible = {
        "non_contractible", "circle_data", "torus_data", "sphere_data",
        "non_trivial_topology", "closed_manifold_data",
    }
    if _matches_any(tags, non_contractible):
        witness = next(t for t in tags if t in non_contractible)
        return Result.true(
            mode="theorem",
            value="essential_classes",
            justification=[
                f"Tag {witness!r}: the full complex has non-trivial homology — "
                "essential classes exist corresponding to non-trivial H_k of the space.",
            ],
            metadata={**base, "criterion": "non_contractible_topology", "witness": witness},
        )

    no_essential = {
        "contractible_data", "convex_point_cloud", "tree_data",
        "no_essential_classes", "contractible_full_complex",
    }
    if _matches_any(tags, no_essential):
        blocking = next(t for t in tags if t in no_essential)
        return Result.false(
            mode="theorem",
            value="essential_classes",
            justification=[
                f"Tag {blocking!r}: the full complex is contractible — no essential "
                "classes in H_k for k >= 1. H_0 has one essential class (connected). "
                "All bars are finite.",
            ],
            metadata={**base, "criterion": "contractible_no_essential"},
        )

    return Result.unknown(
        mode="symbolic",
        value="essential_classes",
        justification=[
            "Insufficient tags to determine essential classes. "
            "Supply tags such as 'essential_homology', 'infinite_bar', 'non_contractible', "
            "'circle_data', 'contractible_data', or 'no_essential_classes'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_structure_theorem(space: Any) -> Result:
    """Check whether the persistence module decomposes via the structure theorem.

    The structure theorem (Zomorodian-Carlsson 2005) holds for finitely presented
    persistence modules over a field. It gives a unique decomposition into interval
    modules, with the barcode as the complete isomorphism invariant. Key facts:
    - Holds for all finite filtrations with field coefficients.
    - Fails for persistence modules over Z (not a field, not a PID in the graded sense
      used): torsion can appear, and interval decomposition is not unique.
    - For zigzag persistence modules (alternating maps), a generalized structure theorem
      holds (Gabriel's theorem for quiver representations of type A).

    Decision layers
    ---------------
    1. Explicit 'structure_theorem' or 'interval_decomposition' tag -> true.
    2. Field coefficients + finite filtration -> true.
    3. Z-coefficients or infinite / non-field tags -> false (structure theorem may fail).
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, STRUCTURE_THEOREM_TAGS):
        witness = next(t for t in tags if t in STRUCTURE_THEOREM_TAGS)
        return Result.true(
            mode="theorem",
            value="structure_theorem",
            justification=[
                f"Tag {witness!r}: the persistence module decomposes as "
                "M ≅ ⊕_j k[b_j, d_j) — a unique sum of interval modules over field k. "
                "The barcode {[b_j, d_j)} is the complete isomorphism invariant.",
            ],
            metadata={**base, "criterion": "explicit_structure_theorem", "witness": witness},
        )

    if _matches_any(tags, FIELD_COEFFICIENTS_TAGS) and _matches_any(
        tags, VIETORIS_RIPS_TAGS | CECH_COMPLEX_TAGS | SUBLEVEL_SET_TAGS |
        {"finite_filtration", "persistence_module"}
    ):
        witness = next(t for t in tags if t in FIELD_COEFFICIENTS_TAGS)
        return Result.true(
            mode="theorem",
            value="structure_theorem",
            justification=[
                f"Tag {witness!r} with finite filtration: field coefficients + finite "
                "filtration satisfies the conditions of the structure theorem. "
                "The persistence module decomposes into interval modules over the field.",
            ],
            metadata={**base, "criterion": "field_coefficients_structure"},
        )

    no_structure = {
        "integer_coefficients", "z_coefficients",
        "torsion_persistence", "non_field_coefficients",
        "infinite_filtration",
    }
    if _matches_any(tags, no_structure):
        blocking = next(t for t in tags if t in no_structure)
        return Result.false(
            mode="theorem",
            value="structure_theorem",
            justification=[
                f"Tag {blocking!r}: the structure theorem in its standard form does NOT "
                "apply. Over Z (not a field), the persistence module may have torsion and "
                "the interval decomposition is not guaranteed to be unique or to exist.",
            ],
            metadata={**base, "criterion": "no_structure_theorem"},
        )

    return Result.unknown(
        mode="symbolic",
        value="structure_theorem",
        justification=[
            "Insufficient tags to determine structure theorem applicability. "
            "Supply tags such as 'structure_theorem', 'field_coefficients', "
            "'z2_coefficients', 'integer_coefficients', or 'finite_filtration'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_persistence(space: Any) -> dict[str, Any]:
    """Classify the persistent homology type of the filtration.

    Keys
    ----
    persistence_class : str
        One of ``"stable_finite"``, ``"stable_essential"``, ``"algebraic"``,
        ``"qualitative"``, ``"unknown"``.
    has_finite_barcode : Result
    is_stable_filtration : Result
    has_essential_classes : Result
    has_structure_theorem : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    barcode_r = has_finite_barcode(space)
    stable_r = is_stable_filtration(space)
    essential_r = has_essential_classes(space)
    structure_r = has_structure_theorem(space)

    if stable_r.is_true and barcode_r.is_true and essential_r.is_true:
        persistence_class = "stable_essential"
    elif stable_r.is_true and barcode_r.is_true:
        persistence_class = "stable_finite"
    elif structure_r.is_true and barcode_r.is_true:
        persistence_class = "algebraic"
    elif stable_r.is_false or _matches_any(tags, {"mapper_graph", "cover_filtration"}):
        persistence_class = "qualitative"
    else:
        persistence_class = "unknown"

    key_properties: list[str] = []
    if barcode_r.is_true:
        key_properties.append("finite_barcode")
    if stable_r.is_true:
        key_properties.append("stable")
    if stable_r.is_false:
        key_properties.append("not_stable")
    if essential_r.is_true:
        key_properties.append("essential_classes")
    if structure_r.is_true:
        key_properties.append("structure_theorem")
    if _matches_any(tags, VIETORIS_RIPS_TAGS):
        key_properties.append("vietoris_rips")
    if _matches_any(tags, CECH_COMPLEX_TAGS):
        key_properties.append("cech_complex")
    if _matches_any(tags, FIELD_COEFFICIENTS_TAGS):
        key_properties.append("field_coefficients")
    if _matches_any(tags, {"mapper_graph", "cover_filtration"}):
        key_properties.append("mapper_qualitative")

    return {
        "persistence_class": persistence_class,
        "has_finite_barcode": barcode_r,
        "is_stable_filtration": stable_r,
        "has_essential_classes": essential_r,
        "has_structure_theorem": structure_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def persistence_profile(space: Any) -> dict[str, Any]:
    """Full persistent homology profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_persistence`.
    named_profiles : tuple[PersistenceProfile, ...]
        Registry of canonical persistent homology examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_persistence(space),
        "named_profiles": get_named_persistence_profiles(),
        "layer_summary": persistence_layer_summary(),
    }


# ===========================================================================
# Constructive persistent-homology engine
# ---------------------------------------------------------------------------
# Everything above is the descriptive/profile layer (preserved for backward
# compatibility). Below is a genuine, dependency-free computation: a
# Vietoris-Rips filtration of a finite metric space, the standard column
# reduction of its boundary matrix over Z/2, and the resulting persistence
# pairs / barcodes. Coefficients are Z/2 (the field used by the classical
# persistence algorithm).
# ===========================================================================


@dataclass(frozen=True)
class FilteredComplex:
    """A Vietoris-Rips style filtration of simplices in filtration order.

    Simplices are tuples of integer vertex indices (sorted). ``births[i]`` is the
    scale at which ``simplices[i]`` enters; ``dimensions[i]`` is its dimension.
    The order satisfies ``births`` nondecreasing with faces before their cofaces.
    """

    simplices: tuple[tuple[int, ...], ...]
    births: tuple[float, ...]
    dimensions: tuple[int, ...]

    def size(self) -> int:
        return len(self.simplices)


@dataclass(frozen=True)
class PersistencePair:
    """A single bar of the persistence barcode in a fixed homological degree."""

    dimension: int
    birth: float
    death: float  # math.inf for an essential (never-dying) class

    @property
    def is_essential(self) -> bool:
        return math.isinf(self.death)

    @property
    def persistence(self) -> float:
        return self.death - self.birth


def vietoris_rips_filtration(
    space: Any,
    max_dimension: int = 1,
    max_scale: float | None = None,
) -> FilteredComplex:
    """Build the Vietoris-Rips filtration of a finite metric ``space``.

    ``space`` is any object exposing ``carrier`` (a finite sequence of points)
    and ``distance_between(x, y)``. A ``k``-simplex enters at its diameter (the
    maximum pairwise distance among its vertices). Simplices of dimension above
    ``max_dimension`` are not generated; those entering after ``max_scale`` (when
    given) are dropped.
    """

    if max_dimension < 0:
        raise ValueError("max_dimension must be nonnegative.")
    points = list(space.carrier)
    n = len(points)
    if n == 0:
        raise ValueError("Vietoris-Rips filtration requires a nonempty point set.")

    def dist(i: int, j: int) -> float:
        return float(space.distance_between(points[i], points[j]))

    entries: list[tuple[float, int, tuple[int, ...]]] = [(0.0, 0, (i,)) for i in range(n)]
    for k in range(1, max_dimension + 1):
        for combo in combinations(range(n), k + 1):
            birth = max(dist(a, b) for a, b in combinations(combo, 2))
            if max_scale is not None and birth > max_scale:
                continue
            entries.append((birth, k, combo))

    entries.sort(key=lambda entry: (entry[0], entry[1], entry[2]))
    return FilteredComplex(
        simplices=tuple(entry[2] for entry in entries),
        births=tuple(entry[0] for entry in entries),
        dimensions=tuple(entry[1] for entry in entries),
    )


def persistence_pairs(
    filtered: FilteredComplex,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Compute persistence pairs via standard Z/2 boundary-matrix reduction.

    Returns one :class:`PersistencePair` per homology class. Essential classes
    have ``death = inf``. Zero-persistence pairs (birth equal to death) are
    omitted unless ``include_zero_persistence`` is set.
    """

    index_of = {simplex: idx for idx, simplex in enumerate(filtered.simplices)}
    columns: list[set[int]] = []
    for simplex, dimension in zip(filtered.simplices, filtered.dimensions):
        if dimension == 0:
            columns.append(set())
        else:
            faces = combinations(simplex, len(simplex) - 1)
            columns.append({index_of[face] for face in faces})

    low_inverse: dict[int, int] = {}  # pivot row -> reducing column index
    for j in range(len(columns)):
        while columns[j]:
            pivot = max(columns[j])
            if pivot in low_inverse:
                columns[j] ^= columns[low_inverse[pivot]]
            else:
                low_inverse[pivot] = j
                break

    pairs: list[PersistencePair] = []
    for creator, destroyer in low_inverse.items():
        birth = filtered.births[creator]
        death = filtered.births[destroyer]
        if not include_zero_persistence and death == birth:
            continue
        pairs.append(PersistencePair(filtered.dimensions[creator], birth, death))

    paired_creators = set(low_inverse)
    for i in range(len(columns)):
        if not columns[i] and i not in paired_creators:
            pairs.append(PersistencePair(filtered.dimensions[i], filtered.births[i], math.inf))

    return tuple(sorted(pairs, key=lambda pair: (pair.dimension, pair.birth, pair.death)))


def persistent_homology(
    space: Any,
    max_dimension: int = 1,
    max_scale: float | None = None,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Convenience: Vietoris-Rips filtration followed by persistence reduction.

    Complexity
    ----------
    The Vietoris-Rips complex on ``n`` points to dimension ``d`` has
    ``O(n^{d+2})`` simplices, and the Z/2 reduction is ``O(m³)`` in the number of
    simplices ``m`` — so this is for **small point clouds** (``n`` of order a few
    dozen for small ``d``). See ``docs/COMPLEXITY.md``.
    """

    filtered = vietoris_rips_filtration(space, max_dimension=max_dimension, max_scale=max_scale)
    return persistence_pairs(filtered, include_zero_persistence=include_zero_persistence)


def barcode(
    pairs: tuple[PersistencePair, ...],
    dimension: int | None = None,
) -> tuple[tuple[float, float], ...]:
    """Return ``(birth, death)`` bars, optionally restricted to one ``dimension``."""

    selected = [p for p in pairs if dimension is None or p.dimension == dimension]
    return tuple((p.birth, p.death) for p in sorted(selected, key=lambda p: (p.birth, p.death)))


def persistence_diagram(pairs: tuple[PersistencePair, ...]) -> dict[int, tuple[tuple[float, float], ...]]:
    """Group persistence pairs into a per-dimension diagram of ``(birth, death)``."""

    diagram: dict[int, list[tuple[float, float]]] = {}
    for pair in pairs:
        diagram.setdefault(pair.dimension, []).append((pair.birth, pair.death))
    return {dim: tuple(sorted(bars)) for dim, bars in sorted(diagram.items())}


def persistence_betti_numbers(pairs: tuple[PersistencePair, ...]) -> dict[int, int]:
    """Count essential (infinite-lifetime) classes per homological dimension.

    Essential pairs — those with ``death = ∞`` — correspond to homology classes
    that survive the entire filtration.  Their count per dimension is the Betti
    number β_k of the underlying space (assuming the filtration is complete).

    Parameters
    ----------
    pairs:
        Output of :func:`persistence_pairs`, :func:`persistence_pairs_twist`,
        or any function returning a tuple of :class:`PersistencePair` objects.

    Returns
    -------
    dict[int, int]
        ``{dimension: betti_number}`` for every dimension that has at least one
        essential class.  Dimensions with no essential classes are absent (not 0).

    Examples
    --------
    A circle point cloud has β₀ = 1 and β₁ = 1::

        pairs = persistence_pairs(vietoris_rips_filtration(circle_cloud))
        persistence_betti_numbers(pairs)   # {0: 1, 1: 1}
    """
    result: dict[int, int] = {}
    for pair in pairs:
        if pair.is_essential:
            result[pair.dimension] = result.get(pair.dimension, 0) + 1
    return result


def euler_characteristic_curve(
    filtered: FilteredComplex,
    scales: tuple[float, ...],
) -> tuple[tuple[float, int], ...]:
    """Return ``(scale, chi)`` pairs: the Euler characteristic of each sublevel set."""

    curve: list[tuple[float, int]] = []
    for scale in scales:
        chi = sum(
            (-1) ** filtered.dimensions[i]
            for i in range(filtered.size())
            if filtered.births[i] <= scale
        )
        curve.append((scale, chi))
    return tuple(curve)


__all__ = [
    "PersistenceProfile",
    "VIETORIS_RIPS_TAGS",
    "CECH_COMPLEX_TAGS",
    "PERSISTENCE_DIAGRAM_TAGS",
    "STABLE_FILTRATION_TAGS",
    "UNSTABLE_OR_SENSITIVE_TAGS",
    "ESSENTIAL_CLASS_TAGS",
    "SUBLEVEL_SET_TAGS",
    "FIELD_COEFFICIENTS_TAGS",
    "STRUCTURE_THEOREM_TAGS",
    "get_named_persistence_profiles",
    "persistence_layer_summary",
    "persistence_chapter_index",
    "persistence_type_index",
    "has_finite_barcode",
    "is_stable_filtration",
    "has_essential_classes",
    "has_structure_theorem",
    "classify_persistence",
    "persistence_profile",
    "FilteredComplex",
    "PersistencePair",
    "vietoris_rips_filtration",
    "persistence_pairs",
    "persistent_homology",
    "barcode",
    "persistence_betti_numbers",
    "persistence_diagram",
    "euler_characteristic_curve",
]
