"""Zero-dimensionality: clopen bases, Cantor universality, and profinite spaces.

Key theorems implemented
------------------------
- A space X is zero-dimensional (ind X = 0) iff it has a base of clopen sets.
- Brouwer's theorem: The Cantor space {0,1}^omega is the unique (up to homeomorphism)
  compact metrizable zero-dimensional perfect space with no isolated points.
- Universality: Every compact metrizable zero-dimensional space embeds in the Cantor set.
- Stone duality: The category of zero-dimensional compact Hausdorff spaces (Stone spaces)
  is dually equivalent to the category of Boolean algebras.
- Profinite characterisation: A space is profinite iff it is compact, Hausdorff, and
  zero-dimensional (equivalently, an inverse limit of finite discrete spaces).
- Dimension monotonicity: Every subspace of a zero-dimensional metrizable space is
  zero-dimensional.
- The rationals Q are zero-dimensional, not locally compact, and not complete.
- The Baire space omega^omega (irrationals) is zero-dimensional and Polish.
- A scattered space is one in which every non-empty subspace has an isolated point;
  all scattered metrizable spaces are zero-dimensional.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class ZeroDimensionalProfile:
    """A curated zero-dimensional space example."""

    key: str
    display_name: str
    space_type: str
    is_compact: bool
    is_metrizable: bool
    is_profinite: bool
    is_scattered: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

ZERO_DIMENSIONAL_TAGS: set[str] = {
    "zero_dimensional", "zero_dim", "ind_zero",
    "clopen_base", "clopen_basis",
    "cantor_set", "cantor_space",
    "profinite", "profinite_space",
    "p_adic", "p_adic_integers", "p_adic_numbers",
    "baire_space", "irrationals",
    "scattered", "discrete",
    "rationals", "rational_numbers",
    "stone_space", "boolean_space",
}
TOTALLY_DISCONNECTED_TAGS: set[str] = {
    "totally_disconnected", "zero_dimensional", "zero_dim",
    "cantor_set", "cantor_space",
    "profinite", "discrete",
    "p_adic", "p_adic_integers",
    "scattered", "stone_space",
    "rationals", "baire_space",
}
PROFINITE_TAGS: set[str] = {
    "profinite", "profinite_space",
    "p_adic_integers",
    "cantor_space", "cantor_set",
    "stone_space", "boolean_space",
    "compact_zero_dimensional", "compact_totally_disconnected",
}
COMPACT_ZD_TAGS: set[str] = {
    "cantor_set", "cantor_space",
    "profinite", "profinite_space",
    "p_adic_integers",
    "compact_zero_dimensional", "compact_totally_disconnected",
    "stone_space", "boolean_space",
    "finite_space", "finite_discrete",
}
SCATTERED_TAGS: set[str] = {
    "scattered", "discrete",
    "finite_space", "finite_discrete",
    "ordinal_space", "successor_ordinal",
    "countable_ordinal",
}
NOT_ZERO_DIMENSIONAL_TAGS: set[str] = {
    "connected", "path_connected", "locally_path_connected",
    "continuum", "interval", "disk",
    "closed_interval", "real_line", "reals",
    "manifold", "topological_manifold",
    "locally_connected_not_zd",
    "positive_dimension",
}
COMPACT_HAUSDORFF_TAGS: set[str] = {
    "compact_hausdorff", "compact_t2",
    "compact_metrizable", "compact_metric",
    "profinite", "stone_space",
    "cantor_set", "cantor_space",
}
STONE_DUALITY_TAGS: set[str] = {
    "compact_hausdorff", "compact_t2",
    "profinite", "stone_space", "boolean_space",
    "compact_metrizable",
    "cantor_set", "cantor_space",
    "p_adic_integers",
}
EMBEDS_IN_CANTOR_TAGS: set[str] = {
    "compact_metrizable", "compact_metric",
    "cantor_set", "cantor_space",
    "profinite",
    "p_adic_integers",
    "compact_zero_dimensional", "compact_totally_disconnected",
    "finite_space", "finite_discrete",
}


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

def get_named_zero_dimensional_profiles() -> tuple[ZeroDimensionalProfile, ...]:
    """Return the registry of canonical zero-dimensional space examples."""
    return (
        ZeroDimensionalProfile(
            key="cantor_space",
            display_name="{0,1}^omega — the Cantor space",
            space_type="compact_metrizable_perfect",
            is_compact=True,
            is_metrizable=True,
            is_profinite=True,
            is_scattered=False,
            presentation_layer="main_text",
            focus=(
                "The Cantor space {0,1}^omega (product of countably many copies of "
                "{0,1} with the discrete topology) is the universal compact metrizable "
                "zero-dimensional space. By Brouwer's theorem, it is (up to homeomorphism) "
                "the unique compact metrizable perfect space that is zero-dimensional. "
                "Every compact metrizable zero-dimensional space is a continuous image "
                "of the Cantor space, and every compact metrizable zero-dimensional "
                "space embeds in it. As a profinite space it is the inverse limit of "
                "finite discrete spaces."
            ),
            chapter_targets=("4", "6", "29"),
        ),
        ZeroDimensionalProfile(
            key="cantor_set",
            display_name="C ⊂ [0,1] — the middle-thirds Cantor set",
            space_type="compact_metrizable_perfect",
            is_compact=True,
            is_metrizable=True,
            is_profinite=True,
            is_scattered=False,
            presentation_layer="main_text",
            focus=(
                "The middle-thirds Cantor set C = [0,1] \\ bigcup_{n=0}^inf (open middle thirds) "
                "is a compact, metrizable, perfect, nowhere dense subset of [0,1]. "
                "It is homeomorphic to the Cantor space {0,1}^omega and hence is the "
                "universal compact metrizable zero-dimensional space. C has Lebesgue "
                "measure zero yet has the cardinality of the continuum. Its clopen base "
                "consists of intersections with dyadic intervals."
            ),
            chapter_targets=("4", "6", "29"),
        ),
        ZeroDimensionalProfile(
            key="p_adic_integers",
            display_name="Zp — the p-adic integers",
            space_type="profinite_ring",
            is_compact=True,
            is_metrizable=True,
            is_profinite=True,
            is_scattered=False,
            presentation_layer="main_text",
            focus=(
                "The ring of p-adic integers Zp = lim_<-- Z/p^n Z is a profinite space: "
                "compact, Hausdorff, and zero-dimensional. It is homeomorphic to the "
                "Cantor space (as a topological space). The p-adic metric d(x,y) = p^{-v_p(x-y)} "
                "makes Zp a compact, perfect, metrizable ultrametric space. Clopen balls "
                "B(x, p^{-n}) = x + p^n Zp form the natural clopen base. "
                "Zp is the completion of Z with respect to the p-adic absolute value."
            ),
            chapter_targets=("4", "29", "52"),
        ),
        ZeroDimensionalProfile(
            key="rational_numbers",
            display_name="Q — the rational numbers",
            space_type="countable_metrizable",
            is_compact=False,
            is_metrizable=True,
            is_profinite=False,
            is_scattered=False,
            presentation_layer="main_text",
            focus=(
                "The rationals Q with the subspace topology from R are zero-dimensional: "
                "the intervals (a, b) ∩ Q with irrational endpoints a, b form a clopen "
                "base (they are clopen in Q). Q is countable, metrizable, and not locally "
                "compact (no neighborhood has compact closure). By Brouwer's theorem for "
                "countable spaces, Q is (up to homeomorphism) the unique countable metrizable "
                "space with no isolated points. Q is not completely metrizable (not Baire) "
                "but every Borel subset of R ∩ Q is a Borel subset of Q."
            ),
            chapter_targets=("4", "6", "29"),
        ),
        ZeroDimensionalProfile(
            key="baire_space",
            display_name="omega^omega — the Baire space (irrationals)",
            space_type="polish_not_compact",
            is_compact=False,
            is_metrizable=True,
            is_profinite=False,
            is_scattered=False,
            presentation_layer="selected_block",
            focus=(
                "The Baire space N = omega^omega (functions N -> N with the product of "
                "discrete topologies) is homeomorphic to the irrationals R \\ Q. "
                "It is Polish (completely metrizable and separable), zero-dimensional "
                "(cylinder sets [s] for finite sequences s form a clopen base), "
                "and not compact. The Baire space is the universal Polish zero-dimensional "
                "space: every Polish space is a continuous image of N. Its name comes from "
                "the Baire category theorem, which it satisfies."
            ),
            chapter_targets=("4", "27", "29"),
        ),
        ZeroDimensionalProfile(
            key="discrete_countable",
            display_name="N — countable discrete space",
            space_type="scattered_discrete",
            is_compact=False,
            is_metrizable=True,
            is_profinite=False,
            is_scattered=True,
            presentation_layer="main_text",
            focus=(
                "The natural numbers N with the discrete topology form the simplest "
                "infinite zero-dimensional space. Every subset is clopen, so the clopen "
                "base is the full topology (the discrete topology). N is scattered (every "
                "non-empty subspace has an isolated point) and metrizable. It is not compact "
                "(no finite subcover of {n} for n in N) but is locally compact (each {n} "
                "is open and compact). The one-point compactification N ∪ {∞} is the "
                "ordinal space omega + 1."
            ),
            chapter_targets=("4", "6"),
        ),
        ZeroDimensionalProfile(
            key="stone_cech_remainder",
            display_name="betaN \\ N — the Stone-Cech remainder",
            space_type="compact_not_metrizable",
            is_compact=True,
            is_metrizable=False,
            is_profinite=False,
            is_scattered=False,
            presentation_layer="advanced_note",
            focus=(
                "The Stone-Cech remainder betaN \\ N is a compact Hausdorff "
                "zero-dimensional space that is not metrizable (it has cardinality 2^c). "
                "It is not scattered, and its topology is extremely complex: "
                "no two points can be separated by a G_delta set. "
                "Under the Continuum Hypothesis, betaN \\ N is homeomorphic to "
                "any other separable compact Hausdorff space of weight 2^omega with "
                "no isolated points. It is a Stone space corresponding to the Boolean "
                "algebra P(N)/Fin (power set of N modulo finite sets)."
            ),
            chapter_targets=("4", "9", "29"),
        ),
    )


def zero_dimensional_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_zero_dimensional_profiles()))


def zero_dimensional_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_zero_dimensional_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def zero_dimensional_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from space_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_zero_dimensional_profiles():
        index.setdefault(p.space_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def has_clopen_base(space: Any) -> Result:
    """Check whether space has a base of clopen (simultaneously open and closed) sets.

    A space X is zero-dimensional (ind X = 0) iff it has a base of clopen sets.
    Key facts:
    - Any discrete space has a clopen base (every set is clopen).
    - The Cantor space, Cantor set, p-adic integers all have clopen bases.
    - Totally disconnected compact Hausdorff spaces (profinite spaces) always have
      clopen bases (this is the content of the Stone representation theorem).
    - The rationals Q have a clopen base (intervals with irrational endpoints).
    - Connected spaces with more than one point do NOT have a clopen base.

    Decision layers
    ---------------
    1. Explicit zero-dimensional / clopen_base tags -> true.
    2. Cantor set/space, discrete, p-adic (canonical examples) -> true.
    3. Profinite or Stone space -> true.
    4. Totally disconnected + compact Hausdorff -> true.
    5. Totally disconnected + metrizable -> true.
    6. Connected (more than one point) -> false.
    7. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"zero_dimensional", "zero_dim", "ind_zero",
                            "clopen_base", "clopen_basis"}):
        witness = next(t for t in tags if t in {"zero_dimensional", "zero_dim",
                                                   "ind_zero", "clopen_base", "clopen_basis"})
        return Result.true(
            mode="theorem",
            value="has_clopen_base",
            justification=[
                f"Tag {witness!r}: space is explicitly zero-dimensional. "
                "Zero-dimensionality (ind X = 0) is equivalent to having a base of "
                "clopen sets.",
            ],
            metadata={**base, "criterion": "explicit_zero_dim", "witness": witness},
        )

    if _matches_any(tags, {"cantor_set", "cantor_space", "p_adic", "p_adic_integers",
                            "discrete", "rationals", "rational_numbers",
                            "baire_space", "irrationals", "scattered"}):
        witness = next(t for t in tags if t in {
            "cantor_set", "cantor_space", "p_adic", "p_adic_integers",
            "discrete", "rationals", "rational_numbers",
            "baire_space", "irrationals", "scattered",
        })
        return Result.true(
            mode="theorem",
            value="has_clopen_base",
            justification=[
                f"Tag {witness!r}: this is a canonical zero-dimensional space. "
                "Its natural topology has a base of clopen sets.",
            ],
            metadata={**base, "criterion": "canonical_zero_dim", "witness": witness},
        )

    if _matches_any(tags, PROFINITE_TAGS):
        witness = next(t for t in tags if t in PROFINITE_TAGS)
        return Result.true(
            mode="theorem",
            value="has_clopen_base",
            justification=[
                f"Tag {witness!r}: profinite and Stone spaces are compact Hausdorff "
                "zero-dimensional spaces. The Stone representation theorem guarantees "
                "a clopen base corresponding to the underlying Boolean algebra.",
            ],
            metadata={**base, "criterion": "profinite", "witness": witness},
        )

    if (_matches_any(tags, TOTALLY_DISCONNECTED_TAGS) and
            _matches_any(tags, COMPACT_HAUSDORFF_TAGS)):
        witness_td = next(t for t in tags if t in TOTALLY_DISCONNECTED_TAGS)
        return Result.true(
            mode="theorem",
            value="has_clopen_base",
            justification=[
                f"Tag {witness_td!r}: a compact Hausdorff totally disconnected space "
                "is zero-dimensional — it has a base of clopen sets. "
                "(Equivalently: compact Hausdorff zero-dimensional = profinite.)",
            ],
            metadata={**base, "criterion": "compact_hausdorff_totally_disconnected",
                       "witness": witness_td},
        )

    if (_matches_any(tags, TOTALLY_DISCONNECTED_TAGS) and
            _matches_any(tags, {"metric", "metrizable"})):
        witness_td = next(t for t in tags if t in TOTALLY_DISCONNECTED_TAGS)
        return Result.true(
            mode="theorem",
            value="has_clopen_base",
            justification=[
                f"Tag {witness_td!r}: a metrizable totally disconnected space has "
                "a base of clopen sets (ind X = 0). "
                "In metrizable spaces, totally disconnected ↔ zero-dimensional.",
            ],
            metadata={**base, "criterion": "metrizable_totally_disconnected",
                       "witness": witness_td},
        )

    if _matches_any(tags, NOT_ZERO_DIMENSIONAL_TAGS):
        blocking = next(t for t in tags if t in NOT_ZERO_DIMENSIONAL_TAGS)
        return Result.false(
            mode="theorem",
            value="has_clopen_base",
            justification=[
                f"Tag {blocking!r}: connected spaces with more than one point do not "
                "have a clopen base. A clopen base would allow separating points, "
                "contradicting connectedness.",
            ],
            metadata={**base, "criterion": "connected_no_clopen_base"},
        )

    return Result.unknown(
        mode="symbolic",
        value="has_clopen_base",
        justification=[
            "Insufficient tags to determine existence of a clopen base. "
            "Supply tags such as 'zero_dimensional', 'totally_disconnected', "
            "'cantor_set', 'discrete', 'profinite', or 'connected'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_zero_dimensional(space: Any) -> Result:
    """Check whether space is zero-dimensional (ind X = 0).

    A space X is zero-dimensional iff ind X = 0, i.e., every point has a
    neighbourhood base of clopen sets. Key facts:
    - In metrizable spaces, zero-dimensional = totally disconnected.
    - Every subspace of a zero-dimensional metrizable space is zero-dimensional
      (dimension monotonicity).
    - The Cantor space is the universal compact metrizable zero-dimensional space.
    - Profinite spaces are precisely the compact Hausdorff zero-dimensional spaces.

    Decision layers
    ---------------
    1. Explicit zero-dimensional tag -> true.
    2. Canonical zero-dimensional spaces (Cantor, Q, irrationals, discrete) -> true.
    3. Profinite / Stone space -> true.
    4. Compact Hausdorff + totally disconnected -> true.
    5. Metrizable + totally disconnected -> true.
    6. Connected space (nontrivial) -> false.
    7. Positive-dimensional -> false.
    8. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, ZERO_DIMENSIONAL_TAGS):
        witness = next(t for t in tags if t in ZERO_DIMENSIONAL_TAGS)
        return Result.true(
            mode="theorem",
            value="zero_dimensional",
            justification=[
                f"Tag {witness!r}: space is zero-dimensional (ind X = 0). "
                "Every point has a neighbourhood base of clopen sets.",
            ],
            metadata={**base, "criterion": "zero_dim_tag", "witness": witness},
        )

    if _matches_any(tags, PROFINITE_TAGS):
        witness = next(t for t in tags if t in PROFINITE_TAGS)
        return Result.true(
            mode="theorem",
            value="zero_dimensional",
            justification=[
                f"Tag {witness!r}: profinite spaces are compact Hausdorff and "
                "zero-dimensional by definition. ind X = 0.",
            ],
            metadata={**base, "criterion": "profinite_implies_zd", "witness": witness},
        )

    if (_matches_any(tags, TOTALLY_DISCONNECTED_TAGS) and
            _matches_any(tags, COMPACT_HAUSDORFF_TAGS | {"metric", "metrizable"})):
        witness_td = next(t for t in tags if t in TOTALLY_DISCONNECTED_TAGS)
        return Result.true(
            mode="theorem",
            value="zero_dimensional",
            justification=[
                f"Tag {witness_td!r}: totally disconnected + compact Hausdorff (or metrizable) "
                "implies zero-dimensional. In these settings, connected components are "
                "points, and clopen neighbourhoods witness ind X = 0.",
            ],
            metadata={**base, "criterion": "totally_disconnected_regular", "witness": witness_td},
        )

    if _matches_any(tags, NOT_ZERO_DIMENSIONAL_TAGS):
        blocking = next(t for t in tags if t in NOT_ZERO_DIMENSIONAL_TAGS)
        return Result.false(
            mode="theorem",
            value="zero_dimensional",
            justification=[
                f"Tag {blocking!r}: connected (nontrivial) spaces or positive-dimensional "
                "spaces are not zero-dimensional. ind X = 0 requires a clopen neighbourhood "
                "base, which fails when connected components are non-trivial.",
            ],
            metadata={**base, "criterion": "connected_or_positive_dim"},
        )

    if _matches_any(tags, {"positive_dimension", "dim_positive", "ind_positive"}):
        blocking = next(t for t in tags if t in {"positive_dimension", "dim_positive",
                                                    "ind_positive"})
        return Result.false(
            mode="theorem",
            value="zero_dimensional",
            justification=[
                f"Tag {blocking!r}: positive inductive dimension implies the space is "
                "not zero-dimensional.",
            ],
            metadata={**base, "criterion": "positive_dimension"},
        )

    return Result.unknown(
        mode="symbolic",
        value="zero_dimensional",
        justification=[
            "Insufficient tags to determine zero-dimensionality. "
            "Supply tags such as 'zero_dimensional', 'totally_disconnected', "
            "'cantor_set', 'profinite', 'discrete', or 'connected'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_profinite(space: Any) -> Result:
    """Check whether space is profinite (compact + Hausdorff + zero-dimensional).

    A topological space X is profinite iff it is homeomorphic to an inverse limit
    of finite discrete spaces. Equivalently:
    - X is compact, Hausdorff, and zero-dimensional.
    - X is compact, Hausdorff, and totally disconnected.
    Key facts:
    - The p-adic integers Zp are profinite.
    - The Cantor space {0,1}^omega is profinite.
    - Every profinite space is a Stone space (spectrum of a Boolean algebra).
    - Finite discrete spaces are trivially profinite.

    Decision layers
    ---------------
    1. Explicit profinite tag -> true.
    2. Compact + Hausdorff + zero_dimensional tags -> true.
    3. Compact + Hausdorff + totally disconnected -> true.
    4. Non-compact -> false.
    5. Non-Hausdorff -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"profinite", "profinite_space"}):
        witness = next(t for t in tags if t in {"profinite", "profinite_space"})
        return Result.true(
            mode="theorem",
            value="profinite",
            justification=[
                f"Tag {witness!r}: space is explicitly profinite. "
                "Profinite spaces are compact, Hausdorff, and zero-dimensional — "
                "equivalently, inverse limits of finite discrete spaces.",
            ],
            metadata={**base, "criterion": "explicit_profinite", "witness": witness},
        )

    if _matches_any(tags, COMPACT_ZD_TAGS) and _matches_any(
        tags, {"hausdorff", "t2", "compact_hausdorff", "compact_t2",
               "compact_metrizable", "compact_metric"}
    ):
        witness = next(t for t in tags if t in COMPACT_ZD_TAGS)
        return Result.true(
            mode="theorem",
            value="profinite",
            justification=[
                f"Tag {witness!r}: compact Hausdorff zero-dimensional spaces are profinite. "
                "By the Stone representation theorem, every such space is the spectrum "
                "of some Boolean algebra and arises as an inverse limit of finite spaces.",
            ],
            metadata={**base, "criterion": "compact_hausdorff_zd", "witness": witness},
        )

    if (_matches_any(tags, TOTALLY_DISCONNECTED_TAGS) and
            _matches_any(tags, {"compact", "compact_hausdorff", "compact_t2",
                                 "compact_metrizable"})):
        witness_td = next(t for t in tags if t in TOTALLY_DISCONNECTED_TAGS)
        return Result.true(
            mode="theorem",
            value="profinite",
            justification=[
                f"Tag {witness_td!r}: compact Hausdorff + totally disconnected implies "
                "profinite. Totally disconnected compact Hausdorff spaces have a "
                "clopen base and are inverse limits of finite discrete spaces.",
            ],
            metadata={**base, "criterion": "compact_totally_disconnected",
                       "witness": witness_td},
        )

    if _matches_any(tags, {"non_compact", "not_compact", "real_line", "reals",
                            "rationals", "rational_numbers", "baire_space",
                            "irrationals", "polish_not_compact"}):
        blocking = next(t for t in tags if t in {"non_compact", "not_compact",
                                                    "real_line", "reals",
                                                    "rationals", "rational_numbers",
                                                    "baire_space", "irrationals",
                                                    "polish_not_compact"})
        return Result.false(
            mode="theorem",
            value="profinite",
            justification=[
                f"Tag {blocking!r}: profinite spaces must be compact. "
                "This space is not compact, so it cannot be profinite.",
            ],
            metadata={**base, "criterion": "not_compact"},
        )

    if _matches_any(tags, {"t0_not_t1", "not_hausdorff", "non_hausdorff"}):
        blocking = next(t for t in tags if t in {"t0_not_t1", "not_hausdorff",
                                                    "non_hausdorff"})
        return Result.false(
            mode="theorem",
            value="profinite",
            justification=[
                f"Tag {blocking!r}: profinite spaces must be Hausdorff. "
                "This space fails the Hausdorff separation axiom.",
            ],
            metadata={**base, "criterion": "not_hausdorff"},
        )

    return Result.unknown(
        mode="symbolic",
        value="profinite",
        justification=[
            "Insufficient tags to determine profiniteness. "
            "Supply tags such as 'profinite', 'compact_hausdorff', "
            "'totally_disconnected', 'cantor_space', or 'p_adic_integers'.",
        ],
        metadata={**base, "criterion": None},
    )


def stone_duality_applicable(space: Any) -> Result:
    """Check whether Stone duality applies to this space.

    Stone duality: the category of Stone spaces (compact Hausdorff zero-dimensional
    spaces) is dually equivalent to the category of Boolean algebras. A Stone space
    X corresponds to the Boolean algebra Clop(X) of its clopen sets. Key facts:
    - Compact Hausdorff zero-dimensional spaces are exactly the Stone spaces.
    - The Cantor set corresponds to the countable atomless Boolean algebra.
    - The Stone-Cech compactification betaS of a discrete set S corresponds to
      the Boolean algebra P(S) of all subsets.
    - betaN \\ N corresponds to P(N)/Fin (power set modulo finite sets).

    Decision layers
    ---------------
    1. Explicit Stone space / Boolean space tag -> true.
    2. Profinite spaces -> true (profinite = Stone space).
    3. Compact + Hausdorff + zero-dimensional tags -> true.
    4. Non-compact or non-Hausdorff -> false (Stone duality requires compactness + T2).
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"stone_space", "boolean_space"}):
        witness = next(t for t in tags if t in {"stone_space", "boolean_space"})
        return Result.true(
            mode="theorem",
            value="stone_duality_applicable",
            justification=[
                f"Tag {witness!r}: space is a Stone space. Stone duality asserts a "
                "contravariant equivalence with the category of Boolean algebras via "
                "X ↦ Clop(X) (clopen subsets). The inverse sends a Boolean algebra B "
                "to its Stone space (prime filters with Zariski topology).",
            ],
            metadata={**base, "criterion": "stone_space_tag", "witness": witness},
        )

    if _matches_any(tags, {"profinite", "profinite_space", "p_adic_integers",
                            "cantor_space", "cantor_set"}):
        witness = next(t for t in tags if t in {"profinite", "profinite_space",
                                                   "p_adic_integers",
                                                   "cantor_space", "cantor_set"})
        return Result.true(
            mode="theorem",
            value="stone_duality_applicable",
            justification=[
                f"Tag {witness!r}: profinite spaces are Stone spaces. "
                "Stone duality applies: Clop(X) is the corresponding Boolean algebra. "
                "For the Cantor set, Clop(C) is the countable atomless Boolean algebra.",
            ],
            metadata={**base, "criterion": "profinite_is_stone", "witness": witness},
        )

    if (_matches_any(tags, STONE_DUALITY_TAGS) and
            _matches_any(tags, {"zero_dimensional", "zero_dim", "clopen_base",
                                 "totally_disconnected"})):
        witness = next(t for t in tags if t in STONE_DUALITY_TAGS)
        return Result.true(
            mode="theorem",
            value="stone_duality_applicable",
            justification=[
                f"Tag {witness!r}: compact Hausdorff zero-dimensional space — Stone duality "
                "applies. The Boolean algebra Clop(X) captures the full topological "
                "structure of X up to homeomorphism.",
            ],
            metadata={**base, "criterion": "compact_hausdorff_zd_stone", "witness": witness},
        )

    if _matches_any(tags, NOT_ZERO_DIMENSIONAL_TAGS):
        blocking = next(t for t in tags if t in NOT_ZERO_DIMENSIONAL_TAGS)
        return Result.false(
            mode="theorem",
            value="stone_duality_applicable",
            justification=[
                f"Tag {blocking!r}: Stone duality requires zero-dimensionality. "
                "Connected or positive-dimensional spaces are not Stone spaces — "
                "their clopen algebra is trivial ({empty set, X}) and duality fails.",
            ],
            metadata={**base, "criterion": "not_zero_dimensional"},
        )

    if _matches_any(tags, {"non_compact", "not_compact", "rationals", "baire_space",
                            "irrationals"}):
        blocking = next(t for t in tags if t in {"non_compact", "not_compact",
                                                    "rationals", "baire_space", "irrationals"})
        return Result.false(
            mode="theorem",
            value="stone_duality_applicable",
            justification=[
                f"Tag {blocking!r}: classical Stone duality requires compactness. "
                "Non-compact zero-dimensional spaces correspond instead to Boolean algebras "
                "under the pointfree/frame-theoretic extension, not the classical Stone duality.",
            ],
            metadata={**base, "criterion": "not_compact_for_stone"},
        )

    return Result.unknown(
        mode="symbolic",
        value="stone_duality_applicable",
        justification=[
            "Insufficient tags to determine Stone duality applicability. "
            "Supply tags such as 'stone_space', 'profinite', 'compact_hausdorff', "
            "'zero_dimensional', or 'connected'.",
        ],
        metadata={**base, "criterion": None},
    )


def cantor_universality(space: Any) -> Result:
    """Check whether space embeds in the Cantor set (universality theorem).

    The Cantor universality theorem: every compact metrizable zero-dimensional space
    embeds homeomorphically in the Cantor set C. Equivalently, C is the universal
    compact metrizable zero-dimensional space. Key facts:
    - Every compact metrizable zero-dimensional space is a closed subset of C.
    - Every compact metrizable zero-dimensional space is a continuous image of C.
    - C itself is the unique (up to homeomorphism) compact metrizable perfect
      zero-dimensional space (Brouwer's theorem).
    - Non-metrizable compact zero-dimensional spaces need not embed in C.

    Decision layers
    ---------------
    1. Is the Cantor set/space itself -> true (trivially, is the universal space).
    2. Compact + metrizable + zero-dimensional -> true (universality theorem).
    3. Profinite + metrizable -> true.
    4. Non-metrizable compact zero-dimensional -> false (universality fails).
    5. Non-compact -> false (compact subset of compact C must be compact).
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"cantor_set", "cantor_space"}):
        witness = next(t for t in tags if t in {"cantor_set", "cantor_space"})
        return Result.true(
            mode="theorem",
            value="embeds_in_cantor",
            justification=[
                f"Tag {witness!r}: the Cantor set/space IS the universal compact metrizable "
                "zero-dimensional space. It embeds in itself (identity embedding). "
                "By Brouwer's theorem, it is the unique perfect compact metrizable "
                "zero-dimensional space.",
            ],
            metadata={**base, "criterion": "is_cantor", "witness": witness},
        )

    if (_matches_any(tags, EMBEDS_IN_CANTOR_TAGS) and
            _matches_any(tags, ZERO_DIMENSIONAL_TAGS | TOTALLY_DISCONNECTED_TAGS) and
            _matches_any(tags, {"metric", "metrizable", "compact_metrizable",
                                 "compact_metric"})):
        witness = next(t for t in tags if t in EMBEDS_IN_CANTOR_TAGS)
        return Result.true(
            mode="theorem",
            value="embeds_in_cantor",
            justification=[
                f"Tag {witness!r}: compact + metrizable + zero-dimensional. "
                "By the Cantor universality theorem, every compact metrizable "
                "zero-dimensional space embeds homeomorphically in the Cantor set C.",
            ],
            metadata={**base, "criterion": "compact_metrizable_zd", "witness": witness},
        )

    if (_matches_any(tags, {"profinite", "p_adic_integers"}) and
            _matches_any(tags, {"metric", "metrizable", "compact_metrizable"})):
        witness = next(t for t in tags if t in {"profinite", "p_adic_integers"})
        return Result.true(
            mode="theorem",
            value="embeds_in_cantor",
            justification=[
                f"Tag {witness!r}: profinite metrizable space (e.g., Zp) is compact, "
                "metrizable, and zero-dimensional. By Cantor universality, it embeds in C. "
                "In fact, Zp is homeomorphic to C as a topological space.",
            ],
            metadata={**base, "criterion": "profinite_metrizable", "witness": witness},
        )

    if (_matches_any(tags, {"compact", "compact_hausdorff"}) and
            _matches_any(tags, {"not_metrizable", "non_metrizable", "uncountable_weight"})):
        blocking = next(t for t in tags if t in {"not_metrizable", "non_metrizable",
                                                    "uncountable_weight"})
        return Result.false(
            mode="theorem",
            value="embeds_in_cantor",
            justification=[
                f"Tag {blocking!r}: the Cantor set C is a compact metrizable (second-countable) "
                "space. A non-metrizable compact space cannot embed in C, since "
                "subspaces of metrizable spaces are metrizable.",
            ],
            metadata={**base, "criterion": "not_metrizable"},
        )

    if _matches_any(tags, {"non_compact", "not_compact", "real_line", "reals",
                            "rationals", "baire_space", "irrationals",
                            "locally_compact_not_compact"}):
        blocking = next(t for t in tags if t in {"non_compact", "not_compact",
                                                    "real_line", "reals",
                                                    "rationals", "baire_space",
                                                    "irrationals",
                                                    "locally_compact_not_compact"})
        return Result.false(
            mode="theorem",
            value="embeds_in_cantor",
            justification=[
                f"Tag {blocking!r}: the Cantor set C is compact. A non-compact space "
                "cannot embed as a subspace of C (closed subsets of compact spaces are "
                "compact; open subsets of compact metrizable spaces have compact closure "
                "only if they are precompact).",
            ],
            metadata={**base, "criterion": "not_compact"},
        )

    return Result.unknown(
        mode="symbolic",
        value="embeds_in_cantor",
        justification=[
            "Insufficient tags to determine Cantor universality. "
            "Supply tags such as 'compact_metrizable', 'zero_dimensional', "
            "'cantor_set', 'profinite', or 'non_compact'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_zero_dimensionality(space: Any) -> dict[str, Any]:
    """Classify the zero-dimensional properties of space.

    Keys
    ----
    zero_dim_type : str
        One of ``"profinite"``, ``"compact_metrizable_zd"``,
        ``"polish_zd"``, ``"scattered"``, ``"zero_dimensional"``,
        ``"not_zero_dimensional"``, ``"unknown"``.
    has_clopen_base : Result
    is_zero_dimensional : Result
    is_profinite : Result
    stone_duality : Result
    embeds_in_cantor : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    clopen_r = has_clopen_base(space)
    zd_r = is_zero_dimensional(space)
    profinite_r = is_profinite(space)
    stone_r = stone_duality_applicable(space)
    cantor_r = cantor_universality(space)

    if profinite_r.is_true:
        zero_dim_type = "profinite"
    elif (_matches_any(tags, {"compact_metrizable", "compact_metric"}) and
          zd_r.is_true):
        zero_dim_type = "compact_metrizable_zd"
    elif (_matches_any(tags, {"polish_space", "polish", "completely_metrizable"}) and
          zd_r.is_true):
        zero_dim_type = "polish_zd"
    elif _matches_any(tags, SCATTERED_TAGS) and zd_r.is_true:
        zero_dim_type = "scattered"
    elif zd_r.is_true:
        zero_dim_type = "zero_dimensional"
    elif zd_r.is_false:
        zero_dim_type = "not_zero_dimensional"
    else:
        zero_dim_type = "unknown"

    key_properties: list[str] = []
    if clopen_r.is_true:
        key_properties.append("clopen_base")
    if zd_r.is_true:
        key_properties.append("zero_dimensional")
    if profinite_r.is_true:
        key_properties.append("profinite")
    if stone_r.is_true:
        key_properties.append("stone_duality")
    if cantor_r.is_true:
        key_properties.append("embeds_in_cantor")
    if _matches_any(tags, SCATTERED_TAGS):
        key_properties.append("scattered")
    if zd_r.is_false:
        key_properties.append("not_zero_dimensional")

    return {
        "zero_dim_type": zero_dim_type,
        "has_clopen_base": clopen_r,
        "is_zero_dimensional": zd_r,
        "is_profinite": profinite_r,
        "stone_duality": stone_r,
        "embeds_in_cantor": cantor_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def zero_dimensionality_profile(space: Any) -> dict[str, Any]:
    """Full zero-dimensionality profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_zero_dimensionality`.
    named_profiles : tuple[ZeroDimensionalProfile, ...]
        Registry of canonical zero-dimensional space examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_zero_dimensionality(space),
        "named_profiles": get_named_zero_dimensional_profiles(),
        "layer_summary": zero_dimensional_layer_summary(),
    }


__all__ = [
    "ZeroDimensionalProfile",
    "ZERO_DIMENSIONAL_TAGS",
    "TOTALLY_DISCONNECTED_TAGS",
    "PROFINITE_TAGS",
    "COMPACT_ZD_TAGS",
    "SCATTERED_TAGS",
    "NOT_ZERO_DIMENSIONAL_TAGS",
    "COMPACT_HAUSDORFF_TAGS",
    "STONE_DUALITY_TAGS",
    "EMBEDS_IN_CANTOR_TAGS",
    "get_named_zero_dimensional_profiles",
    "zero_dimensional_layer_summary",
    "zero_dimensional_chapter_index",
    "zero_dimensional_type_index",
    "has_clopen_base",
    "is_zero_dimensional",
    "is_profinite",
    "stone_duality_applicable",
    "cantor_universality",
    "classify_zero_dimensionality",
    "zero_dimensionality_profile",
]
