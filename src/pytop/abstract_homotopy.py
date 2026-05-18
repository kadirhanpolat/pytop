"""Abstract homotopy theory: model categories, homotopy pushouts/pullbacks,
and infinity-categories.

Key theorems and constructions implemented
------------------------------------------
- Model category axioms (Quillen 1967): a category M with three distinguished classes
  of morphisms — weak equivalences W, fibrations F, cofibrations C — satisfying:
  (M1) M has all small limits and colimits.
  (M2) 2-of-3: if two of f, g, gf are weak equivalences, so is the third.
  (M3) W, F, C are closed under retracts.
  (M4) Lifting: acyclic cofibrations have the LLP w.r.t. fibrations; cofibrations
       have the LLP w.r.t. acyclic fibrations (acyclic = weak equivalence ∩ fibration).
  (M5) Factorization: every morphism factors as (i) acyclic cofibration then fibration,
       and (ii) cofibration then acyclic fibration.
  The homotopy category Ho(M) = M[W^{-1}] inverts all weak equivalences.
- Quillen adjunction (Quillen 1967): an adjunction L: M ⇌ N :R between model categories
  where L preserves cofibrations and acyclic cofibrations (equivalently, R preserves
  fibrations and acyclic fibrations). The derived functors LF: Ho(M) -> Ho(N) and
  RG: Ho(N) -> Ho(M) are well-defined. A Quillen adjunction is a Quillen equivalence
  if LF and RG are inverse equivalences of homotopy categories.
- Homotopy pushout (Mather 1976): the homotopy pushout of a span A <- C -> B is the
  pushout of a diagram in which C is replaced by a cofibrant resolution (cofibrant
  replacement). Concretely: replace C -> A by a cofibration C' -> A' (cofibrant
  replacement of C), then form the ordinary pushout A' ∪_{C'} B. The result is
  homotopy-invariant: it depends only on the homotopy types of A, B, C and the
  homotopy classes of the maps. The homotopy pushout fits into the Mayer-Vietoris
  long exact sequence and is the derived functor of the pushout.
  Homotopy pullback: dual — replace A -> C <- B by fibrant resolutions.
- Proper model categories: M is left proper if pushouts along cofibrations preserve
  weak equivalences; M is right proper if pullbacks along fibrations preserve weak
  equivalences. Properness is needed for the gluing lemma and for Bousfield localization.
  Top (Quillen) and sSet (Kan-Quillen) are both left and right proper.
- Bousfield localization (Bousfield 1975, Hirschhorn 2003): for a left proper, cellular
  or combinatorial model category M and a set of maps S, the left Bousfield localization
  L_S M has the same cofibrations as M but more weak equivalences (the S-local equivalences:
  maps that induce weak equivalences on S-local objects). The fibrant objects of L_S M are
  the S-local fibrant objects of M. Left Bousfield localization exists under mild conditions
  (cellular or combinatorial M, left proper M).
- Quasi-categories (Boardman-Vogt 1973, Joyal 2002): a quasi-category is a simplicial
  set X satisfying the inner horn filling condition: every inner horn Lambda^n_k -> X
  (0 < k < n) extends to Delta^n -> X. Quasi-categories are the fibrant objects in the
  Joyal model structure on sSet. The category of quasi-categories is equivalent (as an
  ∞-category) to the category of (∞,1)-categories. The Joyal model structure presents
  the homotopy theory of (∞,1)-categories.
- Stable model categories (Hovey 1999): a pointed model category M is stable if the
  suspension functor Sigma: Ho(M) -> Ho(M) (left adjoint to the loop functor Omega) is
  an equivalence of categories. The homotopy category Ho(M) of a stable model category
  is naturally triangulated (with distinguished triangles from the cofiber sequences).
  Examples: spectra (Bousfield-Friedlander), chain complexes over a ring, modules over
  an Eilenberg-MacLane ring spectrum.
- Brown representability (Brown 1962): on Ho(M) for a stable model category satisfying
  mild conditions, every cohomological functor is representable. Applies to the stable
  homotopy category SH and gives the Adams spectral sequence as the tool for computing
  maps between spectra.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class AbstractHomotopyProfile:
    """A curated abstract homotopy theory example."""

    key: str
    display_name: str
    category_type: str
    weak_equivalences: str
    fibrations: str
    cofibrations: str
    is_proper: bool
    is_stable: bool
    admits_localization: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

MODEL_CATEGORY_TAGS: frozenset[str] = frozenset({
    "model_category",
    "quillen_model_structure",
    "weak_equivalence",
    "fibration_cofibration",
    "lifting_property",
    "factorization_axiom",
    "homotopy_category",
})

QUILLEN_ADJUNCTION_TAGS: frozenset[str] = frozenset({
    "quillen_adjunction",
    "quillen_equivalence",
    "derived_functor",
    "left_derived",
    "right_derived",
    "total_derived_functor",
    "quillen_pair",
})

HOMOTOPY_LIMIT_TAGS: frozenset[str] = frozenset({
    "homotopy_limit",
    "homotopy_colimit",
    "homotopy_pushout",
    "homotopy_pullback",
    "derived_pushout",
    "derived_pullback",
    "mayer_vietoris",
    "homotopy_fiber",
    "homotopy_cofiber",
})

INFINITY_CATEGORY_TAGS: frozenset[str] = frozenset({
    "infinity_category",
    "quasi_category",
    "kan_complex",
    "joyal_model",
    "inner_horn_filling",
    "complete_segal_space",
    "segal_category",
    "homotopy_coherent",
})

STABLE_HOMOTOPY_TAGS: frozenset[str] = frozenset({
    "stable_model_category",
    "spectra",
    "suspension_equivalence",
    "loop_space_equivalence",
    "triangulated_homotopy_category",
    "stable_homotopy_category",
    "bousfield_friedlander",
    "symmetric_spectra",
})

BOUSFIELD_LOCALIZATION_TAGS: frozenset[str] = frozenset({
    "bousfield_localization",
    "left_bousfield_localization",
    "right_bousfield_localization",
    "local_objects",
    "local_equivalences",
    "nullification",
})

COFIBRANT_FIBRANT_TAGS: frozenset[str] = frozenset({
    "cofibrant_replacement",
    "fibrant_replacement",
    "cofibrant_object",
    "fibrant_object",
    "cofibrant_fibrant",
    "q_cofibrant",
    "q_fibrant",
    "resolution",
})

PROPER_MODEL_TAGS: frozenset[str] = frozenset({
    "left_proper",
    "right_proper",
    "proper_model",
    "gluing_lemma",
    "pushout_weak_equivalence",
    "pullback_weak_equivalence",
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

def get_named_abstract_homotopy_profiles() -> tuple[AbstractHomotopyProfile, ...]:
    """Return the registry of canonical abstract homotopy theory examples."""
    return (
        AbstractHomotopyProfile(
            key="topological_spaces_quillen",
            display_name="Top — Quillen model structure on topological spaces",
            category_type="model_category",
            weak_equivalences="weak homotopy equivalences (pi_n isomorphisms for all n >= 0)",
            fibrations="Serre fibrations (RLP w.r.t. disk inclusions D^n -> D^n x I)",
            cofibrations="retracts of relative CW-complex inclusions",
            is_proper=True,
            is_stable=False,
            admits_localization=True,
            presentation_layer="main_text",
            focus=(
                "The Quillen model structure on Top (Quillen 1967) is the original example "
                "of a model category and the template for all subsequent constructions. "
                "Weak equivalences: f: X -> Y is a weak equivalence iff it induces "
                "isomorphisms pi_n(X, x) -> pi_n(Y, f(x)) for all n >= 0 and all basepoints x. "
                "Fibrations: Serre fibrations — maps with the RLP (right lifting property) with "
                "respect to all disk inclusions D^n x {0} -> D^n x I. Equivalently, maps with "
                "the homotopy lifting property for all CW complexes. "
                "Cofibrations: retracts of relative CW inclusions A -> B where B is built from A "
                "by attaching cells. Every CW complex is cofibrant (A = empty). "
                "Factorization: (i) every f: X -> Y factors as X -i-> Z -p-> Y where i is an "
                "acyclic cofibration (a relative CW inclusion that is also a weak equivalence) "
                "and p is a Serre fibration; (ii) factors as cofibration then acyclic fibration. "
                "The second factorization uses the small object argument. "
                "Ho(Top): the homotopy category obtained by inverting weak equivalences. "
                "By the Whitehead theorem, a weak equivalence between CW complexes is a "
                "homotopy equivalence, so Ho(Top) restricted to CW complexes agrees with "
                "the classical homotopy category. "
                "Properness: Top is both left proper (pushouts of weak equivalences along "
                "cofibrations are weak equivalences) and right proper (pullbacks of weak "
                "equivalences along fibrations are weak equivalences). "
                "Quillen adjunction: the geometric realization-singular complex adjunction "
                "|-|: sSet ⇌ Top: Sing is a Quillen equivalence between the Kan-Quillen "
                "model structure on sSet and the Quillen model structure on Top. "
                "This means sSet and Top have equivalent homotopy theories."
            ),
            chapter_targets=("12", "22", "35"),
        ),
        AbstractHomotopyProfile(
            key="simplicial_sets_kan_quillen",
            display_name="sSet — Kan-Quillen model structure on simplicial sets",
            category_type="model_category",
            weak_equivalences="simplicial weak equivalences (|f| is a weak homotopy equivalence)",
            fibrations="Kan fibrations (RLP w.r.t. all horn inclusions Lambda^n_k -> Delta^n)",
            cofibrations="monomorphisms of simplicial sets",
            is_proper=True,
            is_stable=False,
            admits_localization=True,
            presentation_layer="main_text",
            focus=(
                "The Kan-Quillen model structure on simplicial sets (Quillen 1967) is the "
                "combinatorial model for classical homotopy theory. "
                "Objects: simplicial sets X = {X_n}_{n>=0} with face/degeneracy maps. "
                "Weak equivalences: f: X -> Y is a weak equivalence iff |f|: |X| -> |Y| "
                "(geometric realization) is a weak homotopy equivalence of topological spaces. "
                "Fibrations: Kan fibrations — maps X -> Y with the RLP w.r.t. all horn "
                "inclusions Lambda^n_k -> Delta^n for all n >= 1, 0 <= k <= n. "
                "Fibrant objects: Kan complexes (simplicial sets satisfying the Kan "
                "extension condition). Every simplicial group is a Kan complex. "
                "Cofibrations: monomorphisms (injections on each X_n). Every simplicial "
                "set is cofibrant (the initial object is empty). "
                "The Quillen equivalence |-|: sSet ⇌ Top: Sing shows that sSet and Top "
                "have the same homotopy theory. "
                "Computational advantage: homotopy groups pi_n(X, x) = pi_n(|X|, |x|) "
                "can be computed combinatorially in a fibrant replacement of X. "
                "Cofibrant replacements: the Kan-Quillen fibrant replacement of X (the "
                "Ex^infty functor of Kan) is a Kan complex weakly equivalent to X. "
                "Properness: sSet is both left and right proper. "
                "Joyal model structure: a second model structure on sSet (Joyal 2002) with "
                "the same cofibrations (monomorphisms) but with quasi-categories as fibrant "
                "objects and inner horn extensions as fibrations. "
                "The Kan-Quillen structure models (∞,0)-categories (Kan complexes = spaces), "
                "while the Joyal structure models (∞,1)-categories (quasi-categories)."
            ),
            chapter_targets=("12", "22", "35"),
        ),
        AbstractHomotopyProfile(
            key="chain_complexes_projective",
            display_name="Ch(R) — projective model structure on chain complexes",
            category_type="model_category",
            weak_equivalences="quasi-isomorphisms (homology isomorphisms in all degrees)",
            fibrations="degreewise surjective maps",
            cofibrations="degreewise injective maps with projective cokernel",
            is_proper=True,
            is_stable=True,
            admits_localization=True,
            presentation_layer="main_text",
            focus=(
                "The projective model structure on Ch(R) (chain complexes of R-modules, "
                "unbounded or non-negatively graded) is the foundational example connecting "
                "homological algebra with abstract homotopy theory. "
                "Weak equivalences: quasi-isomorphisms f: A -> B, i.e., maps inducing "
                "isomorphisms H_n(A) -> H_n(B) for all n. "
                "Fibrations: degreewise surjections (surjective in each degree). "
                "Cofibrations: degreewise injections with projective cokernel in each degree. "
                "Cofibrant objects: complexes of projective R-modules. "
                "The homotopy category Ho(Ch(R)) is the classical derived category D(R). "
                "The derived category D(R) inverts quasi-isomorphisms and has a natural "
                "triangulated structure (from the suspension = shift X[1]_n = X_{n-1}). "
                "Stability: Ch(R) is stable — the suspension functor Sigma = [1] (shift by 1) "
                "is an auto-equivalence of Ho(Ch(R)) = D(R). The loop functor is [-1] (shift "
                "by -1). This makes D(R) a triangulated category. "
                "Derived functors: the derived tensor product (-) ⊗^L_R M is computed by "
                "replacing the first argument by a projective resolution (cofibrant replacement). "
                "The derived Hom RHom(M, N) is computed by replacing N by an injective "
                "resolution (fibrant replacement in the injective model structure). "
                "Quillen adjunction: - ⊗_R M: Ch(R) ⇌ Ch(R): Hom(M, -) is a Quillen adjunction "
                "for projective R-modules M. "
                "Properness: Ch(R) is both left and right proper."
            ),
            chapter_targets=("12", "22", "35"),
        ),
        AbstractHomotopyProfile(
            key="quasi_categories_joyal",
            display_name="sSet — Joyal model structure for ∞-categories (quasi-categories)",
            category_type="infinity_category",
            weak_equivalences="categorical equivalences of quasi-categories",
            fibrations="isofibrations (inner Kan fibrations + equivalence lifting)",
            cofibrations="monomorphisms of simplicial sets",
            is_proper=False,
            is_stable=False,
            admits_localization=True,
            presentation_layer="main_text",
            focus=(
                "The Joyal model structure on sSet (Joyal 2002, formalized by Lurie 2009) "
                "presents the homotopy theory of (∞,1)-categories. "
                "Quasi-categories (Boardman-Vogt 1973): a quasi-category is a simplicial set "
                "X satisfying the inner horn filling condition: every inner horn Lambda^n_k -> X "
                "(0 < k < n) has a (not necessarily unique) filler Delta^n -> X. "
                "Outer horns (k=0, k=n) need not fill — this is what distinguishes quasi-categories "
                "from Kan complexes (which fill all horns). "
                "Fibrant objects in Joyal structure: exactly the quasi-categories. "
                "Cofibrations: monomorphisms (same as Kan-Quillen). "
                "Weak equivalences: categorical equivalences — maps f: X -> Y inducing an "
                "equivalence of Ho(X) -> Ho(Y) (the homotopy categories) and weak equivalences "
                "on all hom-spaces Hom_X(a,b) -> Hom_Y(f(a), f(b)). "
                "The nerve functor N: Cat -> sSet embeds ordinary categories as quasi-categories; "
                "the nerve of a category C is the quasi-category corresponding to C. "
                "The homotopy coherent nerve hN: sCat -> sSet gives the Bergner-Cordier "
                "construction for simplicial categories. "
                "Examples of quasi-categories: N(C) for any category C; the coherent nerve "
                "hN(Top^Delta^op) of the simplicial category of topological spaces; the "
                "∞-category of ∞-groupoids (Kan complexes) = the homotopy hypothesis (Grothendieck). "
                "Lurie's Higher Topos Theory: the full development of ∞-category theory "
                "using the Joyal model structure, including ∞-limits, ∞-colimits, ∞-adjunctions, "
                "and the ∞-categorical Yoneda lemma. "
                "NOT right proper: the Joyal model structure is left proper but not right proper, "
                "which limits the applicability of some localization results."
            ),
            chapter_targets=("12", "22", "35"),
        ),
        AbstractHomotopyProfile(
            key="spectra_stable_model",
            display_name="Sp — stable model category of spectra",
            category_type="stable_model_category",
            weak_equivalences="stable weak equivalences (pi_* isomorphisms)",
            fibrations="Omega-spectrum fibrations",
            cofibrations="Cofibrant spectra inclusions",
            is_proper=True,
            is_stable=True,
            admits_localization=True,
            presentation_layer="main_text",
            focus=(
                "Spectra are the fundamental objects of stable homotopy theory. A spectrum "
                "E = {E_n, sigma_n: Sigma E_n -> E_{n+1}} is a sequence of based topological "
                "spaces E_n with structure maps. An Omega-spectrum has the adjoint structure "
                "maps E_n -> Omega E_{n+1} as weak equivalences. "
                "Bousfield-Friedlander model structure (1978): on the category Sp of spectra "
                "(sequential Kan spectra), with weak equivalences = pi_* isomorphisms (maps "
                "inducing isomorphisms on all stable homotopy groups pi_n(E) = colim_k pi_{n+k}(E_k)), "
                "fibrations = Omega-spectrum fibrations (level-wise Kan fibrations with Omega-spectrum "
                "condition on the fiber), and cofibrations determined by LLP. "
                "Stability: the stable model structure is stable — Sigma: Ho(Sp) -> Ho(Sp) "
                "(the suspension spectrum functor) is an equivalence with inverse Omega: Ho(Sp) -> Ho(Sp). "
                "Ho(Sp) is the stable homotopy category SH, which is triangulated with "
                "distinguished triangles from cofiber sequences A -> B -> B/A -> Sigma A. "
                "Smash product: symmetric spectra (Hovey-Shipley-Smith 2000) and orthogonal "
                "spectra (Mandell-May-Schwede-Shipley 2001) provide model categories of spectra "
                "with a symmetric monoidal smash product. The unit is the sphere spectrum S. "
                "E-local spectra (Bousfield 1975): the localization L_E Sp (inverting "
                "E_*-isomorphisms) gives the E-local stable homotopy category. "
                "Rational spectra (p = 0): SH ⊗ Q ≃ graded Q-vector spaces (Serre). "
                "p-local spectra: E = HZ/p (Eilenberg-MacLane spectrum) gives p-completion; "
                "E = M(Z/p) gives mod-p Moore spectrum. "
                "Brown representability: every cohomology theory on finite CW spectra is "
                "representable by a spectrum — this is the Brown representability theorem for SH."
            ),
            chapter_targets=("22", "35"),
        ),
        AbstractHomotopyProfile(
            key="homotopy_pushout_cofibrant",
            display_name="Homotopy pushout — derived pushout via cofibrant replacement",
            category_type="model_category",
            weak_equivalences="induced weak equivalences by cofibrant resolution",
            fibrations="fibration structure inherited from ambient model category",
            cofibrations="cofibrant replacement of the span diagram",
            is_proper=False,
            is_stable=False,
            admits_localization=False,
            presentation_layer="selected_block",
            focus=(
                "The homotopy pushout is the derived version of the ordinary pushout, defined "
                "to be homotopy-invariant under weak equivalences of the input span. "
                "Construction: given a span A <- C -> B in a model category M, the ordinary "
                "pushout A ∪_C B is not homotopy-invariant. The homotopy pushout is obtained "
                "by first replacing the span by a cofibrant diagram: "
                "(1) Cofibrantly replace C by a cofibrant object C' (cofibrant replacement C' -> C "
                "    is a weak equivalence with C' cofibrant). "
                "(2) Replace C -> A and C -> B by cofibrations: factor C' -> A as "
                "    C' -~-> C'' ->> A' (acyclic cofibration then fibration, then take "
                "    the cofibration C' -> A'). "
                "(3) Form the ordinary pushout A' ∪_{C'} B of the cofibrant span C' -> A', C' -> B. "
                "The result A' ∪_{C'} B is the homotopy pushout, written A ∪^h_C B. "
                "Homotopy-invariance: if f: (A, C, B) -> (A', C', B') is a levelwise weak "
                "equivalence of spans, then A ∪^h_C B -> A' ∪^h_{C'} B' is a weak equivalence. "
                "In Top: the homotopy pushout of A <- C -> B is the double mapping cylinder "
                "A ∪_{C x {0}} (C x [0,1]) ∪_{C x {1}} B. For the span {*} <- S^{n-1} -> {*}, "
                "the homotopy pushout is S^n (the suspension of S^{n-1}). "
                "Mayer-Vietoris: the homotopy pushout A ∪^h_C B fits into a long exact sequence "
                "H_n(C) -> H_n(A) ⊕ H_n(B) -> H_n(A ∪^h_C B) -> H_{n-1}(C) -> ... "
                "(the Mayer-Vietoris sequence for homotopy pushouts). "
                "Homotopy pullback (dual): replace fibrant objects, take ordinary pullback. "
                "For a cospan A -> C <- B, the homotopy pullback A x^h_C B is the space of "
                "paths in C from A to B: {(a, p, b) : a in A, b in B, p: [0,1] -> C, p(0)=f(a), p(1)=g(b)}."
            ),
            chapter_targets=("12", "22"),
        ),
        AbstractHomotopyProfile(
            key="left_bousfield_localization",
            display_name="L_S M — left Bousfield localization at a set of maps",
            category_type="model_category",
            weak_equivalences="S-local equivalences (maps inducing weak equivalences on S-local objects)",
            fibrations="maps with RLP w.r.t. S-local acyclic cofibrations",
            cofibrations="same cofibrations as M",
            is_proper=True,
            is_stable=False,
            admits_localization=True,
            presentation_layer="selected_block",
            focus=(
                "Left Bousfield localization L_S M of a model category M at a set of maps S "
                "provides a systematic way to invert S in the homotopy category. "
                "Setup: M is a left proper cellular (or combinatorial) model category; "
                "S = {f_i: A_i -> B_i} is a set of morphisms in M. "
                "S-local objects: X is S-local if for every f: A -> B in S, the induced map "
                "f*: Map(B, X) -> Map(A, X) is a weak equivalence of mapping spaces. "
                "S-local equivalences: g: X -> Y is an S-local equivalence if for every "
                "S-local fibrant object Z, Map(Y, Z) -> Map(X, Z) is a weak equivalence. "
                "L_S M model structure: same underlying category as M, with "
                "- Cofibrations: same as in M. "
                "- Weak equivalences: the S-local equivalences (strictly more than W_M). "
                "- Fibrations: maps with the RLP w.r.t. S-local acyclic cofibrations. "
                "- Fibrant objects: the S-local fibrant objects of M. "
                "Existence (Hirschhorn 2003): L_S M exists as a model category when M is "
                "left proper and cellular (or left proper and combinatorial, by Smith 2001). "
                "Ho(L_S M) = Ho(M)[S-loc. equiv.^{-1}]: the homotopy category of L_S M is "
                "obtained from Ho(M) by further inverting S-local equivalences. "
                "The localization functor L_S: Ho(M) -> Ho(L_S M) is the universal functor "
                "inverting S. "
                "Example 1 — rational homotopy: M = sSet with S = {Sigma^n Z -> Sigma^n Z "
                "(p-fold)}, the rationalization L_S inverts all p-torsion to give rational spaces. "
                "Example 2 — p-completion: localize at {BZ/p -> {*}} to get p-complete spaces. "
                "Example 3 — stable homotopy: L_E (spectra localized at E_*-isomorphisms) "
                "gives Bousfield's E-local stable category (e.g., L_{HZ/p} = p-local spectra). "
                "Right Bousfield localization (colocalization) R_K M: dual — same fibrations, "
                "more cofibrations (K-colocal cofibrations), K-colocal objects are cofibrant."
            ),
            chapter_targets=("22", "35"),
        ),
    )


def abstract_homotopy_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_abstract_homotopy_profiles()
    ))


def abstract_homotopy_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_abstract_homotopy_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def abstract_homotopy_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from category_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_abstract_homotopy_profiles():
        index.setdefault(p.category_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_proper_model_category(space: Any) -> Result:
    """Check whether the model category is both left and right proper.

    A model category M is left proper if pushouts of weak equivalences along
    cofibrations are weak equivalences. It is right proper if pullbacks of weak
    equivalences along fibrations are weak equivalences. Properness is essential
    for the gluing lemma, for Bousfield localization, and for many other constructions.

    Decision layers
    ---------------
    1. Explicit 'proper_model' or 'left_proper' + 'right_proper' tags -> true.
    2. Recognized proper structures (Top, sSet, Ch(R)) tags -> true.
    3. Not-proper tag -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if "proper_model" in tags or (
        "left_proper" in tags and "right_proper" in tags
    ):
        witness = "proper_model" if "proper_model" in tags else "left_proper+right_proper"
        return Result.true(
            mode="theorem",
            value="proper_model_category",
            justification=[
                f"Tag {witness!r}: the model category is proper — pushouts of weak "
                "equivalences along cofibrations are weak equivalences (left proper), "
                "and pullbacks of weak equivalences along fibrations are weak equivalences "
                "(right proper). The gluing lemma holds.",
            ],
            metadata={**base, "criterion": "explicit_proper", "witness": witness},
        )

    canonical_proper = {
        "topological_spaces", "simplicial_sets", "kan_quillen",
        "chain_complexes", "projective_model", "injective_model",
        "quillen_top", "bousfield_friedlander",
    }
    if _matches_any(tags, canonical_proper):
        witness = next(t for t in tags if t in canonical_proper)
        return Result.true(
            mode="theorem",
            value="proper_model_category",
            justification=[
                f"Tag {witness!r}: this is a classically proper model category. "
                "Both Top (Quillen) and sSet (Kan-Quillen) are left and right proper; "
                "Ch(R) (projective/injective) is left and right proper.",
            ],
            metadata={**base, "criterion": "canonical_proper", "witness": witness},
        )

    if _matches_any(tags, PROPER_MODEL_TAGS):
        witness = next(t for t in tags if t in PROPER_MODEL_TAGS)
        return Result.true(
            mode="theorem",
            value="proper_model_category",
            justification=[
                f"Tag {witness!r}: properness criterion detected — the model category "
                "satisfies the indicated properness condition.",
            ],
            metadata={**base, "criterion": "proper_tag", "witness": witness},
        )

    not_proper = {
        "not_proper", "not_left_proper", "not_right_proper",
        "joyal_not_right_proper",
    }
    if _matches_any(tags, not_proper):
        blocking = next(t for t in tags if t in not_proper)
        return Result.false(
            mode="theorem",
            value="proper_model_category",
            justification=[
                f"Tag {blocking!r}: the model category is NOT (fully) proper. "
                "The Joyal model structure on sSet is left proper but NOT right proper. "
                "Properness is needed for Bousfield localization; partial properness may "
                "suffice for left Bousfield localization (requires only left proper).",
            ],
            metadata={**base, "criterion": "not_proper"},
        )

    return Result.unknown(
        mode="symbolic",
        value="proper_model_category",
        justification=[
            "Insufficient tags to determine properness. "
            "Supply tags such as 'left_proper', 'right_proper', 'proper_model', "
            "'topological_spaces', 'simplicial_sets', 'chain_complexes', "
            "or 'not_right_proper'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_homotopy_limits(space: Any) -> Result:
    """Check whether the category admits all homotopy limits and homotopy colimits.

    A model category M has all homotopy limits and colimits because it has all small
    limits and colimits (axiom M1) and these can be derived (replaced by homotopy-invariant
    versions via cofibrant/fibrant replacement of diagram categories). The homotopy limit
    of a diagram D: I -> M is computed by fibrantly replacing D in the diagram category
    M^I (with the injective model structure) and taking the ordinary limit.

    Decision layers
    ---------------
    1. Explicit 'homotopy_limit' or 'homotopy_colimit' tags -> true.
    2. Model category tags -> true (all model categories have homotopy limits).
    3. Not-a-model-category tags -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, HOMOTOPY_LIMIT_TAGS):
        witness = next(t for t in tags if t in HOMOTOPY_LIMIT_TAGS)
        return Result.true(
            mode="theorem",
            value="homotopy_limits",
            justification=[
                f"Tag {witness!r}: homotopy limits/colimits are present. "
                "Homotopy pushouts/pullbacks are computed via cofibrant/fibrant replacement "
                "of the span/cospan diagram, then taking the ordinary pushout/pullback. "
                "The result is homotopy-invariant: weak equivalences of input diagrams "
                "give weak equivalences of outputs.",
            ],
            metadata={**base, "criterion": "explicit_homotopy_limit", "witness": witness},
        )

    if _matches_any(tags, MODEL_CATEGORY_TAGS):
        witness = next(t for t in tags if t in MODEL_CATEGORY_TAGS)
        return Result.true(
            mode="theorem",
            value="homotopy_limits",
            justification=[
                f"Tag {witness!r}: every model category has all homotopy limits and colimits "
                "(axiom M1 guarantees all small limits/colimits, and the derived functors "
                "holim, hocolim exist via the (injective/projective) diagram model structures). "
                "Homotopy limits = right derived functor of lim; hocolim = left derived of colim.",
            ],
            metadata={**base, "criterion": "model_category_has_holim", "witness": witness},
        )

    no_holim = {
        "no_homotopy_limits", "not_complete", "not_cocomplete",
        "missing_factorization",
    }
    if _matches_any(tags, no_holim):
        blocking = next(t for t in tags if t in no_holim)
        return Result.false(
            mode="theorem",
            value="homotopy_limits",
            justification=[
                f"Tag {blocking!r}: the category does not have all homotopy limits/colimits. "
                "This may occur for categories lacking the model category axioms (e.g., "
                "missing small limits/colimits or failing the factorization axiom).",
            ],
            metadata={**base, "criterion": "no_holim"},
        )

    return Result.unknown(
        mode="symbolic",
        value="homotopy_limits",
        justification=[
            "Insufficient tags to determine homotopy limit existence. "
            "Supply tags such as 'homotopy_limit', 'homotopy_colimit', 'model_category', "
            "'homotopy_pushout', or 'no_homotopy_limits'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_stable_model_category(space: Any) -> Result:
    """Check whether the model category is stable.

    A pointed model category M is stable if the suspension functor
    Sigma: Ho(M) -> Ho(M) is an equivalence of categories (with inverse the
    loop functor Omega). The homotopy category Ho(M) of a stable model category
    is canonically triangulated with cofiber sequences as distinguished triangles.

    Decision layers
    ---------------
    1. Explicit 'stable_model_category' or 'suspension_equivalence' tag -> true.
    2. Known stable categories (spectra, chain complexes) tags -> true.
    3. Known unstable categories (Top, sSet) tags -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, STABLE_HOMOTOPY_TAGS):
        witness = next(t for t in tags if t in STABLE_HOMOTOPY_TAGS)
        return Result.true(
            mode="theorem",
            value="stable_model_category",
            justification=[
                f"Tag {witness!r}: the model category is stable — the suspension functor "
                "Sigma: Ho(M) -> Ho(M) is an equivalence of categories (inverse: loop functor Omega). "
                "The homotopy category Ho(M) is canonically triangulated. "
                "Cofiber sequences A -> B -> B/A -> Sigma A are the distinguished triangles.",
            ],
            metadata={**base, "criterion": "explicit_stable", "witness": witness},
        )

    if _matches_any(tags, {"chain_complexes", "derived_category",
                           "projective_model", "injective_model"}):
        witness = next(t for t in tags if t in {
            "chain_complexes", "derived_category", "projective_model", "injective_model"
        })
        return Result.true(
            mode="theorem",
            value="stable_model_category",
            justification=[
                f"Tag {witness!r}: chain complexes (over any ring) form a stable model category — "
                "the shift functor [1] is Sigma and [-1] is Omega, both are auto-equivalences "
                "of the derived category D(R) = Ho(Ch(R)).",
            ],
            metadata={**base, "criterion": "chain_complex_stable", "witness": witness},
        )

    not_stable = {
        "not_stable_model", "unstable_homotopy",
        "topological_spaces", "simplicial_sets", "kan_quillen", "quillen_top",
    }
    if _matches_any(tags, not_stable):
        blocking = next(t for t in tags if t in not_stable)
        return Result.false(
            mode="theorem",
            value="stable_model_category",
            justification=[
                f"Tag {blocking!r}: the model category is NOT stable. "
                "Top (Quillen) and sSet (Kan-Quillen) are unstable: the suspension functor "
                "Sigma is not an equivalence of Ho(Top) (e.g., pi_n(S^n) != pi_{n+1}(S^{n+1}) "
                "in general). Stable homotopy theory requires passage to spectra.",
            ],
            metadata={**base, "criterion": "not_stable"},
        )

    return Result.unknown(
        mode="symbolic",
        value="stable_model_category",
        justification=[
            "Insufficient tags to determine stability. "
            "Supply tags such as 'stable_model_category', 'spectra', 'suspension_equivalence', "
            "'chain_complexes', 'topological_spaces', or 'not_stable_model'.",
        ],
        metadata={**base, "criterion": None},
    )


def admits_bousfield_localization(space: Any) -> Result:
    """Check whether the model category admits left Bousfield localization.

    Left Bousfield localization L_S M at a set S of maps exists when M is left proper
    AND either cellular (Hirschhorn 2003) or combinatorial (Smith 2001 / Dugger 2001).
    Combinatorial model categories are locally presentable categories with a cofibrantly
    generated model structure. Cellular model categories have a slightly weaker condition
    (based on smallness of the generating sets).

    Decision layers
    ---------------
    1. Explicit 'bousfield_localization' or 'left_bousfield_localization' tag -> true.
    2. Combinatorial + left proper -> true.
    3. Cellular + left proper -> true.
    4. Not-left-proper or not-cellular/combinatorial -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, BOUSFIELD_LOCALIZATION_TAGS):
        witness = next(t for t in tags if t in BOUSFIELD_LOCALIZATION_TAGS)
        return Result.true(
            mode="theorem",
            value="admits_bousfield_localization",
            justification=[
                f"Tag {witness!r}: left Bousfield localization is applicable. "
                "The localized model category L_S M has the same cofibrations, the same "
                "underlying category, but S-local equivalences as weak equivalences and "
                "S-local fibrant objects as fibrant objects. "
                "Existence requires: left proper + cellular or combinatorial.",
            ],
            metadata={**base, "criterion": "explicit_bousfield", "witness": witness},
        )

    combinatorial = {"combinatorial_model", "locally_presentable", "cofibrantly_generated"}
    cellular = {"cellular_model", "cellular_cofibrations"}
    is_comb_or_cell = _matches_any(tags, combinatorial | cellular)
    is_lp = _matches_any(tags, {"left_proper"} | PROPER_MODEL_TAGS)

    if is_comb_or_cell and is_lp:
        witness = next(
            t for t in tags if t in combinatorial | cellular | {"left_proper"} | PROPER_MODEL_TAGS
        )
        return Result.true(
            mode="theorem",
            value="admits_bousfield_localization",
            justification=[
                f"Tag {witness!r}: the model category is left proper and "
                "cellular/combinatorial — Hirschhorn's theorem guarantees that left Bousfield "
                "localization L_S M exists for any set of maps S. "
                "(Combinatorial: Smith 2001; Cellular: Hirschhorn 2003.)",
            ],
            metadata={**base, "criterion": "proper_cellular_combinatorial"},
        )

    no_localization = {
        "not_left_proper", "not_combinatorial", "not_cellular",
        "no_bousfield_localization",
    }
    if _matches_any(tags, no_localization):
        blocking = next(t for t in tags if t in no_localization)
        return Result.false(
            mode="theorem",
            value="admits_bousfield_localization",
            justification=[
                f"Tag {blocking!r}: left Bousfield localization may not exist. "
                "Hirschhorn's theorem requires left properness; without it, the "
                "localized weak equivalences may not satisfy the 2-of-3 axiom. "
                "Non-cellular/non-combinatorial structures lack the size conditions "
                "needed for the small object argument.",
            ],
            metadata={**base, "criterion": "localization_fails"},
        )

    return Result.unknown(
        mode="symbolic",
        value="admits_bousfield_localization",
        justification=[
            "Insufficient tags to determine Bousfield localization admissibility. "
            "Supply tags such as 'left_proper', 'combinatorial_model', 'cellular_model', "
            "'bousfield_localization', or 'not_left_proper'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_abstract_homotopy(space: Any) -> dict[str, Any]:
    """Classify the abstract homotopy type of the model/homotopy structure.

    Keys
    ----
    homotopy_class : str
        One of ``"stable_proper"``, ``"stable_localizable"``, ``"unstable_proper"``,
        ``"infinity_categorical"``, ``"basic_model"``, ``"unknown"``.
    is_proper_model_category : Result
    has_homotopy_limits : Result
    is_stable_model_category : Result
    admits_bousfield_localization : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    proper_r = is_proper_model_category(space)
    holim_r = has_homotopy_limits(space)
    stable_r = is_stable_model_category(space)
    bousfield_r = admits_bousfield_localization(space)

    if stable_r.is_true and proper_r.is_true and bousfield_r.is_true:
        homotopy_class = "stable_proper"
    elif stable_r.is_true and bousfield_r.is_true:
        homotopy_class = "stable_localizable"
    elif _matches_any(tags, INFINITY_CATEGORY_TAGS):
        homotopy_class = "infinity_categorical"
    elif proper_r.is_true and holim_r.is_true:
        homotopy_class = "unstable_proper"
    elif holim_r.is_true:
        homotopy_class = "basic_model"
    else:
        homotopy_class = "unknown"

    key_properties: list[str] = []
    if proper_r.is_true:
        key_properties.append("proper")
    if proper_r.is_false:
        key_properties.append("not_fully_proper")
    if holim_r.is_true:
        key_properties.append("homotopy_limits_colimits")
    if stable_r.is_true:
        key_properties.append("stable")
    if stable_r.is_false:
        key_properties.append("unstable")
    if bousfield_r.is_true:
        key_properties.append("admits_localization")
    if _matches_any(tags, INFINITY_CATEGORY_TAGS):
        key_properties.append("infinity_categorical")
    if _matches_any(tags, QUILLEN_ADJUNCTION_TAGS):
        key_properties.append("quillen_adjunction")
    if _matches_any(tags, COFIBRANT_FIBRANT_TAGS):
        key_properties.append("cofibrant_fibrant_replacement")

    return {
        "homotopy_class": homotopy_class,
        "is_proper_model_category": proper_r,
        "has_homotopy_limits": holim_r,
        "is_stable_model_category": stable_r,
        "admits_bousfield_localization": bousfield_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def abstract_homotopy_profile(space: Any) -> dict[str, Any]:
    """Full abstract homotopy profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_abstract_homotopy`.
    named_profiles : tuple[AbstractHomotopyProfile, ...]
        Registry of canonical abstract homotopy theory examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_abstract_homotopy(space),
        "named_profiles": get_named_abstract_homotopy_profiles(),
        "layer_summary": abstract_homotopy_layer_summary(),
    }


__all__ = [
    "AbstractHomotopyProfile",
    "MODEL_CATEGORY_TAGS",
    "QUILLEN_ADJUNCTION_TAGS",
    "HOMOTOPY_LIMIT_TAGS",
    "INFINITY_CATEGORY_TAGS",
    "STABLE_HOMOTOPY_TAGS",
    "BOUSFIELD_LOCALIZATION_TAGS",
    "COFIBRANT_FIBRANT_TAGS",
    "PROPER_MODEL_TAGS",
    "get_named_abstract_homotopy_profiles",
    "abstract_homotopy_layer_summary",
    "abstract_homotopy_chapter_index",
    "abstract_homotopy_type_index",
    "is_proper_model_category",
    "has_homotopy_limits",
    "is_stable_model_category",
    "admits_bousfield_localization",
    "classify_abstract_homotopy",
    "abstract_homotopy_profile",
]
