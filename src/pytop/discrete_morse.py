"""Discrete Morse theory for finite simplicial complexes (Forman 1998).

A discrete gradient vector field pairs p-simplices with (p+1)-simplices such
that each simplex appears in at most one pair and the induced gradient flow is
acyclic (no closed V-paths).  Unpaired simplices are *critical*; they satisfy
the Morse inequalities: m_p ≥ β_p and Σ(-1)^p m_p = χ(K).

Public API
----------
MorsePair                  — a single gradient pair (face, coface)
MorseMatching              — the full gradient vector field
MorseInequalities          — Morse inequality data for a matching
discrete_gradient_matching — acyclic greedy Morse matching
is_valid_morse_matching    — validity check
check_morse_inequalities   — compute and verify Morse inequalities

References
----------
Forman, R. (1998). Morse theory for cell complexes. *Advances in Mathematics*,
134(1), 90–145.
Lewiner, T., Lopes, H., & Tavares, G. (2003). Optimal discrete Morse functions
for 2-manifolds. *Computational Geometry*, 26(3), 221–233.
"""

from __future__ import annotations

from dataclasses import dataclass

from .simplices import Simplex
from .simplicial_complexes import SimplicialComplex

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MorsePair:
    """A gradient pair (face, coface) in a discrete vector field.

    ``face`` has dimension p and ``coface`` has dimension p+1; ``face`` is a
    codimension-one face of ``coface``.
    """

    face: Simplex
    coface: Simplex

    def __post_init__(self) -> None:
        if self.coface.dimension != self.face.dimension + 1:
            raise ValueError(
                f"coface dimension {self.coface.dimension} must equal "
                f"face dimension {self.face.dimension} + 1"
            )
        if not self.face.vertices.issubset(self.coface.vertices):
            raise ValueError("face vertices must be a subset of coface vertices")


@dataclass(frozen=True)
class MorseMatching:
    """A discrete gradient vector field on a simplicial complex.

    ``pairs`` is the set of gradient pairs; ``critical`` is the set of unpaired
    critical simplices.  Every simplex of the complex appears in exactly one of
    the two sets.

    Note: this dataclass does not self-validate that ``pairs ∪ critical`` covers
    a particular complex.  Use ``is_valid_morse_matching`` to verify acyclicity
    before drawing conclusions from the Morse vector or inequalities.
    """

    pairs: frozenset[MorsePair]
    critical: frozenset[Simplex]

    def critical_by_dimension(self, dim: int) -> frozenset[Simplex]:
        """Return critical simplices of a given dimension."""
        return frozenset(s for s in self.critical if s.dimension == dim)

    def morse_vector(self) -> tuple[int, ...]:
        """Return (m_0, m_1, ..., m_d): critical cell counts per dimension.

        Returns an empty tuple when there are no critical cells.
        """
        if not self.critical:
            return ()
        max_dim = max(s.dimension for s in self.critical)
        return tuple(len(self.critical_by_dimension(d)) for d in range(max_dim + 1))

    def euler_characteristic(self) -> int:
        """Alternating sum of critical cell counts.

        By the Morse theorem this equals χ(K).
        """
        return sum((-1) ** d * m for d, m in enumerate(self.morse_vector()))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_coface_map(complex_obj: SimplicialComplex) -> dict[Simplex, list[Simplex]]:
    """Map each p-simplex to its (p+1)-cofaces present in the complex."""
    cofaces: dict[Simplex, list[Simplex]] = {s: [] for s in complex_obj.simplexes}
    for tau in complex_obj.simplexes:
        for sigma in tau.boundary_faces():
            if sigma in cofaces:
                cofaces[sigma].append(tau)
    return cofaces


def _canonical_key(s: Simplex) -> tuple[str, ...]:
    return tuple(sorted(repr(v) for v in s.vertices))


def _has_v_path_to(
    source: Simplex,
    target: Simplex,
    coface_of: dict[Simplex, Simplex],
) -> bool:
    """Return True if there is a V-path from ``source`` to ``target``.

    A V-path is a sequence α_0, β_0, α_1, β_1, ... where (α_i, β_i) is a
    gradient pair and α_{i+1} ≠ α_i is a face of β_i.  We follow the gradient
    arrows encoded in ``coface_of`` (face → gradient coface).
    """
    visited: set[Simplex] = set()
    stack: list[Simplex] = [source]
    while stack:
        curr = stack.pop()
        if curr == target:
            return True
        if curr in visited:
            continue
        visited.add(curr)
        if curr in coface_of:
            tau = coface_of[curr]
            for face in tau.boundary_faces():
                if face != curr and face not in visited:
                    stack.append(face)
    return False


# ---------------------------------------------------------------------------
# Gradient vector field computation
# ---------------------------------------------------------------------------


def discrete_gradient_matching(
    complex_obj: SimplicialComplex,
    strategy: str = "greedy",
) -> MorseMatching:
    """Compute an acyclic discrete gradient vector field on a simplicial complex.

    Parameters
    ----------
    complex_obj:
        A finite face-closed simplicial complex.
    strategy:
        ``"greedy"`` (default): process simplices in order of increasing
        dimension (then lexicographic order of vertices).  For each unpaired
        p-simplex σ, try to pair it with an unpaired (p+1)-coface τ such that
        the addition of (σ, τ) does not create a V-path cycle.  If no such τ
        exists, σ is declared critical.

    Returns
    -------
    MorseMatching
        A valid acyclic discrete gradient vector field.  The Morse inequalities
        m_p ≥ β_p(K) and Σ(-1)^p m_p = χ(K) are always satisfied.

    Notes
    -----
    Cycle detection runs a DFS (O(n)) for each face of each candidate coface, so
    the overall algorithm is O(n³) in the number of simplices.  For contractible
    subcomplexes the greedy algorithm finds a perfect Morse matching (one critical
    0-cell, no higher critical cells).
    """
    if strategy != "greedy":
        raise ValueError(f"Unknown strategy {strategy!r}; only 'greedy' is supported.")

    coface_map = _build_coface_map(complex_obj)
    # Maps a FACE simplex to its gradient COFACE (for cycle detection).
    coface_of: dict[Simplex, Simplex] = {}
    paired: set[Simplex] = set()
    pairs: list[MorsePair] = []

    sorted_simplices = sorted(
        complex_obj.simplexes,
        key=lambda s: (s.dimension, _canonical_key(s)),
    )

    for sigma in sorted_simplices:
        if sigma in paired:
            continue

        available = [tau for tau in coface_map[sigma] if tau not in paired]
        available.sort(key=_canonical_key)

        paired_with: Simplex | None = None
        for tau in available:
            # Adding (sigma, tau) creates a cycle iff some face of tau other
            # than sigma can reach sigma via existing V-paths.
            creates_cycle = any(
                alpha != sigma and _has_v_path_to(alpha, sigma, coface_of)
                for alpha in tau.boundary_faces()
            )
            if not creates_cycle:
                paired_with = tau
                break

        if paired_with is not None:
            pairs.append(MorsePair(face=sigma, coface=paired_with))
            coface_of[sigma] = paired_with
            paired.add(sigma)
            paired.add(paired_with)

    critical = frozenset(s for s in complex_obj.simplexes if s not in paired)
    return MorseMatching(pairs=frozenset(pairs), critical=critical)


# ---------------------------------------------------------------------------
# Validity check
# ---------------------------------------------------------------------------


def is_valid_morse_matching(
    complex_obj: SimplicialComplex,
    matching: MorseMatching,
) -> bool:
    """Return True if *matching* is a valid discrete gradient vector field on *complex_obj*.

    Checks that:
    - Every pair (σ, τ) has σ as a codimension-one face of τ.
    - No simplex appears more than once across all pairs.
    - The union of paired simplices and critical simplices equals the full complex.
    - The matching is acyclic (no closed V-paths).
    """
    all_simplices = complex_obj.simplexes
    used_faces = {p.face for p in matching.pairs}
    used_cofaces = {p.coface for p in matching.pairs}

    if used_faces & used_cofaces:
        return False
    if used_faces & matching.critical or used_cofaces & matching.critical:
        return False
    if (used_faces | used_cofaces | matching.critical) != all_simplices:
        return False

    for pair in matching.pairs:
        if pair.face not in all_simplices or pair.coface not in all_simplices:
            return False
        if not pair.face.vertices.issubset(pair.coface.vertices):
            return False
        if pair.coface.dimension != pair.face.dimension + 1:
            return False

    # Acyclicity check: rebuild coface_of and check for V-path cycles.
    coface_of: dict[Simplex, Simplex] = {p.face: p.coface for p in matching.pairs}
    for p in matching.pairs:
        for alpha in p.coface.boundary_faces():
            if alpha != p.face and _has_v_path_to(alpha, p.face, coface_of):
                return False

    return True


# ---------------------------------------------------------------------------
# Morse inequalities
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MorseInequalities:
    """Morse inequality data for a discrete gradient vector field.

    The weak Morse inequalities state m_p ≥ β_p(K) for all p.
    The Euler identity states Σ(-1)^p m_p = χ(K).
    """

    morse_vector: tuple[int, ...]
    betti_numbers: tuple[int, ...]
    euler_from_morse: int
    euler_from_complex: int
    weak_inequalities_satisfied: bool
    euler_identity_satisfied: bool

    @property
    def all_satisfied(self) -> bool:
        return self.weak_inequalities_satisfied and self.euler_identity_satisfied

    def describe(self) -> str:
        lines = [
            f"Morse vector  : {self.morse_vector}",
            f"Betti numbers : {self.betti_numbers}",
            f"Euler (Morse) : {self.euler_from_morse}",
            f"Euler (χ)     : {self.euler_from_complex}",
            f"Weak inequalities satisfied : {self.weak_inequalities_satisfied}",
            f"Euler identity satisfied    : {self.euler_identity_satisfied}",
        ]
        return "\n".join(lines)


def check_morse_inequalities(
    complex_obj: SimplicialComplex,
    matching: MorseMatching,
) -> MorseInequalities:
    """Compute and verify the Morse inequalities for *matching* on *complex_obj*.

    Computes integral simplicial homology to obtain Betti numbers, then checks
    that m_p ≥ β_p for all p and that the alternating sum of m_p equals χ(K).

    Parameters
    ----------
    complex_obj:
        The simplicial complex on which *matching* is defined.
    matching:
        A discrete gradient vector field (need not be from
        :func:`discrete_gradient_matching`; any valid matching works).

    Returns
    -------
    MorseInequalities
        Inequality data.  ``all_satisfied`` is True iff the matching is
        consistent with the homology of the complex.
    """
    from .homology import betti_numbers as _betti

    mv = matching.morse_vector()
    betti = _betti(complex_obj)
    max_dim = max(len(mv), len(betti)) if (mv or betti) else 0

    mv_padded = mv + (0,) * (max_dim - len(mv))
    betti_padded = betti + (0,) * (max_dim - len(betti))

    weak_ok = all(mv_padded[p] >= betti_padded[p] for p in range(max_dim))
    euler_morse = sum((-1) ** p * mv_padded[p] for p in range(max_dim))
    euler_complex = complex_obj.euler_characteristic()

    return MorseInequalities(
        morse_vector=mv,
        betti_numbers=betti,
        euler_from_morse=euler_morse,
        euler_from_complex=euler_complex,
        weak_inequalities_satisfied=weak_ok,
        euler_identity_satisfied=(euler_morse == euler_complex),
    )
