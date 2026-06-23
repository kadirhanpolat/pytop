r"""Spectral sequences: Serre, Adams, Eilenberg-Moore, Atiyah-Hirzebruch, Leray-Hirsch,
Lyndon-Hochschild-Serre, Bockstein, Grothendieck; convergence, differentials, filtrations.

Key theorems and constructions implemented
------------------------------------------
- Spectral sequence definition: a spectral sequence is a collection {E_r^{p,q}, d_r}_{r>=2}
  where d_r: E_r^{p,q} -> E_r^{p+r, q-r+1} (cohomological convention) with d_r^2 = 0,
  and E_{r+1}^{p,q} = H^{p,q}(E_r, d_r) = ker(d_r) / im(d_r). Convergence: a spectral
  sequence converges to H^n (written E_r => H^n) means there is a filtration
  F^0 H^n supset F^1 H^n supset ... supset F^{n+1} H^n = 0 (complete and bounded) such
  that E_infty^{p,q} = gr^p H^{p+q} = F^p H^{p+q} / F^{p+1} H^{p+q} for all p, q.
  Strong convergence: E_r => H^n strongly when F^p H^n = 0 for p >> 0 and
  union_{p} F^p H^n = H^n (Hausdorff + complete filtration). Conditional convergence
  (Boardman): allows lim^1 obstructions; the Adams spectral sequence is conditionally
  but not always strongly convergent.

- Serre spectral sequence (Serre 1951): for a fibration F -> E -> B with B simply
  connected (pi_1(B) = 0), the Serre spectral sequence has E_2^{p,q} = H^p(B; H^q(F))
  (cohomology of B with local coefficients H^q(F)) converging strongly to H^{p+q}(E).
  Multiplicative structure: the Serre SS is a spectral sequence of algebras; the product
  on E_2 is the cup product on H^*(B) tensor H^*(F), and the spectral sequence converges
  to the filtered algebra H^*(E). Key applications:
  - Path-loop fibration: Omega X -> PX -> X (PX contractible), so E_2^{p,q} =
    H^p(X; H^q(Omega X)) => H^{p+q}(PX) = Z in degree 0. This allows computation
    of H^*(Omega X) from H^*(X) by induction using the transgression d_r.
  - Gysin sequence: for a sphere bundle S^k -> E -> B, the Serre SS gives the Gysin
    long exact sequence ... -> H^n(E) -> H^{n-k}(B) -> H^n(B) -> H^{n+1}(E) -> ...
    involving the Euler class e in H^{k+1}(B).
  - Edge homomorphisms: E_2^{p,0} -> H^p(E) (base edge) and H^n(E) -> E_infty^{0,n}
    -> E_2^{0,n} = H^n(F) (fiber edge) are natural maps arising from the spectral
    sequence filtration.
  - Cohomology of CP^infty: using S^1 -> S^infty -> CP^infty with S^infty contractible,
    the Serre SS gives H^*(CP^infty) = Z[x] with |x| = 2.

- Adams spectral sequence (Adams 1958): for a p-local spectrum X, the Adams spectral
  sequence has E_2^{s,t} = Ext^{s,t}_{A}(H^*(X; F_p), F_p) where A is the Steenrod
  algebra, converging conditionally to pi_{t-s}(X)_p^hat (p-completed stable homotopy
  groups). For X = S^0: E_2 = Ext^{s,t}_A(F_p, F_p) => pi_{t-s}^s(S^0)_p^hat.
  Key properties:
  - The Adams resolution: an A-free resolution 0 -> F_p -> C^0 -> C^1 -> ... of
    H^*(X; F_p) as A-modules gives the E_2 page via Ext groups.
  - The d_2 differential: d_2: E_2^{s,t} -> E_2^{s+2,t+1} is related to the
    secondary cohomology operations.
  - Hopf invariant one: the Adams spectral sequence detects elements h_j in
    Ext^{1,2^j} corresponding to Hopf invariant one maps; Adams' theorem states
    that only h_1, h_2, h_3 (corresponding to dimensions 2, 4, 8: complex numbers,
    quaternions, octonions) survive to give non-trivial elements in pi_*^s(S^0).
  - Stem computations: the chart of Ext_A(F_2, F_2) encodes the 2-primary stable
    homotopy groups of spheres, with the rho, nu, sigma, eta generators visible.

- Eilenberg-Moore spectral sequence: for a pullback diagram X = E x_B PB (fiber
  product of E -> B with the path fibration PB -> B), the Eilenberg-Moore spectral
  sequence has E_2^{-s,t} = Tor^{-s,t}_{H^*(B)}(H^*(E), k) converging to H^*(X)
  when B is simply connected. Special case: for E = {b_0} a point,
  E_2 = Tor_{H^*(B)}(k, k) => H^*(Omega B). The bar construction B(H^*(B)) computes
  these Tor groups and serves as the E_1 page of the bar spectral sequence. The EM SS
  is multiplicative and converges in the second quadrant (s >= 0, arbitrary t).

- Atiyah-Hirzebruch spectral sequence (AHSS): for a generalized cohomology theory h^*
  and a CW-complex X, the AHSS has E_2^{p,q} = H^p(X; h^q(pt)) converging to
  h^{p+q}(X). For h^* = K^* (complex K-theory): E_2^{p,q} = H^p(X; Z) for q even
  (using K^0(pt) = Z) and 0 for q odd (using K^1(pt) = 0), converging to K^{p+q}(X).
  The first non-trivial differential d_3 = Sq^3 (the Steenrod operation composed with
  the Bockstein). For h^* = MU^* (complex cobordism): the AHSS has
  E_2^{p,q} = H^p(X; MU^q(pt)) => MU^{p+q}(X). For CP^n: the AHSS for K-theory
  collapses at E_2 because all differentials vanish (degree reasons), giving
  K^*(CP^n) directly from H^*(CP^n; Z) via the Chern character isomorphism
  ch: K^0(CP^n) tensor Q -> H^{ev}(CP^n; Q).

- Leray-Serre theorem / Leray-Hirsch: if a fibration F -> E -> B has the property
  that H^*(F; k) is a free k-module and there exist global cohomology classes in
  H^*(E; k) restricting to a basis of H^*(F; k) at every fiber (the Leray-Hirsch
  condition), then H^*(E; k) = H^*(B; k) tensor_k H^*(F; k) as H^*(B; k)-modules
  and the Serre spectral sequence collapses at the E_2 page. Applications: principal
  bundles with contractible structure groups, sphere bundles over simply connected
  bases satisfying the orientation condition, and K-theory of CP^n.

- Lyndon-Hochschild-Serre (LHS) spectral sequence: for a group extension
  1 -> N -> G -> Q -> 1 and a G-module M, the LHS spectral sequence has
  E_2^{p,q} = H^p(Q; H^q(N; M)) converging to H^{p+q}(G; M). The 5-term exact
  sequence extracted from the LHS SS: 0 -> H^1(Q; M^N) -> H^1(G; M) -> H^1(N; M)^Q
  -> H^2(Q; M^N) -> H^2(G; M) is the inflation-restriction exact sequence in group
  cohomology. Applications: computing group cohomology of semidirect products,
  p-groups, and central extensions.

- Convergence theory: strong convergence of a spectral sequence {E_r, d_r} to H^*
  means (1) for all (p,q), d_r^{p,q} = 0 for r >> 0 (the sequence stabilizes to
  E_infty^{p,q}), and (2) H^n has a complete Hausdorff filtration with
  gr^p H^{p+q} = E_infty^{p,q}. A first-quadrant spectral sequence (E_2^{p,q} = 0
  for p < 0 or q < 0) converges strongly automatically when the differentials
  eventually vanish. Conditionally convergent spectral sequences (Boardman) require
  additional conditions (like Re-indexing or Milnor lim^1 = 0) to ensure the map
  E_infty -> gr H^* is an isomorphism.

- Bockstein spectral sequence: associated to a short exact sequence of coefficient
  groups 0 -> Z -p-> Z -> Z/p -> 0, the Bockstein spectral sequence has E_1 = H^*(X; Z/p)
  with d_1 = beta (the Bockstein operation, i.e., the connecting homomorphism of the
  long exact sequence in cohomology). E_2 detects the Z/p-free part of H^*(X; Z),
  and the spectral sequence converges to H^*(X; Z) tensor Z/p. Collapses at E_2
  iff H^*(X; Z) has no p-torsion.

- Grothendieck spectral sequence: for a composition of left-exact functors F, G:
  A -> B -> C (abelian categories, G taking injectives to F-acyclics), the Grothendieck
  spectral sequence has E_2^{p,q} = (R^p F)(R^q G)(A) converging to R^{p+q}(FG)(A).
  Gives a systematic construction of long exact sequences from short ones via derived
  functors. The Leray spectral sequence for a map f: X -> Y is the special case
  F = Gamma(Y, -), G = f_* (direct image sheaf): E_2^{p,q} = H^p(Y; R^q f_*(F))
  => H^{p+q}(X; F).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result

# ---------------------------------------------------------------------------
# SpectralSequenceProfile dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SpectralSequenceProfile:
    """A curated spectral sequence theory example."""

    key: str
    display_name: str
    sequence_type: str          # "serre", "adams", "eilenberg_moore",
                                # "atiyah_hirzebruch", "leray",
                                # "lyndon_hochschild_serre", "bockstein",
                                # "mayer_vietoris"
    cohomology_type: str        # "singular", "k_theory", "group", "general"
    converges_to: str
    is_multiplicative: bool
    is_first_quadrant: bool
    collapses_at_e2: bool
    is_conditionally_convergent: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

SERRE_SS_TAGS: frozenset[str] = frozenset({
    "serre_spectral_sequence",
    "serre_fibration",
    "serre_ss",
    "path_space_fibration",
    "transgression",
    "edge_homomorphism",
    "euler_class_ss",
    "gysin_sequence",
})

ADAMS_SS_TAGS: frozenset[str] = frozenset({
    "adams_spectral_sequence",
    "adams_ss",
    "ext_steenrod",
    "steenrod_algebra",
    "stable_homotopy",
    "adams_resolution",
    "hopf_invariant",
    "p_local_homotopy",
})

EILENBERG_MOORE_SS_TAGS: frozenset[str] = frozenset({
    "eilenberg_moore_ss",
    "eilenberg_moore",
    "tor_functor_ss",
    "loop_space_ss",
    "bar_spectral_sequence",
    "cobar_spectral_sequence",
    "path_fibration_ss",
})

ATIYAH_HIRZEBRUCH_SS_TAGS: frozenset[str] = frozenset({
    "atiyah_hirzebruch_ss",
    "ahss",
    "k_theory_ss",
    "generalized_cohomology_ss",
    "chern_character_ss",
    "cobordism_ss",
    "elliptic_cohomology_ss",
})

LERAY_SS_TAGS: frozenset[str] = frozenset({
    "leray_ss",
    "leray_spectral_sequence",
    "leray_hirsch",
    "sheaf_cohomology_ss",
    "derived_functor_ss",
    "grothendieck_ss",
    "hypercohomology_ss",
})

CONVERGENCE_TAGS: frozenset[str] = frozenset({
    "strong_convergence",
    "conditional_convergence",
    "e_infinity_page",
    "filtration_ss",
    "associated_graded",
    "ss_convergence",
    "first_quadrant_ss",
})

DIFFERENTIAL_TAGS: frozenset[str] = frozenset({
    "differential_d_r",
    "differentials_ss",
    "d2_differential",
    "d3_differential",
    "transgression",
    "steenrod_operations_ss",
    "massey_products",
})

FILTRATION_TAGS: frozenset[str] = frozenset({
    "filtration",
    "decreasing_filtration",
    "hausdorff_filtration",
    "complete_filtration",
    "bockstein_ss",
    "mayer_vietoris_ss",
    "long_exact_sequence_ss",
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

def get_named_spectral_sequence_profiles() -> tuple[SpectralSequenceProfile, ...]:
    """Return the registry of canonical spectral sequence examples."""
    return (
        SpectralSequenceProfile(
            key="serre_fibration_ss",
            display_name="Serre spectral sequence for fibrations — E_2 = H^p(B; H^q(F)) => H^*(E)",
            sequence_type="serre",
            cohomology_type="singular",
            converges_to="H*(total_space)",
            is_multiplicative=True,
            is_first_quadrant=True,
            collapses_at_e2=False,
            is_conditionally_convergent=False,
            presentation_layer="main_text",
            focus=(
                "The Serre spectral sequence is a first-quadrant spectral sequence of algebras "
                "associated to a fibration F -> E -> B with B simply connected. "
                "The E_2 page is E_2^{p,q} = H^p(B; H^q(F)) (singular cohomology of B "
                "with local coefficients in the fiber cohomology H^q(F)), and the "
                "sequence converges strongly to H^{p+q}(E) via the filtration "
                "F^p H^n(E) = ker(H^n(E) -> H^n(E^{(p-1)})) where E^{(p)} is the p-th "
                "stage of the CW-filtration of B pulled back to E. "
                "The differentials d_r: E_r^{p,q} -> E_r^{p+r,q-r+1} decrease total "
                "degree |d_r| = 1; key differentials are d_2 (often zero for simple "
                "fibrations) and the transgression tau = d_r for the appropriate r. "
                "Edge homomorphisms: the base edge map H^p(B) = E_2^{p,0} -> E_infty^{p,0} "
                "-> H^p(E) and the fiber edge map H^n(E) -> E_infty^{0,n} -> E_2^{0,n} = H^n(F) "
                "are natural and coincide with the maps induced by i: F -> E and pi: E -> B. "
                "The Gysin sequence for a sphere bundle S^k -> E -> B arises from the "
                "Serre SS when H^*(S^k) = Z[0] + Z[k]: the only nonzero differential is "
                "d_{k+1} = cup product with the Euler class e in H^{k+1}(B), giving "
                "... -> H^n(B) -e-> H^{n+k+1}(B) -> H^{n+k+1}(E) -> H^{n+1}(B) -> ... "
                "The path-loop fibration Omega X -> PX -> X (PX contractible) gives "
                "E_2^{p,q} = H^p(X; H^q(Omega X)) abutting to Z in degree 0, "
                "allowing inductive computation of H^*(Omega X) via transgression. "
                "Example: H^*(Omega S^{n+1}) = Z[x] with |x| = n for n odd, "
                "= Z{1, x, x^2, ...} with |x^k| = kn for n even."
            ),
            chapter_targets=("30", "42", "58"),
        ),
        SpectralSequenceProfile(
            key="adams_ss_stable_homotopy",
            display_name="Adams spectral sequence — E_2 = Ext_A(H^*(X), F_p) => pi_*^s(X)_p",
            sequence_type="adams",
            cohomology_type="singular",
            converges_to="pi_*^s(S^0)_p",
            is_multiplicative=True,
            is_first_quadrant=True,
            collapses_at_e2=False,
            is_conditionally_convergent=True,
            presentation_layer="main_text",
            focus=(
                "The Adams spectral sequence (Adams 1958) is the fundamental computational "
                "tool for p-local stable homotopy theory. For a p-local spectrum X with "
                "H^*(X; F_p) a finitely generated A-module (A = Steenrod algebra), "
                "the E_2 page is E_2^{s,t} = Ext^{s,t}_A(H^*(X; F_p), F_p) where "
                "Ext is computed over the Steenrod algebra A = H^*(H F_p; F_p). "
                "The spectral sequence converges conditionally to pi_{t-s}(X)_p^hat "
                "(p-completed stable homotopy groups). For X = S^0, this gives "
                "E_2^{s,t} = Ext^{s,t}_A(F_p, F_p) => pi_{t-s}^s(S^0)_p. "
                "The Adams resolution: an A-free resolution 0 -> F_p -> K^0 -> K^1 -> ... "
                "of F_p = H^*(S^0; F_p) gives the E_1 = Hom_A(K^*, F_p) with "
                "d_1 induced by the boundary maps; E_2 = H(E_1, d_1) = Ext_A(F_p, F_p). "
                "The E_2-chart at p=2 in stem-filtration coordinates (t-s, s): "
                "s=1: h_0 (eta), h_1 (nu at stem 3), h_2 (sigma at stem 7), h_3 (at 15). "
                "Hopf invariant one theorem (Adams): the elements h_j in Ext^{1,2^j}_A "
                "correspond to hypothetical maps S^{2^j-1} -> S^0 of Hopf invariant one; "
                "Adams proved only h_1 (j=1, dim 1), h_2 (j=2, dim 3), h_3 (j=3, dim 7) "
                "survive, corresponding to multiplication by complex numbers, quaternions, "
                "and octonions. The rho, nu, sigma generators correspond to the Hopf "
                "fibrations S^1->S^2, S^3->S^4, S^7->S^8. Conditional convergence: "
                "the Adams SS converges conditionally; strong convergence requires "
                "lim^1 term vanishing, which holds for finite spectra."
            ),
            chapter_targets=("30", "42", "58"),
        ),
        SpectralSequenceProfile(
            key="eilenberg_moore_ss",
            display_name="Eilenberg-Moore spectral sequence — E_2 = Tor_{H^*(B)} => H^*(fiber product)",
            sequence_type="eilenberg_moore",
            cohomology_type="singular",
            converges_to="H*(fiber_product)",
            is_multiplicative=True,
            is_first_quadrant=False,
            collapses_at_e2=False,
            is_conditionally_convergent=True,
            presentation_layer="main_text",
            focus=(
                "The Eilenberg-Moore spectral sequence (EMSS) applies to the homotopy pullback "
                "X = E x_B PB in the diagram E -> B <- PB (path fibration PB -> B). "
                "When B is simply connected, the EMSS has "
                "E_2^{-s,t} = Tor^{-s,t}_{H^*(B;k)}(H^*(E;k), k) converging to H^*(X;k). "
                "Here Tor is the graded Tor functor computed via the bar construction "
                "B(H^*(B), H^*(E), k): E_1 = B(H^*(B), H^*(E), k) with bar differential. "
                "The EMSS is a second-quadrant spectral sequence (E_r^{p,q} potentially nonzero "
                "for p <= 0 and q >= 0), making it conditionally convergent in general. "
                "Special case — loop space: for E = {b_0}, X = Omega B; "
                "E_2 = Tor_{H^*(B)}(k, k) => H^*(Omega B). "
                "Example: H^*(Omega S^n; F_p) for p odd: Tor_{H^*(S^n; F_p)}(F_p, F_p) "
                "= F_p[x] with |x| = n-1 (exterior algebra for n even). "
                "The bar construction model: the EMSS arises from filtering the bar complex "
                "B(C^*(B); C^*(E)) by bar length; the E_1-page is the bar complex itself "
                "and E_2 = Tor. The cobar construction gives the Adams spectral sequence. "
                "Multiplicative structure: the EMSS is a spectral sequence of algebras when "
                "the fibration is orientable; the algebra structure on E_2 comes from "
                "the multiplicative structure of Tor (the shuffle product on the bar complex). "
                "Applications: computing H^*(Omega X) for H-spaces and co-H-spaces, "
                "cohomology of homogeneous spaces G/H via H^*(G) and H^*(H), "
                "and string topology via the EMSS for the free loop space LX."
            ),
            chapter_targets=("30", "42", "58"),
        ),
        SpectralSequenceProfile(
            key="atiyah_hirzebruch_ss",
            display_name="Atiyah-Hirzebruch SS — E_2 = H^p(X; h^q(pt)) => h^{p+q}(X)",
            sequence_type="atiyah_hirzebruch",
            cohomology_type="k_theory",
            converges_to="K*(X)",
            is_multiplicative=True,
            is_first_quadrant=True,
            collapses_at_e2=False,
            is_conditionally_convergent=False,
            presentation_layer="main_text",
            focus=(
                "The Atiyah-Hirzebruch spectral sequence (AHSS) converts singular cohomology "
                "computations into computations in a generalized cohomology theory h^*. "
                "For a CW-complex X and a multiplicative cohomology theory h^*, the AHSS "
                "has E_2^{p,q} = H^p(X; h^q(pt)) converging strongly (first-quadrant SS) "
                "to h^{p+q}(X). The filtration: F^p h^n(X) = ker(h^n(X) -> h^n(X^{(p-1)})) "
                "where X^{(k)} is the k-skeleton of X. "
                "For h^* = K^* (complex K-theory): K^0(pt) = Z, K^1(pt) = 0 (Bott periodicity "
                "K^{n+2}(pt) = K^n(pt)), so E_2^{p,q} = H^p(X; Z) for q even, 0 for q odd, "
                "converging to K^{p+q}(X) = K^0(X) for p+q even, K^1(X) for p+q odd. "
                "The first potentially non-trivial differential: d_3 = Sq^3 (the composition "
                "of Sq^2 with the Bockstein beta: d_3 = beta Sq^2 in the K-theory AHSS). "
                "For CP^n: all differentials vanish (E_r^{p,q} = 0 unless p even, q = 0; "
                "no room for nonzero d_r), so K^*(CP^n) = Z^{n+1} in degree 0, 0 in degree 1. "
                "Chern character: ch: K^0(X) tensor Q -> H^{ev}(X; Q) is an isomorphism "
                "compatible with the AHSS and its rational degeneration. "
                "For h^* = MU^* (complex cobordism): E_2^{p,q} = H^p(X; MU^q(pt)) => MU^{p+q}(X); "
                "MU^*(pt) = Z[x_1, x_2, ...] (Milnor's complex bordism ring, |x_i| = 2i). "
                "Elliptic cohomology and tmf: the AHSS for tmf (topological modular forms) "
                "has E_2^{p,q} = H^p(X; pi_q(tmf)) and gives powerful new invariants."
            ),
            chapter_targets=("30", "42", "58"),
        ),
        SpectralSequenceProfile(
            key="leray_hirsch_theorem",
            display_name="Leray-Hirsch — H*(E) = H*(B) tensor H*(F), Serre SS collapses at E_2",
            sequence_type="leray",
            cohomology_type="singular",
            converges_to="H*(total_space)",
            is_multiplicative=True,
            is_first_quadrant=True,
            collapses_at_e2=True,
            is_conditionally_convergent=False,
            presentation_layer="main_text",
            focus=(
                "The Leray-Hirsch theorem gives a powerful sufficient condition for the "
                "Serre spectral sequence to collapse at the E_2 page. Statement: for a "
                "fibration F -> E -> B with B path-connected and H^*(F; k) a free k-module, "
                "if there exist classes c_1, ..., c_n in H^*(E; k) such that their restrictions "
                "i^*(c_j) = e_j form a k-basis of H^*(F; k) at every fiber (the global "
                "sections condition), then H^*(E; k) = H^*(B; k) tensor_k H^*(F; k) as "
                "H^*(B; k)-modules via the map H^*(B) tensor H^*(F) -> H^*(E), "
                "b tensor e_j |-> pi^*(b) cup c_j. The Serre SS collapses: all "
                "differentials d_r = 0 for r >= 2, so E_infty = E_2 = H^*(B) tensor H^*(F). "
                "Consequence: Kunneth formula for fibrations. "
                "Examples of Leray-Hirsch fibrations: "
                "(1) Trivial fibrations F x B -> B: obviously H^*(F x B) = H^*(B) tensor H^*(F). "
                "(2) Principal G-bundles G -> EG -> BG when H^*(G) has exterior generators "
                "detected by universal characteristic classes (e.g., U(n) bundles over "
                "simply connected 4-manifolds). "
                "(3) Flag variety fibrations GL_n/B -> GL_n/P for parabolic subgroups P. "
                "(4) The Hopf bundle S^3 -> S^7 -> S^4 does NOT satisfy Leray-Hirsch "
                "(H^*(S^3) is not globally realized in H^*(S^7)). "
                "Proof: define phi: H^*(B) tensor H^*(F) -> H^*(E) by phi(b tensor e_j) = "
                "pi^*(b) cup c_j; show phi is an isomorphism by induction on skeleta "
                "using the Serre SS and the five-lemma. "
                "Leray's original theorem (1945): in the language of sheaf cohomology, "
                "if f: X -> Y is a map with R^q f_*(F) locally free for all q, then the "
                "Leray spectral sequence collapses to give H^n(X; F) = direct_sum_{p+q=n} "
                "H^p(Y; R^q f_*(F)) (under additional acyclicity conditions on the fibers)."
            ),
            chapter_targets=("30", "42", "58"),
        ),
        SpectralSequenceProfile(
            key="lhs_group_extension",
            display_name="Lyndon-Hochschild-Serre SS — 1->N->G->Q->1, E_2=H^p(Q;H^q(N;M))=>H^*(G;M)",
            sequence_type="lyndon_hochschild_serre",
            cohomology_type="group",
            converges_to="H*(G;M)",
            is_multiplicative=True,
            is_first_quadrant=True,
            collapses_at_e2=False,
            is_conditionally_convergent=False,
            presentation_layer="main_text",
            focus=(
                "The Lyndon-Hochschild-Serre (LHS) spectral sequence is the group-theoretic "
                "analogue of the Serre spectral sequence for group extensions. For a group "
                "extension 1 -> N -> G -> Q -> 1 and a G-module M, the LHS SS has "
                "E_2^{p,q} = H^p(Q; H^q(N; M)) converging strongly to H^{p+q}(G; M). "
                "Here H^q(N; M) is equipped with the Q-module structure via the conjugation "
                "action of G on N. "
                "Construction: the LHS SS arises from filtering the bar resolution of G "
                "by the normal subgroup N; equivalently, it is the Serre SS for the "
                "homotopy fibration BN -> BG -> BQ. "
                "The 5-term exact sequence (from low-degree terms of the LHS SS): "
                "0 -> H^1(Q; M^N) -> H^1(G; M) -> H^1(N; M)^Q -> H^2(Q; M^N) -> H^2(G; M) "
                "where M^N = {m in M : nm = m for all n in N} is the invariant submodule. "
                "Inflation-restriction: the map H^1(Q; M^N) -> H^1(G; M) is the inflation "
                "inf^*: H^*(Q; -) -> H^*(G; -) induced by G -> Q; the map H^1(G; M) -> H^1(N; M)^Q "
                "is the restriction res^*: H^*(G; -) -> H^*(N; -)^Q. "
                "Applications: "
                "(1) Semidirect products G = N rtimes Q: H^*(G; M) computable from H^*(N; M) "
                "and H^*(Q; H^*(N; M)) via the LHS SS. "
                "(2) p-groups: the LHS SS for a central extension 1 -> Z/p -> G -> Z/p^{n-1} -> 1 "
                "computes H^*(G; Z/p) from H^*(Z/p; H^*(Z/p; Z/p)). "
                "(3) The Hochschild-Serre spectral sequence in Lie algebra cohomology: "
                "for a Lie algebra extension 0 -> n -> g -> q -> 0, the analogue gives "
                "E_2^{p,q} = H^p_Lie(q; H^q_Lie(n; M)) => H^{p+q}_Lie(g; M). "
                "Multiplicativity: the LHS SS is a spectral sequence of graded-commutative "
                "algebras (using the cup product in group cohomology), and the convergence "
                "is compatible with the algebra structure."
            ),
            chapter_targets=("30", "42", "58"),
        ),
        SpectralSequenceProfile(
            key="bockstein_ss",
            display_name="Bockstein spectral sequence — differential = beta, p-torsion detection",
            sequence_type="bockstein",
            cohomology_type="singular",
            converges_to="H*(X;Z)",
            is_multiplicative=False,
            is_first_quadrant=True,
            collapses_at_e2=True,
            is_conditionally_convergent=False,
            presentation_layer="main_text",
            focus=(
                "The Bockstein spectral sequence arises from the short exact sequence "
                "of coefficient groups 0 -> Z -p-> Z -> Z/p -> 0 (multiplication by p). "
                "Applying cohomology gives the long exact sequence "
                "... -> H^n(X; Z) -p-> H^n(X; Z) -> H^n(X; Z/p) -beta-> H^{n+1}(X; Z) -> ... "
                "where beta = the Bockstein homomorphism (connecting homomorphism). "
                "The Bockstein SS has E_1 = H^*(X; Z/p) with d_1 = beta (the Bockstein "
                "operation: beta: H^n(X; Z/p) -> H^{n+1}(X; Z/p) is the composition of "
                "the connecting homomorphism with the mod-p reduction). "
                "E_2 = H(H^*(X; Z/p), beta) = ker(beta) / im(beta). "
                "The spectral sequence converges to (H^*(X; Z) / torsion) tensor Z/p, "
                "detecting precisely the p-torsion-free part of H^*(X; Z). "
                "Collapse at E_2: the Bockstein SS collapses at E_2 (meaning E_2 = E_infty) "
                "if and only if H^*(X; Z) has no p-torsion. "
                "p-torsion detection: the rank of E_infty^n = rank(H^n(X; Z/p) after "
                "quotienting by beta-exact classes) equals the rank of the free part of H^n(X; Z). "
                "The difference rank(H^n(X; Z/p)) - rank(E_infty^n) measures the amount "
                "of p-torsion in H^*(X; Z). "
                "Examples: for X = RP^infty, H^*(RP^infty; Z/2) = Z/2[x] with |x|=1 and "
                "beta = 0 (since H^*(RP^infty; Z) = Z[y]/(2y) has 2-torsion in every degree), "
                "so E_infty = 0 except in degree 0. "
                "Steenrod operations: the Bockstein beta at p=2 is Sq^1; at odd p, "
                "beta is the p-th Bockstein. The relation Sq^1 Sq^{2k} = Sq^{2k+1} "
                "reflects the interaction of the Bockstein with Steenrod squares."
            ),
            chapter_targets=("30", "42", "58"),
        ),
        SpectralSequenceProfile(
            key="grothendieck_ss",
            display_name="Grothendieck SS — E_2=R^pF(R^qG(A))=>R^{p+q}(FG)(A), derived functors",
            sequence_type="leray",
            cohomology_type="general",
            converges_to="R(FG)(A)",
            is_multiplicative=False,
            is_first_quadrant=True,
            collapses_at_e2=False,
            is_conditionally_convergent=False,
            presentation_layer="main_text",
            focus=(
                "The Grothendieck spectral sequence is the fundamental tool for computing "
                "derived functors of compositions. For left-exact functors F: B -> C and "
                "G: A -> B between abelian categories (with A, B having enough injectives "
                "and G taking injective objects of A to F-acyclic objects of B), the "
                "Grothendieck SS has E_2^{p,q} = (R^p F)(R^q G)(A) converging to "
                "R^{p+q}(FG)(A) (the derived functors of the composition FG). "
                "Proof sketch: take an injective resolution I^* of A in A; apply G to "
                "get G(I^*) (not injective in B in general); take an injective resolution "
                "J^{**} of G(I^*); apply F to the double complex F(J^{**}) and take "
                "the two spectral sequences of the resulting double complex. "
                "Special cases (the Leray spectral sequence): for a continuous map "
                "f: X -> Y of topological spaces and a sheaf F on X, take G = f_* "
                "(direct image) and F = Gamma(Y, -) (global sections). Then "
                "R^q G(F) = R^q f_*(F) (higher direct images) and R^p F(R^q f_*(F)) = "
                "H^p(Y; R^q f_*(F)), giving E_2^{p,q} = H^p(Y; R^q f_*(F)) => H^{p+q}(X; F). "
                "Other special cases: "
                "(1) Hochschild-Serre (group cohomology): G = (-)^N (N-invariants), F = (-)^Q; "
                "    E_2^{p,q} = H^p(Q; H^q(N; M)) => H^{p+q}(G; M). "
                "(2) Lyndon's SS for profinite groups: same as LHS for pro-finite extensions. "
                "(3) Local-to-global Ext: E_2^{p,q} = H^p(X; Ext^q(F, G)) => Ext^{p+q}(F, G). "
                "(4) Hypercohomology: for a complex of sheaves F^*, "
                "    E_2^{p,q} = H^p(X; H^q(F^*)) => H^{p+q}(X; F^*). "
                "The Grothendieck SS is first-quadrant (E_2^{p,q} = 0 for p < 0 or q < 0 "
                "since R^p F = 0 for p < 0) and converges strongly. The associated "
                "5-term exact sequence: 0 -> R^1F(GA) -> R^1(FG)(A) -> F(R^1 G(A)) -> "
                "R^2 F(GA) -> R^2(FG)(A) is the edge-homomorphism exact sequence."
            ),
            chapter_targets=("30", "42", "58"),
        ),
    )


# ---------------------------------------------------------------------------
# Summary / index functions
# ---------------------------------------------------------------------------

def spectral_sequence_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_spectral_sequence_profiles()
    ))


def spectral_sequence_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_spectral_sequence_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {ch: tuple(keys) for ch, keys in sorted(chapter_map.items())}


def spectral_sequence_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from sequence_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_spectral_sequence_profiles():
        index.setdefault(p.sequence_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_multiplicative_spectral_sequence(space: Any) -> Result:
    """Check whether the spectral sequence is multiplicative.

    A multiplicative spectral sequence is a spectral sequence of algebras:
    each E_r^{*,*} is a bigraded algebra, the differentials d_r are derivations
    (d_r(xy) = d_r(x)y + (-1)^{|x|} x d_r(y)), and the product on E_{r+1} is
    induced from that on E_r via the isomorphism E_{r+1} = H(E_r, d_r).
    Examples: Serre, Adams, AHSS, Leray-Hirsch spectral sequences.

    Decision layers
    ---------------
    1. Explicit multiplicative tags or Serre/Adams tags -> true.
    2. AHSS or Leray SS tags -> true (both are multiplicative).
    3. Known non-multiplicative spectral sequences (Bockstein, explicit tags) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    multiplicative_explicit = {"multiplicative_ss", "spectral_sequence_of_algebras"}
    if _matches_any(tags, multiplicative_explicit | SERRE_SS_TAGS | ADAMS_SS_TAGS):
        witness = next(t for t in tags if t in (multiplicative_explicit | SERRE_SS_TAGS | ADAMS_SS_TAGS))
        return Result.true(
            mode="theorem",
            value="multiplicative_ss",
            justification=[
                f"Tag {witness!r}: the Serre and Adams spectral sequences are multiplicative — "
                "each page E_r is a bigraded algebra and the differentials are derivations "
                "satisfying d_r(xy) = d_r(x)y + (-1)^{|x|} x d_r(y). "
                "The product on E_{r+1} = H(E_r, d_r) is induced from E_r.",
            ],
            metadata={**base, "criterion": "explicit_multiplicative_or_serre_adams", "witness": witness},
        )

    leray_ahss = ATIYAH_HIRZEBRUCH_SS_TAGS | LERAY_SS_TAGS
    if _matches_any(tags, leray_ahss):
        witness = next(t for t in tags if t in leray_ahss)
        return Result.true(
            mode="theorem",
            value="multiplicative_ss",
            justification=[
                f"Tag {witness!r}: the Atiyah-Hirzebruch and Leray spectral sequences "
                "are multiplicative spectral sequences of algebras. The AHSS respects "
                "the ring structure of h^*, and the Leray SS is multiplicative for "
                "the cup product on sheaf cohomology.",
            ],
            metadata={**base, "criterion": "ahss_or_leray_multiplicative", "witness": witness},
        )

    non_multiplicative = {"bockstein_ss", "non_multiplicative_ss", "not_multiplicative_ss"}
    if _matches_any(tags, non_multiplicative):
        witness = next(t for t in tags if t in non_multiplicative)
        return Result.false(
            mode="theorem",
            value="not_multiplicative_ss",
            justification=[
                f"Tag {witness!r}: the spectral sequence is not multiplicative. "
                "The Bockstein spectral sequence, for example, does not carry a natural "
                "multiplicative structure compatible with the differentials.",
            ],
            metadata={**base, "criterion": "explicit_non_multiplicative", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate multiplicativity or its failure for this spectral sequence. "
            "Cannot determine whether the spectral sequence is multiplicative.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def converges_strongly(space: Any) -> Result:
    """Check whether the spectral sequence converges strongly.

    Strong convergence E_r => H^n means: for all (p,q), d_r^{p,q} = 0 for r >> 0
    (the pages stabilize to E_infty^{p,q}), and H^n admits a complete Hausdorff
    filtration with gr^p H^{p+q} = E_infty^{p,q}. First-quadrant spectral sequences
    always converge strongly.

    Decision layers
    ---------------
    1. Explicit strong convergence or first_quadrant_ss tags -> true.
    2. Known strongly convergent types by tag (Serre, AHSS, Leray, LHS) -> true.
    3. Known conditionally (not strongly) convergent (Adams, EM) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    strong_explicit = {"strong_convergence", "first_quadrant_ss"}
    if _matches_any(tags, strong_explicit):
        witness = next(t for t in tags if t in strong_explicit)
        return Result.true(
            mode="theorem",
            value="strongly_convergent",
            justification=[
                f"Tag {witness!r}: the spectral sequence converges strongly — "
                "E_infty^{p,q} = gr^p H^{p+q} with a complete Hausdorff filtration. "
                "First-quadrant spectral sequences converge strongly when the pages stabilize.",
            ],
            metadata={**base, "criterion": "explicit_strong_convergence", "witness": witness},
        )

    first_quadrant_types = SERRE_SS_TAGS | ATIYAH_HIRZEBRUCH_SS_TAGS | LERAY_SS_TAGS
    lhs_tags = {"lyndon_hochschild_serre", "lhs_ss", "lhs_group_extension",
                "group_extension_ss", "inflation_restriction"}
    strongly_convergent = first_quadrant_types | lhs_tags
    if _matches_any(tags, strongly_convergent):
        witness = next(t for t in tags if t in strongly_convergent)
        return Result.true(
            mode="theorem",
            value="strongly_convergent",
            justification=[
                f"Tag {witness!r}: the Serre, Atiyah-Hirzebruch, Leray, and LHS spectral "
                "sequences are all first-quadrant spectral sequences and hence converge "
                "strongly. The E_infty page is the associated graded of the filtration "
                "on the abutment.",
            ],
            metadata={**base, "criterion": "first_quadrant_type_strongly_convergent", "witness": witness},
        )

    conditional_tags = {"conditional_convergence", "conditionally_convergent"}
    adams_em_tags = ADAMS_SS_TAGS | EILENBERG_MOORE_SS_TAGS
    not_strong = conditional_tags | adams_em_tags
    if _matches_any(tags, not_strong):
        witness = next(t for t in tags if t in not_strong)
        return Result.false(
            mode="theorem",
            value="not_strongly_convergent",
            justification=[
                f"Tag {witness!r}: the spectral sequence is conditionally convergent "
                "but not necessarily strongly convergent. The Adams SS and EM SS are "
                "conditionally convergent; strong convergence requires additional "
                "conditions (lim^1 vanishing for Adams, bounded-below filtration for EM).",
            ],
            metadata={**base, "criterion": "conditionally_not_strongly_convergent", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate strong convergence or its failure. "
            "Cannot determine whether the spectral sequence converges strongly.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def has_collapse_at_e2(space: Any) -> Result:
    """Check whether the spectral sequence collapses at the E_2 page.

    A spectral sequence collapses at E_2 if all differentials d_r = 0 for r >= 2,
    so E_infty = E_2. This gives a direct formula H^n = direct_sum_{p+q=n} E_2^{p,q}
    (no extension problems), and for multiplicative SS it means H^*(E) = H^*(B) tensor H^*(F).
    The Leray-Hirsch theorem gives a sufficient condition for collapse.

    Decision layers
    ---------------
    1. Explicit collapse tags (collapses_at_e2, e2_degeneration) -> true.
    2. Leray-Hirsch type tags (leray_hirsch, trivial_fibration) -> true.
    3. Known non-collapsing types (d3_differential, Adams, EM) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    collapse_explicit = {"collapses_at_e2", "e2_degeneration", "e2_collapse",
                         "e2_page_collapses", "ss_degenerates_at_e2"}
    if _matches_any(tags, collapse_explicit):
        witness = next(t for t in tags if t in collapse_explicit)
        return Result.true(
            mode="theorem",
            value="collapses_at_e2",
            justification=[
                f"Tag {witness!r}: all differentials d_r = 0 for r >= 2, so E_infty = E_2. "
                "This gives a direct computation of H^n as a direct sum of E_2^{p,q}. "
                "For multiplicative SS this means H^*(E) = H^*(B) tensor H^*(F).",
            ],
            metadata={**base, "criterion": "explicit_e2_collapse", "witness": witness},
        )

    leray_hirsch_tags = {"leray_hirsch", "trivial_fibration", "product_fibration",
                         "global_sections_fiber", "bockstein_ss"}
    if _matches_any(tags, leray_hirsch_tags | LERAY_SS_TAGS):
        candidate_tags = leray_hirsch_tags | LERAY_SS_TAGS
        witness = next(t for t in tags if t in candidate_tags)
        return Result.true(
            mode="theorem",
            value="collapses_at_e2",
            justification=[
                f"Tag {witness!r}: the Leray-Hirsch theorem guarantees collapse at E_2. "
                "When H^*(F; k) is free and globally realized in H^*(E; k), all "
                "differentials vanish and E_infty = E_2 = H^*(B) tensor H^*(F). "
                "The Bockstein SS also collapses at E_2 when H^*(X; Z) has no p-torsion.",
            ],
            metadata={**base, "criterion": "leray_hirsch_collapse", "witness": witness},
        )

    non_collapse = {"d3_differential", "non_trivial_differential", "does_not_collapse"}
    if _matches_any(tags, non_collapse | ADAMS_SS_TAGS | EILENBERG_MOORE_SS_TAGS):
        candidate_tags = non_collapse | ADAMS_SS_TAGS | EILENBERG_MOORE_SS_TAGS
        witness = next(t for t in tags if t in candidate_tags)
        return Result.false(
            mode="theorem",
            value="does_not_collapse_at_e2",
            justification=[
                f"Tag {witness!r}: the spectral sequence does not collapse at E_2. "
                "The Adams SS has nontrivial higher differentials (d_2, d_3, ...) "
                "detected by secondary and higher cohomology operations. "
                "The EM SS also has nontrivial differentials in general. "
                "A d_3 differential is present in the AHSS for K-theory (d_3 = Sq^3).",
            ],
            metadata={**base, "criterion": "explicit_non_collapse", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate whether the spectral sequence collapses at E_2. "
            "Cannot determine collapse without more information.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def is_first_quadrant_spectral_sequence(space: Any) -> Result:
    """Check whether the spectral sequence is a first-quadrant spectral sequence.

    A first-quadrant SS has E_r^{p,q} = 0 for p < 0 or q < 0. These always converge
    strongly and have finite E_infty pages in each total degree. Examples: Serre,
    AHSS, Leray, LHS, Grothendieck. The Adams and EM spectral sequences occupy
    the upper half-plane or second quadrant respectively.

    Decision layers
    ---------------
    1. Explicit first_quadrant_ss tag or CONVERGENCE_TAGS -> true.
    2. Known first-quadrant types (Serre, AHSS, Leray, LHS tags) -> true.
    3. Known non-first-quadrant (Adams upper half, EM second quadrant) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    fq_explicit = {"first_quadrant_ss", "strong_convergence"}
    if _matches_any(tags, fq_explicit):
        witness = next(t for t in tags if t in fq_explicit)
        return Result.true(
            mode="theorem",
            value="first_quadrant_ss",
            justification=[
                f"Tag {witness!r}: the spectral sequence is first-quadrant — "
                "E_r^{p,q} = 0 for p < 0 or q < 0. This guarantees strong convergence "
                "and finiteness of the computation in each total degree.",
            ],
            metadata={**base, "criterion": "explicit_first_quadrant", "witness": witness},
        )

    fq_types = SERRE_SS_TAGS | ATIYAH_HIRZEBRUCH_SS_TAGS
    lhs_tags = {"lyndon_hochschild_serre", "lhs_ss", "lhs_group_extension",
                "group_extension_ss", "inflation_restriction",
                "grothendieck_ss", "leray_spectral_sequence", "leray_ss"}
    if _matches_any(tags, fq_types | lhs_tags):
        candidate_tags = fq_types | lhs_tags
        witness = next(t for t in tags if t in candidate_tags)
        return Result.true(
            mode="theorem",
            value="first_quadrant_ss",
            justification=[
                f"Tag {witness!r}: the Serre, AHSS, Leray, LHS, and Grothendieck "
                "spectral sequences are all first-quadrant spectral sequences "
                "(E_2^{p,q} = 0 for p < 0 or q < 0). They converge strongly.",
            ],
            metadata={**base, "criterion": "known_first_quadrant_type", "witness": witness},
        )

    non_fq = ADAMS_SS_TAGS | EILENBERG_MOORE_SS_TAGS
    if _matches_any(tags, non_fq):
        witness = next(t for t in tags if t in non_fq)
        return Result.false(
            mode="theorem",
            value="not_first_quadrant_ss",
            justification=[
                f"Tag {witness!r}: the Adams spectral sequence occupies the upper "
                "half-plane (s >= 0, t-s arbitrary) and is not strictly first-quadrant. "
                "The Eilenberg-Moore SS occupies the second quadrant (p <= 0, q >= 0). "
                "Neither is a first-quadrant spectral sequence.",
            ],
            metadata={**base, "criterion": "adams_or_em_not_first_quadrant", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate whether the spectral sequence is first-quadrant. "
            "Cannot determine without more information about the E_2 page support.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


# ---------------------------------------------------------------------------
# Facade functions
# ---------------------------------------------------------------------------

def classify_spectral_sequence(space: Any) -> dict[str, Any]:
    """Run all spectral sequence analysis functions and return a combined result dict."""
    return {
        "is_multiplicative_spectral_sequence": is_multiplicative_spectral_sequence(space),
        "converges_strongly":                  converges_strongly(space),
        "has_collapse_at_e2":                  has_collapse_at_e2(space),
        "is_first_quadrant_spectral_sequence": is_first_quadrant_spectral_sequence(space),
    }


def spectral_sequence_profile(space: Any) -> dict[str, Any]:
    """Return a comprehensive spectral sequence profile of the space."""
    classification = classify_spectral_sequence(space)
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
    "SpectralSequenceProfile",
    "SERRE_SS_TAGS",
    "ADAMS_SS_TAGS",
    "EILENBERG_MOORE_SS_TAGS",
    "ATIYAH_HIRZEBRUCH_SS_TAGS",
    "LERAY_SS_TAGS",
    "CONVERGENCE_TAGS",
    "DIFFERENTIAL_TAGS",
    "FILTRATION_TAGS",
    "get_named_spectral_sequence_profiles",
    "spectral_sequence_layer_summary",
    "spectral_sequence_chapter_index",
    "spectral_sequence_type_index",
    "is_multiplicative_spectral_sequence",
    "converges_strongly",
    "has_collapse_at_e2",
    "is_first_quadrant_spectral_sequence",
    "classify_spectral_sequence",
    "spectral_sequence_profile",
    # P7.4 computational objects
    "SpectralPage",
    "FilteredChainComplex",
    "filtered_chain_complex_from_simplices",
    "differential_d_r",
    "converges_to",
]


# ===========================================================================
# P7.4: Computational spectral sequence from filtered chain complexes
# ===========================================================================
#
# Mathematical background
# -----------------------
# A filtration of a chain complex (C_*, ∂) is a decreasing sequence of
# subcomplexes F^p C_* with ∩F^p = 0 and ∪F^p = C_*.
#
# The associated spectral sequence {E^r_{p,q}, d^r} satisfies:
#   E^1_{p,q} = H_{p+q}(F^p C / F^{p+1} C)   (associated-graded homology)
#   d^r : E^r_{p,q} → E^r_{p−r, q+r−1}        (bidegree (−r, r−1))
#   E^{r+1}_{p,q} = ker(d^r_{p,q}) / im(d^r_{p+r, q−r+1})
#   E^∞_{p,q}  ≅ Gr^p H_{p+q}(C_*)            (associated graded of total homology)
#
# For the Künneth / product filtration the sequence degenerates at E^2.

from dataclasses import dataclass as _dataclass  # noqa: E402

_Matrix = list[list[int]]


@_dataclass
class SpectralPage:
    """A single E^r page of a bigraded spectral sequence.

    Entries E^r_{p,q} are finitely generated abelian groups stored as
    (betti, torsion) pairs where ``betti`` is the free rank and ``torsion``
    is a tuple of invariant factors > 1.

    Attributes
    ----------
    page_number : int
        The page index r (r ≥ 1).
    groups : dict[tuple[int,int], tuple[int, tuple[int,...]]]
        Maps ``(p, q)`` → ``(betti, torsion)``.  Missing entries = zero group.
    max_p : int
        Largest filtration degree p with a nonzero entry (for display).
    max_total : int
        Largest total degree n = p + q with a nonzero entry.
    """

    page_number: int
    groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]]
    max_p: int = 0
    max_total: int = 0

    def get(self, p: int, q: int) -> tuple[int, tuple[int, ...]]:
        """Return E^r_{p,q} as (betti, torsion), defaulting to (0, ())."""
        return self.groups.get((p, q), (0, ()))

    def betti(self, p: int, q: int) -> int:
        """Free rank of E^r_{p,q}."""
        return self.get(p, q)[0]

    def torsion(self, p: int, q: int) -> tuple[int, ...]:
        """Torsion invariant factors of E^r_{p,q}."""
        return self.get(p, q)[1]

    def total_rank(self, n: int) -> int:
        """Sum of Betti numbers ⊕_{p+q=n} E^r_{p,q}."""
        return sum(self.get(p, n - p)[0] for p in range(n + 1))

    def is_zero(self) -> bool:
        """True if all entries are the zero group."""
        return all(b == 0 and not t for b, t in self.groups.values())

    def nonzero_positions(self) -> list[tuple[int, int]]:
        """List of (p,q) positions with nonzero groups."""
        return [(p, q) for (p, q), (b, t) in self.groups.items() if b > 0 or t]


@_dataclass
class FilteredChainComplex:
    """A chain complex together with a filtration by integer degree.

    Attributes
    ----------
    num_degrees : int
        Homological degrees run from 0 to ``num_degrees − 1``.
    num_filtration : int
        Filtration levels 0, 1, …, ``num_filtration − 1``.
    generators : dict[int, list[tuple[int, int]]]
        Maps k → list of ``(filtration_p, local_index)`` for each C_k generator,
        sorted by filtration_p (non-decreasing).
    boundary : dict[int, _Matrix]
        Maps k → integer boundary matrix ∂_k: C_k → C_{k−1}.
        Rows indexed by (k−1)-generators, columns by k-generators in the same
        order as ``generators[k]``.
    """

    num_degrees: int
    num_filtration: int
    generators: dict[int, list[tuple[int, int]]]
    boundary: dict[int, _Matrix]


def filtered_chain_complex_from_simplices(
    simplices_by_degree: dict[int, list[tuple[int, tuple[int, ...]]]],
) -> FilteredChainComplex:
    """Build a FilteredChainComplex from explicitly graded simplices.

    Parameters
    ----------
    simplices_by_degree : dict
        Maps homological degree k → list of ``(filtration_p, simplex_vertices)``
        where ``simplex_vertices`` is a sorted tuple of non-negative integer
        vertex indices.  The list order within each degree defines the column
        order of the boundary matrix.

    Returns
    -------
    FilteredChainComplex
        With boundary matrices computed from the standard oriented simplicial
        boundary formula: ∂(v₀,…,vₖ) = Σᵢ (−1)ⁱ (v₀,…,v̂ᵢ,…,vₖ).

    Examples
    --------
    Build the filtered complex for the interval [0,1] with filtration 0:

    >>> fcc = filtered_chain_complex_from_simplices({
    ...     0: [(0, (0,)), (0, (1,))],
    ...     1: [(0, (0, 1))],
    ... })
    >>> fcc.num_degrees
    2
    """
    if not simplices_by_degree:
        return FilteredChainComplex(
            num_degrees=0, num_filtration=0, generators={}, boundary={}
        )

    all_k = sorted(simplices_by_degree.keys())
    max_k = max(all_k)
    max_filt = max(
        p for gens in simplices_by_degree.values() for p, _ in gens
    ) + 1

    generators: dict[int, list[tuple[int, int]]] = {}
    simplex_to_col: dict[int, dict[tuple[int, ...], int]] = {}

    for k in range(max_k + 1):
        raw = simplices_by_degree.get(k, [])
        generators[k] = [(p, i) for i, (p, _) in enumerate(raw)]
        simplex_to_col[k] = {vs: i for i, (_, vs) in enumerate(raw)}

    boundary: dict[int, _Matrix] = {}
    for k in range(1, max_k + 1):
        k_gens = simplices_by_degree.get(k, [])
        km1_idx = simplex_to_col.get(k - 1, {})
        n_k = len(k_gens)
        n_km1 = len(simplices_by_degree.get(k - 1, []))
        mat: _Matrix = [[0] * n_k for _ in range(n_km1)]
        for col, (_, sigma) in enumerate(k_gens):
            for i in range(len(sigma)):
                face = sigma[:i] + sigma[i + 1:]
                if face in km1_idx:
                    mat[km1_idx[face]][col] += (-1) ** i
        boundary[k] = mat

    return FilteredChainComplex(
        num_degrees=max_k + 1,
        num_filtration=max_filt,
        generators=generators,
        boundary=boundary,
    )


def _e1_page_from_fcc(fcc: FilteredChainComplex) -> SpectralPage:
    """Compute E^1 page: E^1_{p,q} = H_{p+q}(F^p C / F^{p+1} C).

    Restricts the boundary matrices to the filtration-p block and computes
    the homology of the associated graded complex via Smith Normal Form.
    """
    from .mayer_vietoris import _snf_ext

    groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
    max_p = 0
    max_total = 0

    for n in range(fcc.num_degrees):
        for p in range(fcc.num_filtration):
            q = n - p
            if q < 0:
                continue

            # Generators at filtration p in degree n (columns)
            cols_n = [
                i for (filt, i) in fcc.generators.get(n, []) if filt == p
            ]
            if not cols_n:
                continue

            # Rows: generators at filtration p in degree n−1
            rows_nm1 = [
                i for (filt, i) in fcc.generators.get(n - 1, []) if filt == p
            ] if n > 0 else []

            # Cols of degree n+1 generators at filtration p (incoming ∂_{n+1})
            cols_np1 = [
                i for (filt, i) in fcc.generators.get(n + 1, []) if filt == p
            ]

            # ∂_n restricted to filt=p block
            mat_n = fcc.boundary.get(n, [])
            if mat_n and rows_nm1:
                dn = [[mat_n[row][col] for col in cols_n] for row in rows_nm1]
            else:
                dn = []

            # ∂_{n+1} restricted to filt=p block (rows = cols_n, cols = cols_np1)
            mat_np1 = fcc.boundary.get(n + 1, [])
            if mat_np1 and cols_np1 and cols_n:
                dn1 = [[mat_np1[row][col] for col in cols_np1] for row in cols_n]
            else:
                dn1 = []

            def _rank(m: _Matrix) -> int:
                if not m or not m[0]:
                    return 0
                if not any(any(v != 0 for v in row) for row in m):
                    return 0
                D, _, _, _, _ = _snf_ext(m, compute_transforms=False)
                sz = min(len(D), len(D[0]) if D else 0)
                return sum(1 for i in range(sz) if i < len(D) and D[i][i] != 0)

            def _torsion(m: _Matrix) -> tuple[int, ...]:
                if not m or not m[0]:
                    return ()
                if not any(any(v != 0 for v in row) for row in m):
                    return ()
                D, _, _, _, _ = _snf_ext(m, compute_transforms=False)
                sz = min(len(D), len(D[0]) if D else 0)
                return tuple(
                    abs(D[i][i]) for i in range(sz)
                    if i < len(D) and abs(D[i][i]) > 1
                )

            rank_dn = _rank(dn)
            rank_dn1 = _rank(dn1)
            tors = _torsion(dn1)
            free_rank = max(0, len(cols_n) - rank_dn - rank_dn1)

            if free_rank > 0 or tors:
                groups[(p, q)] = (free_rank, tors)
                max_p = max(max_p, p)
                max_total = max(max_total, n)

    return SpectralPage(
        page_number=1,
        groups=groups,
        max_p=max_p,
        max_total=max_total,
    )


def differential_d_r(
    page: SpectralPage,
    p: int,
    q: int,
) -> dict[tuple[int, int], int]:
    """Return the bidegree and rank of d^r at position (p, q).

    d^r: E^r_{p,q} → E^r_{p−r, q+r−1}  (bidegree (−r, r−1)).

    For a spectral sequence presented by Betti numbers (free abelian groups),
    the differential is represented by its rank — the maximum number of
    generators that can map nontrivially to the target.

    Returns
    -------
    dict
        ``{(p − r, q + r − 1): rank}`` if both source and target are nonzero,
        else an empty dict.

    Examples
    --------
    On the E^2 page of a product spectral sequence (Künneth), all
    differentials d^2, d^3, … are zero, so this returns ``{}``.
    """
    r = page.page_number
    src_betti, _ = page.get(p, q)
    tgt_betti, _ = page.get(p - r, q + r - 1)
    if src_betti == 0 or tgt_betti == 0:
        return {}
    return {(p - r, q + r - 1): min(src_betti, tgt_betti)}


def converges_to(
    fcc: FilteredChainComplex,
) -> tuple[SpectralPage, list[SpectralPage]]:
    """Compute all pages of the spectral sequence until convergence (E^∞).

    Starts from E^1, then iterates d^r page-turns until the page stabilises.
    Each step computes E^{r+1}_{p,q} = ker(d^r_{p,q}) / im(d^r_{p+r, q−r+1}).

    Parameters
    ----------
    fcc : FilteredChainComplex
        A finite filtered chain complex built by
        ``filtered_chain_complex_from_simplices`` or supplied directly.

    Returns
    -------
    (e_inf, pages)
        ``e_inf`` — the stabilised E^∞ page.
        ``pages`` — list [E^1, E^2, …] of all computed pages.

    Notes
    -----
    Convergence: E^∞_{p,q} ≅ Gr^p H_{p+q}(C_*).
    For a product filtration: sequence degenerates at E^2 (Künneth formula).
    For a Serre fibration: E^2_{p,q} = H_p(B; H_q(F)) ⇒ H_{p+q}(E).
    """
    e1 = _e1_page_from_fcc(fcc)
    pages: list[SpectralPage] = [e1]
    current = e1
    max_steps = fcc.num_filtration + fcc.num_degrees + 4

    for _ in range(max_steps):
        r = current.page_number
        next_groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}

        # Collect all relevant positions (source positions + positions that
        # receive incoming differentials)
        positions: set[tuple[int, int]] = set(current.groups.keys())
        for p, q in list(positions):
            positions.add((p + r, q - r + 1))  # positions sending to (p,q)

        for p, q in positions:
            src_betti, src_tors = current.get(p, q)
            # Incoming: d^r from (p+r, q−r+1) → (p, q)
            in_betti, _ = current.get(p + r, q - r + 1)
            # Outgoing: d^r from (p, q) → (p−r, q+r−1)
            out_betti, _ = current.get(p - r, q + r - 1)

            rank_in = min(src_betti, in_betti)
            rank_out = min(src_betti, out_betti)
            new_betti = max(0, src_betti - rank_in - rank_out)

            if new_betti > 0 or src_tors:
                next_groups[(p, q)] = (new_betti, src_tors)

        new_max_p = max((p for p, _ in next_groups), default=0)
        new_max_total = max((p + q for p, q in next_groups), default=0)
        next_page = SpectralPage(
            page_number=r + 1,
            groups=next_groups,
            max_p=new_max_p,
            max_total=new_max_total,
        )
        pages.append(next_page)

        if next_groups == current.groups:
            return next_page, pages

        current = next_page

    return current, pages
