r"""Higher categories: (∞,1)-categories, quasi-categories, Kan complexes, complete Segal spaces,
stable ∞-categories, ∞-operads, ∞-toposes, enriched categories.

Key theorems and constructions implemented
------------------------------------------
- (∞,1)-categories: objects, 1-morphisms, k-morphisms for k≥2 all invertible.
  Models include quasi-categories (Joyal), Kan complexes as ∞-groupoids, complete
  Segal spaces (Rezk), Segal categories, and simplicially enriched categories.
  The Quillen equivalences between all these models are encoded in the Bergner model
  structure on simplicial categories and Joyal's model structure on sSet.

- Quasi-categories (Joyal 2002, Lurie 2009): a simplicial set X is a quasi-category
  if every inner horn Lambda^n_k -> X (0 < k < n) extends to Delta^n -> X. Objects
  are 0-simplices, morphisms are 1-simplices, and composition is given by filling
  2-horns (Lambda^2_1). The homotopy category hX has objects X_0, morphisms pi_0(X_1),
  and composition is pi_0 of horn fillers. The Joyal model structure on sSet has fibrant
  objects = quasi-categories and weak equivalences = categorical equivalences (equivalences
  of quasi-categories). This is distinct from the classical Kan-Quillen model structure
  (which models homotopy types).

- Kan complexes and ∞-groupoids: a simplicial set X is a Kan complex if ALL horns
  (including outer horns Lambda^n_0 and Lambda^n_n) extend. Kan complexes model
  ∞-groupoids where all morphisms are invertible up to coherent homotopy. The
  Grothendieck homotopy hypothesis states that ∞-groupoids are equivalent to homotopy
  types (topological spaces up to weak homotopy equivalence). Concretely: the singular
  complex functor Sing: Top -> sSet lands in Kan complexes, and geometric realization
  |−|: sSet -> Top is its left adjoint; this Quillen adjunction (Kan-Quillen model
  structure) implements the equivalence between Kan complexes and CW-complexes.

- Complete Segal spaces (Rezk 2001): a bisimplicial set W: Delta^op -> sSet satisfying
  (1) the Segal condition W_n \simeq W_1 x_{W_0} ... x_{W_0} W_1 (n-fold iterated
  pullback over W_0), meaning composition is essentially unique and associative up to
  homotopy; and (2) the completeness condition: the map W_0 -> W_hoequiv (subspace of
  homotopy equivalences in W_1) is a weak equivalence. This completeness encodes that
  homotopy equivalences in the ∞-category are detected by identity morphisms. The
  Bergner model structure on sSet-categories and Rezk's model structure on bisimplicial
  sets are Quillen equivalent, as are both to Joyal's model structure and to Segal
  categories.

- Lurie's ∞-categorical machinery (Higher Topos Theory, 2009): the ∞-categorical Yoneda
  lemma holds: for a quasi-category C and an object x, the functor j(x): C^op -> S
  (presheaves of spaces) given by y |-> Map_C(y, x) is fully faithful. Limits and
  colimits in a quasi-category C are defined as terminal/initial objects in the
  appropriate slice quasi-categories of functor quasi-categories. An adjunction between
  quasi-categories L: C <-> D: R is given by a unit transformation eta: id -> RL
  satisfying the triangle identities up to coherent homotopy. An ∞-topos is an
  ∞-category X that arises as a left exact localization of a presheaf ∞-category P(C)
  = Fun(C^op, S) (or equivalently, satisfies Lurie's ∞-categorical Giraud axioms:
  colimits are universal, coproducts are disjoint, and groupoid objects are effective).

- Stable ∞-categories: an ∞-category C is stable if (1) it has a zero object 0
  (both initial and final), (2) every morphism has a fiber and a cofiber (i.e., all
  pushouts and pullbacks exist), and (3) a square is a pushout iff it is a pullback
  (all squares are both bicartesian). Every stable ∞-category has a triangulated
  homotopy category (with suspension Sigma = cofiber of id -> 0). Key examples: the
  ∞-category of spectra Sp (the initial stable ∞-category with a unit), the derived
  ∞-category D(R) for a ring R (nerves of model categories of chain complexes), and
  the stable ∞-category of A-modules Mod_A for an E_∞-ring spectrum A. A t-structure
  on a stable ∞-category C is a pair (C_{>=0}, C_{<=0}) of full subcategories closed
  under positive/negative shifts satisfying the usual axioms; the heart C^♥ = C_{>=0}
  ∩ C_{<=0} is an abelian category.

- ∞-operads and ∞-algebras (Lurie, Higher Algebra 2017): in Lurie's framework, an
  ∞-operad is a functor O^⊗ -> N(Fin_*) satisfying certain Segal conditions, where
  Fin_* is the category of finite pointed sets (with basepoint). An ∞-algebra over an
  ∞-operad O in a symmetric monoidal ∞-category (C^⊗ -> N(Fin_*)) is a map of
  ∞-operads O^⊗ -> C^⊗ over N(Fin_*). Key examples: the E_n ∞-operad (from the
  operad of little n-disks); E_n-algebras generalize E_1 = A_∞ (associative up to
  all coherences) and E_∞ = commutative algebras. The Ass ∞-operad gives A_∞-algebras.
  Spectra with symmetric monoidal product (smash product of spectra ∧ giving the
  symmetric monoidal ∞-category Sp^⊗) admit E_∞-ring spectra as algebras.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result

# ---------------------------------------------------------------------------
# HigherCategoryProfile dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HigherCategoryProfile:
    """A curated higher category theory example."""

    key: str
    display_name: str
    category_type: str          # "quasi_category", "kan_complex", "segal_space",
                                # "complete_segal_space", "simplicial_category",
                                # "stable_infinity", "infinity_topos", "enriched_category"
    model_type: str             # "simplicial_set", "bisimplicial_set", "enriched", "general"
    is_stable: bool
    has_all_limits: bool
    has_all_colimits: bool
    is_presentable: bool
    has_t_structure: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

QUASI_CATEGORY_TAGS: frozenset[str] = frozenset({
    "quasi_category",
    "inner_horn_filling",
    "joyal_model",
    "categorical_equivalence",
    "quasi_functor",
    "joyal_fibration",
    "nerve_functor",
    "homotopy_coherent",
})

KAN_COMPLEX_TAGS: frozenset[str] = frozenset({
    "kan_complex",
    "kan_fibration",
    "infinity_groupoid",
    "horn_filling_all",
    "homotopy_type",
    "grothendieck_homotopy",
    "kan_quillen_model",
    "fibrant_simplicial_set",
})

SEGAL_SPACE_TAGS: frozenset[str] = frozenset({
    "segal_space",
    "complete_segal_space",
    "rezk_model",
    "segal_condition",
    "completeness_condition",
    "bisimplicial_set",
    "segal_category",
    "css_model",
})

STABLE_INFINITY_TAGS: frozenset[str] = frozenset({
    "stable_infinity_category",
    "stable_category",
    "spectra_category",
    "triangulated_infinity",
    "exact_triangle_infinity",
    "zero_object_infinity",
    "pushout_pullback_stable",
    "derived_infinity_category",
})

INFINITY_TOPOS_TAGS: frozenset[str] = frozenset({
    "infinity_topos",
    "infinity_sheaf_topos",
    "left_exact_localization",
    "infinity_giraud",
    "presentable_infinity",
    "accessible_infinity",
    "higher_topos",
    "lurie_topos",
})

ADJUNCTION_TAGS: frozenset[str] = frozenset({
    "infinity_adjunction",
    "unit_counit_infinity",
    "infinity_functor",
    "right_adjoint_infinity",
    "left_adjoint_infinity",
    "adjoint_functor_theorem",
    "infinity_limit_colimit",
    "yoneda_infinity",
})

MODEL_CATEGORY_TAGS: frozenset[str] = frozenset({
    "model_category",
    "quillen_model",
    "cofibration",
    "fibration_mc",
    "weak_equivalence",
    "quillen_adjunction",
    "left_proper_model",
    "right_proper_model",
})

ENRICHED_CATEGORY_TAGS: frozenset[str] = frozenset({
    "enriched_category",
    "simplicially_enriched",
    "dg_category",
    "spectral_enrichment",
    "bergner_model",
    "dwyer_kan",
    "hammock_localization",
    "simplicial_localization",
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

def get_named_higher_category_profiles() -> tuple[HigherCategoryProfile, ...]:
    """Return the registry of canonical higher category theory examples."""
    return (
        HigherCategoryProfile(
            key="quasi_category",
            display_name="Quasi-category (Joyal) — inner horn filling, homotopy coherent composition",
            category_type="quasi_category",
            model_type="simplicial_set",
            is_stable=False,
            has_all_limits=True,
            has_all_colimits=True,
            is_presentable=False,
            has_t_structure=False,
            presentation_layer="main_text",
            focus=(
                "Quasi-categories are the primary model for (∞,1)-categories developed by "
                "Joyal (2002) and extensively studied by Lurie (2009, Higher Topos Theory). "
                "A simplicial set X is a quasi-category if every inner horn Lambda^n_k -> X "
                "(0 < k < n, the inner horn condition) extends to a map Delta^n -> X. "
                "This extension is not required to be unique, encoding the homotopy-coherent "
                "nature of composition. Objects are 0-simplices X_0, morphisms are 1-simplices "
                "X_1, and the composition of f: x -> y and g: y -> z is a 1-simplex h fitting "
                "into a 2-simplex filling Lambda^2_1. The homotopy category hX has objects X_0 "
                "and hom-sets pi_0(Map_X(x, y)) where Map_X(x, y) = the Kan complex of "
                "morphisms from x to y (the mapping space). The Joyal model structure on sSet "
                "has: cofibrations = monomorphisms, fibrant objects = quasi-categories, and "
                "weak equivalences = categorical equivalences (inner hom-bijective on pi_0 of "
                "mapping spaces). This is distinct from the Kan-Quillen model structure "
                "(fibrant = Kan complex, weak eq = weak homotopy equivalences). Quasi-categories "
                "have all limits and colimits (defined as terminal/initial objects in slice "
                "quasi-categories), and the nerve functor N: Cat -> sSet lands in quasi-categories, "
                "showing that ordinary categories are quasi-categories with unique horn fillers."
            ),
            chapter_targets=("45", "60", "72"),
        ),
        HigherCategoryProfile(
            key="kan_complex_groupoid",
            display_name="Kan complex — all horns fill, ∞-groupoid, Grothendieck homotopy hypothesis",
            category_type="kan_complex",
            model_type="simplicial_set",
            is_stable=False,
            has_all_limits=True,
            has_all_colimits=True,
            is_presentable=False,
            has_t_structure=False,
            presentation_layer="main_text",
            focus=(
                "Kan complexes are simplicial sets X in which ALL horns Lambda^n_k -> X "
                "(for all 0 <= k <= n, including outer horns k=0 and k=n) extend to Delta^n. "
                "The outer horn filling encodes the invertibility of morphisms: the filler of "
                "Lambda^2_0 (given f: x -> y and g: x -> z) gives a 'right inverse', and "
                "Lambda^2_2 gives a 'left inverse', up to homotopy. Thus Kan complexes model "
                "∞-groupoids — (∞,1)-categories where all morphisms are invertible up to all "
                "higher homotopies. The Grothendieck homotopy hypothesis (proved in various "
                "forms by Quillen, Whitehead, and others) states that ∞-groupoids are equivalent "
                "to homotopy types: the singular complex functor Sing: Top -> sSet lands in Kan "
                "complexes and its left adjoint geometric realization |−|: sSet -> Top implements "
                "the Quillen equivalence (Kan-Quillen model structure) between Kan complexes and "
                "spaces. Concretely, for a CW-complex X, |Sing(X)| -> X is a weak homotopy "
                "equivalence. The ∞-groupoid pi_{<=∞}(X) associated to X encodes all homotopy "
                "groups pi_n(X) and their coherent actions. Kan fibrations (horns fill for "
                "p: X -> Y, relative) are the fibrations in the Kan-Quillen model structure."
            ),
            chapter_targets=("45", "60", "72"),
        ),
        HigherCategoryProfile(
            key="complete_segal_space",
            display_name="Complete Segal space (Rezk) — bisimplicial, Segal + completeness, Bergner equiv",
            category_type="complete_segal_space",
            model_type="bisimplicial_set",
            is_stable=False,
            has_all_limits=True,
            has_all_colimits=True,
            is_presentable=False,
            has_t_structure=False,
            presentation_layer="main_text",
            focus=(
                "Complete Segal spaces (CSS) were introduced by Rezk (2001) as a model for "
                "(∞,1)-categories using bisimplicial sets W: Delta^op -> sSet. Two conditions "
                "are required: (1) the Segal condition: the Segal maps W_n -> W_1 x_{W_0} ... "
                "x_{W_0} W_1 (n-fold pullback) are weak equivalences for all n >= 2. This says "
                "n-tuples of composable morphisms are determined up to homotopy by their "
                "individual morphisms, encoding homotopy-coherent composition. (2) The "
                "completeness condition: the map W_0 -> W_hoequiv (from objects W_0 into the "
                "space of homotopy equivalences inside W_1) is a weak equivalence. This says "
                "equivalences in the ∞-category are detected by identities — preventing "
                "distinct but equivalent objects from being genuinely different. Rezk proved "
                "a model structure on bisimplicial sets (Reedy model structure localized) with "
                "fibrant objects = CSS. Bergner's theorem (2007): there are Quillen equivalences "
                "between (a) Joyal's model structure on sSet (quasi-categories), (b) Rezk's CSS "
                "model, (c) Segal categories (simplicial spaces with discrete W_0), and (d) "
                "Bergner's model structure on sSet-enriched categories. All four models present "
                "the same (∞,2)-category of (∞,1)-categories."
            ),
            chapter_targets=("45", "60", "72"),
        ),
        HigherCategoryProfile(
            key="stable_infinity_category",
            display_name="Stable ∞-category — Sp, D(R), triangulated homotopy, t-structure",
            category_type="stable_infinity",
            model_type="general",
            is_stable=True,
            has_all_limits=True,
            has_all_colimits=True,
            is_presentable=False,
            has_t_structure=True,
            presentation_layer="main_text",
            focus=(
                "A stable ∞-category C (Lurie, Higher Algebra §1) is an ∞-category with: "
                "(1) a zero object 0 (both initial and terminal), (2) all pushouts and "
                "pullbacks exist, and (3) a square is a pushout if and only if it is a pullback "
                "(all squares are bicartesian). The suspension functor Sigma: C -> C is defined "
                "as Sigma(X) = cofiber(X -> 0) = pushout of 0 <- X -> 0, and the loop functor "
                "Omega = fiber(0 -> X) = pullback of 0 -> X <- 0. Stability means Sigma and "
                "Omega are inverse equivalences. The homotopy category hC of a stable ∞-category "
                "is triangulated: exact triangles are the images of cofiber sequences. Primary "
                "examples: the ∞-category of spectra Sp (the initial stable ∞-category with "
                "unit S^0), the derived ∞-category D(R) for a ring R (localization of the "
                "category of chain complexes at quasi-isomorphisms), and Mod_A for an E_∞-ring A. "
                "A t-structure on C is a pair (C_{>=0}, C_{<=0}) with C_{>=0}[−1] ⊂ C_{>=0}, "
                "C_{<=0}[1] ⊂ C_{<=0}, Hom(C_{>=0}, C_{<=0}[−1]) = 0, and C = C_{>=0} * C_{<=0}. "
                "The heart C^♥ = C_{>=0} ∩ C_{<=0} is an abelian category. Truncation functors "
                "tau_{>=0}: C -> C_{>=0} and tau_{<=0}: C -> C_{<=0} are right and left adjoints."
            ),
            chapter_targets=("45", "60", "72"),
        ),
        HigherCategoryProfile(
            key="presentable_infinity_category",
            display_name="Presentable ∞-category — accessible localization of P(C), adjoint functor thm",
            category_type="quasi_category",
            model_type="simplicial_set",
            is_stable=False,
            has_all_limits=True,
            has_all_colimits=True,
            is_presentable=True,
            has_t_structure=False,
            presentation_layer="main_text",
            focus=(
                "A presentable ∞-category (Lurie, HTT §5.5) is an ∞-category C that is "
                "accessible (has a small set of generators under filtered colimits) and "
                "admits all small colimits. Equivalently, C is a presentable ∞-category "
                "iff it arises as an accessible localization L: P(A) <-> C: i of the "
                "presheaf ∞-category P(A) = Fun(A^op, S) for some small ∞-category A. "
                "Here S = the ∞-category of spaces (Kan complexes). Presentable ∞-categories "
                "automatically have all small limits (by the adjoint functor theorem). The "
                "∞-categorical adjoint functor theorem (Lurie): a functor F: C -> D between "
                "presentable ∞-categories has a right adjoint iff it preserves small colimits; "
                "it has a left adjoint iff it preserves limits and is accessible. This is the "
                "∞-categorical upgrade of the classical adjoint functor theorem (GAFT). The "
                "∞-category of presentable ∞-categories with colimit-preserving functors is "
                "itself well-behaved: tensor product C ⊗ D classifies bilinear functors, and "
                "Fun^L(C, D) (colimit-preserving functors) is again presentable. Every ∞-topos "
                "is in particular a presentable ∞-category, and the ∞-categorical Yoneda "
                "embedding j: A -> P(A) is fully faithful with P(A) presentable."
            ),
            chapter_targets=("45", "60", "72"),
        ),
        HigherCategoryProfile(
            key="infinity_topos",
            display_name="∞-topos (Lurie) — left exact localization, Giraud axioms, ∞-sheaves",
            category_type="infinity_topos",
            model_type="general",
            is_stable=False,
            has_all_limits=True,
            has_all_colimits=True,
            is_presentable=True,
            has_t_structure=False,
            presentation_layer="main_text",
            focus=(
                "An ∞-topos (Lurie, HTT §6) is a presentable ∞-category X satisfying the "
                "∞-categorical Giraud axioms: (1) colimits in X are universal (i.e., pullback "
                "along any morphism preserves colimits), (2) coproducts are disjoint (X ×_{X+Y} "
                "Y = ∅ for any X, Y), and (3) every groupoid object in X is effective (i.e., "
                "the colimit of a simplicial object given by a Cech nerve is the correct "
                "quotient). Equivalently, X is an ∞-topos iff it is an accessible left exact "
                "localization of a presheaf ∞-category P(C) = Fun(C^op, S). Examples: the "
                "∞-category of spaces S = P(*) is the terminal ∞-topos. For a site (C, J), "
                "the ∞-category of ∞-sheaves Shv_∞(C, J) (sheaves of ∞-groupoids / spaces "
                "satisfying ∞-categorical descent) is an ∞-topos. The ∞-topos associated to a "
                "topological space X is Shv_∞(X) = sheaves of spaces on X. Descent: an object "
                "F in an ∞-topos satisfies descent (hypercompleteness is the condition that "
                "F satisfies descent for all hypercoverings). The slice X/A of an ∞-topos X "
                "over any object A is again an ∞-topos. Geometric morphisms between ∞-toposes "
                "are adjoint pairs (f^*, f_*) with f^* left exact."
            ),
            chapter_targets=("45", "60", "72"),
        ),
        HigherCategoryProfile(
            key="dg_category",
            display_name="dg-category — Tabuada model, dg-nerve, stable ∞-cat, Bondal-Kapranov pretriangulated",
            category_type="enriched_category",
            model_type="enriched",
            is_stable=True,
            has_all_limits=False,
            has_all_colimits=False,
            is_presentable=False,
            has_t_structure=True,
            presentation_layer="main_text",
            focus=(
                "A dg-category (differential graded category) is a category enriched over "
                "chain complexes (dg-modules over a commutative ring k): for any two objects "
                "x, y, the hom-set Hom(x, y) is a cochain complex, and composition is a "
                "map of complexes. dg-categories are the linear algebraic analogues of "
                "∞-categories. Tabuada (2005) constructed a model structure on the category "
                "of small dg-categories with weak equivalences = quasi-equivalences (DK-equivalences "
                "on the level of H^0 and quasi-isomorphisms on hom-complexes). Lurie's dg-nerve "
                "construction N_{dg}: dgCat_k -> sSet sends a dg-category A to a quasi-category "
                "N_{dg}(A) whose mapping spaces are the truncations of the hom-complexes. "
                "The dg-nerve of a pretriangulated dg-category is a stable ∞-category, "
                "providing the bridge between dg-algebra and ∞-categorical stable homotopy "
                "theory. A dg-category A is pretriangulated (Bondal-Kapranov 1990) if the "
                "Yoneda image A -> H^0(A)-mod lands in complexes closed under shifts and "
                "cones — equivalently if the homotopy category H^0(A) is triangulated. "
                "The derived category D(A) of a dg-algebra A is an example of both a "
                "triangulated category and (via the dg-nerve) a stable ∞-category. "
                "dg-categories have t-structures inherited from their underlying abelian "
                "or triangulated categories, but they do not automatically have all limits."
            ),
            chapter_targets=("45", "60", "72"),
        ),
        HigherCategoryProfile(
            key="model_category_quillen",
            display_name="Quillen model category — presents ∞-category, Dwyer-Kan localization, hammock",
            category_type="enriched_category",
            model_type="general",
            is_stable=False,
            has_all_limits=True,
            has_all_colimits=True,
            is_presentable=False,
            has_t_structure=False,
            presentation_layer="main_text",
            focus=(
                "Quillen model categories (Quillen 1967) provide presentations of ∞-categories "
                "via the Dwyer-Kan localization / hammock localization construction. A model "
                "category M is a complete and cocomplete category with three distinguished "
                "classes (weak equivalences W, cofibrations C, fibrations F) satisfying the "
                "two-out-of-three property for W, the retract axiom, and the lifting/factorization "
                "axioms. The associated ∞-category N(M)[W^{-1}] (Dwyer-Kan localization of the "
                "nerve at W) is the ∞-categorical localization; equivalently, the hammock "
                "localization L^H(M, W) is a simplicially enriched category whose classifying "
                "space is the mapping space of the ∞-category. Simplicial model categories "
                "(enriched over sSet with compatibility conditions) present ∞-categories directly: "
                "the underlying quasi-category is the coherent nerve N(M^cf) of the full "
                "subcategory of cofibrant-fibrant objects. Left Bousfield localization L_S M "
                "(inverting a set S of morphisms) produces a new model structure on the same "
                "underlying category with more weak equivalences, presenting the left localization "
                "of the ∞-category. Model categories have all limits and colimits by assumption; "
                "the homotopy category Ho(M) = M[W^{-1}] is the localization. The Quillen "
                "adjunction F: M <-> N: G lifts to an adjunction of ∞-categories."
            ),
            chapter_targets=("45", "60", "72"),
        ),
    )


# ---------------------------------------------------------------------------
# Summary / index functions
# ---------------------------------------------------------------------------

def higher_category_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_higher_category_profiles()
    ))


def higher_category_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_higher_category_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {ch: tuple(keys) for ch, keys in sorted(chapter_map.items())}


def higher_category_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from category_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_higher_category_profiles():
        index.setdefault(p.category_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_infinity_categorical(space: Any) -> Result:
    """Check whether the space/structure is ∞-categorical (models an (∞,1)-category).

    Quasi-categories, Kan complexes, complete Segal spaces, stable ∞-categories, and
    ∞-toposes are all explicit models of (∞,1)-categories. Model categories and
    enriched categories present ∞-categories via localization.

    Decision layers
    ---------------
    1. QUASI_CATEGORY_TAGS | KAN_COMPLEX_TAGS -> true (explicit ∞-category model).
    2. SEGAL_SPACE_TAGS | STABLE_INFINITY_TAGS | INFINITY_TOPOS_TAGS -> true
       (recognized ∞-categorical models).
    3. MODEL_CATEGORY_TAGS | ENRICHED_CATEGORY_TAGS -> true (present ∞-categories
       via Dwyer-Kan localization or dg-nerve).
    4. Strict 1-categorical tags -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    explicit_infinity = QUASI_CATEGORY_TAGS | KAN_COMPLEX_TAGS
    if _matches_any(tags, explicit_infinity):
        witness = next(t for t in tags if t in explicit_infinity)
        return Result.true(
            mode="theorem",
            value="explicit_infinity_category",
            justification=[
                f"Tag {witness!r}: quasi-categories (inner horn filling) and Kan complexes "
                "(all horns fill, ∞-groupoids) are primary models of (∞,1)-categories. "
                "The Joyal model structure presents quasi-categories as fibrant objects, "
                "and Kan complexes are fibrant in the Kan-Quillen model structure.",
            ],
            metadata={**base, "criterion": "explicit_infinity_category", "witness": witness},
        )

    recognized_models = SEGAL_SPACE_TAGS | STABLE_INFINITY_TAGS | INFINITY_TOPOS_TAGS
    if _matches_any(tags, recognized_models):
        witness = next(t for t in tags if t in recognized_models)
        return Result.true(
            mode="theorem",
            value="recognized_infinity_model",
            justification=[
                f"Tag {witness!r}: complete Segal spaces (Rezk), stable ∞-categories, "
                "and ∞-toposes (Lurie) are recognized models of (∞,1)-categories, "
                "Quillen-equivalent to quasi-categories via Bergner's theorem.",
            ],
            metadata={**base, "criterion": "recognized_infinity_model", "witness": witness},
        )

    presents_infinity = MODEL_CATEGORY_TAGS | ENRICHED_CATEGORY_TAGS
    if _matches_any(tags, presents_infinity):
        witness = next(t for t in tags if t in presents_infinity)
        return Result.true(
            mode="theorem",
            value="presents_infinity_category",
            justification=[
                f"Tag {witness!r}: model categories and enriched categories present "
                "∞-categories via the Dwyer-Kan hammock localization (model cats) or "
                "the dg-nerve / coherent nerve (enriched cats). These are not themselves "
                "∞-categories but functorially present them.",
            ],
            metadata={**base, "criterion": "presents_infinity_category", "witness": witness},
        )

    strict_1_cat = {"strict_1_category", "ordinary_category", "set_category"}
    if _matches_any(tags, strict_1_cat):
        witness = next(t for t in tags if t in strict_1_cat)
        return Result.false(
            mode="theorem",
            value="strict_1_category_not_infinity",
            justification=[
                f"Tag {witness!r}: a strict 1-category has no higher morphisms — it is "
                "not an ∞-category in the proper sense (though every 1-category embeds "
                "into the ∞-categorical world via the nerve functor N: Cat -> sSet).",
            ],
            metadata={**base, "criterion": "strict_category", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate an ∞-categorical structure. Cannot determine whether "
            "the space/structure models an (∞,1)-category.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def is_stable_infinity_category(space: Any) -> Result:
    """Check whether the structure is a stable ∞-category.

    A stable ∞-category has a zero object, all pushouts/pullbacks, and pushout squares
    are exactly pullback squares. The homotopy category is triangulated.
    Examples: Sp (spectra), D(R) (derived ∞-category), dg-nerve of pretriangulated dg-cats.

    Decision layers
    ---------------
    1. STABLE_INFINITY_TAGS -> true.
    2. Explicit stable structure tags -> true.
    3. Tags ruling out stability (∞-toposes, Segal spaces, Kan complexes) -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, STABLE_INFINITY_TAGS):
        witness = next(t for t in tags if t in STABLE_INFINITY_TAGS)
        return Result.true(
            mode="theorem",
            value="stable_infinity_category",
            justification=[
                f"Tag {witness!r}: a stable ∞-category has a zero object, all pushouts "
                "and pullbacks, and bicartesian squares. The homotopy category is "
                "triangulated with suspension Sigma = cofiber(X -> 0).",
            ],
            metadata={**base, "criterion": "stable_infinity_tags", "witness": witness},
        )

    explicit_stable = {"spectra_category", "derived_infinity_category",
                       "dg_category", "stable_category"}
    if _matches_any(tags, explicit_stable):
        witness = next(t for t in tags if t in explicit_stable)
        return Result.true(
            mode="theorem",
            value="stable_infinity_category",
            justification=[
                f"Tag {witness!r}: the ∞-category of spectra Sp, derived ∞-categories D(R), "
                "and dg-nerves of pretriangulated dg-categories are stable ∞-categories. "
                "These form the categorical backbone of modern stable homotopy theory.",
            ],
            metadata={**base, "criterion": "explicit_stable_type", "witness": witness},
        )

    not_stable = {"infinity_topos", "segal_space", "kan_complex"}
    if _matches_any(tags, not_stable):
        witness = next(t for t in tags if t in not_stable)
        return Result.false(
            mode="theorem",
            value="not_stable_infinity_category",
            justification=[
                f"Tag {witness!r}: ∞-toposes, Segal spaces, and Kan complexes are NOT "
                "stable ∞-categories. ∞-toposes are presentable but not stable (they have "
                "an initial object ∅ and a final object *, not a zero object). Kan complexes "
                "model ∞-groupoids, which are stable only in trivial cases.",
            ],
            metadata={**base, "criterion": "not_stable", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate stability of the ∞-category. Cannot determine whether "
            "pushout squares are pullback squares without more information.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def has_all_limits_and_colimits(space: Any) -> Result:
    """Check whether the ∞-category has all small limits and colimits.

    ∞-toposes and presentable ∞-categories have all small limits and colimits.
    Quasi-categories also admit all limits and colimits (as terminal/initial
    objects in slice functor ∞-categories). dg-categories do not in general.

    Decision layers
    ---------------
    1. INFINITY_TOPOS_TAGS | ADJUNCTION_TAGS -> true (∞-toposes and presentable cats).
    2. Explicit presentability or quasi-category tags -> true.
    3. dg-categories or explicit incompleteness -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    complete_cocomplete = INFINITY_TOPOS_TAGS | ADJUNCTION_TAGS
    if _matches_any(tags, complete_cocomplete):
        witness = next(t for t in tags if t in complete_cocomplete)
        return Result.true(
            mode="theorem",
            value="has_all_limits_and_colimits",
            justification=[
                f"Tag {witness!r}: ∞-toposes are presentable and have all small limits "
                "and colimits. Presentable ∞-categories have all colimits by definition "
                "and all limits by the adjoint functor theorem (Lurie, HTT 5.5.2.4). "
                "Adjunction data implies the existence of limits via right adjoints.",
            ],
            metadata={**base, "criterion": "infinity_topos_or_adjunction", "witness": witness},
        )

    quasi_presentable = {"presentable_infinity", "accessible_infinity", "quasi_category"}
    if _matches_any(tags, quasi_presentable):
        witness = next(t for t in tags if t in quasi_presentable)
        return Result.true(
            mode="theorem",
            value="has_all_limits_and_colimits",
            justification=[
                f"Tag {witness!r}: presentable and accessible ∞-categories have all small "
                "limits and colimits. Quasi-categories also have all limits and colimits "
                "as terminal/initial objects in appropriate slice quasi-categories.",
            ],
            metadata={**base, "criterion": "presentable_or_quasi_category", "witness": witness},
        )

    incomplete = {"dg_category", "not_complete", "no_limits"}
    if _matches_any(tags, incomplete):
        witness = next(t for t in tags if t in incomplete)
        return Result.false(
            mode="theorem",
            value="does_not_have_all_limits_colimits",
            justification=[
                f"Tag {witness!r}: dg-categories do not automatically have all limits and "
                "colimits — they are enriched categories, not ∞-categories. A dg-category "
                "may have a triangulated homotopy category without having ∞-categorical "
                "limits. Explicit 'not_complete' or 'no_limits' tags confirm this.",
            ],
            metadata={**base, "criterion": "dg_or_not_complete", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate completeness/cocompleteness. Cannot determine whether "
            "the ∞-category has all small limits and colimits.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


def is_presentable_infinity_category(space: Any) -> Result:
    """Check whether the ∞-category is presentable.

    A presentable ∞-category is an accessible ∞-category with all small colimits,
    equivalently an accessible localization of a presheaf ∞-category P(C).
    ∞-toposes are presentable. dg-categories and small categories are not.

    Decision layers
    ---------------
    1. INFINITY_TOPOS_TAGS -> true (∞-toposes are presentable).
    2. Explicit presentability tags | ADJUNCTION_TAGS -> true.
    3. Tags ruling out presentability -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, INFINITY_TOPOS_TAGS):
        witness = next(t for t in tags if t in INFINITY_TOPOS_TAGS)
        return Result.true(
            mode="theorem",
            value="presentable_infinity_category",
            justification=[
                f"Tag {witness!r}: every ∞-topos is a presentable ∞-category — it arises "
                "as an accessible left exact localization of a presheaf ∞-category P(C). "
                "The ∞-categorical Giraud theorem characterizes ∞-toposes among presentable "
                "∞-categories by colimit universality, disjoint coproducts, and effective groupoids.",
            ],
            metadata={**base, "criterion": "infinity_topos_is_presentable", "witness": witness},
        )

    presentable_explicit = {"presentable_infinity", "accessible_infinity"}
    if _matches_any(tags, presentable_explicit | ADJUNCTION_TAGS):
        candidate = presentable_explicit | ADJUNCTION_TAGS
        witness = next(t for t in tags if t in candidate)
        return Result.true(
            mode="theorem",
            value="presentable_infinity_category",
            justification=[
                f"Tag {witness!r}: presentable and accessible ∞-categories are by definition "
                "accessible with all small colimits. Adjunction data (adjoint functor theorem) "
                "also implies presentability in many contexts.",
            ],
            metadata={**base, "criterion": "explicit_presentable_or_adjunction", "witness": witness},
        )

    not_presentable = {"dg_category", "not_presentable", "small_category"}
    if _matches_any(tags, not_presentable):
        witness = next(t for t in tags if t in not_presentable)
        return Result.false(
            mode="theorem",
            value="not_presentable",
            justification=[
                f"Tag {witness!r}: dg-categories are not presentable ∞-categories (they "
                "are enriched categories, not ∞-categories). Small categories (including "
                "small ∞-categories) are not presentable unless they have all colimits. "
                "Explicit 'not_presentable' confirms non-presentability.",
            ],
            metadata={**base, "criterion": "dg_or_not_presentable", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="unknown",
        justification=[
            "No tags indicate whether the ∞-category is presentable. Cannot determine "
            "accessibility and cocompleteness without more information.",
        ],
        metadata={**base, "criterion": "insufficient_data"},
    )


# ---------------------------------------------------------------------------
# Facade functions
# ---------------------------------------------------------------------------

def classify_higher_category(space: Any) -> dict[str, Any]:
    """Run all higher category analysis functions and return a combined result dict."""
    return {
        "is_infinity_categorical":          is_infinity_categorical(space),
        "is_stable_infinity_category":      is_stable_infinity_category(space),
        "has_all_limits_and_colimits":      has_all_limits_and_colimits(space),
        "is_presentable_infinity_category": is_presentable_infinity_category(space),
    }


def higher_category_profile(space: Any) -> dict[str, Any]:
    """Return a comprehensive higher category profile of the space."""
    classification = classify_higher_category(space)
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
    "HigherCategoryProfile",
    "QUASI_CATEGORY_TAGS",
    "KAN_COMPLEX_TAGS",
    "SEGAL_SPACE_TAGS",
    "STABLE_INFINITY_TAGS",
    "INFINITY_TOPOS_TAGS",
    "ADJUNCTION_TAGS",
    "MODEL_CATEGORY_TAGS",
    "ENRICHED_CATEGORY_TAGS",
    "get_named_higher_category_profiles",
    "higher_category_layer_summary",
    "higher_category_chapter_index",
    "higher_category_type_index",
    "is_infinity_categorical",
    "is_stable_infinity_category",
    "has_all_limits_and_colimits",
    "is_presentable_infinity_category",
    "classify_higher_category",
    "higher_category_profile",
]
