"""
cofinality.py — Cilt IV v0.1.67
=================================
Durable API for cofinality and regularity — Cilt IV third corridor.

Concepts covered
----------------
- Cofinal subsets of a limit ordinal / cardinal
- Cofinality cf(alpha): least cardinality of a cofinal subset
- Regular cardinals: cf(kappa) = kappa
- Singular cardinals: cf(kappa) < kappa
- Key instances: cf(omega) = omega (regular), cf(omega_1) = omega_1 (regular),
  cf(omega_omega) = omega (singular)
- Successor cardinals are always regular
- Topological bridge: cofinality and compactness / countable compactness in ordinal spaces
- Bridge to cardinal functions (Chapter 29-31)

Public surface
--------------
cofinality_class(space)         -> str
cofinality_profile(space)       -> dict
analyze_cofinality(space)       -> Result
CofinAlityError                 -> exception class

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

class CofinAlityError(Exception):
    """Raised when a cofinality operation cannot be completed."""


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
# Cofinality class
# ---------------------------------------------------------------------------

_CF_FINITE          = "finite"           # n (finite ordinal/cardinal)
_CF_OMEGA_REGULAR   = "omega_regular"    # cf = omega, regular (cf(omega)=omega)
_CF_SUCCESSOR_REG   = "successor_regular"# cf = kappa (successor cardinal, always regular)
_CF_UNCOUNTABLE_REG = "uncountable_regular"  # cf = kappa = omega_1, omega_2, ...
_CF_SINGULAR        = "singular"         # cf(kappa) < kappa  (e.g. cf(omega_omega)=omega)
_CF_UNKNOWN         = "unknown"


def cofinality_class(space: Any) -> str:
    """
    Return the cofinality regularity class of *space*.

    Class labels
    ------------
    "finite"              -- finite ordinal/cardinal; cf(n) = 1 for n > 0, cf(0) = 0
    "omega_regular"       -- cf = omega (omega is regular: cf(omega)=omega)
    "successor_regular"   -- successor cardinal; always regular (cf(kappa^+) = kappa^+)
    "uncountable_regular" -- regular uncountable cardinal (omega_1, omega_2, ...)
    "singular"            -- cf(kappa) < kappa (e.g. omega_omega, beth_omega)
    "unknown"             -- insufficient information
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)

    # --- Finite ---
    if rep == "finite":
        return _CF_FINITE
    if n is not None:
        return _CF_FINITE

    # --- Singular cardinals ---
    if any(t in tags for t in ("singular", "singular_cardinal",
                                "omega_omega", "beth_omega",
                                "aleph_omega", "singular_limit")):
        return _CF_SINGULAR

    # --- omega / first infinite ordinal (regular) ---
    if any(t in tags for t in ("omega", "first_infinite_ordinal",
                                "countably_infinite", "omega_regular")):
        return _CF_OMEGA_REGULAR

    # --- Successor cardinals (always regular) ---
    if any(t in tags for t in ("successor_cardinal", "omega_1_successor",
                                "omega_2_successor", "aleph_1", "aleph_2",
                                "successor_regular")):
        return _CF_SUCCESSOR_REG

    # --- Uncountable regular cardinals ---
    if any(t in tags for t in ("omega_1", "first_uncountable_ordinal",
                                "uncountable_regular", "regular_cardinal",
                                "inaccessible")):
        return _CF_UNCOUNTABLE_REG

    # --- Representation hints ---
    rep_lower = rep.lower()
    if "singular" in rep_lower:
        return _CF_SINGULAR
    if "omega_1" in rep_lower or "uncountable_regular" in rep_lower:
        return _CF_UNCOUNTABLE_REG
    if "omega" in rep_lower:
        return _CF_OMEGA_REGULAR

    return _CF_UNKNOWN


# ---------------------------------------------------------------------------
# cofinality_profile
# ---------------------------------------------------------------------------

def cofinality_profile(space: Any) -> dict[str, Any]:
    """
    Return a comprehensive cofinality profile for *space*.

    Keys
    ----
    cofinality_class        : str   -- class label
    cofinality_label        : str   -- human-readable cf value
    regularity_status       : str   -- "regular" / "singular" / "trivial" / "unknown"
    cofinal_subset_note     : str   -- what a minimal cofinal subset looks like
    successor_regularity    : str   -- why successor cardinals are always regular
    singular_examples       : str   -- standard singular cardinal examples
    topological_bridge      : str   -- link to ordinal spaces, compactness
    cardinal_function_bridge: str   -- link to Chapters 29-31
    key_theorems            : list[str]
    key_examples            : list[str]
    representation          : str
    """
    rep = _representation_of(space)
    tags = _tags_of(space)  # noqa: F841
    n = _carrier_size(space)
    cf_class = cofinality_class(space)

    # --- Cofinality label ---
    if cf_class == _CF_FINITE:
        if n == 0:
            label = "0  (cf(0) = 0 by convention)"
        elif n == 1:
            label = "1  (cf(1) = 1)"
        else:
            label = "1  (cf(n) = 1 for finite n > 0: {n-1} is already cofinal)"
    elif cf_class == _CF_OMEGA_REGULAR:
        label = "omega  (cf(omega) = omega)"
    elif cf_class == _CF_SUCCESSOR_REG:
        label = "kappa^+  (successor cardinal is its own cofinality)"
    elif cf_class == _CF_UNCOUNTABLE_REG:
        label = "omega_1  (or another regular uncountable cardinal)"
    elif cf_class == _CF_SINGULAR:
        label = "< kappa  (cofinality strictly less than the cardinal itself)"
    else:
        label = "unknown"

    # --- Regularity status ---
    if cf_class == _CF_FINITE:
        reg_status = "trivial" if (n is not None and n <= 1) else "trivial"
    elif cf_class in (_CF_OMEGA_REGULAR, _CF_SUCCESSOR_REG, _CF_UNCOUNTABLE_REG):
        reg_status = "regular"
    elif cf_class == _CF_SINGULAR:
        reg_status = "singular"
    else:
        reg_status = "unknown"

    # --- Cofinal subset note ---
    if cf_class == _CF_FINITE:
        n_str = str(n) if n is not None else "n"
        cofinal_note = (
            "For a finite ordinal n, the singleton {n-1} is already cofinal (n-1 >= all beta < n). "
            f"Hence cf(n) = 1 for n > 0. Here n = {n_str}."
        )
    elif cf_class == _CF_OMEGA_REGULAR:
        cofinal_note = (
            "cf(omega) = omega: no finite set is cofinal in omega "
            "(for any finite F subset omega, max(F)+1 is not covered). "
            "The full set omega itself is the minimal-cardinality cofinal subset."
        )
    elif cf_class == _CF_SUCCESSOR_REG:
        cofinal_note = (
            "A successor cardinal kappa^+ is regular: cf(kappa^+) = kappa^+. "
            "Any cofinal subset of kappa^+ must have cardinality kappa^+, "
            "because kappa^+ cannot be written as a union of fewer than kappa^+ sets "
            "each of size < kappa^+."
        )
    elif cf_class == _CF_UNCOUNTABLE_REG:
        cofinal_note = (
            "cf(omega_1) = omega_1: omega_1 cannot be written as a countable union "
            "of countable ordinals (this would make omega_1 countable — contradiction). "
            "Any cofinal subset of omega_1 must be uncountable."
        )
    elif cf_class == _CF_SINGULAR:
        cofinal_note = (
            "For a singular cardinal kappa, there exists a cofinal subset of cardinality "
            "strictly less than kappa. Example: omega_omega = sup{omega, omega^2, omega^3, ...}; "
            "the sequence omega, omega^2, omega^3, ... is cofinal with cardinality omega < omega_omega."
        )
    else:
        cofinal_note = (
            "A cofinal subset of a limit ordinal alpha is a subset A such that "
            "for every beta < alpha there exists gamma in A with gamma >= beta. "
            "cf(alpha) = min{|A| : A cofinal in alpha}. "
            "The cofinality class of this space is not determined from available tags."
        )

    # --- Successor regularity ---
    succ_reg = (
        "Every successor cardinal kappa^+ is regular: cf(kappa^+) = kappa^+. "
        "Proof sketch: if kappa^+ = union of fewer than kappa^+ sets each of size <= kappa, "
        "then |kappa^+| <= kappa * kappa = kappa < kappa^+ — contradiction. "
        "So kappa^+ cannot be covered by a cofinal family of size < kappa^+."
    )

    # --- Singular examples ---
    sing_ex = (
        "Standard singular cardinals: "
        "omega_omega = sup{omega_n : n in omega} with cf(omega_omega) = omega; "
        "beth_omega with cf(beth_omega) = omega; "
        "any limit cardinal of countable cofinality. "
        "The singular cardinal hypothesis (SCH) concerns the power of singular cardinals."
    )

    # --- Topological bridge ---
    if cf_class == _CF_FINITE:
        top_bridge = (
            "Finite ordinal spaces [0, n] are compact (finite = compact). "
            "Cofinality plays no role for finite spaces."
        )
    elif cf_class == _CF_OMEGA_REGULAR:
        top_bridge = (
            "cf(omega) = omega is the reason sequences suffice in first-countable spaces: "
            "every neighbourhood base is indexed by omega, and convergence is captured by "
            "omega-indexed nets (sequences). "
            "The ordinal space [0, omega) = N with discrete topology; "
            "[0, omega+1] = one-point compactification of N."
        )
    elif cf_class == _CF_UNCOUNTABLE_REG:
        top_bridge = (
            "cf(omega_1) = omega_1 explains why [0, omega_1) is countably compact: "
            "every countable increasing sequence in omega_1 is bounded (has supremum < omega_1), "
            "so [0, omega_1) has no countable cofinal subset — every countable open cover "
            "has a finite subcover. Yet [0, omega_1) is NOT compact (the cover by "
            "initial segments has no finite subcover)."
        )
    elif cf_class == _CF_SINGULAR:
        top_bridge = (
            "Singular cardinals of cofinality omega produce ordinal spaces with "
            "interesting compactness behaviour: [0, omega_omega) is NOT countably compact "
            "(the cofinal omega-sequence witnesses a countable cover with no finite subcover). "
            "Singular cofinality = omega is the key dividing line."
        )
    else:
        top_bridge = (
            "Cofinality determines whether an ordinal space [0, alpha) is countably compact: "
            "if cf(alpha) > omega then [0, alpha) is countably compact; "
            "if cf(alpha) = omega then [0, alpha) is NOT countably compact. "
            "This is the main topological application of cofinality in general topology."
        )

    # --- Cardinal function bridge ---
    cf_bridge = (
        "Cofinality appears in cardinal-function inequalities (Chapters 29-31): "
        "the Hajnal-Juhasz inequality uses cf; "
        "the Shelah theorem on powers of singular cardinals; "
        "the relationship between weight w(X), density d(X), and cofinality of index cardinals. "
        "Regular vs singular behaviour of kappa affects how cardinal arithmetic propagates "
        "through products and function spaces."
    )

    # --- Key theorems ---
    key_theorems: list[str] = [
        "cf(alpha) is always a regular cardinal (the cofinality of any ordinal is regular).",
        "cf(cf(alpha)) = cf(alpha): cofinality is idempotent.",
        "Every successor cardinal kappa^+ is regular: cf(kappa^+) = kappa^+.",
        "cf(omega) = omega: no finite subset of omega is cofinal.",
        "cf(omega_1) = omega_1: no countable subset of omega_1 is cofinal "
        "(countable union of countable sets is countable, but omega_1 is uncountable).",
        "A cardinal kappa is singular iff kappa = sup of fewer than kappa cardinals "
        "each less than kappa.",
        "Topological: [0, alpha) is countably compact iff cf(alpha) > omega.",
        "König's theorem: cf(2^kappa) > kappa for any infinite cardinal kappa.",
    ]

    # --- Key examples ---
    key_examples: list[str] = [
        "cf(0) = 0 (convention); cf(1) = 1; cf(n) = 1 for finite n > 0.",
        "cf(omega) = omega: omega is the first infinite regular cardinal.",
        "cf(omega+1) = 1: {omega} is cofinal in omega+1.",
        "cf(omega_1) = omega_1: omega_1 is regular and uncountable.",
        "cf(omega_omega) = omega: the sequence omega_0, omega_1, ..., omega_n, ... "
        "is cofinal in omega_omega with cardinality omega < omega_omega.",
        "cf(beth_omega) = omega: beth_omega is singular of cofinality omega.",
        "[0, omega_1): countably compact, not compact (cf(omega_1)=omega_1 > omega).",
        "[0, omega_omega): NOT countably compact (cf(omega_omega)=omega).",
        "Long line: cf considerations determine local compactness properties.",
        "König: cf(2^{aleph_0}) > aleph_0, so 2^{aleph_0} != aleph_omega "
        "(since cf(aleph_omega) = omega).",
    ]

    return {
        "cofinality_class": cf_class,
        "cofinality_label": label,
        "regularity_status": reg_status,
        "cofinal_subset_note": cofinal_note,
        "successor_regularity": succ_reg,
        "singular_examples": sing_ex,
        "topological_bridge": top_bridge,
        "cardinal_function_bridge": cf_bridge,
        "key_theorems": key_theorems,
        "key_examples": key_examples,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

def analyze_cofinality(space: Any) -> Result:
    """
    Single-call facade: full cofinality and regularity analysis for *space*.

    Returns a Result whose ``value`` is the ``cofinality_profile`` dict.

    Version
    -------
    v0.1.67 -- Cilt IV cofinality and regularity entry corridor.
    """
    rep = _representation_of(space)
    n = _carrier_size(space)
    profile = cofinality_profile(space)
    cf_class = profile["cofinality_class"]
    label = profile["cofinality_label"]
    reg = profile["regularity_status"]

    if cf_class == _CF_FINITE:
        mode = "exact"
    elif cf_class in (_CF_OMEGA_REGULAR, _CF_SUCCESSOR_REG,
                      _CF_UNCOUNTABLE_REG, _CF_SINGULAR):
        mode = "theorem"
    else:
        mode = "symbolic"

    justification: list[str] = [
        f"Representation: {rep}.",
        f"Cofinality class: {cf_class} -- label: {label}.",
        f"Regularity status: {reg}.",
        "Cofinal subset: {}".format(profile["cofinal_subset_note"][:90]),
        "Topological bridge: {}...".format(profile["topological_bridge"][:90]),
    ]
    if rep == "finite" and n is not None:
        justification.insert(1, f"Finite ordinal n={n}: cf(n)=1 for n>0 (exact).")

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": "0.1.67",
            "domain_representation": rep,
            "carrier_size": n,
            "cofinality_class": cf_class,
            "cofinality_label": label,
            "regularity_status": reg,
        },
    )


__all__ = [
    "CofinAlityError",
    "cofinality_class",
    "cofinality_profile",
    "analyze_cofinality",
]
