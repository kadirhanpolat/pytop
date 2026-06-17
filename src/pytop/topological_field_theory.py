r"""Topological Field Theory (TFT): Atiyah-Segal axioms, cobordism hypothesis, Frobenius algebras,
Chern-Simons theory, Donaldson theory, factorization algebras, topological strings.

Key constructions and theorems
------------------------------
- Atiyah-Segal TFT axioms (Atiyah 1988, Segal 1988): a TFT of dimension n is a symmetric
  monoidal functor Z: Cob_n -> Vect_k from the cobordism category Cob_n (objects = closed
  (n-1)-manifolds, morphisms = cobordisms modulo diffeomorphism) to vector spaces over k.
  The gluing axiom (locality) encodes cutting and pasting: if M = M_1 \cup_\Sigma M_2 then
  Z(M) = Z(M_1) \circ Z(M_2). State spaces Z(\Sigma) are finite-dimensional by the
  compactness of \Sigma. The partition function Z(M) \in k for a closed n-manifold M is
  the primary invariant.

- 2D TFT \leftrightarrow Commutative Frobenius algebras (Abrams 1996, Kock 2004): every
  2-dimensional TFT is equivalent to a commutative Frobenius algebra A = Z(S^1). The
  Frobenius structure (multiplication \mu: A \otimes A \to A, unit \eta: k \to A,
  comultiplication \delta: A \to A \otimes A, counit \epsilon: A \to k) satisfies the
  Frobenius relation: (\mu \otimes 1) \circ (1 \otimes \delta) = \delta \circ \mu =
  (1 \otimes \mu) \circ (\delta \otimes 1). Handle decomposition of cobordisms corresponds
  to the pair-of-pants decomposition (genus-g surface from Frobenius operations).

- Cobordism hypothesis (Baez-Dolan 1995, Lurie 2009): a fully extended framed TFT of
  dimension n is determined by its value on the point, which must be a fully dualizable
  object in the target symmetric monoidal (\infty,n)-category C. The O(n) action on
  fully dualizable objects \simeq the space of fully extended framed TFTs. This is the
  \infty-categorical classification theorem that subsumes all lower-dimensional TFT
  classification results.

- Chern-Simons theory (Witten 1989): a 3-dimensional TFT with gauge group G, action
  S_{CS}(A) = (k/4\pi) \int_M Tr(A \wedge dA + (2/3) A \wedge A \wedge A). The
  partition function Z(M, k) is a topological invariant of 3-manifolds. Link invariants
  arise from Wilson loop operators W_R(\gamma) = Tr_R Hol_\gamma(A). For G = SU(2) and
  R = fundamental representation, Chern-Simons theory computes the Jones polynomial.
  The state space Z(S^2) carries modular tensor category structure via WZW model.

- Donaldson theory (Donaldson 1983): a 4-dimensional TFT counting anti-self-dual
  instantons of Yang-Mills connections on 4-manifolds. Donaldson invariants
  D_k(M) \in \mathbb{Z} are defined by integrating cohomology classes over the moduli
  space \mathcal{M}_k of ASD connections. Witten's reformulation (1988) as a TFT
  uses twisted N=2 supersymmetric Yang-Mills. Seiberg-Witten invariants (1994) give
  simpler invariants detecting the same smooth structure information.

- Factorization algebras (Costello-Gwilliam 2016): a framework for perturbative QFT on
  manifolds M. A prefactorization algebra F assigns a cochain complex F(U) to each open
  U \subset M, with structure maps F(U_1) \otimes ... \otimes F(U_k) \to F(V) for
  disjoint U_i \subset V, satisfying locality (Weiss cosheaf condition on the Ran space
  of finite subsets). Perturbative quantum field theories produce factorization algebras
  of quantum observables via the BV/BD formalism. Lurie's (\infty,1)-categorical
  factorization algebras correspond to E_n-algebras on \mathbb{R}^n.

- Topological string theories (Witten 1988, 1991): the A-model TFT (Gromov-Witten
  invariants, quantum cohomology, counts of holomorphic curves in a symplectic manifold)
  and B-model TFT (variations of Hodge structure, holomorphic geometry of Calabi-Yau
  manifolds). Mirror symmetry exchanges A-model on X with B-model on the mirror X^\vee.
  The topological vertex (Aganagic-Klemm-Marino-Vafa) computes all-genus Gromov-Witten
  invariants of toric Calabi-Yau 3-folds. Genus expansion: F = \sum_g \lambda^{2g-2} F_g.
"""

from __future__ import annotations

from dataclasses import dataclass

from .result import Result

# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

ATIYAH_SEGAL_TAGS: frozenset[str] = frozenset({
    "atiyah_segal", "cobordism_category", "functor_from_cobordisms",
    "symmetric_monoidal", "partition_function", "state_space",
    "gluing_axiom", "tft_axioms"
})

COBORDISM_HYPOTHESIS_TAGS: frozenset[str] = frozenset({
    "cobordism_hypothesis", "baez_dolan", "lurie_classification",
    "fully_dualizable", "framed_cobordism", "o_n_action",
    "infinity_categorical_tft", "classification_theorem"
})

FROBENIUS_ALGEBRA_TAGS: frozenset[str] = frozenset({
    "frobenius_algebra", "frobenius_structure", "commutative_frobenius",
    "two_dim_tft", "handle_decomposition", "pants_decomposition",
    "multiplication_comultiplication", "frobenius_relation"
})

EXTENDED_TFT_TAGS: frozenset[str] = frozenset({
    "extended_tft", "fully_extended", "higher_categorical",
    "bordism_bicategory", "dualizable_object", "once_extended",
    "twice_extended", "n_extended"
})

CHERN_SIMONS_TAGS: frozenset[str] = frozenset({
    "chern_simons", "three_dim_tft", "gauge_theory",
    "wilson_line", "link_invariant", "jones_polynomial",
    "wess_zumino_witten", "modular_tensor_category"
})

FACTORIZATION_ALGEBRA_TAGS: frozenset[str] = frozenset({
    "factorization_algebra", "costello_gwilliam", "local_observables",
    "prefactorization", "ran_space", "operadic_product",
    "perturbative_qft", "bd_algebra"
})

DONALDSON_TAGS: frozenset[str] = frozenset({
    "donaldson_theory", "four_manifold", "instanton",
    "yang_mills", "donaldson_invariant", "seiberg_witten",
    "gauge_group", "moduli_space_instantons"
})

TOPOLOGICAL_STRING_TAGS: frozenset[str] = frozenset({
    "topological_string", "a_model", "b_model",
    "gromov_witten", "mirror_symmetry_tft", "calabi_yau",
    "genus_expansion", "topological_vertex"
})

# ---------------------------------------------------------------------------
# TFTProfile dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TFTProfile:
    """A curated topological field theory profile."""

    key: str
    display_name: str
    tft_type: str  # "atiyah_segal" | "topological_conformal" | "extended_tft"
                   # | "factorization_algebra" | "frobenius" | "chern_simons"
                   # | "donaldson" | "topological_string"
    dimension: int  # spacetime dimension: 1, 2, 3, 4, etc.
    is_extended: bool
    has_frobenius_structure: bool
    is_oriented: bool
    has_anomaly: bool
    admits_higher_categorical_formulation: bool
    presentation_layer: int  # 1-4
    focus: str  # 300+ character description
    chapter_targets: list[str]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_tags(description: str) -> frozenset[str]:
    return frozenset(w.lower().strip(".,;:") for w in description.split())


def _representation_of(profile: TFTProfile) -> frozenset[str]:
    return _extract_tags(profile.focus)


def _matches_any(tags: frozenset[str], target: frozenset[str]) -> bool:
    return bool(tags & target)


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

def get_named_tft_profiles() -> tuple[TFTProfile, ...]:
    """Return the registry of 8 canonical topological field theory profiles."""
    return (
        TFTProfile(
            key="atiyah_segal_tft",
            display_name="Atiyah-Segal TFT — symmetric monoidal functor from cobordism category",
            tft_type="atiyah_segal",
            dimension=2,
            is_extended=False,
            has_frobenius_structure=True,
            is_oriented=True,
            has_anomaly=False,
            admits_higher_categorical_formulation=True,
            presentation_layer=2,
            focus=(
                "The Atiyah-Segal formulation of topological field theory defines a TFT as a "
                "symmetric monoidal functor Z: Cob_n -> Vect_k from the cobordism category to "
                "vector spaces. Objects in Cob_n are closed oriented (n-1)-manifolds (state spaces) "
                "and morphisms are oriented n-dimensional cobordisms up to diffeomorphism. The "
                "symmetric monoidal structure corresponds to disjoint union on manifolds and tensor "
                "product of vector spaces. The gluing axiom encodes locality: the partition function "
                "of a manifold cut along a hypersurface factors through the state space. For "
                "dimension 2, the circle S^1 maps to a Frobenius algebra (the state space Z(S^1)), "
                "and the atiyah_segal tft_axioms encode cobordism_category structure with "
                "functor_from_cobordisms giving partition_function invariants. The Frobenius "
                "structure frobenius_algebra on Z(S^1) encodes the pair-of-pants multiplication "
                "and comultiplication. This is the foundational framework for all modern TFTs, "
                "unifying quantum field theory invariants with categorical algebra via the "
                "cobordism hypothesis and higher categorical generalizations."
            ),
            chapter_targets=["50", "62", "74"],
        ),
        TFTProfile(
            key="cobordism_hypothesis_tft",
            display_name="Cobordism hypothesis TFT — Baez-Dolan, Lurie, fully dualizable, O(n)-action",
            tft_type="extended_tft",
            dimension=3,
            is_extended=True,
            has_frobenius_structure=False,
            is_oriented=False,
            has_anomaly=False,
            admits_higher_categorical_formulation=True,
            presentation_layer=4,
            focus=(
                "The cobordism hypothesis (Baez-Dolan 1995, proved by Lurie 2009) gives a complete "
                "classification of fully extended framed TFTs. A fully extended framed n-dimensional "
                "TFT is a symmetric monoidal functor from the framed_cobordism bordism_bicategory "
                "Bord_n^{fr} (with morphisms at all levels from points to n-manifolds) to a target "
                "symmetric monoidal (infinity_categorical_tft, n)-category C. The cobordism_hypothesis "
                "states: such functors are classified by fully_dualizable objects in C, and the space "
                "of such functors is equivalent to the space of fully dualizable objects. The o_n_action "
                "of the orthogonal group O(n) on fully dualizable objects encodes different framings "
                "(framed vs oriented vs unoriented vs spin). The lurie_classification theorem is a "
                "classification_theorem for (infinity,n)-categorical TFTs. The baez_dolan conjecture "
                "predicts that fully extended TFTs are entirely determined by their value on the point, "
                "which must be a once_extended, twice_extended, n_extended fully dualizable object in "
                "the target higher categorical structure. This is the deepest structural result in "
                "modern topological field theory, connecting higher category theory with manifold topology."
            ),
            chapter_targets=["52", "65", "78"],
        ),
        TFTProfile(
            key="two_dim_frobenius_tft",
            display_name="2D Frobenius TFT — commutative Frobenius algebra, pants decomposition",
            tft_type="frobenius",
            dimension=2,
            is_extended=False,
            has_frobenius_structure=True,
            is_oriented=True,
            has_anomaly=False,
            admits_higher_categorical_formulation=False,
            presentation_layer=1,
            focus=(
                "Two-dimensional oriented topological field theories are classified by commutative "
                "Frobenius algebras (Abrams 1996, Kock 2004). A commutative_frobenius algebra A has "
                "multiplication_comultiplication structure: multiplication mu: A tensor A -> A, unit "
                "eta: k -> A, comultiplication delta: A -> A tensor A, counit epsilon: A -> k, all "
                "satisfying the frobenius_relation (mu tensor 1)(1 tensor delta) = delta mu = "
                "(1 tensor mu)(delta tensor 1), plus commutativity and cocommutativity. The "
                "two_dim_tft functor Z: Cob_2 -> Vect satisfies Z(S^1) = A with the Frobenius "
                "structure coming from the pair_of_pants (multiplication), cap (unit), reverse pants "
                "(comultiplication), and cup (counit) cobordisms. The handle_decomposition of a "
                "genus-g surface is computed by the Frobenius algebra operations. The pants_decomposition "
                "theorem says every 2D cobordism factors into these elementary pieces. This gives a "
                "complete frobenius_structure classification with no higher categorical input needed, "
                "making it the most accessible example of a TFT classification theorem and the "
                "starting point for understanding the general atiyah_segal framework."
            ),
            chapter_targets=["50", "62"],
        ),
        TFTProfile(
            key="chern_simons_tft",
            display_name="Chern-Simons TFT — 3D gauge theory, Jones polynomial, modular tensor category",
            tft_type="chern_simons",
            dimension=3,
            is_extended=False,
            has_frobenius_structure=False,
            is_oriented=True,
            has_anomaly=True,
            admits_higher_categorical_formulation=True,
            presentation_layer=3,
            focus=(
                "Chern-Simons theory (Witten 1989) is a three_dim_tft gauge_theory with gauge_group G "
                "and Chern-Simons action S_{CS}(A) = (k/4pi) integral_M Tr(A wedge dA + (2/3) A wedge "
                "A wedge A) for a connection A on a principal G-bundle. The theory satisfies "
                "atiyah_segal tft_axioms as a functor Z: Cob_3 -> Vect. Key features: the "
                "partition_function Z(M, k) is a topological invariant of closed 3-manifolds; "
                "wilson_line operators W_R(gamma) = Tr_R Hol_gamma(A) produce link_invariant "
                "polynomial invariants. For G = SU(2) and fundamental representation, this gives the "
                "jones_polynomial of knots and links. The state_space Z(Sigma_g) of a genus-g surface "
                "carries modular_tensor_category structure from the wess_zumino_witten model at level k. "
                "The theory has a gravitational anomaly (has_anomaly=True): the partition function is "
                "not fully diffeomorphism-invariant but requires a framing. The chern_simons TFT admits "
                "higher categorical formulation via factorization homology and the cobordism_hypothesis "
                "framework. This is the central example connecting 3-manifold topology, quantum groups, "
                "conformal field theory, and categorical representation theory in modern mathematical physics."
            ),
            chapter_targets=["51", "63", "76"],
        ),
        TFTProfile(
            key="once_extended_tft",
            display_name="Once-extended TFT — bordism bicategory, 2-categorical structure, Frobenius",
            tft_type="extended_tft",
            dimension=2,
            is_extended=True,
            has_frobenius_structure=True,
            is_oriented=True,
            has_anomaly=False,
            admits_higher_categorical_formulation=True,
            presentation_layer=3,
            focus=(
                "A once_extended TFT of dimension 2 is a symmetric monoidal functor from the "
                "bordism_bicategory Bord_2 (2-category with objects = points, 1-morphisms = 1-manifolds "
                "with boundary, 2-morphisms = 2-dimensional cobordisms with corners) to a target "
                "2-category C. This is the first step in the extended_tft hierarchy toward the "
                "fully_extended cobordism hypothesis formulation. For oriented once_extended 2D TFTs, "
                "the value on a point must be a dualizable_object (separable symmetric Frobenius algebra "
                "object) in C. The Frobenius structure frobenius_algebra arises naturally: the once_extended "
                "higher_categorical structure refines the ordinary 2D TFT classification by remembering "
                "the point-level data. In a 2-categorical target such as Alg_k (algebras, bimodules, "
                "bimodule maps), the value on the point is a separable Frobenius algebra. The n_extended "
                "generalization leads to the full cobordism hypothesis. The bordism_bicategory has a "
                "natural symmetric monoidal structure, and twice_extended versions involve 3-categories. "
                "This example demonstrates how the frobenius_relation emerges from corner-and-gluing "
                "axioms in higher dimensional bordism categories, unifying Frobenius and extended TFT."
            ),
            chapter_targets=["51", "63", "75"],
        ),
        TFTProfile(
            key="factorization_algebra_tft",
            display_name="Factorization algebra TFT — Costello-Gwilliam, local observables, BV/BD",
            tft_type="factorization_algebra",
            dimension=4,
            is_extended=True,
            has_frobenius_structure=False,
            is_oriented=True,
            has_anomaly=True,
            admits_higher_categorical_formulation=True,
            presentation_layer=4,
            focus=(
                "Factorization algebras (costello_gwilliam 2016) provide a mathematical framework for "
                "perturbative_qft on manifolds. A prefactorization algebra F on a manifold M assigns "
                "a cochain complex F(U) of local_observables to each open subset U, with structure maps "
                "F(U_1) tensor ... tensor F(U_k) -> F(V) for disjoint U_i inside V (the operadic_product "
                "of the prefactorization structure). The ran_space of finite subsets of M organizes the "
                "locality data into the Weiss cosheaf condition: F is a factorization algebra if the "
                "Cech complex of F with respect to Weiss covers is quasi-isomorphic to F. The bd_algebra "
                "(Beilinson-Drinfeld algebra) structure arises in the classical-to-quantum deformation. "
                "Perturbative QFTs produce factorization algebras via the BV (Batalin-Vilkovisky) "
                "formalism for gauge theories. In four dimensions, factorization algebras encode "
                "the operator product expansion of four_manifold quantum field theories. The "
                "extended_tft structure of factorization algebras uses higher_categorical language: "
                "locally constant factorization algebras on R^n correspond to E_n-algebras in the "
                "n_extended sense. The theory admits_higher_categorical_formulation via Lurie's "
                "operadic_product framework and has_anomaly from quantum corrections to the BV action."
            ),
            chapter_targets=["53", "66", "79"],
        ),
        TFTProfile(
            key="donaldson_tft",
            display_name="Donaldson TFT — 4-manifolds, instantons, Yang-Mills, Seiberg-Witten",
            tft_type="donaldson",
            dimension=4,
            is_extended=False,
            has_frobenius_structure=False,
            is_oriented=True,
            has_anomaly=False,
            admits_higher_categorical_formulation=False,
            presentation_layer=3,
            focus=(
                "Donaldson theory (donaldson_theory, Donaldson 1983) is a four_manifold gauge theory "
                "TFT counting anti-self-dual instantons of yang_mills connections. Given a compact "
                "oriented Riemannian four_manifold M with gauge_group G = SU(2) or SO(3), Donaldson "
                "invariants donaldson_invariant D_k(M) in Z are defined by integrating cohomology "
                "classes over moduli_space_instantons of anti-self-dual connections (solutions to "
                "F^+ = 0 where F is the curvature and ^+ denotes self-dual projection). The "
                "instanton moduli space M_k has virtual dimension 8k - 3(1+b_1(M)) + b_2^+(M) for "
                "SU(2) bundles with second Chern class k. Witten's reformulation (1988) as a twisted "
                "N=2 super-Yang-Mills TFT satisfies the atiyah_segal axioms as a functor Cob_4 -> Vect. "
                "The seiberg_witten invariants (Seiberg-Witten 1994) provide simpler monopole equations "
                "detecting the same smooth structure information for four-manifolds with b_2^+ > 1. "
                "Donaldson's theorem: the intersection form of a smooth simply-connected closed "
                "four_manifold must be diagonalizable over Z. Donaldson theory with yang_mills gauge "
                "theory provides the foundation for understanding exotic smooth structures on R^4 "
                "and the moduli_space_instantons structure. The gauge_group action on connection space "
                "modulo gauge equivalence gives the donaldson_invariant configuration space."
            ),
            chapter_targets=["52", "64", "77"],
        ),
        TFTProfile(
            key="topological_string_tft",
            display_name="Topological string TFT — A/B-model, Gromov-Witten, mirror symmetry",
            tft_type="topological_string",
            dimension=2,
            is_extended=True,
            has_frobenius_structure=True,
            is_oriented=True,
            has_anomaly=False,
            admits_higher_categorical_formulation=True,
            presentation_layer=4,
            focus=(
                "Topological string theories (topological_string, Witten 1988, 1991) are two-dimensional "
                "TFTs arising from twisting N=2 superconformal field theories. The a_model TFT computes "
                "gromov_witten invariants: counts of holomorphic curves in a symplectic manifold X, "
                "organized into the quantum cohomology ring QH*(X). The b_model TFT encodes the "
                "holomorphic geometry of calabi_yau manifolds via variations of Hodge structure and "
                "the Kodaira-Spencer theory of gravity. mirror_symmetry_tft exchanges the a_model on "
                "a Calabi-Yau X with the b_model on the mirror calabi_yau manifold X^vee. The "
                "genus_expansion of the free energy F = sum_g lambda^{2g-2} F_g organizes all-genus "
                "invariants. The topological_vertex (Aganagic-Klemm-Marino-Vafa 2005) computes all-genus "
                "Gromov-Witten invariants of toric Calabi-Yau 3-folds via combinatorial vertex rules. "
                "The frobenius_algebra structure on the state space of the a_model encodes quantum "
                "cohomology ring structure, and the frobenius_structure satisfies the frobenius_relation "
                "from the pair-of-pants worldsheet cobordism. The topological string is an extended_tft "
                "with higher_categorical formulation: the open-closed TFT structure involves "
                "dualizable_object Calabi-Yau categories, and mirror symmetry is an equivalence of "
                "n_extended topological field theories. The genus expansion and topological vertex "
                "connect to the cobordism hypothesis via Lurie's classification at the infinity_categorical_tft level."
            ),
            chapter_targets=["51", "64", "77"],
        ),
    )


# ---------------------------------------------------------------------------
# Summary functions
# ---------------------------------------------------------------------------

def tft_summary() -> dict[str, object]:
    """Return a high-level summary of all named TFT profiles."""
    profiles = get_named_tft_profiles()
    by_type: dict[str, int] = {}
    by_dim: dict[int, int] = {}
    for p in profiles:
        by_type[p.tft_type] = by_type.get(p.tft_type, 0) + 1
        by_dim[p.dimension] = by_dim.get(p.dimension, 0) + 1
    return {
        "total": len(profiles),
        "by_type": by_type,
        "by_dimension": by_dim,
    }


def tft_type_registry() -> dict[str, list[str]]:
    """Return a mapping from tft_type -> list of profile keys."""
    registry: dict[str, list[str]] = {}
    for p in get_named_tft_profiles():
        registry.setdefault(p.tft_type, []).append(p.key)
    return registry


def tft_dimension_registry() -> dict[int, list[str]]:
    """Return a mapping from dimension -> list of profile keys."""
    registry: dict[int, list[str]] = {}
    for p in get_named_tft_profiles():
        registry.setdefault(p.dimension, []).append(p.key)
    return registry


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def is_extended_tft(description: str, *, mode: str = "symbolic") -> Result:
    """Determine whether a description corresponds to an extended TFT."""
    tags = _extract_tags(description)
    if _matches_any(tags, EXTENDED_TFT_TAGS):
        return Result.true(mode=mode, justification=["Tags match EXTENDED_TFT_TAGS"])
    if _matches_any(tags, COBORDISM_HYPOTHESIS_TAGS):
        return Result.true(mode=mode, justification=["Cobordism hypothesis implies fully extended structure"])
    if _matches_any(tags, FACTORIZATION_ALGEBRA_TAGS):
        return Result.true(mode=mode, justification=["Factorization algebras admit extended formulation"])
    if _matches_any(tags, ATIYAH_SEGAL_TAGS | FROBENIUS_ALGEBRA_TAGS):
        return Result.false(mode=mode, justification=["Classical TFT not extended by default"])
    return Result.unknown(mode=mode, justification=["Insufficient data to determine extended structure"])


def satisfies_atiyah_segal_axioms(description: str, *, mode: str = "symbolic") -> Result:
    """Determine whether a description satisfies Atiyah-Segal TFT axioms."""
    tags = _extract_tags(description)
    if _matches_any(tags, ATIYAH_SEGAL_TAGS):
        return Result.true(mode=mode, justification=["Tags match Atiyah-Segal axioms"])
    if _matches_any(tags, FROBENIUS_ALGEBRA_TAGS):
        return Result.true(mode=mode, justification=["2D TFT satisfies Atiyah-Segal via Frobenius"])
    if _matches_any(tags, CHERN_SIMONS_TAGS):
        return Result.true(mode=mode, justification=["Chern-Simons satisfies Atiyah-Segal axioms"])
    if _matches_any(tags, DONALDSON_TAGS):
        return Result.true(mode=mode, justification=["Donaldson theory satisfies Atiyah-Segal axioms"])
    return Result.unknown(mode=mode, justification=["Cannot verify Atiyah-Segal axioms from description"])


def has_frobenius_algebra_structure(description: str, *, mode: str = "symbolic") -> Result:
    """Determine whether a description admits Frobenius algebra structure."""
    tags = _extract_tags(description)
    if _matches_any(tags, FROBENIUS_ALGEBRA_TAGS):
        return Result.true(mode=mode, justification=["Tags match Frobenius algebra structure"])
    if _matches_any(tags, TOPOLOGICAL_STRING_TAGS):
        return Result.true(mode=mode, justification=["Topological string theories have Frobenius structure"])
    if _matches_any(tags, COBORDISM_HYPOTHESIS_TAGS):
        return Result.false(mode=mode, justification=["Extended TFTs via cobordism hypothesis don't require Frobenius"])
    if _matches_any(tags, FACTORIZATION_ALGEBRA_TAGS):
        return Result.false(mode=mode, justification=["Factorization algebras generalize beyond Frobenius"])
    return Result.unknown(mode=mode, justification=["Insufficient data to determine Frobenius structure"])


def admits_higher_categorical_formulation(description: str, *, mode: str = "symbolic") -> Result:
    """Determine whether a description admits a higher categorical formulation."""
    tags = _extract_tags(description)
    if _matches_any(tags, COBORDISM_HYPOTHESIS_TAGS):
        return Result.true(mode=mode, justification=["Cobordism hypothesis is fundamentally ∞-categorical"])
    if _matches_any(tags, EXTENDED_TFT_TAGS):
        return Result.true(mode=mode, justification=["Extended TFTs require higher categorical language"])
    if _matches_any(tags, FACTORIZATION_ALGEBRA_TAGS):
        return Result.true(mode=mode, justification=["Factorization algebras use ∞-categorical structure"])
    if _matches_any(tags, FROBENIUS_ALGEBRA_TAGS) and not _matches_any(tags, EXTENDED_TFT_TAGS):
        return Result.false(mode=mode, justification=["Classical Frobenius formulation is 1-categorical"])
    return Result.unknown(mode=mode, justification=["Higher categorical formulation unclear from description"])


# ---------------------------------------------------------------------------
# Facade functions
# ---------------------------------------------------------------------------

def classify_tft(description: str, *, mode: str = "symbolic") -> dict[str, Result]:
    """Classify a TFT description across all four analysis dimensions."""
    return {
        "is_extended_tft": is_extended_tft(description, mode=mode),
        "satisfies_atiyah_segal_axioms": satisfies_atiyah_segal_axioms(description, mode=mode),
        "has_frobenius_algebra_structure": has_frobenius_algebra_structure(description, mode=mode),
        "admits_higher_categorical_formulation": admits_higher_categorical_formulation(description, mode=mode),
    }


def tft_profile_report(profile: TFTProfile, *, mode: str = "symbolic") -> dict[str, object]:
    """Generate a full analysis report for a TFTProfile."""
    analysis = classify_tft(profile.focus, mode=mode)
    return {
        "key": profile.key,
        "display_name": profile.display_name,
        "tft_type": profile.tft_type,
        "dimension": profile.dimension,
        "is_extended": profile.is_extended,
        "has_frobenius_structure": profile.has_frobenius_structure,
        "is_oriented": profile.is_oriented,
        "has_anomaly": profile.has_anomaly,
        "admits_higher_categorical_formulation": profile.admits_higher_categorical_formulation,
        "analysis": analysis,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "TFTProfile",
    "ATIYAH_SEGAL_TAGS", "COBORDISM_HYPOTHESIS_TAGS", "FROBENIUS_ALGEBRA_TAGS",
    "EXTENDED_TFT_TAGS", "CHERN_SIMONS_TAGS", "FACTORIZATION_ALGEBRA_TAGS",
    "DONALDSON_TAGS", "TOPOLOGICAL_STRING_TAGS",
    "get_named_tft_profiles",
    "tft_summary", "tft_type_registry", "tft_dimension_registry",
    "is_extended_tft", "satisfies_atiyah_segal_axioms",
    "has_frobenius_algebra_structure", "admits_higher_categorical_formulation",
    "classify_tft", "tft_profile_report",
]
