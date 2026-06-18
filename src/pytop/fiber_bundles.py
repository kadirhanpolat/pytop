"""Fiber bundles: local triviality, vector bundles, principal bundles, and sections.

Key theorems implemented
------------------------
- Every fiber bundle pi: E -> B with fiber F is locally trivial: each point b in B
  has a neighbourhood U such that pi^{-1}(U) is homeomorphic to U x F over U.
- A vector bundle is a fiber bundle whose fiber is a vector space R^n (or C^n)
  with transition functions in GL(n,R) (or GL(n,C)).
- The zero section sigma_0: B -> E (b |-> 0_b) always exists for any vector bundle.
- Hairy ball theorem: the tangent bundle TS^{2n} has no nowhere-zero section.
  Equivalently, every continuous vector field on S^{2n} vanishes somewhere.
  This follows from the Poincare-Hopf theorem: chi(S^{2n}) = 2 != 0, so the
  Euler class e(TS^{2n}) != 0, obstructing a nowhere-zero section.
- Odd-dimensional spheres S^{2n-1} admit a nowhere-zero tangent vector field
  (rotate each tangent vector by 90 degrees in the fibre), since chi(S^{2n-1}) = 0.
- S^n is parallelizable (TS^n trivial) only for n = 1, 3, 7 (Adams' theorem via
  K-theory and Adams operations).
- The Mobius band is the total space of the non-trivial real line bundle over S^1.
  It has no nowhere-zero section: a non-vanishing section would yield a continuous
  map S^1 -> R\\{0} that changes sign after one full loop — contradicting continuity.
- The Hopf fibration eta: S^3 -> S^2 with fibre S^1 is a principal U(1)-bundle.
  Its Hopf invariant equals 1 and it represents the generator of pi_3(S^2) ≅ Z.
- Every principal GL(n)-bundle (frame bundle of a smooth manifold) admits a
  reduction of structure group to O(n): pick a Riemannian metric via partition of unity.
- A fiber bundle over a contractible base is trivial (homotopy lifting property).
- Classification: principal G-bundles over a paracompact space X are classified by
  homotopy classes [X, BG], where BG is the classifying space of G.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class FiberBundleProfile:
    """A curated fiber bundle example."""

    key: str
    display_name: str
    bundle_type: str
    is_locally_trivial: bool
    is_vector_bundle: bool
    is_principal: bool
    is_trivial: bool
    has_nowhere_zero_section: bool
    is_orientable: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

LOCALLY_TRIVIAL_TAGS: frozenset[str] = frozenset({
    "fiber_bundle", "locally_trivial",
    "vector_bundle", "line_bundle",
    "principal_bundle", "trivial_bundle",
    "real_vector_bundle", "complex_vector_bundle",
    "mobius_band", "tangent_bundle", "cotangent_bundle",
    "hopf_bundle", "frame_bundle",
    "tautological_bundle", "normal_bundle",
    "rank_n_bundle",
})

VECTOR_BUNDLE_TAGS: frozenset[str] = frozenset({
    "vector_bundle", "real_vector_bundle", "complex_vector_bundle",
    "line_bundle", "rank_n_bundle",
    "tangent_bundle", "cotangent_bundle",
    "normal_bundle", "tautological_bundle",
    "mobius_band",
})

PRINCIPAL_BUNDLE_TAGS: frozenset[str] = frozenset({
    "principal_bundle", "principal_g_bundle",
    "frame_bundle", "hopf_bundle",
    "principal_u1_bundle", "principal_on_bundle",
    "principal_gln_bundle", "principal_spinn_bundle",
    "principal_sun_bundle",
})

TRIVIAL_BUNDLE_TAGS: frozenset[str] = frozenset({
    "trivial_bundle", "product_bundle",
    "parallelizable", "trivial_vector_bundle",
    "contractible_base_bundle",
})

NOWHERE_ZERO_SECTION_TAGS: frozenset[str] = frozenset({
    "parallelizable", "has_nowhere_zero_section",
    "trivial_bundle", "product_bundle",
    "sphere_s1_tangent", "sphere_s3_tangent", "sphere_s7_tangent",
    "odd_sphere_tangent",
    "nonzero_euler_class_zero",
})

ORIENTABLE_BUNDLE_TAGS: frozenset[str] = frozenset({
    "orientable_bundle", "oriented_bundle",
    "complex_vector_bundle",
    "trivial_bundle",
    "w1_zero",
    "tangent_bundle_orientable_manifold",
    "sphere_tangent_bundle",
    "real_vector_bundle_orientable",
})

NOT_TRIVIAL_TAGS: frozenset[str] = frozenset({
    "nontrivial_bundle", "non_trivial_bundle",
    "mobius_band",
    "hopf_bundle",
    "tautological_bundle",
    "non_parallelizable_tangent",
    "w1_nonzero",
})

NOT_NOWHERE_ZERO_SECTION_TAGS: frozenset[str] = frozenset({
    "no_nowhere_zero_section",
    "even_sphere_tangent",
    "sphere_s2_tangent", "sphere_s4_tangent",
    "nonzero_euler_class",
    "mobius_band",
    "w1_nonzero",
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

def get_named_fiber_bundle_profiles() -> tuple[FiberBundleProfile, ...]:
    """Return the registry of canonical fiber bundle examples."""
    return (
        FiberBundleProfile(
            key="product_bundle",
            display_name="M x R^k -> M (trivial vector bundle)",
            bundle_type="trivial",
            is_locally_trivial=True,
            is_vector_bundle=True,
            is_principal=False,
            is_trivial=True,
            has_nowhere_zero_section=True,
            is_orientable=True,
            presentation_layer="main_text",
            focus=(
                "A trivial (product) vector bundle over a base space M is the direct "
                "product E = M x R^k with projection pi(m, v) = m. Every trivial bundle "
                "has a nowhere-zero global section (e.g., sigma(m) = (m, e_1) where "
                "e_1 is the first standard basis vector). A vector bundle E -> B is "
                "trivial iff it admits k linearly independent global sections "
                "(k = fibre dimension). Trivial bundles arise over contractible bases "
                "(homotopy lifting property: any bundle over a contractible space is "
                "trivial), over parallelizable manifolds (TS^1 = S^1 x R, "
                "TS^3 = S^3 x R^3, TS^7 = S^7 x R^7), and as pullbacks along "
                "null-homotopic maps. The trivial bundle is the identity element in "
                "the monoid of isomorphism classes of vector bundles under direct sum."
            ),
            chapter_targets=("7", "25", "49"),
        ),
        FiberBundleProfile(
            key="mobius_band",
            display_name="gamma^1(S^1) — Mobius band (non-trivial line bundle over S^1)",
            bundle_type="line_bundle",
            is_locally_trivial=True,
            is_vector_bundle=True,
            is_principal=False,
            is_trivial=False,
            has_nowhere_zero_section=False,
            is_orientable=False,
            presentation_layer="main_text",
            focus=(
                "The Mobius band is the total space of the unique non-trivial real "
                "line bundle gamma^1 over S^1. It is constructed by identifying the "
                "two ends of [0,1] x R with a twist (x,t) ~ (1-x,-t). "
                "It is locally trivial (over each of two open arcs covering S^1, "
                "the bundle is a product), but globally non-trivial. "
                "The Mobius band has NO nowhere-zero global section: a non-vanishing "
                "section s: S^1 -> R\\ {0} would be a continuous map that is positive "
                "at some point but reverses sign after traversing the full circle — "
                "contradicting the intermediate value theorem. This is captured by "
                "the non-vanishing first Stiefel-Whitney class w_1(gamma^1) in H^1(S^1;Z/2) ≅ Z/2. "
                "The Mobius band is non-orientable: its total space is a non-orientable surface "
                "with boundary (homeomorphic to RP^2 minus an open disc if compactified)."
            ),
            chapter_targets=("7", "25"),
        ),
        FiberBundleProfile(
            key="tangent_bundle_even_sphere",
            display_name="TS^{2n} — tangent bundle of an even-dimensional sphere",
            bundle_type="tangent_bundle",
            is_locally_trivial=True,
            is_vector_bundle=True,
            is_principal=False,
            is_trivial=False,
            has_nowhere_zero_section=False,
            is_orientable=True,
            presentation_layer="main_text",
            focus=(
                "The tangent bundle TS^{2n} of an even-dimensional sphere S^{2n} is a "
                "rank-2n real orientable vector bundle over S^{2n}. "
                "The hairy ball theorem states that TS^{2n} has NO nowhere-zero global "
                "section: every continuous tangent vector field on S^{2n} must vanish "
                "at some point. Proof via Poincare-Hopf: the Euler characteristic "
                "chi(S^{2n}) = 2 != 0 equals the sum of indices of any vector field "
                "with isolated zeros, so the field cannot be everywhere non-zero. "
                "Equivalently, the Euler class e(TS^{2n}) in H^{2n}(S^{2n};Z) ≅ Z "
                "equals chi(S^{2n}) = 2 != 0, obstructing a nowhere-zero section. "
                "TS^{2n} is orientable (spheres are orientable manifolds) but "
                "non-trivial for n >= 1 except when 2n in {1, 3, 7} — since only "
                "S^1, S^3, S^7 are parallelizable (Adams' theorem). For n = 1 "
                "(S^2), the hairy ball theorem has the famous physical interpretation: "
                "there is no continuous wind pattern on Earth without a cyclone."
            ),
            chapter_targets=("7", "25", "49"),
        ),
        FiberBundleProfile(
            key="hopf_fibration",
            display_name="eta: S^3 -> S^2 — Hopf fibration",
            bundle_type="principal_bundle",
            is_locally_trivial=True,
            is_vector_bundle=False,
            is_principal=True,
            is_trivial=False,
            has_nowhere_zero_section=False,
            is_orientable=True,
            presentation_layer="main_text",
            focus=(
                "The Hopf fibration eta: S^3 -> S^2 is the map sending a unit "
                "quaternion q in S^3 subset H to q * i * q^{-1} in S^2 = Im(H) ∩ S^3. "
                "Equivalently, viewing S^3 subset C^2 and S^2 = CP^1, it sends "
                "(z_0, z_1) to the complex line [z_0 : z_1]. The fibre over each "
                "point is a great circle S^1, and eta is a principal U(1)-bundle. "
                "The Hopf fibration is NON-TRIVIAL: pi_3(S^2) ≅ Z is generated by [eta], "
                "with Hopf invariant H(eta) = 1. The associated long exact sequence "
                "of homotopy groups: ... -> pi_3(S^1) -> pi_3(S^3) -> pi_3(S^2) -> pi_2(S^1) -> ... "
                "gives pi_3(S^2) ≅ Z via the connecting homomorphism. "
                "The Hopf fibration is the prototypical example of a non-trivial "
                "circle bundle and appears in the classification of line bundles over S^2 "
                "(which correspond to Z = H^2(S^2;Z) via the first Chern class c_1)."
            ),
            chapter_targets=("7", "25", "49"),
        ),
        FiberBundleProfile(
            key="frame_bundle",
            display_name="GL(M) — frame bundle of a smooth manifold",
            bundle_type="principal_bundle",
            is_locally_trivial=True,
            is_vector_bundle=False,
            is_principal=True,
            is_trivial=False,
            has_nowhere_zero_section=False,
            is_orientable=True,
            presentation_layer="selected_block",
            focus=(
                "The frame bundle GL(M) of a smooth n-manifold M is the principal "
                "GL(n,R)-bundle whose fibre over x in M is the set of all ordered "
                "bases (frames) of the tangent space T_x M. It is a locally trivial "
                "bundle: a local trivialisation is equivalent to a local coordinate "
                "chart. The frame bundle encodes all tensor bundles over M: "
                "an associated bundle construction with any GL(n,R)-representation "
                "recovers the corresponding tensor bundle. "
                "Reduction of structure group: the frame bundle admits a reduction to "
                "O(n) subset GL(n,R) iff M admits a Riemannian metric — which always "
                "exists on paracompact manifolds (partition of unity). "
                "A reduction to SO(n) iff M is orientable. "
                "A reduction to Spin(n) iff the second Stiefel-Whitney class w_2(TM) = 0 "
                "(spin structure exists). The frame bundle has no canonical global "
                "section: a global section would be a nowhere-zero frame field, "
                "i.e., M would be parallelizable."
            ),
            chapter_targets=("7", "25", "49"),
        ),
        FiberBundleProfile(
            key="tautological_bundle",
            display_name="gamma^k_n -> Gr(k,n) — tautological bundle over Grassmannian",
            bundle_type="classifying",
            is_locally_trivial=True,
            is_vector_bundle=True,
            is_principal=False,
            is_trivial=False,
            has_nowhere_zero_section=False,
            is_orientable=False,
            presentation_layer="selected_block",
            focus=(
                "The tautological (canonical) k-plane bundle gamma^k_n over the "
                "Grassmannian Gr(k,n) = Gr(k, R^n) has fibre at [V] in Gr(k,n) equal "
                "to the k-dimensional subspace V subset R^n itself. "
                "It is a rank-k real vector bundle, locally trivial (Grassmannians "
                "admit local trivialisations via complementary subspaces). "
                "The tautological bundle is NON-TRIVIAL for k, n >= 1 with n > k: "
                "its Stiefel-Whitney classes are non-trivial in H^*(Gr(k,n);Z/2). "
                "Universal property: every rank-k vector bundle E -> X over a "
                "paracompact space X is isomorphic to f*(gamma^k_n) for some "
                "classifying map f: X -> Gr(k,n), for n sufficiently large. "
                "In the limit n -> inf, the universal bundle gamma^k over BO(k) = Gr(k,inf) "
                "classifies all rank-k real vector bundles up to isomorphism: "
                "Vect_k(X) ≅ [X, BO(k)] for paracompact X. "
                "The tautological line bundle over RP^n (k=1, F=R) has w_1 != 0 "
                "(non-orientable), while over CP^n (k=1, F=C) it is the "
                "hyperplane bundle with first Chern class c_1 = -1 in H^2(CP^n;Z) ≅ Z."
            ),
            chapter_targets=("7", "25", "49"),
        ),
    )


def fiber_bundle_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_fiber_bundle_profiles()))


def fiber_bundle_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_fiber_bundle_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def fiber_bundle_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from bundle_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_fiber_bundle_profiles():
        index.setdefault(p.bundle_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_locally_trivial(space: Any) -> Result:
    """Check whether space carries a locally trivial fiber bundle structure.

    A map pi: E -> B is a fiber bundle with fiber F if every point b in B has
    a neighbourhood U and a homeomorphism phi: pi^{-1}(U) -> U x F with
    pi = proj_U o phi. All vector bundles and principal G-bundles are locally trivial.
    Key facts:
    - Every vector bundle is locally trivial by definition.
    - Every principal G-bundle is locally trivial.
    - Locally trivial does NOT imply globally trivial (Mobius band, Hopf fibration).
    - A fiber bundle over a contractible base IS trivial (homotopy lifting).

    Decision layers
    ---------------
    1. Explicit fiber_bundle / locally_trivial tag -> true.
    2. Vector bundle tag (rank-n, line bundle, tangent/cotangent) -> true.
    3. Principal bundle tag -> true.
    4. Trivial / product bundle -> true.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"fiber_bundle", "locally_trivial"}):
        witness = next(t for t in tags if t in {"fiber_bundle", "locally_trivial"})
        return Result.true(
            mode="theorem",
            value="locally_trivial",
            justification=[
                f"Tag {witness!r}: the bundle is locally trivial — every point of the "
                "base has a neighbourhood over which the bundle is homeomorphic to a "
                "product U x F.",
            ],
            metadata={**base, "criterion": "explicit_locally_trivial", "witness": witness},
        )

    if _matches_any(tags, VECTOR_BUNDLE_TAGS):
        witness = next(t for t in tags if t in VECTOR_BUNDLE_TAGS)
        return Result.true(
            mode="theorem",
            value="locally_trivial",
            justification=[
                f"Tag {witness!r}: vector bundles are locally trivial by definition — "
                "transition functions in GL(n,R) are defined on intersections of "
                "trivialising neighbourhoods, ensuring local product structure.",
            ],
            metadata={**base, "criterion": "vector_bundle_locally_trivial", "witness": witness},
        )

    if _matches_any(tags, PRINCIPAL_BUNDLE_TAGS):
        witness = next(t for t in tags if t in PRINCIPAL_BUNDLE_TAGS)
        return Result.true(
            mode="theorem",
            value="locally_trivial",
            justification=[
                f"Tag {witness!r}: principal G-bundles are locally trivial by definition — "
                "local sections exist over trivialising neighbourhoods, giving "
                "homeomorphisms pi^{{-1}}(U) ≅ U x G.",
            ],
            metadata={**base, "criterion": "principal_bundle_locally_trivial",
                       "witness": witness},
        )

    if _matches_any(tags, TRIVIAL_BUNDLE_TAGS):
        witness = next(t for t in tags if t in TRIVIAL_BUNDLE_TAGS)
        return Result.true(
            mode="theorem",
            value="locally_trivial",
            justification=[
                f"Tag {witness!r}: a trivial (product) bundle E = B x F is locally "
                "trivial with a single global trivialisation.",
            ],
            metadata={**base, "criterion": "trivial_bundle_locally_trivial", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="locally_trivial",
        justification=[
            "Insufficient tags to determine local triviality. "
            "Supply tags such as 'fiber_bundle', 'vector_bundle', 'principal_bundle', "
            "'line_bundle', 'tangent_bundle', or 'trivial_bundle'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_vector_bundle(space: Any) -> Result:
    """Check whether space is a vector bundle.

    A vector bundle pi: E -> B of rank k is a fiber bundle with fiber R^k (or C^k)
    such that each fibre E_b = pi^{-1}(b) is a k-dimensional vector space and the
    transition functions lie in GL(k,R) (or GL(k,C)). Key facts:
    - The zero section sigma_0: B -> E (b |-> 0_b) exists for every vector bundle.
    - A nowhere-zero section exists iff the bundle has Euler class zero (rank = dim(B))
      or is of lower rank than the base dimension.
    - The tangent and cotangent bundles of any smooth manifold are vector bundles.
    - Complex vector bundles have canonical orientations (Chern classes live in H^{2k}).
    - Principal G-bundles are NOT vector bundles in general (Hopf fibration: G = U(1)).

    Decision layers
    ---------------
    1. Explicit vector_bundle / line_bundle / rank_n_bundle tag -> true.
    2. Tangent / cotangent / normal / tautological bundle -> true.
    3. Mobius band (line bundle, but check separately) -> true.
    4. Principal bundle (not a vector bundle unless G = GL(n)) -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"vector_bundle", "real_vector_bundle",
                            "complex_vector_bundle", "line_bundle",
                            "rank_n_bundle"}):
        witness = next(t for t in tags if t in {"vector_bundle", "real_vector_bundle",
                                                   "complex_vector_bundle", "line_bundle",
                                                   "rank_n_bundle"})
        return Result.true(
            mode="theorem",
            value="vector_bundle",
            justification=[
                f"Tag {witness!r}: the bundle is a vector bundle — each fibre is a "
                "vector space and transition functions lie in GL(n,R) or GL(n,C). "
                "The zero section always provides a canonical global section.",
            ],
            metadata={**base, "criterion": "explicit_vector_bundle", "witness": witness},
        )

    if _matches_any(tags, {"tangent_bundle", "cotangent_bundle",
                            "normal_bundle", "tautological_bundle",
                            "mobius_band"}):
        witness = next(t for t in tags if t in {"tangent_bundle", "cotangent_bundle",
                                                   "normal_bundle", "tautological_bundle",
                                                   "mobius_band"})
        return Result.true(
            mode="theorem",
            value="vector_bundle",
            justification=[
                f"Tag {witness!r}: tangent, cotangent, normal, tautological bundles, "
                "and the Mobius band are all vector bundles. Their fibres are vector "
                "spaces with smooth (or continuous) linear transition functions.",
            ],
            metadata={**base, "criterion": "canonical_vector_bundle", "witness": witness},
        )

    if _matches_any(tags, {"hopf_bundle", "principal_bundle",
                            "principal_g_bundle", "principal_u1_bundle",
                            "frame_bundle", "principal_on_bundle"}):
        blocking = next(t for t in tags if t in {"hopf_bundle", "principal_bundle",
                                                    "principal_g_bundle",
                                                    "principal_u1_bundle",
                                                    "frame_bundle",
                                                    "principal_on_bundle"})
        return Result.false(
            mode="theorem",
            value="vector_bundle",
            justification=[
                f"Tag {blocking!r}: a principal G-bundle is not a vector bundle in "
                "general — the fibre G acts on itself by group multiplication, not by "
                "linear transformations. The Hopf fibration S^3 -> S^2 has fibre S^1 = U(1), "
                "which is a Lie group but not a vector space.",
            ],
            metadata={**base, "criterion": "principal_not_vector"},
        )

    return Result.unknown(
        mode="symbolic",
        value="vector_bundle",
        justification=[
            "Insufficient tags to determine vector bundle status. "
            "Supply tags such as 'vector_bundle', 'line_bundle', 'tangent_bundle', "
            "'cotangent_bundle', 'mobius_band', 'principal_bundle', or 'hopf_bundle'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_trivial_bundle(space: Any) -> Result:
    """Check whether the bundle is globally trivial (isomorphic to a product).

    A bundle pi: E -> B is trivial if there exists a homeomorphism E ≅ B x F
    over B. Key facts:
    - Any bundle over a contractible base is trivial (homotopy lifting property).
    - A rank-k vector bundle over B is trivial iff it admits k everywhere-linearly-
      independent global sections (a global frame).
    - S^n is parallelizable (TS^n trivial) only for n = 1, 3, 7 (Adams' theorem).
    - The Mobius band, Hopf fibration, and tautological bundles are non-trivial.
    - Classification: principal G-bundles over X are classified by [X, BG]; a bundle
      is trivial iff the classifying map f: X -> BG is null-homotopic.

    Decision layers
    ---------------
    1. Explicit trivial / product bundle tag -> true.
    2. Contractible base (homotopy lifting) -> true.
    3. Parallelizable manifold tangent bundle -> true.
    4. Mobius band / Hopf bundle / tautological bundle -> false.
    5. Non-parallelizable manifold tangent bundle -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, TRIVIAL_BUNDLE_TAGS):
        witness = next(t for t in tags if t in TRIVIAL_BUNDLE_TAGS)
        return Result.true(
            mode="theorem",
            value="trivial_bundle",
            justification=[
                f"Tag {witness!r}: the bundle is globally trivial — it admits a "
                "homeomorphism E ≅ B x F over B. Trivial bundles arise over contractible "
                "bases or from parallelizable manifolds (TS^1, TS^3, TS^7).",
            ],
            metadata={**base, "criterion": "explicit_trivial", "witness": witness},
        )

    if _matches_any(tags, {"contractible_base"}):
        return Result.true(
            mode="theorem",
            value="trivial_bundle",
            justification=[
                "Tag 'contractible_base': any fiber bundle over a contractible space "
                "is trivial. The homotopy lifting property implies that the classifying "
                "map f: B -> BG is null-homotopic (B is contractible), so the bundle "
                "pulls back from the trivial bundle over a point.",
            ],
            metadata={**base, "criterion": "contractible_base_trivial"},
        )

    if _matches_any(tags, NOT_TRIVIAL_TAGS):
        blocking = next(t for t in tags if t in NOT_TRIVIAL_TAGS)
        return Result.false(
            mode="theorem",
            value="trivial_bundle",
            justification=[
                f"Tag {blocking!r}: the bundle is non-trivial. The Mobius band has "
                "w_1 != 0 (non-orientable, first Stiefel-Whitney class obstructs "
                "trivialisation). The Hopf fibration generates pi_3(S^2) ≅ Z. "
                "Tautological bundles are non-trivial by the universal property of "
                "classifying spaces.",
            ],
            metadata={**base, "criterion": "nontrivial_tag", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="trivial_bundle",
        justification=[
            "Insufficient tags to determine global triviality. "
            "Supply tags such as 'trivial_bundle', 'parallelizable', 'contractible_base', "
            "'mobius_band', 'hopf_bundle', 'tautological_bundle', or 'nontrivial_bundle'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_nowhere_zero_section(space: Any) -> Result:
    """Check whether the vector bundle has a nowhere-zero global section.

    A nowhere-zero section of a vector bundle E -> B is a continuous map
    s: B -> E with pi o s = id_B and s(b) != 0_b for all b in B. Key facts:
    - The zero section always exists but is NOT nowhere-zero.
    - Hairy ball theorem: TS^{2n} has no nowhere-zero section (chi(S^{2n}) = 2 != 0).
    - TS^{2n-1} has a nowhere-zero section (chi(S^{2n-1}) = 0).
    - The Mobius band (line bundle over S^1) has no nowhere-zero section (w_1 != 0).
    - Trivial bundles always have nowhere-zero sections (constant sections).
    - Poincare-Hopf: a vector field on a compact manifold has a zero iff chi(M) != 0.
    - A rank-k vector bundle over an n-manifold (k > n) always has a nowhere-zero
      section (by dimensional reasons; general position argument).

    Decision layers
    ---------------
    1. Trivial / product bundle / parallelizable -> true.
    2. Odd sphere tangent bundle (chi = 0 -> nowhere-zero field) -> true.
    3. Explicit nowhere-zero section tag -> true.
    4. Even sphere tangent bundle (hairy ball theorem) -> false.
    5. Mobius band / non-orientable line bundle (w_1 != 0) -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, TRIVIAL_BUNDLE_TAGS | {"parallelizable"}):
        witness = next(t for t in tags if t in TRIVIAL_BUNDLE_TAGS | {"parallelizable"})
        return Result.true(
            mode="theorem",
            value="nowhere_zero_section",
            justification=[
                f"Tag {witness!r}: trivial and parallelizable bundles have nowhere-zero "
                "global sections. A trivial bundle E = B x R^k admits the section "
                "s(b) = (b, e_1) (first standard basis vector, everywhere non-zero). "
                "S^1, S^3, S^7 are parallelizable: their tangent bundles are trivial.",
            ],
            metadata={**base, "criterion": "trivial_has_section", "witness": witness},
        )

    if _matches_any(tags, {"odd_sphere_tangent", "sphere_s1_tangent",
                            "sphere_s3_tangent", "sphere_s7_tangent",
                            "nonzero_euler_class_zero"}):
        witness = next(t for t in tags if t in {"odd_sphere_tangent",
                                                   "sphere_s1_tangent",
                                                   "sphere_s3_tangent",
                                                   "sphere_s7_tangent",
                                                   "nonzero_euler_class_zero"})
        return Result.true(
            mode="theorem",
            value="nowhere_zero_section",
            justification=[
                f"Tag {witness!r}: odd-dimensional sphere tangent bundle. "
                "chi(S^{{2n-1}}) = 0, so by the Poincare-Hopf theorem, a vector field "
                "on S^{{2n-1}} need not vanish. Concretely: v(x_1,...,x_{2n}) = "
                "(-x_2, x_1, -x_4, x_3, ...) is a nowhere-zero tangent vector field.",
            ],
            metadata={**base, "criterion": "odd_sphere_section", "witness": witness},
        )

    if _matches_any(tags, NOT_NOWHERE_ZERO_SECTION_TAGS):
        blocking = next(t for t in tags if t in NOT_NOWHERE_ZERO_SECTION_TAGS)
        return Result.false(
            mode="theorem",
            value="nowhere_zero_section",
            justification=[
                f"Tag {blocking!r}: no nowhere-zero global section exists. "
                "Hairy ball theorem: every tangent vector field on S^{{2n}} must vanish "
                "somewhere (chi(S^{{2n}}) = 2 != 0, Poincare-Hopf). "
                "For the Mobius band: a non-vanishing section s: S^1 -> R\\{{0}} would "
                "change sign after one loop — impossible by the intermediate value theorem.",
            ],
            metadata={**base, "criterion": "no_section", "witness": blocking},
        )

    return Result.unknown(
        mode="symbolic",
        value="nowhere_zero_section",
        justification=[
            "Insufficient tags to determine existence of a nowhere-zero section. "
            "Supply tags such as 'trivial_bundle', 'parallelizable', 'odd_sphere_tangent', "
            "'even_sphere_tangent', 'mobius_band', or 'no_nowhere_zero_section'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_orientable_bundle(space: Any) -> Result:
    """Check whether the vector bundle is orientable.

    A real vector bundle pi: E -> B of rank k is orientable if its first
    Stiefel-Whitney class w_1(E) in H^1(B; Z/2) vanishes, equivalently if
    the structure group reduces from GL(k,R) to GL^+(k,R) (matrices with
    positive determinant). Key facts:
    - Every complex vector bundle is orientable (complex structure -> canonical orientation).
    - Every trivial real bundle is orientable (constant positive frame).
    - The tangent bundle TM is orientable iff M is an orientable manifold.
    - The Mobius band (line bundle over S^1) is NOT orientable: w_1 != 0.
    - Tautological real line bundle over RP^n is NOT orientable.
    - The Hopf bundle (S^3 -> S^2, principal U(1)-bundle) is not a vector bundle
      (principal bundles need not carry a natural orientation notion).

    Decision layers
    ---------------
    1. Complex vector bundle (canonical orientation from complex structure) -> true.
    2. Trivial / product real bundle -> true.
    3. Tangent bundle of orientable manifold -> true.
    4. Explicit orientable bundle tag -> true.
    5. Mobius band / w_1 != 0 tag -> false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"complex_vector_bundle"}):
        return Result.true(
            mode="theorem",
            value="orientable_bundle",
            justification=[
                "Tag 'complex_vector_bundle': every complex vector bundle is orientable. "
                "The complex structure provides a canonical orientation on each fibre: "
                "the transition functions lie in GL(n,C) subset GL(2n,R)^+, "
                "so the real realisation has structure group reducing to GL^+(2n,R).",
            ],
            metadata={**base, "criterion": "complex_bundle_orientable"},
        )

    if _matches_any(tags, TRIVIAL_BUNDLE_TAGS):
        witness = next(t for t in tags if t in TRIVIAL_BUNDLE_TAGS)
        return Result.true(
            mode="theorem",
            value="orientable_bundle",
            justification=[
                f"Tag {witness!r}: trivial bundles are orientable. The constant "
                "positive frame (e_1,...,e_k) provides a global orientation.",
            ],
            metadata={**base, "criterion": "trivial_orientable", "witness": witness},
        )

    if _matches_any(tags, ORIENTABLE_BUNDLE_TAGS):
        witness = next(t for t in tags if t in ORIENTABLE_BUNDLE_TAGS)
        return Result.true(
            mode="theorem",
            value="orientable_bundle",
            justification=[
                f"Tag {witness!r}: the vector bundle is orientable — its first "
                "Stiefel-Whitney class w_1 vanishes. The structure group reduces "
                "from GL(k,R) to GL^+(k,R).",
            ],
            metadata={**base, "criterion": "orientable_tag", "witness": witness},
        )

    if _matches_any(tags, {"mobius_band", "w1_nonzero",
                            "non_orientable_bundle", "tautological_real_line"}):
        blocking = next(t for t in tags if t in {"mobius_band", "w1_nonzero",
                                                    "non_orientable_bundle",
                                                    "tautological_real_line"})
        return Result.false(
            mode="theorem",
            value="orientable_bundle",
            justification=[
                f"Tag {blocking!r}: the bundle is NOT orientable — its first "
                "Stiefel-Whitney class w_1 in H^1(B;Z/2) is non-zero. "
                "The Mobius band is the canonical non-orientable line bundle over S^1: "
                "after a full loop, the fibre orientation is reversed.",
            ],
            metadata={**base, "criterion": "non_orientable_w1"},
        )

    return Result.unknown(
        mode="symbolic",
        value="orientable_bundle",
        justification=[
            "Insufficient tags to determine bundle orientability. "
            "Supply tags such as 'complex_vector_bundle', 'trivial_bundle', "
            "'orientable_bundle', 'tangent_bundle_orientable_manifold', "
            "'mobius_band', or 'w1_nonzero'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_bundle(space: Any) -> dict[str, Any]:
    """Classify the fiber bundle properties of space.

    Keys
    ----
    bundle_class : str
        One of ``"trivial"``, ``"vector_bundle"``, ``"principal"``,
        ``"locally_trivial"``, ``"unknown"``.
    is_locally_trivial : Result
    is_vector_bundle : Result
    is_trivial_bundle : Result
    has_nowhere_zero_section : Result
    is_orientable_bundle : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    loc_r = is_locally_trivial(space)
    vec_r = is_vector_bundle(space)
    triv_r = is_trivial_bundle(space)
    sec_r = has_nowhere_zero_section(space)
    ori_r = is_orientable_bundle(space)

    if triv_r.is_true:
        bundle_class = "trivial"
    elif vec_r.is_true:
        bundle_class = "vector_bundle"
    elif _matches_any(tags, PRINCIPAL_BUNDLE_TAGS):
        bundle_class = "principal"
    elif loc_r.is_true:
        bundle_class = "locally_trivial"
    else:
        bundle_class = "unknown"

    key_properties: list[str] = []
    if loc_r.is_true:
        key_properties.append("locally_trivial")
    if vec_r.is_true:
        key_properties.append("vector_bundle")
    if triv_r.is_true:
        key_properties.append("trivial")
    if triv_r.is_false:
        key_properties.append("non_trivial")
    if sec_r.is_true:
        key_properties.append("nowhere_zero_section")
    if sec_r.is_false:
        key_properties.append("no_nowhere_zero_section")
    if ori_r.is_true:
        key_properties.append("orientable")
    if ori_r.is_false:
        key_properties.append("non_orientable")
    if _matches_any(tags, PRINCIPAL_BUNDLE_TAGS):
        key_properties.append("principal_bundle")

    return {
        "bundle_class": bundle_class,
        "is_locally_trivial": loc_r,
        "is_vector_bundle": vec_r,
        "is_trivial_bundle": triv_r,
        "has_nowhere_zero_section": sec_r,
        "is_orientable_bundle": ori_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def fiber_bundle_profile(space: Any) -> dict[str, Any]:
    """Full fiber bundle profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_bundle`.
    named_profiles : tuple[FiberBundleProfile, ...]
        Registry of canonical fiber bundle examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_bundle(space),
        "named_profiles": get_named_fiber_bundle_profiles(),
        "layer_summary": fiber_bundle_layer_summary(),
    }


__all__ = [
    "FiberBundleProfile",
    "LOCALLY_TRIVIAL_TAGS",
    "VECTOR_BUNDLE_TAGS",
    "PRINCIPAL_BUNDLE_TAGS",
    "TRIVIAL_BUNDLE_TAGS",
    "NOWHERE_ZERO_SECTION_TAGS",
    "ORIENTABLE_BUNDLE_TAGS",
    "NOT_TRIVIAL_TAGS",
    "NOT_NOWHERE_ZERO_SECTION_TAGS",
    "get_named_fiber_bundle_profiles",
    "fiber_bundle_layer_summary",
    "fiber_bundle_chapter_index",
    "fiber_bundle_type_index",
    "is_locally_trivial",
    "is_vector_bundle",
    "is_trivial_bundle",
    "has_nowhere_zero_section",
    "is_orientable_bundle",
    "classify_bundle",
    "fiber_bundle_profile",
]
