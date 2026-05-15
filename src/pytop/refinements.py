"""
refinements.py — Cilt III v0.1.63
===================================
Durable API for cover refinement language.

Concepts covered
----------------
- Locally finite covers / families
- Refinements (open refinements, closed refinements)
- Star-refinements (barycentric refinements)
- Shrinkings of covers
- σ-locally finite bases (Nagata-Smirnov metrization link)

Public surface
--------------
is_locally_finite_cover(space)     → Result
refinement_profile(space)          → dict
analyze_cover_refinement(space)    → Result
RefinementError                    → exception class
"""

from __future__ import annotations
from typing import Any, Dict, List

from .result import Result

try:
    from .finite_spaces import FiniteTopologicalSpace
except Exception:  # pragma: no cover
    FiniteTopologicalSpace = None  # type: ignore


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class RefinementError(Exception):
    """Raised when a cover-refinement operation cannot be completed."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _representation_of(space: Any) -> str:
    if FiniteTopologicalSpace is not None and isinstance(space, FiniteTopologicalSpace):
        return "finite"
    metadata = getattr(space, "metadata", {}) or {}
    if isinstance(metadata, dict) and "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(space, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _tags_of(space: Any) -> frozenset:
    metadata = getattr(space, "metadata", {}) or {}
    raw = metadata.get("tags", []) if isinstance(metadata, dict) else []
    if not raw:
        raw = getattr(space, "tags", []) or []
    return frozenset(str(t).lower().strip() for t in raw)


def _carrier_size(space: Any) -> int | None:
    if FiniteTopologicalSpace is not None and isinstance(space, FiniteTopologicalSpace):
        return len(space.carrier)
    carrier = getattr(space, "carrier", None)
    if carrier is not None:
        try:
            return len(carrier)
        except TypeError:
            pass
    return None


# ---------------------------------------------------------------------------
# is_locally_finite_cover
# ---------------------------------------------------------------------------

def is_locally_finite_cover(space: Any) -> Result:
    """
    Determine whether *space* admits locally finite open covers for every
    open cover (i.e. whether it is paracompact).

    This is the *cover-language* restatement of paracompactness:
      X is paracompact  ⟺  every open cover has a locally finite open refinement.

    Decision chain
    --------------
    1. Negative tags → false
    2. Finite space → true (exact): all covers are finite, hence locally finite
    3. Metrizable → true (Stone's theorem)
    4. Compact → true
    5. Regular + Lindelöf → true (Michael)
    6. Paracompact tag → true
    7. Otherwise → unknown
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    if "not_paracompact" in tags or "not_locally_finite_cover" in tags:
        return Result.false(
            mode="theorem",
            value="no_locally_finite_refinement",
            justification=[
                "Space tagged as not admitting locally finite refinements / not paracompact."
            ],
            metadata={"version": "0.1.63", "criterion": "tag"},
        )

    if rep == "finite":
        n = _carrier_size(space)
        return Result.true(
            mode="exact",
            value="locally_finite_cover_exists",
            justification=[
                f"Finite space (|X|={n}): every open cover is finite and "
                "hence locally finite — every point has a neighbourhood meeting "
                "only finitely many cover members."
            ],
            metadata={"version": "0.1.63", "carrier_size": n, "criterion": "finite"},
        )

    if "metrizable" in tags or "metric" in tags:
        return Result.true(
            mode="theorem",
            value="locally_finite_cover_exists",
            justification=[
                "Metrizable ⟹ paracompact (Stone 1948) ⟹ every open cover "
                "has a locally finite open refinement."
            ],
            metadata={"version": "0.1.63", "criterion": "stone_theorem"},
        )

    if "compact" in tags or "compact_hausdorff" in tags:
        return Result.true(
            mode="theorem",
            value="locally_finite_cover_exists",
            justification=[
                "Compact ⟹ paracompact ⟹ every open cover has a locally finite refinement."
            ],
            metadata={"version": "0.1.63", "criterion": "compact"},
        )

    has_regular = any(t in tags for t in ("regular","t3","regular_t1","t3_5",
                                           "tychonoff","normal","hausdorff","t2"))
    has_lindelof = any(t in tags for t in ("lindelof","second_countable",
                                            "separable_metrizable",
                                            "second_countable_hausdorff"))
    if has_regular and has_lindelof:
        return Result.true(
            mode="theorem",
            value="locally_finite_cover_exists",
            justification=[
                "Regular + Lindelöf ⟹ paracompact (Michael) ⟹ "
                "every open cover has a locally finite open refinement."
            ],
            metadata={"version": "0.1.63", "criterion": "michael_theorem"},
        )

    if "paracompact" in tags:
        return Result.true(
            mode="theorem",
            value="locally_finite_cover_exists",
            justification=["Paracompact (by tag) ⟹ locally finite refinements exist."],
            metadata={"version": "0.1.63", "criterion": "tag"},
        )

    return Result.unknown(
        mode="symbolic",
        value="locally_finite_cover_unknown",
        justification=["Insufficient tags to determine existence of locally finite refinements."],
        metadata={"version": "0.1.63"},
    )


# ---------------------------------------------------------------------------
# refinement_profile
# ---------------------------------------------------------------------------

def refinement_profile(space: Any) -> Dict[str, Any]:
    """
    Full refinement language profile for *space*.

    Keys
    ----
    locally_finite_result   : Result
    star_refinement         : str   — star-refinements / full normality
    barycentric_refinement  : str   — barycentric = star-refinement
    shrinking               : str   — shrinkings of normal covers
    sigma_locally_finite    : str   — σ-locally finite bases (Nagata-Smirnov link)
    definitions             : dict  — formal definitions of key terms
    key_theorems            : list[str]
    representation          : str
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    lf_result = is_locally_finite_cover(space)

    # --- Star-refinement / full normality ---
    if rep == "finite":
        star_ref = (
            "yes — finite space is fully normal; "
            "every open cover has a star-refinement (take the cover itself)."
        )
    elif lf_result.status == "true" and (
        "hausdorff" in tags or "t2" in tags or "t3" in tags
        or "metrizable" in tags or "normal" in tags or "compact" in tags
    ):
        star_ref = (
            "yes — paracompact Hausdorff ⟺ fully normal: "
            "every open cover has an open star-refinement 𝒱 such that "
            "{St(x,𝒱) : x∈X} refines the original cover."
        )
    elif lf_result.status == "true":
        star_ref = (
            "paracompact (confirmed); Hausdorff not confirmed — "
            "full normality (star-refinement) requires paracompact + Hausdorff."
        )
    else:
        star_ref = "paracompactness not confirmed — star-refinement undetermined."

    # --- Barycentric refinement ---
    bary = (
        "A barycentric refinement of cover 𝒰 is an open cover 𝒱 such that "
        "for each V∈𝒱 there exists U∈𝒰 with St(V,𝒱) ⊆ U. "
        "Barycentric = star-refinement (the two notions coincide). "
        "A space is fully normal iff every open cover has a barycentric refinement."
    )

    # --- Shrinking ---
    if rep == "finite" or "normal" in tags or "metrizable" in tags or (
        lf_result.status == "true" and (
            "hausdorff" in tags or "t2" in tags or "t3" in tags or "compact" in tags
        )
    ):
        shrink = (
            "yes — normal spaces admit shrinkings: for every open cover {Uₐ} "
            "indexed by a well-order there is a closed cover {Fₐ} with Fₐ ⊆ Uₐ. "
            "Paracompact Hausdorff ⟹ normal ⟹ shrinking exists."
        )
    else:
        shrink = (
            "Shrinkings exist in normal spaces. "
            "Normality not confirmed from current tags."
        )

    # --- σ-locally finite ---
    if "metrizable" in tags or "metric" in tags:
        sigma_lf = (
            "yes — metrizable spaces have a σ-locally finite base (Nagata-Smirnov: "
            "a space is metrizable iff it has a σ-locally finite base). "
            "The base is a countable union ⋃ₙ Bₙ where each Bₙ is locally finite."
        )
    elif "second_countable" in tags or "separable_metrizable" in tags:
        sigma_lf = (
            "yes — second countable implies σ-locally finite base "
            "(countable base is trivially σ-locally finite)."
        )
    elif rep == "finite":
        sigma_lf = (
            "yes — finite space has a finite base, "
            "which is trivially σ-locally finite."
        )
    elif lf_result.status == "true":
        sigma_lf = (
            "paracompact spaces have σ-locally finite refinements; "
            "Nagata-Smirnov metrization requires additionally locally metrizable."
        )
    else:
        sigma_lf = "σ-locally finite base: undetermined from current tags."

    # --- Definitions ---
    definitions = {
        "locally_finite_family": (
            "A family {Aₐ} in X is locally finite if every x∈X has a neighbourhood "
            "U such that {α : U ∩ Aₐ ≠ ∅} is finite."
        ),
        "refinement": (
            "Cover 𝒱 refines cover 𝒰 if every V∈𝒱 is contained in some U∈𝒰."
        ),
        "star_of_point": (
            "St(x,𝒰) = ⋃{U∈𝒰 : x∈U} — the star of x with respect to cover 𝒰."
        ),
        "star_refinement": (
            "𝒱 is a star-refinement of 𝒰 if {St(x,𝒱) : x∈X} refines 𝒰."
        ),
        "sigma_locally_finite": (
            "A family is σ-locally finite if it is a countable union of locally finite families."
        ),
    }

    key_theorems = [
        "Paracompactness ⟺ every open cover has a locally finite open refinement.",
        "Full normality ⟺ every open cover has an open star-refinement.",
        "Paracompact Hausdorff ⟺ fully normal (A.H. Stone).",
        "Nagata-Smirnov: X metrizable ⟺ X has a σ-locally finite base.",
        "Smirnov: X metrizable ⟺ X paracompact + locally metrizable.",
        "Normal space ⟹ every open cover has a shrinking.",
    ]

    return {
        "locally_finite_result": lf_result,
        "star_refinement": star_ref,
        "barycentric_refinement": bary,
        "shrinking": shrink,
        "sigma_locally_finite": sigma_lf,
        "definitions": definitions,
        "key_theorems": key_theorems,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

def analyze_cover_refinement(space: Any) -> Result:
    """
    Single-call facade: full cover-refinement analysis for *space*.

    Returns a Result whose ``value`` is the ``refinement_profile`` dict.
    """
    rep = _representation_of(space)
    profile = refinement_profile(space)
    n = _carrier_size(space)
    lf = profile["locally_finite_result"]

    mode = "exact" if rep == "finite" else lf.mode

    justification = [
        f"Domain representation: {rep}",
        f"Locally finite refinements: {lf.status} ({lf.mode})",
        f"Star-refinement/full normality: {profile['star_refinement'][:70]}...",
        f"σ-locally finite base: {profile['sigma_locally_finite'][:70]}...",
    ]
    if rep == "finite" and n is not None:
        justification.insert(1, f"|X|={n}: finite ⟹ all covers are locally finite (exact).")

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": "0.1.63",
            "domain_representation": rep,
            "carrier_size": n,
            "locally_finite_status": lf.status,
            "locally_finite_criterion": lf.metadata.get("criterion"),
        },
    )
