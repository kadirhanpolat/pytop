"""
quantitative_topology.py -- Cilt IV v0.1.68
=============================================
Durable API for quantitative topology -- pedagogical positioning after
set-theoretic preparation (cardinals, ordinals, cofinality).

Concepts covered
----------------
- Qualitative vs quantitative reading of topological properties
- Weight w(X): least cardinality of a base
- Density d(X): least cardinality of a dense subset
- Character chi(X): least cardinality of a neighbourhood base at any point
- Local character chi(x, X): neighbourhood base size at a specific point
- Lindelof number L(X): least kappa s.t. every open cover has a subcover of size <= kappa
- Separability, second-countability, first-countability as threshold instances (all = aleph_0)
- Pedagogical bridge: these are the "qualitative properties made quantitative"
- Set-theoretic preparation bridge: w/d/chi/L live in the same cardinal arithmetic
  developed in Chapters 26-28 (cardinal, ordinal, cofinality)

Public surface
--------------
quantitative_profile(space)          -> dict
analyze_quantitative_topology(space) -> Result
QuantitativeTopologyError            -> exception class

Design constraint
-----------------
This module does not copy wording or proof text from any reference source.
The reference book (Engelking) is treated solely as a scope checklist.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

from .result import Result

try:
    from .finite_spaces import FiniteTopologicalSpace
except Exception:  # pragma: no cover
    FiniteTopologicalSpace = None  # type: ignore


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class QuantitativeTopologyError(Exception):
    """Raised when a quantitative topology operation cannot be completed."""


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


def _carrier_size(space: Any) -> Optional[int]:
    if FiniteTopologicalSpace is not None and isinstance(space, FiniteTopologicalSpace):
        return len(space.carrier)
    carrier = getattr(space, "carrier", None)
    if carrier is not None:
        try:
            return len(carrier)
        except TypeError:
            pass
    return None


def _topology_size(space: Any) -> Optional[int]:
    """Return |tau| if available (for finite spaces)."""
    if FiniteTopologicalSpace is not None and isinstance(space, FiniteTopologicalSpace):
        return len(space.topology)
    return None


# ---------------------------------------------------------------------------
# Weight estimate
# ---------------------------------------------------------------------------

def _weight_estimate(space: Any, rep: str, tags: frozenset, n: Optional[int]) -> str:
    """Return a string description of w(X) for *space*."""
    if rep == "finite":
        if n is not None and n == 0:
            return "0 (empty space)"
        if n is not None:
            return "finite (at most {})".format(n)
        return "finite"

    if any(t in tags for t in ("second_countable", "separable_metrizable",
                                "real_line", "reals", "euclidean")):
        return "aleph_0  (second-countable: countable base exists)"
    if any(t in tags for t in ("discrete_uncountable", "uncountable_discrete")):
        return "= |X| (uncountable discrete: each singleton is a base element)"
    if any(t in tags for t in ("indiscrete",)):
        return "1  (indiscrete: {X} is a base)"
    if any(t in tags for t in ("second_countable",)):
        return "aleph_0"
    if any(t in tags for t in ("omega", "countably_infinite", "discrete_countable")):
        return "aleph_0  (countable discrete: singleton base)"
    return "unknown (insufficient tags)"


def _density_estimate(space: Any, rep: str, tags: frozenset, n: Optional[int]) -> str:
    """Return a string description of d(X) for *space*."""
    if rep == "finite":
        if n is not None and n == 0:
            return "0"
        if n is not None:
            return "finite (at most {})".format(n)
        return "finite"

    if any(t in tags for t in ("separable", "second_countable",
                                "separable_metrizable", "real_line", "reals")):
        return "aleph_0  (separable: countable dense subset exists)"
    if any(t in tags for t in ("discrete_uncountable", "uncountable_discrete")):
        return "= |X|  (discrete: no proper dense subset)"
    if any(t in tags for t in ("indiscrete",)):
        return "1  (indiscrete: any singleton is dense)"
    if any(t in tags for t in ("omega", "countably_infinite", "discrete_countable")):
        return "aleph_0  (countable discrete)"
    return "unknown (insufficient tags)"


def _character_estimate(space: Any, rep: str, tags: frozenset, n: Optional[int]) -> str:
    """Return a string description of chi(X) for *space*."""
    if rep == "finite":
        return "finite"
    if any(t in tags for t in ("first_countable", "second_countable",
                                "metrizable", "metric", "real_line", "reals",
                                "separable_metrizable")):
        return "aleph_0  (first-countable: countable neighbourhood base at each point)"
    if any(t in tags for t in ("indiscrete",)):
        return "1  (indiscrete: only X itself is a neighbourhood of any point)"
    if any(t in tags for t in ("omega_1", "ordinal_space")):
        return "aleph_1  (ordinal space [0,omega_1]: character = aleph_1 at limit points)"
    return "unknown (insufficient tags)"


def _lindelof_estimate(space: Any, rep: str, tags: frozenset, n: Optional[int]) -> str:
    """Return a string description of L(X) for *space*."""
    if rep == "finite":
        return "finite (every open cover has a finite subcover)"
    if any(t in tags for t in ("compact", "compact_hausdorff")):
        return "1  (compact: every open cover has a finite subcover)"
    if any(t in tags for t in ("second_countable", "separable_metrizable",
                                "real_line", "reals", "lindelof")):
        return "aleph_0  (Lindelof: every open cover has a countable subcover)"
    if any(t in tags for t in ("discrete_uncountable", "uncountable_discrete")):
        return "= |X|  (uncountable discrete: only subcovers of full size work)"
    return "unknown (insufficient tags)"


# ---------------------------------------------------------------------------
# quantitative_profile
# ---------------------------------------------------------------------------

def quantitative_profile(space: Any) -> Dict[str, Any]:
    """
    Return a comprehensive quantitative topology profile for *space*.

    Keys
    ----
    weight                  : str  -- w(X) estimate
    density                 : str  -- d(X) estimate
    character               : str  -- chi(X) estimate
    lindelof_number         : str  -- L(X) estimate
    qualitative_quantitative_bridge : str  -- how qualitative properties become quantitative
    set_theoretic_bridge    : str  -- link to cardinal/ordinal/cofinality (Chapters 26-28)
    threshold_instances     : str  -- when w=d=chi=L=aleph_0 (second-countable spaces)
    pedagogical_positioning : str  -- why this chapter follows the set-theoretic preparation
    key_inequalities        : list[str]  -- basic inequalities among w, d, chi, L
    key_examples            : list[str]
    representation          : str
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)

    weight   = _weight_estimate(space, rep, tags, n)
    density  = _density_estimate(space, rep, tags, n)
    character = _character_estimate(space, rep, tags, n)
    lindelof = _lindelof_estimate(space, rep, tags, n)

    # qualitative-quantitative bridge
    qq_bridge = (
        "Qualitative: 'X is second-countable' = 'X has a countable base'. "
        "Quantitative: w(X) = min{|B| : B is a base for X}. "
        "The qualitative property is the threshold instance w(X) <= aleph_0. "
        "Similarly: separable <=> d(X) <= aleph_0; "
        "first-countable <=> chi(X) <= aleph_0; "
        "Lindelof <=> L(X) <= aleph_0."
    )

    # set-theoretic bridge
    st_bridge = (
        "The values w(X), d(X), chi(X), L(X) are infinite cardinals — elements of the "
        "cardinal hierarchy developed in Chapter 26. "
        "Comparing them uses the same cardinal arithmetic (aleph_0 <= aleph_1 <= ...). "
        "Cofinality (Chapter 28) enters when asking whether a base of size kappa "
        "can be refined to one of size cf(kappa). "
        "Ordinal-indexed nets (Chapter 27) are the convergence tool when chi(X) > aleph_0."
    )

    # threshold instances
    threshold = (
        "Second-countable spaces: w(X) = aleph_0, d(X) = aleph_0, chi(X) = aleph_0, L(X) = aleph_0. "
        "All four cardinal functions collapse to the same threshold aleph_0. "
        "This is why second-countable Hausdorff spaces are the 'nicest' infinite spaces: "
        "they are separable, first-countable, and Lindelof simultaneously. "
        "Examples: R^n with Euclidean topology, any separable metrizable space."
    )

    # pedagogical positioning
    ped_pos = (
        "Quantitative topology is placed AFTER the set-theoretic preparation (Chapters 26-28) "
        "because: (1) the values w(X), d(X), chi(X), L(X) are infinite cardinals and "
        "must be compared using cardinal arithmetic; "
        "(2) cofinality determines which cardinal functions can coincide; "
        "(3) ordinal-indexed nets are needed when chi(X) > aleph_0. "
        "Placing this chapter before the set-theoretic corridor would make the "
        "cardinal-valued definitions feel unmotivated."
    )

    # key inequalities
    key_ineqs: List[str] = [
        "d(X) <= w(X): every base contains a dense subset (pick one point per base element).",
        "chi(X) <= w(X): a base for X restricts to a local base at each point.",
        "L(X) <= w(X): second-countable implies Lindelof.",
        "w(X) <= d(X) * chi(X): Arhangel'skii-type bound (approximate).",
        "d(X) <= 2^{chi(X)}: density is bounded by 2 raised to character.",
        "For T_1 spaces: |X| <= 2^{chi(X) * L(X)} (Arhangel'skii inequality).",
        "w(X) = d(X) for metrizable spaces (Urysohn metrization).",
        "chi(X) <= w(X) always; equality for homogeneous spaces.",
    ]

    # key examples
    key_examples: List[str] = [
        "R (real line, Euclidean): w=d=chi=L = aleph_0 — all four coincide at the threshold.",
        "R^n (n >= 1, Euclidean): same as R; second-countable.",
        "Discrete space on N: w=d=chi=L = aleph_0.",
        "Discrete space on R: w=d=chi = |R| = c; L = c (not Lindelof).",
        "Indiscrete space on X: w=1, d=1, chi=1, L=1 regardless of |X|.",
        "[0, omega_1) (ordinal space): w = aleph_1, d = aleph_0, chi = aleph_1, L = aleph_1.",
        "Sorgenfrey line (lower limit topology): d = aleph_0 but w = c (not second-countable).",
        "Stone-Cech compactification beta(N): w = c, d = aleph_0, chi = c.",
    ]

    return {
        "weight": weight,
        "density": density,
        "character": character,
        "lindelof_number": lindelof,
        "qualitative_quantitative_bridge": qq_bridge,
        "set_theoretic_bridge": st_bridge,
        "threshold_instances": threshold,
        "pedagogical_positioning": ped_pos,
        "key_inequalities": key_ineqs,
        "key_examples": key_examples,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

def analyze_quantitative_topology(space: Any) -> Result:
    """
    Single-call facade: full quantitative topology analysis for *space*.

    Returns a Result whose ``value`` is the ``quantitative_profile`` dict.

    Version
    -------
    v0.1.68 -- Cilt IV quantitative topology pedagogical positioning corridor.
    """
    rep = _representation_of(space)
    n = _carrier_size(space)
    profile = quantitative_profile(space)

    if rep == "finite":
        mode = "exact"
    elif any(t in _tags_of(space) for t in (
        "second_countable", "separable_metrizable", "real_line", "reals",
        "metrizable", "compact", "lindelof", "separable", "first_countable",
        "omega", "countably_infinite", "discrete_countable",
        "discrete_uncountable", "indiscrete", "ordinal_space", "omega_1",
    )):
        mode = "theorem"
    else:
        mode = "symbolic"

    justification: List[str] = [
        "Representation: {}.".format(rep),
        "Weight w(X): {}.".format(profile["weight"]),
        "Density d(X): {}.".format(profile["density"]),
        "Character chi(X): {}.".format(profile["character"]),
        "Lindelof L(X): {}.".format(profile["lindelof_number"]),
        "Pedagogical note: {}".format(profile["pedagogical_positioning"][:80]),
    ]
    if rep == "finite" and n is not None:
        justification.insert(1, "|X| = {} (finite space: all cardinal functions are finite).".format(n))

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": "0.1.68",
            "domain_representation": rep,
            "carrier_size": n,
            "weight": profile["weight"],
            "density": profile["density"],
            "character": profile["character"],
            "lindelof_number": profile["lindelof_number"],
        },
    )
