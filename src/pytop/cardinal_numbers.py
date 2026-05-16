"""
cardinal_numbers.py — Cilt IV v0.1.65
=======================================
Durable API for cardinal number entry — Cilt IV opening corridor.

Concepts covered
----------------
- Equinumerosity and cardinality comparison language
- Countable / uncountable threshold
- Basic cardinal arithmetic vocabulary (sum, product, power)
- Cantor's diagonal argument (uncountability of R)
- Cantor's power-set theorem (|A| < |P(A)|)
- Schroeder-Bernstein theorem
- Continuum cardinal c
- Bridge to topological cardinal functions (weight, density, etc.)

Public surface
--------------
cardinality_class(space)           -> str
cardinal_number_profile(space)     -> dict
analyze_cardinal_numbers(space)    -> Result
CardinalNumberError                -> exception class

Design constraint
-----------------
This module does not copy wording or proof text from any reference source.
The reference book (Engelking) is treated solely as a scope checklist.
"""

from __future__ import annotations

from typing import Any, Optional

from .result import Result

try:
    from .finite_spaces import FiniteTopologicalSpace
except Exception:  # pragma: no cover
    FiniteTopologicalSpace = None  # type: ignore


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class CardinalNumberError(Exception):
    """Raised when a cardinal-number operation cannot be completed."""


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


# ---------------------------------------------------------------------------
# Cardinality class
# ---------------------------------------------------------------------------

_TIER_FINITE       = "finite"
_TIER_COUNTABLE    = "countably_infinite"
_TIER_CONTINUUM    = "continuum"
_TIER_UNCOUNTABLE  = "uncountable"
_TIER_UNKNOWN      = "unknown"


def cardinality_class(space: Any) -> str:
    """
    Return the cardinality tier of *space*.

    Tier labels
    -----------
    "finite"             -- |X| is a natural number  (exact, from carrier)
    "countably_infinite" -- |X| = aleph_0  (from tags or symbolic marker)
    "continuum"          -- |X| = c  (e.g. real line, Cantor set, R^n)
    "uncountable"        -- |X| > aleph_0, precise tier unknown
    "unknown"            -- insufficient information
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)

    if rep == "finite":
        return _TIER_FINITE
    if n is not None:
        return _TIER_FINITE

    if any(t in tags for t in ("continuum", "real_line", "reals", "cantor_set",
                                "hilbert_cube", "baire_space", "irrationals")):
        return _TIER_CONTINUUM
    if any(t in tags for t in ("uncountable", "uncountably_infinite")):
        return _TIER_UNCOUNTABLE
    if any(t in tags for t in ("countably_infinite", "omega",
                                "discrete_countable", "rationals")):
        return _TIER_COUNTABLE

    rep_lower = rep.lower()
    if "real" in rep_lower or "continuum" in rep_lower:
        return _TIER_CONTINUUM
    if "countable" in rep_lower:
        return _TIER_COUNTABLE

    return _TIER_UNKNOWN


# ---------------------------------------------------------------------------
# cardinal_number_profile
# ---------------------------------------------------------------------------

def cardinal_number_profile(space: Any) -> dict[str, Any]:
    """
    Return a comprehensive cardinal-number profile for *space*.

    Keys
    ----
    cardinality_tier         : str   -- tier label
    cardinality_label        : str   -- human-readable cardinal symbol
    equinumerosity_note      : str   -- what equinumerosity means for this tier
    countability_threshold   : str   -- position relative to aleph_0 / c thresholds
    power_set_tier           : str   -- tier of P(space) by Cantor's theorem
    schroeder_bernstein_note : str   -- Schroeder-Bernstein applicability note
    continuum_note           : str   -- relationship to the continuum cardinal
    topological_bridge       : str   -- bridge to cardinal functions
    key_theorems             : list[str]
    key_examples             : list[str]
    representation           : str
    """
    rep = _representation_of(space)
    tags = _tags_of(space)  # noqa: F841
    n = _carrier_size(space)
    tier = cardinality_class(space)

    # cardinality label
    if tier == _TIER_FINITE:
        label = str(n) if n is not None else "n (finite)"
    elif tier == _TIER_COUNTABLE:
        label = "aleph_0"
    elif tier == _TIER_CONTINUUM:
        label = "c  (= 2^{aleph_0})"
    elif tier == _TIER_UNCOUNTABLE:
        label = "> aleph_0 (precise tier unknown)"
    else:
        label = "unknown"

    # equinumerosity note
    if tier == _TIER_FINITE:
        equinum = (
            "Two finite sets are equinumerous iff they have the same element count. "
            "Here |X| = {}.".format(n if n is not None else "n")
        )
    elif tier == _TIER_COUNTABLE:
        equinum = (
            "A countably infinite set is equinumerous with N. "
            "Key examples: Z, Q, NxN (diagonal enumeration), "
            "any countable union of countable sets."
        )
    elif tier == _TIER_CONTINUUM:
        equinum = (
            "A set of continuum cardinality is equinumerous with R. "
            "Key examples: any non-degenerate interval (open, closed, or half-open), "
            "R^n for any n >= 1, the Cantor set, P(N), 2^N."
        )
    else:
        equinum = (
            "Equinumerosity is determined by the existence of a bijection. "
            "The cardinality tier of this space is not determined from available tags."
        )

    # countability threshold
    if tier == _TIER_FINITE:
        threshold = "strictly below aleph_0 — finite cardinal."
    elif tier == _TIER_COUNTABLE:
        threshold = (
            "at the aleph_0 threshold — countably infinite. "
            "Every infinite subset is again countably infinite; "
            "every countable union of countable sets is countable."
        )
    elif tier in (_TIER_CONTINUUM, _TIER_UNCOUNTABLE):
        threshold = (
            "strictly above aleph_0 — uncountable. "
            "Cantor's diagonal argument shows R (and any interval) cannot be "
            "enumerated by N."
        )
    else:
        threshold = "countability status not determined from available information."

    # power-set tier
    if tier == _TIER_FINITE:
        n_label = str(n) if n is not None else "n"
        ps_note = (
            f"P(X) has 2^{n_label} elements (Cantor: |P(A)| > |A| for all A). "
            "For finite X this is exponential growth."
        )
    elif tier == _TIER_COUNTABLE:
        ps_note = (
            "P(X) has cardinality 2^{aleph_0} = c (the continuum). "
            "Cantor's theorem: P(N) is uncountable — in fact equinumerous with R."
        )
    elif tier == _TIER_CONTINUUM:
        ps_note = (
            "P(X) has cardinality 2^c, strictly larger than c (Cantor's theorem). "
            "This new cardinal is not usually given a simple name in standard topology."
        )
    else:
        ps_note = (
            "By Cantor's theorem |P(X)| > |X| regardless of the tier. "
            "The precise power-set tier is not determined from available information."
        )

    # Schroeder-Bernstein note
    sb_note = (
        "Schroeder-Bernstein theorem: if f: A -> B and g: B -> A are both injective "
        "then A and B are equinumerous. This allows cardinality equality to be "
        "established by constructing two one-sided injections rather than a single bijection."
    )

    # continuum note
    if tier == _TIER_CONTINUUM:
        continuum_note = (
            "This space has continuum cardinality c = 2^{aleph_0}. "
            "Every non-degenerate interval in R also has cardinality c "
            "(proved by an explicit bijection, e.g. the tangent map on (0,1)). "
            "The continuum hypothesis (CH) states that there is no cardinal strictly "
            "between aleph_0 and c; CH is independent of ZFC (Goedel 1940, Cohen 1963)."
        )
    elif tier == _TIER_COUNTABLE:
        continuum_note = (
            "This space is countably infinite (|X| = aleph_0 < c). "
            "Its power set P(X) has cardinality c, matching the cardinality of R."
        )
    elif tier == _TIER_FINITE:
        continuum_note = (
            "This space is finite; its cardinality is far below c. "
            "The continuum is the cardinality of R = 2^{aleph_0}."
        )
    else:
        continuum_note = (
            "The continuum cardinal c = 2^{aleph_0} = |R| is the standard uncountable "
            "reference point in general topology. This space's relationship to c is "
            "not determined from available tags."
        )

    # topological bridge
    if tier == _TIER_FINITE:
        top_bridge = (
            "For finite topological spaces cardinal functions (weight w(X), "
            "density d(X), character chi(X)) are all finite natural numbers, "
            "computable directly from the carrier and topology."
        )
    elif tier == _TIER_COUNTABLE:
        top_bridge = (
            "For second-countable (or separable metrizable) spaces the cardinal "
            "functions satisfy w(X) = d(X) = chi(X) = aleph_0. "
            "The countability-axioms chapter establishes that aleph_0 is the 'small' "
            "threshold for topological complexity."
        )
    elif tier == _TIER_CONTINUUM:
        top_bridge = (
            "For spaces of continuum cardinality, cardinal functions can range from "
            "aleph_0 (e.g. R with the standard topology: w(R) = aleph_0) to c or higher. "
            "Cardinal arithmetic at this level is the entry point to Cilt IV-V topics: "
            "weight, density, tightness, network weight, and their classical inequalities."
        )
    else:
        top_bridge = (
            "Cardinal functions (weight, density, character, tightness, ...) measure "
            "the 'size' of topological data in units of infinite cardinals. "
            "The cardinal-number language developed here is the prerequisite for "
            "Chapters 29-31 (cardinal functions framework and examples)."
        )

    # key theorems
    key_theorems: list[str] = [
        "Equinumerosity is an equivalence relation: reflexive (id_A), "
        "symmetric (f^{-1}), transitive (g o f).",
        "Every infinite set contains a countably infinite subset "
        "(sequential selection: x_1, x_2, ... avoiding previous choices).",
        "Countable union of countable sets is countable "
        "(diagonal enumeration; NxN is countable).",
        "Cantor diagonal: (0,1) subset R is uncountable "
        "(any enumeration misses the anti-diagonal element).",
        "Every non-degenerate open interval (a,b) has cardinality c "
        "(explicit bijection: x |-> tan(pi*(x - 1/2)) maps (0,1) onto R).",
        "Schroeder-Bernstein: f: A -> B injective and g: B -> A injective "
        "implies A ~ B "
        "(partition into A*, A\\A* using iterated images of A_0 = A\\g[B]).",
        "Cantor power-set: |A| < |P(A)| for every set A "
        "(diagonal set D = {a in A : a not in f(a)} witnesses non-surjectivity).",
        "Cardinal arithmetic: |A|+|B| = |A sqcup B|, |A|*|B| = |A x B|, "
        "|B|^|A| = |B^A| (all functions A -> B).",
    ]

    # key examples
    key_examples: list[str] = [
        "N ~ 2N (even naturals): f(n) = 2n — proper subset equinumerous with the whole.",
        "Z is countably infinite: 0, 1, -1, 2, -2, ... enumerates all integers.",
        "NxN is countable: diagonal sweep (m,n) ordered by m+n.",
        "Q is countable: embed Q_+ into NxN via p/q |-> (p,q), then add Q_- and {0}.",
        "R is uncountable: Cantor diagonal on decimal expansions.",
        "(0,1) ~ R ~ any open interval: all have cardinality c = 2^{aleph_0}.",
        "P(N) ~ R ~ 2^N: all have cardinality c.",
        "P(R) has cardinality 2^c > c: Cantor's theorem applied to R.",
    ]

    return {
        "cardinality_tier": tier,
        "cardinality_label": label,
        "equinumerosity_note": equinum,
        "countability_threshold": threshold,
        "power_set_tier": ps_note,
        "schroeder_bernstein_note": sb_note,
        "continuum_note": continuum_note,
        "topological_bridge": top_bridge,
        "key_theorems": key_theorems,
        "key_examples": key_examples,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

def analyze_cardinal_numbers(space: Any) -> Result:
    """
    Single-call facade: full cardinal-number analysis for *space*.

    Returns a Result whose ``value`` is the ``cardinal_number_profile`` dict.

    Version
    -------
    v0.1.65 -- Cilt IV cardinal-number entry corridor.
    """
    rep = _representation_of(space)
    n = _carrier_size(space)
    profile = cardinal_number_profile(space)
    tier = profile["cardinality_tier"]
    label = profile["cardinality_label"]

    if tier == _TIER_FINITE:
        mode = "exact"
    elif tier in (_TIER_COUNTABLE, _TIER_CONTINUUM, _TIER_UNCOUNTABLE):
        mode = "theorem"
    else:
        mode = "symbolic"

    justification: list[str] = [
        f"Representation: {rep}.",
        f"Cardinality tier: {tier} -- label: {label}.",
        "Countability threshold: {}".format(profile["countability_threshold"]),
        "Topological bridge: {}...".format(profile["topological_bridge"][:100]),
    ]
    if rep == "finite" and n is not None:
        justification.insert(1, f"|X| = {n} (exact finite cardinal).")

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": "0.1.65",
            "domain_representation": rep,
            "carrier_size": n,
            "cardinality_tier": tier,
            "cardinality_label": label,
        },
    )


__all__ = [
    "CardinalNumberError",
    "cardinality_class",
    "cardinal_number_profile",
    "analyze_cardinal_numbers",
]
