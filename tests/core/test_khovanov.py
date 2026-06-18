"""Known-answer and structural tests for Khovanov homology.

``khovanov_homology(diagram)`` returns the bigraded integral Khovanov homology
``Kh^{i,j}`` (free rank + torsion per bidegree).  Tests pin the standard small
diagrams (unknot, trefoil, figure-eight, Hopf link) against their published
integral Khovanov groups — including the ℤ/2 torsion — and check the two
defining structural properties:

* ``d² = 0`` (the cube differential is a cochain complex),
* the graded Euler characteristic equals the unnormalised Jones polynomial,
  cross-checked against pytop's :func:`jones_polynomial`.
"""

from __future__ import annotations

from pytop import KhovanovHomology, khovanov_homology
from pytop.knot_invariants import KnotDiagram, jones_polynomial
from pytop.khovanov import _khovanov_complex

# Diagrams (PD codes + signs).  Signs fix only the (n₊, n₋) grading shift.
UNKNOT = KnotDiagram([], signs=())
TREFOIL = KnotDiagram([(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)], signs=(-1, -1, -1))
FIGURE_EIGHT = KnotDiagram(
    [(4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)], signs=(1, -1, 1, -1)
)
HOPF = KnotDiagram([(1, 4, 2, 3), (3, 2, 4, 1)], signs=(1, 1), components=2)


def _d_squared_is_zero(diagram: KnotDiagram) -> bool:
    _elements, differentials = _khovanov_complex(diagram)
    for (i, j), lower in differentials.items():
        upper = differentials.get((i + 1, j))
        if not upper:
            continue
        inner, cols = len(lower), len(lower[0]) if lower else 0
        for r in range(len(upper)):
            for c in range(cols):
                if sum(upper[r][k] * lower[k][c] for k in range(inner)) != 0:
                    return False
    return True


def _expected_euler(diagram: KnotDiagram) -> dict[int, int]:
    """``(−1)^{c−1} (q + q⁻¹) · V(t = q²)`` as ``{q-power: coeff}``."""
    components = diagram.components
    sign = -1 if components % 2 == 0 else 1
    out: dict[int, int] = {}
    for power, coeff in jones_polynomial(diagram).coeffs.items():
        q_power = int(2 * power)
        for shift in (1, -1):
            out[q_power + shift] = out.get(q_power + shift, 0) + sign * coeff
    return {k: v for k, v in out.items() if v != 0}


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


class TestKhovanovHomologyType:
    def test_accessors(self):
        kh = KhovanovHomology({(0, 1): (1, ()), (3, 7): (0, (2,))})
        assert kh.free_rank(0, 1) == 1
        assert kh.free_rank(9, 9) == 0
        assert kh.torsion(3, 7) == (2,)
        assert kh.total_rank() == 1

    def test_graded_euler_characteristic(self):
        kh = KhovanovHomology({(0, 1): (1, ()), (0, 3): (1, ()), (2, 5): (1, ())})
        assert kh.graded_euler_characteristic() == {1: 1, 3: 1, 5: 1}


# ---------------------------------------------------------------------------
# Known integral Khovanov groups
# ---------------------------------------------------------------------------


class TestKnownGroups:
    def test_unknot(self):
        assert khovanov_homology(UNKNOT).groups == {(0, 1): (1, ()), (0, -1): (1, ())}

    def test_trefoil_with_z2_torsion(self):
        # Left-handed trefoil (pytop encodes it with three negative crossings):
        # free ℤ at (0,−1),(0,−3),(−2,−5),(−3,−9); ℤ/2 torsion at (−2,−7).
        assert khovanov_homology(TREFOIL).groups == {
            (0, -1): (1, ()),
            (0, -3): (1, ()),
            (-2, -5): (1, ()),
            (-2, -7): (0, (2,)),
            (-3, -9): (1, ()),
        }

    def test_figure_eight(self):
        # Amphichiral: symmetric free part, ℤ/2 torsion at (−1,−3) and (2,3).
        assert khovanov_homology(FIGURE_EIGHT).groups == {
            (-2, -5): (1, ()),
            (-1, -3): (0, (2,)),
            (-1, -1): (1, ()),
            (0, -1): (1, ()),
            (0, 1): (1, ()),
            (1, 1): (1, ()),
            (2, 3): (0, (2,)),
            (2, 5): (1, ()),
        }

    def test_hopf_link(self):
        # Positive Hopf link: four free ℤ, no torsion.
        assert khovanov_homology(HOPF).groups == {
            (0, 0): (1, ()),
            (0, 2): (1, ()),
            (2, 4): (1, ()),
            (2, 6): (1, ()),
        }

    def test_total_ranks(self):
        assert khovanov_homology(UNKNOT).total_rank() == 2
        assert khovanov_homology(TREFOIL).total_rank() == 4
        assert khovanov_homology(FIGURE_EIGHT).total_rank() == 6
        assert khovanov_homology(HOPF).total_rank() == 4


# ---------------------------------------------------------------------------
# Structural properties
# ---------------------------------------------------------------------------


class TestStructure:
    def test_differential_squares_to_zero(self):
        assert _d_squared_is_zero(TREFOIL)
        assert _d_squared_is_zero(FIGURE_EIGHT)
        assert _d_squared_is_zero(HOPF)

    def test_euler_characteristic_is_jones_trefoil(self):
        kh = khovanov_homology(TREFOIL)
        assert kh.graded_euler_characteristic() == _expected_euler(TREFOIL)

    def test_euler_characteristic_is_jones_figure_eight(self):
        kh = khovanov_homology(FIGURE_EIGHT)
        assert kh.graded_euler_characteristic() == _expected_euler(FIGURE_EIGHT)

    def test_euler_characteristic_is_jones_hopf(self):
        kh = khovanov_homology(HOPF)
        assert kh.graded_euler_characteristic() == _expected_euler(HOPF)

    def test_hopf_euler_characteristic_explicit(self):
        # The positive Hopf link's Khovanov–Jones is q⁰ + q² + q⁴ + q⁶.
        assert khovanov_homology(HOPF).graded_euler_characteristic() == {
            0: 1,
            2: 1,
            4: 1,
            6: 1,
        }
