"""Topos theory: Grothendieck toposes, sheaves, geometric morphisms, classifying toposes.

Key theorems implemented
------------------------
- Elementary toposes: a category E is an elementary topos if it has finite limits,
  is cartesian closed (every object X has an exponential Y^X), and has a subobject
  classifier — an object Omega with a monomorphism true: 1 -> Omega such that every
  monomorphism m: A -> X is the pullback of true along a unique characteristic map
  chi_m: X -> Omega. Key examples: Set, Sh(X), [C^op, Set], the effective topos Eff.
- Giraud's theorem (1964): a category E is a Grothendieck topos iff it has a small
  generating set, is cocomplete, finite limits commute with filtered colimits
  (coproducts are universal and disjoint), and every equivalence relation is effective.
  Equivalently: E = Sh(C, J) for some small site (C, J).
- Boolean toposes: a topos E is Boolean if every subobject A ⊆ X has a complement
  A^c with A ∪ A^c = X and A ∩ A^c = emptyset. Equivalently, the subobject classifier
  Omega is a Boolean algebra object (every element satisfies a ∨ ¬a = 1). Boolean
  toposes have classical internal logic (law of excluded middle holds). Key examples:
  Set, [G-Set] for a group G, sheaves on a Boolean space (Stone space).
- Localic toposes: a Grothendieck topos E is localic if it is equivalent to Sh(L)
  for a locale L (i.e., the site is a locale with the canonical coverage). Localic
  toposes form a full subcategory of Groth-Top equivalent to the category of locales
  (Joyal-Tierney theorem: every Grothendieck topos is bounded over a localic topos).
- Geometric morphisms: a geometric morphism f: E -> F is an adjoint pair f* -| f_*
  where the inverse image f*: F -> E preserves finite limits. The direct image
  f_*: E -> F is the right adjoint. Key examples: the unique morphism E -> Set
  (giving the 'global sections' functor Gamma = (f_*)(1)), and the structure morphisms
  of classifying toposes. An essential geometric morphism has f* with a left adjoint f_!.
- Classifying toposes (Lawvere 1970, Makkai-Reyes 1977): for each coherent (geometric)
  theory T there is a Grothendieck topos B[T] — the classifying topos — such that
  models of T in any Grothendieck topos E correspond to geometric morphisms E -> B[T].
  This makes topos theory a 'geometry of theories'. Examples: BG classifies G-torsors,
  the Zariski topos classifies local rings, the etale topos classifies strict local rings.
- The effective topos Eff (Hyland 1982): an elementary topos with a natural number
  object (NNO) that is NOT a Grothendieck topos. Its objects are 'modest sets' (sets
  with a realizability structure). The internal logic is intuitionistic. Eff models the
  effective topos of realizability and is the home of the recursive/computable reals.
  Giraud's theorem fails for Eff: it lacks a small generating set in the sense required.
- Etale topos of a scheme: for a scheme X, the small etale topos Sh(X_et) consists of
  sheaves on the etale site (etale morphisms U -> X with the etale topology). Its
  cohomology H^n_et(X, F) — etale cohomology — is the foundation of the Weil conjectures
  proof (Grothendieck, Deligne). The etale topos is not Boolean and has a complex internal
  logic reflecting the arithmetic geometry of X.
- Surjective geometric morphisms (localic surjections): f: E -> F is a surjection if f*
  reflects isomorphisms. The Joyal-Tierney theorem: every Grothendieck topos admits a
  surjective localic geometric morphism from a localic topos — making localic toposes
  'enough' to generate all Grothendieck toposes.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class ToposProfile:
    """A curated topos theory example."""

    key: str
    display_name: str
    topos_type: str
    is_grothendieck: bool
    is_elementary: bool
    is_boolean: bool
    is_localic: bool
    has_natural_number_object: bool
    has_enough_points: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

GROTHENDIECK_TOPOS_TAGS: frozenset[str] = frozenset({
    "grothendieck_topos",
    "sheaves_on_site", "sheaves_on_space", "sheaves_on_locale",
    "presheaf_topos",
    "localic_topos",
    "classifying_topos",
    "etale_topos", "zariski_topos",
    "petit_topos", "gros_topos",
    "coherent_topos",
    "bounded_topos",
})

ELEMENTARY_TOPOS_TAGS: frozenset[str] = frozenset({
    "elementary_topos",
    "cartesian_closed_with_omega",
    "subobject_classifier",
    "grothendieck_topos",
    "sheaves_on_site",
    "presheaf_topos",
    "realizability_topos",
    "effective_topos",
})

BOOLEAN_TOPOS_TAGS: frozenset[str] = frozenset({
    "boolean_topos",
    "classical_logic_topos",
    "law_of_excluded_middle_topos",
    "sheaves_boolean_space",
    "presheaf_topos",
    "set_topos",
    "g_sets_topos",
    "discrete_groupoid_topos",
    "atomic_topos",
})

LOCALIC_TOPOS_TAGS: frozenset[str] = frozenset({
    "localic_topos",
    "sheaves_on_locale",
    "sheaves_on_space",
    "localic_geometric_morphism",
    "spatial_topos",
    "open_subtopos",
})

ENOUGH_POINTS_TAGS: frozenset[str] = frozenset({
    "enough_points_topos",
    "set_valued_points",
    "presheaf_topos",
    "set_topos",
    "g_sets_topos",
    "sheaves_hausdorff_space",
    "atomic_boolean_topos",
    "spatial_topos",
    "localic_spatial",
})

NOT_BOOLEAN_TOPOS_TAGS: frozenset[str] = frozenset({
    "not_boolean_topos",
    "intuitionistic_topos",
    "heyting_valued_logic",
    "etale_topos",
    "zariski_topos",
    "effective_topos",
    "sheaves_non_discrete",
})

NOT_GROTHENDIECK_TAGS: frozenset[str] = frozenset({
    "not_grothendieck_topos",
    "realizability_topos",
    "effective_topos",
    "no_small_generating_set",
})

GEOMETRIC_MORPHISM_TAGS: frozenset[str] = frozenset({
    "geometric_morphism",
    "inverse_image_left_exact",
    "essential_geometric_morphism",
    "localic_surjection",
    "open_geometric_morphism",
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

def get_named_topos_profiles() -> tuple[ToposProfile, ...]:
    """Return the registry of canonical topos theory examples."""
    return (
        ToposProfile(
            key="set_topos",
            display_name="Set — the topos of sets",
            topos_type="boolean_topos",
            is_grothendieck=True,
            is_elementary=True,
            is_boolean=True,
            is_localic=True,
            has_natural_number_object=True,
            has_enough_points=True,
            presentation_layer="main_text",
            focus=(
                "The category Set of sets and functions is the terminal Grothendieck topos: "
                "every Grothendieck topos E has a unique geometric morphism E -> Set (the "
                "global sections morphism, with inverse image the constant sheaf functor "
                "and direct image the global sections Gamma). "
                "Set = Sh(1) — sheaves on the terminal site (one object, one morphism, "
                "the trivial coverage). It is also Sh(L) for L the one-element locale. "
                "Set is Boolean: every subset A ⊆ X has a complement X\\A, and the "
                "subobject classifier is Omega = {true, false} = 2. The internal logic "
                "of Set is classical (full law of excluded middle). "
                "Set has a natural number object (NNO): the set N with zero: 1 -> N and "
                "successor: N -> N, satisfying the universal property of primitive "
                "recursion. Every Grothendieck topos has an NNO (the constant sheaf N). "
                "Set has enough points: the identity geometric morphism id: Set -> Set "
                "provides the canonical point. More generally, E has enough points if the "
                "points p: Set -> E (geometric morphisms) jointly detect isomorphisms — "
                "which for Set itself is trivially true. "
                "Giraud's theorem: Set satisfies all Giraud axioms (generating set: any "
                "set of singletons; coproducts universal and disjoint; effective equivalence "
                "relations). The subobject classifier Omega = 2 is Boolean."
            ),
            chapter_targets=("11", "29", "53"),
        ),
        ToposProfile(
            key="sheaves_topological_space",
            display_name="Sh(X) — sheaves on a topological space",
            topos_type="localic_topos",
            is_grothendieck=True,
            is_elementary=True,
            is_boolean=False,
            is_localic=True,
            has_natural_number_object=True,
            has_enough_points=True,
            presentation_layer="main_text",
            focus=(
                "For a topological space X, the category Sh(X) of sheaves of sets on X "
                "is the fundamental example of a Grothendieck topos. Its objects are "
                "sheaves F: Open(X)^op -> Set satisfying the sheaf condition: for every "
                "open cover U = union U_i, the diagram "
                "F(U) -> prod F(U_i) ⇉ prod F(U_i ∩ U_j) is an equalizer. "
                "Sh(X) is a localic topos: it equals Sh(Omega(X)) where Omega(X) is the "
                "frame of opens of X. When X is sober, Sh(X) encodes X completely: "
                "the points of Sh(X) (geometric morphisms Set -> Sh(X)) correspond "
                "bijectively to points of X. Hence Sh(X) has enough points when X is sober. "
                "Sh(X) is generally NOT Boolean: the subobject classifier is Omega(U) = "
                "{open V : V ⊆ U} (the opens contained in U), which is a Heyting algebra "
                "but not Boolean unless X is discrete or Omega(X) is a Boolean algebra. "
                "The internal logic of Sh(X) is intuitionistic (Heyting-valued). "
                "Key applications: sheaf cohomology H^n(X, F) — the derived functors "
                "of global sections Gamma: Sh(X) -> Set — generalises Cech cohomology and "
                "is the foundation of algebraic topology and algebraic geometry over X. "
                "The NNO in Sh(X) is the constant sheaf N (the sheafification of the "
                "presheaf U mapsto N for all open U)."
            ),
            chapter_targets=("11", "29", "53"),
        ),
        ToposProfile(
            key="presheaf_topos",
            display_name="[C^op, Set] — presheaf topos on a small category",
            topos_type="boolean_topos",
            is_grothendieck=True,
            is_elementary=True,
            is_boolean=True,
            is_localic=False,
            has_natural_number_object=True,
            has_enough_points=True,
            presentation_layer="main_text",
            focus=(
                "For a small category C, the category [C^op, Set] of presheaves "
                "(contravariant functors C -> Set) is a Grothendieck topos — the "
                "presheaf topos on C. It equals Sh(C, J_trivial) where J_trivial is "
                "the trivial (chaotic) coverage (every sieve covers). "
                "[C^op, Set] is Boolean: the subobject classifier is Omega(c) = "
                "{sieves on c} = {S : S is a right ideal in C(-,c)}, which is a "
                "Boolean algebra because every sieve has a complement (the complement "
                "of a sieve S at c is C(-,c) \\ S). The law of excluded middle holds "
                "internally. "
                "The presheaf topos [C^op, Set] has enough points: the 'representable "
                "point' at each object c in C gives a geometric morphism "
                "p_c: Set -> [C^op, Set] (with p_c^*(F) = F(c)). The family of all "
                "representable points jointly detects isomorphisms. "
                "[C^op, Set] is localic iff C is a preorder (poset-like category). "
                "When C is a group G (viewed as a one-object category), [G^op, Set] = "
                "[G-Set] = G-sets, the classifying topos for G (see key_example BG). "
                "The Yoneda lemma: F(c) ≅ Nat(hom(-,c), F) — natural transformations "
                "from the representable functor to F — is the fundamental calculation. "
                "Free colimit completion: [C^op, Set] is the free cocomplete category "
                "generated by C (Kan extension characterisation)."
            ),
            chapter_targets=("11", "29", "53"),
        ),
        ToposProfile(
            key="classifying_topos_bg",
            display_name="BG = [G-Set] — classifying topos for a discrete group G",
            topos_type="boolean_topos",
            is_grothendieck=True,
            is_elementary=True,
            is_boolean=True,
            is_localic=False,
            has_natural_number_object=True,
            has_enough_points=True,
            presentation_layer="selected_block",
            focus=(
                "For a discrete group G, the classifying topos BG is the category [G-Set] "
                "of G-sets (sets equipped with a left G-action). This is the presheaf "
                "topos on the one-object category BG (the delooping of G), i.e., BG = "
                "[BG^op, Set] where BG is the groupoid with one object and hom = G. "
                "The classifying property: geometric morphisms E -> BG from any "
                "Grothendieck topos E to BG correspond bijectively to G-torsors in E "
                "(locally trivial G-principal bundles). This makes BG 'the classifying '  "
                "space for G in the topos-theoretic sense. "
                "BG is Boolean: as a presheaf topos on a groupoid (G acts by conjugation), "
                "the subobject classifier is 2 = {0,1} with trivial G-action, giving "
                "classical internal logic. "
                "BG has enough points: the unique point p: Set -> BG (forget the G-action) "
                "detects isomorphisms (a map f: X -> Y in G-Set is an isomorphism iff the "
                "underlying map of sets is a bijection). "
                "The fundamental group of a topos: for a connected locally simply "
                "connected topological space X, the fundamental group pi_1(X,x) satisfies "
                "Sh(X) ≃ B(pi_1(X,x)) over Set. The etale fundamental group of a scheme "
                "is the profinite analogue."
            ),
            chapter_targets=("11", "29"),
        ),
        ToposProfile(
            key="etale_topos",
            display_name="Sh(X_et) — the small etale topos of a scheme",
            topos_type="grothendieck_topos",
            is_grothendieck=True,
            is_elementary=True,
            is_boolean=False,
            is_localic=False,
            has_natural_number_object=True,
            has_enough_points=False,
            presentation_layer="selected_block",
            focus=(
                "For a scheme X (e.g., Spec Z, an algebraic variety over a field k), "
                "the small etale topos Sh(X_et) consists of sheaves on the etale site: "
                "the category Et(X) of etale morphisms U -> X equipped with the etale "
                "topology (surjective families of etale maps cover). "
                "An etale morphism is a formally etale flat morphism of finite type — the "
                "algebro-geometric analogue of a local homeomorphism. The etale site is "
                "much finer than the Zariski site (which misses arithmetic information). "
                "The etale topos is NOT Boolean: the internal logic is intuitionistic, "
                "reflecting the complexity of arithmetic. The subobject classifier Omega "
                "is the etale sheaf of truth values, which is a Heyting algebra sheaf. "
                "The etale topos generally lacks enough points in the classical sense: "
                "geometric morphisms Set -> Sh(X_et) correspond to geometric points "
                "x: Spec(k^alg) -> X, but for arithmetic schemes these are scarce. "
                "Etale cohomology H^n_et(X, F) (for a sheaf F, e.g., the constant sheaf "
                "Z/l-Z for a prime l) is the key invariant: for X a smooth projective "
                "variety over F_q, the Weil conjectures (proved by Deligne 1974 using "
                "etale cohomology) state that the zeta function Z(X,t) is rational, "
                "satisfies a functional equation, and the eigenvalues of Frobenius on "
                "H^n_et(X, Q_l) have absolute value q^{n/2} (Riemann hypothesis for "
                "varieties). The l-adic cohomology H^n_et(X, Q_l) = lim H^n_et(X, Z/l^n) "
                "is the algebraic-geometric analogue of singular cohomology."
            ),
            chapter_targets=("11", "29"),
        ),
        ToposProfile(
            key="effective_topos",
            display_name="Eff — the effective (realizability) topos",
            topos_type="elementary_topos",
            is_grothendieck=False,
            is_elementary=True,
            is_boolean=False,
            is_localic=False,
            has_natural_number_object=True,
            has_enough_points=False,
            presentation_layer="selected_block",
            focus=(
                "The effective topos Eff (Hyland 1982) is the paradigmatic example of an "
                "elementary topos that is NOT a Grothendieck topos. Its objects are "
                "'assemblies' — sets A equipped with a realizability relation: each "
                "element a in A has a non-empty set of 'realizers' in Kleene's partial "
                "combinatory algebra (the natural numbers with partial application). "
                "Eff violates Giraud's axioms: it does not have a small generating set "
                "in the Giraud sense (the generating set would need to be closed under "
                "all the realizability operations, which requires going outside any fixed "
                "small category). Hence Eff is not of the form Sh(C, J). "
                "Eff has a natural number object (the standard N with computable successor "
                "and zero), but its internal logic is intuitionistic: the law of excluded "
                "middle fails (no realizer can uniformly decide all propositions). "
                "The Church-Turing thesis holds internally in Eff: every function N -> N "
                "is computable. The Brouwer fixed-point theorem fails (discontinuous "
                "functions N -> N that are internally functions do not exist). "
                "Eff does not have enough points: geometric morphisms Set -> Eff are "
                "rare (only the 'standard point' exists), so the points do not detect "
                "all internal structure. "
                "Eff is a key example in the semantics of programming languages "
                "(realizability semantics) and in foundations: it provides a model where "
                "all functions are computable, providing a consistency proof that "
                "Church's thesis is compatible with intuitionistic mathematics."
            ),
            chapter_targets=("11", "29"),
        ),
    )


def topos_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_topos_profiles()
    ))


def topos_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_topos_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def topos_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from topos_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_topos_profiles():
        index.setdefault(p.topos_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_grothendieck_topos(space: Any) -> Result:
    """Check whether the topos is a Grothendieck topos (sheaves on a site).

    A Grothendieck topos is a category equivalent to Sh(C, J) — sheaves on a
    small site (C, J). By Giraud's theorem (1964), E is a Grothendieck topos iff:
    (1) E has a small generating set; (2) E is cocomplete; (3) colimits are
    universal (stable under pullback) and coproducts are disjoint; (4) every
    equivalence relation is effective. Key facts:
    - Set, Sh(X), [C^op, Set], BG are all Grothendieck toposes.
    - The effective topos Eff is elementary but NOT Grothendieck (fails (1)).
    - Every Grothendieck topos is elementary.

    Decision layers
    ---------------
    1. Explicit 'grothendieck_topos' or sheaves-on-site tag -> true.
    2. Localic / presheaf / classifying topos -> true (all are Grothendieck).
    3. Realizability / effective topos -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"grothendieck_topos", "sheaves_on_site",
                            "sheaves_on_space", "sheaves_on_locale"}):
        witness = next(t for t in tags if t in {"grothendieck_topos",
                                                   "sheaves_on_site",
                                                   "sheaves_on_space",
                                                   "sheaves_on_locale"})
        return Result.true(
            mode="theorem",
            value="grothendieck_topos",
            justification=[
                f"Tag {witness!r}: the topos is Grothendieck — it is equivalent to "
                "Sh(C, J) for some small site (C, J). By Giraud's theorem, it has a "
                "small generating set, universal colimits, disjoint coproducts, and "
                "effective equivalence relations.",
            ],
            metadata={**base, "criterion": "explicit_grothendieck", "witness": witness},
        )

    if _matches_any(tags, {"localic_topos", "presheaf_topos", "classifying_topos",
                            "etale_topos", "zariski_topos", "coherent_topos",
                            "bounded_topos", "petit_topos", "set_topos",
                            "g_sets_topos"}):
        witness = next(t for t in tags if t in {"localic_topos", "presheaf_topos",
                                                   "classifying_topos", "etale_topos",
                                                   "zariski_topos", "coherent_topos",
                                                   "bounded_topos", "petit_topos",
                                                   "set_topos", "g_sets_topos"})
        return Result.true(
            mode="theorem",
            value="grothendieck_topos",
            justification=[
                f"Tag {witness!r}: this is a known class of Grothendieck toposes. "
                "Presheaf toposes [C^op, Set], localic toposes Sh(L), classifying "
                "toposes BG, and etale toposes Sh(X_et) are all Grothendieck toposes "
                "satisfying Giraud's axioms.",
            ],
            metadata={**base, "criterion": "known_grothendieck_class", "witness": witness},
        )

    if _matches_any(tags, NOT_GROTHENDIECK_TAGS):
        blocking = next(t for t in tags if t in NOT_GROTHENDIECK_TAGS)
        return Result.false(
            mode="theorem",
            value="grothendieck_topos",
            justification=[
                f"Tag {blocking!r}: the topos is NOT a Grothendieck topos. "
                "The effective topos Eff (Hyland 1982) is elementary but violates "
                "Giraud's axiom (1): it has no small generating set. Hence Eff is "
                "not equivalent to Sh(C, J) for any small site.",
            ],
            metadata={**base, "criterion": "not_grothendieck"},
        )

    return Result.unknown(
        mode="symbolic",
        value="grothendieck_topos",
        justification=[
            "Insufficient tags to determine Grothendieck topos. "
            "Supply tags such as 'grothendieck_topos', 'sheaves_on_site', "
            "'presheaf_topos', 'localic_topos', 'effective_topos', or 'realizability_topos'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_boolean_topos(space: Any) -> Result:
    """Check whether the topos has Boolean (classical) internal logic.

    A topos E is Boolean if every subobject A ⊆ X has a complement: a subobject
    B ⊆ X with A ∪ B = X and A ∩ B = 0. Equivalently:
    - The subobject classifier Omega is a Boolean algebra (every element satisfies
      a ∨ ¬a = 1 in the internal Heyting algebra).
    - The law of excluded middle holds internally (for every proposition P,
      P ∨ ¬P is provable).
    Key facts:
    - Set and all presheaf toposes [C^op, Set] are Boolean.
    - Sh(X) is Boolean iff X is a Boolean (Stone) space (or more generally iff
      Omega(X) is a Boolean algebra — i.e., X is extremally disconnected).
    - Etale toposes and general sheaf toposes are NOT Boolean.
    - The effective topos Eff is NOT Boolean (Church-Turing thesis holds internally).

    Decision layers
    ---------------
    1. Explicit 'boolean_topos' or classical-logic tag -> true.
    2. Presheaf / Set / G-sets (all Boolean) -> true.
    3. Etale / Zariski / effective topos -> false.
    4. 'not_boolean_topos' / intuitionistic tag -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"boolean_topos", "classical_logic_topos",
                            "law_of_excluded_middle_topos"}):
        witness = next(t for t in tags if t in {"boolean_topos",
                                                   "classical_logic_topos",
                                                   "law_of_excluded_middle_topos"})
        return Result.true(
            mode="theorem",
            value="boolean_topos",
            justification=[
                f"Tag {witness!r}: the topos is Boolean — the subobject classifier "
                "Omega is a Boolean algebra, and every subobject has a complement. "
                "The internal logic is classical: the law of excluded middle holds.",
            ],
            metadata={**base, "criterion": "explicit_boolean", "witness": witness},
        )

    if _matches_any(tags, {"presheaf_topos", "set_topos", "g_sets_topos",
                            "sheaves_boolean_space", "atomic_topos",
                            "discrete_groupoid_topos"}):
        witness = next(t for t in tags if t in {"presheaf_topos", "set_topos",
                                                   "g_sets_topos",
                                                   "sheaves_boolean_space",
                                                   "atomic_topos",
                                                   "discrete_groupoid_topos"})
        return Result.true(
            mode="theorem",
            value="boolean_topos",
            justification=[
                f"Tag {witness!r}: presheaf toposes [C^op, Set] and Set are Boolean: "
                "the subobject classifier Omega(c) = P(C(-,c)) is the power-set "
                "Boolean algebra of the representable sieve. Every sieve has a "
                "complement (its set-theoretic complement in C(-,c)).",
            ],
            metadata={**base, "criterion": "presheaf_boolean", "witness": witness},
        )

    if _matches_any(tags, {"etale_topos", "zariski_topos"} | NOT_GROTHENDIECK_TAGS):
        blocking = next(t for t in tags if t in ({"etale_topos", "zariski_topos"}
                                                    | NOT_GROTHENDIECK_TAGS))
        return Result.false(
            mode="theorem",
            value="boolean_topos",
            justification=[
                f"Tag {blocking!r}: etale and Zariski toposes are NOT Boolean. "
                "The subobject classifier is a Heyting algebra (not Boolean): "
                "the law of excluded middle fails internally, reflecting the "
                "intuitionistic nature of arithmetic/algebraic geometry. "
                "The effective topos also fails: Church-Turing thesis implies "
                "no uniform classical truth assignment.",
            ],
            metadata={**base, "criterion": "not_boolean_topos"},
        )

    if _matches_any(tags, NOT_BOOLEAN_TOPOS_TAGS):
        blocking = next(t for t in tags if t in NOT_BOOLEAN_TOPOS_TAGS)
        return Result.false(
            mode="theorem",
            value="boolean_topos",
            justification=[
                f"Tag {blocking!r}: the topos has intuitionistic (non-Boolean) internal "
                "logic. The subobject classifier Omega is a Heyting algebra where "
                "a ∨ ¬a = 1 may fail. Sheaves on non-discrete spaces have this property.",
            ],
            metadata={**base, "criterion": "not_boolean_heyting"},
        )

    return Result.unknown(
        mode="symbolic",
        value="boolean_topos",
        justification=[
            "Insufficient tags to determine Boolean logic. "
            "Supply tags such as 'boolean_topos', 'presheaf_topos', 'set_topos', "
            "'etale_topos', 'effective_topos', or 'not_boolean_topos'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_localic_topos(space: Any) -> Result:
    """Check whether the topos is localic (equivalent to Sh(L) for a locale L).

    A Grothendieck topos E is localic if it is equivalent to Sh(L) for some locale L.
    Equivalently, E is generated by its subobjects of 1 (the subterminal objects form
    a generating set), or the canonical geometric morphism E -> Sh(Omega_E) (where
    Omega_E is the locale of subterminal objects) is an equivalence. Key facts:
    - Sh(X) for X a topological space is localic: L = Omega(X).
    - Set is localic: L = 1 (the one-element locale).
    - Presheaf toposes [C^op, Set] are NOT localic unless C is a preorder.
    - The Joyal-Tierney theorem: every Grothendieck topos E admits a surjective
      localic geometric morphism from a localic topos S -> E (localic surjection).

    Decision layers
    ---------------
    1. Explicit 'localic_topos' / 'sheaves_on_locale' / 'sheaves_on_space' tag -> true.
    2. Set topos (sheaves on the one-element locale) -> true.
    3. Presheaf topos [C^op, Set] (not localic unless C is a preorder) -> false.
    4. Etale / classifying topos (not localic in general) -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"localic_topos", "sheaves_on_locale", "sheaves_on_space",
                            "spatial_topos", "open_subtopos"}):
        witness = next(t for t in tags if t in {"localic_topos", "sheaves_on_locale",
                                                   "sheaves_on_space", "spatial_topos",
                                                   "open_subtopos"})
        return Result.true(
            mode="theorem",
            value="localic_topos",
            justification=[
                f"Tag {witness!r}: the topos is localic — equivalent to Sh(L) for "
                "a locale L. Its subterminal objects form a generating set, and the "
                "canonical map to the localic reflection is an equivalence.",
            ],
            metadata={**base, "criterion": "explicit_localic", "witness": witness},
        )

    if _matches_any(tags, {"set_topos"}):
        return Result.true(
            mode="theorem",
            value="localic_topos",
            justification=[
                "Tag 'set_topos': Set = Sh(1) is localic — it is sheaves on the "
                "one-element locale (the terminal locale). The only subterminal object "
                "of Set is 1 itself, and Omega_Set = 1.",
            ],
            metadata={**base, "criterion": "set_localic"},
        )

    if _matches_any(tags, {"presheaf_topos", "g_sets_topos",
                            "classifying_topos", "etale_topos"}):
        blocking = next(t for t in tags if t in {"presheaf_topos", "g_sets_topos",
                                                    "classifying_topos", "etale_topos"})
        return Result.false(
            mode="theorem",
            value="localic_topos",
            justification=[
                f"Tag {blocking!r}: presheaf toposes [C^op, Set] for non-preorder C, "
                "classifying toposes BG, and etale toposes are generally NOT localic. "
                "For BG (G non-trivial group): the only subobjects of 1 in [G-Set] are "
                "the empty set and {*} (one-point G-set), so Omega_BG = 2 — but BG is "
                "not equivalent to Sh(2); it has non-trivial G-action structure.",
            ],
            metadata={**base, "criterion": "not_localic_presheaf"},
        )

    return Result.unknown(
        mode="symbolic",
        value="localic_topos",
        justification=[
            "Insufficient tags to determine localic topos. "
            "Supply tags such as 'localic_topos', 'sheaves_on_space', 'set_topos', "
            "'presheaf_topos', 'g_sets_topos', or 'etale_topos'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_enough_points_topos(space: Any) -> Result:
    """Check whether the topos has enough points.

    A Grothendieck topos E has enough points if the collection of geometric
    morphisms {p: Set -> E} (the 'points' of E) jointly reflects isomorphisms:
    a morphism f: X -> Y in E is an iso iff p*(f) is an iso in Set for every
    point p. Key facts:
    - Set, [C^op, Set], BG, and Sh(X) for X sober all have enough points.
    - Barr's theorem: every Grothendieck topos has a surjective geometric morphism
      from a Boolean topos with enough points (so every topos is 'covered' by one
      with enough points).
    - The etale topos of an arithmetic scheme may lack enough points (geometric
      points are scarce over number fields).
    - The effective topos Eff has very few points (only the standard model).

    Decision layers
    ---------------
    1. Explicit 'enough_points_topos' tag -> true.
    2. Presheaf / Set / G-sets / Sh(sober space) -> true.
    3. Effective / realizability topos -> false.
    4. 'not_enough_points' tag -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"enough_points_topos", "set_valued_points",
                            "spatial_topos", "localic_spatial"}):
        witness = next(t for t in tags if t in {"enough_points_topos",
                                                   "set_valued_points", "spatial_topos",
                                                   "localic_spatial"})
        return Result.true(
            mode="theorem",
            value="enough_points",
            justification=[
                f"Tag {witness!r}: the topos has enough points — geometric morphisms "
                "Set -> E jointly detect isomorphisms. Each point p: Set -> E gives "
                "a 'stalk' functor p*: E -> Set.",
            ],
            metadata={**base, "criterion": "explicit_enough_points", "witness": witness},
        )

    if _matches_any(tags, {"presheaf_topos", "set_topos", "g_sets_topos",
                            "sheaves_hausdorff_space", "atomic_boolean_topos"}):
        witness = next(t for t in tags if t in {"presheaf_topos", "set_topos",
                                                   "g_sets_topos",
                                                   "sheaves_hausdorff_space",
                                                   "atomic_boolean_topos"})
        return Result.true(
            mode="theorem",
            value="enough_points",
            justification=[
                f"Tag {witness!r}: presheaf toposes have enough points (representable "
                "functors p_c: Set -> [C^op, Set] with p_c^*(F) = F(c) are jointly "
                "conservative). Set has enough points trivially. Sheaves on sober "
                "spaces have enough points (points = points of the space).",
            ],
            metadata={**base, "criterion": "presheaf_enough_points", "witness": witness},
        )

    if _matches_any(tags, NOT_GROTHENDIECK_TAGS | {"not_enough_points",
                                                     "no_set_valued_points"}):
        blocking = next(t for t in tags if t in (NOT_GROTHENDIECK_TAGS |
                                                    {"not_enough_points",
                                                     "no_set_valued_points"}))
        return Result.false(
            mode="theorem",
            value="enough_points",
            justification=[
                f"Tag {blocking!r}: the topos does NOT have enough points. "
                "The effective topos Eff has very few geometric morphisms from Set "
                "(only the standard model). The non-classical internal logic prevents "
                "enough classical points from existing.",
            ],
            metadata={**base, "criterion": "not_enough_points"},
        )

    return Result.unknown(
        mode="symbolic",
        value="enough_points",
        justification=[
            "Insufficient tags to determine enough points. "
            "Supply tags such as 'enough_points_topos', 'presheaf_topos', 'set_topos', "
            "'effective_topos', 'not_enough_points', or 'sheaves_hausdorff_space'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_topos(space: Any) -> dict[str, Any]:
    """Classify the topos type of space.

    Keys
    ----
    topos_class : str
        One of ``"set"``, ``"boolean_grothendieck"``, ``"localic"``,
        ``"grothendieck"``, ``"elementary"``, ``"unknown"``.
    is_grothendieck_topos : Result
    is_boolean_topos : Result
    is_localic_topos : Result
    has_enough_points_topos : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    groth_r = is_grothendieck_topos(space)
    bool_r = is_boolean_topos(space)
    localic_r = is_localic_topos(space)
    points_r = has_enough_points_topos(space)

    if _matches_any(tags, {"set_topos"}):
        topos_class = "set"
    elif groth_r.is_true and bool_r.is_true and not localic_r.is_true:
        topos_class = "boolean_grothendieck"
    elif localic_r.is_true:
        topos_class = "localic"
    elif groth_r.is_true:
        topos_class = "grothendieck"
    elif _matches_any(tags, ELEMENTARY_TOPOS_TAGS):
        topos_class = "elementary"
    else:
        topos_class = "unknown"

    key_properties: list[str] = []
    if groth_r.is_true:
        key_properties.append("grothendieck")
    if groth_r.is_false:
        key_properties.append("not_grothendieck")
    if bool_r.is_true:
        key_properties.append("boolean")
    if bool_r.is_false:
        key_properties.append("intuitionistic")
    if localic_r.is_true:
        key_properties.append("localic")
    if points_r.is_true:
        key_properties.append("enough_points")
    if points_r.is_false:
        key_properties.append("no_enough_points")
    if _matches_any(tags, {"has_natural_number_object", "grothendieck_topos",
                            "presheaf_topos", "sheaves_on_site", "set_topos",
                            "effective_topos"}):
        key_properties.append("natural_number_object")

    return {
        "topos_class": topos_class,
        "is_grothendieck_topos": groth_r,
        "is_boolean_topos": bool_r,
        "is_localic_topos": localic_r,
        "has_enough_points_topos": points_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def topos_profile(space: Any) -> dict[str, Any]:
    """Full topos theory profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_topos`.
    named_profiles : tuple[ToposProfile, ...]
        Registry of canonical topos theory examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_topos(space),
        "named_profiles": get_named_topos_profiles(),
        "layer_summary": topos_layer_summary(),
    }


# ---------------------------------------------------------------------------
# Computational engines (P8.2)
# ---------------------------------------------------------------------------

def site_from_finite_topology(
    open_sets: list[frozenset],
    universe: frozenset,
) -> dict[str, Any]:
    """Build a Grothendieck site from a finite topological space.

    Objects = open sets. Morphisms = inclusions U ⊆ V (restriction direction).
    Covering J(U) = the maximal sieve = all open sets V with V ⊆ U.
    Also validates that the input forms a valid topology.

    Parameters
    ----------
    open_sets: list of open sets (each a frozenset of points)
    universe: the total space (= union of all open sets)

    Returns
    -------
    dict with ``n_objects``, ``n_morphisms``, ``coverings``,
    ``topology_valid``, ``objects``.

    Examples
    --------
    >>> site = site_from_finite_topology(
    ...     [frozenset(), frozenset({0}), frozenset({0, 1})],
    ...     frozenset({0, 1}),
    ... )
    >>> site["n_objects"]
    3
    """
    objs: list[frozenset] = list({frozenset(s) for s in open_sets})
    morphisms = [(u, v) for u in objs for v in objs if u < v]
    fs_universe = frozenset(universe)
    has_empty = frozenset() in objs
    has_universe = fs_universe in objs
    closed_union = all(u | v in objs for u in objs for v in objs)
    closed_inter = all(u & v in objs for u in objs for v in objs)
    valid = has_empty and has_universe and closed_union and closed_inter
    # Covering sieve J(U) = all opens V ⊆ U (maximal Grothendieck topology)
    coverings: dict[Any, list[frozenset]] = {u: [v for v in objs if v <= u] for u in objs}
    return {
        "n_objects": len(objs),
        "n_morphisms": len(morphisms),
        "coverings": coverings,
        "topology_valid": valid,
        "objects": objs,
    }


def sheaf_on_site(
    site: dict[str, Any],
    assignment: dict[frozenset, Any],
) -> dict[str, Any]:
    """Check sheaf conditions for a constant presheaf on a finite site.

    The presheaf F assigns a value to each open set. Restriction maps are
    assumed identity (constant presheaf). Checks:
    - Locality: cover values agree → value on U must agree with them.
    - Gluing: cover values are consistent → value on U equals them.

    Parameters
    ----------
    site: output of ``site_from_finite_topology``
    assignment: maps each open set to an integer section value

    Returns
    -------
    dict with ``locality_ok``, ``gluing_ok``, ``is_sheaf``, ``failures``.

    Examples
    --------
    Constant assignment is always a sheaf:

    >>> site = site_from_finite_topology(
    ...     [frozenset(), frozenset({0}), frozenset({0, 1})], frozenset({0, 1})
    ... )
    >>> sheaf_on_site(site, {u: 1 for u in site["objects"]})["is_sheaf"]
    True
    """
    objects: list[frozenset] = site.get("objects", [])
    coverings: dict[Any, list[frozenset]] = site.get("coverings", {})
    locality_ok = True
    gluing_ok = True
    failures: list[str] = []
    for u in objects:
        cover = [v for v in coverings.get(u, []) if v < u]
        if not cover:
            continue
        u_val = assignment.get(u)
        cover_vals = [assignment.get(v) for v in cover if v in assignment]
        non_none = [v for v in cover_vals if v is not None]
        if not non_none:
            continue
        unique = set(non_none)
        if len(unique) == 1:
            cv = next(iter(unique))
            if u_val is not None and u_val != cv:
                locality_ok = False
                failures.append(
                    f"locality: U={set(u)!r} cover agrees on {cv} but F(U)={u_val}"
                )
        if non_none and u_val is not None and not all(v == u_val for v in non_none):
            gluing_ok = False
            failures.append(
                f"gluing: U={set(u)!r} cover={non_none}, F(U)={u_val}"
            )
    return {
        "locality_ok": locality_ok,
        "gluing_ok": gluing_ok,
        "is_sheaf": locality_ok and gluing_ok,
        "failures": failures,
    }


def sheafification_finite(
    site: dict[str, Any],
    presheaf: dict[frozenset, Any],
) -> dict[str, Any]:
    """Sheafification of a presheaf over a finite site (+ construction).

    For each open U, F^+(U) is computed by taking the value consistent with
    the cover: if the restrictions to all proper opens V ⊆ U agree on a
    value c, then F^+(U) is set to c (overriding any inconsistent value).
    One application of + suffices for finite topological spaces.

    Parameters
    ----------
    site: output of ``site_from_finite_topology``
    presheaf: maps each open set to a comparable value

    Returns
    -------
    dict with ``sheafification``, ``already_sheaf``, ``n_corrections``,
    ``is_sheaf_after``.

    Examples
    --------
    Constant presheaf is already a sheaf:

    >>> site = site_from_finite_topology(
    ...     [frozenset(), frozenset({0}), frozenset({0, 1})], frozenset({0, 1})
    ... )
    >>> r = sheafification_finite(site, {u: 7 for u in site["objects"]})
    >>> r["already_sheaf"]
    True
    """
    objects: list[frozenset] = site.get("objects", [])
    coverings: dict[Any, list[frozenset]] = site.get("coverings", {})
    result: dict[frozenset, Any] = {}
    n_corrections = 0
    for u in objects:
        cover = [v for v in coverings.get(u, []) if v < u]
        u_val = presheaf.get(u)
        if not cover:
            result[u] = u_val
            continue
        cover_vals = [presheaf.get(v) for v in cover if v in presheaf]
        non_none = [v for v in cover_vals if v is not None]
        if non_none and all(v == non_none[0] for v in non_none):
            canonical = non_none[0]
            if u_val != canonical:
                result[u] = canonical
                n_corrections += 1
            else:
                result[u] = u_val
        else:
            result[u] = u_val
    check = sheaf_on_site(site, result)
    return {
        "sheafification": result,
        "already_sheaf": n_corrections == 0 and check["is_sheaf"],
        "n_corrections": n_corrections,
        "is_sheaf_after": check["is_sheaf"],
    }


def topos_check(
    open_sets: list[frozenset],
    universe: frozenset,
) -> dict[str, Any]:
    """Verify Giraud axioms for Sh(X) where X is a finite topological space.

    For any topological space (X, τ), Sh(X) is a Grothendieck topos. This
    function checks the concrete conditions for finite X:
    - Terminal object: the sheaf assigning {*} to every U exists.
    - Fiber products: exist when intersections of opens are open.
    - Subobject classifier: Ω(U) = {V open : V ⊆ U} is always a sheaf.

    Parameters
    ----------
    open_sets: list of open sets (as frozensets)
    universe: the total space

    Returns
    -------
    dict with ``has_terminal``, ``has_fiber_products``,
    ``has_subobject_classifier``, ``is_grothendieck_topos``.

    Examples
    --------
    Any valid topology gives a Grothendieck topos:

    >>> topos_check([frozenset(), frozenset({0}), frozenset({0, 1})],
    ...             frozenset({0, 1}))["is_grothendieck_topos"]
    True
    """
    site = site_from_finite_topology(open_sets, universe)
    objs: list[frozenset] = site["objects"]
    valid: bool = site["topology_valid"]
    has_terminal = valid
    has_fp = all(u & v in objs for u in objs for v in objs)
    has_omega = has_fp  # Ω(U)={V:V⊆U} is always a sheaf when ∩ is open
    is_topos = valid and has_terminal and has_fp and has_omega
    return {
        "n_objects": len(objs),
        "has_terminal": has_terminal,
        "has_fiber_products": has_fp,
        "has_subobject_classifier": has_omega,
        "is_grothendieck_topos": is_topos,
    }


__all__ = [
    "ToposProfile",
    "GROTHENDIECK_TOPOS_TAGS",
    "ELEMENTARY_TOPOS_TAGS",
    "BOOLEAN_TOPOS_TAGS",
    "LOCALIC_TOPOS_TAGS",
    "ENOUGH_POINTS_TAGS",
    "NOT_BOOLEAN_TOPOS_TAGS",
    "NOT_GROTHENDIECK_TAGS",
    "GEOMETRIC_MORPHISM_TAGS",
    "get_named_topos_profiles",
    "topos_layer_summary",
    "topos_chapter_index",
    "topos_type_index",
    "is_grothendieck_topos",
    "is_boolean_topos",
    "is_localic_topos",
    "has_enough_points_topos",
    "classify_topos",
    "topos_profile",
    # P8.2 computational engines
    "site_from_finite_topology",
    "sheaf_on_site",
    "sheafification_finite",
    "topos_check",
]
