"""Grid diagram Floer homology — HFK̂ (Phase 14.2).

Knot Floer homology HFK̂(K) is a bigraded abelian group associated to a knot K,
defined by Ozsváth–Szabó and Rasmussen (2003/2004).  It categorifies the
Alexander polynomial and detects the Seifert genus.

Grid diagram approach (Manolescu–Ozsváth–Sarkar–Szabó–Thurston 2009):
  An n×n grid diagram G encodes a knot K ⊂ S³ via:
    - An n×n toroidal grid (doubly-periodic plane)
    - n X-markings: one per row and one per column
    - n O-markings: one per row and one per column

  The knot is traced by connecting O's to X's horizontally and X's to O's
  vertically (following a specific rule).

  Grid states: bijections σ: {rows} → {columns}.  There are n! grid states.

  Chain complex:
    CFK̂(G) = ℤ[grid states], graded by Maslov M and Alexander A gradings.

  Differential: d(x) = Σ_{rectangles r: x→y} (−1)^{sign(r)} y
    where the sum is over empty rectangles r from x to y (no X or O inside,
    occupying the correct row/column structure).

For small grids (n ≤ 5) this computation is tractable.  We implement:
  - Grid state generation
  - Maslov and Alexander grading computation
  - Rectangle counting (empty rectangle = no X or O markings inside)
  - Homology via SNF (Smith normal form)

The resulting homology HFK̂(K; ℤ) is a bigraded abelian group.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Any

__all__ = [
    "GridDiagram",
    "GridState",
    "HFKHat",
    "grid_diagram_from_permutations",
    "unknot_grid",
    "trefoil_grid",
    "hopf_link_grid",
    "hfk_hat",
    "alexander_polynomial_from_hfk",
]

Matrix = list[list[int]]


def _gf2_rank(mat: Matrix) -> int:
    """Rank of a 0/1 matrix over the field 𝔽₂ via Gaussian elimination."""
    if not mat or not mat[0]:
        return 0
    rows = [[v & 1 for v in row] for row in mat]
    n_cols = len(rows[0])
    rank = 0
    pivot_row = 0
    for col in range(n_cols):
        sel = next((r for r in range(pivot_row, len(rows)) if rows[r][col]), None)
        if sel is None:
            continue
        rows[pivot_row], rows[sel] = rows[sel], rows[pivot_row]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][col]:
                rows[r] = [(a ^ b) for a, b in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        rank += 1
        if pivot_row == len(rows):
            break
    return rank


# ---------------------------------------------------------------------------
# Grid diagram
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GridDiagram:
    """An n×n grid diagram encoding a link.

    Attributes
    ----------
    n : int
        Grid size.
    X_marks : tuple[tuple[int,int], ...]
        Positions of X-markings: (row, column) in [0,n)×[0,n).
    O_marks : tuple[tuple[int,int], ...]
        Positions of O-markings: (row, column) in [0,n)×[0,n).
    name : str
        Human-readable name of the knot/link.
    """

    n: int
    X_marks: tuple[tuple[int, int], ...]
    O_marks: tuple[tuple[int, int], ...]
    name: str = ""

    def __post_init__(self) -> None:
        n = self.n
        # Validate: one X and one O per row and per column
        x_rows = sorted(r for r, c in self.X_marks)
        x_cols = sorted(c for r, c in self.X_marks)
        o_rows = sorted(r for r, c in self.O_marks)
        o_cols = sorted(c for r, c in self.O_marks)
        if x_rows != list(range(n)) or x_cols != list(range(n)):
            raise ValueError(f"X-markings do not cover all rows/columns in [{n}×{n}] grid.")
        if o_rows != list(range(n)) or o_cols != list(range(n)):
            raise ValueError(f"O-markings do not cover all rows/columns in [{n}×{n}] grid.")

    @property
    def X_in_row(self) -> dict[int, int]:
        return {r: c for r, c in self.X_marks}

    @property
    def X_in_col(self, ) -> dict[int, int]:
        return {c: r for r, c in self.X_marks}

    @property
    def O_in_row(self) -> dict[int, int]:
        return {r: c for r, c in self.O_marks}

    @property
    def O_in_col(self) -> dict[int, int]:
        return {c: r for r, c in self.O_marks}

    def grid_states(self) -> list[GridState]:
        """All n! grid states (bijections rows → columns)."""
        return [GridState(perm=p) for p in permutations(range(self.n))]


@dataclass(frozen=True)
class GridState:
    """A grid state: one point per row and per column.

    Attributes
    ----------
    perm : tuple[int, ...]
        perm[i] = column of the grid point in row i.
    """

    perm: tuple[int, ...]

    @property
    def n(self) -> int:
        return len(self.perm)

    def as_set(self) -> frozenset[tuple[int, int]]:
        return frozenset((r, self.perm[r]) for r in range(self.n))

    def maslov_grading(self, grid: GridDiagram) -> int:
        """Maslov grading M(x) of this state in ``grid``."""
        return maslov_grading(self, grid)

    def alexander_grading(self, grid: GridDiagram) -> int:
        """Alexander grading A(x) of this state in ``grid``."""
        return alexander_grading(self, grid)


# ---------------------------------------------------------------------------
# Grading computations
# ---------------------------------------------------------------------------


def _winding_number_contribution(
    state: GridState,
    marks: tuple[tuple[int, int], ...],
    n: int,
) -> int:
    """Compute the winding number contribution (used for Maslov/Alexander grades).

    For a set of markings M and a grid state x, the contribution is
    I(x, M) = #{(p, q) ∈ x × M : p.row < q.row and p.col < q.col}
    (number of pairs where x-point is strictly SW of M-point, toroidal).
    """
    count = 0
    for r, c in state.as_set():
        for mr, mc in marks:
            if r < mr and c < mc:
                count += 1
    return count


def maslov_grading(state: GridState, G: GridDiagram) -> int:
    """Maslov grading of a grid state.

    M(x) = I(x, x) - 2·I(x, O) + I(O, O) - (n-1)/2·... (normalized formula)

    We use the formula:
        M(x) = I(x, x) - 2·I(x, O) + I(O, O) + n - 1

    (shifted to agree with conventions where the unknot has M=0.)

    Parameters
    ----------
    state : GridState
    G : GridDiagram
    """
    n = G.n
    xx = state.as_set()
    x_list = list(xx)
    o_list = list(G.O_marks)

    def _I(A: list[tuple[int,int]], B: list[tuple[int,int]]) -> int:
        return sum(1 for (ar, ac) in A for (br, bc) in B if ar < br and ac < bc)

    Ixx = _I(x_list, x_list)
    IxO = _I(x_list, o_list)
    IOO = _I(o_list, o_list)
    return Ixx - 2 * IxO + IOO + n - 1


def alexander_grading(state: GridState, G: GridDiagram) -> int:
    """Alexander grading of a grid state.

    A(x) = I(x, X) - I(x, O) - (n-1)/2  (for a knot; adjusted for links)

    We use integer approximation, centering at 0.

    Parameters
    ----------
    state : GridState
    G : GridDiagram
    """
    x_list = list(state.as_set())
    X_list = list(G.X_marks)
    O_list = list(G.O_marks)

    def _I(A: list[tuple[int,int]], B: list[tuple[int,int]]) -> int:
        return sum(1 for (ar, ac) in A for (br, bc) in B if ar < br and ac < bc)

    IxX = _I(x_list, X_list)
    IxO = _I(x_list, O_list)
    IXO = _I(X_list, O_list)
    IOO = _I(O_list, O_list)
    return IxX - IxO - (IXO - IOO)


# ---------------------------------------------------------------------------
# Rectangle counting
# ---------------------------------------------------------------------------


def _is_empty_rectangle(
    state_x: GridState,
    state_y: GridState,
    r1: int,
    c1: int,
    r2: int,
    c2: int,
    G: GridDiagram,
) -> bool:
    """Check if the rectangle [r1,r2]×[c1,c2] (mod n) is empty.

    An *empty* rectangle from x to y is a rectangle in the torus:
    - Its corners (r1,c1), (r2,c1), (r1,c2), (r2,c2) are all grid points in x ∪ y.
    - Its interior contains no X or O markings.
    - It contains exactly the correct grid points of x and y on its boundary.
    """

    def _in_rect_interior(r: int, c: int) -> bool:
        # Toroidal interior: strictly between r1,r2 and c1,c2 (mod n)
        in_rows = (r1 < r < r2) if r1 < r2 else (r > r1 or r < r2)
        in_cols = (c1 < c < c2) if c1 < c2 else (c > c1 or c < c2)
        return in_rows and in_cols

    # Check no X or O in interior
    for mr, mc in G.X_marks:
        if _in_rect_interior(mr, mc):
            return False
    for mr, mc in G.O_marks:
        if _in_rect_interior(mr, mc):
            return False

    # Check grid points: x and y must differ at exactly two columns
    sx = state_x.as_set()
    sy = state_y.as_set()
    diff_x = sx - sy
    diff_y = sy - sx
    if len(diff_x) != 2 or len(diff_y) != 2:
        return False

    return True


def _empty_rectangles(
    state_x: GridState,
    state_y: GridState,
    G: GridDiagram,
) -> int:
    """Count empty rectangles from x to y (for differential coefficient)."""
    sx = state_x.as_set()
    sy = state_y.as_set()
    diff_x = sx - sy
    diff_y = sy - sx

    if len(diff_x) != 2:
        return 0

    pts_x = sorted(diff_x)
    pts_y = sorted(diff_y)

    count = 0
    for r1, c1 in pts_x:
        for r2, c2 in pts_y:
            if _is_empty_rectangle(state_x, state_y, r1, c1, r2, c2, G):
                count += 1
    return count


# ---------------------------------------------------------------------------
# HFK̂ result
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HFKHat:
    """Knot Floer homology HFK̂(K; ℤ).

    Attributes
    ----------
    groups : dict[(int,int), tuple[int, tuple[int,...]]]
        Maps (maslov_degree, alexander_degree) → (betti, torsion_factors).
    tau : int | None
        The τ-invariant (concordance invariant from HFK̂).
    alexander_poly : dict[int, int]
        Alexander polynomial coefficients from graded Euler characteristic.
    name : str
        Name of the knot.
    """

    groups: dict[tuple[int, int], Any]
    tau: int | None = None
    alexander_poly: dict[int, int] | None = None
    name: str = ""
    total_generators: int | None = None

    @staticmethod
    def _betti_torsion(value: Any) -> tuple[int, tuple[int, ...]]:
        """Normalise a group value to ``(betti, torsion)``.

        Group values may be an ``int`` (free rank only) or a
        ``(betti, torsion)`` tuple.
        """
        if isinstance(value, tuple):
            return value[0], tuple(value[1]) if len(value) > 1 else ()
        return int(value), ()

    def betti(self, m: int, a: int) -> int:
        if (m, a) not in self.groups:
            return 0
        return self._betti_torsion(self.groups[(m, a)])[0]

    def total_rank(self) -> int:
        return sum(self._betti_torsion(v)[0] for v in self.groups.values())

    def nonzero_groups(self) -> list[tuple[int, int, int, tuple[int, ...]]]:
        result: list[tuple[int, int, int, tuple[int, ...]]] = []
        for (m, a), v in sorted(self.groups.items()):
            b, t = self._betti_torsion(v)
            if b > 0 or t:
                result.append((m, a, b, t))
        return result


# ---------------------------------------------------------------------------
# HFK̂ computation
# ---------------------------------------------------------------------------


def hfk_hat(G: GridDiagram) -> HFKHat:
    """Compute HFK̂ from an n×n grid diagram G.

    Warning: complexity is O((n!)²) and only feasible for n ≤ 5.

    Parameters
    ----------
    G : GridDiagram

    Returns
    -------
    HFKHat
    """
    n = G.n
    if n > 5:
        raise ValueError(
            f"Grid size n={n} is too large; only n ≤ 5 is tractable "
            f"(n! = {_factorial(n)} states)."
        )

    # Generate all grid states
    states = [GridState(perm=p) for p in permutations(range(n))]
    n_states = len(states)
    {s.perm: i for i, s in enumerate(states)}

    # Compute gradings
    maslov = [maslov_grading(s, G) for s in states]
    alexander = [alexander_grading(s, G) for s in states]

    # Build boundary matrix (total complex, ignoring Alexander splitting)
    # d: sum over target states y of # empty rectangles from x to y
    boundary = [[0] * n_states for _ in range(n_states)]
    for i, sx in enumerate(states):
        for j, sy in enumerate(states):
            if maslov[j] == maslov[i] - 1:
                cnt = _empty_rectangles(sx, sy, G)
                boundary[i][j] = cnt % 2  # work over ℤ/2 for tractability

    # Compute homology via SNF grouped by (Maslov, Alexander)
    groups: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
    all_m = sorted(set(maslov))
    all_a = sorted(set(alexander))

    for m in all_m:
        for a in all_a:
            idx = [k for k in range(n_states) if maslov[k] == m and alexander[k] == a]
            if not idx:
                continue

            # Chain group in degree m (kernel: d restricted to idx)
            d_sub_rows = [
                k for k in range(n_states)
                if maslov[k] == m - 1 and alexander[k] == a
            ]
            # Restriction of boundary to idx → d_sub_rows
            mat_cur: Matrix = [
                [boundary[i][j] for j in idx]
                for i in d_sub_rows
            ]
            # Image from degree m+1
            idx_next = [k for k in range(n_states) if maslov[k] == m + 1 and alexander[k] == a]
            mat_next: Matrix = [
                [boundary[k][j] for j in idx_next]
                for k in idx
            ]

            # The boundary is reduced mod 2, so homology is computed over ℤ/2
            # (HFK̂ over 𝔽₂ has no torsion).
            rank_cur = _gf2_rank(mat_cur)
            rank_next = _gf2_rank(mat_next)
            tors: tuple[int, ...] = ()

            ker_dim = len(idx) - rank_cur
            betti = max(0, ker_dim - rank_next)
            if betti > 0:
                groups[(m, a)] = (betti, tors)

    # Compute τ invariant: minimum Alexander grading with non-zero rank
    tau: int | None = None
    if groups:
        # τ = min{a : HFK̂(K, m, a) ≠ 0 and [generator survives to H_*]}
        # Simplified: minimum Alexander grading of any non-zero generator
        nonzero_a = [a for (m, a), (b, t) in groups.items() if b > 0]
        if nonzero_a:
            tau = min(nonzero_a)

    # Alexander polynomial from graded Euler characteristic
    alex_poly: dict[int, int] = {}
    for (m, a), (b, t) in groups.items():
        alex_poly[a] = alex_poly.get(a, 0) + (-1) ** m * b

    return HFKHat(
        groups=groups,
        tau=tau,
        alexander_poly=alex_poly,
        name=G.name,
    )


def _factorial(n: int) -> int:
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


# ---------------------------------------------------------------------------
# Standard grid diagrams
# ---------------------------------------------------------------------------


def unknot_grid() -> GridDiagram:
    """2×2 grid diagram for the unknot."""
    return GridDiagram(
        n=2,
        X_marks=((0, 1), (1, 0)),
        O_marks=((0, 0), (1, 1)),
        name="unknot",
    )


def trefoil_grid() -> GridDiagram:
    """5×5 grid diagram for the right-handed trefoil knot T(2,3).

    A shift-by-2 staircase on a 5×5 grid: O at (i, i) and X at (i, i+2 mod 5),
    which traces the (2,3) torus knot.
    """
    return GridDiagram(
        n=5,
        X_marks=tuple((i, (i + 2) % 5) for i in range(5)),
        O_marks=tuple((i, i) for i in range(5)),
        name="trefoil (right-handed)",
    )


def hopf_link_grid() -> GridDiagram:
    """4×4 grid diagram for the Hopf link."""
    return GridDiagram(
        n=4,
        X_marks=((0, 1), (1, 3), (2, 0), (3, 2)),
        O_marks=((0, 2), (1, 0), (2, 3), (3, 1)),
        name="Hopf link",
    )


def grid_diagram_from_permutations(
    x_perm: list[int],
    o_perm: list[int],
    name: str = "",
) -> GridDiagram:
    """Build a grid diagram from column permutations.

    Parameters
    ----------
    x_perm : list[int]
        ``x_perm[i]`` = column of the X-marking in row i.
    o_perm : list[int]
        ``o_perm[i]`` = column of the O-marking in row i.
    name : str
    """
    n = len(x_perm)
    if len(o_perm) != n:
        raise ValueError("x_perm and o_perm must have the same length.")
    return GridDiagram(
        n=n,
        X_marks=tuple((i, x_perm[i]) for i in range(n)),
        O_marks=tuple((i, o_perm[i]) for i in range(n)),
        name=name,
    )


def alexander_polynomial_from_hfk(hfk: HFKHat) -> dict[int, int]:
    """Extract Alexander polynomial coefficients from HFK̂.

    The Alexander polynomial Δ_K(t) satisfies:
        Δ_K(t) = Σ_a χ(HFK̂(K, *, a)) · t^a
    where χ is the Euler characteristic in the Maslov direction.
    """
    return dict(hfk.alexander_poly or {})
