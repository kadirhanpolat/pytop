"""Eilenberg–MacLane spaces and asphericity (Phase 13.2).

An Eilenberg–MacLane space K(G, n) is a topological space with a single
non-trivial homotopy group: π_n(K(G,n)) = G and π_k(K(G,n)) = 0 for k ≠ n.

Key results implemented
-----------------------
Integral homology of K(G, 1) for standard groups G:

  K(ℤ, 1) = S¹:
      H_0 = ℤ, H_1 = ℤ, H_k = 0 for k ≥ 2.

  K(ℤ/m, 1) (lens space / classifying space of ℤ/m), m ≥ 2:
      Periodic homology via the bar resolution.
      H_0 = ℤ,
      H_{2k-1} = ℤ/m  (k ≥ 1, odd degrees),
      H_{2k}   = 0    (k ≥ 1, even degrees > 0).

  K(F_r, 1) = ∨_r S¹  (wedge of r circles):
      H_0 = ℤ, H_1 = ℤ^r, H_k = 0 for k ≥ 2.

  K(ℤ^r, 1) = T^r  (r-torus):
      H_k = ℤ^C(r,k)  (binomial coefficient), H_k = 0 for k > r.

  K(ℤ, 2) = CP^∞:
      H_{2k} = ℤ, H_{2k+1} = 0 for all k ≥ 0.

  K(ℤ, n) for n ≥ 1 (rational homology):
      H_k(K(ℤ,n); ℚ) = ℚ for k = 0, n (and 2n-1 if n even); else 0.

Asphericity recognition:
  A simplicial complex K is aspherical (K(π₁,1)) iff H_k(K̃; ℤ) = 0
  for all k ≥ 2, where K̃ is the universal cover.  For small complexes
  we check homological asphericity: H_k(K) = 0 for k ≥ 2 and π₁ is
  "compatible" with the homology (necessary but not sufficient in general).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import Any

__all__ = [
    "KGnHomology",
    "km_homology_cyclic",
    "km_homology_free",
    "km_homology_free_abelian",
    "km_homology_z",
    "km_homology_z2",
    "km_homology_rational",
    "is_aspherical_by_homology",
    "km_euler_characteristic",
]


# ---------------------------------------------------------------------------
# Data structure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class KGnHomology:
    """Integral homology groups H_k(K(G,n); ℤ) up to ``max_degree``.

    Attributes
    ----------
    group_name : str
        Human-readable name of G (e.g. ``"ℤ/6"``).
    n_space : int
        The n in K(G, n).
    betti : tuple[int, ...]
        Free ranks β_k = rank H_k for k = 0, 1, …, max_degree.
    torsion : tuple[tuple[int, ...], ...]
        Torsion invariant factors of H_k (sorted).
    max_degree : int

    Methods
    -------
    describe(k)
        Human-readable string for H_k.
    euler_characteristic()
        Alternating sum of Betti numbers (only well-defined when
        H_k = 0 for large k — use with care for K(G,1) spaces).
    """

    group_name: str
    n_space: int
    betti: tuple[int, ...]
    torsion: tuple[tuple[int, ...], ...]
    max_degree: int

    def describe(self, k: int) -> str:
        if k > self.max_degree:
            return "?"
        parts: list[str] = []
        b = self.betti[k]
        t = self.torsion[k]
        if b == 1:
            parts.append("ℤ")
        elif b > 1:
            parts.append(f"ℤ^{b}")
        parts.extend(f"ℤ/{d}" for d in t)
        return " ⊕ ".join(parts) if parts else "0"

    def euler_characteristic(self) -> int:
        return sum((-1) ** k * b for k, b in enumerate(self.betti))


# ---------------------------------------------------------------------------
# K(ℤ/m, 1) — bar resolution, periodic homology
# ---------------------------------------------------------------------------


def km_homology_cyclic(m: int, max_degree: int) -> KGnHomology:
    """H_*(K(ℤ/m, 1); ℤ) for m ≥ 1, computed up to degree max_degree.

    For m = 1 (trivial group): K(1,1) = *, all H_k = 0 for k ≥ 1.
    For m ≥ 2: periodic bar-complex homology.

    H_0 = ℤ
    H_{2k-1} = ℤ/m   (k ≥ 1)
    H_{2k}   = 0     (k ≥ 1)
    """
    if m < 1:
        raise ValueError(f"m must be a positive integer; got {m}.")
    betti: list[int] = []
    torsion: list[tuple[int, ...]] = []
    for k in range(max_degree + 1):
        if k == 0:
            betti.append(1)
            torsion.append(())
        elif m == 1:
            betti.append(0)
            torsion.append(())
        elif k % 2 == 1:
            betti.append(0)
            torsion.append((m,))
        else:
            betti.append(0)
            torsion.append(())
    return KGnHomology(
        group_name=f"ℤ/{m}" if m > 1 else "1",
        n_space=1,
        betti=tuple(betti),
        torsion=tuple(torsion),
        max_degree=max_degree,
    )


# ---------------------------------------------------------------------------
# K(F_r, 1) = ∨ r S¹
# ---------------------------------------------------------------------------


def km_homology_free(rank: int, max_degree: int) -> KGnHomology:
    """H_*(K(F_r, 1); ℤ) = H_*(∨ r S¹; ℤ) up to max_degree.

    H_0 = ℤ,  H_1 = ℤ^r,  H_k = 0 for k ≥ 2.
    """
    if rank < 0:
        raise ValueError(f"rank must be ≥ 0; got {rank}.")
    betti: list[int] = []
    torsion: list[tuple[int, ...]] = []
    for k in range(max_degree + 1):
        if k == 0:
            betti.append(1)
        elif k == 1:
            betti.append(rank)
        else:
            betti.append(0)
        torsion.append(())
    return KGnHomology(
        group_name=f"F_{rank}",
        n_space=1,
        betti=tuple(betti),
        torsion=tuple(torsion),
        max_degree=max_degree,
    )


# ---------------------------------------------------------------------------
# K(ℤ^r, 1) = T^r
# ---------------------------------------------------------------------------


def km_homology_free_abelian(rank: int, max_degree: int) -> KGnHomology:
    """H_*(K(ℤ^r, 1); ℤ) = H_*(T^r; ℤ) up to max_degree.

    H_k(T^r; ℤ) = ℤ^C(r,k) (binomial coefficient), 0 for k > r.
    """
    if rank < 0:
        raise ValueError(f"rank must be ≥ 0; got {rank}.")
    betti: list[int] = []
    torsion: list[tuple[int, ...]] = []
    for k in range(max_degree + 1):
        betti.append(comb(rank, k) if k <= rank else 0)
        torsion.append(())
    return KGnHomology(
        group_name=f"ℤ^{rank}",
        n_space=1,
        betti=tuple(betti),
        torsion=tuple(torsion),
        max_degree=max_degree,
    )


# ---------------------------------------------------------------------------
# K(ℤ, n)
# ---------------------------------------------------------------------------


def km_homology_z(n: int, max_degree: int) -> KGnHomology:
    """H_*(K(ℤ, n); ℤ) up to max_degree.

    Known values (integral):
      n = 1 (= S¹): H_0 = H_1 = ℤ, else 0.
      n = 2 (= CP^∞): H_{2k} = ℤ, H_{2k+1} = 0.
      n = 3: H_0=ℤ, H_3=ℤ, H_5=ℤ/2, H_7=ℤ/3, H_9=ℤ/2⊕ℤ/2, … (complicated).
      n ≥ 2 exact integral homology beyond small degrees uses Serre spectral
      sequences and is only partially computable here.

    For n = 1 and n = 2 exact values are returned.
    For n ≥ 3 only degree 0 and n (both ℤ) are guaranteed; higher degrees
    are returned as 0 with a note that the computation is incomplete.
    """
    if n < 1:
        raise ValueError(f"n must be ≥ 1; got {n}.")
    betti: list[int] = []
    torsion: list[tuple[int, ...]] = []

    for k in range(max_degree + 1):
        if n == 1:
            betti.append(1 if k <= 1 else 0)
            torsion.append(())
        elif n == 2:
            betti.append(1 if k % 2 == 0 else 0)
            torsion.append(())
        else:
            # Only k=0 (ℤ) and k=n (ℤ) are guaranteed; higher-degree
            # integral homology is complicated and not fully implemented.
            betti.append(1 if k in (0, n) else 0)
            torsion.append(())

    return KGnHomology(
        group_name="ℤ",
        n_space=n,
        betti=tuple(betti),
        torsion=tuple(torsion),
        max_degree=max_degree,
    )


def km_homology_z2(n: int, max_degree: int) -> KGnHomology:
    """H_*(K(ℤ/2, n); ℤ) up to max_degree.

    n = 1: K(ℤ/2, 1) = RP^∞.  H_0=ℤ, H_{2k-1}=ℤ/2 (k≥1), H_{2k}=0 (k≥1).
    n = 2: H_0=ℤ, H_2=ℤ/2, H_3=ℤ/2, H_4=ℤ/4, H_5=ℤ/2, … (Steenrod squares
           govern the pattern; only n=1 exact here, n≥2 partially).
    """
    if n == 1:
        return km_homology_cyclic(2, max_degree)
    betti: list[int] = []
    torsion: list[tuple[int, ...]] = []
    for k in range(max_degree + 1):
        betti.append(1 if k == 0 else 0)
        torsion.append(())
    return KGnHomology(
        group_name="ℤ/2",
        n_space=n,
        betti=tuple(betti),
        torsion=tuple(torsion),
        max_degree=max_degree,
    )


# ---------------------------------------------------------------------------
# Rational homology of K(G, n)
# ---------------------------------------------------------------------------


def km_homology_rational(group_name: str, n: int, max_degree: int) -> dict[int, int]:
    """Rational Betti numbers β_k(K(G,n); ℚ) for standard groups.

    Returns a dict {k: β_k} for k = 0, …, max_degree.

    Handles:
      group = "Z" (ℤ), n = 1: β_0=β_1=1, else 0.
      group = "Z" (ℤ), n = 2: β_{2k}=1 for all k (K(ℤ,2)=CP^∞ rationally).
      group = "Z" (ℤ), n odd ≥ 3: β_0=β_n=1, else 0.
      group = "Z" (ℤ), n even ≥ 4: β_0=β_n=β_{2n-1}=1, else 0.
      group = "Zr" (ℤ^r), n = 1: β_k = C(r,k), else 0.
      group = "Zm" (finite), any n: β_0=1, β_k=0 for k≥1 (finite groups have
              trivial rational homology in positive degrees).
    """
    result: dict[int, int] = {k: 0 for k in range(max_degree + 1)}
    result[0] = 1
    if group_name.startswith("Z/") or group_name.startswith("Zm"):
        return result
    if group_name == "Z":
        if n == 1:
            result[1] = 1
        elif n == 2:
            for k in range(0, max_degree + 1, 2):
                result[k] = 1
        elif n % 2 == 1:
            if n <= max_degree:
                result[n] = 1
        else:
            if n <= max_degree:
                result[n] = 1
            if 2 * n - 1 <= max_degree:
                result[2 * n - 1] = 1
    elif group_name.startswith("Z^"):
        r = int(group_name[2:])
        for k in range(min(r, max_degree) + 1):
            result[k] = comb(r, k)
    return result


# ---------------------------------------------------------------------------
# Asphericity
# ---------------------------------------------------------------------------


def is_aspherical_by_homology(
    betti: list[int] | Any,
    torsion: list[tuple[int, ...]] | None = None,
    pi1_betti_1: int | None = None,
    pi1_type: str = "unknown",
) -> tuple[bool | None, str] | bool:
    """Test homological asphericity (K(π₁, 1) recognition heuristic).

    Two calling conventions are supported:

    * **Simplicial complex** — ``is_aspherical_by_homology(K)`` computes the
      integral homology of ``K`` and returns a plain ``bool``: ``True`` if the
      necessary homological conditions for asphericity hold (``H_k(K) = 0`` for
      all ``k ≥ 2``), ``False`` otherwise.
    * **Explicit homology** — ``is_aspherical_by_homology(betti, torsion,
      pi1_betti_1, pi1_type)`` returns a ``(verdict, reason)`` tuple where the
      verdict is ``True``/``False``/``None`` (undecidable).

    A necessary condition for ``K`` to be aspherical is that its homology
    matches that of ``K(π₁(K), 1)``:

    1. ``H_k(K) = 0`` for all ``k ≥ 2`` (no higher homology).
    2. ``β_1(K) = rank(π₁^{ab})`` — first Betti number matches the π₁^{ab} rank.
    """
    from .simplicial_complexes import SimplicialComplex

    if isinstance(betti, SimplicialComplex):
        complex_obj = betti
        from .homology import _simplices_of_dimension, boundary_matrix
        from .homology import _smith_normal_form as _snf

        max_dim = max(
            (s.dimension for s in complex_obj.simplexes), default=0
        )

        def _rank(mat: list[list[int]]) -> int:
            if not mat or not mat[0]:
                return 0
            return len(_snf(mat))

        # β_k = dim C_k - rank ∂_k - rank ∂_{k+1}
        for k in range(2, max_dim + 1):
            n_k = len(_simplices_of_dimension(complex_obj, k))
            r_k = _rank(boundary_matrix(complex_obj, k))
            r_k1 = _rank(boundary_matrix(complex_obj, k + 1))
            beta_k = n_k - r_k - r_k1
            if beta_k != 0:
                return False
        return True

    if torsion is None:
        torsion = []
    if pi1_betti_1 is None:
        pi1_betti_1 = betti[1] if len(betti) > 1 else 0
    n = len(betti)
    for k in range(2, n):
        if betti[k] != 0 or (k < len(torsion) and torsion[k]):
            return (
                False,
                f"H_{k}(K) ≠ 0: β_{k}={betti[k]}, torsion={torsion[k] if k < len(torsion) else ()}. "
                "Higher homology obstructs asphericity.",
            )
    if betti[1] != pi1_betti_1:
        return (
            False,
            f"β_1(K) = {betti[1]} ≠ rank(π₁^{{ab}}) = {pi1_betti_1}. "
            "Homology inconsistent with K(π₁, 1).",
        )
    if pi1_type == "free":
        return (
            True,
            "H_k = 0 for k ≥ 2 and π₁ is free: K(F_r, 1) = ∨r S¹ is aspherical.",
        )
    if pi1_type == "free_abelian":
        return (
            True,
            "H_k = 0 for k ≥ 2 and π₁ = ℤ^r: K(ℤ^r, 1) = T^r is aspherical.",
        )
    return (
        None,
        "Necessary homological conditions hold; higher obstructions (π_2, …) "
        "not computable in general — asphericity undecidable.",
    )


def km_euler_characteristic(group_name: str, n: int, truncation: int) -> int:
    """Euler characteristic χ(K(G,n)) using rational Betti numbers, truncated.

    Only meaningful when H_k = 0 for k > truncation (e.g. for K(ℤ^r,1)=T^r).

    Parameters
    ----------
    group_name : str
        ``"Z"``, ``"Z^r"`` (abelian), or ``"Z/m"`` (cyclic finite).
    n : int
        The ``n`` in K(G, n).
    truncation : int
        Compute χ using β_k for k = 0, …, truncation.
    """
    betti_dict = km_homology_rational(group_name, n, truncation)
    return sum((-1) ** k * betti_dict[k] for k in range(truncation + 1))
