r"""Motivic homotopy theory: A¹-homotopy, Nisnevich topology, motivic cohomology,
algebraic K-theory, Milnor K-theory, stable motivic homotopy category, Voevodsky theorems.

Key theorems and constructions implemented
------------------------------------------
- A¹-homotopy theory (Morel-Voevodsky, 1999): the motivic homotopy category H(k) is
  constructed by taking the category of sheaves of simplicial sets on the Nisnevich site
  Sm/k (smooth k-schemes), then inverting two types of weak equivalences:
  (1) simplicial weak equivalences (Nisnevich-local), and
  (2) A¹-weak equivalences (maps X x A¹ -> X are equivalences for A¹ = Spec k[t]).
  The role of the unit interval [0,1] in classical homotopy theory is played by the
  affine line A¹ = Spec k[t]. This gives a model category whose homotopy category H(k)
  contains classical topology (via X |-> X(C) for k = C) and algebraic geometry.
  The A¹-fundamental group pi_1^{A¹}(P^1) was computed by Morel to be the free
  A¹-group on one generator, recovered as the Grothendieck-Witt group GW(k) for k = R.
  Key examples: P^1 = S^1 ^ (A¹\{0}) (motivic) — the motivic version of S^2.
  The Hopf fibration eta: A²\{0} -> P^1 is an A¹-fibration, the motivic analogue of
  the classical Hopf map S³ -> S². The motivic Hopf map is non-trivial and generates
  the motivic stable homotopy of the sphere spectrum.

- Nisnevich topology: introduced by Nisnevich (1989), it is a Grothendieck topology on
  the category Sm/k of smooth k-schemes, intermediate between the Zariski and étale
  topologies. A covering family {U_i -> X} is a Nisnevich cover if every point x in X
  (not just geometric points) has a preimage with the same residue field. Formally: a
  morphism f: U -> X is a Nisnevich cover if it is étale and for every point x in X,
  there exists u in U with f(u) = x and k(u) = k(x) (residue field isomorphism).
  The Nisnevich topology is crucial because: (a) cohomological dimension is bounded
  (cd_{Nis}(k) <= d = dim k), (b) étale sheaves descend to Nisnevich sheaves, and
  (c) the Nisnevich cohomology of algebraic K-theory equals algebraic K-theory itself
  (Brown-Gersten property: K-theory satisfies Nisnevich descent).
  Brown-Gersten property: a presheaf F satisfies Nisnevich descent if for every
  elementary distinguished square (Cartesian square with f étale, Z closed, open
  complement isomorphic), the square F(X) -> F(U) x_{F(W)} F(V) is a homotopy
  pullback.

- Motivic cohomology H^{p,q}(X, Z): a bigraded cohomology theory for smooth k-schemes X,
  defined using Voevodsky's motivic complexes Z(q) (the sheaves of the DM category).
  The bidegree (p, q) has: p = cohomological degree, q = motivic weight (or twist).
  Fundamental isomorphism: H^{2n,n}(X, Z) = CH^n(X) (Chow groups). This unifies
  classical intersection theory with homotopy theory. Other cases:
  H^{0,0}(Spec k, Z) = Z, H^{1,1}(Spec k, Z) = k* (units of k),
  H^{n,n}(Spec k, Z) = K^M_n(k) (Milnor K-theory), and
  H^{p,q}(X, Z/l) ≅ H^p(X, mu_l^{tensor q}) (étale cohomology for l != char k).
  The motivic cohomology H^{p,q}(-, Z) is represented in SH(k) by the motivic
  Eilenberg-MacLane spectrum HZ: [Sigma^{p,q} Sigma^inf X_+, HZ] ≅ H^{p,q}(X, Z).
  Beilinson-Lichtenbaum conjecture (proved by Voevodsky): for l prime != char k,
  the natural map H^{p,q}(X, Z/l) -> H^p_ét(X, mu_l^{tensor q}) is an isomorphism
  for p <= q. Combined with the Milnor conjecture (Voevodsky 2003), this proves the
  Bloch-Kato conjecture for all primes l.

- Algebraic K-theory K(X): for a smooth scheme X, the algebraic K-groups K_n(X) measure
  information about vector bundles (coherent sheaves) on X. Defined as pi_n of the
  K-theory space BGL(X)+ (plus-construction) or via Quillen's Q-construction.
  Bott periodicity: in topology, K(X)[beta^{-1}] = KU(X) (complex K-theory). In
  algebraic geometry, inverting the Bott element beta in K_*(X) gives periodic K-theory.
  Atiyah-Hirzebruch spectral sequence (motivic): E_2^{p,q} = H^{-q,-q/2}(X, Z) =>
  K_{-p-q}(X) — the motivic version relating motivic cohomology and K-theory.
  Bass-Quillen theorem: for a smooth affine variety X over a field k, K_n(X x A^1) = K_n(X)
  for all n (K-theory is A¹-invariant on smooth affine varieties).
  Algebraic K-theory is represented in SH(k) by the K-theory spectrum KGL, and the
  periodicity theorem KGL = KGL[beta^{-1}] holds in SH(k). The motivic Adams operations
  psi^k: KGL -> KGL play the role of Adams operations in topology.

- Milnor K-theory K^M_*(k): for a field k, the Milnor K-theory is
  K^M_n(k) = k* tensor ... tensor k* / (a_1 tensor ... tensor a_n : a_i + a_j = 1 for some i!=j).
  The generators are symbols {a_1, ..., a_n} = a_1 tensor ... tensor a_n in k* ^{tensor n}.
  The Milnor K-group K^M_n(k) is the quotient of (k*)^n by the Steinberg relations
  {a_1, ..., a_n} = 0 whenever a_i + a_j = 1 for some i != j.
  Fundamental isomorphism: H^{n,n}(Spec k, Z) = K^M_n(k) (Nesterenko-Suslin, Totaro 1989).
  Milnor conjecture (proved by Voevodsky 1996, Fields Medal 2002): the natural map
  K^M_n(k) / 2 -> H^n_ét(k, Z/2) is an isomorphism for all n and all fields k of
  characteristic != 2. This resolved a conjecture open since 1970.
  Bloch-Kato conjecture (proved by Voevodsky-Rost-Weibel 2009): for any prime l != char k,
  K^M_n(k) / l -> H^n_ét(k, mu_l^{tensor n}) is an isomorphism.
  The motivic Steenrod algebra and motivic cohomology operations (motivic Sq^i) are key
  tools in the proof, constructed via the motivic Eilenberg-MacLane spectrum HZ/l.

- Stable motivic homotopy category SH(k): the motivic analogue of the stable homotopy
  category. Constructed by formally inverting the bigraded spheres S^{p,q} = (S^1)^{p-q}
  ^ (A¹\{0})^q (smash product). The sphere spectrum S^{0,0} = Spec k_+ and the motivic
  spheres satisfy S^{1,0} = S^1 (topological), S^{1,1} = A¹\{0} (Gm, algebraic),
  S^{2,1} = P^1 (projective line = S^1 ^ Gm).
  Motivic stable homotopy groups: pi_{p,q}(S^{0,0}) are highly non-trivial; the first
  non-trivial element is eta in pi_{1,1}(S^{0,0}) (motivic Hopf map), satisfying
  2 eta = 0 and eta^4 = 0. Over R, eta is non-nilpotent (unlike in topology).
  Oriented spectra: a ring spectrum E in SH(k) is oriented if the tautological line
  bundle over P^inf has a Thom class. Oriented spectra satisfy the projective bundle
  formula E*(P(V)) = E*(X)[t]/(t^{n+1}) for V -> X a rank n+1 bundle.
  Algebraic cobordism MGL: the universal oriented cohomology theory in SH(k), defined
  as the Thom spectrum of the canonical bundle over the algebraic Grassmannian. MGL
  is the motivic analogue of complex cobordism MU.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result

# ---------------------------------------------------------------------------
# MotivicHomotopyProfile dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MotivicHomotopyProfile:
    """A curated motivic homotopy theory example."""

    key: str
    display_name: str
    motivic_type: str        # "a1_homotopy", "stable_motivic", "motivic_cohomology",
                             # "algebraic_k_theory", "milnor_k_theory", "nisnevich"
    base_field: str          # "general", "algebraically_closed", "real_closed",
                             # "finite", "number_field"
    is_stable: bool          # lives in stable motivic homotopy category SH(k)
    has_transfers: bool      # carries Voevodsky transfers (sheaf with transfers)
    is_oriented: bool        # oriented cohomology theory (Thom class for line bundles)
    is_a1_invariant: bool    # satisfies A¹-invariance: F(X) ≅ F(X x A¹)
    has_nisnevich_descent: bool  # satisfies Nisnevich descent / Brown-Gersten property
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

A1_HOMOTOPY_TAGS: frozenset[str] = frozenset({
    "a1_homotopy",
    "a1_local",
    "a1_invariant",
    "a1_fibration",
    "a1_weak_equivalence",
    "motivic_space",
    "morel_voevodsky",
    "a1_fundamental_group",
    "motivic_homotopy",
    "a1_homotopy_theory",
})

NISNEVICH_TOPOLOGY_TAGS: frozenset[str] = frozenset({
    "nisnevich_topology",
    "nisnevich_sheaf",
    "nisnevich_cover",
    "nisnevich_descent",
    "nisnevich_site",
    "brown_gersten",
    "elementary_distinguished_square",
    "nisnevich_local",
    "etale_vs_nisnevich",
})

MOTIVIC_COHOMOLOGY_TAGS: frozenset[str] = frozenset({
    "motivic_cohomology",
    "motivic_complex",
    "bigraded_cohomology",
    "motivic_eilenberg_maclane",
    "hz_spectrum",
    "chow_group",
    "motivic_weight",
    "beilinson_lichtenbaum",
    "bloch_kato",
    "voevodsky_complex",
})

ALGEBRAIC_K_THEORY_TAGS: frozenset[str] = frozenset({
    "algebraic_k_theory",
    "kgl_spectrum",
    "k_theory_spectrum",
    "quillen_k_theory",
    "higher_k_theory",
    "k0_group",
    "bott_periodicity_algebraic",
    "bass_quillen",
    "atiyah_hirzebruch_motivic",
    "adams_operations_motivic",
})

MILNOR_K_THEORY_TAGS: frozenset[str] = frozenset({
    "milnor_k_theory",
    "milnor_k_group",
    "steinberg_relation",
    "milnor_conjecture",
    "milnor_symbol",
    "k_milnor",
    "galois_cohomology_milnor",
    "norm_residue",
    "bloch_kato_milnor",
})

STABLE_MOTIVIC_TAGS: frozenset[str] = frozenset({
    "stable_motivic",
    "sh_k",
    "motivic_spectrum",
    "bigraded_sphere",
    "motivic_stable_homotopy",
    "algebraic_cobordism",
    "mgl_spectrum",
    "motivic_adams",
    "motivic_hopf",
    "oriented_spectrum",
})

VOEVODSKY_TAGS: frozenset[str] = frozenset({
    "voevodsky",
    "voevodsky_motives",
    "dm_category",
    "triangulated_motives",
    "dm_gm",
    "mixed_motives",
    "motivic_sheaf",
    "cor_finite_correspondences",
    "presheaf_with_transfers",
})

MOTIVIC_SPHERE_TAGS: frozenset[str] = frozenset({
    "motivic_sphere",
    "s11_sphere",
    "gm_sphere",
    "bigraded_sphere",
    "projective_line_sphere",
    "p1_sphere",
    "motivic_suspension",
    "a1_punctured",
    "motivic_hopf_fibration",
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

def get_named_motivic_profiles() -> tuple[MotivicHomotopyProfile, ...]:
    """Return the registry of canonical motivic homotopy theory examples."""
    return (
        MotivicHomotopyProfile(
            key="a1_homotopy_space",
            display_name="A¹-homotopy space — motivic space on Sm/k with A¹-local fibrant replacement",
            motivic_type="a1_homotopy",
            base_field="general",
            is_stable=False,
            has_transfers=False,
            is_oriented=False,
            is_a1_invariant=True,
            has_nisnevich_descent=True,
            presentation_layer="main_text",
            focus=(
                "The A¹-homotopy category H(k) of Morel-Voevodsky (1999) is the central "
                "object of motivic homotopy theory. Construction: start with the category "
                "sPre(Sm/k) of simplicial presheaves on smooth k-schemes (the Nisnevich site). "
                "Impose two localization conditions: "
                "(1) Nisnevich descent: sheaves satisfy the Brown-Gersten property for "
                "elementary distinguished squares; and "
                "(2) A¹-invariance: the projection X x A¹ -> X induces a weak equivalence "
                "F(X) -> F(X x A¹) for all smooth X. "
                "The A¹-local model structure on sPre(Sm/k) is obtained by Bousfield "
                "localization at Nisnevich hypercovers and A¹-projections. "
                "The homotopy category H(k) = Ho(sPre_{A¹}(Sm/k)) is the motivic "
                "homotopy category. "
                "Every smooth k-scheme X represents an object in H(k) via the Yoneda "
                "embedding X |-> hom(-, X). Under the realization map rho: H(k) -> H (over "
                "k = C), smooth C-varieties X map to their analytic spaces X(C). "
                "A¹-fundamental group: pi_1^{A¹}(P^1_k) = K^{MW}_1(k) (Milnor-Witt K-theory "
                "in degree 1). Over algebraically closed k: pi_1^{A¹}(P^1) = k*. "
                "Over k = R: pi_1^{A¹}(P^1_R) is the free A¹-group on a generator, which "
                "after sheafification gives the Grothendieck-Witt group GW(R). "
                "A¹-homotopy invariance: algebraic K-theory, motivic cohomology, and "
                "algebraic cobordism are all A¹-invariant (on smooth schemes)."
            ),
            chapter_targets=("40", "52", "63"),
        ),
        MotivicHomotopyProfile(
            key="nisnevich_sheaf",
            display_name="Nisnevich sheaf — sheaf on the Nisnevich site Sm/k",
            motivic_type="nisnevich",
            base_field="general",
            is_stable=False,
            has_transfers=False,
            is_oriented=False,
            is_a1_invariant=False,
            has_nisnevich_descent=True,
            presentation_layer="main_text",
            focus=(
                "The Nisnevich topology is a Grothendieck topology on Sm/k (smooth "
                "k-schemes of finite type) defined by Nisnevich (1989). "
                "Covering condition: {f_i: U_i -> X} is a Nisnevich cover if each f_i is "
                "étale and for every point x in X there exists i and u in U_i with "
                "f_i(u) = x AND the residue field extension k(u)/k(x) is an isomorphism "
                "(not just algebraic). "
                "Comparison: Zariski < Nisnevich < étale (in terms of which maps are covers). "
                "Every étale cover is a Nisnevich cover; not every Nisnevich cover is Zariski. "
                "Example: {A¹ \\ {0} -> P¹ \\ {infty}, A¹ -> P¹} is a Nisnevich cover of P¹. "
                "Brown-Gersten property: a presheaf F: (Sm/k)^op -> sSet satisfies "
                "Nisnevich descent if for every elementary distinguished square "
                "(Cartesian: U = X \\ Z, V -> X étale with V x_X (X \\ U) ≅ X \\ U), "
                "the square F(X) -> F(U) x_{F(W)} F(V) is a homotopy pullback in sSet. "
                "Algebraic K-theory satisfies the Brown-Gersten property (Thomason-Trobaugh). "
                "Cohomological dimension: cd_{Nis}(k) = dim(k) (Krull dimension), much "
                "smaller than the étale cohomological dimension cd_ét(k) = 2 dim(k) + 1. "
                "This smaller cohomological dimension makes Nisnevich cohomology "
                "computationally more tractable than étale cohomology. "
                "Motivic homotopy: the Nisnevich site is the correct topology for "
                "constructing motivic cohomology and A¹-homotopy theory. The Zariski site "
                "is too coarse (K-theory doesn't satisfy Zariski descent in general), "
                "and the étale site adds too much (A¹-invariance fails étale-locally)."
            ),
            chapter_targets=("40", "52", "63"),
        ),
        MotivicHomotopyProfile(
            key="motivic_cohomology_hz",
            display_name="Motivic Eilenberg-MacLane spectrum HZ — representing motivic cohomology",
            motivic_type="motivic_cohomology",
            base_field="general",
            is_stable=True,
            has_transfers=True,
            is_oriented=True,
            is_a1_invariant=True,
            has_nisnevich_descent=True,
            presentation_layer="main_text",
            focus=(
                "Motivic cohomology H^{p,q}(X, Z) is a bigraded cohomology theory for "
                "smooth k-schemes, represented in the stable motivic homotopy category "
                "SH(k) by the motivic Eilenberg-MacLane spectrum HZ. "
                "Construction (Voevodsky): define the motivic complex Z(q) as the sheaf "
                "of normalized Moore chains on the free presheaf with transfers Z_{tr}(A^q) "
                "shifted by q. Then H^{p,q}(X, Z) = H^p_{Nis}(X, Z(q)). "
                "Key isomorphisms: "
                "- H^{0,0}(Spec k, Z) = Z "
                "- H^{1,1}(Spec k, Z) = k* (units) "
                "- H^{2,1}(Spec k, Z) = 0 "
                "- H^{n,n}(Spec k, Z) = K^M_n(k) (Milnor K-theory) [Nesterenko-Suslin] "
                "- H^{2n,n}(X, Z) = CH^n(X) (Chow groups) [main theorem] "
                "Beilinson-Lichtenbaum: for l prime, l != char k, "
                "H^{p,q}(X, Z/l) -> H^p_ét(X, mu_l^{tensor q}) is isomorphism for p <= q. "
                "This conjecture (now theorem, proved by Voevodsky using motivic Steenrod "
                "operations) unifies motivic and étale cohomology. "
                "Transfers: HZ has a structure of sheaf with transfers — for a finite "
                "correspondence Z in Cor(X, Y), there is a pushforward map "
                "H^{p,q}(Y, Z) -> H^{p,q}(X, Z). This is the algebraic analogue of the "
                "transfer in equivariant topology. "
                "Relation to K-theory: the Atiyah-Hirzebruch spectral sequence "
                "E_2^{p,q} = H^{p-q,-q}(X, Z) => K_{-p}(X) converges to K-theory "
                "(degeneration up to extension problems)."
            ),
            chapter_targets=("40", "52", "63"),
        ),
        MotivicHomotopyProfile(
            key="algebraic_k_theory_kgl",
            display_name="Algebraic K-theory spectrum KGL — motivic analogue of topological K-theory",
            motivic_type="algebraic_k_theory",
            base_field="general",
            is_stable=True,
            has_transfers=False,
            is_oriented=True,
            is_a1_invariant=True,
            has_nisnevich_descent=True,
            presentation_layer="main_text",
            focus=(
                "Algebraic K-theory K(X) assigns to a smooth scheme X a sequence of "
                "abelian groups K_n(X) = pi_n(BGL(X)+) (via Quillen's plus construction) "
                "or equivalently via the Q-construction on the category of vector bundles. "
                "K_0(X) = Grothendieck group of vector bundles (algebraic analogue of "
                "topological K^0). For X = Spec k (a field): K_0(k) = Z, K_1(k) = k*, "
                "K_2(k) = K^M_2(k) = k* tensor k* / Steinberg (Matsumoto's theorem). "
                "A¹-invariance: for smooth affine X, K_n(X x A¹) ≅ K_n(X) for all n "
                "(Bass-Quillen theorem, proved by Quillen 1976). This is the algebraic "
                "analogue of the fact that complex K-theory is homotopy-invariant. "
                "Nisnevich descent (Brown-Gersten): K-theory satisfies the Brown-Gersten "
                "property — it is a sheaf for the Nisnevich topology. "
                "The K-theory spectrum KGL in SH(k): Voevodsky showed K-theory is "
                "representable in SH(k) by a motivic ring spectrum KGL with "
                "[Sigma^{p,q} X_+, KGL] = K_{2q-p}(X) (for q >= p). "
                "Bott periodicity: there is a Bott element beta in K_2(P^1) = K_0(k)[beta] "
                "with KGL[beta^{-1}] = KGL (periodicity). The motivic analogue of complex "
                "Bott periodicity: pi_{2,1}(KGL) = Z[beta] with |beta| = (2,1). "
                "Adams operations: motivic Adams operations psi^k: KGL -> KGL satisfy "
                "psi^k(x) = k^q x for x in K_0 coming from a rank-q bundle. These are "
                "ring spectrum maps and are used to split KGL into motivic eigensummands "
                "corresponding to different Adams weights. "
                "Relation to motivic cohomology: the motivic AHSS "
                "E_2^{p,q} = H^{p-q,-q}(X, Z) => K_{-p}(X) degenerates (up to 2-torsion) "
                "for smooth varieties over a field of characteristic zero."
            ),
            chapter_targets=("40", "52", "63"),
        ),
        MotivicHomotopyProfile(
            key="milnor_k_theory",
            display_name="Milnor K-theory K^M_n(k) — symbols in k* modulo Steinberg relations",
            motivic_type="milnor_k_theory",
            base_field="general",
            is_stable=False,
            has_transfers=True,
            is_oriented=False,
            is_a1_invariant=True,
            has_nisnevich_descent=True,
            presentation_layer="main_text",
            focus=(
                "Milnor K-theory was introduced by Milnor (1970) as the graded ring "
                "K^M_*(k) = T^*(k*) / (a tensor (1-a) : a in k*, a != 1), where T^* "
                "is the tensor algebra of k* = k \\ {0}. "
                "Generators: K^M_n(k) is generated by symbols {a_1, ..., a_n} for a_i in k*, "
                "subject to: multilinearity, and the Steinberg relation {a_1,...,a_n} = 0 "
                "whenever a_i + a_j = 1 for some i != j (equivalently a_i + a_j - 1 = 0). "
                "Low degrees: K^M_0(k) = Z, K^M_1(k) = k*, "
                "K^M_2(k) = k* tensor k* / ({a, 1-a} : a != 0, 1) = K_2(k) [Matsumoto]. "
                "Norm residue map (Galois symbol): rho_n: K^M_n(k) / l -> H^n_ét(k, mu_l^n). "
                "Milnor conjecture (l=2, proved Voevodsky 1996): rho_n is an isomorphism "
                "for all n, for l=2, char k != 2. "
                "Bloch-Kato conjecture (all primes l, proved Voevodsky-Rost-Weibel 2003-2009): "
                "rho_n: K^M_n(k)/l -> H^n_ét(k, mu_l^n) is an isomorphism for all n, l, "
                "char k != l. This is one of the deepest theorems in algebraic K-theory. "
                "Motivic cohomology: H^{n,n}(Spec k, Z) = K^M_n(k) "
                "(Nesterenko-Suslin 1989, Totaro 1992). "
                "This places Milnor K-theory naturally within the motivic cohomology framework. "
                "Milnor-Witt K-theory K^{MW}_*(k): a refinement encoding quadratic forms "
                "(used by Morel in the computation of A¹-homotopy groups of punctured affine "
                "spaces), satisfying K^{MW}_n / eta = K^M_n and K^{MW}_n / h = K^W_n "
                "(Witt K-theory), where eta is the motivic Hopf element."
            ),
            chapter_targets=("40", "52", "63"),
        ),
        MotivicHomotopyProfile(
            key="stable_motivic_sphere_s11",
            display_name="Motivic sphere S^{1,1} = Gm = A¹\\{0} — the multiplicative group",
            motivic_type="stable_motivic",
            base_field="general",
            is_stable=True,
            has_transfers=False,
            is_oriented=False,
            is_a1_invariant=False,
            has_nisnevich_descent=True,
            presentation_layer="main_text",
            focus=(
                "In motivic homotopy theory, the bigraded spheres S^{p,q} replace "
                "the single sphere S^n of classical topology. "
                "Motivic sphere definitions: "
                "S^{1,0} = S^1 = Delta^1 / partial Delta^1 (topological circle, constant sheaf), "
                "S^{1,1} = A¹ \\ {0} = Gm = Spec k[t, t^{-1}] (multiplicative group), "
                "S^{2,1} = S^1 ^ S^{1,1} = P^1 (projective line = motivic 'S^2'), "
                "S^{p,q} = (S^1)^{p-q} ^ (Gm)^q (smash products). "
                "A¹-invariance of S^{1,1}: Gm is NOT A¹-invariant (pi_0(Gm) = k* is a sheaf "
                "of groups, and A¹ \\ {0} -> point induces k* != {1} = pi_0(point)). "
                "Nisnevich descent: Gm does satisfy Nisnevich descent as a sheaf of groups. "
                "Motivic Hopf map eta: the map eta: A² \\ {0} -> P¹, (x,y) |-> [x:y], "
                "is an A¹-fibration with fiber A¹ \\ {0} = S^{1,1}. This gives the "
                "motivic Hopf fibration S^{3,2} -> S^{2,1} with fiber S^{1,1}. "
                "The element eta in pi_{1,1}^{A¹}(S^{0,0}) is the motivic Hopf element; "
                "it is NOT nilpotent over the reals (unlike in topology where eta^4 = 0). "
                "Over a field k, eta is 4-nilpotent if char k != 2 (Morel). "
                "Stable motivic homotopy: in SH(k), the sphere spectrum S = {S^{0,0}} has "
                "pi_{1,1}(S) = K^{MW}_1(k) = k* (Morel), confirming that motivic stable "
                "homotopy groups encode algebraic information about the base field. "
                "The Picard group of SH(k): the invertible spectra are the bigraded spheres "
                "S^{p,q} for (p, q) in Z x Z, forming a Z x Z-graded theory."
            ),
            chapter_targets=("40", "52", "63"),
        ),
        MotivicHomotopyProfile(
            key="chow_group",
            display_name="Chow groups CH^n(X) = H^{2n,n}(X, Z) — algebraic cycles modulo rational equivalence",
            motivic_type="motivic_cohomology",
            base_field="general",
            is_stable=False,
            has_transfers=True,
            is_oriented=True,
            is_a1_invariant=False,
            has_nisnevich_descent=True,
            presentation_layer="main_text",
            focus=(
                "Chow groups CH^n(X) = Z^n(X) / ~ are the groups of algebraic cycles of "
                "codimension n on X modulo rational equivalence. An algebraic cycle of "
                "codimension n is a formal Z-linear combination of irreducible closed "
                "subvarieties of codimension n. Two cycles Z_0 and Z_1 are rationally "
                "equivalent if there exists a cycle W on X x P¹ flat over P¹ with "
                "W|_{t=0} = Z_0 and W|_{t=1} = Z_1. "
                "Motivic cohomology isomorphism: CH^n(X) ≅ H^{2n,n}(X, Z) "
                "(Bloch 1986, Voevodsky). This is the fundamental relationship connecting "
                "algebraic cycles to motivic cohomology. "
                "Cycle class map: there is a natural map "
                "cl: CH^n(X) -> H^{2n}(X(C), Z) (singular cohomology) for X over C. "
                "The Hodge conjecture asks whether cl is surjective onto Hdg^{2n}(X) "
                "(Hodge classes). This remains an open Millennium Prize Problem. "
                "Intersection theory: CH^*(X) = direct sum_n CH^n(X) is a graded ring "
                "under intersection product: [Z] . [W] = [Z cap W] (for transverse Z, W). "
                "This extends to the full CH^* via moving lemmas. "
                "Pushforward and pullback: for f: X -> Y, there is f_*: CH^{n-d}(X) -> CH^{n-d}(Y) "
                "(proper pushforward) and f^*: CH^n(Y) -> CH^n(X) (flat pullback), making "
                "CH^* a contravariant functor for flat morphisms. "
                "Examples: CH^0(X) = Z (connected X), CH^1(X) = Pic(X) (Picard group), "
                "CH^n(X) = CH_0(X) = degree 0 cycles for dim X = n (zero cycles). "
                "The degree map deg: CH^0(Spec k) = Z computes the degree of a 0-cycle. "
                "Transfers in motivic cohomology: for a finite cover f: Y -> X of degree d, "
                "the transfer map Tr_f: CH^n(Y) -> CH^n(X) satisfies Tr_f o f^* = d id."
            ),
            chapter_targets=("40", "52", "63"),
        ),
        MotivicHomotopyProfile(
            key="algebraic_cobordism_mgl",
            display_name="Algebraic cobordism MGL — universal oriented cohomology in SH(k)",
            motivic_type="stable_motivic",
            base_field="general",
            is_stable=True,
            has_transfers=False,
            is_oriented=True,
            is_a1_invariant=True,
            has_nisnevich_descent=True,
            presentation_layer="main_text",
            focus=(
                "Algebraic cobordism MGL (motivic Grassmannian-Lazard spectrum) is the "
                "universal oriented cohomology theory in the stable motivic homotopy "
                "category SH(k), constructed as the Thom spectrum of the tautological "
                "bundle over the infinite Grassmannian Gr = colim_{m,n} Gr(m, m+n). "
                "Universality: for any oriented cohomology theory E (a commutative ring "
                "spectrum in SH(k) with a Thom class for line bundles), there is a unique "
                "ring spectrum map MGL -> E. This makes MGL the motivic analogue of "
                "complex cobordism MU in topology. "
                "Oriented cohomology theory: a ring spectrum E in SH(k) is oriented if "
                "there exists a Thom class c_1^E(L) in E^{2,1}(Th(L)) for every line "
                "bundle L -> X, natural in X. Equivalently, E(P^inf) = E(*)[t] (projective "
                "bundle formula with t of bidegree (2,1)). "
                "Formal group law: MGL^{*,*}(*) = MGL^{2*,*}(*) and there is a formal "
                "group law F_{MGL}(x, y) = x + y + sum_{i,j} a_{ij} x^i y^j where "
                "a_{ij} in MGL^{2-2(i+j-1), 1-(i+j-1)}. "
                "Levine-Morel algebraic cobordism Omega^*(X): for smooth X over k, "
                "Omega^*(X) is the universal oriented Borel-Moore homology theory, "
                "satisfying Omega^*(Spec k) = L (Lazard ring). "
                "Comparison: pi_{2n,n}(MGL) = Omega^n(Spec k) = L^n (n-th graded piece "
                "of the Lazard ring), and after inverting the exponential characteristic, "
                "MGL_{(p)} splits into a wedge of HZ-module spectra (Hopkins-Morel-Hoyois). "
                "Applications: oriented characteristic classes (Chern classes c_i^E for "
                "any oriented E), Riemann-Roch type formulas, and the computation of "
                "motivic stable homotopy groups via Adams spectral sequences "
                "E_2^{p,q} = Ext_{MGL_*MGL}(MGL_*, MGL_*) => pi_{p-q}(S^{0,0}) over "
                "algebraically closed fields."
            ),
            chapter_targets=("40", "52", "63"),
        ),
    )


# ---------------------------------------------------------------------------
# Summary / index functions
# ---------------------------------------------------------------------------

def motivic_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_motivic_profiles()
    ))


def motivic_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_motivic_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {ch: tuple(keys) for ch, keys in sorted(chapter_map.items())}


def motivic_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from motivic_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_motivic_profiles():
        index.setdefault(p.motivic_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_a1_invariant(space: Any) -> Result:
    """Check whether the space/theory satisfies A¹-invariance.

    A presheaf F on Sm/k is A¹-invariant if the projection pr: X x A¹ -> X
    induces a weak equivalence F(X) -> F(X x A¹) for every smooth X. This is
    the motivic analogue of homotopy invariance (the interval [0,1] is replaced
    by the affine line A¹ = Spec k[t]).

    Decision layers
    ---------------
    1. Explicit A¹-homotopy or A¹-invariant tags -> true.
    2. Known A¹-invariant theories (K-theory, motivic cohomology, MGL) -> true.
    3. Known non-A¹-invariant objects (Gm as presheaf, Pic non-invariant cases) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    explicit_a1 = {"a1_invariant", "a1_local", "a1_homotopy", "motivic_homotopy"}
    if _matches_any(tags, explicit_a1):
        witness = next(t for t in tags if t in explicit_a1)
        return Result.true(
            mode="theorem",
            value="a1_invariant",
            justification=[
                f"Tag {witness!r}: the space/theory is explicitly A¹-invariant — "
                "the map F(X) -> F(X x A¹) is a weak equivalence for all smooth X.",
            ],
            metadata={**base, "criterion": "explicit_a1_invariant", "witness": witness},
        )

    if _matches_any(tags, A1_HOMOTOPY_TAGS):
        witness = next(t for t in tags if t in A1_HOMOTOPY_TAGS)
        return Result.true(
            mode="theorem",
            value="a1_invariant",
            justification=[
                f"Tag {witness!r}: objects in the A¹-homotopy category are, by "
                "construction, A¹-local and hence A¹-invariant. "
                "A¹-local fibrant replacement enforces A¹-invariance.",
            ],
            metadata={**base, "criterion": "a1_homotopy_category", "witness": witness},
        )

    known_a1_invariant = {
        "algebraic_k_theory", "kgl_spectrum", "motivic_cohomology", "hz_spectrum",
        "algebraic_cobordism", "mgl_spectrum", "oriented_spectrum",
        "chow_group", "milnor_k_theory",
    }
    if _matches_any(tags, known_a1_invariant | ALGEBRAIC_K_THEORY_TAGS | MOTIVIC_COHOMOLOGY_TAGS
                    | STABLE_MOTIVIC_TAGS | MILNOR_K_THEORY_TAGS):
        relevant = (known_a1_invariant | ALGEBRAIC_K_THEORY_TAGS | MOTIVIC_COHOMOLOGY_TAGS
                    | STABLE_MOTIVIC_TAGS | MILNOR_K_THEORY_TAGS) & tags
        witness = next(iter(relevant))
        return Result.true(
            mode="theorem",
            value="a1_invariant",
            justification=[
                f"Tag {witness!r}: algebraic K-theory, motivic cohomology, algebraic "
                "cobordism, and Milnor K-theory are all A¹-invariant theories "
                "(Bass-Quillen for K-theory; by construction for HZ and MGL).",
            ],
            metadata={**base, "criterion": "known_a1_invariant_theory", "witness": witness},
        )

    non_a1 = {
        "non_a1_invariant", "gm_sheaf", "pic_non_trivial",
        "not_a1_local", "a1_non_invariant",
    }
    if _matches_any(tags, non_a1):
        witness = next(t for t in tags if t in non_a1)
        return Result.false(
            mode="theorem",
            value="not_a1_invariant",
            justification=[
                f"Tag {witness!r}: the sheaf/theory is not A¹-invariant. "
                "Example: Gm = A¹ \\ {{0}} is not A¹-invariant as a presheaf "
                "(H^1(A¹, Gm) = 0 but H^1(A¹ x A¹, Gm) != 0 in étale topology).",
            ],
            metadata={**base, "criterion": "explicit_non_a1", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate A¹-invariance or its failure. "
            "Cannot determine A¹-invariance status.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def has_nisnevich_descent(space: Any) -> Result:
    """Check whether the theory satisfies Nisnevich descent (Brown-Gersten property).

    A presheaf F: (Sm/k)^op -> sSet satisfies Nisnevich descent if for every
    elementary distinguished square (p: V -> X étale, Z closed in X, j: U = X \\ Z -> X
    open, p^{-1}(U) ≅ U), the square F(X) -> F(U) x_{F(p^{-1}(U))} F(V) is a
    homotopy pullback in sSet. This is the motivic analogue of Mayer-Vietoris.

    Decision layers
    ---------------
    1. Explicit Nisnevich tags -> true.
    2. Known theories satisfying Nisnevich descent (K-theory, motivic cohomology) -> true.
    3. Explicit Zariski-only or non-descent failure tags -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, NISNEVICH_TOPOLOGY_TAGS):
        witness = next(t for t in tags if t in NISNEVICH_TOPOLOGY_TAGS)
        return Result.true(
            mode="theorem",
            value="nisnevich_descent",
            justification=[
                f"Tag {witness!r}: the theory explicitly satisfies Nisnevich descent — "
                "it is a sheaf for the Nisnevich topology and satisfies the "
                "Brown-Gersten property for elementary distinguished squares.",
            ],
            metadata={**base, "criterion": "explicit_nisnevich", "witness": witness},
        )

    known_nisnevich = {
        "algebraic_k_theory", "kgl_spectrum", "motivic_cohomology", "hz_spectrum",
        "algebraic_cobordism", "mgl_spectrum", "milnor_k_theory", "chow_group",
        "motivic_space", "a1_local", "nisnevich_sheaf",
    }
    if _matches_any(tags, known_nisnevich | ALGEBRAIC_K_THEORY_TAGS | MOTIVIC_COHOMOLOGY_TAGS
                    | VOEVODSKY_TAGS | STABLE_MOTIVIC_TAGS):
        relevant = (known_nisnevich | ALGEBRAIC_K_THEORY_TAGS | MOTIVIC_COHOMOLOGY_TAGS
                    | VOEVODSKY_TAGS | STABLE_MOTIVIC_TAGS) & tags
        witness = next(iter(relevant))
        return Result.true(
            mode="theorem",
            value="nisnevich_descent",
            justification=[
                f"Tag {witness!r}: algebraic K-theory satisfies Nisnevich descent "
                "(Thomason-Trobaugh); motivic cohomology and MGL are Nisnevich sheaves "
                "by construction. Objects in H(k) and SH(k) satisfy Nisnevich descent.",
            ],
            metadata={**base, "criterion": "known_nisnevich_descent", "witness": witness},
        )

    non_descent = {
        "zariski_only", "fails_nisnevich_descent", "no_nisnevich_descent",
        "non_nisnevich",
    }
    if _matches_any(tags, non_descent):
        witness = next(t for t in tags if t in non_descent)
        return Result.false(
            mode="theorem",
            value="no_nisnevich_descent",
            justification=[
                f"Tag {witness!r}: the theory fails Nisnevich descent. "
                "It may only be a Zariski sheaf, or it may fail the "
                "Brown-Gersten property for some elementary distinguished square.",
            ],
            metadata={**base, "criterion": "explicit_non_nisnevich", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate Nisnevich descent or its failure. "
            "Cannot determine Nisnevich descent status.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def is_motivic_cohomology_theory(space: Any) -> Result:
    """Check whether the space/theory is (or represents) motivic cohomology.

    Motivic cohomology H^{p,q}(X, Z) is the bigraded cohomology theory represented
    by the motivic Eilenberg-MacLane spectrum HZ in SH(k). It satisfies:
    - H^{2n,n}(X, Z) = CH^n(X) (Chow groups),
    - H^{n,n}(Spec k, Z) = K^M_n(k) (Milnor K-theory),
    - Nisnevich descent, A¹-invariance, transfers.

    Decision layers
    ---------------
    1. Explicit motivic cohomology or HZ tags -> true.
    2. Chow groups or Milnor K-theory (which are motivic cohomology groups) -> true.
    3. Non-motivic-cohomology tags (topological cohomology only, no bigrading) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, MOTIVIC_COHOMOLOGY_TAGS):
        witness = next(t for t in tags if t in MOTIVIC_COHOMOLOGY_TAGS)
        return Result.true(
            mode="theorem",
            value="motivic_cohomology",
            justification=[
                f"Tag {witness!r}: the theory is motivic cohomology H^{{p,q}}(-, Z), "
                "represented by the motivic Eilenberg-MacLane spectrum HZ in SH(k). "
                "Key: H^{{2n,n}}(X, Z) = CH^n(X), H^{{n,n}}(Spec k, Z) = K^M_n(k).",
            ],
            metadata={**base, "criterion": "explicit_motivic_cohomology", "witness": witness},
        )

    milnor_chow = {
        "milnor_k_theory", "k_milnor", "chow_group", "algebraic_cycles",
        "bloch_cycle_complex", "higher_chow",
    }
    if _matches_any(tags, milnor_chow | MILNOR_K_THEORY_TAGS):
        relevant = (milnor_chow | MILNOR_K_THEORY_TAGS) & tags
        witness = next(iter(relevant))
        return Result.true(
            mode="theorem",
            value="motivic_cohomology",
            justification=[
                f"Tag {witness!r}: Chow groups CH^n = H^{{2n,n}}(-, Z) and Milnor "
                "K-theory K^M_n(k) = H^{{n,n}}(Spec k, Z) are specific motivic "
                "cohomology groups. The theory is motivic cohomology.",
            ],
            metadata={**base, "criterion": "chow_milnor_implies_motivic", "witness": witness},
        )

    non_motivic = {
        "singular_cohomology", "de_rham_only", "topological_only",
        "no_bigrading", "non_motivic",
    }
    if _matches_any(tags, non_motivic):
            witness = next(t for t in tags if t in non_motivic)
            return Result.false(
                mode="theorem",
                value="not_motivic_cohomology",
                justification=[
                    f"Tag {witness!r}: the theory is not motivic cohomology — it lacks "
                    "the bigrading (p, q) and the A¹-invariance essential for motivic "
                    "cohomology. It is a purely topological cohomology theory.",
                ],
                metadata={**base, "criterion": "explicit_non_motivic", "witness": witness},
            )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate motivic cohomology or an obstruction. "
            "Cannot determine motivic cohomology status.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def has_algebraic_k_theory_structure(space: Any) -> Result:
    """Check whether the space/theory carries algebraic K-theory structure.

    Algebraic K-theory K(X) is the universal additive invariant of exact categories
    (via Quillen's Q-construction) or stable ∞-categories (via Waldhausen S-construction).
    A theory has algebraic K-theory structure if it is or factors through K-theory:
    satisfies Nisnevich descent (Brown-Gersten), A¹-invariance on smooth schemes,
    and is representable by KGL in SH(k).

    Decision layers
    ---------------
    1. Explicit algebraic K-theory or KGL tags -> true.
    2. Theories known to factor through K-theory (G-theory for regular, Chow via AHSS) -> true.
    3. Theories with no K-theory content -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, ALGEBRAIC_K_THEORY_TAGS):
        witness = next(t for t in tags if t in ALGEBRAIC_K_THEORY_TAGS)
        return Result.true(
            mode="theorem",
            value="algebraic_k_theory",
            justification=[
                f"Tag {witness!r}: the theory is algebraic K-theory K(X), represented "
                "in SH(k) by KGL. Satisfies A¹-invariance (Bass-Quillen) and "
                "Nisnevich descent (Brown-Gersten / Thomason-Trobaugh).",
            ],
            metadata={**base, "criterion": "explicit_k_theory", "witness": witness},
        )

    k_theory_adjacent = {
        "g_theory", "grothendieck_group", "k0_group",
        "vector_bundles", "bott_periodicity_algebraic", "quillen_construction",
        "waldhausen_construction",
    }
    if _matches_any(tags, k_theory_adjacent):
        witness = next(t for t in tags if t in k_theory_adjacent)
        return Result.true(
            mode="theorem",
            value="algebraic_k_theory",
            justification=[
                f"Tag {witness!r}: Grothendieck K_0, G-theory (K-theory of coherent sheaves), "
                "and Quillen/Waldhausen constructions are all part of algebraic K-theory. "
                "For smooth varieties over a field, K(X) = G(X) (Poincaré duality).",
            ],
            metadata={**base, "criterion": "k_theory_adjacent", "witness": witness},
        )

    non_k = {
        "no_k_theory", "non_additive", "non_k_theory",
        "only_cohomological", "topological_k_only",
    }
    if _matches_any(tags, non_k):
        witness = next(t for t in tags if t in non_k)
        return Result.false(
            mode="theorem",
            value="no_k_theory_structure",
            justification=[
                f"Tag {witness!r}: the theory does not carry algebraic K-theory structure. "
                "It may be purely cohomological (no additive invariant structure) or "
                "only topological K-theory without the algebraic A¹-invariance property.",
            ],
            metadata={**base, "criterion": "explicit_non_k_theory", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate algebraic K-theory structure or its absence. "
            "Cannot determine K-theory status.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


# ---------------------------------------------------------------------------
# Facade functions
# ---------------------------------------------------------------------------

def classify_motivic(space: Any) -> dict[str, Any]:
    """Run all motivic analysis functions and return a combined result dict."""
    return {
        "is_a1_invariant":                is_a1_invariant(space),
        "has_nisnevich_descent":          has_nisnevich_descent(space),
        "is_motivic_cohomology_theory":   is_motivic_cohomology_theory(space),
        "has_algebraic_k_theory_structure": has_algebraic_k_theory_structure(space),
    }


def motivic_profile(space: Any) -> dict[str, Any]:
    """Return a comprehensive motivic profile of the space."""
    classification = classify_motivic(space)
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
    "MotivicHomotopyProfile",
    "A1_HOMOTOPY_TAGS",
    "NISNEVICH_TOPOLOGY_TAGS",
    "MOTIVIC_COHOMOLOGY_TAGS",
    "ALGEBRAIC_K_THEORY_TAGS",
    "MILNOR_K_THEORY_TAGS",
    "STABLE_MOTIVIC_TAGS",
    "VOEVODSKY_TAGS",
    "MOTIVIC_SPHERE_TAGS",
    "get_named_motivic_profiles",
    "motivic_layer_summary",
    "motivic_chapter_index",
    "motivic_type_index",
    "is_a1_invariant",
    "has_nisnevich_descent",
    "is_motivic_cohomology_theory",
    "has_algebraic_k_theory_structure",
    "classify_motivic",
    "motivic_profile",
]
