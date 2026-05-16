"""
ordinal_numbers.py — Cilt IV v0.1.66
=======================================
Durable API for ordinal number entry — Cilt IV second corridor.

Concepts covered
----------------
- Well-ordering and order type
- Successor ordinals vs limit ordinals (0, successor, limit trichotomy)
- First infinite ordinal omega; omega+1 as successor
- Ordinal arithmetic non-commutativity (1+omega = omega != omega+1)
- Transfinite induction schema (base / successor / limit steps)
- Cofinality preview (bridge to Chapter 28)
- Cardinal vs ordinal distinction (|omega| = |omega+1| but omega != omega+1 as order types)
- Bridge to topological uses: nets indexed by ordinals, long line, ordinal spaces

Public surface
--------------
ordinal_class(space)           -> str
ordinal_profile(space)         -> dict
analyze_ordinal_numbers(space) -> Result
OrdinalNumberError             -> exception class

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

class OrdinalNumberError(Exception):
    """Raised when an ordinal-number operation cannot be completed."""


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
# Ordinal class
# ---------------------------------------------------------------------------

_OTYPE_FINITE       = "finite_ordinal"       # 0, 1, 2, ... n
_OTYPE_OMEGA        = "omega"                # first infinite ordinal w
_OTYPE_SUCCESSOR    = "infinite_successor"   # w+1, w+2, w*2+1, ...
_OTYPE_LIMIT        = "infinite_limit"       # w, w*2, w^2, ... (non-successor limit)
_OTYPE_ORDINAL_SPACE = "ordinal_space"       # [0, alpha) or [0, alpha] topology
_OTYPE_UNKNOWN      = "unknown"


def ordinal_class(space: Any) -> str:
    """
    Return the ordinal type of *space*.

    Type labels
    -----------
    "finite_ordinal"     -- order type is a natural number n
    "omega"              -- order type is the first infinite ordinal omega
    "infinite_successor" -- order type is a successor ordinal > omega
    "infinite_limit"     -- order type is an infinite limit ordinal
    "ordinal_space"      -- the space IS an ordinal space [0,alpha) with order topology
    "unknown"            -- insufficient information

    Notes
    -----
    Reads space.metadata["tags"] and space.representation.
    For concrete FiniteTopologicalSpace objects the carrier size determines the type.
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)

    # --- Finite: order type = n ---
    if rep == "finite":
        return _OTYPE_FINITE
    if n is not None:
        return _OTYPE_FINITE

    # --- Ordinal space topology ---
    if any(t in tags for t in ("ordinal_space", "long_line",
                                "ordinal_topology", "order_topology_ordinal")):
        return _OTYPE_ORDINAL_SPACE

    # --- omega specifically ---
    if any(t in tags for t in ("omega", "first_infinite_ordinal",
                                "discrete_countable_omega")):
        return _OTYPE_OMEGA

    # --- Successor ordinals ---
    if any(t in tags for t in ("successor_ordinal", "omega_plus_1",
                                "omega_plus_n", "infinite_successor")):
        return _OTYPE_SUCCESSOR

    # --- Limit ordinals ---
    if any(t in tags for t in ("limit_ordinal", "infinite_limit",
                                "omega_times_2", "omega_squared",
                                "omega_1", "first_uncountable_ordinal")):
        return _OTYPE_LIMIT

    # --- Representation hints ---
    rep_lower = rep.lower()
    if "ordinal" in rep_lower:
        return _OTYPE_ORDINAL_SPACE
    if "omega" in rep_lower:
        return _OTYPE_OMEGA

    return _OTYPE_UNKNOWN


# ---------------------------------------------------------------------------
# ordinal_profile
# ---------------------------------------------------------------------------

def ordinal_profile(space: Any) -> dict[str, Any]:
    """
    Return a comprehensive ordinal-number profile for *space*.

    Keys
    ----
    ordinal_type           : str   -- one of the type labels above
    order_type_label       : str   -- human-readable label (omega, omega+1, n, ...)
    well_ordering_note     : str   -- what well-ordering means for this type
    successor_limit_class  : str   -- "zero" / "successor" / "limit" (trichotomy)
    cardinal_vs_ordinal    : str   -- distinction note
    arithmetic_note        : str   -- non-commutativity and arithmetic caution
    transfinite_induction  : str   -- the three-step schema applicable here
    cofinality_preview     : str   -- bridge to Chapter 28
    topological_bridge     : str   -- bridge to ordinal spaces, long line, nets
    key_theorems           : list[str]
    key_examples           : list[str]
    representation         : str
    """
    rep = _representation_of(space)
    tags = _tags_of(space)  # noqa: F841
    n = _carrier_size(space)
    otype = ordinal_class(space)

    # --- Order type label ---
    if otype == _OTYPE_FINITE:
        label = str(n) if n is not None else "n (finite ordinal)"
    elif otype == _OTYPE_OMEGA:
        label = "omega  (first infinite ordinal)"
    elif otype == _OTYPE_SUCCESSOR:
        label = "alpha+1  (infinite successor ordinal)"
    elif otype == _OTYPE_LIMIT:
        label = "lambda  (infinite limit ordinal)"
    elif otype == _OTYPE_ORDINAL_SPACE:
        label = "[0, alpha) or [0, alpha]  (ordinal space with order topology)"
    else:
        label = "unknown"

    # --- Well-ordering note ---
    if otype == _OTYPE_FINITE:
        wo_note = (
            "Every non-empty subset of a finite well-ordered set has a least element. "
            "For order type n = {}, the standard linear order is the unique well-ordering.".format(
                n if n is not None else "n"
            )
        )
    elif otype == _OTYPE_OMEGA:
        wo_note = (
            "omega = {0, 1, 2, ...} with the standard order is well-ordered: "
            "every non-empty subset of natural numbers has a least element. "
            "This is the foundation of ordinary mathematical induction."
        )
    elif otype == _OTYPE_SUCCESSOR:
        wo_note = (
            "A successor ordinal alpha+1 is well-ordered. It has a greatest element (alpha itself). "
            "Well-ordering extends through the successor operation."
        )
    elif otype == _OTYPE_LIMIT:
        wo_note = (
            "A limit ordinal lambda is well-ordered but has no greatest element. "
            "Every element has a successor, but there is no single last step before lambda."
        )
    elif otype == _OTYPE_ORDINAL_SPACE:
        wo_note = (
            "An ordinal space [0, alpha) carries the order topology induced by the ordinal ordering. "
            "The underlying set is well-ordered; the topology is generated by order-open intervals."
        )
    else:
        wo_note = (
            "Well-ordering: every non-empty subset has a least element. "
            "The ordinal type of this space is not determined from available tags."
        )

    # --- Successor/limit trichotomy ---
    if otype == _OTYPE_FINITE:
        sl_class = "successor" if (n is not None and n > 0) else "zero"
    elif otype == _OTYPE_OMEGA:
        sl_class = "limit"
    elif otype == _OTYPE_SUCCESSOR:
        sl_class = "successor"
    elif otype in (_OTYPE_LIMIT, _OTYPE_ORDINAL_SPACE):
        sl_class = "limit"
    else:
        sl_class = "unknown"

    # --- Cardinal vs ordinal distinction ---
    if otype == _OTYPE_FINITE:
        cv_note = (
            "For finite ordinals, cardinal and ordinal coincide: |n| = n as a cardinal. "
            "The distinction becomes essential only with infinite ordinals."
        )
    elif otype == _OTYPE_OMEGA:
        cv_note = (
            "omega and omega+1 have the same cardinality (both aleph_0) "
            "but different order types: |omega| = |omega+1| = aleph_0, "
            "yet omega != omega+1 as ordinals. "
            "This is the first and most important cardinal-ordinal distinction."
        )
    elif otype == _OTYPE_SUCCESSOR:
        cv_note = (
            "An infinite successor ordinal alpha+1 has the same cardinality as alpha "
            "(adding one element does not change infinite cardinality), "
            "but a strictly greater order type."
        )
    elif otype == _OTYPE_LIMIT:
        cv_note = (
            "Infinite limit ordinals can share cardinality with many other ordinals. "
            "For example, omega, omega*2, omega^2 all have cardinality aleph_0 "
            "but are mutually distinct as order types."
        )
    elif otype == _OTYPE_ORDINAL_SPACE:
        cv_note = (
            "The ordinal space [0, omega_1) (first uncountable ordinal) is a key topological example: "
            "it is countably compact but not compact, and not second-countable. "
            "Its cardinality is aleph_1, but its ordinal type is omega_1."
        )
    else:
        cv_note = (
            "Cardinal size measures 'how many'; ordinal type measures 'in what order pattern'. "
            "Two sets can be equinumerous yet have distinct well-order types."
        )

    # --- Arithmetic note ---
    if otype == _OTYPE_FINITE:
        arith_note = (
            "For finite ordinals, ordinal arithmetic coincides with natural-number arithmetic: "
            "1 + 2 = 2 + 1 = 3. Commutativity holds."
        )
    else:
        arith_note = (
            "Ordinal arithmetic is NOT commutative in general. "
            "Key witness: 1 + omega = omega (omega absorbs finite additions from the left), "
            "but omega + 1 != omega (appending one element to the right creates a new successor). "
            "Similarly: 2 * omega = omega but omega * 2 = omega + omega != omega. "
            "This asymmetry is essential when building long sequences or transfinite constructions."
        )

    # --- Transfinite induction ---
    if otype == _OTYPE_FINITE:
        tf_induction = (
            "Ordinary mathematical induction suffices for finite ordinals: "
            "base case n=0, inductive step n -> n+1."
        )
    else:
        tf_induction = (
            "Transfinite induction has three cases: "
            "(1) Base: prove P(0). "
            "(2) Successor step: if P(alpha) then P(alpha+1). "
            "(3) Limit step: if P(beta) for all beta < lambda then P(lambda). "
            "All three cases must be handled when the claim ranges over all ordinals."
        )

    # --- Cofinality preview ---
    if otype == _OTYPE_FINITE or (otype == _OTYPE_FINITE and n == 0):
        cf_preview = "Cofinality is 1 for any successor ordinal, and 0 for the ordinal 0."
    elif otype == _OTYPE_OMEGA:
        cf_preview = (
            "cf(omega) = omega: the cofinality of omega is omega itself "
            "(no finite cofinal subset exists). "
            "Chapter 28 will make this precise and connect it to regularity."
        )
    elif otype == _OTYPE_SUCCESSOR:
        cf_preview = (
            "cf(alpha+1) = 1 for any successor ordinal: "
            "the singleton {alpha} is already cofinal in alpha+1. "
            "All successor ordinals are regular in this sense."
        )
    elif otype == _OTYPE_LIMIT:
        cf_preview = (
            "For limit ordinals cofinality can vary: "
            "cf(omega) = omega (regular), cf(omega_omega) = omega (singular). "
            "A limit ordinal is regular if cf(lambda) = lambda, singular otherwise. "
            "Chapter 28 develops this distinction."
        )
    elif otype == _OTYPE_ORDINAL_SPACE:
        cf_preview = (
            "The cofinality of the ordinal alpha determines key topological properties "
            "of [0, alpha): if cf(alpha) = omega the space is not countably compact "
            "above every point; if cf(alpha) > omega then [0, alpha) is countably compact. "
            "Chapter 28 will make this connection explicit."
        )
    else:
        cf_preview = (
            "Cofinality cf(alpha) = the least cardinal kappa such that alpha "
            "has a cofinal subset of size kappa. Chapter 28 develops this concept "
            "and connects it to regularity and topological compactness arguments."
        )

    # --- Topological bridge ---
    if otype == _OTYPE_FINITE:
        top_bridge = (
            "Finite ordinals appear as index sets for finite open covers, "
            "finite nets, and finite inductive steps in proofs about finite topological spaces."
        )
    elif otype == _OTYPE_OMEGA:
        top_bridge = (
            "omega = N is the standard index set for sequences. "
            "Sequence convergence in first-countable spaces is completely captured by "
            "omega-indexed nets. The ordinal space [0, omega) is homeomorphic to N "
            "with the discrete topology."
        )
    elif otype == _OTYPE_SUCCESSOR:
        top_bridge = (
            "omega+1 with the order topology is homeomorphic to the one-point "
            "compactification of N (adding a limit point at infinity). "
            "More generally, [0, alpha+1] is compact for any ordinal alpha."
        )
    elif otype == _OTYPE_LIMIT:
        top_bridge = (
            "The ordinal space [0, omega_1) (first uncountable ordinal) is the "
            "classical example of a space that is countably compact but not compact, "
            "and sequentially compact but not metrizable. "
            "Ordinal-indexed nets (transfinite sequences) are essential for convergence "
            "in non-first-countable spaces."
        )
    elif otype == _OTYPE_ORDINAL_SPACE:
        top_bridge = (
            "Ordinal spaces with the order topology are a rich source of counterexamples: "
            "[0, omega_1) is countably compact, not compact, not second-countable; "
            "[0, omega_1] is compact Hausdorff, not metrizable; "
            "the long line (omega_1 * [0,1)) is a connected, locally Euclidean space "
            "that is not second-countable and not metrizable."
        )
    else:
        top_bridge = (
            "Ordinal numbers provide index sets for transfinite nets and sequences, "
            "ordinal spaces with the order topology, and the long line. "
            "They are the combinatorial backbone of cardinal-function inequalities "
            "and compactness arguments in Chapters 29-35."
        )

    # --- Key theorems ---
    key_theorems: list[str] = [
        "Every well-ordered set has a unique ordinal type "
        "(two well-ordered sets are isomorphic iff they have the same order type).",
        "Trichotomy: every ordinal is either 0, a successor ordinal, or a limit ordinal.",
        "Transfinite induction: to prove P(alpha) for all ordinals, "
        "it suffices to handle the base, successor, and limit cases separately.",
        "Ordinal arithmetic is not commutative: "
        "1 + omega = omega but omega + 1 != omega.",
        "|omega| = |omega+1| = aleph_0: adding one element to an infinite well-ordered "
        "set does not change its cardinality, but does change its order type.",
        "Every ordinal alpha is the set of all smaller ordinals: "
        "alpha = {beta : beta < alpha} (von Neumann representation).",
        "The class of all ordinals is well-ordered but is not a set (Burali-Forti).",
        "cf(alpha+1) = 1 for any ordinal alpha; "
        "cf(omega) = omega; cf(omega_1) = omega_1.",
    ]

    # --- Key examples ---
    key_examples: list[str] = [
        "0 = empty set; 1 = {0}; 2 = {0,1}; n = {0,...,n-1} (von Neumann).",
        "omega = {0,1,2,...}: first infinite ordinal, order type of N.",
        "omega+1: append one point after all naturals; has a maximum element.",
        "1+omega = omega: prepend one point to N gives the same order type as N.",
        "omega+1 != omega: omega+1 has a maximum; omega does not.",
        "omega*2 = omega+omega: two copies of omega end-to-end.",
        "2*omega = omega: two elements then repeat gives order type omega.",
        "[0, omega_1): first uncountable ordinal space — countably compact, not compact.",
        "[0, omega_1]: one-point extension — compact Hausdorff, not metrizable.",
        "Long line: omega_1 copies of [0,1) — connected, locally Euclidean, not second-countable.",
    ]

    return {
        "ordinal_type": otype,
        "order_type_label": label,
        "well_ordering_note": wo_note,
        "successor_limit_class": sl_class,
        "cardinal_vs_ordinal": cv_note,
        "arithmetic_note": arith_note,
        "transfinite_induction": tf_induction,
        "cofinality_preview": cf_preview,
        "topological_bridge": top_bridge,
        "key_theorems": key_theorems,
        "key_examples": key_examples,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

def analyze_ordinal_numbers(space: Any) -> Result:
    """
    Single-call facade: full ordinal-number analysis for *space*.

    Returns a Result whose ``value`` is the ``ordinal_profile`` dict.

    Version
    -------
    v0.1.66 -- Cilt IV ordinal-number entry corridor.
    """
    rep = _representation_of(space)
    n = _carrier_size(space)
    profile = ordinal_profile(space)
    otype = profile["ordinal_type"]
    label = profile["order_type_label"]
    sl = profile["successor_limit_class"]

    if otype == _OTYPE_FINITE:
        mode = "exact"
    elif otype in (_OTYPE_OMEGA, _OTYPE_SUCCESSOR, _OTYPE_LIMIT, _OTYPE_ORDINAL_SPACE):
        mode = "theorem"
    else:
        mode = "symbolic"

    justification: list[str] = [
        f"Representation: {rep}.",
        f"Ordinal type: {otype} -- label: {label}.",
        f"Successor/limit class: {sl}.",
        "Cardinal vs ordinal: {}".format(profile["cardinal_vs_ordinal"][:90]),
        "Topological bridge: {}...".format(profile["topological_bridge"][:90]),
    ]
    if rep == "finite" and n is not None:
        justification.insert(1, f"Order type = {n} (exact finite ordinal).")

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": "0.1.66",
            "domain_representation": rep,
            "carrier_size": n,
            "ordinal_type": otype,
            "order_type_label": label,
            "successor_limit_class": sl,
        },
    )


__all__ = [
    "OrdinalNumberError",
    "ordinal_class",
    "ordinal_profile",
    "analyze_ordinal_numbers",
]
