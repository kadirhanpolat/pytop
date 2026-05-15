"""
compactness_variants.py — Cilt III v0.1.61
============================================
Durable API for advanced compactness variants.

Variants covered
----------------
- Countable compactness
- Sequential compactness
- Pseudocompactness
- ω-compactness (Lindelöf property)
- Compactness itself (for comparison)

Public surface
--------------
is_countably_compact(space)       → Result
is_sequentially_compact(space)    → Result
is_pseudocompact(space)           → Result
is_lindelof(space)                → Result
compactness_variant_profile(space) → dict
analyze_compactness_variants(space) → Result
CompactnessVariantError            → exception class
"""

from __future__ import annotations
from typing import Any, Dict

from .result import Result

try:
    from .finite_spaces import FiniteTopologicalSpace
except Exception:  # pragma: no cover
    FiniteTopologicalSpace = None  # type: ignore


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class CompactnessVariantError(Exception):
    """Raised when a compactness-variant operation cannot be completed."""


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
# Countable compactness
# ---------------------------------------------------------------------------

def is_countably_compact(space: Any) -> Result:
    """
    Determine whether *space* is countably compact.

    A space X is countably compact if every countable open cover has a
    finite subcover (equivalently: every infinite subset has an ω-accumulation
    point; equivalently: every sequence has a cluster point).

    Returns
    -------
    Result with status "true"/"false"/"unknown"
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    # Negative witnesses
    if "not_countably_compact" in tags:
        return Result.false(
            mode="theorem",
            value="not_countably_compact",
            justification=["Space tagged not_countably_compact."],
            metadata={"version": "0.1.61", "criterion": "tag"},
        )
    if "lindelof_not_compact" in tags or "sigma_compact_not_compact" in tags:
        return Result.false(
            mode="theorem",
            value="not_countably_compact",
            justification=["Lindelöf + not compact does not imply countably compact in general."],
            metadata={"version": "0.1.61", "criterion": "tag"},
        )

    # Finite spaces: always countably compact
    if rep == "finite":
        n = _carrier_size(space)
        return Result.true(
            mode="exact",
            value="countably_compact",
            justification=[
                f"Finite space (|X|={n}): every open cover is finite, "
                "so every countable subcover is already finite."
            ],
            metadata={"version": "0.1.61", "carrier_size": n, "criterion": "finite"},
        )

    # Positive tags
    if any(t in tags for t in ("compact", "sequentially_compact", "countably_compact")):
        witness = next(t for t in ("compact", "sequentially_compact", "countably_compact") if t in tags)
        return Result.true(
            mode="theorem",
            value="countably_compact",
            justification=[
                f"Space tagged '{witness}'; "
                "compactness and sequential compactness both imply countable compactness."
            ],
            metadata={"version": "0.1.61", "criterion": witness},
        )

    # Metric + sequentially compact ⟹ countably compact
    if "metric" in tags or "metrizable" in tags:
        if "sequentially_compact" in tags:
            return Result.true(
                mode="theorem",
                value="countably_compact",
                justification=[
                    "Metrizable + sequentially compact ⟹ countably compact "
                    "(in metric spaces the three notions coincide)."
                ],
                metadata={"version": "0.1.61", "criterion": "metrizable_seq_compact"},
            )

    return Result.unknown(
        mode="symbolic",
        value="countably_compact_unknown",
        justification=["Insufficient tags to determine countable compactness."],
        metadata={"version": "0.1.61"},
    )


# ---------------------------------------------------------------------------
# Sequential compactness
# ---------------------------------------------------------------------------

def is_sequentially_compact(space: Any) -> Result:
    """
    Determine whether *space* is sequentially compact.

    A space X is sequentially compact if every sequence in X has a
    convergent subsequence.
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    if "not_sequentially_compact" in tags:
        return Result.false(
            mode="theorem",
            value="not_sequentially_compact",
            justification=["Space tagged not_sequentially_compact."],
            metadata={"version": "0.1.61", "criterion": "tag"},
        )

    # Finite
    if rep == "finite":
        n = _carrier_size(space)
        return Result.true(
            mode="exact",
            value="sequentially_compact",
            justification=[
                f"Finite space (|X|={n}): every sequence is eventually in a "
                "finite set, so a constant subsequence converges."
            ],
            metadata={"version": "0.1.61", "carrier_size": n, "criterion": "finite"},
        )

    if "sequentially_compact" in tags:
        return Result.true(
            mode="theorem",
            value="sequentially_compact",
            justification=["Space explicitly tagged sequentially_compact."],
            metadata={"version": "0.1.61", "criterion": "tag"},
        )

    # Metrizable + compact ⟹ sequentially compact (Bolzano–Weierstrass)
    if ("metrizable" in tags or "metric" in tags) and (
        "compact" in tags or "compact_hausdorff" in tags
    ):
        return Result.true(
            mode="theorem",
            value="sequentially_compact",
            justification=[
                "Compact metrizable space is sequentially compact "
                "(Bolzano–Weierstrass / Heine–Borel)."
            ],
            metadata={"version": "0.1.61", "criterion": "compact_metrizable"},
        )

    # Warning: compact does NOT imply sequentially compact in general
    if "compact" in tags or "compact_hausdorff" in tags:
        return Result.unknown(
            mode="theorem",
            value="sequentially_compact_unknown",
            justification=[
                "Compact does not imply sequentially compact in general "
                "(e.g. β(ℕ) is compact but not sequentially compact). "
                "Need metrizable or explicit sequential tag."
            ],
            metadata={"version": "0.1.61", "criterion": "compact_no_seq"},
        )

    return Result.unknown(
        mode="symbolic",
        value="sequentially_compact_unknown",
        justification=["Insufficient tags to determine sequential compactness."],
        metadata={"version": "0.1.61"},
    )


# ---------------------------------------------------------------------------
# Pseudocompactness
# ---------------------------------------------------------------------------

def is_pseudocompact(space: Any) -> Result:
    """
    Determine whether *space* is pseudocompact.

    A Tychonoff space X is pseudocompact if every continuous real-valued
    function on X is bounded.  Equivalent (for Tychonoff spaces) to:
    every locally finite open cover is finite.
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    if "not_pseudocompact" in tags:
        return Result.false(
            mode="theorem",
            value="not_pseudocompact",
            justification=["Space tagged not_pseudocompact."],
            metadata={"version": "0.1.61", "criterion": "tag"},
        )

    # Finite: trivially pseudocompact
    if rep == "finite":
        n = _carrier_size(space)
        return Result.true(
            mode="exact",
            value="pseudocompact",
            justification=[
                f"Finite space (|X|={n}): every real-valued function on a "
                "finite space is bounded."
            ],
            metadata={"version": "0.1.61", "carrier_size": n, "criterion": "finite"},
        )

    # Countably compact Tychonoff ⟹ pseudocompact
    if ("countably_compact" in tags or "compact" in tags or "sequentially_compact" in tags):
        witness = next(
            t for t in ("compact", "countably_compact", "sequentially_compact") if t in tags
        )
        return Result.true(
            mode="theorem",
            value="pseudocompact",
            justification=[
                f"Space tagged '{witness}'; countable compactness implies pseudocompactness "
                "for Tychonoff spaces."
            ],
            metadata={"version": "0.1.61", "criterion": witness},
        )

    if "pseudocompact" in tags:
        return Result.true(
            mode="theorem",
            value="pseudocompact",
            justification=["Space explicitly tagged pseudocompact."],
            metadata={"version": "0.1.61", "criterion": "tag"},
        )

    # Non-compact metrizable Lindelöf: NOT pseudocompact
    if ("metrizable" in tags or "metric" in tags) and (
        "lindelof" in tags or "second_countable" in tags
    ) and "compact" not in tags:
        return Result.false(
            mode="theorem",
            value="not_pseudocompact",
            justification=[
                "Metrizable Lindelöf non-compact space is not pseudocompact "
                "(e.g. ℝ: f(x)=x is unbounded)."
            ],
            metadata={"version": "0.1.61", "criterion": "metrizable_lindelof_noncompact"},
        )

    return Result.unknown(
        mode="symbolic",
        value="pseudocompact_unknown",
        justification=["Insufficient tags to determine pseudocompactness."],
        metadata={"version": "0.1.61"},
    )


# ---------------------------------------------------------------------------
# Lindelöf property
# ---------------------------------------------------------------------------

def is_lindelof(space: Any) -> Result:
    """
    Determine whether *space* has the Lindelöf property.

    A space X is Lindelöf if every open cover has a countable subcover.
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    if "not_lindelof" in tags:
        return Result.false(
            mode="theorem",
            value="not_lindelof",
            justification=["Space tagged not_lindelof."],
            metadata={"version": "0.1.61", "criterion": "tag"},
        )

    # Finite ⟹ Lindelöf (trivially compact)
    if rep == "finite":
        n = _carrier_size(space)
        return Result.true(
            mode="exact",
            value="lindelof",
            justification=[
                f"Finite space (|X|={n}): every open cover is finite, "
                "hence has a countable (even finite) subcover."
            ],
            metadata={"version": "0.1.61", "carrier_size": n, "criterion": "finite"},
        )

    # Positive tags
    if any(t in tags for t in ("lindelof", "second_countable", "compact",
                                "separable_metrizable", "second_countable_hausdorff")):
        witness = next(t for t in ("lindelof", "second_countable", "compact",
                                   "separable_metrizable", "second_countable_hausdorff")
                       if t in tags)
        justification = {
            "lindelof": "Space explicitly tagged lindelof.",
            "second_countable": "Second countable ⟹ Lindelöf (countable basis gives countable subcovers).",
            "compact": "Compact ⟹ Lindelöf (every finite subcover is countable).",
            "separable_metrizable": "Separable metrizable ⟹ second countable ⟹ Lindelöf.",
            "second_countable_hausdorff": "Second countable ⟹ Lindelöf.",
        }
        return Result.true(
            mode="theorem",
            value="lindelof",
            justification=[justification[witness]],
            metadata={"version": "0.1.61", "criterion": witness},
        )

    # Uncountable discrete ⟹ not Lindelöf
    if "uncountable" in tags and ("discrete" in tags or "discrete_topology" in tags):
        return Result.false(
            mode="theorem",
            value="not_lindelof",
            justification=[
                "Uncountable discrete space: the cover by singletons has no countable subcover."
            ],
            metadata={"version": "0.1.61", "criterion": "uncountable_discrete"},
        )

    return Result.unknown(
        mode="symbolic",
        value="lindelof_unknown",
        justification=["Insufficient tags to determine Lindelöf property."],
        metadata={"version": "0.1.61"},
    )


# ---------------------------------------------------------------------------
# Combined profile
# ---------------------------------------------------------------------------

def compactness_variant_profile(space: Any) -> Dict[str, Any]:
    """
    Return all four variant results for *space* as a single dict.

    Returns
    -------
    dict with keys:
        representation, countably_compact, sequentially_compact,
        pseudocompact, lindelof
    Each value is a Result object.
    """
    return {
        "representation": _representation_of(space),
        "countably_compact": is_countably_compact(space),
        "sequentially_compact": is_sequentially_compact(space),
        "pseudocompact": is_pseudocompact(space),
        "lindelof": is_lindelof(space),
    }


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

def analyze_compactness_variants(space: Any) -> Result:
    """
    Single-call facade: analyse all compactness variants for *space*.

    Returns a Result whose ``value`` is the ``compactness_variant_profile``
    dict and whose justification summarises each variant's verdict.
    """
    rep = _representation_of(space)
    profile = compactness_variant_profile(space)
    n = _carrier_size(space)

    mode = "exact" if rep == "finite" else "theorem"

    def _verdict(r: Result) -> str:
        return f"{r.status} ({r.mode})"

    justification = [
        f"Domain representation: {rep}",
        f"Countably compact: {_verdict(profile['countably_compact'])}",
        f"Sequentially compact: {_verdict(profile['sequentially_compact'])}",
        f"Pseudocompact: {_verdict(profile['pseudocompact'])}",
        f"Lindelöf: {_verdict(profile['lindelof'])}",
    ]
    if rep == "finite" and n is not None:
        justification.insert(
            1,
            f"|X|={n}: finite space satisfies all four variants exactly."
        )

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": "0.1.61",
            "domain_representation": rep,
            "carrier_size": n,
        },
    )


__all__ = [
    "CompactnessVariantError",
    "is_countably_compact",
    "is_sequentially_compact",
    "is_pseudocompact",
    "is_lindelof",
    "compactness_variant_profile",
    "analyze_compactness_variants",
]
