"""Foliation theory: foliations of manifolds, Frobenius integrability, leaf spaces,
holonomy, taut foliations, and the Godbillon-Vey invariant.

Key theorems and constructions implemented
------------------------------------------
- Foliation (Ehresmann 1950, Reeb 1952): a codimension-q foliation F of a smooth
  n-manifold M is a maximal atlas of charts {(U_i, phi_i)} with phi_i: U_i -> R^n
  such that the transition maps phi_j ∘ phi_i^{-1} have the block form
  (x, y) |-> (f(x,y), g(y)) — they preserve the horizontal slices R^k × {y}
  (here k = n - q = leaf dimension). The leaves are the maximal connected submanifolds
  locally modeled on the R^k slices; they are immersed submanifolds of dimension k.
  Locally M looks like the product R^k × R^q, but globally leaves can be dense,
  non-compact, or have complicated topology.
- Frobenius theorem (Frobenius 1877): a smooth rank-k distribution D ⊂ TM (a smooth
  field of k-dimensional subspaces of the tangent bundle) is integrable (i.e., is the
  tangent distribution of a codimension-(n-k) foliation) if and only if D is involutive:
  for all smooth vector fields X, Y with X_p, Y_p ∈ D_p, the Lie bracket [X,Y]_p ∈ D_p.
  Equivalently (Cartan's formulation): a codimension-q distribution defined locally by
  1-forms omega_1, ..., omega_q is integrable iff d(omega_i) ≡ 0 mod {omega_1,...,omega_q}
  for each i (i.e., d(omega_i) ∧ omega_1 ∧ ... ∧ omega_q = 0).
  The Frobenius theorem reduces integrability (a global geometric condition) to involutivity
  (a pointwise algebraic condition on the Lie bracket).
- Reeb foliation of S^3 (Reeb 1952): the canonical example of a codimension-1 foliation
  of S^3. Construction: write S^3 = D^2 × S^1 ∪_{T^2} S^1 × D^2 (Heegaard splitting).
  On D^2 × S^1 define a foliation with leaves the graphs of f(r,theta) = exp(1/(1-r^2))
  (which all accumulate on the boundary torus T^2 = ∂D^2 × S^1). The boundary torus is
  the unique compact leaf; all other leaves are diffeomorphic to R^2 and spiral toward T^2.
  Novikov's theorem (1965): every codimension-1 C^2 foliation of S^3 has a compact leaf.
  The Reeb foliation shows this is tight: there is exactly one compact leaf (the torus).
- Leaf space (holonomy groupoid): the quotient space M/F = {leaves of F} with the
  quotient topology is in general non-Hausdorff and non-locally-compact (e.g., for the
  Kronecker foliation of T^2 with irrational slope, M/F is indiscrete). The correct
  object is the holonomy groupoid (Winkelnkemper 1983) or the C*-algebra C*(M,F)
  (Connes 1979), which provides a 'noncommutative leaf space' amenable to K-theory.
  Morita equivalence of groupoids captures when two foliations have equivalent transverse
  structures.
- Holonomy (Ehresmann 1950): for a leaf L of F and a loop gamma: [0,1] -> L (gamma(0)
  = gamma(1) = x), the holonomy of gamma is a germ of diffeomorphism of a transversal T_x
  at x. The holonomy group Hol(L, x) = {germs of holonomy diffeomorphisms} is a group of
  germs; it measures how nearby leaves 'return' after following gamma. A leaf has trivial
  holonomy if Hol(L, x) = {id}. All leaves of a Riemannian foliation have trivial
  holonomy (Molino's theorem). A foliation is without holonomy iff the holonomy groupoid
  is equivalent to the fundamental groupoid of the leaf space.
- Taut foliations (Thurston 1986, Gabai 1983): a codimension-1 foliation F of a closed
  3-manifold M is taut if every leaf of F meets a closed transversal (a loop in M
  transverse to F). Equivalently (Sullivan 1976): F is taut iff there exists a closed
  2-form omega on M such that omega|_L is a positive area form on each leaf L.
  Gabai proved that every fibered knot complement admits a taut foliation; taut foliations
  imply the leaves are volume-minimizing in their homology class. Thurston norm: the
  Thurston norm on H_2(M,∂M;Z) measures the minimal complexity of surfaces representing
  a homology class; taut foliations are the leaf-wise minimizers.
- Godbillon-Vey invariant (Godbillon-Vey 1971): for a codimension-1 C^2 foliation F
  defined by a 1-form omega (locally: ker(omega)), the 1-form eta satisfying
  d(omega) = eta ∧ omega is not unique but eta ∧ d(eta) is a closed 3-form independent
  of the choice of eta. Its cohomology class gv(F) = [eta ∧ d(eta)] ∈ H^3(M; R) is the
  Godbillon-Vey invariant, the first and most studied secondary characteristic class.
  For codimension-q foliations: the Godbillon-Vey class lives in H^{2q+1}(M; R) and is
  defined via the Bott connection. Thurston (1972) showed gv can be any real number for
  foliations of S^3; in particular, gv is not determined by the topology of M alone.
  Brooks-Goldman theorem: for foliations of compact 3-manifolds, gv depends only on the
  foliation (not the representing form), confirming it is a genuine foliation invariant.
- Riemannian foliations (Reinhart 1959): a foliation F is Riemannian if there is a
  holonomy-invariant Riemannian metric on the transverse bundle Q = TM/TF. All leaves of
  a Riemannian foliation have trivial holonomy; leaves are locally equidistant (the
  distance between leaves is locally constant). Molino's theorem (1988): the closure of
  leaves of a Riemannian foliation on a compact manifold are the fibers of a fiber bundle,
  and locally the foliation decomposes as a product of a Riemannian foliation and a
  connected Lie group orbit (the 'Molino sheaf'). Riemannian foliations are the
  'tamest' class: their transverse geometry is classical Riemannian geometry.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class FoliationProfile:
    """A curated foliation theory example."""

    key: str
    display_name: str
    foliation_type: str
    codimension: str
    leaf_dimension: str
    has_compact_leaf: bool
    is_taut: bool
    holonomy_type: str
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

FROBENIUS_THEOREM_TAGS: frozenset[str] = frozenset({
    "frobenius_theorem",
    "involutive_distribution",
    "integrable_distribution",
    "frobenius_integrability",
    "cartan_frobenius",
    "lie_bracket_closed",
    "distribution_integrable",
})

COMPACT_LEAF_TAGS: frozenset[str] = frozenset({
    "compact_leaf",
    "closed_leaf",
    "novikov_theorem",
    "compact_torus_leaf",
    "closed_surface_leaf",
    "novikov_compact",
})

REEB_FOLIATION_TAGS: frozenset[str] = frozenset({
    "reeb_foliation",
    "reeb_component",
    "reeb_s3",
    "spiraling_leaves",
    "heegaard_foliation",
    "reeb_torus_leaf",
})

TRANSVERSE_GEOMETRY_TAGS: frozenset[str] = frozenset({
    "transversely_riemannian",
    "riemannian_foliation",
    "transverse_metric",
    "molino_theorem",
    "holonomy_invariant_metric",
    "transversely_flat",
    "transversely_projective",
})

HOLONOMY_TAGS: frozenset[str] = frozenset({
    "holonomy_group",
    "trivial_holonomy",
    "holonomy_representation",
    "holonomy_groupoid",
    "non_trivial_holonomy",
    "holonomy_germ",
    "monodromy_holonomy",
})

TAUT_FOLIATION_TAGS: frozenset[str] = frozenset({
    "taut_foliation",
    "closed_transversal",
    "sullivan_taut",
    "thurston_norm",
    "volume_minimizing_leaf",
    "gabai_taut",
    "homologically_nontrivial_leaf",
})

GODBILLON_VEY_TAGS: frozenset[str] = frozenset({
    "godbillon_vey",
    "secondary_characteristic_class",
    "exotic_class",
    "godbillon_vey_invariant",
    "bott_connection",
    "foliation_cohomology",
    "characteristic_class_foliation",
})

LEAF_SPACE_TAGS: frozenset[str] = frozenset({
    "leaf_space",
    "non_hausdorff_leaf_space",
    "foliation_groupoid",
    "morita_equivalence",
    "connes_c_star",
    "noncommutative_leaf_space",
    "quotient_foliation",
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

def get_named_foliation_profiles() -> tuple[FoliationProfile, ...]:
    """Return the registry of canonical foliation theory examples."""
    return (
        FoliationProfile(
            key="reeb_foliation_s3",
            display_name="Reeb foliation of S^3 — codimension-1 with one compact torus leaf",
            foliation_type="reeb",
            codimension="1",
            leaf_dimension="2",
            has_compact_leaf=True,
            is_taut=False,
            holonomy_type="non_trivial",
            presentation_layer="main_text",
            focus=(
                "The Reeb foliation (Reeb 1952) is the fundamental example of a codimension-1 "
                "foliation of S^3 and the motivating example for Novikov's theorem. "
                "Construction via Heegaard splitting: write S^3 = D^2 × S^1 ∪_{T^2} S^1 × D^2 "
                "(each solid torus glued along their common boundary torus T^2). "
                "On each solid torus D^2 × S^1 with polar coordinates (r, theta) on D^2 "
                "and angle phi on S^1, define leaves as level sets of "
                "F(r, theta, phi) = phi - exp(1/(1 - r^2)). As r -> 1 (approaching ∂D^2 = S^1), "
                "the leaves spiral faster and faster toward the boundary torus T^2. "
                "Leaves: T^2 = ∂D^2 × S^1 is the unique compact leaf (diffeomorphic to T^2). "
                "All other leaves are diffeomorphic to R^2 (planes), and they are non-compact; "
                "they accumulate on T^2 as one approaches the boundary. "
                "Novikov's theorem (1965): every codimension-1 C^2 foliation of S^3 has a "
                "compact leaf. The Reeb foliation is the canonical example; Novikov's proof "
                "shows that any such foliation must contain a leaf diffeomorphic to T^2. "
                "Not taut: the Reeb foliation is NOT taut. The compact torus leaf T^2 bounds "
                "a solid torus (it is null-homologous on one side), so no closed transversal can "
                "penetrate the Reeb component and exit through the torus leaf. "
                "Holonomy: the holonomy of the compact torus leaf T^2 is non-trivial — "
                "paths in T^2 have holonomy given by diffeomorphisms of an interval that fix "
                "the boundary and contract the interior (the spiraling Reeb component). "
                "Generalization: a Reeb component is any solid torus foliated like the Reeb "
                "foliation of D^2 × S^1. A foliation of a 3-manifold is called Reeb-free "
                "(or taut) if it contains no Reeb components."
            ),
            chapter_targets=("14", "24", "37"),
        ),
        FoliationProfile(
            key="frobenius_integrable",
            display_name="Frobenius integrability — involutive distribution defines a foliation",
            foliation_type="frobenius",
            codimension="q",
            leaf_dimension="k",
            has_compact_leaf=False,
            is_taut=False,
            holonomy_type="variable",
            presentation_layer="main_text",
            focus=(
                "The Frobenius theorem is the bridge between the pointwise algebraic data "
                "(a distribution D ⊂ TM) and the global geometric data (a foliation F of M). "
                "Setup: let M be a smooth n-manifold and D ⊂ TM a smooth rank-k distribution "
                "(a smooth assignment p |-> D_p ⊂ T_pM with dim D_p = k). "
                "Frobenius theorem: D is integrable (i.e., is the tangent distribution TF of "
                "some codimension-q = n-k foliation F) if and only if D is involutive: "
                "[X, Y] ∈ Gamma(D) for all X, Y ∈ Gamma(D). "
                "Cartan's formulation: if D = ker(omega_1) ∩ ... ∩ ker(omega_q) locally, "
                "then D is integrable iff d(omega_i) ∧ omega_1 ∧ ... ∧ omega_q = 0 for all i "
                "(the exterior differential form version). "
                "Example: the 1-form omega = dz - y dx on R^3. Then "
                "d(omega) = -dy ∧ dx and d(omega) ∧ omega = -dy ∧ dx ∧ (dz - y dx) = "
                "-dy ∧ dx ∧ dz ≠ 0, so D = ker(omega) is NOT integrable — no foliation. "
                "(D is the standard contact structure on R^3.) "
                "Example: omega = dz - f(x,y)dx for any f. Then d(omega) = -df/dy dy ∧ dx, "
                "and d(omega) ∧ omega = 0 iff the distribution is integrable — checked easily. "
                "Local model: locally, every integrable distribution looks like the horizontal "
                "distribution of R^k × R^q (the slices R^k × {y} for fixed y ∈ R^q). "
                "This is the content of the rectification theorem (local triviality of foliations). "
                "Non-integrable: contact distributions (dim D = n-1, the contact condition is "
                "maximally non-integrable: omega ∧ (d omega)^{n/2} ≠ 0 everywhere)."
            ),
            chapter_targets=("14", "24", "37"),
        ),
        FoliationProfile(
            key="kronecker_foliation_torus",
            display_name="Kronecker foliation of T^2 — irrational slope, all leaves dense",
            foliation_type="linear",
            codimension="1",
            leaf_dimension="1",
            has_compact_leaf=False,
            is_taut=True,
            holonomy_type="trivial",
            presentation_layer="main_text",
            focus=(
                "The Kronecker foliation (also called the linear foliation of the torus) is "
                "the simplest example of a foliation with non-Hausdorff leaf space. "
                "Construction: on T^2 = R^2/Z^2, define the foliation F_alpha by the vector "
                "field X = ∂/∂x + alpha · ∂/∂y for a fixed alpha ∈ R. The leaves are "
                "lines of slope alpha: L_{(x_0,y_0)} = {(x_0 + t, y_0 + alpha·t) mod Z^2 : t ∈ R}. "
                "Rational slope (alpha = p/q in lowest terms): every leaf is a closed curve "
                "(diffeomorphic to S^1), winding p times in x and q times in y. The foliation "
                "is a fiber bundle T^2 -> S^1 with fiber S^1. All leaves are compact. "
                "Irrational slope (alpha ∉ Q): every leaf is a dense immersed line in T^2 "
                "(diffeomorphic to R). No compact leaf exists. The foliation F_alpha is "
                "topologically equivalent to F_{alpha'} for any other irrational alpha'. "
                "Leaf space: for irrational alpha, the quotient T^2/F_alpha with the quotient "
                "topology is indiscrete (every open set is T^2 or empty). This is the "
                "prototypical example of a non-Hausdorff, non-locally-compact leaf space. "
                "Connes's noncommutative geometry: the foliation groupoid for irrational alpha "
                "is Morita equivalent to the irrational rotation C*-algebra A_alpha = "
                "C*(Z, C(S^1), alpha-rotation). A_alpha is a simple, purely infinite (for "
                "alpha irrational) C*-algebra with K_0(A_alpha) = Z + alpha·Z ⊂ R. "
                "Taut: the irrational Kronecker foliation IS taut — any transverse circle "
                "(a circle in T^2 transverse to F_alpha, e.g., {0} × S^1) is a closed "
                "transversal meeting every leaf. "
                "Holonomy: trivial — all leaves are simply connected covers of their image "
                "in T^2/F_alpha and have trivial holonomy."
            ),
            chapter_targets=("14", "24", "37"),
        ),
        FoliationProfile(
            key="taut_foliation_3manifold",
            display_name="Taut foliation of a 3-manifold — Sullivan-Thurston-Gabai theory",
            foliation_type="taut",
            codimension="1",
            leaf_dimension="2",
            has_compact_leaf=False,
            is_taut=True,
            holonomy_type="trivial",
            presentation_layer="main_text",
            focus=(
                "Taut foliations are codimension-1 foliations F of closed 3-manifolds M "
                "in which every leaf meets a closed transversal — a circle in M that is "
                "everywhere transverse to the leaves of F. "
                "Sullivan's characterization (1976): F is taut iff there exists a closed "
                "2-form omega on M with omega|_L > 0 (a positive area form) on every leaf L. "
                "Equivalently: F is taut iff it carries a transverse invariant measure with "
                "full support (Thurston 1986). "
                "Thurston norm: for a compact oriented 3-manifold M, the Thurston norm "
                "||·||_T on H_2(M, ∂M; Z) measures the minimal complexity chi_-(S) = "
                "sum_{components S_i} max(0, -chi(S_i)) over all embedded surfaces S "
                "representing a given homology class. Taut foliations give norm-minimizing "
                "surfaces: a leaf L of a taut foliation represents a class in H_2(M; Z) "
                "that is a Thurston-norm minimizer. "
                "Gabai's theorem (1983): if K ⊂ S^3 is a fibered knot (the knot complement "
                "S^3 \\ K is a fiber bundle over S^1 with fiber a Seifert surface), then "
                "S^3 \\ K admits a taut foliation. More generally, any irreducible 3-manifold "
                "with a non-trivial Thurston-norm class admits a taut foliation (Gabai 1983-87). "
                "Reeb-free foliations: a taut foliation is Reeb-free (contains no Reeb "
                "components). Conversely, a Reeb-free foliation of a closed 3-manifold with "
                "no torus boundary components is taut (Thurston's theorem). "
                "Holonomy-free: many taut foliations have trivial holonomy (all leaves have "
                "trivial holonomy), making them amenable to smoothing theorems. "
                "L-space conjecture (Boyer-Gordon-Watson, Ozsváth-Szabó): a closed, irreducible, "
                "rational homology 3-sphere is an L-space iff it admits no taut foliation iff "
                "its fundamental group is not left-orderable. Partially proven by Hanselman- "
                "Rasmussen-Watson (2024) for graph manifolds."
            ),
            chapter_targets=("14", "24"),
        ),
        FoliationProfile(
            key="riemannian_foliation",
            display_name="Riemannian foliation — holonomy-invariant transverse metric",
            foliation_type="riemannian",
            codimension="q",
            leaf_dimension="k",
            has_compact_leaf=False,
            is_taut=False,
            holonomy_type="trivial",
            presentation_layer="selected_block",
            focus=(
                "A Riemannian foliation (Reinhart 1959) is a foliation F of codimension q "
                "on a Riemannian manifold (M, g) such that the transverse metric g_Q on "
                "Q = TM/TF (the normal bundle) is holonomy-invariant: for any path gamma "
                "in a leaf L, the holonomy map gamma_*: T_{gamma(0)}^⊥ -> T_{gamma(1)}^⊥ "
                "is an isometry of the transverse metric. "
                "Equivalently: F is Riemannian iff the leaves are locally equidistant "
                "(the distance between two leaves is locally constant along each leaf). "
                "All fibers of a Riemannian submersion f: M -> B are the leaves of a "
                "Riemannian foliation (the canonical example). "
                "Molino's theorem (1988): for a Riemannian foliation F of a compact manifold M, "
                "the closure of each leaf cl(L) is a submanifold of M, and the closed leaves "
                "form a (singular) Riemannian foliation F_bar (the 'Molino foliation'). "
                "The leaf closures are the orbits of a locally constant sheaf of Lie algebras "
                "(the 'structural Lie algebra' g_0 of F). "
                "Trivial holonomy: every leaf of a Riemannian foliation has trivial holonomy. "
                "This follows from the holonomy-invariance of the transverse metric and the "
                "compactness of the holonomy group. "
                "Transversely flat foliations: F is transversely flat if g_Q is flat (zero "
                "transverse curvature). Transversely projective: if the holonomy factors "
                "through PGL(q+1, R). These are further specializations of Riemannian foliations. "
                "Haefliger structure: any foliation F is classified by a map M -> BΓ_q "
                "(the classifying space of the Haefliger groupoid Γ_q of germs of local "
                "diffeomorphisms of R^q). For Riemannian foliations, the classifying map "
                "factors through BO(q) ⊂ BΓ_q."
            ),
            chapter_targets=("14", "24", "37"),
        ),
        FoliationProfile(
            key="godbillon_vey_example",
            display_name="Godbillon-Vey invariant — secondary characteristic class gv(F) ∈ H^3(M; R)",
            foliation_type="codim1_with_gv",
            codimension="1",
            leaf_dimension="2",
            has_compact_leaf=False,
            is_taut=False,
            holonomy_type="non_trivial",
            presentation_layer="selected_block",
            focus=(
                "The Godbillon-Vey invariant gv(F) ∈ H^3(M; R) is the primary secondary "
                "characteristic class of codimension-1 foliations, discovered by Godbillon-Vey (1971). "
                "Construction: let F be a codimension-1 C^2 foliation of M^{n+1}, defined locally "
                "by a nowhere-zero 1-form omega (ker(omega) = TF). Since d(omega) is a 2-form "
                "and omega is a 1-form, d(omega) ∧ omega = 0 (because d(omega) ∧ omega is a "
                "3-form and ker(omega) has codimension 1, so locally d(omega) = eta ∧ omega for "
                "some 1-form eta). The Frobenius condition is automatically satisfied: F is always "
                "integrable (we start with a foliation). "
                "The 3-form eta ∧ d(eta): although eta is not uniquely determined (eta' = eta + f·omega "
                "is another choice), one computes: "
                "eta' ∧ d(eta') = (eta + f·omega) ∧ d(eta + f·omega) = eta ∧ d(eta) + [terms vanishing mod omega]. "
                "Thus eta ∧ d(eta) is well-defined mod exact forms, and [eta ∧ d(eta)] ∈ H^3(M; R) "
                "is the Godbillon-Vey class gv(F). "
                "Thurston's example (1972): for any real number c ∈ R, there exists a codimension-1 "
                "C^infty foliation F_c of S^3 with gv(F_c) = c. This shows gv is not a topological "
                "invariant of M (since all F_c live on the same manifold S^3 but have different gv). "
                "Brooks-Goldman theorem: gv(F) depends only on F (not on the choice of omega or eta), "
                "confirming it is a genuine foliation invariant. "
                "Geometric interpretation: gv(F) measures the 'helical wobble' of the foliation — "
                "the rate at which the transverse curvature of the leaves varies along the foliation. "
                "For the Reeb foliation of S^3: gv = 0 (the Reeb foliation has zero Godbillon-Vey "
                "invariant, despite being non-trivial topologically). "
                "Generalization to codimension q: the Godbillon-Vey class lives in H^{2q+1}(M; R) "
                "and is constructed via the Bott connection — an sl(q,R)-valued connection form on "
                "the normal bundle of F. The full set of secondary characteristic classes of F "
                "constitutes the Gel'fand-Fuks cohomology of the Lie algebra of formal vector fields."
            ),
            chapter_targets=("14", "24"),
        ),
        FoliationProfile(
            key="haefliger_classifying_space",
            display_name="BΓ_q — Haefliger classifying space for codimension-q foliations",
            foliation_type="classifying",
            codimension="q",
            leaf_dimension="n-q",
            has_compact_leaf=False,
            is_taut=False,
            holonomy_type="variable",
            presentation_layer="selected_block",
            focus=(
                "The Haefliger classifying space BΓ_q (Haefliger 1970) classifies codimension-q "
                "foliations on smooth manifolds via homotopy classes of maps into BΓ_q. "
                "Haefliger groupoid Γ_q: the groupoid of germs of local diffeomorphisms of R^q. "
                "An object of Γ_q is a point x ∈ R^q; a morphism from x to y is a germ of a "
                "diffeomorphism phi: U -> V (U, V neighborhoods of x, y) with phi(x) = y. "
                "Composition is composition of germs. "
                "Classifying space BΓ_q: the classifying space of the groupoid Γ_q (constructed "
                "by Milnor's join construction or Segal's nerve construction). Its homotopy type "
                "is the key invariant: pi_1(BΓ_1) classifies codimension-1 foliations, and "
                "H^*(BΓ_q; R) = Gel'fand-Fuks cohomology of the Lie algebra of formal vector "
                "fields on R^q (Haefliger 1971, Bott-Segal 1977). "
                "Classification theorem (Haefliger 1971): for a compact manifold M of dim n >= 3, "
                "every element of [M, BΓ_q] is represented by a codimension-q foliation of M × R "
                "(one dimension higher). For dim(M) > 2q, every homotopy class in [M, BΓ_q] is "
                "represented by an actual foliation of M (no extra dimension needed). "
                "Bott vanishing: the Pontryagin classes p_i(Q) of the normal bundle Q of F "
                "vanish for i > q (Bott 1972). This gives topological obstructions to a "
                "rank-k subbundle of TM being integrable. "
                "Secondary characteristic classes: the map M -> BΓ_q pulls back classes from "
                "H^*(BΓ_q; R) to H^*(M; R). The non-trivial classes (in degrees > 2q, above "
                "the Bott vanishing range) are the secondary characteristic classes — they "
                "include the Godbillon-Vey class and its generalizations (the Bernstein-Rosenfeld "
                "classes, the Godbillon-Vey classes in all codimensions). "
                "Thurston's theorem (1974): BΓ_q is 'wild' — H^k(BΓ_q; R) ≠ 0 for all k <= 2q+1 "
                "and the higher homology is enormous (detected by Thurston's example of foliations "
                "with arbitrary Godbillon-Vey)."
            ),
            chapter_targets=("24", "37"),
        ),
    )


def foliation_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_foliation_profiles()
    ))


def foliation_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_foliation_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def foliation_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from foliation_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_foliation_profiles():
        index.setdefault(p.foliation_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_frobenius_integrable(space: Any) -> Result:
    """Check whether a distribution satisfies the Frobenius integrability condition.

    The Frobenius theorem (1877): a distribution D ⊂ TM is integrable (i.e., is the
    tangent distribution of a foliation) iff it is involutive: [X,Y] ∈ D for all
    X, Y ∈ Gamma(D). In Cartan's formulation, the defining forms omega_i satisfy
    d(omega_i) ∧ omega_1 ∧ ... ∧ omega_q = 0 for each i.

    Decision layers
    ---------------
    1. Explicit 'frobenius_theorem' or 'integrable_distribution' tag -> true.
    2. Known integrable structures (foliation, taut, Riemannian foliation) -> true.
    3. Non-integrable (contact distribution) tags -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, FROBENIUS_THEOREM_TAGS):
        witness = next(t for t in tags if t in FROBENIUS_THEOREM_TAGS)
        return Result.true(
            mode="theorem",
            value="frobenius_integrable",
            justification=[
                f"Tag {witness!r}: the distribution satisfies the Frobenius integrability "
                "condition — it is involutive ([X,Y] ∈ D for all X,Y ∈ D), hence integrable: "
                "it is the tangent distribution of a smooth foliation.",
            ],
            metadata={**base, "criterion": "explicit_frobenius", "witness": witness},
        )

    integrable_structures = {
        "foliation", "taut_foliation", "reeb_foliation", "riemannian_foliation",
        "linear_foliation", "codim1_foliation", "fibration_foliation",
        "godbillon_vey", "kronecker_foliation",
    }
    if _matches_any(tags, integrable_structures):
        witness = next(t for t in tags if t in integrable_structures)
        return Result.true(
            mode="theorem",
            value="frobenius_integrable",
            justification=[
                f"Tag {witness!r}: the structure is a foliation — by definition its tangent "
                "distribution TF is involutive and integrable (Frobenius condition satisfied).",
            ],
            metadata={**base, "criterion": "foliation_implies_integrable", "witness": witness},
        )

    non_integrable = {
        "contact_distribution", "contact_structure", "non_integrable",
        "maximally_non_integrable", "sub_riemannian",
    }
    if _matches_any(tags, non_integrable):
        blocking = next(t for t in tags if t in non_integrable)
        return Result.false(
            mode="theorem",
            value="frobenius_integrable",
            justification=[
                f"Tag {blocking!r}: the distribution is NOT Frobenius-integrable. "
                "Contact distributions are maximally non-integrable: omega ∧ (d omega)^n ≠ 0 "
                "everywhere, which directly violates the Frobenius integrability condition "
                "d(omega) ∧ omega = 0.",
            ],
            metadata={**base, "criterion": "not_integrable"},
        )

    return Result.unknown(
        mode="symbolic",
        value="frobenius_integrable",
        justification=[
            "Insufficient tags to determine Frobenius integrability. "
            "Supply tags such as 'frobenius_theorem', 'integrable_distribution', "
            "'involutive_distribution', 'foliation', or 'contact_structure'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_compact_leaf(space: Any) -> Result:
    """Check whether the foliation has at least one compact leaf.

    Novikov's theorem (1965): every codimension-1 C^2 foliation of S^3 has a compact
    leaf (diffeomorphic to T^2). For general 3-manifolds this is false. Compact leaves
    exist in Reeb foliations (the boundary torus) and in foliations of fiber bundles
    (all fibers are compact). For irrational Kronecker foliations of T^2, no compact
    leaf exists.

    Decision layers
    ---------------
    1. Explicit 'compact_leaf' or 'closed_leaf' tag -> true.
    2. Reeb foliation or Novikov tags -> true.
    3. Kronecker (irrational) or dense-leaf tags -> false.
    4. Taut foliation (often no compact leaf in 3-manifold context) -> unknown.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, COMPACT_LEAF_TAGS):
        witness = next(t for t in tags if t in COMPACT_LEAF_TAGS)
        return Result.true(
            mode="theorem",
            value="compact_leaf",
            justification=[
                f"Tag {witness!r}: the foliation has a compact leaf. "
                "Compact leaves are closed submanifolds of M; their holonomy is a "
                "finitely generated group of germs of diffeomorphisms.",
            ],
            metadata={**base, "criterion": "explicit_compact_leaf", "witness": witness},
        )

    if _matches_any(tags, REEB_FOLIATION_TAGS):
        witness = next(t for t in tags if t in REEB_FOLIATION_TAGS)
        return Result.true(
            mode="theorem",
            value="compact_leaf",
            justification=[
                f"Tag {witness!r}: Reeb foliation has exactly one compact leaf — the boundary "
                "torus T^2 = ∂D^2 × S^1. All other leaves are non-compact R^2-planes that "
                "spiral toward T^2. Novikov's theorem guarantees this for any codim-1 foliation of S^3.",
            ],
            metadata={**base, "criterion": "reeb_compact_torus", "witness": witness},
        )

    no_compact = {
        "no_compact_leaf", "all_leaves_dense", "irrational_kronecker",
        "all_leaves_noncompact", "dense_leaves",
    }
    if _matches_any(tags, no_compact):
        blocking = next(t for t in tags if t in no_compact)
        return Result.false(
            mode="theorem",
            value="compact_leaf",
            justification=[
                f"Tag {blocking!r}: the foliation has no compact leaf. "
                "The Kronecker foliation with irrational slope on T^2 has all leaves "
                "diffeomorphic to R and dense in T^2 — no closed (compact) leaf exists.",
            ],
            metadata={**base, "criterion": "no_compact_leaf"},
        )

    return Result.unknown(
        mode="symbolic",
        value="compact_leaf",
        justification=[
            "Insufficient tags to determine compact leaf existence. "
            "Supply tags such as 'compact_leaf', 'reeb_foliation', 'novikov_theorem', "
            "'no_compact_leaf', 'irrational_kronecker', or 'all_leaves_dense'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_taut_foliation(space: Any) -> Result:
    """Check whether the foliation is taut.

    A codimension-1 foliation F is taut if every leaf meets a closed transversal.
    Equivalently (Sullivan 1976): F is taut iff there exists a closed 2-form omega
    with omega|_L > 0 on every leaf L. Taut foliations are Reeb-free.

    Decision layers
    ---------------
    1. Explicit 'taut_foliation' or 'sullivan_taut' tag -> true.
    2. Gabai/fibered knot tags -> true.
    3. Reeb foliation or Reeb component tags -> false (Reeb foliations are not taut).
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, TAUT_FOLIATION_TAGS):
        witness = next(t for t in tags if t in TAUT_FOLIATION_TAGS)
        return Result.true(
            mode="theorem",
            value="taut_foliation",
            justification=[
                f"Tag {witness!r}: the foliation is taut — every leaf meets a closed transversal. "
                "Equivalently (Sullivan 1976), there exists a closed 2-form omega restricting to "
                "a positive area form on each leaf. Taut foliations are Reeb-free.",
            ],
            metadata={**base, "criterion": "explicit_taut", "witness": witness},
        )

    if _matches_any(tags, {"kronecker_foliation", "linear_foliation", "irrational_slope"}):
        witness = next(t for t in tags if t in {
            "kronecker_foliation", "linear_foliation", "irrational_slope"
        })
        return Result.true(
            mode="theorem",
            value="taut_foliation",
            justification=[
                f"Tag {witness!r}: the Kronecker (linear) foliation on T^2 is taut — "
                "any transverse circle {*} × S^1 is a closed transversal meeting every leaf.",
            ],
            metadata={**base, "criterion": "kronecker_taut", "witness": witness},
        )

    not_taut = {
        "reeb_foliation", "reeb_component", "not_taut",
        "reeb_s3", "spiraling_leaves",
    }
    if _matches_any(tags, not_taut):
        blocking = next(t for t in tags if t in not_taut)
        return Result.false(
            mode="theorem",
            value="taut_foliation",
            justification=[
                f"Tag {blocking!r}: the foliation is NOT taut. Reeb foliations contain a Reeb "
                "component (solid torus foliated with the compact torus leaf on the boundary) — "
                "no closed transversal can penetrate a Reeb component and return through the "
                "torus leaf. Reeb foliations are never taut.",
            ],
            metadata={**base, "criterion": "reeb_not_taut"},
        )

    return Result.unknown(
        mode="symbolic",
        value="taut_foliation",
        justification=[
            "Insufficient tags to determine tautness. "
            "Supply tags such as 'taut_foliation', 'sullivan_taut', 'closed_transversal', "
            "'reeb_foliation', 'gabai_taut', or 'not_taut'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_trivial_holonomy(space: Any) -> Result:
    """Check whether all leaves have trivial holonomy.

    A leaf L has trivial holonomy if every loop gamma in L has trivial holonomy germ
    (the local return map near L is the identity). Riemannian foliations have all
    trivial holonomy (Molino). Taut foliations often have trivial holonomy. Reeb
    foliations have non-trivial holonomy on the compact torus leaf.

    Decision layers
    ---------------
    1. Explicit 'trivial_holonomy' tag -> true.
    2. Riemannian foliation tags -> true (Molino's theorem).
    3. Kronecker/linear foliation -> true.
    4. Non-trivial holonomy or Reeb foliation -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if "trivial_holonomy" in tags:
        return Result.true(
            mode="theorem",
            value="trivial_holonomy",
            justification=[
                "Tag 'trivial_holonomy': all leaves have trivial holonomy — every loop in "
                "any leaf has identity holonomy germ. The foliation behaves locally like "
                "a product near every point.",
            ],
            metadata={**base, "criterion": "explicit_trivial_holonomy", "witness": "trivial_holonomy"},
        )

    if _matches_any(tags, TRANSVERSE_GEOMETRY_TAGS):
        witness = next(t for t in tags if t in TRANSVERSE_GEOMETRY_TAGS)
        return Result.true(
            mode="theorem",
            value="trivial_holonomy",
            justification=[
                f"Tag {witness!r}: Riemannian foliations have trivial holonomy on all leaves "
                "(Molino's theorem — the holonomy-invariant transverse metric forces the "
                "holonomy group to be compact, and for the metric to be smooth it must be "
                "trivial).",
            ],
            metadata={**base, "criterion": "riemannian_trivial_holonomy", "witness": witness},
        )

    if _matches_any(tags, {"kronecker_foliation", "linear_foliation",
                           "irrational_kronecker", "irrational_slope"}):
        witness = next(t for t in tags if t in {
            "kronecker_foliation", "linear_foliation",
            "irrational_kronecker", "irrational_slope",
        })
        return Result.true(
            mode="theorem",
            value="trivial_holonomy",
            justification=[
                f"Tag {witness!r}: the Kronecker foliation has trivial holonomy — leaves are "
                "simply connected (R or S^1), and the foliation is a group quotient, so all "
                "holonomy representations are trivial.",
            ],
            metadata={**base, "criterion": "kronecker_trivial_holonomy", "witness": witness},
        )

    if _matches_any(tags, {"non_trivial_holonomy", "holonomy_germ"} | REEB_FOLIATION_TAGS):
        blocking = next(t for t in tags if t in {
            "non_trivial_holonomy", "holonomy_germ"
        } | REEB_FOLIATION_TAGS)
        return Result.false(
            mode="theorem",
            value="trivial_holonomy",
            justification=[
                f"Tag {blocking!r}: the foliation has non-trivial holonomy. "
                "The compact torus leaf of the Reeb foliation has non-trivial holonomy: "
                "loops in T^2 have holonomy germs contracting an interval toward the fixed "
                "point (the leaf itself), so the holonomy group is non-trivial.",
            ],
            metadata={**base, "criterion": "non_trivial_holonomy"},
        )

    return Result.unknown(
        mode="symbolic",
        value="trivial_holonomy",
        justification=[
            "Insufficient tags to determine holonomy triviality. "
            "Supply tags such as 'trivial_holonomy', 'riemannian_foliation', "
            "'molino_theorem', 'non_trivial_holonomy', 'reeb_foliation', or "
            "'kronecker_foliation'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_foliation(space: Any) -> dict[str, Any]:
    """Classify the foliation type based on its structural properties.

    Keys
    ----
    foliation_class : str
        One of ``"taut_trivial_holonomy"``, ``"riemannian"``, ``"reeb_type"``,
        ``"compact_leaf_nontrivial"``, ``"general_foliation"``, ``"unknown"``.
    is_frobenius_integrable : Result
    has_compact_leaf : Result
    is_taut_foliation : Result
    has_trivial_holonomy : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    frobenius_r = is_frobenius_integrable(space)
    compact_r = has_compact_leaf(space)
    taut_r = is_taut_foliation(space)
    holonomy_r = has_trivial_holonomy(space)

    if taut_r.is_true and holonomy_r.is_true:
        foliation_class = "taut_trivial_holonomy"
    elif _matches_any(tags, TRANSVERSE_GEOMETRY_TAGS):
        foliation_class = "riemannian"
    elif _matches_any(tags, REEB_FOLIATION_TAGS):
        foliation_class = "reeb_type"
    elif compact_r.is_true and holonomy_r.is_false:
        foliation_class = "compact_leaf_nontrivial"
    elif frobenius_r.is_true:
        foliation_class = "general_foliation"
    else:
        foliation_class = "unknown"

    key_properties: list[str] = []
    if frobenius_r.is_true:
        key_properties.append("frobenius_integrable")
    if compact_r.is_true:
        key_properties.append("compact_leaf")
    if compact_r.is_false:
        key_properties.append("no_compact_leaf")
    if taut_r.is_true:
        key_properties.append("taut")
    if taut_r.is_false:
        key_properties.append("not_taut")
    if holonomy_r.is_true:
        key_properties.append("trivial_holonomy")
    if holonomy_r.is_false:
        key_properties.append("non_trivial_holonomy")
    if _matches_any(tags, TRANSVERSE_GEOMETRY_TAGS):
        key_properties.append("riemannian_foliation")
    if _matches_any(tags, GODBILLON_VEY_TAGS):
        key_properties.append("godbillon_vey")
    if _matches_any(tags, LEAF_SPACE_TAGS):
        key_properties.append("leaf_space_structure")
    if _matches_any(tags, REEB_FOLIATION_TAGS):
        key_properties.append("reeb_component")

    return {
        "foliation_class": foliation_class,
        "is_frobenius_integrable": frobenius_r,
        "has_compact_leaf": compact_r,
        "is_taut_foliation": taut_r,
        "has_trivial_holonomy": holonomy_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def foliation_profile(space: Any) -> dict[str, Any]:
    """Full foliation profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_foliation`.
    named_profiles : tuple[FoliationProfile, ...]
        Registry of canonical foliation theory examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_foliation(space),
        "named_profiles": get_named_foliation_profiles(),
        "layer_summary": foliation_layer_summary(),
    }


__all__ = [
    "FoliationProfile",
    "FROBENIUS_THEOREM_TAGS",
    "COMPACT_LEAF_TAGS",
    "REEB_FOLIATION_TAGS",
    "TRANSVERSE_GEOMETRY_TAGS",
    "HOLONOMY_TAGS",
    "TAUT_FOLIATION_TAGS",
    "GODBILLON_VEY_TAGS",
    "LEAF_SPACE_TAGS",
    "get_named_foliation_profiles",
    "foliation_layer_summary",
    "foliation_chapter_index",
    "foliation_type_index",
    "is_frobenius_integrable",
    "has_compact_leaf",
    "is_taut_foliation",
    "has_trivial_holonomy",
    "classify_foliation",
    "foliation_profile",
]
