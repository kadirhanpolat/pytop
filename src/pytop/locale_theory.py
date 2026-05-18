"""Locale theory: frames, locales, pointfree topology, and the Isbell adjunction.

Key theorems implemented
------------------------
- Frames and locales: a frame L is a complete lattice satisfying the infinite
  distributive law a ^ (big-join S) = big-join{a ^ s : s in S} for all a in L
  and all S ⊆ L. A locale is a frame regarded as a generalised space; the
  category Loc = Frm^op. Frame homomorphisms f: L -> M preserve finite meets
  and arbitrary joins; localic maps go in the opposite direction.
- The Isbell adjunction: there is a contravariant adjunction
      Omega: Top^op ⟶⟵ Frm : pt
  where Omega(X) is the frame of open sets of X and pt(L) is the space of
  frame homomorphisms L -> {0,1} (the 'points' of L). The adjunction restricts
  to a dual equivalence between sober topological spaces and spatial locales.
- Spatial locales: a locale L is spatial if the canonical surjection
  Omega(pt(L)) -> L is an isomorphism — equivalently, L has enough points to
  distinguish its elements. The locale Omega(X) is spatial iff X is sober.
  In ZFC every compact regular locale is spatial; constructively this fails.
- Compact regular locales: in classical mathematics, compact regular locales
  correspond exactly to compact Hausdorff spaces (Isbell 1972). The compact
  regular locales form a reflective subcategory of Loc.
- The locale of random reals (measure algebra locale): the measure algebra
  B(R)/N — Borel sets modulo Lebesgue null sets — is a complete Boolean
  algebra, hence a compact zero-dimensional regular locale. Its points (frame
  homomorphisms to {0,1}) require the ultrafilter lemma; constructively (or in
  ZF without AC) this locale has no points at all, yet it carries a canonical
  probability measure. This is the canonical example showing locales strictly
  extend classical point-set topology.
- Stone locales (localic Stone duality): a locale is a Stone locale iff it
  is compact, regular, and zero-dimensional (complemented elements form a
  base). Stone duality for locales: Stone locales correspond to Boolean
  algebras (Johnstone 1982). A spatial Stone locale is a Stone space
  (compact totally disconnected Hausdorff space).
- Isbell's density theorem for localic groups: every localic group (a group
  object in Loc) is spatial — it has enough points (Isbell 1988). Hence
  locally compact localic groups coincide with locally compact Hausdorff
  topological groups. This theorem shows localic groups do not go beyond
  classical topology, unlike general locales.
- The well-inside relation: in a frame L, b << a ('b is well-inside a') means
  b* v a = 1 where b* = join{c : b ^ c = 0} is the pseudocomplement. A locale
  is regular iff a = join{b : b << a} for every a in L. It is completely
  regular iff the well-inside relation satisfies interpolation: b << a implies
  there exists c with b << c << a.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class LocaleProfile:
    """A curated locale theory example."""

    key: str
    display_name: str
    locale_type: str
    is_spatial: bool
    is_compact: bool
    is_regular: bool
    is_completely_regular: bool
    is_zero_dimensional: bool
    is_localic_group: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

SPATIAL_LOCALE_TAGS: frozenset[str] = frozenset({
    "spatial_locale", "has_enough_points",
    "sober", "sober_space",
    "hausdorff", "t2", "compact_hausdorff", "metrizable",
    "stone_space", "profinite",
    "completely_regular", "tychonoff",
    "locally_compact_hausdorff",
    "localic_group",
})

COMPACT_LOCALE_TAGS: frozenset[str] = frozenset({
    "compact_locale",
    "compact", "compact_hausdorff",
    "stone_space", "profinite",
    "finite_locale",
    "compact_regular_locale", "compact_regular",
    "stone_locale", "boolean_locale",
})

REGULAR_LOCALE_TAGS: frozenset[str] = frozenset({
    "regular_locale",
    "compact_hausdorff", "metrizable",
    "stone_space", "profinite",
    "completely_regular_locale",
    "locally_compact_regular",
    "compact_regular", "compact_regular_locale",
    "boolean_locale", "stone_locale",
    "complete_boolean_algebra",
})

COMPLETELY_REGULAR_LOCALE_TAGS: frozenset[str] = frozenset({
    "completely_regular_locale",
    "tychonoff_locale",
    "compact_hausdorff", "metrizable",
    "stone_space", "profinite",
    "compact_regular", "compact_regular_locale",
    "boolean_locale", "stone_locale",
    "complete_boolean_algebra",
})

ZERO_DIMENSIONAL_LOCALE_TAGS: frozenset[str] = frozenset({
    "zero_dimensional_locale",
    "stone_locale", "boolean_locale",
    "stone_space", "profinite",
    "complete_boolean_algebra",
    "clopen_base_locale",
})

NON_SPATIAL_LOCALE_TAGS: frozenset[str] = frozenset({
    "non_spatial_locale",
    "no_classical_points",
    "measure_algebra_locale",
    "pointfree_only",
    "non_spatial_frame",
    "random_real_locale",
})

LOCALIC_GROUP_TAGS: frozenset[str] = frozenset({
    "localic_group",
    "group_object_in_loc",
    "topological_group_sober",
    "localic_abelian_group",
    "localic_compact_group",
})

NOT_REGULAR_LOCALE_TAGS: frozenset[str] = frozenset({
    "not_regular_locale",
    "t0_not_t1",
    "sierpinski_locale",
    "generic_point_locale",
    "not_hausdorff_locale",
    "not_completely_regular",
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

def get_named_locale_profiles() -> tuple[LocaleProfile, ...]:
    """Return the registry of canonical locale theory examples."""
    return (
        LocaleProfile(
            key="localic_real_line",
            display_name="Omega(R) — the localic real line",
            locale_type="spatial_locale",
            is_spatial=True,
            is_compact=False,
            is_regular=True,
            is_completely_regular=True,
            is_zero_dimensional=False,
            is_localic_group=True,
            presentation_layer="main_text",
            focus=(
                "The localic real line is the locale Omega(R) — the frame of open "
                "subsets of the classical real line R, ordered by inclusion. Since R is "
                "a completely regular (Tychonoff) sober space, Omega(R) is a spatial "
                "locale: the canonical map Omega(pt(Omega(R))) -> Omega(R) is an "
                "isomorphism, and pt(Omega(R)) recovers R up to homeomorphism. "
                "Omega(R) is a regular frame: every open U equals the join of all "
                "opens V with V << U (well-inside). It is completely regular, with "
                "the well-inside relation satisfying interpolation. "
                "Omega(R) is NOT compact: the open cover {(-n,n) : n in N} has no "
                "finite subcover. "
                "R is a topological group (under addition), and its sobriety implies "
                "that Omega(R) is a localic group: a group object in Loc. By Isbell's "
                "density theorem, all localic groups are spatial — so no new examples "
                "arise beyond classical topological groups in this setting. "
                "The frame Omega(R) is not zero-dimensional: the connected topology of "
                "R means no clopen base exists. The localic real line is the reference "
                "object for constructive/pointfree analysis (constructive Dedekind reals)."
            ),
            chapter_targets=("10", "28", "52"),
        ),
        LocaleProfile(
            key="random_real_locale",
            display_name="B(R)/N — locale of random reals (measure algebra)",
            locale_type="non_spatial_locale",
            is_spatial=False,
            is_compact=True,
            is_regular=True,
            is_completely_regular=True,
            is_zero_dimensional=True,
            is_localic_group=False,
            presentation_layer="main_text",
            focus=(
                "The measure algebra locale is the locale associated with the complete "
                "Boolean algebra B(R)/N — the sigma-algebra of Borel sets of R modulo "
                "the Lebesgue null sets. It is a complete Boolean algebra, hence a "
                "compact zero-dimensional regular locale (Stone locale in the localic "
                "sense). Every complete Boolean algebra gives a Stone locale by "
                "Johnstone's localic Stone duality. "
                "This locale is NOT spatial: its points would be ultrafilters on B(R)/N "
                "satisfying countable completeness — their existence requires the "
                "ultrafilter lemma (a weak form of AC). Constructively (in IZF or ZF "
                "without AC), this locale has no points at all. Yet it is a perfectly "
                "well-defined locale carrying a canonical probability measure P (the "
                "push-forward of Lebesgue measure along the quotient map). "
                "This is the flagship example of pointfree topology's superiority: a "
                "locale with rich mathematical structure (measure, group actions of R by "
                "translation) but no classical points. The Gelfand duality for measure "
                "algebras — relating B(R)/N to the space of 'random reals' — is "
                "foundational in abstract measure theory and categorical logic. "
                "The Boolean algebra B(R)/N has no atoms (every non-zero element splits) "
                "and is sigma-complete (countable joins exist), making it the unique "
                "(up to isomorphism) separable atomless complete Boolean algebra."
            ),
            chapter_targets=("10", "28", "52"),
        ),
        LocaleProfile(
            key="stone_locale_profinite",
            display_name="Profinite completion — Stone locale (compact zero-dimensional regular)",
            locale_type="stone_locale",
            is_spatial=True,
            is_compact=True,
            is_regular=True,
            is_completely_regular=True,
            is_zero_dimensional=True,
            is_localic_group=False,
            presentation_layer="main_text",
            focus=(
                "A Stone locale is a compact, zero-dimensional, regular locale — "
                "one whose complemented elements (those a in L with a v a* = 1 and "
                "a ^ a* = 0) form a generating set (base). Stone locales correspond "
                "bijectively to Boolean algebras: the Boolean algebra is the set of "
                "complemented elements, and the Stone locale is its ideal completion. "
                "Spatial Stone locales are exactly the Stone spaces (compact totally "
                "disconnected Hausdorff spaces). "
                "The profinite completion of a residually finite group G — "
                "the inverse limit lim G/N over normal subgroups of finite index — "
                "is a Stone space (profinite group), hence a spatial Stone locale. "
                "Key examples: the p-adic integers Z_p = lim Z/p^n Z (Stone space, "
                "profinite abelian group), the absolute Galois group Gal(Q^alg / Q) "
                "(profinite group, Stone space), and the Cantor set 2^N (Stone space, "
                "universal object in Stone spaces). "
                "Stone duality for locales: Stone Loc ≃ Bool^op. The Boolean algebra "
                "corresponding to a Stone locale L is the lattice of complemented "
                "elements of the frame O(L). This dualises the classical Stone "
                "representation theorem for Boolean algebras."
            ),
            chapter_targets=("10", "28", "52"),
        ),
        LocaleProfile(
            key="unit_interval_locale",
            display_name="[0,1] — the localic unit interval",
            locale_type="compact_regular",
            is_spatial=True,
            is_compact=True,
            is_regular=True,
            is_completely_regular=True,
            is_zero_dimensional=False,
            is_localic_group=False,
            presentation_layer="main_text",
            focus=(
                "The localic unit interval is the locale Omega([0,1]) — the frame of "
                "open sets of the closed unit interval with the subspace topology from R. "
                "Since [0,1] is compact Hausdorff (hence sober), Omega([0,1]) is a "
                "spatial compact regular locale. By the classical theorem (Isbell 1972), "
                "compact regular locales correspond exactly to compact Hausdorff spaces "
                "(in the presence of AC), so Omega([0,1]) represents the compact "
                "Hausdorff space [0,1] in the localic world. "
                "[0,1] is connected and locally connected, hence Omega([0,1]) is NOT "
                "zero-dimensional: the topology has no clopen base (the only clopen "
                "sets of [0,1] are the empty set and [0,1] itself). "
                "The well-inside relation in Omega([0,1]) corresponds to: V << U iff "
                "cl(V) ⊆ U (closure contained in U). Regularity: every open U equals "
                "the join of all opens V with cl(V) ⊆ U, reflecting the normality of "
                "[0,1]. Completely regular: for each x in U, Urysohn's lemma gives a "
                "continuous f: [0,1] -> [0,1] with f(x) = 0 and f = 1 off U, "
                "witnessing the interpolation of well-inside. "
                "Constructively, the localic unit interval [0,1]_loc is defined by "
                "generators (p,q) for p < q rationals and relations encoding "
                "overlapping intervals — it is the correct constructive analogue of [0,1]."
            ),
            chapter_targets=("10", "28", "52"),
        ),
        LocaleProfile(
            key="sierpinski_locale",
            display_name="S — the Sierpinski locale (two-point T0 non-regular locale)",
            locale_type="t0_locale",
            is_spatial=True,
            is_compact=True,
            is_regular=False,
            is_completely_regular=False,
            is_zero_dimensional=False,
            is_localic_group=False,
            presentation_layer="selected_block",
            focus=(
                "The Sierpinski locale is the locale corresponding to the Sierpinski "
                "space S = {0,1} with open sets {empty, {1}, {0,1}}. As a frame, "
                "O(S) = {bot, u, top} where bot < u < top with u = {1} = the "
                "generic open. O(S) is isomorphic to the three-element chain. "
                "S is T0 but NOT T1 (the point 0 is not closed: its closure is {0,1}). "
                "Since S is not T1, it is not regular and not completely regular. "
                "S is compact (finite), sober (S = Spec(Z/(2) -> Z/(0)) has a generic "
                "point at 0 and a closed point at 1), and spatial. "
                "The Sierpinski locale is NOT zero-dimensional: the only clopen sets of "
                "S are the empty set and S itself, so the clopen sets do not form a "
                "base for the topology. The generic point 0 prevents any clopen "
                "separation. "
                "The Sierpinski locale serves as the subobject classifier in the topos "
                "of sheaves on a topological space: a map X -> S (localically) "
                "classifies open subsets of X. More precisely, the Sierpinski space is "
                "the 'truth value object' in many logical and sheaf-theoretic contexts. "
                "Dually, the frame O(S) = {bot, u, top} is the initial frame: every "
                "frame has a unique frame homomorphism from it."
            ),
            chapter_targets=("10", "28"),
        ),
        LocaleProfile(
            key="localic_torus",
            display_name="T^2 — the localic torus (compact spatial localic group)",
            locale_type="localic_group",
            is_spatial=True,
            is_compact=True,
            is_regular=True,
            is_completely_regular=True,
            is_zero_dimensional=False,
            is_localic_group=True,
            presentation_layer="selected_block",
            focus=(
                "The localic torus is the locale Omega(T^2) where T^2 = S^1 x S^1 "
                "is the classical torus. Since T^2 is a compact Hausdorff space "
                "(hence sober), Omega(T^2) is a compact regular spatial locale. "
                "T^2 carries a topological group structure (the product group "
                "(R/Z) x (R/Z)) with continuous multiplication and inversion, and "
                "sobriety implies that Omega(T^2) is a localic group: a group object "
                "in the category Loc of locales. "
                "Isbell's density theorem (1988): every localic group is spatial, "
                "i.e., has enough points. This means that localic groups — despite "
                "being defined purely in terms of the frame of opens — automatically "
                "recover a classical space of points. Thus localic group theory is "
                "equivalent to sober topological group theory in classical mathematics. "
                "Constructively, Isbell's theorem requires only modest choice principles. "
                "Omega(T^2) is NOT zero-dimensional: T^2 is connected (path-connected), "
                "so the only clopen sets are the empty set and T^2 itself. "
                "The fundamental group pi_1(T^2) = Z x Z. "
                "Compact localic groups correspond to compact Hausdorff topological "
                "groups by Isbell's theorem; Pontryagin duality applies in the spatial "
                "case. The localic perspective on T^2 is valuable in constructive "
                "harmonic analysis and classifying topos theory."
            ),
            chapter_targets=("10", "28"),
        ),
    )


def locale_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_locale_profiles()
    ))


def locale_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_locale_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def locale_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from locale_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_locale_profiles():
        index.setdefault(p.locale_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_spatial_locale(space: Any) -> Result:
    """Check whether the locale associated to space is spatial (has enough points).

    A locale L is spatial if the canonical surjection Omega(pt(L)) -> L is an
    isomorphism. Equivalently, L has enough frame homomorphisms L -> {0,1} to
    distinguish its elements. Key facts:
    - Omega(X) is spatial iff X is sober (the unit X -> pt(Omega(X)) is a homeomorphism).
    - Every Hausdorff (T2) space is sober, hence Omega(X) is spatial.
    - Every metrizable space is sober (metrizable => T2 => sober).
    - The measure algebra locale B(R)/N is NOT spatial: no 'random reals' exist
      constructively, and classically their existence requires the ultrafilter lemma.
    - In ZFC, every compact regular locale is spatial; constructively this fails.
    - Localic groups are always spatial (Isbell's density theorem).

    Decision layers
    ---------------
    1. Explicit 'spatial_locale' / 'sober' / 'sober_space' tag -> true.
    2. Hausdorff / metrizable / compact Hausdorff (T2 => sober => spatial) -> true.
    3. Stone space / profinite / tychonoff -> true.
    4. Localic group (Isbell's density theorem: localic groups are spatial) -> true.
    5. Non-spatial / no-classical-points / measure-algebra -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"spatial_locale", "sober", "sober_space", "has_enough_points"}):
        witness = next(t for t in tags if t in {"spatial_locale", "sober",
                                                   "sober_space", "has_enough_points"})
        return Result.true(
            mode="theorem",
            value="spatial_locale",
            justification=[
                f"Tag {witness!r}: the locale is spatial — it has enough points. "
                "The canonical map Omega(pt(L)) -> L is an isomorphism: the frame "
                "recovers completely from its space of points.",
            ],
            metadata={**base, "criterion": "explicit_spatial", "witness": witness},
        )

    if _matches_any(tags, {"hausdorff", "t2", "compact_hausdorff",
                            "metrizable", "completely_regular", "tychonoff"}):
        witness = next(t for t in tags if t in {"hausdorff", "t2", "compact_hausdorff",
                                                   "metrizable", "completely_regular",
                                                   "tychonoff"})
        return Result.true(
            mode="theorem",
            value="spatial_locale",
            justification=[
                f"Tag {witness!r}: T2 (Hausdorff) spaces are sober, hence the "
                "associated locale Omega(X) is spatial. The T2 separation axiom "
                "guarantees that irreducible closed sets are closures of points.",
            ],
            metadata={**base, "criterion": "hausdorff_spatial", "witness": witness},
        )

    if _matches_any(tags, {"stone_space", "profinite", "locally_compact_hausdorff"}):
        witness = next(t for t in tags if t in {"stone_space", "profinite",
                                                   "locally_compact_hausdorff"})
        return Result.true(
            mode="theorem",
            value="spatial_locale",
            justification=[
                f"Tag {witness!r}: Stone spaces and profinite spaces are compact "
                "Hausdorff, hence sober — the associated locale is spatial.",
            ],
            metadata={**base, "criterion": "stone_spatial", "witness": witness},
        )

    if _matches_any(tags, LOCALIC_GROUP_TAGS):
        witness = next(t for t in tags if t in LOCALIC_GROUP_TAGS)
        return Result.true(
            mode="theorem",
            value="spatial_locale",
            justification=[
                f"Tag {witness!r}: Isbell's density theorem (1988) — every localic "
                "group is spatial. The group structure forces the locale to have "
                "enough points, making localic group theory equivalent to sober "
                "topological group theory.",
            ],
            metadata={**base, "criterion": "isbell_localic_group", "witness": witness},
        )

    if _matches_any(tags, NON_SPATIAL_LOCALE_TAGS):
        blocking = next(t for t in tags if t in NON_SPATIAL_LOCALE_TAGS)
        return Result.false(
            mode="theorem",
            value="spatial_locale",
            justification=[
                f"Tag {blocking!r}: the locale does NOT have enough points. "
                "The canonical map Omega(pt(L)) -> L is not surjective — distinct "
                "elements of the frame cannot be separated by frame homomorphisms to "
                "{0,1}. The measure algebra locale B(R)/N is the paradigmatic example: "
                "its points (ultrafilters) require the ultrafilter lemma.",
            ],
            metadata={**base, "criterion": "non_spatial_locale"},
        )

    return Result.unknown(
        mode="symbolic",
        value="spatial_locale",
        justification=[
            "Insufficient tags to determine spatiality. "
            "Supply tags such as 'spatial_locale', 'sober', 'hausdorff', "
            "'stone_space', 'localic_group', 'non_spatial_locale', or 'measure_algebra_locale'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_compact_locale(space: Any) -> Result:
    """Check whether the locale is compact.

    A locale L is compact if every directed open cover has a finite subcover:
    equivalently, the top element of the frame is inaccessible by directed joins
    of proper elements. In frame terms: 1 = big-join S implies 1 in S_finite for
    some finite S_finite ⊆ S. Key facts:
    - Omega(X) is compact iff X is compact.
    - Complete Boolean algebras give compact locales (Stone locales).
    - The Stone-Cech compactification of a Tychonoff space is compact regular.
    - Compact locales need not be spatial (the measure algebra locale).

    Decision layers
    ---------------
    1. Explicit 'compact_locale' / 'compact' / 'compact_hausdorff' tag -> true.
    2. Stone locale / Boolean locale / profinite (compact by definition) -> true.
    3. Measure algebra (complete Boolean algebra => compact locale) -> true.
    4. 'non_compact_locale' / real-line-like tags -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"compact_locale", "compact", "compact_hausdorff",
                            "compact_regular", "compact_regular_locale"}):
        witness = next(t for t in tags if t in {"compact_locale", "compact",
                                                   "compact_hausdorff", "compact_regular",
                                                   "compact_regular_locale"})
        return Result.true(
            mode="theorem",
            value="compact_locale",
            justification=[
                f"Tag {witness!r}: the locale is compact. Every directed cover of "
                "the top element 1 by frame elements has a finite sub-cover. "
                "Equivalently, in the frame, 1 is inaccessible by proper directed joins.",
            ],
            metadata={**base, "criterion": "explicit_compact", "witness": witness},
        )

    if _matches_any(tags, {"stone_locale", "boolean_locale", "stone_space",
                            "profinite", "finite_locale"}):
        witness = next(t for t in tags if t in {"stone_locale", "boolean_locale",
                                                   "stone_space", "profinite", "finite_locale"})
        return Result.true(
            mode="theorem",
            value="compact_locale",
            justification=[
                f"Tag {witness!r}: Stone locales (compact zero-dimensional regular) "
                "are compact by definition. Profinite spaces and Stone spaces are "
                "compact Hausdorff, hence their locales are compact.",
            ],
            metadata={**base, "criterion": "stone_compact", "witness": witness},
        )

    if _matches_any(tags, {"measure_algebra_locale", "complete_boolean_algebra",
                            "random_real_locale"}):
        witness = next(t for t in tags if t in {"measure_algebra_locale",
                                                   "complete_boolean_algebra",
                                                   "random_real_locale"})
        return Result.true(
            mode="theorem",
            value="compact_locale",
            justification=[
                f"Tag {witness!r}: complete Boolean algebras give compact locales "
                "(their ideal completions are Stone locales, which are compact). "
                "The measure algebra B(R)/N is a complete Boolean algebra, hence "
                "its locale is compact — even without classical points.",
            ],
            metadata={**base, "criterion": "boolean_compact", "witness": witness},
        )

    if _matches_any(tags, {"non_compact_locale", "real_line_locale", "open_locale"}):
        blocking = next(t for t in tags if t in {"non_compact_locale",
                                                    "real_line_locale", "open_locale"})
        return Result.false(
            mode="theorem",
            value="compact_locale",
            justification=[
                f"Tag {blocking!r}: the locale is NOT compact. "
                "The real line locale Omega(R) is not compact: the cover by "
                "bounded intervals has no finite subcover.",
            ],
            metadata={**base, "criterion": "non_compact"},
        )

    return Result.unknown(
        mode="symbolic",
        value="compact_locale",
        justification=[
            "Insufficient tags to determine compactness. "
            "Supply tags such as 'compact_locale', 'compact', 'stone_locale', "
            "'profinite', 'measure_algebra_locale', or 'non_compact_locale'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_regular_locale(space: Any) -> Result:
    """Check whether the locale is regular.

    A locale L is regular if every element a in L satisfies a = join{b : b << a},
    where b << a (b is well-inside a) means b* v a = 1 (the pseudocomplement
    b* = join{c : b ^ c = 0} satisfies b* v a = 1). Key facts:
    - Every Hausdorff space gives a regular locale (T3 spaces satisfy the condition).
    - Every compact Hausdorff locale is regular.
    - Complete Boolean algebras give regular locales (every Boolean algebra is regular).
    - T0 but non-T1 spaces (e.g., Sierpinski) give non-regular locales.

    Decision layers
    ---------------
    1. Explicit 'regular_locale' tag -> true.
    2. Compact Hausdorff / metrizable -> true.
    3. Stone locale / Boolean algebra -> true.
    4. 'not_regular_locale' / 't0_not_t1' / 'sierpinski_locale' -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"regular_locale", "completely_regular_locale",
                            "tychonoff_locale"}):
        witness = next(t for t in tags if t in {"regular_locale",
                                                   "completely_regular_locale",
                                                   "tychonoff_locale"})
        return Result.true(
            mode="theorem",
            value="regular_locale",
            justification=[
                f"Tag {witness!r}: the locale is regular — every frame element a "
                "equals the join of all b well-inside a (b << a). "
                "Regularity is the pointfree analogue of the T3 separation axiom.",
            ],
            metadata={**base, "criterion": "explicit_regular", "witness": witness},
        )

    if _matches_any(tags, {"compact_hausdorff", "metrizable",
                            "locally_compact_regular", "compact_regular",
                            "compact_regular_locale"}):
        witness = next(t for t in tags if t in {"compact_hausdorff", "metrizable",
                                                   "locally_compact_regular",
                                                   "compact_regular", "compact_regular_locale"})
        return Result.true(
            mode="theorem",
            value="regular_locale",
            justification=[
                f"Tag {witness!r}: compact Hausdorff and metrizable spaces are T3 "
                "(regular Hausdorff), hence their frames are regular locales. "
                "In a compact Hausdorff space, every open U contains cl(V) ⊆ U for "
                "some open V, witnessing the well-inside relation.",
            ],
            metadata={**base, "criterion": "compact_hausdorff_regular", "witness": witness},
        )

    if _matches_any(tags, {"stone_locale", "boolean_locale", "stone_space",
                            "profinite", "complete_boolean_algebra",
                            "measure_algebra_locale"}):
        witness = next(t for t in tags if t in {"stone_locale", "boolean_locale",
                                                   "stone_space", "profinite",
                                                   "complete_boolean_algebra",
                                                   "measure_algebra_locale"})
        return Result.true(
            mode="theorem",
            value="regular_locale",
            justification=[
                f"Tag {witness!r}: Boolean algebras and their ideal completions give "
                "regular locales: for any complemented element b, b** = b and the "
                "well-inside relation satisfies b << a iff b ^ a* = 0, i.e., b <= a "
                "and b is complemented below a. Every element is a join of elements "
                "well-inside it.",
            ],
            metadata={**base, "criterion": "boolean_regular", "witness": witness},
        )

    if _matches_any(tags, NOT_REGULAR_LOCALE_TAGS):
        blocking = next(t for t in tags if t in NOT_REGULAR_LOCALE_TAGS)
        return Result.false(
            mode="theorem",
            value="regular_locale",
            justification=[
                f"Tag {blocking!r}: the locale is NOT regular. "
                "The Sierpinski locale and T0-not-T1 spaces fail regularity: "
                "the generic open u in Omega(S) = {bot, u, top} satisfies u << u "
                "only if u* v u = 1, but u* = bot (since u ^ bot = bot = 0 and "
                "u* = join{c : u ^ c = bot} = bot), so bot v u = u != top.",
            ],
            metadata={**base, "criterion": "not_regular"},
        )

    return Result.unknown(
        mode="symbolic",
        value="regular_locale",
        justification=[
            "Insufficient tags to determine locale regularity. "
            "Supply tags such as 'regular_locale', 'compact_hausdorff', 'metrizable', "
            "'stone_locale', 'sierpinski_locale', or 'not_regular_locale'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_stone_locale(space: Any) -> Result:
    """Check whether the locale is a Stone locale (compact zero-dimensional regular).

    A Stone locale is a compact, regular, zero-dimensional locale — one whose
    complemented elements form a generating set (base). Key facts:
    - Stone duality for locales: Stone Loc ≃ Bool^op (Johnstone 1982).
    - Every Boolean algebra B gives a Stone locale Idl(B) (the frame of ideals).
    - Spatial Stone locales are exactly the Stone spaces (compact T.D. Hausdorff).
    - The measure algebra B(R)/N gives a non-spatial Stone locale.
    - Connected locales (like [0,1] or R) are NOT Stone (no non-trivial clopen base).

    Decision layers
    ---------------
    1. Explicit 'stone_locale' / 'boolean_locale' tag -> true.
    2. Stone space / profinite -> true (spatial Stone locales).
    3. Complete Boolean algebra / measure algebra -> true (possibly non-spatial).
    4. 'connected_nontrivial' / 'not_zero_dimensional' -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"stone_locale", "boolean_locale", "clopen_base_locale"}):
        witness = next(t for t in tags if t in {"stone_locale", "boolean_locale",
                                                   "clopen_base_locale"})
        return Result.true(
            mode="theorem",
            value="stone_locale",
            justification=[
                f"Tag {witness!r}: the locale is a Stone locale — compact, regular, "
                "and zero-dimensional. Its frame is the ideal completion of a Boolean "
                "algebra. Stone duality: Stone Loc ≃ Bool^op maps each Boolean algebra "
                "to its Stone locale and back.",
            ],
            metadata={**base, "criterion": "explicit_stone_locale", "witness": witness},
        )

    if _matches_any(tags, {"stone_space", "profinite"}):
        witness = next(t for t in tags if t in {"stone_space", "profinite"})
        return Result.true(
            mode="theorem",
            value="stone_locale",
            justification=[
                f"Tag {witness!r}: Stone spaces (compact totally disconnected "
                "Hausdorff) and profinite spaces are spatial Stone locales. "
                "Their frames are Boolean: every open set is a (possibly infinite) "
                "join of clopen sets. Examples: Cantor set 2^N, p-adic integers Z_p.",
            ],
            metadata={**base, "criterion": "stone_space_locale", "witness": witness},
        )

    if _matches_any(tags, {"complete_boolean_algebra", "measure_algebra_locale",
                            "random_real_locale"}):
        witness = next(t for t in tags if t in {"complete_boolean_algebra",
                                                   "measure_algebra_locale",
                                                   "random_real_locale"})
        return Result.true(
            mode="theorem",
            value="stone_locale",
            justification=[
                f"Tag {witness!r}: complete Boolean algebras give Stone locales "
                "(compact zero-dimensional regular locales) via their ideal completion. "
                "The measure algebra B(R)/N gives a non-spatial Stone locale: a Stone "
                "locale without classical points, possible only in the localic world.",
            ],
            metadata={**base, "criterion": "boolean_stone_locale", "witness": witness},
        )

    if _matches_any(tags, {"connected_nontrivial", "not_zero_dimensional",
                            "path_connected", "simply_connected"}):
        blocking = next(t for t in tags if t in {"connected_nontrivial",
                                                    "not_zero_dimensional",
                                                    "path_connected", "simply_connected"})
        return Result.false(
            mode="theorem",
            value="stone_locale",
            justification=[
                f"Tag {blocking!r}: connected spaces / locales are NOT Stone. "
                "A Stone locale has a clopen base, but a non-trivial connected "
                "space has only trivial clopen sets (empty and whole space).",
            ],
            metadata={**base, "criterion": "connected_not_stone"},
        )

    return Result.unknown(
        mode="symbolic",
        value="stone_locale",
        justification=[
            "Insufficient tags to determine Stone locale. "
            "Supply tags such as 'stone_locale', 'stone_space', 'boolean_locale', "
            "'complete_boolean_algebra', 'profinite', or 'connected_nontrivial'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_localic_group(space: Any) -> Result:
    """Check whether space carries the structure of a localic group.

    A localic group is a group object in the category Loc of locales: a locale L
    equipped with localic maps m: L x L -> L (multiplication), i: L -> L (inversion),
    and e: 1 -> L (unit) satisfying the group axioms. Key facts:
    - Every sober topological group gives a localic group via Omega(-).
    - Isbell's density theorem: every localic group is spatial — the space of
      points pt(L) carries a canonical topological group structure, recovering L.
    - Hence the category of localic groups is equivalent to the category of sober
      topological groups (which in the Hausdorff case equals all topological groups).
    - Locally compact localic groups = locally compact Hausdorff topological groups.

    Decision layers
    ---------------
    1. Explicit 'localic_group' / 'group_object_in_loc' tag -> true.
    2. Sober topological group (Isbell: its Omega is a localic group) -> true.
    3. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, LOCALIC_GROUP_TAGS):
        witness = next(t for t in tags if t in LOCALIC_GROUP_TAGS)
        return Result.true(
            mode="theorem",
            value="localic_group",
            justification=[
                f"Tag {witness!r}: the locale is a localic group — a group object in "
                "Loc with localic maps for multiplication and inversion. By Isbell's "
                "density theorem (1988), every localic group is spatial, recovering a "
                "sober topological group whose frame of opens is the given locale.",
            ],
            metadata={**base, "criterion": "explicit_localic_group", "witness": witness},
        )

    if (_matches_any(tags, {"topological_group"}) and
            _matches_any(tags, {"sober", "hausdorff", "metrizable", "compact_hausdorff"})):
        return Result.true(
            mode="theorem",
            value="localic_group",
            justification=[
                "Tags 'topological_group' + sober/Hausdorff: a sober topological "
                "group G gives a localic group Omega(G). By Isbell's theorem, all "
                "localic groups arise this way — so Omega(G) is a localic group and "
                "pt(Omega(G)) ≅ G as topological groups.",
            ],
            metadata={**base, "criterion": "sober_group_localic"},
        )

    return Result.unknown(
        mode="symbolic",
        value="localic_group",
        justification=[
            "Insufficient tags to determine localic group structure. "
            "Supply tags such as 'localic_group', 'group_object_in_loc', "
            "'localic_abelian_group', or 'topological_group' combined with 'sober'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_locale(space: Any) -> dict[str, Any]:
    """Classify the locale type of space.

    Keys
    ----
    locale_class : str
        One of ``"non_spatial"``, ``"stone"``, ``"localic_group"``,
        ``"compact_regular"``, ``"spatial"``, ``"unknown"``.
    is_spatial_locale : Result
    is_compact_locale : Result
    is_regular_locale : Result
    is_stone_locale : Result
    is_localic_group : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    spatial_r = is_spatial_locale(space)
    compact_r = is_compact_locale(space)
    regular_r = is_regular_locale(space)
    stone_r = is_stone_locale(space)
    localic_group_r = is_localic_group(space)

    if _matches_any(tags, NON_SPATIAL_LOCALE_TAGS):
        locale_class = "non_spatial"
    elif stone_r.is_true and spatial_r.is_true:
        locale_class = "stone"
    elif localic_group_r.is_true:
        locale_class = "localic_group"
    elif compact_r.is_true and regular_r.is_true:
        locale_class = "compact_regular"
    elif spatial_r.is_true:
        locale_class = "spatial"
    else:
        locale_class = "unknown"

    key_properties: list[str] = []
    if spatial_r.is_true:
        key_properties.append("spatial")
    if spatial_r.is_false:
        key_properties.append("non_spatial")
    if compact_r.is_true:
        key_properties.append("compact")
    if regular_r.is_true:
        key_properties.append("regular")
    if stone_r.is_true:
        key_properties.append("stone_locale")
    if localic_group_r.is_true:
        key_properties.append("localic_group")
    if _matches_any(tags, ZERO_DIMENSIONAL_LOCALE_TAGS):
        key_properties.append("zero_dimensional")
    if _matches_any(tags, NOT_REGULAR_LOCALE_TAGS):
        key_properties.append("not_regular")

    return {
        "locale_class": locale_class,
        "is_spatial_locale": spatial_r,
        "is_compact_locale": compact_r,
        "is_regular_locale": regular_r,
        "is_stone_locale": stone_r,
        "is_localic_group": localic_group_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def locale_profile(space: Any) -> dict[str, Any]:
    """Full locale theory profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_locale`.
    named_profiles : tuple[LocaleProfile, ...]
        Registry of canonical locale theory examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_locale(space),
        "named_profiles": get_named_locale_profiles(),
        "layer_summary": locale_layer_summary(),
    }


__all__ = [
    "LocaleProfile",
    "SPATIAL_LOCALE_TAGS",
    "COMPACT_LOCALE_TAGS",
    "REGULAR_LOCALE_TAGS",
    "COMPLETELY_REGULAR_LOCALE_TAGS",
    "ZERO_DIMENSIONAL_LOCALE_TAGS",
    "NON_SPATIAL_LOCALE_TAGS",
    "LOCALIC_GROUP_TAGS",
    "NOT_REGULAR_LOCALE_TAGS",
    "get_named_locale_profiles",
    "locale_layer_summary",
    "locale_chapter_index",
    "locale_type_index",
    "is_spatial_locale",
    "is_compact_locale",
    "is_regular_locale",
    "is_stone_locale",
    "is_localic_group",
    "classify_locale",
    "locale_profile",
]
