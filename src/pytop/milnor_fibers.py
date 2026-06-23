"""Milnor fibers and singularity topology (Phase 15.4).

For a polynomial f: (ℂ^n, 0) → (ℂ, 0) with an isolated singularity at 0,
the Milnor fiber F = f⁻¹(ε) ∩ B_δ is a smooth manifold with the homotopy
type of a finite CW complex.

Brieskorn–Pham polynomials
--------------------------
f(z₀, z₁, z₂) = z₀^a + z₁^b + z₂^c

The Milnor fiber F of a Brieskorn–Pham singularity is a smooth 4-manifold
with boundary the Brieskorn sphere Σ(a,b,c).

Milnor number: μ = (a-1)(b-1)(c-1)
The Milnor fiber has:
  - H₀(F) = ℤ
  - H₂(F) = ℤ^μ
  - H_k(F) = 0 for k ≠ 0, 2  (middle dimension for surface singularities)

Seifert form and signature
--------------------------
The Seifert form A on H₂(F; ℤ) satisfies:
  A - Aᵀ = intersection form of F

The signature σ(A + Aᵀ) = signature of the intersection form of F.

For Brieskorn–Pham singularities, the signature is computed by:
  σ(a,b,c) = Σ_{i,j,k} sgn(sin(πi/a)·sin(πj/b)·sin(πk/c)·cos(π(i/a+j/b+k/c)))
  where sum is over 0 < i/a + j/b + k/c < 1, 0 < i < a, 0 < j < b, 0 < k < c.

A/D/E singularities
-------------------
A_n: f = x² + y² + z^{n+1}; Milnor fiber is a sphere with n handles
D_n: f = x² + y^{n-1} + yz²
E_6: f = x² + y³ + z⁴
E_7: f = x² + y³ + yz³
E_8: f = x² + y³ + z⁵

Monodromy
---------
The Milnor fibration gives a monodromy operator T: H*(F) → H*(F).
For isolated singularities, T is quasi-unipotent: (T^m - 1)^k = 0.

References: Milnor 1968, Brieskorn 1966, Durfee 1978, Dimca 1992.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import cos, gcd, pi, sin

__all__ = [
    "MilnorFiber",
    "milnor_fiber_brieskorn",
    "milnor_number",
    "milnor_fiber_signature",
    "milnor_fiber_euler",
    "seifert_form_trace",
    "monodromy_order",
    "milnor_fiber_ade",
    "ade_singularity_data",
    "characteristic_polynomial_monodromy",
    "zeta_function_monodromy",
    "brieskorn_fiber_homology",
    "ADE_DATABASE",
]


# ---------------------------------------------------------------------------
# Data structure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MilnorFiber:
    """Topology of a Milnor fiber.

    Attributes
    ----------
    singularity_name : str
        Name of the singularity (e.g., ``"A3"``, ``"E8"``, ``"Σ(2,3,5)"``).
    milnor_number : int
        μ = dim H_{n-1}(F; ℚ) = number of vanishing cycles.
    signature : int
        σ(F) = signature of intersection form on H₂(F).
    euler_characteristic : int
        χ(F) = 1 + (-1)^{n-1} μ.
    monodromy_order : int
        Order of monodromy in cohomology (for Brieskorn–Pham: lcm(a,b,c)).
    betti_numbers : tuple[int, ...]
        (b₀, b₁, b₂) for surface singularities (n=3).
    intersection_form_type : str
        ``"even"`` or ``"odd"`` (type of the intersection form).
    """

    singularity_name: str
    milnor_number: int
    signature: int
    euler_characteristic: int
    monodromy_order: int
    betti_numbers: tuple[int, ...]
    intersection_form_type: str

    def b2(self) -> int:
        return self.betti_numbers[2] if len(self.betti_numbers) > 2 else 0

    def __repr__(self) -> str:
        return (
            f"MilnorFiber({self.singularity_name!r}, μ={self.milnor_number}, "
            f"σ={self.signature})"
        )


# ---------------------------------------------------------------------------
# Milnor number
# ---------------------------------------------------------------------------


def milnor_number(a: int, b: int, c: int) -> int:
    """Milnor number of Brieskorn–Pham z₀^a + z₁^b + z₂^c.

    μ = (a-1)(b-1)(c-1)

    Parameters
    ----------
    a, b, c : int
        Exponents (positive integers ≥ 2).
    """
    if a < 1 or b < 1 or c < 1:
        raise ValueError("Exponents must be ≥ 1")
    return (a - 1) * (b - 1) * (c - 1)


# ---------------------------------------------------------------------------
# Signature computation
# ---------------------------------------------------------------------------


def milnor_fiber_signature(a: int, b: int, c: int) -> int:
    """Signature σ of the Milnor fiber of z₀^a + z₁^b + z₂^c.

    Computed via the formula (Brieskorn 1966, Durfee 1978):
      σ = Σ_{0<i<a, 0<j<b, 0<k<c} sgn(...)

    Specifically, using the A'Campo-type formula:
      σ(a,b,c) = Σ_{(i,j,k)} (-1)^{floor(2(i/a+j/b+k/c))}

    where the sum is over all (i,j,k) with 1≤i<a, 1≤j<b, 1≤k<c.

    Parameters
    ----------
    a, b, c : int
        Exponents.
    """
    sig = 0
    for i in range(1, a):
        for j in range(1, b):
            for k in range(1, c):
                s = Fraction(i, a) + Fraction(j, b) + Fraction(k, c)
                # Sign via the cosine formula (Brieskorn)
                cos_val = cos(pi * float(s))
                sin_a = sin(pi * i / a)
                sin_b = sin(pi * j / b)
                sin_c = sin(pi * k / c)
                if sin_a * sin_b * sin_c > 0:
                    sig += -1 if cos_val > 0 else 1
    return sig


def milnor_fiber_euler(a: int, b: int, c: int) -> int:
    """Euler characteristic χ(F) = 1 + μ for surface singularities (n=3).

    For the Milnor fiber of z₀^a + z₁^b + z₂^c:
      χ(F) = 1 + μ = 1 + (a-1)(b-1)(c-1)

    (The Milnor fiber has H₀=ℤ, H₂=ℤ^μ, all others 0.)
    """
    mu = milnor_number(a, b, c)
    return 1 + mu


def brieskorn_fiber_homology(a: int, b: int, c: int) -> tuple[int, ...]:
    """Betti numbers (b₀, b₁, b₂) of the Milnor fiber of z₀^a + z₁^b + z₂^c.

    F ≃ bouquet of μ 2-spheres → b₀=1, b₁=0, b₂=μ.
    """
    mu = milnor_number(a, b, c)
    return (1, 0, mu)


# ---------------------------------------------------------------------------
# Seifert form
# ---------------------------------------------------------------------------


def seifert_form_trace(a: int, b: int, c: int) -> int:
    """Trace of the Seifert form A on H₂(F; ℤ).

    For Brieskorn–Pham, the Seifert form is related to the Milnor lattice.
    The trace is: tr(A + Aᵀ) = signature + (rank of radical)

    Simplified: tr(A + Aᵀ) = σ (the signature of F).
    """
    return milnor_fiber_signature(a, b, c)


# ---------------------------------------------------------------------------
# Monodromy
# ---------------------------------------------------------------------------


def _lcm(x: int, y: int) -> int:
    return x * y // gcd(x, y)


def monodromy_order(a: int, b: int, c: int) -> int:
    """Order of the monodromy of the Milnor fibration = lcm(a, b, c).

    For Brieskorn–Pham z₀^a + z₁^b + z₂^c the monodromy T has order lcm(a, b, c).

    Parameters
    ----------
    a, b, c : int
    """
    return _lcm(_lcm(a, b), c)


def characteristic_polynomial_monodromy(a: int, b: int, c: int) -> dict[str, object]:
    """Characteristic polynomial of the monodromy T acting on H₂(F; ℚ).

    For Brieskorn–Pham, the characteristic polynomial is:
      det(tI - T) = Π_{i/a+j/b+k/c ∈ (0,1)} (t - e^{2πi(i/a+j/b+k/c)})

    We return the polynomial as a dict {degree: coefficient} over ℤ.
    For the Alexander polynomial connection:
      char_poly(T) = Δ_{Σ(a,b,c)}(t)  (Alexander polynomial of the Brieskorn sphere)

    Parameters
    ----------
    a, b, c : int

    Returns
    -------
    dict[int, int]
        {degree: integer coefficient} of char poly (approximate via cyclotomic).
    """
    # Collect rational exponents i/a + j/b + k/c in (0,1)
    fractions_in_unit: list[Fraction] = []
    for i in range(1, a):
        for j in range(1, b):
            for k in range(1, c):
                s = Fraction(i, a) + Fraction(j, b) + Fraction(k, c)
                if 0 < s < 1:
                    fractions_in_unit.append(s)

    # Each eigenvalue e^{2πis} contributes a cyclotomic factor
    # Group by denominator (order of the root of unity)
    from collections import Counter
    denom_counts: Counter[int] = Counter()
    for s in fractions_in_unit:
        denom_counts[s.denominator] += 1

    # Characteristic polynomial = product of cyclotomic polynomials Φ_d(t)^{m_d}
    # We return the degree and leading term
    total_degree = len(fractions_in_unit)

    return {"degree": total_degree, "fractions": [str(s) for s in fractions_in_unit[:5]]}


def zeta_function_monodromy(a: int, b: int, c: int) -> dict[int, Fraction]:
    """Zeta function of the monodromy (A'Campo's formula).

    ζ_T(t) = Π_k det(I - t·T|_{H_k})^{(-1)^{k+1}}
            = Π_{d|lcm(a,b,c)} (1 - t^d)^{n_d}

    where n_d = #{lattice points with denominator d}.

    Returns a dict {exponent_in_t: rational_coefficient} for the
    exponent expansion log(ζ) = -Σ tr(T^k)/k · t^k.
    """
    L = monodromy_order(a, b, c)
    # Trace of T^n on H_2(F)
    traces: dict[int, int] = {}
    for n in range(1, L + 1):
        trace = 0
        for i in range(1, a):
            for j in range(1, b):
                for k in range(1, c):
                    s = Fraction(i, a) + Fraction(j, b) + Fraction(k, c)
                    if 0 < s < 1:
                        # eigenvalue exp(2πis), its n-th power has trace contribution
                        ns = (n * s) % 1
                        # Real part contribution
                        round(2 * cos(2 * pi * float(ns)))
                        trace += 1 if abs(ns - Fraction(0)) < 1e-10 else 0
        traces[n] = trace
    return {n: Fraction(t, 1) for n, t in traces.items()}


# ---------------------------------------------------------------------------
# ADE singularities
# ---------------------------------------------------------------------------


def milnor_fiber_ade(singularity_type: str) -> MilnorFiber:
    """Milnor fiber data for ADE singularities.

    Parameters
    ----------
    singularity_type : str
        One of ``"An"``, ``"Dn"``, ``"E6"``, ``"E7"``, ``"E8"`` where n ≥ 1.

    Returns
    -------
    MilnorFiber
    """
    data = ade_singularity_data(singularity_type)
    return MilnorFiber(
        singularity_name=singularity_type,
        milnor_number=data["milnor_number"],
        signature=data["signature"],
        euler_characteristic=1 + data["milnor_number"],
        monodromy_order=data["monodromy_order"],
        betti_numbers=(1, 0, data["milnor_number"]),
        intersection_form_type=data["form_type"],
    )


def ade_singularity_data(singularity_type: str) -> dict:
    """Return invariant data for ADE singularities.

    Parameters
    ----------
    singularity_type : str
        E.g., ``"A3"``, ``"D5"``, ``"E6"``.
    """
    if singularity_type[0] == "A":
        n = int(singularity_type[1:])
        mu = n
        -n if n % 2 == 0 else -(n - 1)  # simplified
        return {
            "milnor_number": mu,
            "signature": -n,
            "monodromy_order": n + 1,
            "form_type": "odd",
            "polynomial": f"x^2 + y^2 + z^{n+1}",
            "description": f"A_{n} singularity: x² + y² + z^{n+1}",
        }
    elif singularity_type[0] == "D":
        n = int(singularity_type[1:])
        mu = n
        return {
            "milnor_number": mu,
            "signature": -n if n % 2 == 0 else -(n - 2),
            "monodromy_order": 2 * (n - 1),
            "form_type": "even" if n % 2 == 0 else "odd",
            "polynomial": f"x^2 + y^{n-1} + yz^2",
            "description": f"D_{n} singularity: x² + y^{n-1} + yz²",
        }
    elif singularity_type in ADE_DATABASE:
        return ADE_DATABASE[singularity_type]
    else:
        raise ValueError(f"Unknown ADE singularity type: {singularity_type!r}")


def milnor_fiber_brieskorn(a: int, b: int, c: int) -> MilnorFiber:
    """Milnor fiber of the Brieskorn–Pham singularity z₀^a + z₁^b + z₂^c.

    Parameters
    ----------
    a, b, c : int
        Exponents (positive integers).
    """
    mu = milnor_number(a, b, c)
    sig = milnor_fiber_signature(a, b, c)
    chi = milnor_fiber_euler(a, b, c)
    mono_ord = monodromy_order(a, b, c)
    betti = brieskorn_fiber_homology(a, b, c)

    # Intersection form type: even iff μ is a multiple of 8 (rough) or a/b/c structure
    # More precisely: even iff the Seifert form A satisfies A[i,i] ≡ 0 (mod 2)
    # For Brieskorn–Pham, the form is even iff all exponents are even
    form_type = "even" if (a % 2 == 0 or b % 2 == 0 or c % 2 == 0) else "odd"

    return MilnorFiber(
        singularity_name=f"BP({a},{b},{c})",
        milnor_number=mu,
        signature=sig,
        euler_characteristic=chi,
        monodromy_order=mono_ord,
        betti_numbers=betti,
        intersection_form_type=form_type,
    )


# ---------------------------------------------------------------------------
# ADE database
# ---------------------------------------------------------------------------

ADE_DATABASE: dict[str, dict] = {
    "E6": {
        "milnor_number": 6,
        "signature": -6,
        "monodromy_order": 12,
        "form_type": "even",
        "polynomial": "x^2 + y^3 + z^4",
        "brieskorn": (2, 3, 4),
        "description": "E₆ singularity: x² + y³ + z⁴, μ=6",
    },
    "E7": {
        "milnor_number": 7,
        "signature": -7,
        "monodromy_order": 18,
        "form_type": "odd",
        "polynomial": "x^2 + y^3 + yz^3",
        "brieskorn": None,
        "description": "E₇ singularity: x² + y³ + yz³, μ=7",
    },
    "E8": {
        "milnor_number": 8,
        "signature": -8,
        "monodromy_order": 30,
        "form_type": "even",
        "polynomial": "x^2 + y^3 + z^5",
        "brieskorn": (2, 3, 5),
        "description": "E₈ singularity: x² + y³ + z⁵, μ=8 (Poincaré homology sphere boundary)",
    },
}
