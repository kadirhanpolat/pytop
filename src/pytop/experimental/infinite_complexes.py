"""Countably infinite CW complexes and claim-free Rips scans.

Homology commutes with direct limits, so ``H_k(K) = colim H_k(K_i)`` for an
exhaustion ``K = union K_i`` by finite subcomplexes. Two facts shape this module:

* A direct limit is **not** determined by the groups alone. In
  ``Z --x2--> Z --x2--> ...`` every group is ``Z`` and every Betti number is 1,
  yet the colimit is ``Z[1/2]``. Nothing here ever infers stabilisation from
  observation -- not from repeated Betti numbers, and not from repeated
  isomorphisms, which a lacunary wedge defeats for any fixed number of steps.
* The only proof route used is structural: attaching a cell of dimension ``d``
  affects only ``H_{d-1}`` and ``H_d``, so if every cell added after stage ``N``
  has dimension ``>= k+2`` then ``H_k(K_N) = H_k(K)``. The threshold is ``k+2``,
  not ``k+1``: a ``(k+1)``-cell can kill a class in ``H_k``.

The module has three parts.

**Part A -- standard spaces.** :func:`rp_infinity_homology`,
:func:`cp_infinity_homology`, :func:`s_infinity_homology` and
:func:`infinite_lens_homology` evaluate an in-module or shipped skeleton at index
``degree + 1`` and return a plain :class:`~pytop.homology.HomologyResult`. They
carry no uncertainty machinery because they take no caller-supplied tower --
though they do guard their *parameters*.

**Part B -- user towers.** :func:`colimit_homology` takes explicit stages and
signed inclusion data, verifies the chain-map law and a non-empty dimension
window, and returns a :class:`ConditionalHomology` naming every tail assumption.

**Part C -- Rips scan.** :func:`rips_betti_scan` reports Betti numbers of Rips
complexes on metric balls and makes no claim about any infinite complex.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal, Protocol, runtime_checkable

from pytop.cellular_homology import (
    CWComplex,
    cellular_homology,
    cw_complex_projective_space,
    cw_real_projective_space,
)
from pytop.homology import HomologyResult, SimplicialComplex, betti_numbers, boundary_matrix
from pytop.metric_spaces import FiniteMetricSpace
from pytop.persistent_homology import vietoris_rips_filtration

__all__ = [
    "Assumptions",
    "ConditionalHomology",
    "InsufficientStagesError",
    "NotATowerError",
    "ProperMetric",
    "RipsBettiScan",
    "ScanStop",
    "StageInclusion",
    "TailAssumption",
    "colimit_homology",
    "cp_infinity_homology",
    "infinite_lens_homology",
    "rips_betti_scan",
    "rp_infinity_homology",
    "s_infinity_homology",
    "z_lattice",
]

Matrix = list[list[int]]


class NotATowerError(ValueError):
    """The supplied stages and inclusions do not form a tower of chain complexes."""


class InsufficientStagesError(ValueError):
    """No non-empty window of the supplied stages satisfies the dimension hypothesis."""


def _check_degree(degree: int) -> None:
    if degree < 0:
        raise ValueError(
            f"degree must be >= 0, got {degree}. Homology is not defined in "
            f"negative degrees, so there is nothing to compute. Pass a "
            f"non-negative degree, e.g. rp_infinity_homology(1)."
        )


def _mul(a: Matrix, b: Matrix, rows: int, inner: int, cols: int) -> Matrix:
    """``a @ b`` with shapes given explicitly.

    Written locally rather than reusing a private helper from another module
    because the boundary matrices here are legitimately empty in low degrees,
    and the shapes must survive that.
    """
    return [
        [sum(a[i][t] * b[t][j] for t in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


# ---------------------------------------------------------------------------
# Part A -- standard spaces
# ---------------------------------------------------------------------------


def _lens_skeleton(p: int, n: int) -> CWComplex:
    """``n``-skeleton of ``S^inf / Z_p`` -- one cell per dimension.

    ``d_k`` is ``[[p]]`` for even ``k`` and ``[[0]]`` for odd ``k``. At ``p = 2``
    this is byte-identical to :func:`~pytop.cellular_homology.cw_real_projective_space`,
    whose ``d_k = 1 + (-1)^k`` takes the same values on the same parity.

    :func:`~pytop.cellular_homology.cw_lens_space` cannot be used as a stage
    function: it takes only ``p`` and returns a fixed 3-dimensional complex, so
    a tower built from it would be constant.
    """
    return CWComplex(
        cell_counts={k: 1 for k in range(n + 1)},
        boundary_maps={k: [[p if k % 2 == 0 else 0]] for k in range(1, n + 1)},
    )


def _s_infinity_skeleton(n: int) -> CWComplex:
    """``n``-skeleton of ``S^inf`` in the antipodal structure -- two cells per dimension.

    ``d_k(e^k_pm) = e^{k-1}_pm + (-1)^k e^{k-1}_mp``.

    :func:`~pytop.cellular_homology.cw_sphere` must **not** be used here: it is
    ``{0: 1, n: 1}``, under which ``S^n`` is not a subcomplex of ``S^{n+1}`` and
    the stages are not nested. Note also that the all-zero-boundary variant
    passes ``CWComplex``'s ``d.d == 0`` check and yields ``Z^2`` in every degree,
    so these matrices are load-bearing.
    """
    return CWComplex(
        cell_counts={k: 2 for k in range(n + 1)},
        boundary_maps={k: [[1, (-1) ** k], [(-1) ** k, 1]] for k in range(1, n + 1)},
    )


def rp_infinity_homology(degree: int) -> HomologyResult:
    """``H_degree(RP^inf; Z)`` -- ``Z`` in degree 0, ``Z/2`` in odd degrees, 0 in even.

    ``RP^n -> RP^{n+1}`` attaches one ``(n+1)``-cell, so every cell added after
    stage ``degree + 1`` has dimension ``>= degree + 2`` and the structural
    theorem applies at that index.

    Examples
    --------
    >>> rp_infinity_homology(1).torsion
    (2,)
    >>> rp_infinity_homology(2).betti
    0
    """
    _check_degree(degree)
    return cellular_homology(cw_real_projective_space(degree + 1), degree)


def cp_infinity_homology(degree: int) -> HomologyResult:
    """``H_degree(CP^inf; Z)`` -- ``Z`` in even degrees, 0 in odd.

    ``CP^n -> CP^{n+1}`` attaches one ``(2n+2)``-cell. Note this tower is *not*
    "skeletal" in the naive sense (stage ``i`` does not add an ``i``-cell), which
    is why the hypothesis is stated on the dimension of the cells added rather
    than on the stage index.

    Examples
    --------
    >>> cp_infinity_homology(2).betti
    1
    >>> cp_infinity_homology(3).betti
    0
    """
    _check_degree(degree)
    return cellular_homology(cw_complex_projective_space(degree + 1), degree)


def s_infinity_homology(degree: int) -> HomologyResult:
    """``H_degree(S^inf; Z)`` -- ``Z`` in degree 0, 0 above. ``S^inf`` is contractible.

    Examples
    --------
    >>> s_infinity_homology(0).betti
    1
    >>> s_infinity_homology(3).betti
    0
    """
    _check_degree(degree)
    return cellular_homology(_s_infinity_skeleton(degree + 1), degree)


def infinite_lens_homology(p: int, degree: int) -> HomologyResult:
    """``H_degree(BZ/p; Z)`` -- ``Z`` in degree 0, ``Z/p`` in odd degrees, 0 in even.

    ``p`` is caller input and is guarded: at ``p = 0`` the skeleton degenerates to
    all-zero boundary maps and would report ``Z`` in every degree, where
    ``BZ/0 = K(Z, 1) = S^1`` has ``H_k = 0`` for ``k >= 2``.

    Examples
    --------
    >>> infinite_lens_homology(5, 1).torsion
    (5,)
    >>> infinite_lens_homology(5, 2).betti
    0
    """
    _check_degree(degree)
    if p < 1:
        raise ValueError(
            f"p must be at least 1, got {p}. BZ/p is the classifying space of a "
            f"cyclic group of order p, and p < 1 names no such group -- at p = 0 "
            f"the skeleton degenerates to all-zero boundary maps and would report "
            f"Z in every degree. Pass p >= 1, e.g. infinite_lens_homology(5, 3)."
        )
    return cellular_homology(_lens_skeleton(p, degree + 1), degree)


# ---------------------------------------------------------------------------
# Part B -- user-supplied towers
# ---------------------------------------------------------------------------


class TailAssumption(Enum):
    """What was assumed about the stages beyond the last one supplied."""

    STAGES_EXIST = "stages_exist"
    INCLUSIONS_VALID = "inclusions_valid"
    CELL_DIMENSIONS = "cell_dimensions"


@dataclass(frozen=True)
class StageInclusion:
    """Signed cell map ``C_*(K_i) -> C_*(K_{i+1})``, one entry per degree.

    ``images`` is a tuple of ``(degree, entries)`` pairs where ``entries[j]`` is
    ``(target_index, sign)`` for the ``j``-th cell of that degree and ``sign`` is
    ``+1`` or ``-1``.

    The sign is required, not decorative: a cellular inclusion is the identity on
    cells only when both complexes orient the shared cells identically. An
    ``RP^2`` sitting inside an ``RP^3`` whose 2-cell is oppositely oriented is a
    genuine subcomplex inclusion that an unsigned map cannot express.

    Stored as nested tuples rather than a mapping so the frozen dataclass is
    actually hashable.
    """

    images: tuple[tuple[int, tuple[tuple[int, int], ...]], ...]

    def at(self, degree: int) -> tuple[tuple[int, int], ...]:
        """Entries for ``degree``; empty when that degree carries no cells."""
        for k, entries in self.images:
            if k == degree:
                return entries
        return ()


@dataclass(frozen=True)
class Assumptions:
    """Exactly what was not proven.

    ``assumed`` names each :class:`TailAssumption` standing behind the result;
    ``verified_steps`` is non-empty by construction, so a result never rests on
    an empty verification window.
    """

    assumed: frozenset[TailAssumption]
    min_tail_cell_dimension: int
    evaluated_stage: int
    verified_steps: tuple[int, ...]


@dataclass(frozen=True)
class ConditionalHomology:
    """A computed group together with the assumptions standing behind it."""

    group: HomologyResult
    assumptions: Assumptions

    def __bool__(self) -> bool:
        """False whenever anything was assumed -- which, for towers, is always."""
        return not self.assumptions.assumed


def _inclusion_matrix(
    inclusion: StageInclusion, degree: int, source_cells: int, target_cells: int
) -> Matrix:
    """Signed ``target_cells x source_cells`` matrix of ``iota_degree``."""
    entries = inclusion.at(degree)
    if len(entries) != source_cells:
        raise NotATowerError(
            f"inclusion at degree {degree} lists {len(entries)} cells but the "
            f"source complex has {source_cells}. Every cell of the source must "
            f"be assigned a (target_index, sign) pair, or the map is not defined "
            f"on all of C_{degree}. Add the missing entries."
        )
    m = [[0] * source_cells for _ in range(target_cells)]
    seen: set[int] = set()
    for j, (target, sign) in enumerate(entries):
        if sign not in (1, -1):
            raise NotATowerError(
                f"inclusion sign at degree {degree}, cell {j} is {sign}; only +1 "
                f"and -1 describe a cellular inclusion, since a cell either keeps "
                f"or reverses its orientation. Use -1 when the two complexes "
                f"orient that shared cell oppositely."
            )
        if not 0 <= target < target_cells:
            raise NotATowerError(
                f"inclusion at degree {degree}, cell {j} targets index {target}, "
                f"but the target complex has {target_cells} cells in that degree. "
                f"Indices are 0-based positions in the target's cell list."
            )
        if target in seen:
            raise NotATowerError(
                f"inclusion at degree {degree} is not injective: two source cells "
                f"both map to target index {target}. A subcomplex inclusion is "
                f"injective on cells. Give each source cell a distinct target."
            )
        seen.add(target)
        m[target][j] = sign
    return m


def _verify_chain_map(
    source: CWComplex, target: CWComplex, inclusion: StageInclusion, step: int
) -> None:
    """Raise :class:`NotATowerError` unless ``d . iota == iota . d`` in every degree.

    Cell counts cannot do this job: they carry no cell identity and no attaching
    data, so a sequence of unrelated complexes with monotone counts would pass a
    count check while having no colimit at all.
    """
    top = max([*source.cell_counts, *target.cell_counts], default=0)

    # Validate every degree the source occupies, degree 0 included. The
    # chain-map loop below starts at 1 and skips empty degrees, so without this
    # pass a malformed degree-0 entry would never be checked -- and
    # `_added_dimensions` trusts its length, so a 2-point stage claiming three
    # images into a 3-point stage would be accepted and report Z^2 for Z^3.
    for k in range(top + 1):
        _inclusion_matrix(
            inclusion, k, source.cell_counts.get(k, 0), target.cell_counts.get(k, 0)
        )

    for k in range(1, top + 1):
        src_k = source.cell_counts.get(k, 0)
        if src_k == 0:
            continue
        src_km1 = source.cell_counts.get(k - 1, 0)
        tgt_k = target.cell_counts.get(k, 0)
        tgt_km1 = target.cell_counts.get(k - 1, 0)
        iota_k = _inclusion_matrix(inclusion, k, src_k, tgt_k)
        iota_km1 = _inclusion_matrix(inclusion, k - 1, src_km1, tgt_km1)
        d_target = target._boundary_matrix(k) or [[0] * tgt_k for _ in range(tgt_km1)]
        d_source = source._boundary_matrix(k) or [[0] * src_k for _ in range(src_km1)]
        lhs = _mul(d_target, iota_k, tgt_km1, tgt_k, src_k)
        rhs = _mul(iota_km1, d_source, tgt_km1, src_km1, src_k)
        if lhs != rhs:
            raise NotATowerError(
                f"step {step}, degree {k}: the chain-map law fails -- "
                f"d.iota = {lhs} but iota.d = {rhs}. The stages and inclusions do "
                f"not describe a subcomplex inclusion, so they bound no colimit. "
                f"If the two complexes orient a shared cell oppositely, give that "
                f"cell sign -1 in the inclusion."
            )


def _added_dimensions(
    source: CWComplex, target: CWComplex, inclusion: StageInclusion
) -> set[int]:
    """Dimensions in which ``target`` has cells outside the image of ``iota``."""
    top = max([*source.cell_counts, *target.cell_counts], default=0)
    return {
        k
        for k in range(top + 1)
        if target.cell_counts.get(k, 0) > len(inclusion.at(k))
    }


def colimit_homology(
    stages: Sequence[CWComplex],
    inclusions: Sequence[StageInclusion],
    degree: int,
) -> ConditionalHomology:
    """``H_degree`` of the colimit of the supplied chain complexes and chain maps.

    This equals ``H_degree(union K_i)`` **only** if the supplied inclusions really
    come from subcomplex inclusions, which this function cannot check: cellular
    chain complexes retain only the degrees of attaching maps, so a chain-level
    embedding that no subcomplex inclusion induces -- ``{e^0, e^4}`` into
    ``CP^2``, say, where ``e^4`` is attached by the Hopf map -- passes
    verification. The algebra is sound; the topological reading is the caller's
    responsibility.

    The result is always conditional: the tail beyond ``stages[-1]`` is assumed,
    never verified. :attr:`ConditionalHomology.assumptions` names what was
    assumed, and the object is falsy whenever anything was.

    Raises
    ------
    NotATowerError
        The inclusions are not injective signed chain maps.
    InsufficientStagesError
        No non-empty window of the supplied stages satisfies the dimension
        hypothesis. This is not a prediction that more stages would help -- that
        is exactly the tail this module refuses to infer.
    """
    _check_degree(degree)
    if len(stages) < 2:
        raise InsufficientStagesError(
            f"at least 2 stages are needed, got {len(stages)}. A single complex "
            f"carries no information about a tail, so nothing follows about a "
            f"colimit. Supply the stages you have, e.g. "
            f"colimit_homology([K0, K1, K2], [i0, i1], degree=1)."
        )
    if len(inclusions) != len(stages) - 1:
        raise NotATowerError(
            f"{len(stages)} stages need {len(stages) - 1} inclusions, got "
            f"{len(inclusions)}. Each consecutive pair of stages needs the map "
            f"between them. Supply one inclusion per pair."
        )

    steps = len(stages) - 1
    for i in range(steps):
        _verify_chain_map(stages[i], stages[i + 1], inclusions[i], step=i)

    min_dim = degree + 2
    added = [
        _added_dimensions(stages[i], stages[i + 1], inclusions[i]) for i in range(steps)
    ]

    # N ranges over 0 .. steps-1, never steps: allowing N = steps would make the
    # quantifier empty and the hypothesis vacuously true for every input.
    chosen: int | None = None
    for n in range(steps):
        if all(all(d >= min_dim for d in added[i]) for i in range(n, steps)):
            chosen = n
            break

    if chosen is None:
        last_bad = max(i for i in range(steps) if any(d < min_dim for d in added[i]))
        low = sorted(d for d in added[last_bad] if d < min_dim)
        raise InsufficientStagesError(
            f"no non-empty window of the supplied stages satisfies the dimension "
            f"hypothesis for degree {degree}: step {last_bad} adds cells of "
            f"dimension {low}, below the required {min_dim}. Without such a window "
            f"nothing connects the supplied stages to the colimit, so no group can "
            f"be reported. Supply stages far enough out that the remaining steps "
            f"add only cells of dimension >= {min_dim} -- this function cannot "
            f"predict how far that is, because that is the tail it refuses to infer."
        )

    return ConditionalHomology(
        group=cellular_homology(stages[chosen], degree),
        assumptions=Assumptions(
            assumed=frozenset(TailAssumption),
            min_tail_cell_dimension=min_dim,
            evaluated_stage=chosen,
            verified_steps=tuple(range(chosen, steps)),
        ),
    )


# ---------------------------------------------------------------------------
# Part C -- claim-free Rips scan
# ---------------------------------------------------------------------------

Norm = Literal["l2", "l1", "linf"]


@runtime_checkable
class ProperMetric(Protocol):
    """A metric space whose balls are finite.

    Finiteness is the provider's contract -- ``ball`` returns a ``Sequence`` --
    not a runtime assertion. Deciding it would mean enumerating a ball, which
    does not terminate for ``Q^2`` or ``R^2``.
    """

    def ball(self, center: Any, radius: float) -> Sequence[Any]:
        """The finite set of points within ``radius`` of ``center``."""
        ...

    def distance(self, x: Any, y: Any) -> float:
        """The ambient distance. Never recomputed inside a ball."""
        ...


@dataclass(frozen=True)
class _ZLattice:
    n: int
    norm: Norm

    def distance(self, x: Any, y: Any) -> float:
        deltas = [abs(a - b) for a, b in zip(x, y, strict=True)]
        if self.norm == "l1":
            return float(sum(deltas))
        if self.norm == "linf":
            return float(max(deltas, default=0))
        return math.sqrt(sum(d * d for d in deltas))

    #: Candidates enumerated before filtering; guards the bounding-box scan
    #: itself, which happens before any caller-side point cap can apply.
    _MAX_CANDIDATES = 5_000_000

    def ball(self, center: Any, radius: float) -> Sequence[Any]:
        r = int(math.floor(radius))
        candidates = (2 * r + 1) ** self.n
        if candidates > self._MAX_CANDIDATES:
            raise ValueError(
                f"ball of radius {radius} in Z^{self.n} would scan "
                f"{candidates:,} lattice points before filtering, over the "
                f"{self._MAX_CANDIDATES:,} limit. The enumeration happens inside "
                f"the metric, so a caller-side point cap cannot stop it. Use a "
                f"smaller radius, or a lower dimension."
            )
        ranges = [range(c - r, c + r + 1) for c in center]
        return [
            point
            for point in itertools.product(*ranges)
            if self.distance(center, point) <= radius
        ]


def z_lattice(n: int, *, norm: Norm = "l2") -> ProperMetric:
    """The integer lattice ``Z^n`` as a :class:`ProperMetric`.

    The norm is explicit because it changes the answer qualitatively, not just
    numerically. Measured at ``eps = 1``, ``max_degree = 1``, radii 1..5: the
    Euclidean disks give ``b_1 = 0, 4, 16, 32, 60`` and the ``l1`` balls
    ``0, 4, 12, 24, 40``, but the ``linf`` balls give ``0`` throughout -- under
    the sup norm a unit square is a 4-clique, so the flag complex fills every
    square and no 1-cycle survives. (``4, 16, 36, 64, 100`` is the cycle rank of
    the ``linf`` *1-skeleton*, which is not what a Rips complex reports at
    ``max_degree >= 1``.)

    Examples
    --------
    >>> len(z_lattice(2).ball((0, 0), 2))
    13
    """
    if n < 1:
        raise ValueError(
            f"n must be >= 1, got {n}. Z^0 is a single point and carries no "
            f"lattice structure to scan. Pass n >= 1, e.g. z_lattice(2)."
        )
    if norm not in ("l2", "l1", "linf"):
        raise ValueError(
            f"norm must be 'l2', 'l1' or 'linf', got {norm!r}. The norm decides "
            f"the shape of every ball and therefore the Betti numbers reported, "
            f"so it cannot be guessed. Pass one of the three, e.g. "
            f"z_lattice(2, norm='l2')."
        )
    return _ZLattice(n=n, norm=norm)


class ScanStop(Enum):
    """Why a scan stopped before finishing its radii.

    Each member names a different stage of the pipeline, because the three costs
    are not interchangeable: a ball can be small in points yet dense enough to
    explode combinatorially, and a complex can be modest in simplex count yet
    carry a boundary matrix too large to reduce.
    """

    POINT_CAP = "point_cap"
    DENSITY_CAP = "density_cap"
    BOUNDARY_CAP = "boundary_cap"


@dataclass(frozen=True)
class RipsBettiScan:
    """Betti numbers of Rips complexes on metric balls, one row per radius.

    This records what was computed on **finite** complexes. It makes no claim
    about any infinite complex.
    """

    eps: float
    max_degree: int
    radii: tuple[float, ...]
    betti_z: tuple[tuple[int, ...], ...]
    stopped_at_radius: float | None
    stopped_reason: ScanStop | None


def _flag_complex_size_bound(
    points: Sequence[Any], distance: Any, eps: float, top_dim: int
) -> int:
    """Upper bound on the simplex count of ``Rips_eps`` truncated at ``top_dim``.

    Every ``i``-simplex of a flag complex is a vertex together with an
    ``i``-subset of that vertex's neighbours, so ``sum_v C(deg(v), i)`` bounds the
    ``i``-simplices. Computing it costs one pass over the ``O(n^2)`` distance
    pairs -- far cheaper than the enumeration it guards, and unlike a point count
    it reacts to density: the same 81 points give a bound of ~13k at eps=sqrt(2)
    and ~10^8 at eps=10, where the ball is a single clique.
    """
    n = len(points)
    degrees = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if distance(points[i], points[j]) <= eps:
                degrees[i] += 1
                degrees[j] += 1
    return n + sum(
        math.comb(d, i) for d in degrees for i in range(1, top_dim + 1)
    )


def rips_betti_scan(
    metric: ProperMetric,
    center: Any,
    eps: float,
    radii: Sequence[float],
    max_degree: int,
    *,
    max_points: int = 200,
    max_simplices: int = 20_000,
    max_boundary_dim: int = 400,
) -> RipsBettiScan:
    """Integral Betti numbers of ``Rips_eps`` on balls of the given radii.

    **Makes no claim about the homology of any infinite complex.** A growing
    Betti sequence does not imply a large colimit -- a system with
    ``H_1(K_i) = Z^i`` whose inclusions kill every earlier generator has colimit
    0 -- and this function tests no induced map, so it licenses no rank statement
    in either direction.

    The complex is built to dimension ``max_degree + 1``, because ``H_k`` is
    faithful only when simplices up to dimension ``k+1`` are present. Rows are
    normalised to exactly ``max_degree + 1`` entries, since the raw Betti tuple
    has length ``complex.dimension + 1`` and that varies with the radius.

    Three bounds guard three different stages, and all stop and record rather
    than raising, so partial results survive. ``max_points`` rejects an oversized
    ball before any pairwise work; ``max_simplices`` rejects a *dense* ball using
    a flag-complex size bound read off the 1-skeleton, before construction; and
    ``max_boundary_dim`` rejects a complex too large to reduce. A bound on
    boundary-matrix size alone cannot stop an enumeration blow-up, because the
    matrix shapes are only known after construction -- and a point cap alone
    cannot either, since a 81-point ball at ``eps = 10`` is a single clique whose
    truncated Rips complex has tens of millions of simplices.

    Examples
    --------
    >>> scan = rips_betti_scan(z_lattice(2), (0, 0), 1.0, [1, 2], max_degree=1)
    >>> [row[1] for row in scan.betti_z]
    [0, 4]
    """
    if eps <= 0:
        raise ValueError(
            f"eps must be > 0, got {eps}. At eps <= 0 the Rips complex has no "
            f"edges and every ball would report its own point count as b_0. "
            f"Pass a positive scale, e.g. eps=1.0."
        )
    if max_degree < 0:
        raise ValueError(
            f"max_degree must be >= 0, got {max_degree}. Pass the top homological "
            f"degree you want reported, e.g. max_degree=1 for H_0 and H_1."
        )
    radii = tuple(radii)
    if any(b <= a for a, b in zip(radii, radii[1:], strict=False)):
        raise ValueError(
            f"radii must be strictly increasing, got {radii}. Each radius names a "
            f"larger ball than the last; repeats and reversals make the rows "
            f"impossible to read. Sort and de-duplicate the radii."
        )

    done: list[float] = []
    rows: list[tuple[int, ...]] = []
    stop_radius: float | None = None
    stop_reason: ScanStop | None = None

    for radius in radii:
        points = list(metric.ball(center, radius))
        if len(points) > max_points:
            stop_radius, stop_reason = radius, ScanStop.POINT_CAP
            break
        if (
            _flag_complex_size_bound(points, metric.distance, eps, max_degree + 1)
            > max_simplices
        ):
            stop_radius, stop_reason = radius, ScanStop.DENSITY_CAP
            break
        space = FiniteMetricSpace(carrier=tuple(points), distance=metric.distance)
        filtration = vietoris_rips_filtration(
            space, max_dimension=max_degree + 1, max_scale=eps
        )
        # max_scale=eps keeps the truncated Rips complex face-closed: a face's
        # diameter never exceeds its coface's.
        complex_ = SimplicialComplex(filtration.simplices)
        shapes = [
            boundary_matrix(complex_, k) for k in range(1, complex_.dimension + 1)
        ]
        if any(
            max(len(m), len(m[0]) if m else 0) > max_boundary_dim for m in shapes
        ):
            stop_radius, stop_reason = radius, ScanStop.BOUNDARY_CAP
            break
        raw = betti_numbers(complex_)
        rows.append(
            tuple(raw[k] if k < len(raw) else 0 for k in range(max_degree + 1))
        )
        done.append(radius)

    return RipsBettiScan(
        eps=eps,
        max_degree=max_degree,
        radii=tuple(done),
        betti_z=tuple(rows),
        stopped_at_radius=stop_radius,
        stopped_reason=stop_reason,
    )
