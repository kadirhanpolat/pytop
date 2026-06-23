"""Tests for pytop.seifert — Seifert algorithm, genus bound, matrix, signature.

Reference diagrams
------------------
* **Unknot** (0₁): no crossings → pd=[], signs=[]
* **Trefoil** (3₁, right-handed): 3 negative crossings
  ``pd=[(1,4,2,5),(3,6,4,1),(5,2,6,3)]``, signs=(−1,−1,−1)
* **Figure-eight** (4₁, 4 crossings): standard alternating PD code
  ``pd=[(1,7,2,6),(3,1,4,8),(5,3,6,2),(7,5,8,4)]``, signs=(+1,−1,+1,−1)
* **Hopf link** (2 components, 2 crossings)
  ``pd=[(1,3,2,4),(3,1,4,2)]``, signs=(−1,−1)
* **Cinquefoil** T(2,5) = 5₁: 5 crossings, all negative
"""


from pytop.knot_invariants import KnotDiagram
from pytop.seifert import (
    seifert_circles,
    seifert_genus_bound,
    seifert_matrix,
    signature,
)

# ---------------------------------------------------------------------------
# Reference diagrams
# ---------------------------------------------------------------------------

def unknot() -> KnotDiagram:
    """Unknot: no crossings."""
    return KnotDiagram(pd=[], signs=[])


def trefoil_rh() -> KnotDiagram:
    """Right-handed trefoil (3₁), 3 negative crossings."""
    return KnotDiagram(
        pd=[(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)],
        signs=(-1, -1, -1),
    )


def trefoil_lh() -> KnotDiagram:
    """Left-handed trefoil (mirror of 3₁), 3 positive crossings.

    Uses the reflected PD code (swapping understrand/overstrand at each crossing).
    The arc labelling differs from the right-handed version to give 2 Seifert
    circles under the A-smoothing (positive crossings → A-smoothing).
    """
    return KnotDiagram(
        pd=[(1, 5, 2, 4), (3, 1, 4, 6), (5, 3, 6, 2)],
        signs=(+1, +1, +1),
    )


def figure_eight() -> KnotDiagram:
    """Figure-eight knot (4₁), 4 alternating crossings.

    PD code: X[1,7,2,6], X[3,1,4,8], X[5,3,6,2], X[7,5,8,4]
    This is the standard KnotInfo encoding; signs alternate (+1,−1,+1,−1).
    """
    return KnotDiagram(
        pd=[(1, 7, 2, 6), (3, 1, 4, 8), (5, 3, 6, 2), (7, 5, 8, 4)],
        signs=(+1, -1, +1, -1),
    )


def hopf_link() -> KnotDiagram:
    """Positive Hopf link: 2 crossings, 2 components."""
    return KnotDiagram(
        pd=[(1, 3, 2, 4), (3, 1, 4, 2)],
        signs=(-1, -1),
        components=2,
    )


def cinquefoil() -> KnotDiagram:
    """Torus knot T(2,5) = 5₁, 5 crossings, all negative."""
    return KnotDiagram(
        pd=[(1, 6, 2, 7), (3, 8, 4, 9), (5, 10, 6, 1), (7, 2, 8, 3), (9, 4, 10, 5)],
        signs=(-1, -1, -1, -1, -1),
    )


# ---------------------------------------------------------------------------
# seifert_circles tests
# ---------------------------------------------------------------------------


class TestSeifertCircles:
    def test_unknot_one_circle(self):
        """The unknot (no crossings) has exactly 1 Seifert circle."""
        circles = seifert_circles(unknot())
        assert len(circles) == 1

    def test_unknot_circle_is_empty_arcs(self):
        """The single unknot circle is the empty frozenset (no arc labels)."""
        circles = seifert_circles(unknot())
        assert circles[0] == frozenset()

    def test_trefoil_two_circles(self):
        """The right-handed trefoil diagram (3 negative crossings) yields 2 Seifert circles."""
        circles = seifert_circles(trefoil_rh())
        assert len(circles) == 2

    def test_trefoil_circles_partition_arcs(self):
        """The Seifert circles of the trefoil together cover all 6 arc labels."""
        circles = seifert_circles(trefoil_rh())
        all_arcs = frozenset().union(*circles)
        assert all_arcs == frozenset(range(1, 7))

    def test_trefoil_circles_disjoint(self):
        """Seifert circles must be pairwise disjoint."""
        circles = seifert_circles(trefoil_rh())
        assert circles[0].isdisjoint(circles[1])

    def test_hopf_link_two_circles(self):
        """The Hopf link diagram (2 negative crossings) yields 2 Seifert circles."""
        circles = seifert_circles(hopf_link())
        assert len(circles) == 2

    def test_hopf_link_circles_partition_arcs(self):
        """Hopf link circles together cover all 4 arc labels."""
        circles = seifert_circles(hopf_link())
        all_arcs = frozenset().union(*circles)
        assert all_arcs == frozenset(range(1, 5))

    def test_figure_eight_three_circles(self):
        """The figure-eight knot (4 alternating crossings) yields 3 Seifert circles."""
        circles = seifert_circles(figure_eight())
        assert len(circles) == 3

    def test_figure_eight_circles_partition_arcs(self):
        """Figure-eight circles cover all 8 arc labels."""
        circles = seifert_circles(figure_eight())
        all_arcs = frozenset().union(*circles)
        assert all_arcs == frozenset(range(1, 9))

    def test_lh_trefoil_two_circles(self):
        """Left-handed trefoil (positive crossings) also gives 2 Seifert circles."""
        circles = seifert_circles(trefoil_lh())
        assert len(circles) == 2

    def test_return_type_frozensets(self):
        """Each Seifert circle must be a frozenset."""
        for circle in seifert_circles(trefoil_rh()):
            assert isinstance(circle, frozenset)

    def test_circles_cover_all_arcs(self):
        """Union of all circles equals the full arc label set for non-empty diagrams."""
        for diag in [trefoil_rh(), figure_eight(), cinquefoil()]:
            circles = seifert_circles(diag)
            all_arcs = frozenset().union(*circles)
            expected = frozenset(label for crossing in diag.pd for label in crossing)
            assert all_arcs == expected

    def test_cinquefoil_two_circles(self):
        """T(2,5) cinquefoil yields 2 Seifert circles (all negative crossings)."""
        circles = seifert_circles(cinquefoil())
        assert len(circles) == 2


# ---------------------------------------------------------------------------
# seifert_genus_bound tests
# ---------------------------------------------------------------------------


class TestSeifertGenusBound:
    def test_unknot_genus_zero(self):
        assert seifert_genus_bound(unknot()) == 0

    def test_trefoil_genus_one(self):
        """Right-handed trefoil: c=3, s=2 → g = (3−2+1)//2 = 1."""
        assert seifert_genus_bound(trefoil_rh()) == 1

    def test_trefoil_lh_genus_one(self):
        """Left-handed trefoil (mirror) also has genus bound 1."""
        assert seifert_genus_bound(trefoil_lh()) == 1

    def test_figure_eight_genus_one(self):
        """Figure-eight: c=4, s=3 → g = (4−3+1)//2 = 1."""
        assert seifert_genus_bound(figure_eight()) == 1

    def test_cinquefoil_genus_two(self):
        """T(2,5) cinquefoil: c=5, s=2 → g = (5−2+1)//2 = 2."""
        assert seifert_genus_bound(cinquefoil()) == 2

    def test_genus_nonnegative(self):
        """Genus bound must always be non-negative."""
        for diag in [unknot(), trefoil_rh(), figure_eight(), hopf_link(), cinquefoil()]:
            assert seifert_genus_bound(diag) >= 0

    def test_formula_consistency(self):
        """Verify g = (c − s + 1) // 2 matches the function output."""
        diag = trefoil_rh()
        s = len(seifert_circles(diag))
        c = diag.crossing_number
        expected = (c - s + 1) // 2
        assert seifert_genus_bound(diag) == expected

    def test_formula_consistency_figure_eight(self):
        """Verify formula for figure-eight."""
        diag = figure_eight()
        s = len(seifert_circles(diag))
        c = diag.crossing_number
        expected = (c - s + 1) // 2
        assert seifert_genus_bound(diag) == expected


# ---------------------------------------------------------------------------
# seifert_matrix tests
# ---------------------------------------------------------------------------


class TestSeifertMatrix:
    def test_unknot_empty_matrix(self):
        """The unknot (c=0, s=1, rank=0) gives the empty matrix."""
        M = seifert_matrix(unknot())
        assert M == []

    def test_trefoil_matrix_2x2(self):
        """Trefoil: c=3, s=2, rank=2g=2 → 2×2 Seifert matrix."""
        M = seifert_matrix(trefoil_rh())
        assert len(M) == 2
        assert all(len(row) == 2 for row in M)

    def test_trefoil_matrix_diagonal_negative(self):
        """Trefoil (all negative crossings): diagonal entries are −1."""
        M = seifert_matrix(trefoil_rh())
        assert M[0][0] == -1
        assert M[1][1] == -1

    def test_trefoil_matrix_determinant(self):
        """Trefoil Seifert matrix det = M[0][0]*M[1][1] − M[0][1]*M[1][0].

        The Alexander polynomial of the trefoil is t − 1 + t⁻¹, which
        means |det(M)| = 1.  The standard matrix [[-1,1],[0,-1]] gives det=1.
        """
        M = seifert_matrix(trefoil_rh())
        det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
        assert abs(det) == 1

    def test_trefoil_lh_matrix_diagonal_positive(self):
        """Left-handed trefoil (positive crossings): diagonal entries are +1."""
        M = seifert_matrix(trefoil_lh())
        assert M[0][0] == 1
        assert M[1][1] == 1

    def test_figure_eight_matrix_2x2(self):
        """Figure-eight: c=4, s=3, rank=2g=2 → 2×2 Seifert matrix."""
        M = seifert_matrix(figure_eight())
        assert len(M) == 2
        assert all(len(row) == 2 for row in M)

    def test_seifert_matrix_integer_entries(self):
        """All Seifert matrix entries must be integers."""
        for diag in [trefoil_rh(), figure_eight(), cinquefoil()]:
            M = seifert_matrix(diag)
            for row in M:
                for val in row:
                    assert isinstance(val, int)

    def test_seifert_matrix_square(self):
        """Seifert matrix must be square."""
        for diag in [trefoil_rh(), figure_eight(), cinquefoil()]:
            M = seifert_matrix(diag)
            n = len(M)
            assert all(len(row) == n for row in M)

    def test_seifert_matrix_size_equals_2g(self):
        """Seifert matrix size must equal 2g (twice the genus bound)."""
        for diag in [trefoil_rh(), figure_eight(), cinquefoil()]:
            M = seifert_matrix(diag)
            g = seifert_genus_bound(diag)
            assert len(M) == 2 * g

    def test_cinquefoil_matrix_4x4(self):
        """Cinquefoil T(2,5): genus=2 → 4×4 Seifert matrix."""
        M = seifert_matrix(cinquefoil())
        assert len(M) == 4
        assert all(len(row) == 4 for row in M)


# ---------------------------------------------------------------------------
# signature tests
# ---------------------------------------------------------------------------


class TestSignature:
    def test_unknot_signature_zero(self):
        """Unknot has signature 0 (empty Seifert matrix)."""
        assert signature(unknot()) == 0

    def test_trefoil_rh_signature_negative(self):
        """Right-handed trefoil has signature −2.

        S = M + Mᵀ for the standard trefoil matrix [[-1,1],[0,-1]] is
        [[-2,1],[1,-2]], with eigenvalues −1 and −3 (both negative).
        Signature = 0 − 2 = −2.
        """
        assert signature(trefoil_rh()) == -2

    def test_trefoil_lh_signature_positive(self):
        """Left-handed trefoil has signature +2 (mirror of right-handed)."""
        assert signature(trefoil_lh()) == 2

    def test_figure_eight_signature_zero(self):
        """Figure-eight knot (4₁) is amphichiral, so its signature is 0."""
        assert signature(figure_eight()) == 0

    def test_signature_return_type(self):
        """Signature must be an integer."""
        for diag in [unknot(), trefoil_rh(), figure_eight()]:
            assert isinstance(signature(diag), int)

    def test_mirror_signature_negation(self):
        """Signature of mirror equals negative of original."""
        sig_rh = signature(trefoil_rh())
        sig_lh = signature(trefoil_lh())
        assert sig_rh == -sig_lh

    def test_signature_even(self):
        """The knot signature is always even."""
        for diag in [unknot(), trefoil_rh(), trefoil_lh(), figure_eight()]:
            assert signature(diag) % 2 == 0
