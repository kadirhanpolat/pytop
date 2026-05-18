"""Spectral spaces, sober spaces, Stone duality, and frame-locale correspondence.

Key theorems implemented
------------------------
- A topological space X is sober if every irreducible closed subset F of X
  (F non-empty, and F = A u B with A, B closed implies F = A or F = B)
  has a unique generic point x (i.e., cl({x}) = F).
- Every Hausdorff (T2) space is sober; the converse fails — sober spaces need
  not be T1 (the Sierpinski space is sober but not T1).
- The Sierpinski space Sigma = {0,1} with open sets {empty, {1}, {0,1}} is the
  paradigmatic sober non-Hausdorff space: the whole space has generic point 1
  (cl({1}) = {0,1}), and {0} has generic point 0.
- Hochster's theorem: a topological space is homeomorphic to Spec(R) for some
  commutative ring R if and only if it is a spectral space.
- A spectral space is a compact sober T0 space whose compact open sets form a
  basis closed under finite intersection.
- Stone duality: the category of Boolean algebras is dually equivalent to the
  category of Stone spaces (compact totally disconnected Hausdorff spaces) via
  the functors Clopen(-) and Spec(-). Every Stone space is spectral.
- Priestley duality: the category of bounded distributive lattices is dually
  equivalent to the category of Priestley spaces (compact ordered spaces with a
  compatible topology where the order is a closed subset of X x X and every
  clopen upper set separates comparable pairs).
- Frame-locale duality: the category of frames (complete lattices satisfying
  a ^ (V b_i) = V(a ^ b_i)) is dually equivalent to the category of locales.
  A frame is spatial if every a < b is witnessed by a point (frame map to {0,1});
  spatial frames correspond bijectively to sober spaces via O(X) (open set frame).
- The Alexandrov topology on a poset (P, <=) (open sets = upper sets of P) is
  always T0. It is sober if and only if P is a dcpo (every directed subset has a
  supremum): the irreducible closed sets are exactly the lower sets of the form
  cl({x}) = {y : y <= x} (principal lower sets), which exist iff every directed
  set has a least upper bound in P.
- The Alexandrov topology on (N, <=) (natural numbers with usual ordering) is NOT
  sober: the lower set N itself is irreducible but has no generic point (N has
  no maximum element).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class SpectralSpaceProfile:
    """A curated spectral/sober space example."""

    key: str
    display_name: str
    space_type: str
    is_sober: bool
    is_spectral: bool
    is_stone_space: bool
    is_t0: bool
    is_t1: bool
    has_generic_point: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

SOBER_POSITIVE_TAGS: frozenset[str] = frozenset({
    "sober", "sober_space",
    "spectral_space", "coherent_space",
    "hausdorff", "compact_hausdorff", "t2",
    "stone_space", "boolean_space", "profinite",
    "spec_ring", "zariski_spectrum", "prime_spectrum",
    "sierpinski_space",
    "alexandrov_dcpo",
    "spatial_locale",
})

SPECTRAL_TAGS: frozenset[str] = frozenset({
    "spectral_space", "coherent_space",
    "spec_ring", "zariski_spectrum", "prime_spectrum",
    "stone_space", "boolean_space", "profinite",
    "alexandrov_finite_poset",
    "compact_sober_t0",
})

STONE_SPACE_TAGS: frozenset[str] = frozenset({
    "stone_space", "boolean_space", "profinite",
    "compact_totally_disconnected_hausdorff",
    "zero_dimensional_compact_hausdorff",
    "cantor_space", "cantor_set",
    "p_adic_integers",
    "profinite_group",
})

SPATIAL_FRAME_TAGS: frozenset[str] = frozenset({
    "spatial_frame", "spatial_locale",
    "frame_of_sober_space",
    "sober", "spectral_space",
    "stone_space",
    "open_set_frame",
})

GENERIC_POINT_TAGS: frozenset[str] = frozenset({
    "generic_point", "has_generic_point",
    "irreducible_space",
    "spec_integral_domain",
    "zariski_spectrum", "prime_spectrum",
    "sierpinski_space",
    "sober_irreducible",
})

NOT_SOBER_TAGS: frozenset[str] = frozenset({
    "not_sober", "t0_not_sober",
    "alexandrov_no_maximum",
    "poset_no_directed_suprema",
    "irreducible_no_generic_point",
})

NOT_T1_TAGS: frozenset[str] = frozenset({
    "t0_not_t1", "not_t1",
    "spec_ring", "zariski_spectrum",
    "sierpinski_space",
    "generic_point_not_closed",
    "non_t1_sober",
})

NOT_STONE_TAGS: frozenset[str] = frozenset({
    "not_hausdorff", "non_hausdorff",
    "not_totally_disconnected",
    "connected_nontrivial",
    "sierpinski_space",
    "spec_ring",
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

def get_named_spectral_space_profiles() -> tuple[SpectralSpaceProfile, ...]:
    """Return the registry of canonical spectral/sober space examples."""
    return (
        SpectralSpaceProfile(
            key="sierpinski_space",
            display_name="Sigma — Sierpinski space {0, 1}",
            space_type="sober_t0",
            is_sober=True,
            is_spectral=True,
            is_stone_space=False,
            is_t0=True,
            is_t1=False,
            has_generic_point=True,
            presentation_layer="main_text",
            focus=(
                "The Sierpinski space Sigma = {0, 1} has open sets {empty, {1}, {0,1}}. "
                "It is T0: the point 1 has a neighbourhood {1} not containing 0. "
                "It is NOT T1: the singleton {1} is open but {0} = Sigma \\ {1} is "
                "closed, while {0} is not open (no neighbourhood of 0 misses 1). "
                "Sigma is sober: the irreducible closed sets are {0} (generic point: 0) "
                "and {0,1} (generic point: 1, since cl({1}) = {0,1}). "
                "Sigma is spectral: it is compact (finite), sober, T0, and the "
                "compact open sets ({1} and {0,1}) form a basis closed under "
                "finite intersection ({1} ^ {0,1} = {1}). "
                "Sigma is the initial object in the category of sober spaces: "
                "every sober space X admits a unique continuous map X -> Sigma "
                "(sends the interior of a closed set to 0, its complement to 1). "
                "Sigma classifies open sets: open subsets of X correspond bijectively "
                "to continuous maps X -> Sigma."
            ),
            chapter_targets=("8", "26", "50"),
        ),
        SpectralSpaceProfile(
            key="spec_integral_domain",
            display_name="Spec(R) — prime spectrum of an integral domain",
            space_type="spectral",
            is_sober=True,
            is_spectral=True,
            is_stone_space=False,
            is_t0=True,
            is_t1=False,
            has_generic_point=True,
            presentation_layer="main_text",
            focus=(
                "The prime spectrum Spec(R) of a commutative ring R is the set of "
                "prime ideals of R, topologised by the Zariski topology: closed sets "
                "are V(I) = {p in Spec(R) : I subset p} for ideals I of R. "
                "When R is an integral domain, (0) is a prime ideal and "
                "cl({(0)}) = V((0)) = Spec(R), so (0) is the generic point of the "
                "whole space. The closed points are exactly the maximal ideals. "
                "Spec(R) is always T0 (different primes are topologically "
                "distinguishable via the basic open sets D(f) = {p : f not in p}). "
                "It is NOT T1 in general: non-maximal primes are not closed "
                "(their closure contains all primes that contain them). "
                "By Hochster's theorem, Spec(R) is spectral, and every spectral "
                "space is homeomorphic to Spec(R) for some R. "
                "The basic opens D(f) form a basis of compact opens closed under "
                "intersection: D(f) ^ D(g) = D(fg)."
            ),
            chapter_targets=("8", "26", "50"),
        ),
        SpectralSpaceProfile(
            key="stone_space",
            display_name="B — Stone / Boolean space (compact totally disconnected T2)",
            space_type="stone",
            is_sober=True,
            is_spectral=True,
            is_stone_space=True,
            is_t0=True,
            is_t1=True,
            has_generic_point=False,
            presentation_layer="main_text",
            focus=(
                "A Stone space (Boolean space) is a compact totally disconnected "
                "Hausdorff space. Stone's representation theorem: the category of "
                "Boolean algebras is dually equivalent to the category of Stone spaces, "
                "via the functors Clopen(X) (clopen sets of X, forming a Boolean algebra) "
                "and Spec(B) (Stone space of ultrafilters on a Boolean algebra B). "
                "Stone spaces are sober (every Hausdorff space is sober) and spectral "
                "(compact Hausdorff + totally disconnected => the clopen sets form a "
                "basis of compact opens closed under intersection). "
                "Stone spaces have no non-trivial generic points: every point is closed "
                "(T1 property), so all irreducible closed sets are singletons with "
                "their unique element as generic point. "
                "Canonical examples: the Cantor set 2^omega = {0,1}^N, p-adic integers Z_p, "
                "and profinite groups (inverse limits of finite discrete groups). "
                "The Cantor set is the unique (up to homeomorphism) compact metrizable "
                "Stone space without isolated points."
            ),
            chapter_targets=("8", "26", "50"),
        ),
        SpectralSpaceProfile(
            key="zariski_affine_line",
            display_name="Spec(k[x]) — Zariski topology on the affine line",
            space_type="spectral",
            is_sober=True,
            is_spectral=True,
            is_stone_space=False,
            is_t0=True,
            is_t1=False,
            has_generic_point=True,
            presentation_layer="main_text",
            focus=(
                "The affine line over an algebraically closed field k is "
                "Spec(k[x]) with the Zariski topology. The prime ideals of k[x] are: "
                "the zero ideal (0) (generic point) and the maximal ideals (x - a) "
                "for each a in k (closed points). "
                "Open sets: complements of finite subsets of k (plus the whole space). "
                "The Zariski topology on Spec(k[x]) is strictly coarser than the "
                "metric topology on k = A^1_k: every non-empty Zariski open set is dense. "
                "This is T0 (D(x-a) separates the closed point (x-a) from (0)) "
                "but NOT T1 (the generic point (0) is not closed: "
                "cl({(0)}) = V((0)) = all of Spec(k[x])). "
                "The whole space is irreducible (k[x] is an integral domain) with "
                "generic point (0). Hochster's theorem confirms this is spectral. "
                "The quasi-compact open sets are exactly the cofinite open sets "
                "together with the empty set. Spec(k[x]) is the fundamental example "
                "of a one-dimensional irreducible Noetherian spectral space."
            ),
            chapter_targets=("8", "26", "50"),
        ),
        SpectralSpaceProfile(
            key="alexandrov_dcpo",
            display_name="Alexandrov(P) — Alexandrov topology on a dcpo",
            space_type="sober_t0",
            is_sober=True,
            is_spectral=False,
            is_stone_space=False,
            is_t0=True,
            is_t1=False,
            has_generic_point=True,
            presentation_layer="selected_block",
            focus=(
                "The Alexandrov topology on a poset (P, <=) has as open sets all "
                "upper sets (upward-closed subsets) of P. Closed sets are lower sets "
                "(downward-closed). The specialisation order of the Alexandrov topology "
                "recovers the original partial order: x <= y iff x in cl({y}). "
                "The Alexandrov topology is always T0. It is sober if and only if P "
                "is a directed-complete partial order (dcpo): every directed subset "
                "D subset P (non-empty, every pair has an upper bound in D) has a "
                "least upper bound sup D in P. "
                "When P is a dcpo: the irreducible closed sets are exactly the closures "
                "cl({x}) = {y : y <= x} (principal lower sets), and every irreducible "
                "closed set has a unique generic point. "
                "Alexandrov topologies on finite posets are always sober (finite sets "
                "are trivially dcpos) and spectral (finite T0 spaces are spectral). "
                "Domains in denotational semantics (Scott domains, omega-algebraic cpos) "
                "are dcpos and hence carry a sober Alexandrov topology."
            ),
            chapter_targets=("8", "26"),
        ),
        SpectralSpaceProfile(
            key="alexandrov_no_max",
            display_name="Alexandrov(N, <=) — natural numbers, NOT sober",
            space_type="t0_not_sober",
            is_sober=False,
            is_spectral=False,
            is_stone_space=False,
            is_t0=True,
            is_t1=False,
            has_generic_point=False,
            presentation_layer="selected_block",
            focus=(
                "The Alexandrov topology on (N, <=) (natural numbers with the usual "
                "ordering) has open sets = upper sets = {k in N : k >= n} for n in N, "
                "plus the empty set. Closed sets = lower sets = {0,1,...,n} plus N. "
                "The space is T0: D(n) = {k : k >= n} distinguishes any two points. "
                "It is NOT T1: the singleton {0} is closed (it is the lower set {0}) "
                "but {1} is not open in the Alexandrov topology (it is not an upper set). "
                "The whole space N, as a lower set, is an irreducible closed set: "
                "if N = A u B with A, B proper lower sets, then A = {0,...,j} and "
                "B = {0,...,k} for some j, k in N, so A u B = {0,...,max(j,k)} != N. "
                "N has NO generic point: a generic point x would satisfy cl({x}) = N, "
                "but cl({x}) = {0,...,x} is always a finite set. "
                "Hence N does NOT satisfy the sobriety condition, and the Alexandrov "
                "topology on (N, <=) is a canonical example of a T0 non-sober space. "
                "This also shows: the Alexandrov topology is sober iff the poset is a dcpo, "
                "and (N, <=) fails this because the directed set N itself has no supremum."
            ),
            chapter_targets=("8", "26"),
        ),
    )


def spectral_space_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_spectral_space_profiles()
    ))


def spectral_space_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_spectral_space_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def spectral_space_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from space_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_spectral_space_profiles():
        index.setdefault(p.space_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_sober(space: Any) -> Result:
    """Check whether space is sober.

    A topological space X is sober if every irreducible closed subset F
    (F != empty, and F = A u B with A, B closed implies F = A or F = B)
    has a unique generic point x (a point x with cl({x}) = F). Key facts:
    - Every Hausdorff space is sober (T2 => sober).
    - Every spectral space is sober by definition.
    - The Sierpinski space is sober (not Hausdorff).
    - Spec(R) of any commutative ring is sober (Zariski topology).
    - The Alexandrov topology on a poset P is sober iff P is a dcpo.
    - The Alexandrov topology on (N, <=) is NOT sober: N is irreducible
      with no generic point.

    Decision layers
    ---------------
    1. Explicit sober tag -> true.
    2. Hausdorff / T2 space (T2 => sober) -> true.
    3. Stone / profinite / Boolean space (compact T.D. Hausdorff => sober) -> true.
    4. Spec(R) / spectral space / coherent space -> true.
    5. Alexandrov on (N,<=) or poset with no maximal/directed suprema -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"sober", "sober_space", "spatial_locale"}):
        witness = next(t for t in tags if t in {"sober", "sober_space", "spatial_locale"})
        return Result.true(
            mode="theorem",
            value="sober",
            justification=[
                f"Tag {witness!r}: the space is sober — every irreducible closed subset "
                "has a unique generic point.",
            ],
            metadata={**base, "criterion": "explicit_sober", "witness": witness},
        )

    if _matches_any(tags, {"hausdorff", "t2", "compact_hausdorff",
                            "metrizable", "compact_metrizable"}):
        witness = next(t for t in tags if t in {"hausdorff", "t2", "compact_hausdorff",
                                                    "metrizable", "compact_metrizable"})
        return Result.true(
            mode="theorem",
            value="sober",
            justification=[
                f"Tag {witness!r}: every Hausdorff (T2) space is sober. In a T2 space, "
                "the only irreducible closed sets are singletons {{x}}, each with "
                "unique generic point x.",
            ],
            metadata={**base, "criterion": "hausdorff_sober", "witness": witness},
        )

    if _matches_any(tags, STONE_SPACE_TAGS):
        witness = next(t for t in tags if t in STONE_SPACE_TAGS)
        return Result.true(
            mode="theorem",
            value="sober",
            justification=[
                f"Tag {witness!r}: Stone / profinite spaces are compact Hausdorff, "
                "hence sober. Their irreducible closed sets are exactly the singletons.",
            ],
            metadata={**base, "criterion": "stone_space_sober", "witness": witness},
        )

    if _matches_any(tags, {"spectral_space", "coherent_space", "spec_ring",
                            "zariski_spectrum", "prime_spectrum",
                            "sierpinski_space", "alexandrov_dcpo"}):
        witness = next(t for t in tags if t in {"spectral_space", "coherent_space",
                                                    "spec_ring", "zariski_spectrum",
                                                    "prime_spectrum", "sierpinski_space",
                                                    "alexandrov_dcpo"})
        return Result.true(
            mode="theorem",
            value="sober",
            justification=[
                f"Tag {witness!r}: spectral spaces and Spec(R) are sober by definition. "
                "The Sierpinski space is sober: {0} has generic point 0, and {0,1} "
                "has generic point 1 (cl({{1}}) = {{0,1}}). "
                "Alexandrov on a dcpo is sober: every directed set has a supremum, "
                "providing generic points for all irreducible lower sets.",
            ],
            metadata={**base, "criterion": "spectral_sober", "witness": witness},
        )

    if _matches_any(tags, NOT_SOBER_TAGS):
        blocking = next(t for t in tags if t in NOT_SOBER_TAGS)
        return Result.false(
            mode="theorem",
            value="sober",
            justification=[
                f"Tag {blocking!r}: the space is NOT sober. The Alexandrov topology on "
                "(N, <=) has N as an irreducible closed set with no generic point: "
                "for any x in N, cl({{x}}) = {{0,...,x}} ≠ N. "
                "Sobriety fails when an irreducible closed set lacks a generic point.",
            ],
            metadata={**base, "criterion": "not_sober", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="sober",
        justification=[
            "Insufficient tags to determine sobriety. "
            "Supply tags such as 'sober', 'hausdorff', 'spectral_space', 'spec_ring', "
            "'sierpinski_space', 'stone_space', 'alexandrov_dcpo', or 'not_sober'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_spectral(space: Any) -> Result:
    """Check whether space is a spectral space.

    A spectral space (or coherent space) is a topological space X that is:
    (i)  compact (every open cover has a finite subcover),
    (ii) sober (every irreducible closed set has a unique generic point),
    (iii) T0,
    (iv) the compact open sets form a basis,
    (v)  the compact open sets are closed under finite intersection.
    Key facts:
    - Hochster's theorem: X is spectral iff X is homeomorphic to Spec(R)
      for some commutative ring R.
    - Every Stone space is spectral (Boolean algebra => distributive lattice =>
      spectral via Stone/Priestley duality).
    - Finite T0 spaces are spectral (finite sets are trivially compact and sober).
    - The Sierpinski space is spectral.
    - The Alexandrov topology on (N, <=) is NOT spectral (not sober, not compact).

    Decision layers
    ---------------
    1. Explicit spectral / coherent / Spec(R) tag -> true.
    2. Stone / profinite space -> true (Boolean algebra => spectral).
    3. Alexandrov topology on a finite poset -> true.
    4. Sierpinski space -> true.
    5. Not sober or not compact -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, SPECTRAL_TAGS):
        witness = next(t for t in tags if t in SPECTRAL_TAGS)
        return Result.true(
            mode="theorem",
            value="spectral",
            justification=[
                f"Tag {witness!r}: the space is spectral — compact, sober, T0, "
                "with compact opens forming a basis closed under finite intersection. "
                "By Hochster's theorem, spectral spaces are exactly the prime spectra "
                "of commutative rings.",
            ],
            metadata={**base, "criterion": "spectral_tag", "witness": witness},
        )

    if _matches_any(tags, {"sierpinski_space"}):
        return Result.true(
            mode="theorem",
            value="spectral",
            justification=[
                "Tag 'sierpinski_space': the Sierpinski space is spectral — it is "
                "finite (hence compact), sober, T0. Its compact open sets {1} and "
                "{0,1} form a basis closed under intersection.",
            ],
            metadata={**base, "criterion": "sierpinski_spectral"},
        )

    if _matches_any(tags, NOT_SOBER_TAGS):
        blocking = next(t for t in tags if t in NOT_SOBER_TAGS)
        return Result.false(
            mode="theorem",
            value="spectral",
            justification=[
                f"Tag {blocking!r}: spectral spaces must be sober. A non-sober space "
                "cannot be spectral, regardless of other properties.",
            ],
            metadata={**base, "criterion": "not_sober_not_spectral", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="spectral",
        justification=[
            "Insufficient tags to determine spectral property. "
            "Supply tags such as 'spectral_space', 'spec_ring', 'stone_space', "
            "'sierpinski_space', 'alexandrov_finite_poset', or 'not_sober'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_stone_space(space: Any) -> Result:
    """Check whether space is a Stone space (compact totally disconnected Hausdorff).

    A Stone space is a compact Hausdorff space that is totally disconnected
    (every connected component is a singleton). Key facts:
    - Stone's representation theorem: the category of Boolean algebras is dually
      equivalent to the category of Stone spaces via Clopen(-) and Spec(-).
    - Stone spaces are also called Boolean spaces or profinite spaces.
    - Every Stone space is zero-dimensional (clopen sets form a basis).
    - Stone spaces are spectral: the clopen sets form a basis of compact opens
      closed under finite intersection and complement.
    - The Cantor set 2^N is the unique compact metrizable Stone space without
      isolated points.
    - Profinite groups (inverse limits of finite discrete groups) are Stone spaces.
    - The Sierpinski space is NOT a Stone space (not T1, not Hausdorff).
    - Spec(R) for a non-field ring is NOT a Stone space (not Hausdorff).

    Decision layers
    ---------------
    1. Explicit Stone / Boolean / profinite space tag -> true.
    2. Compact totally disconnected Hausdorff tag -> true.
    3. Cantor set / p-adic integers -> true.
    4. Non-Hausdorff (Sierpinski, Spec(R)) -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, STONE_SPACE_TAGS):
        witness = next(t for t in tags if t in STONE_SPACE_TAGS)
        return Result.true(
            mode="theorem",
            value="stone_space",
            justification=[
                f"Tag {witness!r}: the space is a Stone space (compact totally "
                "disconnected Hausdorff). By Stone's representation theorem, it "
                "corresponds to a Boolean algebra via the Clopen(-) functor.",
            ],
            metadata={**base, "criterion": "stone_tag", "witness": witness},
        )

    if _matches_any(tags, NOT_STONE_TAGS):
        blocking = next(t for t in tags if t in NOT_STONE_TAGS)
        return Result.false(
            mode="theorem",
            value="stone_space",
            justification=[
                f"Tag {blocking!r}: the space is NOT a Stone space. "
                "Stone spaces must be Hausdorff — the Sierpinski space and Spec(R) "
                "(for non-field R) are not T1, hence not Hausdorff. "
                "Connected non-trivial spaces are not totally disconnected.",
            ],
            metadata={**base, "criterion": "not_stone", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="stone_space",
        justification=[
            "Insufficient tags to determine Stone space property. "
            "Supply tags such as 'stone_space', 'profinite', 'boolean_space', "
            "'cantor_space', 'compact_totally_disconnected_hausdorff', "
            "'sierpinski_space', or 'not_hausdorff'.",
        ],
        metadata={**base, "criterion": None},
    )


def frame_is_spatial(space: Any) -> Result:
    """Check whether the frame O(X) of open sets of space is spatial.

    A frame is a complete lattice L satisfying the infinite distributive law:
    a ^ (V S) = V{a ^ s : s in S} for all a in L and S subset L.
    A frame is spatial if for any a < b in L there exists a frame homomorphism
    p: L -> {0,1} (a 'point') with p(b) = 1 and p(a) = 0 — i.e., the points
    separate elements. Key facts:
    - The open set lattice O(X) of any topological space X is a frame.
    - O(X) is spatial if and only if X is sober.
    - Spatial frames are in bijective correspondence with sober spaces:
      the functor O: SoberSpaces -> Framesop and pt: Framesop -> SoberSpaces
      establish an equivalence of categories.
    - Non-spatial frames exist: the free frame on countably many generators
      contains non-spatial elements.
    - Every Stone space has a spatial frame (Boolean algebra => spatial frame).

    Decision layers
    ---------------
    1. Explicit spatial frame tag -> true.
    2. Sober space (O(X) spatial iff X sober) -> true.
    3. Stone / Boolean space -> true.
    4. Non-sober space (O(X) not spatial) -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, SPATIAL_FRAME_TAGS):
        witness = next(t for t in tags if t in SPATIAL_FRAME_TAGS)
        return Result.true(
            mode="theorem",
            value="spatial_frame",
            justification=[
                f"Tag {witness!r}: the frame O(X) is spatial — there are enough points "
                "(frame maps to {{0,1}}) to separate the open sets. "
                "Spatial frames correspond bijectively to sober spaces via the "
                "adjunction between the functors O and pt.",
            ],
            metadata={**base, "criterion": "spatial_frame_tag", "witness": witness},
        )

    if _matches_any(tags, SOBER_POSITIVE_TAGS):
        witness = next(t for t in tags if t in SOBER_POSITIVE_TAGS)
        return Result.true(
            mode="theorem",
            value="spatial_frame",
            justification=[
                f"Tag {witness!r}: the space is sober, so its frame O(X) of open sets "
                "is spatial. The frame-locale duality: O(X) is spatial iff X is sober. "
                "Sober spaces and spatial frames are equivalent via O and pt.",
            ],
            metadata={**base, "criterion": "sober_frame_spatial", "witness": witness},
        )

    if _matches_any(tags, NOT_SOBER_TAGS):
        blocking = next(t for t in tags if t in NOT_SOBER_TAGS)
        return Result.false(
            mode="theorem",
            value="spatial_frame",
            justification=[
                f"Tag {blocking!r}: the space is not sober, so its frame O(X) is "
                "NOT spatial. There exist open sets in O(X) that are not separated "
                "by the available frame maps to {{0,1}} (the 'points' of the locale).",
            ],
            metadata={**base, "criterion": "not_sober_not_spatial"},
        )

    return Result.unknown(
        mode="symbolic",
        value="spatial_frame",
        justification=[
            "Insufficient tags to determine whether the frame is spatial. "
            "Supply tags such as 'sober', 'spatial_frame', 'stone_space', "
            "'spectral_space', 'not_sober', or 'hausdorff'.",
        ],
        metadata={**base, "criterion": None},
    )


def stone_duality_applies(space: Any) -> Result:
    """Check whether Stone duality provides a Boolean algebra correspondence.

    Stone's representation theorem (1936): the category of Boolean algebras is
    dually equivalent to the category of Stone spaces via:
    - Clopen: Stone spaces -> Boolean algebras   (X |-> Clopen(X))
    - Spec:   Boolean algebras -> Stone spaces    (B |-> ultrafilters on B)
    Key facts:
    - Every Boolean algebra B corresponds to a unique Stone space Spec(B).
    - Every Stone space X corresponds to a unique Boolean algebra Clopen(X).
    - Generalisation: Priestley duality extends this to bounded distributive
      lattices and Priestley spaces (compact ordered spaces).
    - Further generalisation: the equivalence between sober spaces and spatial
      frames is the locale-theoretic extension.
    - The Stone-Cech compactification beta(X) is a Stone space containing X as
      a dense subspace (for discrete X, C(beta(X)) = l^inf(X)).
    - Stone duality does NOT apply to Sierpinski space or Spec(R) for non-field R
      (these are T0 non-Hausdorff; the Boolean algebra structure is absent).

    Decision layers
    ---------------
    1. Stone / Boolean / profinite space -> true.
    2. Compact totally disconnected Hausdorff -> true.
    3. Boolean algebra explicitly tagged -> true.
    4. Non-Hausdorff / non-T1 space (Sierpinski, Spec(R)) -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, STONE_SPACE_TAGS | {"boolean_algebra"}):
        witness = next(t for t in tags if t in STONE_SPACE_TAGS | {"boolean_algebra"})
        return Result.true(
            mode="theorem",
            value="stone_duality",
            justification=[
                f"Tag {witness!r}: Stone duality applies. The space is a Stone space, "
                "corresponding to a Boolean algebra B = Clopen(X) via Stone's "
                "representation theorem. The functors Clopen(-) and Spec(-) give "
                "a dual equivalence of categories.",
            ],
            metadata={**base, "criterion": "stone_duality_tag", "witness": witness},
        )

    if _matches_any(tags, NOT_STONE_TAGS | NOT_T1_TAGS):
        blocking = next(t for t in tags if t in (NOT_STONE_TAGS | NOT_T1_TAGS))
        return Result.false(
            mode="theorem",
            value="stone_duality",
            justification=[
                f"Tag {blocking!r}: Stone duality does NOT apply. The space is not "
                "Hausdorff or not totally disconnected, so it is not a Stone space. "
                "Stone duality requires compact totally disconnected Hausdorff structure. "
                "Non-T1 spaces (Sierpinski, Zariski spectra) do not have a Boolean "
                "algebra of clopen sets separating points.",
            ],
            metadata={**base, "criterion": "not_stone_duality", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="stone_duality",
        justification=[
            "Insufficient tags to determine Stone duality applicability. "
            "Supply tags such as 'stone_space', 'profinite', 'boolean_space', "
            "'cantor_space', 'sierpinski_space', 'not_hausdorff', or 'spec_ring'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_spectral_space(space: Any) -> dict[str, Any]:
    """Classify the spectral/sober properties of space.

    Keys
    ----
    space_class : str
        One of ``"stone"``, ``"spectral"``, ``"sober"``,
        ``"t0_not_sober"``, ``"unknown"``.
    is_sober : Result
    is_spectral : Result
    is_stone_space : Result
    frame_is_spatial : Result
    stone_duality : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    sober_r = is_sober(space)
    spectral_r = is_spectral(space)
    stone_r = is_stone_space(space)
    frame_r = frame_is_spatial(space)
    duality_r = stone_duality_applies(space)

    if stone_r.is_true:
        space_class = "stone"
    elif spectral_r.is_true:
        space_class = "spectral"
    elif sober_r.is_true:
        space_class = "sober"
    elif sober_r.is_false:
        space_class = "t0_not_sober"
    else:
        space_class = "unknown"

    key_properties: list[str] = []
    if sober_r.is_true:
        key_properties.append("sober")
    if sober_r.is_false:
        key_properties.append("not_sober")
    if spectral_r.is_true:
        key_properties.append("spectral")
    if stone_r.is_true:
        key_properties.append("stone_space")
    if frame_r.is_true:
        key_properties.append("spatial_frame")
    if duality_r.is_true:
        key_properties.append("stone_duality")
    if duality_r.is_false:
        key_properties.append("stone_duality_fails")
    if _matches_any(tags, NOT_T1_TAGS):
        key_properties.append("t0_not_t1")

    return {
        "space_class": space_class,
        "is_sober": sober_r,
        "is_spectral": spectral_r,
        "is_stone_space": stone_r,
        "frame_is_spatial": frame_r,
        "stone_duality": duality_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def spectral_space_profile(space: Any) -> dict[str, Any]:
    """Full spectral space profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_spectral_space`.
    named_profiles : tuple[SpectralSpaceProfile, ...]
        Registry of canonical spectral/sober space examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_spectral_space(space),
        "named_profiles": get_named_spectral_space_profiles(),
        "layer_summary": spectral_space_layer_summary(),
    }


__all__ = [
    "SpectralSpaceProfile",
    "SOBER_POSITIVE_TAGS",
    "SPECTRAL_TAGS",
    "STONE_SPACE_TAGS",
    "SPATIAL_FRAME_TAGS",
    "GENERIC_POINT_TAGS",
    "NOT_SOBER_TAGS",
    "NOT_T1_TAGS",
    "NOT_STONE_TAGS",
    "get_named_spectral_space_profiles",
    "spectral_space_layer_summary",
    "spectral_space_chapter_index",
    "spectral_space_type_index",
    "is_sober",
    "is_spectral",
    "is_stone_space",
    "frame_is_spatial",
    "stone_duality_applies",
    "classify_spectral_space",
    "spectral_space_profile",
]
