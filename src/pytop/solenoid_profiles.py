"""Solenoids and inverse limit spaces.

Key theorems implemented
------------------------
- A solenoid Sigma_p is the inverse limit lim_<-- (S^1 <--phi_p-- S^1 <--phi_p-- ...)
  where phi_p(z) = z^p is the p-fold covering map of the circle.
- Compactness of inverse limits (Tychonoff): the inverse limit of compact spaces
  with continuous bonding maps is compact.
- Connectedness of inverse limits: if all factor spaces are connected and all
  bonding maps are surjective, the inverse limit is connected.
- Indecomposability: every solenoid is an indecomposable continuum — it cannot
  be written as the union of two proper subcontinua.
- Homogeneity: solenoids are compact abelian topological groups and hence
  homogeneous (every point has a homeomorphism of the whole space sending it
  to any other point).
- Local structure: locally, every solenoid is homeomorphic to (Cantor set) x (0,1).
- Non-local connectedness: solenoids are NOT locally connected — no connected
  open neighbourhood exists at any point.
- Pontryagin duality: the Pontryagin dual of the p-adic solenoid Sigma_p is the
  Prufer group Z(p^inf) = Z[1/p]/Z.
- Metrizable inverse limits: a countable inverse limit of compact metrizable
  spaces is compact metrizable (hence second-countable).
- The Cantor set arises as the inverse limit of finite discrete spaces.
- The Hilbert cube [0,1]^omega is the inverse limit of [0,1]^n with projection maps.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class SolenoidProfile:
    """A curated solenoid or inverse limit space example."""

    key: str
    display_name: str
    space_type: str
    is_compact: bool
    is_connected: bool
    is_metrizable: bool
    is_indecomposable: bool
    is_homogeneous: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

SOLENOID_TAGS: set[str] = {
    "solenoid", "dyadic_solenoid", "p_adic_solenoid",
    "generalized_solenoid", "solenoid_group",
    "inverse_limit_circles",
}
INVERSE_LIMIT_TAGS: set[str] = {
    "inverse_limit", "projective_limit",
    "solenoid", "dyadic_solenoid", "p_adic_solenoid",
    "generalized_solenoid",
    "profinite", "p_adic_integers",
    "cantor_set", "cantor_space",
    "hilbert_cube",
}
INDECOMPOSABLE_TAGS: set[str] = {
    "indecomposable", "indecomposable_continuum",
    "solenoid", "dyadic_solenoid", "p_adic_solenoid",
    "generalized_solenoid",
    "pseudo_arc",
}
COMPACT_FACTOR_TAGS: set[str] = {
    "compact_factors", "compact_metrizable_factors",
    "solenoid", "dyadic_solenoid", "p_adic_solenoid",
    "generalized_solenoid",
    "profinite", "p_adic_integers",
    "cantor_set", "hilbert_cube",
    "compact_inverse_limit",
}
CONNECTED_FACTOR_TAGS: set[str] = {
    "connected_factors", "surjective_bonding_maps",
    "solenoid", "dyadic_solenoid", "p_adic_solenoid",
    "generalized_solenoid",
    "hilbert_cube",
    "connected_inverse_limit",
}
HOMOGENEOUS_TAGS: set[str] = {
    "homogeneous", "topological_group", "abelian_group",
    "solenoid", "dyadic_solenoid", "p_adic_solenoid",
    "generalized_solenoid", "solenoid_group",
    "cantor_space", "cantor_set",
    "torus", "circle",
}
NOT_SOLENOID_TAGS: set[str] = {
    "locally_connected", "locally_path_connected",
    "manifold", "topological_manifold",
    "interval", "disk", "sphere",
    "discrete", "scattered", "zero_dimensional",
    "finite_space",
}
LOCALLY_DISCONNECTED_TAGS: set[str] = {
    "solenoid", "dyadic_solenoid", "p_adic_solenoid",
    "generalized_solenoid",
    "not_locally_connected", "locally_disconnected",
    "cantor_set", "cantor_space",
    "profinite",
}
METRIZABLE_INVERSE_LIMIT_TAGS: set[str] = {
    "solenoid", "dyadic_solenoid", "p_adic_solenoid",
    "generalized_solenoid",
    "profinite", "p_adic_integers",
    "cantor_set", "cantor_space",
    "hilbert_cube",
    "compact_metrizable_factors",
    "countable_inverse_limit",
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

def get_named_solenoid_profiles() -> tuple[SolenoidProfile, ...]:
    """Return the registry of canonical solenoid and inverse limit examples."""
    return (
        SolenoidProfile(
            key="dyadic_solenoid",
            display_name="Sigma_2 — the dyadic solenoid",
            space_type="solenoid_group",
            is_compact=True,
            is_connected=True,
            is_metrizable=True,
            is_indecomposable=True,
            is_homogeneous=True,
            presentation_layer="main_text",
            focus=(
                "The dyadic solenoid Sigma_2 = lim_<-- (S^1 <--phi_2-- S^1 <--phi_2-- ...) "
                "where phi_2(z) = z^2 is the double covering map of the circle. "
                "It is a compact, connected, metrizable topological group. "
                "As an abelian group, Sigma_2 is the Pontryagin dual of the Prufer 2-group "
                "Z(2^inf) = Z[1/2]/Z. "
                "Sigma_2 is an indecomposable continuum: it cannot be written as the "
                "union of two proper closed connected subsets. "
                "Locally it looks like (Cantor set) x (open interval), so it is NOT "
                "locally connected. Sigma_2 embeds in the solid torus T^2, winding "
                "densely inside."
            ),
            chapter_targets=("6", "28", "46"),
        ),
        SolenoidProfile(
            key="p_adic_solenoid",
            display_name="Sigma_p — the p-adic solenoid (prime p)",
            space_type="solenoid_group",
            is_compact=True,
            is_connected=True,
            is_metrizable=True,
            is_indecomposable=True,
            is_homogeneous=True,
            presentation_layer="main_text",
            focus=(
                "The p-adic solenoid Sigma_p = lim_<-- (S^1 <--phi_p-- S^1 <--phi_p-- ...) "
                "for a prime p, where phi_p(z) = z^p. "
                "Sigma_p is a compact connected metrizable abelian topological group. "
                "Its Pontryagin dual is the Prufer p-group Z(p^inf) = Z[1/p]/Z. "
                "Sigma_p is homeomorphic to (Zp x R) / Z where Zp is the p-adic integers "
                "and Z embeds diagonally. "
                "Every p-adic solenoid is an indecomposable continuum and is homogeneous. "
                "For different primes p and q, Sigma_p is not homeomorphic to Sigma_q "
                "(they have different first homology groups)."
            ),
            chapter_targets=("6", "28", "46"),
        ),
        SolenoidProfile(
            key="generalized_solenoid",
            display_name="Sigma_{p_1,p_2,...} — generalized solenoid",
            space_type="solenoid_group",
            is_compact=True,
            is_connected=True,
            is_metrizable=True,
            is_indecomposable=True,
            is_homogeneous=True,
            presentation_layer="selected_block",
            focus=(
                "The generalized solenoid Sigma_{p_1,p_2,...} = "
                "lim_<-- (S^1 <--phi_{p_1}-- S^1 <--phi_{p_2}-- S^1 ...) "
                "uses possibly different covering degrees p_i at each stage. "
                "If all p_i = p (constant), this reduces to the p-adic solenoid. "
                "Generalized solenoids are classified (up to homeomorphism) by their "
                "supernatural number: the formal product prod p_i^{n_p} where n_p "
                "counts the number of times prime p appears among the p_i. "
                "All generalized solenoids are compact, connected, indecomposable "
                "metrizable continua and homogeneous topological groups."
            ),
            chapter_targets=("6", "28", "46"),
        ),
        SolenoidProfile(
            key="p_adic_integers_lim",
            display_name="Zp = lim_<-- Z/p^nZ — p-adic integers as inverse limit",
            space_type="profinite_inverse_limit",
            is_compact=True,
            is_connected=False,
            is_metrizable=True,
            is_indecomposable=False,
            is_homogeneous=True,
            presentation_layer="main_text",
            focus=(
                "The p-adic integers Zp = lim_<-- (... -> Z/p^2Z -> Z/p Z) form a "
                "compact, zero-dimensional, metrizable topological ring. "
                "As an inverse limit of finite discrete groups, Zp is profinite. "
                "It is homeomorphic to the Cantor set (not to a solenoid) because "
                "it is totally disconnected. Zp is a homogeneous topological group. "
                "Unlike solenoids, Zp is NOT connected — it is a profinite (zero-dimensional) "
                "inverse limit, not a connected one. Zp appears as a factor in the "
                "description of solenoids: Sigma_p cong (Zp x R) / Z."
            ),
            chapter_targets=("6", "29", "46"),
        ),
        SolenoidProfile(
            key="hilbert_cube_lim",
            display_name="[0,1]^omega = lim_<-- [0,1]^n — Hilbert cube as inverse limit",
            space_type="compact_ar_inverse_limit",
            is_compact=True,
            is_connected=True,
            is_metrizable=True,
            is_indecomposable=False,
            is_homogeneous=False,
            presentation_layer="selected_block",
            focus=(
                "The Hilbert cube [0,1]^omega = lim_<-- ([0,1]^n, pi_n) where pi_n "
                "is the projection dropping the last coordinate is a compact, connected, "
                "metrizable absolute retract (AR). "
                "It is not homogeneous: end points (sequences constantly 0 or 1) are "
                "topologically different from interior points. "
                "The Hilbert cube is the unique (up to homeomorphism) compact metrizable "
                "AR — the Anderson-Kadec theorem. "
                "Every compact metrizable space embeds in [0,1]^omega. "
                "The Hilbert cube is NOT indecomposable: it is an AR (and in particular "
                "an absolute neighbourhood retract), which implies it is an AR-continuum, "
                "hence locally connected and certainly decomposable."
            ),
            chapter_targets=("4", "9", "28"),
        ),
        SolenoidProfile(
            key="cantor_set_lim",
            display_name="C = lim_<-- {0,1}^n — Cantor set as inverse limit",
            space_type="profinite_inverse_limit",
            is_compact=True,
            is_connected=False,
            is_metrizable=True,
            is_indecomposable=False,
            is_homogeneous=True,
            presentation_layer="main_text",
            focus=(
                "The Cantor set C = lim_<-- ({0,1}^n, pi_n) is the inverse limit of "
                "finite discrete spaces {0,1}^n with projection bonding maps. "
                "It is compact, metrizable, perfect, and zero-dimensional. "
                "C is homogeneous (every point looks the same) and is the universal "
                "compact metrizable zero-dimensional space. "
                "As a totally disconnected inverse limit, C is the prototypical "
                "profinite space — in sharp contrast to solenoids, which are connected "
                "inverse limits of circles."
            ),
            chapter_targets=("4", "6", "29"),
        ),
        SolenoidProfile(
            key="warsaw_circle_lim",
            display_name="Warsaw circle — inverse limit of arcs",
            space_type="chainable_continuum",
            is_compact=True,
            is_connected=True,
            is_metrizable=True,
            is_indecomposable=False,
            is_homogeneous=False,
            presentation_layer="advanced_note",
            focus=(
                "The Warsaw circle is a compact connected metrizable space built by "
                "attaching a topologist's sine curve to its limit segment. "
                "It is chainable (an inverse limit of arcs) and is a continuum, but "
                "is NOT locally connected (the sine limit segment has no connected "
                "neighbourhood). Unlike solenoids, the Warsaw circle is NOT a "
                "topological group and is NOT homogeneous. "
                "It is not indecomposable: it can be decomposed into the topologist's "
                "sine curve and the arc. The Warsaw circle is the standard example "
                "of a compact connected space that is not path-connected."
            ),
            chapter_targets=("6", "28"),
        ),
    )


def solenoid_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_solenoid_profiles()))


def solenoid_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_solenoid_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def solenoid_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from space_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_solenoid_profiles():
        index.setdefault(p.space_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_solenoid(space: Any) -> Result:
    """Check whether space is a solenoid (inverse limit of circles).

    A solenoid is an inverse limit lim_<-- (S^1 <--phi_{p_i}-- S^1 ...) where
    each phi_{p_i} is a p_i-fold covering map of the circle. Key facts:
    - Solenoids are compact, connected, metrizable abelian topological groups.
    - Every solenoid is an indecomposable continuum.
    - Solenoids are NOT locally connected.
    - A space is a solenoid iff it is a compact connected metrizable abelian group
      whose Pontryagin dual is a subgroup of Q (rational numbers).

    Decision layers
    ---------------
    1. Explicit solenoid tags -> true.
    2. Inverse limit of circles with covering maps -> true.
    3. Locally connected -> false (solenoids are never locally connected).
    4. Manifold / arc / sphere -> false.
    5. Discrete / zero-dimensional -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, SOLENOID_TAGS):
        witness = next(t for t in tags if t in SOLENOID_TAGS)
        return Result.true(
            mode="theorem",
            value="is_solenoid",
            justification=[
                f"Tag {witness!r}: space is a solenoid — an inverse limit of circles "
                "with covering maps as bonding maps. "
                "Solenoids are compact connected metrizable indecomposable continua.",
            ],
            metadata={**base, "criterion": "solenoid_tag", "witness": witness},
        )

    if _matches_any(tags, {"inverse_limit_circles"}):
        witness = "inverse_limit_circles"
        return Result.true(
            mode="theorem",
            value="is_solenoid",
            justification=[
                f"Tag {witness!r}: an inverse limit of circles with covering bonding "
                "maps is a solenoid by definition.",
            ],
            metadata={**base, "criterion": "inverse_limit_circles", "witness": witness},
        )

    if _matches_any(tags, {"locally_connected", "locally_path_connected"}):
        blocking = next(t for t in tags if t in {"locally_connected",
                                                    "locally_path_connected"})
        return Result.false(
            mode="theorem",
            value="is_solenoid",
            justification=[
                f"Tag {blocking!r}: solenoids are never locally connected. "
                "Locally, a solenoid looks like (Cantor set) x (open interval), "
                "so no point has a connected open neighbourhood.",
            ],
            metadata={**base, "criterion": "locally_connected_excludes_solenoid"},
        )

    if _matches_any(tags, NOT_SOLENOID_TAGS):
        blocking = next(t for t in tags if t in NOT_SOLENOID_TAGS)
        return Result.false(
            mode="theorem",
            value="is_solenoid",
            justification=[
                f"Tag {blocking!r}: manifolds, arcs, disks, discrete spaces, and "
                "zero-dimensional spaces are not solenoids. Solenoids are connected "
                "one-dimensional continua that are not locally connected.",
            ],
            metadata={**base, "criterion": "not_solenoid_type"},
        )

    return Result.unknown(
        mode="symbolic",
        value="is_solenoid",
        justification=[
            "Insufficient tags to determine whether space is a solenoid. "
            "Supply tags such as 'solenoid', 'dyadic_solenoid', 'p_adic_solenoid', "
            "'inverse_limit_circles', or 'locally_connected'.",
        ],
        metadata={**base, "criterion": None},
    )


def inverse_limit_is_compact(space: Any) -> Result:
    """Check whether the inverse limit is compact (Tychonoff for inverse limits).

    By the Tychonoff theorem, the inverse limit of any family of compact spaces
    with continuous bonding maps is compact (it is a closed subspace of the
    product, which is compact by Tychonoff). Key facts:
    - Solenoids: compact (each circle factor S^1 is compact).
    - Zp = lim_<-- Z/p^nZ: compact (finite discrete factors are compact).
    - Cantor set as lim_<-- {0,1}^n: compact.
    - Hilbert cube [0,1]^omega: compact.
    - If even one factor is not compact, the inverse limit may fail to be compact.

    Decision layers
    ---------------
    1. Solenoid (compact by definition) -> true.
    2. Compact factor spaces (Tychonoff) -> true.
    3. Profinite / Cantor / Hilbert cube -> true.
    4. Non-compact factors explicitly mentioned -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, SOLENOID_TAGS):
        witness = next(t for t in tags if t in SOLENOID_TAGS)
        return Result.true(
            mode="theorem",
            value="inverse_limit_compact",
            justification=[
                f"Tag {witness!r}: solenoids are compact by construction — "
                "they are inverse limits of compact circles S^1. "
                "By the Tychonoff theorem, the inverse limit is compact.",
            ],
            metadata={**base, "criterion": "solenoid_compact", "witness": witness},
        )

    if _matches_any(tags, COMPACT_FACTOR_TAGS):
        witness = next(t for t in tags if t in COMPACT_FACTOR_TAGS)
        return Result.true(
            mode="theorem",
            value="inverse_limit_compact",
            justification=[
                f"Tag {witness!r}: the factor spaces are compact. "
                "By the Tychonoff theorem (inverse limit form), the inverse limit of "
                "compact spaces is compact — it is a closed subspace of the compact product.",
            ],
            metadata={**base, "criterion": "compact_factors_tychonoff", "witness": witness},
        )

    if _matches_any(tags, {"non_compact_factors", "not_compact_factors",
                            "real_line_factors", "open_interval_factors"}):
        blocking = next(t for t in tags if t in {"non_compact_factors",
                                                    "not_compact_factors",
                                                    "real_line_factors",
                                                    "open_interval_factors"})
        return Result.false(
            mode="theorem",
            value="inverse_limit_compact",
            justification=[
                f"Tag {blocking!r}: the factor spaces are not compact. "
                "The inverse limit of non-compact spaces need not be compact: "
                "Tychonoff's theorem applies only to compact factor spaces.",
            ],
            metadata={**base, "criterion": "non_compact_factors"},
        )

    return Result.unknown(
        mode="symbolic",
        value="inverse_limit_compact",
        justification=[
            "Insufficient tags to determine compactness of the inverse limit. "
            "Supply tags such as 'compact_factors', 'solenoid', 'profinite', "
            "'hilbert_cube', or 'non_compact_factors'.",
        ],
        metadata={**base, "criterion": None},
    )


def inverse_limit_is_connected(space: Any) -> Result:
    """Check whether the inverse limit is connected.

    If all factor spaces are connected and all bonding maps are surjective, then
    the inverse limit is connected. Key facts:
    - Solenoids: connected (circle S^1 is connected, covering maps are surjective).
    - Hilbert cube: connected (each [0,1]^n factor is connected).
    - Cantor set as inverse limit: NOT connected (finite discrete factors are
      disconnected when |factor| > 1).
    - Zp: NOT connected (finite group factors Z/p^nZ with discrete topology are
      disconnected for p^n > 1).

    Decision layers
    ---------------
    1. Solenoid (always connected) -> true.
    2. Connected factors + surjective bonding maps -> true.
    3. Hilbert cube -> true.
    4. Profinite / Cantor set / Zp (disconnected factors) -> false.
    5. Totally disconnected inverse limit -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, SOLENOID_TAGS):
        witness = next(t for t in tags if t in SOLENOID_TAGS)
        return Result.true(
            mode="theorem",
            value="inverse_limit_connected",
            justification=[
                f"Tag {witness!r}: solenoids are connected — the circle S^1 is connected "
                "and the covering maps phi_p are surjective. An inverse limit of connected "
                "spaces with surjective bonding maps is connected.",
            ],
            metadata={**base, "criterion": "solenoid_connected", "witness": witness},
        )

    if _matches_any(tags, CONNECTED_FACTOR_TAGS) and _matches_any(
        tags, {"surjective_bonding_maps", "connected_factors",
               "hilbert_cube", "connected_inverse_limit"}
    ):
        witness = next(t for t in tags if t in CONNECTED_FACTOR_TAGS)
        return Result.true(
            mode="theorem",
            value="inverse_limit_connected",
            justification=[
                f"Tag {witness!r}: the factor spaces are connected and the bonding maps "
                "are surjective. The inverse limit of connected spaces with surjective "
                "bonding maps is connected.",
            ],
            metadata={**base, "criterion": "connected_factors_surjective", "witness": witness},
        )

    if _matches_any(tags, {"profinite", "p_adic_integers", "cantor_set",
                            "cantor_space", "totally_disconnected",
                            "profinite_inverse_limit"}):
        blocking = next(t for t in tags if t in {"profinite", "p_adic_integers",
                                                    "cantor_set", "cantor_space",
                                                    "totally_disconnected",
                                                    "profinite_inverse_limit"})
        return Result.false(
            mode="theorem",
            value="inverse_limit_connected",
            justification=[
                f"Tag {blocking!r}: profinite and Cantor-type inverse limits have "
                "totally disconnected (finite discrete) factor spaces. "
                "The inverse limit of disconnected spaces is disconnected when "
                "the factors are totally disconnected.",
            ],
            metadata={**base, "criterion": "disconnected_factors"},
        )

    if _matches_any(tags, {"disconnected_factors", "discrete_factors"}):
        blocking = next(t for t in tags if t in {"disconnected_factors", "discrete_factors"})
        return Result.false(
            mode="theorem",
            value="inverse_limit_connected",
            justification=[
                f"Tag {blocking!r}: disconnected factor spaces yield a disconnected "
                "inverse limit when the bonding maps preserve the disconnected structure.",
            ],
            metadata={**base, "criterion": "discrete_factors"},
        )

    return Result.unknown(
        mode="symbolic",
        value="inverse_limit_connected",
        justification=[
            "Insufficient tags to determine connectedness of the inverse limit. "
            "Supply tags such as 'solenoid', 'connected_factors', 'surjective_bonding_maps', "
            "'profinite', or 'cantor_set'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_indecomposable_continuum(space: Any) -> Result:
    """Check whether space is an indecomposable continuum.

    A continuum X is indecomposable if it cannot be written as the union of two
    proper subcontinua (proper closed connected subsets). Key facts:
    - Every solenoid is an indecomposable continuum.
    - The pseudo-arc is another classic indecomposable continuum.
    - Locally connected continua are NEVER indecomposable (by a theorem of
      Sierpinski: every locally connected continuum is decomposable).
    - Arcs, disks, circles, tori are all decomposable (locally connected).
    - An indecomposable continuum has uncountably many composants (maximal
      proper subcontinua that are not the whole space).

    Decision layers
    ---------------
    1. Explicit solenoid or indecomposable tags -> true.
    2. Locally connected continuum -> false (Sierpinski's theorem).
    3. Arc / disk / sphere / torus -> false (decomposable manifolds).
    4. Discrete / zero-dimensional -> false (not a continuum).
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, INDECOMPOSABLE_TAGS):
        witness = next(t for t in tags if t in INDECOMPOSABLE_TAGS)
        return Result.true(
            mode="theorem",
            value="indecomposable_continuum",
            justification=[
                f"Tag {witness!r}: solenoids (and pseudo-arcs) are indecomposable "
                "continua. A solenoid cannot be written as the union of two proper "
                "subcontinua. Its composants (maximal proper connected subsets) are "
                "dense and uncountably many.",
            ],
            metadata={**base, "criterion": "solenoid_indecomposable", "witness": witness},
        )

    if _matches_any(tags, {"locally_connected", "locally_path_connected"}):
        blocking = next(t for t in tags if t in {"locally_connected",
                                                    "locally_path_connected"})
        return Result.false(
            mode="theorem",
            value="indecomposable_continuum",
            justification=[
                f"Tag {blocking!r}: by Sierpinski's theorem, every locally connected "
                "continuum is decomposable. Indecomposable continua are never locally "
                "connected.",
            ],
            metadata={**base, "criterion": "locally_connected_decomposable"},
        )

    if _matches_any(tags, {"arc", "interval", "disk", "sphere", "torus",
                            "closed_interval", "circle", "manifold",
                            "topological_manifold", "hilbert_cube"}):
        blocking = next(t for t in tags if t in {"arc", "interval", "disk",
                                                    "sphere", "torus", "closed_interval",
                                                    "circle", "manifold",
                                                    "topological_manifold",
                                                    "hilbert_cube"})
        return Result.false(
            mode="theorem",
            value="indecomposable_continuum",
            justification=[
                f"Tag {blocking!r}: arcs, disks, spheres, tori, and manifolds are "
                "locally connected continua — all decomposable by Sierpinski's theorem.",
            ],
            metadata={**base, "criterion": "manifold_decomposable"},
        )

    if _matches_any(tags, {"discrete", "scattered", "zero_dimensional",
                            "cantor_set", "cantor_space", "profinite",
                            "totally_disconnected"}):
        blocking = next(t for t in tags if t in {"discrete", "scattered",
                                                    "zero_dimensional", "cantor_set",
                                                    "cantor_space", "profinite",
                                                    "totally_disconnected"})
        return Result.false(
            mode="theorem",
            value="indecomposable_continuum",
            justification=[
                f"Tag {blocking!r}: zero-dimensional and totally disconnected spaces "
                "are not continua (a continuum must be connected). "
                "Indecomposability is a property of connected spaces only.",
            ],
            metadata={**base, "criterion": "not_connected_not_continuum"},
        )

    return Result.unknown(
        mode="symbolic",
        value="indecomposable_continuum",
        justification=[
            "Insufficient tags to determine indecomposability. "
            "Supply tags such as 'solenoid', 'indecomposable', 'pseudo_arc', "
            "'locally_connected' (-> false), or 'manifold' (-> false).",
        ],
        metadata={**base, "criterion": None},
    )


def solenoid_is_homogeneous(space: Any) -> Result:
    """Check whether space is homogeneous (as a topological group or continuum).

    A topological space X is homogeneous if for every pair of points x, y in X
    there is a homeomorphism h: X -> X with h(x) = y. Key facts:
    - Every topological group is homogeneous (left translation is a homeomorphism).
    - Solenoids are topological groups, hence homogeneous.
    - The Cantor set is homogeneous.
    - The Hilbert cube is NOT homogeneous (boundary points vs interior points).
    - The Warsaw circle is NOT homogeneous.
    - Arcs [0,1] are not homogeneous (endpoints are topologically distinct).

    Decision layers
    ---------------
    1. Solenoid or explicit homogeneous / topological group -> true.
    2. Cantor set/space (universal homogeneous compact metrizable zero-dim) -> true.
    3. Hilbert cube -> false (not homogeneous).
    4. Arc / interval / disk -> false (endpoints/boundary points differ).
    5. Warsaw circle / chainable continuum without group structure -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, SOLENOID_TAGS | HOMOGENEOUS_TAGS):
        witness = next(t for t in tags if t in (SOLENOID_TAGS | HOMOGENEOUS_TAGS))
        return Result.true(
            mode="theorem",
            value="homogeneous",
            justification=[
                f"Tag {witness!r}: solenoids are compact abelian topological groups, "
                "hence homogeneous: left translation h_g(x) = g + x is a homeomorphism "
                "for every group element g. The Cantor space is also homogeneous.",
            ],
            metadata={**base, "criterion": "topological_group_homogeneous", "witness": witness},
        )

    if _matches_any(tags, {"hilbert_cube"}):
        return Result.false(
            mode="theorem",
            value="homogeneous",
            justification=[
                "Tag 'hilbert_cube': the Hilbert cube [0,1]^omega is NOT homogeneous. "
                "Points with all coordinates in (0,1) (interior points) are "
                "topologically different from points with some coordinate equal to 0 or 1 "
                "(boundary points). No homeomorphism can send an interior point to a "
                "boundary point.",
            ],
            metadata={**base, "criterion": "hilbert_cube_not_homogeneous"},
        )

    if _matches_any(tags, {"arc", "interval", "closed_interval", "disk"}):
        blocking = next(t for t in tags if t in {"arc", "interval",
                                                    "closed_interval", "disk"})
        return Result.false(
            mode="theorem",
            value="homogeneous",
            justification=[
                f"Tag {blocking!r}: arcs and disks are not homogeneous. "
                "Endpoints of an arc have only one side, while interior points have two — "
                "no homeomorphism can map an endpoint to an interior point.",
            ],
            metadata={**base, "criterion": "arc_not_homogeneous"},
        )

    if _matches_any(tags, {"warsaw_circle", "chainable_continuum",
                            "not_homogeneous", "non_homogeneous"}):
        blocking = next(t for t in tags if t in {"warsaw_circle",
                                                    "chainable_continuum",
                                                    "not_homogeneous",
                                                    "non_homogeneous"})
        return Result.false(
            mode="theorem",
            value="homogeneous",
            justification=[
                f"Tag {blocking!r}: the Warsaw circle and chainable continua (that are "
                "not groups) are not homogeneous. The special limit arc has a different "
                "local topology from the rest of the space.",
            ],
            metadata={**base, "criterion": "warsaw_not_homogeneous"},
        )

    return Result.unknown(
        mode="symbolic",
        value="homogeneous",
        justification=[
            "Insufficient tags to determine homogeneity. "
            "Supply tags such as 'solenoid', 'topological_group', 'homogeneous', "
            "'hilbert_cube', 'cantor_set', or 'arc'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_solenoid(space: Any) -> dict[str, Any]:
    """Classify the solenoid and inverse limit properties of space.

    Keys
    ----
    solenoid_type : str
        One of ``"solenoid"``, ``"profinite_inverse_limit"``,
        ``"connected_inverse_limit"``, ``"compact_inverse_limit"``,
        ``"not_solenoid"``, ``"unknown"``.
    is_solenoid : Result
    is_compact : Result
    is_connected : Result
    is_indecomposable : Result
    is_homogeneous : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    sol_r = is_solenoid(space)
    cpt_r = inverse_limit_is_compact(space)
    con_r = inverse_limit_is_connected(space)
    ind_r = is_indecomposable_continuum(space)
    hom_r = solenoid_is_homogeneous(space)

    if sol_r.is_true:
        solenoid_type = "solenoid"
    elif (_matches_any(tags, {"profinite", "p_adic_integers", "cantor_set",
                               "cantor_space"}) and cpt_r.is_true):
        solenoid_type = "profinite_inverse_limit"
    elif con_r.is_true and cpt_r.is_true:
        solenoid_type = "connected_inverse_limit"
    elif cpt_r.is_true:
        solenoid_type = "compact_inverse_limit"
    elif sol_r.is_false:
        solenoid_type = "not_solenoid"
    else:
        solenoid_type = "unknown"

    key_properties: list[str] = []
    if sol_r.is_true:
        key_properties.append("solenoid")
    if cpt_r.is_true:
        key_properties.append("compact")
    if con_r.is_true:
        key_properties.append("connected")
    if con_r.is_false:
        key_properties.append("disconnected")
    if ind_r.is_true:
        key_properties.append("indecomposable")
    if ind_r.is_false:
        key_properties.append("decomposable")
    if hom_r.is_true:
        key_properties.append("homogeneous")
    if hom_r.is_false:
        key_properties.append("not_homogeneous")

    return {
        "solenoid_type": solenoid_type,
        "is_solenoid": sol_r,
        "is_compact": cpt_r,
        "is_connected": con_r,
        "is_indecomposable": ind_r,
        "is_homogeneous": hom_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def solenoid_profile(space: Any) -> dict[str, Any]:
    """Full solenoid profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_solenoid`.
    named_profiles : tuple[SolenoidProfile, ...]
        Registry of canonical solenoid and inverse limit examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_solenoid(space),
        "named_profiles": get_named_solenoid_profiles(),
        "layer_summary": solenoid_layer_summary(),
    }


__all__ = [
    "SolenoidProfile",
    "SOLENOID_TAGS",
    "INVERSE_LIMIT_TAGS",
    "INDECOMPOSABLE_TAGS",
    "COMPACT_FACTOR_TAGS",
    "CONNECTED_FACTOR_TAGS",
    "HOMOGENEOUS_TAGS",
    "NOT_SOLENOID_TAGS",
    "LOCALLY_DISCONNECTED_TAGS",
    "METRIZABLE_INVERSE_LIMIT_TAGS",
    "get_named_solenoid_profiles",
    "solenoid_layer_summary",
    "solenoid_chapter_index",
    "solenoid_type_index",
    "is_solenoid",
    "inverse_limit_is_compact",
    "inverse_limit_is_connected",
    "is_indecomposable_continuum",
    "solenoid_is_homogeneous",
    "classify_solenoid",
    "solenoid_profile",
]
