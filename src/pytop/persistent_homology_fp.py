"""Persistent homology over Z/p for arbitrary prime p.

Implements the standard column-reduction algorithm with coefficients in the
finite field F_p = Z/pZ.  For p = 2 this is equivalent to the XOR-based
reduction in :mod:`.persistent_homology`; for p > 2 it tracks explicit
coefficients and uses modular inverses (Fermat's little theorem) to eliminate
pivots.

The output ``PersistencePair`` objects are identical in type to those produced
by all other pytop persistence pipelines, so the result is directly compatible
with barcode, diagram, and distance utilities.

When to prefer different primes
--------------------------------
- p = 2 (default): fastest, always correct for orientable manifolds.
- p = 3, 5, 7, ...: detects torsion in H_*(X; Z) that is invisible over F_2
  (e.g., RP² has H_1(RP²; Z/2) = Z/2 but H_1(RP²; Z/3) = 0).
- Comparing barcodes across multiple primes gives information about
  Z-homology torsion subgroups.

Public API
----------
persistence_pairs_fp   — filtration + prime → barcode over F_p
is_prime               — small primality helper
"""

from __future__ import annotations

import math
from itertools import combinations

from .persistent_homology import FilteredComplex, PersistencePair

# ---------------------------------------------------------------------------
# Arithmetic helpers
# ---------------------------------------------------------------------------


def is_prime(n: int) -> bool:
    """Return True iff n is a prime number."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def _modinv(a: int, p: int) -> int:
    """Modular inverse of a mod p (p prime) via Fermat's little theorem."""
    return pow(a, p - 2, p)


# ---------------------------------------------------------------------------
# Z/p column operations
# ---------------------------------------------------------------------------

# A column is a sparse vector: nonzero row-index → coefficient in {1, ..., p-1}
_Col = dict[int, int]


def _pivot(col: _Col) -> int | None:
    return max(col) if col else None


def _add_scaled(target: _Col, source: _Col, scalar: int, p: int) -> None:
    """target += scalar * source  (in-place, over F_p)."""
    for row, coeff in source.items():
        new = (target.get(row, 0) + scalar * coeff) % p
        if new == 0:
            target.pop(row, None)
        else:
            target[row] = new


# ---------------------------------------------------------------------------
# Main reduction
# ---------------------------------------------------------------------------


def persistence_pairs_fp(
    filtered: FilteredComplex,
    prime: int = 2,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Compute persistence pairs of ``filtered`` over the field F_p = Z/pZ.

    Parameters
    ----------
    filtered:
        A :class:`.FilteredComplex` (from any pytop filtration builder).
    prime:
        The characteristic of the coefficient field.  Must be a prime integer
        ≥ 2.  Default is 2, which matches the output of
        :func:`.persistence_pairs` exactly.
    include_zero_persistence:
        Whether to include pairs where birth == death.

    Returns
    -------
    tuple[PersistencePair, ...]
        Persistence pairs sorted by (dimension, birth, death).  Essential
        classes have ``death = math.inf``.

    Raises
    ------
    ValueError
        If ``prime`` is not a prime integer ≥ 2.

    Examples
    --------
    Klein bottle has torsion H_1(K; Z) = Z ⊕ Z/2, so:

    >>> from pytop.persistent_homology import FilteredComplex
    >>> # Compare p=2 vs p=3 barcodes to detect torsion (see tests for detail)

    Notes
    -----
    Complexity: O(m³) in the number of simplices m, same as the Z/2 algorithm.
    For p = 2 the reduction is identical to standard XOR-based persistence
    (the symmetric difference of sets).
    """
    if not is_prime(prime):
        raise ValueError(f"prime must be a prime integer ≥ 2, got {prime!r}.")

    index_of = {simplex: idx for idx, simplex in enumerate(filtered.simplices)}
    columns: list[_Col] = []
    for simplex, dimension in zip(filtered.simplices, filtered.dimensions):
        if dimension == 0:
            columns.append({})
        else:
            col: _Col = {}
            for i, face in enumerate(combinations(simplex, len(simplex) - 1)):
                row = index_of[face]
                # ∂_k: i-th face gets coefficient (-1)^i
                sign = 1 if i % 2 == 0 else prime - 1
                col[row] = (col.get(row, 0) + sign) % prime
                if col[row] == 0:
                    col.pop(row)
            columns.append(col)

    low_inverse: dict[int, int] = {}
    for j in range(len(columns)):
        while (piv := _pivot(columns[j])) is not None:
            if piv not in low_inverse:
                low_inverse[piv] = j
                break
            prev = low_inverse[piv]
            c_j = columns[j][piv]
            c_prev = columns[prev][piv]
            # Eliminate pivot: columns[j] -= (c_j / c_prev) * columns[prev]
            scalar = (prime - c_j * _modinv(c_prev, prime) % prime) % prime
            _add_scaled(columns[j], columns[prev], scalar, prime)

    pairs: list[PersistencePair] = []
    for creator, destroyer in low_inverse.items():
        birth = filtered.births[creator]
        death = filtered.births[destroyer]
        if not include_zero_persistence and death == birth:
            continue
        pairs.append(PersistencePair(filtered.dimensions[creator], birth, death))

    paired_creators = set(low_inverse)
    for i in range(len(columns)):
        if not columns[i] and i not in paired_creators:
            pairs.append(PersistencePair(
                filtered.dimensions[i], filtered.births[i], math.inf
            ))

    return tuple(sorted(pairs, key=lambda pair: (pair.dimension, pair.birth, pair.death)))
