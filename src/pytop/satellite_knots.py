"""Satellite knots and cable operations (Phase 14.4).

A *satellite knot* S(P, K) is constructed from:
  - A *companion knot* K ⊂ S³ (the "axis")
  - A *pattern* P ⊂ V = S¹ × D² (a knot in the solid torus)

The satellite is obtained by embedding the solid torus V into a tubular
neighborhood of K (via the Seifert framing) and taking the image of P.

The *winding number* w(P) = algebraic intersection of P with a disk D² × {pt}.

Key invariants of satellite knots
-----------------------------------
Alexander polynomial (Morton 1978):
  If P has winding number w in V, then:
    Δ_{S(P,K)}(t) = Δ_P(t) · Δ_K(t^w)

  Here Δ_P is the Alexander polynomial of P as a knot in S³ (image of P
  under the standard embedding V ↪ S³), and Δ_K(t^w) is the Alexander
  polynomial of K evaluated at t^w.

Seifert genus (Gabai):
  g(S(P,K)) = g(P in V) + w(P)·g(K)

  where g(P in V) is the genus of P in the solid torus (i.e. the genus of
  a minimal Seifert surface for P in V after bounding a disk there).

Cable knots C(K; p, q) — (p,q)-cable:
  The pattern P = T(p,q) (torus knot on ∂V = T², winding number p).
  The (p,q)-cable ties p strands around K with q twists total.

  Δ_{C(K;p,q)}(t) = Δ_{T(p,q)}(t) · Δ_K(t^p)

  where Δ_{T(p,q)}(t) is the Alexander polynomial of the torus knot T(p,q).

  Seifert genus: g(C(K;p,q)) = p·g(K) + g(T(p,q)) = p·g(K) + (p-1)(q-1)/2.

  For the (p,1)-cable (longitude):
    C(K; p, 1) has Δ(t) = Δ_K(t^p)·(t^{p/2} - t^{-p/2})/(t^{1/2}-t^{-1/2})
    ... actually Δ_{T(p,1)}(t) = 1 (torus knot T(p,1) is the unknot),
    so Δ_{C(K;p,1)}(t) = Δ_K(t^p).

Whitehead doubles and Bing doubles are important special cases.

References: Morton 1978, Seifert 1950 (cables), Gabai 1986 (genus).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from typing import Any

__all__ = [
    "SatelliteKnot",
    "CableKnot",
    "satellite_alexander_poly",
    "cable_alexander_poly",
    "cable_genus",
    "cable_tau",
    "cable_signature",
    "whitehead_double",
    "torus_knot_alexander_poly",
    "satellite_data",
    "longitudinal_cable",
    "SATELLITE_KNOT_DATA",
]


# ---------------------------------------------------------------------------
# Laurent polynomial helpers
# ---------------------------------------------------------------------------


def _poly_mul(p: dict[int, int], q: dict[int, int]) -> dict[int, int]:
    """Multiply two Laurent polynomials (degree → coefficient dicts)."""
    result: dict[int, int] = {}
    for d1, c1 in p.items():
        for d2, c2 in q.items():
            result[d1 + d2] = result.get(d1 + d2, 0) + c1 * c2
    return {d: c for d, c in result.items() if c != 0}


def _poly_substitute(p: dict[int, int], w: int) -> dict[int, int]:
    """Substitute t → t^w in a Laurent polynomial."""
    return {w * d: c for d, c in p.items() if c != 0}


def _poly_normalize(p: dict[int, int]) -> dict[int, int]:
    """Remove zero coefficients and return sorted dict."""
    return {d: c for d, c in p.items() if c != 0}


def _poly_add(p: dict[int, int], q: dict[int, int]) -> dict[int, int]:
    result = dict(p)
    for d, c in q.items():
        result[d] = result.get(d, 0) + c
    return _poly_normalize(result)


def _poly_exact_divide(num: dict[int, int], den: dict[int, int]) -> dict[int, int]:
    """Exact long division of integer polynomials (assumes den | num).

    Both arguments are dicts {degree: coefficient} with non-negative degrees.
    Returns the quotient {degree: coefficient}; the remainder is discarded
    (it is zero whenever the division is exact, which holds for the torus-knot
    Alexander polynomial).
    """
    rem = {d: c for d, c in num.items() if c != 0}
    den = {d: c for d, c in den.items() if c != 0}
    den_deg = max(den)
    den_lead = den[den_deg]
    quotient: dict[int, int] = {}
    while rem:
        deg = max(rem)
        if deg < den_deg:
            break
        shift = deg - den_deg
        coeff = rem[deg] // den_lead
        if coeff == 0:
            break
        quotient[shift] = quotient.get(shift, 0) + coeff
        for dd, cc in den.items():
            target = dd + shift
            rem[target] = rem.get(target, 0) - coeff * cc
            if rem[target] == 0:
                del rem[target]
    return {d: c for d, c in quotient.items() if c != 0}


# ---------------------------------------------------------------------------
# Torus knot Alexander polynomial
# ---------------------------------------------------------------------------


def torus_knot_alexander_poly(p: int, q: int) -> dict[int, int]:
    """Alexander polynomial of the torus knot T(p, q).

    Δ_{T(p,q)}(t) = (t^{pq} - 1)(t - 1) / ((t^p - 1)(t^q - 1))

    For the (p,q)-torus knot with p, q ≥ 2 coprime.

    The result is expressed as a Laurent polynomial centered at degree 0
    (symmetrized form with Δ(t) = Δ(t^{-1})).

    Parameters
    ----------
    p, q : int
        Coprime positive integers.

    Returns
    -------
    dict[int, int]
        {degree: coefficient} for the symmetrized Alexander polynomial.
    """
    if gcd(p, q) != 1:
        raise ValueError(f"gcd({p},{q}) = {gcd(p,q)} ≠ 1; T(p,q) requires coprime p,q.")
    if p < 1 or q < 1:
        raise ValueError("p,q must be ≥ 1.")
    if p == 1 or q == 1:
        return {0: 1}  # T(1,q) or T(p,1) is the unknot

    # Δ_{T(p,q)}(t) = (t^{pq} - 1)(t - 1) / ((t^p - 1)(t^q - 1)), then symmetrize.
    # Numerator  = (t^{pq} - 1)(t - 1) = t^{pq+1} - t^{pq} - t + 1
    # Denominator = (t^p - 1)(t^q - 1) = t^{p+q} - t^p - t^q + 1
    num: dict[int, int] = {p * q + 1: 1, p * q: -1, 1: -1, 0: 1}
    den: dict[int, int] = {p + q: 1, p: 0, q: 0, 0: 1}
    den[p] = den.get(p, 0) - 1
    den[q] = den.get(q, 0) - 1

    quotient = _poly_exact_divide(num, den)

    # Symmetrize: the quotient has degree (p-1)(q-1); shift to center at 0.
    center = (p - 1) * (q - 1) // 2
    poly = {d - center: c for d, c in quotient.items()}
    return _poly_normalize(poly)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SatelliteKnot:
    """A satellite knot S(P, K).

    Attributes
    ----------
    companion_name : str
        Name of the companion knot K.
    pattern_name : str
        Name of the pattern P (as a knot in the solid torus).
    winding_number : int
        Algebraic winding number of P in V.
    alexander_poly : dict[int, int]
        Alexander polynomial of S(P,K).
    seifert_genus_lower : int | None
        Lower bound on Seifert genus from Gabai's formula.
    companion_genus : int | None
        Seifert genus of K (if known).
    pattern_genus_in_solid_torus : int | None
        Genus of P in V.
    """

    companion_name: str
    pattern_name: str
    winding_number: int
    alexander_poly: dict[int, int]
    seifert_genus_lower: int | None
    companion_genus: int | None
    pattern_genus_in_solid_torus: int | None

    @property
    def seifert_genus(self) -> int | None:
        """Best available Seifert genus (the Gabai lower bound)."""
        return self.seifert_genus_lower


@dataclass(frozen=True)
class CableKnot:
    """A (p,q)-cable satellite knot C(K; p, q).

    Attributes
    ----------
    companion_name : str
    p : int
        Longitudinal winding (number of strands).
    q : int
        Meridional winding (twists).
    alexander_poly : dict[int, int]
    seifert_genus : int | None
    tau : int | None
        τ invariant of C(K; p, q) (computable for torus-knot companions).
    """

    companion_name: str
    p: int
    q: int
    alexander_poly: dict[int, int]
    seifert_genus: int | None
    tau: int | None

    @property
    def name(self) -> str:
        return f"C({self.companion_name}; {self.p}, {self.q})"


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def satellite_alexander_poly(
    pattern_poly: dict[int, int],
    companion_poly: dict[int, int],
    winding: int,
) -> dict[int, int]:
    """Alexander polynomial of the satellite knot S(P, K).

    Morton's formula:
        Δ_{S(P,K)}(t) = Δ_P(t) · Δ_K(t^w)

    Parameters
    ----------
    pattern_poly : dict[int, int]
        Alexander polynomial of the pattern P (as a knot in S³).
    companion_poly : dict[int, int]
        Alexander polynomial of the companion K.
    winding : int
        Algebraic winding number w(P).
    """
    companion_substituted = _poly_substitute(companion_poly, winding)
    return _poly_normalize(_poly_mul(pattern_poly, companion_substituted))


def cable_alexander_poly(
    companion_poly: dict[int, int],
    p: int,
    q: int,
) -> dict[int, int]:
    """Alexander polynomial of the (p,q)-cable C(K; p, q).

    Δ_{C(K;p,q)}(t) = Δ_{T(p,q)}(t) · Δ_K(t^p)

    Parameters
    ----------
    companion_poly : dict[int, int]
        Alexander polynomial of the companion knot K.
    p, q : int
        Cable parameters; gcd(p,q) = 1.
    """
    if gcd(p, q) != 1:
        raise ValueError(f"Cable parameters must be coprime; gcd({p},{q}) = {gcd(p,q)}.")
    pattern = torus_knot_alexander_poly(p, q)
    companion_sub = _poly_substitute(companion_poly, p)
    return _poly_normalize(_poly_mul(pattern, companion_sub))


def cable_genus(seifert_genus: int, p: int, q: int) -> int:
    """Seifert genus of the (p,q)-cable C(K; p, q).

    g(C(K;p,q)) = p·g(K) + (p-1)(q-1)/2  (Gabai 1986 + torus knot genus).

    Parameters
    ----------
    seifert_genus : int
        Seifert genus g(K) of the companion.
    p, q : int
        Cable parameters (p ≥ 1, q ≥ 1, gcd(p,q) = 1).
    """
    torus_genus = (p - 1) * (q - 1) // 2 if p >= 2 and q >= 2 else 0
    return p * seifert_genus + torus_genus


def cable_tau(companion_tau: int, p: int, q: int) -> int:
    """τ invariant of the (p,q)-cable C(K; p, q).

    The Hedden formula (2009) for the τ invariant of cables:
      τ(C(K;p,q)) = p·τ(K) + τ(T(p,q))   if q/p > 2τ(K)
                    = p·τ(K)               if q/p = 2τ(K)
                    = p·τ(K) + (q-1)(p-1)/2 - (p-1)  if q/p < 2τ(K)

    Simplified (standard formula):
      τ(C(K;p,q)) = p·τ(K) + max(0, floor((q - 2τ(K)·p) / (2p)) + ...)

    We use the formula from Hedden (2009):
      τ(C(K;p,q)) = p·τ(K) + τ(T(p,q))  when q > p·2τ(K)
                  = p·τ(K) + (τ(T(p,q)) or variation)  otherwise.

    For simplicity we implement the case q > 0 (positive cables):
      τ(C(K;p,q)) = p·τ(K) + (p-1)(q-1)/2  for q/p > 2τ(K)/1
    (torus knot formula when the companion contributes τ(T(p,q)) = (p-1)(q-1)/2)

    Parameters
    ----------
    companion_tau : int
        τ(K) of the companion knot K.
    p, q : int
        Cable parameters.
    """
    torus_tau = (p - 1) * (q - 1) // 2  # τ(T(p,q))
    # Hedden's formula (simplified for q/p ≠ 2τ(K)):
    if q > 2 * companion_tau * p:
        return p * companion_tau + torus_tau
    elif q < 0:
        return p * companion_tau + q * (p - 1) // 2
    else:
        return p * companion_tau


def cable_signature(companion_signature: int, p: int, q: int) -> int:
    """Knot signature of the (p,q)-cable C(K; p, q).

    σ(C(K;p,q)) = p·σ(K) + σ(T(p,q))  (signature is linear for satellites
    when winding number = p and the pattern is the torus knot T(p,q)).

    This uses the additivity of the signature under satellite operations
    (Litherland 1979):
      σ(S(P,K)) = σ(P_S³) + w(P)²·σ(K)   for certain satellite formulas.

    For (p,q)-cables: σ(C(K;p,q)) = σ(T(p,q)) + p²·σ(K)... not quite right.
    The correct formula (Litherland):
      σ(C(K;p,q)) = σ(T(p,q)) + p·σ(K)  (for the standard cable where w=p).

    We use: σ(cable) = σ(T(p,q)) + p·σ(K).
    For T(2,q): σ(T(2,q)) = -(q-1) for q odd.
    """
    from .concordance import signature_torus_knot
    torus_sig = signature_torus_knot(p, q) if p >= 2 and q >= 2 else 0
    return torus_sig + p * companion_signature


def satellite_data(
    companion_name: str,
    companion_poly: dict[int, int] | None = None,
    companion_genus: int | None = None,
    pattern_name: str | None = None,
    pattern_poly: dict[int, int] | None = None,
    winding_number: int | None = None,
    pattern_genus_v: int | None = None,
) -> SatelliteKnot:
    """Build complete satellite knot data, or look one up by name.

    Two calling conventions:

    * ``satellite_data(name)`` — look up a known satellite knot in the
      built-in :data:`SATELLITE_KNOT_DATA` database.
    * ``satellite_data(companion_name, companion_poly, companion_genus,
      pattern_name, pattern_poly, winding_number, pattern_genus_v)`` — build
      the data explicitly.

    Parameters
    ----------
    companion_name, companion_poly, companion_genus :
        Data for the companion knot K.  When only ``companion_name`` is given
        it is treated as a database key.
    pattern_name, pattern_poly, winding_number :
        Data for the pattern P.
    pattern_genus_v : int | None
        Genus of P in the solid torus V (if known).
    """
    if companion_poly is None:
        if companion_name not in SATELLITE_KNOT_DATA:
            raise KeyError(
                f"Satellite knot {companion_name!r} not in database. "
                f"Known: {sorted(SATELLITE_KNOT_DATA.keys())}"
            )
        spec = SATELLITE_KNOT_DATA[companion_name]
        companion_poly = spec["companion_poly"]
        companion_genus = spec["companion_genus"]
        pattern_name = spec["pattern_name"]
        pattern_poly = spec["pattern_poly"]
        winding_number = spec["winding_number"]
        pattern_genus_v = spec.get("pattern_genus_v")

    assert companion_poly is not None and pattern_poly is not None
    assert winding_number is not None and companion_genus is not None
    assert pattern_name is not None
    alex = satellite_alexander_poly(pattern_poly, companion_poly, winding_number)
    genus_lower: int | None = None
    if pattern_genus_v is not None:
        genus_lower = pattern_genus_v + winding_number * companion_genus
    return SatelliteKnot(
        companion_name=companion_name,
        pattern_name=pattern_name,
        winding_number=winding_number,
        alexander_poly=alex,
        seifert_genus_lower=genus_lower,
        companion_genus=companion_genus,
        pattern_genus_in_solid_torus=pattern_genus_v,
    )


def whitehead_double(
    companion_poly: dict[int, int] | None = None,
    companion_genus: int = 0,
    companion_name: str = "K",
    framing: int = 0,
) -> SatelliteKnot:
    """Whitehead double of a knot K.

    The Whitehead double Wh(K) uses the Whitehead pattern (untwisted):
      - Pattern P = Whitehead link component in V
      - Winding number w(P) = 0
      - Δ_{Wh(K)}(t) = Δ_P(t) · Δ_K(t^0) = Δ_P(t) · 1

    For the (untwisted) Whitehead double:
      Δ_{Wh(K)}(t) = 1  (always!)
    This is because Δ_P(t) = 1 for the Whitehead pattern.

    For twisted Whitehead doubles with framing n:
      Δ_{Wh_n(K)}(t) = 1  (still trivial Alexander polynomial!)

    The interesting invariants are τ and s:
      τ(Wh(K)) = 0  if τ(K) = 0 (Hedden)
      |τ(Wh(K))| ≤ 1  in general

    Parameters
    ----------
    companion_poly : dict[int, int]
        Alexander polynomial of K.
    companion_genus : int
        Genus of K.
    companion_name : str
    framing : int
        Blackboard framing (0 = untwisted).
    """
    if companion_poly is None:
        companion_poly = {0: 1}
    whitehead_pattern_poly = {0: 1}  # Whitehead pattern has Δ=1
    alex = satellite_alexander_poly(whitehead_pattern_poly, companion_poly, 0)
    return SatelliteKnot(
        companion_name=companion_name,
        pattern_name=f"Whitehead pattern (framing {framing})",
        winding_number=0,
        alexander_poly=alex,
        seifert_genus_lower=1 if companion_genus > 0 else 0,
        companion_genus=companion_genus,
        pattern_genus_in_solid_torus=1,
    )


def longitudinal_cable(
    companion_poly: dict[int, int],
    companion_genus: int,
    p: int,
    companion_name: str = "K",
) -> CableKnot:
    """Build the (p,1)-cable (longitudinal cable) of K.

    C(K; p, 1) has Δ_{C(K;p,1)}(t) = Δ_K(t^p) · Δ_{T(p,1)}(t) = Δ_K(t^p)
    since T(p,1) is the unknot (Δ=1).

    Parameters
    ----------
    companion_poly : dict[int, int]
        Alexander polynomial of K.
    companion_genus : int
    p : int
        Number of strands.
    """
    alex = cable_alexander_poly(companion_poly, p, 1)
    genus = cable_genus(companion_genus, p, 1)
    return CableKnot(
        companion_name=companion_name,
        p=p,
        q=1,
        alexander_poly=alex,
        seifert_genus=genus,
        tau=None,  # Need τ(K) to compute
    )


# ---------------------------------------------------------------------------
# Known satellite knot database
# ---------------------------------------------------------------------------

SATELLITE_KNOT_DATA: dict[str, dict[str, Any]] = {
    "Wh+(T_{2,3})": {
        "companion_poly": {-1: 1, 0: -1, 1: 1},  # trefoil Δ
        "companion_genus": 1,
        "pattern_name": "Whitehead (+clasp)",
        "pattern_poly": {0: 1},  # Whitehead pattern has Δ = 1
        "winding_number": 0,
        "pattern_genus_v": 1,
    },
    "Wh-(T_{2,3})": {
        "companion_poly": {-1: 1, 0: -1, 1: 1},
        "companion_genus": 1,
        "pattern_name": "Whitehead (-clasp)",
        "pattern_poly": {0: 1},
        "winding_number": 0,
        "pattern_genus_v": 1,
    },
}
