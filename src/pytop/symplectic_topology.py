"""Symplectic topology: symplectic manifolds, Darboux theorem, Hamiltonian dynamics,
Lagrangian submanifolds, symplectomorphisms, Moser stability, Gromov non-squeezing.

Key theorems and constructions implemented
------------------------------------------
- Symplectic manifold (M, omega): a smooth even-dimensional manifold M^{2n} equipped
  with a closed (d omega = 0) and non-degenerate 2-form omega. Non-degeneracy means
  omega^n = omega ^ ... ^ omega (n-fold wedge) is a volume form (never zero). The pair
  (M, omega) is a symplectic manifold; omega is the symplectic form.
  Examples: (R^{2n}, omega_0) with omega_0 = sum_{i=1}^n dx_i ^ dp_i; cotangent bundle
  T*M with canonical form; Kahler manifolds; coadjoint orbits of Lie groups.
  Note: symplectic manifolds must be even-dimensional (omega^n != 0 requires 2n) and
  orientable. Compact symplectic manifolds without boundary: [omega]^n != 0 in H^{2n}(M).
- Darboux theorem (Darboux 1882): every point of a symplectic manifold (M^{2n}, omega)
  has a coordinate neighborhood (U; x_1,...,x_n, p_1,...,p_n) in which
  omega|_U = sum_{i=1}^n dx_i ^ dp_i.
  Consequence: there are no local invariants of symplectic structure — all symplectic
  manifolds of the same dimension are locally identical. This is in sharp contrast with
  Riemannian geometry, where curvature is a local invariant.
  Proof sketch (Moser's argument): use the isotopy method. Given two symplectic forms
  omega_0, omega_1 with [omega_0] = [omega_1], write omega_t = (1-t)omega_0 + t*omega_1.
  Solve the ODE d/dt(phi_t* omega_t) = 0 for a family of diffeomorphisms phi_t; this
  requires inverting omega_t to find a vector field X_t, which is possible because omega_t
  is non-degenerate for all t (both forms define the same cohomology class near a point).
- Hamiltonian vector fields and Hamiltonian dynamics: given (M, omega) and a smooth
  function H: M -> R (the Hamiltonian), the Hamiltonian vector field X_H is uniquely
  defined by i_{X_H} omega = -dH (or equivalently omega(X_H, .) = -dH(.)). The flow
  phi_t of X_H consists of symplectomorphisms (phi_t* omega = omega). The Poisson bracket
  {f, g} = omega(X_f, X_g) = X_g(f) = -X_f(g) makes C^inf(M) a Poisson algebra.
  Noether's theorem: if H is invariant under a Lie group action with moment map mu, then
  the components of mu are conserved quantities along the Hamiltonian flow.
  Liouville's theorem: the volume form omega^n is preserved by Hamiltonian flow, i.e.,
  phi_t* (omega^n) = omega^n. This is the symplectic version of Liouville's theorem.
- Lagrangian submanifolds: a submanifold L^n of (M^{2n}, omega) is Lagrangian if
  omega|_L = 0 and dim L = n (half the dimension of M). Equivalently, TL = (TL)^perp
  with respect to omega. Every cotangent fiber T*_x M is Lagrangian in T*M (the zero
  section is also Lagrangian). The graph of a diffeomorphism f: M -> M is Lagrangian in
  (M x M, omega_1 - omega_2) iff f is a symplectomorphism. Arnold's Maslov index and
  the Lagrangian Grassmannian are key tools in Floer theory and quantum mechanics.
  Weinstein's Lagrangian neighborhood theorem: every Lagrangian L in (M, omega) has a
  neighborhood symplectomorphic to a neighborhood of the zero section in T*L.
- Symplectomorphism group: Symp(M, omega) = {f: M -> M diffeomorphism : f* omega = omega}.
  This is a group under composition and an infinite-dimensional Lie group. The Lie algebra
  is the space of symplectic vector fields (L_X omega = 0, or equivalently d(i_X omega) = 0).
  Hamiltonian vector fields form a sub-Lie-algebra; H^1(M; R) measures the discrepancy.
  Ham(M, omega) = connected component of the identity in Symp_0(M, omega) (for simply
  connected M, Symp_0 = Ham).
- Moser stability theorem (Moser 1965): if omega_t is a smooth family of cohomologous
  symplectic forms on a compact manifold M (i.e., d/dt [omega_t] = 0 in H^2(M; R)),
  then there exists a smooth family of diffeomorphisms phi_t with phi_t* omega_t = omega_0.
  Consequence: the symplectic structure on a compact manifold depends only on the
  cohomology class [omega] in H^2(M; R) (up to diffeomorphism); deformations within a
  fixed cohomology class are all equivalent.
- Gromov non-squeezing theorem (Gromov 1985): the closed ball B^{2n}(r) = {z in R^{2n} :
  |z| <= r} cannot be symplectically embedded into B^2(R) x R^{2n-2} if r > R, even
  though it can be embedded volumetrically (when 2n >= 4). This is the first rigidity
  result distinguishing symplectomorphisms from volume-preserving maps. The proof uses
  J-holomorphic curves (pseudoholomorphic curves), a technique introduced by Gromov.
  The symplectic width (Gromov width) of a domain U is the supremum of radii r such that
  B^{2n}(r) symplectically embeds in U. It is a genuine symplectic invariant.
- Cotangent bundle T*M: for any smooth manifold M, the cotangent bundle T*M carries a
  canonical symplectic form omega = -d lambda, where lambda = sum p_i dq_i is the
  tautological (Liouville) 1-form. The zero section of T*M is a Lagrangian submanifold.
  Every fiber T*_x M is also Lagrangian. The cotangent bundle is the canonical example
  of an exact symplectic manifold (omega = d(-lambda) is exact).
- Kahler manifolds: a Kahler manifold is a complex manifold (M, J) with a Hermitian
  metric g compatible with J and whose Kahler form omega(X,Y) = g(JX, Y) is closed.
  Every Kahler manifold is symplectic; the converse is false (there exist symplectic
  manifolds with no compatible complex structure). Complex projective space CP^n with the
  Fubini-Study form is the fundamental example. For Kahler manifolds, the Hodge numbers
  h^{p,q} and the hard Lefschetz theorem (L^{n-k}: H^k -> H^{2n-k} is an isomorphism)
  give strong topological constraints not shared by all symplectic manifolds.
- Coadjoint orbits (Kirillov-Kostant-Souriau): for a Lie group G with Lie algebra g,
  the coadjoint representation Ad*: G -> GL(g*) gives G-orbits O_mu = {Ad*_g mu : g in G}
  in g*. Each orbit carries a canonical KKS symplectic form omega^{KKS}_{mu}(ad*_X mu,
  ad*_Y mu) = mu([X, Y]). For G = SU(2), the coadjoint orbits are 2-spheres of radius r
  with omega = r * area form, recovering symplectic S^2. The coadjoint orbit is the
  phase space of a particle in a magnetic field (via geometric quantization).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result

# ---------------------------------------------------------------------------
# SymplecticProfile dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SymplecticProfile:
    """A curated symplectic topology example."""

    key: str
    display_name: str
    symplectic_type: str       # "standard", "cotangent", "kahler", "coadjoint_orbit", "product", "twisted"
    manifold_dimension: str    # "2n", "2", "4", "2n (2n >= 4)", etc.
    is_exact: bool             # omega = d alpha (exact 2-form)
    is_kahler: bool            # admits compatible Kahler structure
    is_compact: bool
    has_lagrangian: bool       # admits a Lagrangian submanifold
    is_monotone: bool          # [omega] = lambda * c_1(M) for some lambda > 0
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

DARBOUX_THEOREM_TAGS: frozenset[str] = frozenset({
    "darboux_theorem",
    "darboux_chart",
    "local_standard_form",
    "symplectic_normal_form",
    "darboux_coordinates",
    "no_local_invariants",
    "symplectic_rectification",
})

HAMILTONIAN_TAGS: frozenset[str] = frozenset({
    "hamiltonian_vector_field",
    "hamiltonian_flow",
    "hamiltonian_system",
    "hamiltonian_function",
    "poisson_bracket",
    "liouville_theorem",
    "noether_theorem",
    "conservation_law",
    "symplectic_flow",
    "integrable_hamiltonian",
})

LAGRANGIAN_TAGS: frozenset[str] = frozenset({
    "lagrangian_submanifold",
    "lagrangian",
    "isotropic_submanifold",
    "maslov_index",
    "lagrangian_grassmannian",
    "weinstein_neighborhood",
    "lagrangian_intersection",
    "floer_theory",
    "lagrangian_fibration",
})

SYMPLECTOMORPHISM_TAGS: frozenset[str] = frozenset({
    "symplectomorphism",
    "symplectic_diffeomorphism",
    "hamiltonian_diffeomorphism",
    "symp_group",
    "symplectic_isotopy",
    "moser_stability",
    "symplectic_equivalence",
    "canonical_transformation",
})

KAHLER_TAGS: frozenset[str] = frozenset({
    "kahler_manifold",
    "kahler_form",
    "kahler_structure",
    "fubini_study",
    "hard_lefschetz",
    "hodge_decomposition",
    "complex_projective",
    "kahler_potential",
    "hermitian_metric",
})

MOSER_THEOREM_TAGS: frozenset[str] = frozenset({
    "moser_theorem",
    "moser_stability",
    "cohomologous_forms",
    "deformation_equivalence",
    "moser_isotopy",
    "symplectic_deformation",
    "moser_trick",
})

GROMOV_NONSQUEEZING_TAGS: frozenset[str] = frozenset({
    "gromov_nonsqueezing",
    "nonsqueezing_theorem",
    "symplectic_width",
    "gromov_width",
    "pseudoholomorphic_curve",
    "j_holomorphic",
    "symplectic_rigidity",
    "symplectic_capacities",
})

COTANGENT_BUNDLE_TAGS: frozenset[str] = frozenset({
    "cotangent_bundle",
    "tautological_form",
    "liouville_form",
    "canonical_symplectic",
    "zero_section_lagrangian",
    "cotangent_fiber_lagrangian",
    "exact_symplectic",
    "phase_space",
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

def get_named_symplectic_profiles() -> tuple[SymplecticProfile, ...]:
    """Return the registry of canonical symplectic topology examples."""
    return (
        SymplecticProfile(
            key="standard_r2n",
            display_name="Standard symplectic (R^{2n}, omega_0) — Darboux's local model",
            symplectic_type="standard",
            manifold_dimension="2n",
            is_exact=True,
            is_kahler=True,
            is_compact=False,
            has_lagrangian=True,
            is_monotone=False,
            presentation_layer="main_text",
            focus=(
                "The standard symplectic manifold (R^{2n}, omega_0) with coordinates "
                "(x_1, ..., x_n, p_1, ..., p_n) and symplectic form "
                "omega_0 = sum_{i=1}^n dx_i ^ dp_i is the fundamental local model "
                "for all symplectic geometry. "
                "Closed and non-degenerate: d(omega_0) = 0 and "
                "omega_0^n = n! dx_1 ^ dp_1 ^ ... ^ dx_n ^ dp_n != 0. "
                "Darboux's theorem (1882) states that every symplectic manifold is "
                "locally symplectomorphic to this standard model — there are no local "
                "symplectic invariants, in stark contrast with Riemannian geometry. "
                "Exactness: omega_0 = d(lambda_0) where lambda_0 = sum p_i dx_i is the "
                "Liouville 1-form; hence omega_0 is exact. "
                "Lagrangian submanifolds: the coordinate hyperplane {p_1=...=p_n=0} = R^n "
                "is Lagrangian (omega_0|_{R^n} = 0 and dim R^n = n). "
                "Hamiltonian mechanics: the classical equations of motion q_dot = dH/dp, "
                "p_dot = -dH/dq are exactly the Hamilton flow of X_H on (R^{2n}, omega_0). "
                "The Poisson bracket {f, g} = sum_i (df/dp_i dg/dx_i - df/dx_i dg/dp_i). "
                "Kahler structure: omega_0 is the imaginary part of the standard Hermitian "
                "form on C^n = R^{2n} (identifying x_i + ip_i); (R^{2n}, J_0, omega_0) "
                "is a Kahler manifold, and the standard complex structure J_0 is compatible."
            ),
            chapter_targets=("15", "25", "38"),
        ),
        SymplecticProfile(
            key="cotangent_bundle_tm",
            display_name="Cotangent bundle T*M — canonical exact symplectic manifold",
            symplectic_type="cotangent",
            manifold_dimension="2n",
            is_exact=True,
            is_kahler=False,
            is_compact=False,
            has_lagrangian=True,
            is_monotone=False,
            presentation_layer="main_text",
            focus=(
                "For any smooth n-manifold M, the cotangent bundle pi: T*M -> M carries "
                "a canonical symplectic form constructed without any choice of metric. "
                "Tautological (Liouville) 1-form lambda: at a covector alpha in T*_q M, "
                "define lambda_alpha = alpha o pi_*  (pulling back via the base projection). "
                "In local coordinates (q_1,...,q_n, p_1,...,p_n): lambda = sum p_i dq_i. "
                "Canonical symplectic form: omega = -d lambda = sum dq_i ^ dp_i. "
                "The sign is chosen so that i_{X_H} omega = -dH gives standard Hamilton "
                "equations. Note omega = d(-lambda), so T*M is exact symplectic. "
                "Compact base: if M is compact, T*M is non-compact (fibers are R^n). "
                "Lagrangian submanifolds: the zero section {p = 0} is Lagrangian "
                "(lambda|_{zero section} = 0, hence omega|_L = 0). Each fiber T*_q M "
                "is also Lagrangian (omega vanishes on vertical tangent vectors). "
                "Graph of a 1-form: the graph of a closed 1-form theta (d theta = 0) "
                "is a Lagrangian submanifold of T*M; if theta = dS (exact), the graph "
                "is exact Lagrangian (key in generating functions / Hamilton-Jacobi theory). "
                "Weinstein's Lagrangian neighborhood theorem: every compact Lagrangian L "
                "in any symplectic manifold has a neighborhood symplectomorphic to "
                "a neighborhood of the zero section in T*L. "
                "Classical mechanics: T*M is the phase space of a mechanical system with "
                "configuration space M; H: T*M -> R encodes kinetic + potential energy."
            ),
            chapter_targets=("15", "25", "38"),
        ),
        SymplecticProfile(
            key="s2_area_form",
            display_name="(S^2, r * dA) — 2-sphere with area form",
            symplectic_type="standard",
            manifold_dimension="2",
            is_exact=False,
            is_kahler=True,
            is_compact=True,
            has_lagrangian=False,
            is_monotone=True,
            presentation_layer="main_text",
            focus=(
                "The 2-sphere S^2 = {(x,y,z) in R^3 : x^2+y^2+z^2 = r^2} with the "
                "area form omega = r * dA (where dA is the standard area element) is the "
                "simplest compact symplectic manifold. "
                "Formula: in spherical coordinates, omega = r sin(theta) d(theta) ^ d(phi). "
                "In stereographic coordinates: omega = 4r^2/(1+|z|^2)^2 * (i/2) dz ^ dz_bar. "
                "Closedness: H^2(S^2; R) = R, and [omega] = 4 pi r^2 [vol_{S^2}] != 0 "
                "(the total area). Since d omega = 0 and [omega] != 0, S^2 is symplectic "
                "but omega is NOT exact (H^2(S^2) != 0 — no global primitive). "
                "Lagrangian submanifolds: S^2 is 2-dimensional, so a Lagrangian would "
                "be 1-dimensional (S^1 or R). But omega restricted to any curve is 0 "
                "trivially; however, the correct notion requires dim L = n = 1, i.e., "
                "curves are isotropic but not Lagrangian in the standard sense. "
                "For compact surfaces, has_lagrangian = False (no closed Lagrangian curve). "
                "Kahler: S^2 = CP^1 is a Riemann surface, hence Kahler with complex "
                "structure J (rotation by 90 degrees). The Fubini-Study form on CP^1 "
                "coincides with the area form up to normalization. "
                "Monotone: [omega] = r * [c_1(TS^2)] (for r = 1, [omega] = [c_1] in H^2). "
                "Coadjoint orbit: S^2 of radius r is the coadjoint orbit of SU(2) through "
                "mu = (0,0,r) in su(2)* = R^3, with KKS symplectic form = r * dA."
            ),
            chapter_targets=("15", "25", "38"),
        ),
        SymplecticProfile(
            key="cpn_fubini_study",
            display_name="(CP^n, omega_{FS}) — complex projective space with Fubini-Study form",
            symplectic_type="kahler",
            manifold_dimension="2n",
            is_exact=False,
            is_kahler=True,
            is_compact=True,
            has_lagrangian=True,
            is_monotone=True,
            presentation_layer="main_text",
            focus=(
                "Complex projective space CP^n = (C^{n+1} \\ {0}) / C* with the "
                "Fubini-Study Kahler form omega_{FS} is the fundamental compact Kahler "
                "manifold and the basic example of a monotone symplectic manifold. "
                "Construction: omega_{FS} = (i/2) del del_bar log(|z|^2), where z "
                "(z_0:...:z_n) are homogeneous coordinates. Locally on the chart "
                "{z_0 != 0}: omega_{FS} = (i/2) del del_bar log(1 + |w|^2) for "
                "w = (z_1/z_0, ..., z_n/z_0) in C^n. "
                "Kahler: the Fubini-Study metric g_{FS} and omega_{FS} are related by "
                "omega_{FS}(X,Y) = g_{FS}(JX,Y) where J is the standard complex structure. "
                "This makes (CP^n, J, g_{FS}, omega_{FS}) a Kahler manifold. "
                "Cohomology: H^{2k}(CP^n; Z) = Z for 0 <= k <= n, generated by [omega_{FS}]^k. "
                "Hard Lefschetz: the map L^k: H^{n-k} -> H^{n+k} (wedge with omega_{FS}) is "
                "an isomorphism — a strong topological constraint on Kahler manifolds. "
                "Monotone: [omega_{FS}] = c_1(T CP^n) in H^2(CP^n; R) — this is the "
                "monotonicity condition essential for Floer theory and quantum cohomology. "
                "Lagrangian submanifolds: RP^n = {[z] in CP^n : z_i in R} is a Lagrangian "
                "submanifold of CP^n (dim RP^n = n, omega_{FS}|_{RP^n} = 0). "
                "Gromov's non-squeezing: CP^1 = S^2 cannot be symplectically squeezed "
                "into a thin cylinder, illustrating non-squeezing at the simplest level."
            ),
            chapter_targets=("15", "25", "38"),
        ),
        SymplecticProfile(
            key="torus_t2n",
            display_name="(T^{2n}, omega_0) — flat torus with standard symplectic form",
            symplectic_type="product",
            manifold_dimension="2n",
            is_exact=False,
            is_kahler=True,
            is_compact=True,
            has_lagrangian=True,
            is_monotone=False,
            presentation_layer="main_text",
            focus=(
                "The 2n-dimensional torus T^{2n} = R^{2n}/Z^{2n} with the descent of "
                "omega_0 = sum dx_i ^ dp_i is a compact symplectic manifold. "
                "Construction: omega_0 is translation-invariant on R^{2n}, hence descends "
                "to T^{2n} = R^{2n}/Z^{2n}. Since d omega_0 = 0 on R^{2n}, we get "
                "d omega_{T^{2n}} = 0. Non-degeneracy follows from R^{2n}. "
                "Not exact: H^2(T^{2n}; R) != 0 ([omega] generates Z in H^2). "
                "Kahler: T^{2n} = C^n / (Z^{2n}) is a complex torus with the standard "
                "complex structure; the Kahler form is omega_0. "
                "Lagrangian fibration: T^{2n} -> T^n (projection onto first n coordinates) "
                "is a Lagrangian fibration — each fiber {p = const} is a Lagrangian torus T^n. "
                "This is the prototype for integrable Hamiltonian systems and "
                "Arnold-Liouville theorem (action-angle coordinates). "
                "Moser stability: any symplectic form cohomologous to omega_0 on T^{2n} "
                "is isotopic to omega_0 by Moser's theorem (since T^{2n} is compact). "
                "Symplectomorphism group: Sp(2n, Z) acts on T^{2n} as a discrete group "
                "of symplectomorphisms; the full Symp(T^{2n}, omega) is much larger. "
                "Applications: T^{2n} appears as the phase space of n decoupled harmonic "
                "oscillators (with action-angle variables), and in the KAM theorem for "
                "nearly integrable Hamiltonian systems."
            ),
            chapter_targets=("15", "25", "38"),
        ),
        SymplecticProfile(
            key="coadjoint_orbit_su2",
            display_name="Coadjoint orbit O_r of SU(2) — KKS symplectic form on S^2",
            symplectic_type="coadjoint_orbit",
            manifold_dimension="2",
            is_exact=False,
            is_kahler=True,
            is_compact=True,
            has_lagrangian=False,
            is_monotone=True,
            presentation_layer="main_text",
            focus=(
                "The Kirillov-Kostant-Souriau (KKS) construction provides a canonical "
                "symplectic structure on every coadjoint orbit of a Lie group. "
                "Setup: G = SU(2), Lie algebra su(2) = span{e_1, e_2, e_3} with "
                "[e_i, e_j] = epsilon_{ijk} e_k. Identify su(2)* = R^3 via the "
                "Killing form. Coadjoint action: Ad*_g(mu) = R_g(mu) (rotation by g). "
                "Coadjoint orbit through mu = (0,0,r): O_r = {Ad*_g mu : g in SU(2)} "
                "= S^2 of radius r (sphere in R^3 = su(2)*). "
                "KKS symplectic form: at mu in O_r, "
                "omega^{KKS}_mu(ad*_X mu, ad*_Y mu) = mu([X,Y]) for X,Y in su(2). "
                "Explicitly: omega^{KKS}|_{S^2(r)} = r * (standard area form on S^2). "
                "Agreement with S^2: this recovers the symplectic S^2 from the "
                "geometric quantization perspective. The sphere of radius r has "
                "total area 4 pi r^2 and [omega^{KKS}] = 4 pi r in H^2(S^2; R). "
                "Geometric quantization: the quantization condition [omega/(2pi h)] in "
                "H^2(O_r; Z) requires r in (h/2) Z (i.e., r = 0, h/2, h, 3h/2, ...) — "
                "this is exactly the quantization of angular momentum in quantum mechanics! "
                "General G: for any compact Lie group G, each coadjoint orbit carries a "
                "KKS symplectic form, and the orbit is a homogeneous Kahler manifold "
                "(Borel-Weil theorem). The Duistermaat-Heckman theorem gives a formula "
                "for the symplectic volume of the orbit in terms of weights."
            ),
            chapter_targets=("15", "25", "38"),
        ),
        SymplecticProfile(
            key="gromov_nonsqueezing_example",
            display_name="Gromov non-squeezing — B^{2n}(r) cannot embed in B^2(R) x R^{2n-2} for r > R",
            symplectic_type="standard",
            manifold_dimension="2n (2n >= 4)",
            is_exact=True,
            is_kahler=False,
            is_compact=False,
            has_lagrangian=True,
            is_monotone=False,
            presentation_layer="main_text",
            focus=(
                "Gromov's non-squeezing theorem (1985) is the first result showing that "
                "symplectomorphisms are more rigid than volume-preserving maps. "
                "Statement: there is no symplectic embedding of the ball "
                "B^{2n}(r) = {z in R^{2n} : |z|^2 <= r^2} into the cylinder "
                "Z^{2n}(R) = {z in R^{2n} : z_1^2 + z_{n+1}^2 <= R^2} if r > R. "
                "Here R = (0 in R^{2n-2} or any value), and the cylinder corresponds "
                "to B^2(R) x R^{2n-2} in the (x_1, p_1) plane. "
                "Volume vs. symplectic: for n >= 2, B^{2n}(r) can be embedded in "
                "B^2(R) x R^{2n-2} volume-preservingly (for any r, R) — one can "
                "compress the ball in all but the first two directions. But symplectically, "
                "the 'shadow' in any 2-dimensional symplectic plane is constrained. "
                "Proof via J-holomorphic curves: Gromov introduced pseudoholomorphic curves "
                "to prove this. If a symplectic embedding phi: B^{2n}(r) -> Z^{2n}(R) "
                "existed with r > R, one constructs a J-holomorphic disk in B^{2n}(r) "
                "with boundary on a torus, whose area under phi would violate the "
                "monotonicity of J-holomorphic curves with respect to omega. "
                "Symplectic capacities: the Gromov width c(M, omega) = sup{pi r^2 : "
                "B^{2n}(r) embeds symplectically in (M, omega)} is a symplectic invariant "
                "that measures the largest ball that fits inside M. For Z^{2n}(R): "
                "c(Z^{2n}(R)) = pi R^2 (equal to the area of the 2D disk). "
                "Applications: symplectic capacities distinguish symplectic manifolds "
                "that are indistinguishable by cohomology or volume alone. "
                "Ekeland-Hofer capacities and the Hofer-Zehnder capacity extend this."
            ),
            chapter_targets=("15", "25", "38"),
        ),
        SymplecticProfile(
            key="moser_stability_example",
            display_name="Moser stability — cohomologous symplectic forms are equivalent",
            symplectic_type="standard",
            manifold_dimension="2n",
            is_exact=False,
            is_kahler=False,
            is_compact=True,
            has_lagrangian=True,
            is_monotone=False,
            presentation_layer="main_text",
            focus=(
                "Moser's stability theorem (1965) shows that the symplectic structure on "
                "a compact manifold is determined (up to diffeomorphism) by its cohomology "
                "class. "
                "Statement: let M be compact and omega_t (t in [0,1]) a smooth path of "
                "symplectic forms on M with [omega_t] constant in H^2(M; R). Then there "
                "exists a smooth isotopy phi_t: M -> M with phi_0 = id and "
                "phi_t* omega_t = omega_0 for all t. "
                "Proof (Moser's trick): "
                "1. Write d/dt omega_t = d(sigma_t) for some 1-form sigma_t "
                "   (possible because d/dt [omega_t] = 0 in H^2, so d/dt omega_t is exact). "
                "2. Solve the equation i_{X_t} omega_t = -sigma_t for vector field X_t "
                "   (possible since omega_t is non-degenerate). "
                "3. Let phi_t be the flow of X_t; compute d/dt(phi_t* omega_t) = "
                "   phi_t*(L_{X_t} omega_t + d/dt omega_t) = phi_t*(d(i_{X_t} omega_t) + d sigma_t) "
                "   = phi_t* d(-sigma_t + sigma_t) = 0. "
                "Consequence: any two cohomologous symplectic forms on a compact manifold "
                "are symplectomorphic. In particular, the symplectic structure up to "
                "diffeomorphism depends only on [omega] in H^2(M; R). "
                "Darboux as corollary: on a small ball, any two symplectic forms are "
                "cohomologous (both are exact near a point), so Moser's argument gives "
                "a local diffeomorphism; this is Darboux's theorem. "
                "Failure for non-compact: Moser stability requires compactness to solve "
                "the ODE globally. For non-compact M, the isotopy may not exist."
            ),
            chapter_targets=("15", "25", "38"),
        ),
    )


# ---------------------------------------------------------------------------
# Summary / index functions
# ---------------------------------------------------------------------------

def symplectic_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_symplectic_profiles()
    ))


def symplectic_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_symplectic_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {ch: tuple(keys) for ch, keys in sorted(chapter_map.items())}


def symplectic_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from symplectic_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_symplectic_profiles():
        index.setdefault(p.symplectic_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_symplectic_manifold(space: Any) -> Result:
    """Check whether a space carries a symplectic structure.

    A symplectic manifold is a smooth even-dimensional manifold (M^{2n}, omega)
    where omega is a closed (d omega = 0) and non-degenerate 2-form.
    Non-degeneracy: omega^n != 0 (equivalently, the map TM -> T*M, v |-> i_v omega,
    is an isomorphism).

    Decision layers
    ---------------
    1. Explicit 'symplectic_manifold' or Darboux/Hamiltonian tags -> true.
    2. Known symplectic structures (cotangent bundle, Kahler, coadjoint orbit) -> true.
    3. Known non-symplectic (odd-dimensional, non-closed form) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    explicit_symplectic = {
        "symplectic_manifold", "symplectic_structure", "symplectic_form",
        "closed_nondegenerate_form",
    }
    if _matches_any(tags, explicit_symplectic):
        witness = next(t for t in tags if t in explicit_symplectic)
        return Result.true(
            mode="theorem",
            value="symplectic_manifold",
            justification=[
                f"Tag {witness!r}: the space is a symplectic manifold — it carries "
                "a closed non-degenerate 2-form omega (d omega = 0, omega^n != 0).",
            ],
            metadata={**base, "criterion": "explicit_symplectic", "witness": witness},
        )

    if _matches_any(tags, DARBOUX_THEOREM_TAGS):
        witness = next(t for t in tags if t in DARBOUX_THEOREM_TAGS)
        return Result.true(
            mode="theorem",
            value="symplectic_manifold",
            justification=[
                f"Tag {witness!r}: the space admits Darboux coordinates — a local "
                "symplectomorphism to (R^{2n}, omega_0). The space is symplectic.",
            ],
            metadata={**base, "criterion": "darboux_chart", "witness": witness},
        )

    if _matches_any(tags, HAMILTONIAN_TAGS):
        witness = next(t for t in tags if t in HAMILTONIAN_TAGS)
        return Result.true(
            mode="theorem",
            value="symplectic_manifold",
            justification=[
                f"Tag {witness!r}: Hamiltonian structure requires a symplectic form "
                "to define vector fields X_H via i_{X_H} omega = -dH. "
                "The space is symplectic.",
            ],
            metadata={**base, "criterion": "hamiltonian_implies_symplectic", "witness": witness},
        )

    derived_symplectic = {
        "cotangent_bundle", "canonical_symplectic", "kahler_manifold",
        "coadjoint_orbit", "kks_form", "fubini_study", "symplectic_torus",
        "area_form_surface", "symplectic_product",
    }
    if _matches_any(tags, derived_symplectic | COTANGENT_BUNDLE_TAGS | KAHLER_TAGS):
        witness = next(
            t for t in tags
            if t in (derived_symplectic | COTANGENT_BUNDLE_TAGS | KAHLER_TAGS)
        )
        return Result.true(
            mode="theorem",
            value="symplectic_manifold",
            justification=[
                f"Tag {witness!r}: cotangent bundles, Kahler manifolds, and coadjoint "
                "orbits all carry canonical symplectic structures. The space is symplectic.",
            ],
            metadata={**base, "criterion": "canonical_construction", "witness": witness},
        )

    non_symplectic = {
        "odd_dimensional", "non_closed_form", "degenerate_form",
        "no_symplectic_structure", "contact_manifold_only",
    }
    if _matches_any(tags, non_symplectic):
        witness = next(t for t in tags if t in non_symplectic)
        return Result.false(
            mode="theorem",
            value="not_symplectic",
            justification=[
                f"Tag {witness!r}: the space does not admit a symplectic structure. "
                "Obstructions include odd dimension, non-closedness, or degeneracy of the form.",
            ],
            metadata={**base, "criterion": "explicit_obstruction", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate a symplectic structure or an obstruction. "
            "Cannot determine whether the space is symplectic.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def is_lagrangian_submanifold(space: Any) -> Result:
    """Check whether the space is a Lagrangian submanifold.

    A Lagrangian submanifold of (M^{2n}, omega) is a submanifold L^n with
    omega|_L = 0 and dim L = n (half the ambient dimension). Equivalently,
    TL = (TL)^{omega-perp} — each tangent space is its own omega-annihilator.

    Decision layers
    ---------------
    1. Explicit 'lagrangian_submanifold' or Maslov/Floer tags -> true.
    2. Known Lagrangian structures (zero section, cotangent fiber, RP^n) -> true.
    3. Known non-Lagrangian (symplectic submanifold, co-isotropic only) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, LAGRANGIAN_TAGS):
        witness = next(t for t in tags if t in LAGRANGIAN_TAGS)
        return Result.true(
            mode="theorem",
            value="lagrangian_submanifold",
            justification=[
                f"Tag {witness!r}: the submanifold is Lagrangian — omega|_L = 0 and "
                "dim L = n = (1/2) dim M. Weinstein's neighborhood theorem applies.",
            ],
            metadata={**base, "criterion": "explicit_lagrangian", "witness": witness},
        )

    known_lagrangian = {
        "zero_section_lagrangian", "cotangent_fiber_lagrangian",
        "real_projective_space", "lagrangian_torus", "lagrangian_fibration",
    }
    if _matches_any(tags, known_lagrangian | COTANGENT_BUNDLE_TAGS):
        relevant = known_lagrangian | {"zero_section_lagrangian", "cotangent_fiber_lagrangian",
                                       "lagrangian_torus", "lagrangian_fibration"}
        matching = tags & relevant
        if matching:
            witness = next(iter(matching))
            return Result.true(
                mode="theorem",
                value="lagrangian_submanifold",
                justification=[
                    f"Tag {witness!r}: this is a standard Lagrangian (zero section, "
                    "cotangent fiber, or Lagrangian torus in T^{2n}).",
                ],
                metadata={**base, "criterion": "known_lagrangian", "witness": witness},
            )

    non_lagrangian = {
        "symplectic_submanifold", "symplectic_surface", "coisotropic_only",
        "complex_submanifold", "non_lagrangian",
    }
    if _matches_any(tags, non_lagrangian):
        witness = next(t for t in tags if t in non_lagrangian)
        return Result.false(
            mode="theorem",
            value="not_lagrangian",
            justification=[
                f"Tag {witness!r}: a symplectic submanifold (omega|_L non-degenerate) "
                "is not Lagrangian (which requires omega|_L = 0). These are "
                "complementary conditions.",
            ],
            metadata={**base, "criterion": "symplectic_vs_lagrangian", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate a Lagrangian structure. "
            "Cannot determine Lagrangian status.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def has_hamiltonian_structure(space: Any) -> Result:
    """Check whether the space admits a Hamiltonian structure.

    A Hamiltonian system is a triple (M, omega, H) where (M, omega) is symplectic
    and H: M -> R is the Hamiltonian function. The Hamiltonian vector field X_H is
    defined by i_{X_H} omega = -dH (equivalently omega(X_H, .) = -dH(.)).
    The flow of X_H preserves omega (Liouville's theorem).

    Decision layers
    ---------------
    1. Explicit Hamiltonian or Poisson tags -> true.
    2. Symplectic manifold tags (all symplectic manifolds admit Hamiltonian functions) -> true.
    3. Non-symplectic obstructions -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, HAMILTONIAN_TAGS):
        witness = next(t for t in tags if t in HAMILTONIAN_TAGS)
        return Result.true(
            mode="theorem",
            value="hamiltonian_structure",
            justification=[
                f"Tag {witness!r}: the space has an explicit Hamiltonian structure — "
                "a symplectic form omega and a Hamiltonian H defining X_H by "
                "i_{X_H} omega = -dH.",
            ],
            metadata={**base, "criterion": "explicit_hamiltonian", "witness": witness},
        )

    symplectic_structures = {
        "symplectic_manifold", "symplectic_form", "symplectic_structure",
        "cotangent_bundle", "canonical_symplectic", "kahler_manifold",
        "coadjoint_orbit",
    }
    if _matches_any(tags, symplectic_structures | COTANGENT_BUNDLE_TAGS | DARBOUX_THEOREM_TAGS):
        relevant = (symplectic_structures | COTANGENT_BUNDLE_TAGS | DARBOUX_THEOREM_TAGS) & tags
        witness = next(iter(relevant))
        return Result.true(
            mode="theorem",
            value="hamiltonian_structure",
            justification=[
                f"Tag {witness!r}: every symplectic manifold admits Hamiltonian structures — "
                "any smooth function H: M -> R defines a Hamiltonian vector field X_H. "
                "The symplectic form provides the required non-degenerate pairing.",
            ],
            metadata={**base, "criterion": "symplectic_implies_hamiltonian", "witness": witness},
        )

    non_symplectic = {
        "odd_dimensional", "non_closed_form", "degenerate_form",
        "no_symplectic_structure",
    }
    if _matches_any(tags, non_symplectic):
        witness = next(t for t in tags if t in non_symplectic)
        return Result.false(
            mode="theorem",
            value="no_hamiltonian_structure",
            justification=[
                f"Tag {witness!r}: without a symplectic form, the equation "
                "i_{X_H} omega = -dH cannot be solved for X_H. No Hamiltonian structure.",
            ],
            metadata={**base, "criterion": "no_symplectic_form", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate a Hamiltonian or symplectic structure. "
            "Cannot determine Hamiltonian status.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def admits_kahler_structure(space: Any) -> Result:
    """Check whether the space admits a Kahler structure.

    A Kahler manifold is a complex manifold (M, J) with a Hermitian metric g such
    that the Kahler form omega(X,Y) = g(JX,Y) is closed. A Kahler manifold is
    automatically symplectic. The converse fails: there exist symplectic manifolds
    (e.g., Kodaira-Thurston manifold) with no compatible complex structure.

    Decision layers
    ---------------
    1. Explicit Kahler tags -> true.
    2. Known Kahler manifolds (CP^n, Riemann surfaces, Kahler tori, coadjoint orbits) -> true.
    3. Explicit non-Kahler tags (symplectic non-Kahler, odd Betti numbers) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, KAHLER_TAGS):
        witness = next(t for t in tags if t in KAHLER_TAGS)
        return Result.true(
            mode="theorem",
            value="kahler_structure",
            justification=[
                f"Tag {witness!r}: the manifold is Kahler — it carries a compatible "
                "triple (J, g, omega) where J is integrable, g is Hermitian, and omega "
                "is closed. Hard Lefschetz and Hodge decomposition hold.",
            ],
            metadata={**base, "criterion": "explicit_kahler", "witness": witness},
        )

    known_kahler = {
        "complex_projective", "riemann_surface", "algebraic_variety",
        "kahler_torus", "complex_torus", "coadjoint_orbit",
    }
    if _matches_any(tags, known_kahler):
        witness = next(t for t in tags if t in known_kahler)
        return Result.true(
            mode="theorem",
            value="kahler_structure",
            justification=[
                f"Tag {witness!r}: complex projective varieties, Riemann surfaces, and "
                "coadjoint orbits of compact Lie groups are Kahler manifolds by "
                "classical theory (Kodaira embedding / Borel-Weil).",
            ],
            metadata={**base, "criterion": "classical_kahler", "witness": witness},
        )

    non_kahler = {
        "non_kahler", "symplectic_non_kahler", "kodaira_thurston",
        "odd_odd_betti", "no_hard_lefschetz",
    }
    if _matches_any(tags, non_kahler):
        witness = next(t for t in tags if t in non_kahler)
        return Result.false(
            mode="theorem",
            value="not_kahler",
            justification=[
                f"Tag {witness!r}: the manifold is symplectic but not Kahler. "
                "Obstructions include: odd odd-degree Betti numbers, failure of "
                "Hard Lefschetz, or explicit Kodaira-Thurston-type construction.",
            ],
            metadata={**base, "criterion": "non_kahler_obstruction", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate a Kahler structure or an obstruction. "
            "Cannot determine Kahler status.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


# ---------------------------------------------------------------------------
# Facade functions
# ---------------------------------------------------------------------------

def classify_symplectic(space: Any) -> dict[str, Any]:
    """Run all symplectic analysis functions and return a combined result dict."""
    return {
        "is_symplectic_manifold":    is_symplectic_manifold(space),
        "is_lagrangian_submanifold": is_lagrangian_submanifold(space),
        "has_hamiltonian_structure": has_hamiltonian_structure(space),
        "admits_kahler_structure":   admits_kahler_structure(space),
    }


def symplectic_profile(space: Any) -> dict[str, Any]:
    """Return a comprehensive symplectic profile of the space."""
    classification = classify_symplectic(space)
    return {
        "space": space,
        "tags": sorted(_extract_tags(space)),
        "representation": _representation_of(space),
        "classification": classification,
        "summary": {
            k: r.value for k, r in classification.items()
        },
    }


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------

__all__ = [
    "SymplecticProfile",
    "DARBOUX_THEOREM_TAGS",
    "HAMILTONIAN_TAGS",
    "LAGRANGIAN_TAGS",
    "SYMPLECTOMORPHISM_TAGS",
    "KAHLER_TAGS",
    "MOSER_THEOREM_TAGS",
    "GROMOV_NONSQUEEZING_TAGS",
    "COTANGENT_BUNDLE_TAGS",
    "get_named_symplectic_profiles",
    "symplectic_layer_summary",
    "symplectic_chapter_index",
    "symplectic_type_index",
    "is_symplectic_manifold",
    "is_lagrangian_submanifold",
    "has_hamiltonian_structure",
    "admits_kahler_structure",
    "classify_symplectic",
    "symplectic_profile",
]
