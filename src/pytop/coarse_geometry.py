"""Coarse geometry: quasi-isometries, asymptotic dimension, ends, and Property A.

Key theorems implemented
------------------------
- Quasi-isometry: a map f: X -> Y between metric spaces is a (L,C)-quasi-isometry
  if (1/L)*d_X(x,x') - C <= d_Y(f(x),f(x')) <= L*d_X(x,x') + C for all x,x' in X
  and every y in Y is within distance C of f(X). Quasi-isometry is the fundamental
  equivalence relation of large-scale (coarse) geometry.
- Gromov's theorem: a finitely generated group has polynomial growth if and only
  if it is virtually nilpotent. Polynomial growth groups are QI to their asymptotic
  cones (nilpotent Lie groups with Carnot-Caratheodory metric).
- Virtually abelian groups are quasi-isometric to R^n (for appropriate n).
  Non-abelian nilpotent groups have polynomial growth but are NOT QI to R^n:
  the Heisenberg group H_3(Z) has polynomial growth of degree 4 but its asymptotic
  cone is the Carnot group, not R^4.
- Asymptotic dimension (Gromov 1993): asdim(X) <= n if for every R > 0 there
  exists a cover of X by uniformly bounded sets of multiplicity <= n+1.
  Key values: asdim(Z^n) = n, asdim(free group) = 1, asdim(H^n) = n.
- Stallings' theorem: a finitely generated group has more than one end iff it
  splits (non-trivially) over a finite subgroup. Exactly:
  0 ends: finite groups; 1 end: most infinite groups; 2 ends: virtually Z groups;
  infinitely many ends: amalgamated products/HNN extensions over finite groups.
- Property A (Yu 2000): a coarse analogue of amenability for metric spaces.
  Property A implies coarse embeddability into a Hilbert space, which implies the
  coarse Baum-Connes conjecture (Kasparov-Yu). Key facts:
  - Amenable groups have Property A.
  - Hyperbolic groups have Property A (Yu 2000).
  - Linear groups have Property A (Guentner-Higson-Weinberger).
  - Expander graph families do NOT have Property A; they do not coarsely embed
    into any Hilbert space (Gromov).
- The Hopf-Rinow theorem fails in general metric spaces: completeness and local
  compactness together do not imply geodesic completeness (unlike Riemannian manifolds).
- Gromov hyperbolicity: a geodesic metric space X is delta-hyperbolic if every
  geodesic triangle is delta-slim (each side lies in the delta-neighbourhood of
  the other two). Key examples: H^n (hyperbolic space), trees (delta=0), free groups
  (Cayley graph with standard generators), and CAT(-1) spaces.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class CoarseGeometryProfile:
    """A curated coarse geometry example."""

    key: str
    display_name: str
    geometry_type: str
    asymptotic_dimension: str
    number_of_ends: str
    has_property_a: bool
    is_gromov_hyperbolic: bool
    is_quasi_isometric_to_euclidean: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

FINITE_ASYMPTOTIC_DIM_TAGS: set[str] = {
    "finite_asymptotic_dimension", "asdim_finite",
    "asdim_zero", "asdim_one", "asdim_two",
    "virtually_abelian", "virtually_nilpotent",
    "hyperbolic_group", "gromov_hyperbolic",
    "free_group", "finite_group",
    "relatively_hyperbolic",
    "coxeter_group", "right_angled_artin_group",
    "mapping_class_group",
    "z_lattice", "euclidean_lattice",
}

PROPERTY_A_TAGS: set[str] = {
    "property_a", "coarsely_amenable",
    "amenable_group",
    "virtually_abelian", "virtually_nilpotent",
    "hyperbolic_group", "gromov_hyperbolic",
    "linear_group", "exact_group",
    "free_group", "finite_group",
    "relatively_hyperbolic",
    "right_angled_artin_group",
    "countable_amenable",
}

HYPERBOLIC_TAGS: set[str] = {
    "hyperbolic_group", "gromov_hyperbolic", "delta_hyperbolic",
    "hyperbolic_space", "free_group",
    "surface_group_hyperbolic",
    "cocompact_lattice_hyperbolic",
    "cat_negative_curvature",
    "tree_group",
}

POLYNOMIAL_GROWTH_TAGS: set[str] = {
    "polynomial_growth",
    "virtually_nilpotent", "virtually_abelian",
    "nilpotent_group", "abelian_group",
    "finite_group", "amenable_polynomial",
    "heisenberg_group",
    "z_lattice", "euclidean_lattice",
}

EXPONENTIAL_GROWTH_TAGS: set[str] = {
    "exponential_growth",
    "free_group", "hyperbolic_group",
    "non_amenable_group",
    "solvable_exponential",
    "linear_group_exponential",
}

TWO_ENDS_TAGS: set[str] = {
    "two_ends", "virtually_z",
    "integer_group", "infinite_cyclic",
    "z_group",
}

INFINITE_ENDS_TAGS: set[str] = {
    "infinitely_many_ends",
    "free_group", "free_group_rank_geq_2",
    "amalgam_over_finite",
    "infinite_ends",
    "free_product_nontrivial",
}

ONE_END_TAGS: set[str] = {
    "one_end",
    "surface_group", "hyperbolic_group_one_end",
    "virtually_z_n_n_geq_2",
    "simply_connected_at_infinity",
    "nilpotent_group",
    "heisenberg_group",
    "z_lattice_n_geq_2",
}

NOT_PROPERTY_A_TAGS: set[str] = {
    "not_property_a", "no_property_a",
    "expander_graph", "expander_family",
    "no_coarse_embedding_hilbert",
    "gromov_monster",
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

def get_named_coarse_geometry_profiles() -> tuple[CoarseGeometryProfile, ...]:
    """Return the registry of canonical coarse geometry examples."""
    return (
        CoarseGeometryProfile(
            key="integer_line",
            display_name="Z — the integers as a metric space",
            geometry_type="euclidean",
            asymptotic_dimension="1",
            number_of_ends="2",
            has_property_a=True,
            is_gromov_hyperbolic=True,
            is_quasi_isometric_to_euclidean=True,
            presentation_layer="main_text",
            focus=(
                "The integers (Z, d_word) with the word metric (d(m,n) = |m-n|) are "
                "quasi-isometric to the real line R: the inclusion Z -> R is a "
                "(1,1)-quasi-isometry. Z is virtually cyclic (it IS cyclic), so by "
                "Stallings' theorem, it has exactly 2 ends: informally, the two "
                "'directions to infinity' (+inf and -inf). "
                "Asymptotic dimension: asdim(Z) = 1. Any R-neighbourhood of Z can be "
                "covered by intervals of diameter 2R+1, with multiplicity <= 2 = 1+1. "
                "Z is Gromov hyperbolic (delta = 0: every geodesic triangle in a tree "
                "or in R is 0-slim). It has polynomial growth of degree 1 (|B(n)| = 2n+1). "
                "Z is amenable (it is abelian), so it has Property A. "
                "The Cayley graph of Z with generators {+1,-1} is the two-way infinite path."
            ),
            chapter_targets=("9", "27", "51"),
        ),
        CoarseGeometryProfile(
            key="euclidean_lattice",
            display_name="Z^n — Euclidean lattice (n >= 2)",
            geometry_type="euclidean",
            asymptotic_dimension="n",
            number_of_ends="1",
            has_property_a=True,
            is_gromov_hyperbolic=False,
            is_quasi_isometric_to_euclidean=True,
            presentation_layer="main_text",
            focus=(
                "The group Z^n with the word metric is quasi-isometric to R^n: "
                "the natural inclusion Z^n -> R^n is a (1, sqrt(n))-quasi-isometry. "
                "For n >= 2, Z^n has exactly 1 end: the complement of any finite ball "
                "is connected at infinity. (For n = 1: Z has 2 ends; for n >= 2: 1 end.) "
                "Asymptotic dimension: asdim(Z^n) = n. This equals the topological "
                "dimension of R^n, illustrating that asdim is the large-scale analogue "
                "of topological dimension. "
                "Z^n is NOT Gromov hyperbolic for n >= 2: quadrilaterals in Z^n "
                "cannot be made delta-slim for any fixed delta. "
                "Z^n has polynomial growth of degree n (|B(r)| ~ C*r^n). By Gromov's "
                "theorem, polynomial growth characterises virtually nilpotent groups. "
                "Z^n is amenable (abelian), hence has Property A."
            ),
            chapter_targets=("9", "27", "51"),
        ),
        CoarseGeometryProfile(
            key="free_group_rank2",
            display_name="F_2 — free group of rank 2",
            geometry_type="hyperbolic",
            asymptotic_dimension="1",
            number_of_ends="infinite",
            has_property_a=True,
            is_gromov_hyperbolic=True,
            is_quasi_isometric_to_euclidean=False,
            presentation_layer="main_text",
            focus=(
                "The free group F_2 = <a,b | > on two generators, with the word metric "
                "from the standard generating set {a,b,a^{-1},b^{-1}}, has Cayley graph "
                "homeomorphic to a 4-regular tree T_4. F_2 is Gromov hyperbolic (delta = 0, "
                "since its Cayley graph is a tree). "
                "F_2 has infinitely many ends: removing any vertex of the tree T_4 leaves "
                "4 infinite connected components; more precisely, any finite set separates "
                "T_4 into infinitely many unbounded components. By Stallings' theorem, "
                "a finitely generated group has infinitely many ends iff it splits as "
                "a non-trivial amalgamated product or HNN extension over a finite group "
                "(F_2 = Z * Z, the free product). "
                "Asymptotic dimension: asdim(F_2) = 1 (trees have asdim = 1). "
                "F_2 is NOT quasi-isometric to any R^n (exponential growth vs polynomial). "
                "F_2 is non-amenable (contains Z * Z), but has Property A (Yu 2000: "
                "all hyperbolic groups have Property A) and coarsely embeds into L^2."
            ),
            chapter_targets=("9", "27", "51"),
        ),
        CoarseGeometryProfile(
            key="hyperbolic_plane",
            display_name="H^2 — hyperbolic plane",
            geometry_type="hyperbolic",
            asymptotic_dimension="2",
            number_of_ends="1",
            has_property_a=True,
            is_gromov_hyperbolic=True,
            is_quasi_isometric_to_euclidean=False,
            presentation_layer="main_text",
            focus=(
                "The hyperbolic plane H^2 (with curvature -1) is the paradigmatic "
                "example of a Gromov hyperbolic geodesic metric space. It is "
                "delta-hyperbolic with delta = log(1 + sqrt(2)) (the slimness constant "
                "of ideal triangles). H^2 has exactly 1 end. "
                "Asymptotic dimension: asdim(H^2) = 2. More generally, asdim(H^n) = n. "
                "Despite having the same asdim as R^2, the spaces H^2 and R^2 are "
                "NOT quasi-isometric: H^2 has exponential volume growth (Vol(B(r)) ~ e^r) "
                "while R^2 has polynomial growth (Vol(B(r)) ~ pi*r^2). "
                "The isometry group of H^2 is PGL(2,R). Cocompact lattices Gamma in "
                "Isom(H^2) are quasi-isometric to H^2 (Milnor-Svarc lemma). "
                "Fundamental groups of closed hyperbolic surfaces are hyperbolic groups "
                "and QI to H^2. H^2 has Property A (it is a CAT(-1) space). "
                "The boundary at infinity of H^2 is the circle S^1."
            ),
            chapter_targets=("9", "27", "51"),
        ),
        CoarseGeometryProfile(
            key="heisenberg_group",
            display_name="H_3(Z) — discrete Heisenberg group",
            geometry_type="nilpotent",
            asymptotic_dimension="4",
            number_of_ends="1",
            has_property_a=True,
            is_gromov_hyperbolic=False,
            is_quasi_isometric_to_euclidean=False,
            presentation_layer="selected_block",
            focus=(
                "The discrete Heisenberg group H_3(Z) consists of upper-triangular "
                "3x3 integer matrices with 1s on the diagonal. It is a finitely generated "
                "nilpotent group (class 2) with polynomial growth of degree 4 "
                "(Bass formula: the growth degree of a nilpotent group equals the sum "
                "of i * rank(gamma_i/gamma_{i+1}) over the lower central series). "
                "By Gromov's theorem, H_3(Z) is virtually nilpotent, hence has "
                "polynomial growth, and conversely. "
                "Asymptotic dimension: asdim(H_3(Z)) = 4 (same as the growth degree). "
                "H_3(Z) has 1 end (nilpotent groups of infinite order have 1 end). "
                "H_3(Z) is NOT quasi-isometric to R^4, despite having polynomial growth "
                "of degree 4: the asymptotic cone of H_3(Z) is the Carnot group "
                "(sub-Riemannian Heisenberg group), not Euclidean space. "
                "This shows that polynomial growth does not imply QI to Euclidean space. "
                "H_3(Z) has Property A (amenable: nilpotent => solvable => amenable)."
            ),
            chapter_targets=("9", "27"),
        ),
        CoarseGeometryProfile(
            key="expander_family",
            display_name="Expander graphs — e.g., Cayley graphs of SL(2, Z/pZ)",
            geometry_type="expander",
            asymptotic_dimension="1",
            number_of_ends="0",
            has_property_a=False,
            is_gromov_hyperbolic=False,
            is_quasi_isometric_to_euclidean=False,
            presentation_layer="selected_block",
            focus=(
                "An expander family is a sequence of finite k-regular graphs "
                "{G_n} with |G_n| -> inf and a uniform spectral gap: the second "
                "eigenvalue of the adjacency matrix is bounded away from k. "
                "Equivalently, the Cheeger constant h(G_n) is uniformly bounded below. "
                "Expanders are used in theoretical computer science, coding theory, "
                "and cryptography. The Cayley graphs of SL(2, Z/pZ) with fixed "
                "generating set (as p ranges over primes) form an expander family "
                "(Selberg's 3/16 theorem / Margulis). "
                "The disjoint union X = union G_n (with unit speed metric on each "
                "component) does NOT have Property A: no equivariant coarsening "
                "provides the required amenability-at-infinity. "
                "Gromov showed that expander families do not coarsely embed into any "
                "Hilbert space (or even into L^p for p >= 1). "
                "Expander families are the primary obstruction to the coarse "
                "Baum-Connes conjecture and underlie Gromov's construction of "
                "'monster' groups that contain expanders in their Cayley graphs. "
                "Each finite component G_n has asdim = 1 (finite graphs are trees "
                "QI-wise), but the family as a whole lacks uniform coarse properties."
            ),
            chapter_targets=("9", "27"),
        ),
    )


def coarse_geometry_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_coarse_geometry_profiles()
    ))


def coarse_geometry_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_coarse_geometry_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def coarse_geometry_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from geometry_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_coarse_geometry_profiles():
        index.setdefault(p.geometry_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def has_finite_asymptotic_dimension(space: Any) -> Result:
    """Check whether space has finite asymptotic dimension.

    The asymptotic dimension asdim(X) of a metric space X is the smallest n
    such that for every R > 0 there exists a cover of X by uniformly bounded
    sets with multiplicity <= n+1. Key values:
    - asdim(finite group) = 0.
    - asdim(Z) = asdim(R) = asdim(tree) = 1.
    - asdim(Z^n) = asdim(R^n) = asdim(H^n) = n.
    - asdim(hyperbolic group) < infinity (Bell-Dranishnikov 2001).
    - asdim(free group F_n) = 1 (Cayley graph is a tree).
    - Expander families: each finite component has asdim = 1, but the
      disjoint union has infinite asdim (no uniform control).

    Decision layers
    ---------------
    1. Explicit finite asdim / virtually abelian / nilpotent tag -> true.
    2. Hyperbolic group (Bell-Dranishnikov theorem) -> true.
    3. Free group (Cayley graph is a tree, asdim = 1) -> true.
    4. Right-angled Artin group or Coxeter group -> true.
    5. Expander family (infinite disjoint union: no finite asdim) -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"finite_asymptotic_dimension", "asdim_finite",
                            "virtually_abelian", "virtually_nilpotent",
                            "asdim_zero", "asdim_one", "asdim_two",
                            "z_lattice", "euclidean_lattice", "finite_group"}):
        witness = next(t for t in tags if t in {
            "finite_asymptotic_dimension", "asdim_finite",
            "virtually_abelian", "virtually_nilpotent",
            "asdim_zero", "asdim_one", "asdim_two",
            "z_lattice", "euclidean_lattice", "finite_group",
        })
        return Result.true(
            mode="theorem",
            value="finite_asymptotic_dimension",
            justification=[
                f"Tag {witness!r}: the space has finite asymptotic dimension. "
                "Virtually abelian and nilpotent groups have asdim equal to their "
                "Hirsch length. Finite groups have asdim = 0.",
            ],
            metadata={**base, "criterion": "finite_asdim_tag", "witness": witness},
        )

    if _matches_any(tags, HYPERBOLIC_TAGS):
        witness = next(t for t in tags if t in HYPERBOLIC_TAGS)
        return Result.true(
            mode="theorem",
            value="finite_asymptotic_dimension",
            justification=[
                f"Tag {witness!r}: hyperbolic groups have finite asymptotic dimension "
                "(Bell-Dranishnikov theorem 2001). Free groups have asdim = 1 "
                "(Cayley graph is a tree). H^n has asdim = n.",
            ],
            metadata={**base, "criterion": "hyperbolic_finite_asdim", "witness": witness},
        )

    if _matches_any(tags, {"right_angled_artin_group", "coxeter_group",
                            "mapping_class_group", "relatively_hyperbolic"}):
        witness = next(t for t in tags if t in {"right_angled_artin_group",
                                                   "coxeter_group",
                                                   "mapping_class_group",
                                                   "relatively_hyperbolic"})
        return Result.true(
            mode="theorem",
            value="finite_asymptotic_dimension",
            justification=[
                f"Tag {witness!r}: right-angled Artin groups, Coxeter groups, "
                "mapping class groups, and relatively hyperbolic groups all have "
                "finite asymptotic dimension.",
            ],
            metadata={**base, "criterion": "raag_finite_asdim", "witness": witness},
        )

    if _matches_any(tags, NOT_PROPERTY_A_TAGS | {"expander_family", "expander_graph"}):
        blocking = next(t for t in tags if t in (NOT_PROPERTY_A_TAGS |
                                                    {"expander_family", "expander_graph"}))
        return Result.false(
            mode="theorem",
            value="finite_asymptotic_dimension",
            justification=[
                f"Tag {blocking!r}: expander families (as infinite disjoint unions) "
                "do not have finite asymptotic dimension — there is no uniform bound "
                "on the covers as the graphs grow. Each finite component has asdim = 1, "
                "but the union lacks finite uniform control.",
            ],
            metadata={**base, "criterion": "expander_infinite_asdim"},
        )

    return Result.unknown(
        mode="symbolic",
        value="finite_asymptotic_dimension",
        justification=[
            "Insufficient tags to determine finite asymptotic dimension. "
            "Supply tags such as 'virtually_abelian', 'hyperbolic_group', 'free_group', "
            "'asdim_finite', 'z_lattice', 'expander_family', or 'coxeter_group'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_property_a(space: Any) -> Result:
    """Check whether space has Property A (coarse amenability).

    Property A (Yu 2000) is a coarse analogue of amenability for metric spaces:
    X has Property A if for every eps > 0 and R > 0 there exist maps A_x: X -> Fin(X x N)
    such that |A_x delta A_y| / |A_x ∩ A_y| < eps whenever d(x,y) <= R and
    the support of A_x is within radius S (depending on eps, R) of x.
    Key facts:
    - Amenable groups have Property A.
    - All hyperbolic groups have Property A (Yu 2000).
    - Linear groups have Property A (Guentner-Higson-Weinberger 2005).
    - Property A implies coarse embeddability into a Hilbert space.
    - Coarse embeddability implies the coarse Baum-Connes conjecture.
    - Expander families do NOT have Property A (Gromov).
    - The Gromov 'monster' groups (containing expanders as subgraphs) also lack Property A.

    Decision layers
    ---------------
    1. Explicit Property A tag -> true.
    2. Amenable group (amenable => Property A) -> true.
    3. Hyperbolic group (Yu 2000: all hyperbolic groups have Property A) -> true.
    4. Linear group (Guentner-Higson-Weinberger) -> true.
    5. Expander family / Gromov monster -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"property_a", "coarsely_amenable", "exact_group"}):
        witness = next(t for t in tags if t in {"property_a", "coarsely_amenable",
                                                   "exact_group"})
        return Result.true(
            mode="theorem",
            value="property_a",
            justification=[
                f"Tag {witness!r}: the space has Property A — for every R, eps > 0 "
                "there exist finite neighbourhoods A_x satisfying the coarse amenability "
                "condition. Property A implies coarse embeddability into Hilbert space.",
            ],
            metadata={**base, "criterion": "explicit_property_a", "witness": witness},
        )

    if _matches_any(tags, {"amenable_group", "virtually_abelian", "virtually_nilpotent",
                            "finite_group", "abelian_group", "nilpotent_group",
                            "countable_amenable", "amenable_polynomial"}):
        witness = next(t for t in tags if t in {
            "amenable_group", "virtually_abelian", "virtually_nilpotent",
            "finite_group", "abelian_group", "nilpotent_group",
            "countable_amenable", "amenable_polynomial",
        })
        return Result.true(
            mode="theorem",
            value="property_a",
            justification=[
                f"Tag {witness!r}: amenable groups have Property A. "
                "Amenability (Folner condition) implies the coarse Folner condition, "
                "which is equivalent to Property A for countable groups.",
            ],
            metadata={**base, "criterion": "amenable_property_a", "witness": witness},
        )

    if _matches_any(tags, HYPERBOLIC_TAGS):
        witness = next(t for t in tags if t in HYPERBOLIC_TAGS)
        return Result.true(
            mode="theorem",
            value="property_a",
            justification=[
                f"Tag {witness!r}: hyperbolic groups have Property A (Yu 2000). "
                "The delta-hyperbolicity provides enough local-to-global control "
                "to construct the required coarse amenability maps.",
            ],
            metadata={**base, "criterion": "hyperbolic_property_a", "witness": witness},
        )

    if _matches_any(tags, {"linear_group", "right_angled_artin_group",
                            "relatively_hyperbolic"}):
        witness = next(t for t in tags if t in {"linear_group",
                                                   "right_angled_artin_group",
                                                   "relatively_hyperbolic"})
        return Result.true(
            mode="theorem",
            value="property_a",
            justification=[
                f"Tag {witness!r}: linear groups have Property A "
                "(Guentner-Higson-Weinberger 2005). Right-angled Artin groups "
                "and relatively hyperbolic groups also have Property A.",
            ],
            metadata={**base, "criterion": "linear_property_a", "witness": witness},
        )

    if _matches_any(tags, NOT_PROPERTY_A_TAGS):
        blocking = next(t for t in tags if t in NOT_PROPERTY_A_TAGS)
        return Result.false(
            mode="theorem",
            value="property_a",
            justification=[
                f"Tag {blocking!r}: the space does NOT have Property A. "
                "Expander families lack Property A: the spectral gap prevents the "
                "construction of coarse amenability maps. Consequently, expander "
                "families do not coarsely embed into any Hilbert space (Gromov).",
            ],
            metadata={**base, "criterion": "expander_no_property_a", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="property_a",
        justification=[
            "Insufficient tags to determine Property A. "
            "Supply tags such as 'property_a', 'amenable_group', 'hyperbolic_group', "
            "'free_group', 'linear_group', 'expander_family', or 'not_property_a'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_gromov_hyperbolic(space: Any) -> Result:
    """Check whether space is Gromov (delta-)hyperbolic.

    A geodesic metric space X is delta-hyperbolic (Gromov 1987) if every geodesic
    triangle in X is delta-slim: each side lies in the delta-neighbourhood of the
    union of the other two. Key facts:
    - Trees are 0-hyperbolic (every geodesic triangle degenerates to a tripod).
    - H^n is delta-hyperbolic with delta = log(1 + sqrt(2)) (all ideal triangles
      have the same inscribed radius).
    - CAT(-1) spaces are delta-hyperbolic.
    - Free groups (Cayley graph = tree) are 0-hyperbolic.
    - Z^n for n >= 2 is NOT hyperbolic: 'fat' quadrilaterals exist.
    - Gromov's theorem: a finitely generated group is hyperbolic iff all asymptotic
      cones are R-trees (real trees).

    Decision layers
    ---------------
    1. Explicit hyperbolic / delta-hyperbolic / CAT(-1) tag -> true.
    2. Free group (Cayley graph = tree, 0-hyperbolic) -> true.
    3. Hyperbolic space H^n -> true.
    4. Euclidean lattice Z^n (n >= 2) or Heisenberg group -> false.
    5. Expander family -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, HYPERBOLIC_TAGS):
        witness = next(t for t in tags if t in HYPERBOLIC_TAGS)
        return Result.true(
            mode="theorem",
            value="gromov_hyperbolic",
            justification=[
                f"Tag {witness!r}: the space is Gromov hyperbolic. "
                "Every geodesic triangle is delta-slim for some fixed delta >= 0. "
                "Free groups are 0-hyperbolic (Cayley graph = tree); H^n has "
                "delta = log(1 + sqrt(2)); CAT(-1) spaces are hyperbolic.",
            ],
            metadata={**base, "criterion": "hyperbolic_tag", "witness": witness},
        )

    if _matches_any(tags, {"z_lattice_n_geq_2", "euclidean_lattice",
                            "heisenberg_group", "nilpotent_group",
                            "polynomial_growth", "virtually_nilpotent"}):
        blocking = next(t for t in tags if t in {"z_lattice_n_geq_2",
                                                    "euclidean_lattice",
                                                    "heisenberg_group",
                                                    "nilpotent_group",
                                                    "polynomial_growth",
                                                    "virtually_nilpotent"})
        return Result.false(
            mode="theorem",
            value="gromov_hyperbolic",
            justification=[
                f"Tag {blocking!r}: the space is NOT Gromov hyperbolic. "
                "Z^n for n >= 2 contains isometrically embedded Z^2 with flat "
                "quadrilaterals that cannot be made slim. Nilpotent groups have "
                "polynomial growth; hyperbolic groups have exponential growth.",
            ],
            metadata={**base, "criterion": "not_hyperbolic_euclidean"},
        )

    if _matches_any(tags, NOT_PROPERTY_A_TAGS | {"expander_family"}):
        blocking = next(t for t in tags if t in (NOT_PROPERTY_A_TAGS | {"expander_family"}))
        return Result.false(
            mode="theorem",
            value="gromov_hyperbolic",
            justification=[
                f"Tag {blocking!r}: expander families are not Gromov hyperbolic. "
                "Their Cheeger constants are bounded below, but they have no "
                "uniform delta-slimness property across the growing family.",
            ],
            metadata={**base, "criterion": "expander_not_hyperbolic"},
        )

    return Result.unknown(
        mode="symbolic",
        value="gromov_hyperbolic",
        justification=[
            "Insufficient tags to determine Gromov hyperbolicity. "
            "Supply tags such as 'hyperbolic_group', 'free_group', 'delta_hyperbolic', "
            "'cat_negative_curvature', 'euclidean_lattice', or 'polynomial_growth'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_quasi_isometric_to_euclidean(space: Any) -> Result:
    """Check whether space is quasi-isometric to R^n for some n.

    Two metric spaces X and Y are quasi-isometric if there exist (L,C)-quasi-
    isometries f: X -> Y and g: Y -> X (not necessarily inverses). Key facts:
    - Z^n is QI to R^n (inclusion Z^n -> R^n is a quasi-isometry).
    - A finitely generated group G is QI to R^n iff G is virtually Z^n
      (Gromov + Stallings + Wolf).
    - Non-abelian nilpotent groups (Heisenberg) are NOT QI to any R^n:
      asymptotic cones of non-abelian nilpotent groups are Carnot groups,
      not Euclidean.
    - Hyperbolic groups with exponential growth are NOT QI to any R^n.
    - The Milnor-Svarc lemma: if a group G acts geometrically (properly,
      coboundedly, by isometries) on a geodesic space X, then G is QI to X.

    Decision layers
    ---------------
    1. Explicitly euclidean / virtually abelian / Z^n tag -> true.
    2. Free group or hyperbolic group (exponential growth) -> false.
    3. Non-abelian nilpotent / Heisenberg group -> false.
    4. Expander family -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"virtually_abelian", "z_lattice", "euclidean_lattice",
                            "quasi_isometric_to_euclidean", "virtually_z",
                            "integer_group", "infinite_cyclic"}):
        witness = next(t for t in tags if t in {
            "virtually_abelian", "z_lattice", "euclidean_lattice",
            "quasi_isometric_to_euclidean", "virtually_z",
            "integer_group", "infinite_cyclic",
        })
        return Result.true(
            mode="theorem",
            value="qi_euclidean",
            justification=[
                f"Tag {witness!r}: the space is quasi-isometric to R^n. "
                "Virtually abelian groups are QI to Z^n, hence to R^n. "
                "The inclusion Z^n -> R^n is a (1, sqrt(n))-quasi-isometry.",
            ],
            metadata={**base, "criterion": "virtually_abelian_qi_euclidean",
                       "witness": witness},
        )

    if _matches_any(tags, HYPERBOLIC_TAGS | EXPONENTIAL_GROWTH_TAGS):
        blocking = next(t for t in tags if t in (HYPERBOLIC_TAGS | EXPONENTIAL_GROWTH_TAGS))
        return Result.false(
            mode="theorem",
            value="qi_euclidean",
            justification=[
                f"Tag {blocking!r}: hyperbolic and exponential-growth groups are NOT "
                "quasi-isometric to any R^n. Volume growth is a QI invariant: "
                "R^n has polynomial growth of degree n, while hyperbolic groups "
                "and free groups have exponential growth.",
            ],
            metadata={**base, "criterion": "exponential_not_euclidean"},
        )

    if _matches_any(tags, {"heisenberg_group", "nilpotent_group",
                            "non_abelian_nilpotent"}):
        blocking = next(t for t in tags if t in {"heisenberg_group", "nilpotent_group",
                                                    "non_abelian_nilpotent"})
        return Result.false(
            mode="theorem",
            value="qi_euclidean",
            justification=[
                f"Tag {blocking!r}: non-abelian nilpotent groups are NOT QI to R^n. "
                "Their asymptotic cones are Carnot groups with sub-Riemannian geometry. "
                "The Heisenberg group H_3(Z) has growth degree 4 but is not QI to R^4.",
            ],
            metadata={**base, "criterion": "nilpotent_not_euclidean"},
        )

    if _matches_any(tags, NOT_PROPERTY_A_TAGS | {"expander_family"}):
        blocking = next(t for t in tags if t in (NOT_PROPERTY_A_TAGS | {"expander_family"}))
        return Result.false(
            mode="theorem",
            value="qi_euclidean",
            justification=[
                f"Tag {blocking!r}: expander families are not QI to Euclidean space. "
                "They have no coarse embedding into any Hilbert space, let alone "
                "a quasi-isometric equivalence with R^n.",
            ],
            metadata={**base, "criterion": "expander_not_euclidean"},
        )

    return Result.unknown(
        mode="symbolic",
        value="qi_euclidean",
        justification=[
            "Insufficient tags to determine quasi-isometry type. "
            "Supply tags such as 'virtually_abelian', 'z_lattice', 'euclidean_lattice', "
            "'free_group', 'hyperbolic_group', 'heisenberg_group', or 'expander_family'.",
        ],
        metadata={**base, "criterion": None},
    )


def coarsely_embeds_in_hilbert(space: Any) -> Result:
    """Check whether space coarsely embeds into a Hilbert space.

    A metric space X coarsely embeds into a Hilbert space H if there exist
    non-decreasing functions rho_-, rho_+: [0,inf) -> [0,inf) with rho_-(t) -> inf
    as t -> inf and a map f: X -> H with rho_-(d(x,y)) <= ||f(x)-f(y)|| <= rho_+(d(x,y)).
    Key facts:
    - Property A implies coarse embeddability into Hilbert space (Yu 2000).
    - Coarse embeddability implies the coarse Baum-Connes conjecture.
    - Hyperbolic groups coarsely embed into Hilbert space.
    - Expander families do NOT coarsely embed into any Hilbert space (Gromov):
      the spectral gap creates a bottleneck that prevents coarse embedding.
    - Amenable groups coarsely embed into Hilbert space.

    Decision layers
    ---------------
    1. Property A (Property A => coarse embeddability) -> true.
    2. Amenable / hyperbolic / linear group -> true.
    3. Expander family / Gromov monster -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"property_a", "coarsely_amenable",
                            "coarse_embedding_hilbert"}):
        witness = next(t for t in tags if t in {"property_a", "coarsely_amenable",
                                                   "coarse_embedding_hilbert"})
        return Result.true(
            mode="theorem",
            value="coarse_hilbert_embedding",
            justification=[
                f"Tag {witness!r}: Property A implies coarse embeddability into "
                "Hilbert space (Yu 2000). The coarse amenability maps can be used "
                "to construct an explicit coarse embedding.",
            ],
            metadata={**base, "criterion": "property_a_hilbert", "witness": witness},
        )

    if _matches_any(tags, PROPERTY_A_TAGS):
        witness = next(t for t in tags if t in PROPERTY_A_TAGS)
        return Result.true(
            mode="theorem",
            value="coarse_hilbert_embedding",
            justification=[
                f"Tag {witness!r}: amenable groups, hyperbolic groups, and linear "
                "groups all have Property A, hence coarsely embed into Hilbert space. "
                "Amenable groups have the Haagerup property (a uniform version of "
                "coarse embeddability).",
            ],
            metadata={**base, "criterion": "property_a_class_hilbert", "witness": witness},
        )

    if _matches_any(tags, NOT_PROPERTY_A_TAGS):
        blocking = next(t for t in tags if t in NOT_PROPERTY_A_TAGS)
        return Result.false(
            mode="theorem",
            value="coarse_hilbert_embedding",
            justification=[
                f"Tag {blocking!r}: expander families do NOT coarsely embed into "
                "any Hilbert space. The spectral gap creates a bottleneck: the "
                "expansion property forces any coarse map to compress distances, "
                "preventing any control function rho_- with rho_-(t) -> inf.",
            ],
            metadata={**base, "criterion": "expander_no_hilbert"},
        )

    return Result.unknown(
        mode="symbolic",
        value="coarse_hilbert_embedding",
        justification=[
            "Insufficient tags to determine coarse Hilbert embeddability. "
            "Supply tags such as 'property_a', 'amenable_group', 'hyperbolic_group', "
            "'expander_family', or 'no_coarse_embedding_hilbert'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_coarse_geometry(space: Any) -> dict[str, Any]:
    """Classify the coarse geometry of space.

    Keys
    ----
    geometry_class : str
        One of ``"hyperbolic"``, ``"euclidean"``, ``"nilpotent"``,
        ``"expander"``, ``"unknown"``.
    has_finite_asymptotic_dimension : Result
    has_property_a : Result
    is_gromov_hyperbolic : Result
    is_quasi_isometric_to_euclidean : Result
    coarsely_embeds_in_hilbert : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    asdim_r = has_finite_asymptotic_dimension(space)
    prop_a_r = has_property_a(space)
    hyp_r = is_gromov_hyperbolic(space)
    eucl_r = is_quasi_isometric_to_euclidean(space)
    hilb_r = coarsely_embeds_in_hilbert(space)

    if _matches_any(tags, NOT_PROPERTY_A_TAGS | {"expander_family"}):
        geometry_class = "expander"
    elif eucl_r.is_true:
        geometry_class = "euclidean"
    elif hyp_r.is_true:
        geometry_class = "hyperbolic"
    elif _matches_any(tags, {"heisenberg_group", "nilpotent_group",
                               "virtually_nilpotent"}):
        geometry_class = "nilpotent"
    else:
        geometry_class = "unknown"

    key_properties: list[str] = []
    if asdim_r.is_true:
        key_properties.append("finite_asymptotic_dimension")
    if asdim_r.is_false:
        key_properties.append("infinite_asymptotic_dimension")
    if prop_a_r.is_true:
        key_properties.append("property_a")
    if prop_a_r.is_false:
        key_properties.append("no_property_a")
    if hyp_r.is_true:
        key_properties.append("gromov_hyperbolic")
    if eucl_r.is_true:
        key_properties.append("quasi_isometric_euclidean")
    if hilb_r.is_true:
        key_properties.append("coarse_hilbert_embedding")
    if hilb_r.is_false:
        key_properties.append("no_hilbert_embedding")
    if _matches_any(tags, TWO_ENDS_TAGS):
        key_properties.append("two_ends")
    if _matches_any(tags, INFINITE_ENDS_TAGS):
        key_properties.append("infinite_ends")
    if _matches_any(tags, ONE_END_TAGS):
        key_properties.append("one_end")

    return {
        "geometry_class": geometry_class,
        "has_finite_asymptotic_dimension": asdim_r,
        "has_property_a": prop_a_r,
        "is_gromov_hyperbolic": hyp_r,
        "is_quasi_isometric_to_euclidean": eucl_r,
        "coarsely_embeds_in_hilbert": hilb_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def coarse_geometry_profile(space: Any) -> dict[str, Any]:
    """Full coarse geometry profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_coarse_geometry`.
    named_profiles : tuple[CoarseGeometryProfile, ...]
        Registry of canonical coarse geometry examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_coarse_geometry(space),
        "named_profiles": get_named_coarse_geometry_profiles(),
        "layer_summary": coarse_geometry_layer_summary(),
    }


__all__ = [
    "CoarseGeometryProfile",
    "FINITE_ASYMPTOTIC_DIM_TAGS",
    "PROPERTY_A_TAGS",
    "HYPERBOLIC_TAGS",
    "POLYNOMIAL_GROWTH_TAGS",
    "EXPONENTIAL_GROWTH_TAGS",
    "TWO_ENDS_TAGS",
    "INFINITE_ENDS_TAGS",
    "ONE_END_TAGS",
    "NOT_PROPERTY_A_TAGS",
    "get_named_coarse_geometry_profiles",
    "coarse_geometry_layer_summary",
    "coarse_geometry_chapter_index",
    "coarse_geometry_type_index",
    "has_finite_asymptotic_dimension",
    "has_property_a",
    "is_gromov_hyperbolic",
    "is_quasi_isometric_to_euclidean",
    "coarsely_embeds_in_hilbert",
    "classify_coarse_geometry",
    "coarse_geometry_profile",
]
