"""Coverage-targeted tests for simplicial_complexes.py (v0.5.1)."""
import pytest
from pytop.simplicial_complexes import (
    SimplicialComplex,
    SimplicialComplexError,
    simplicial_complex,
)


# ---------------------------------------------------------------------------
# SimplicialComplex.__init__ — line 44 (empty simplex family raises)
# ---------------------------------------------------------------------------

def test_empty_simplexes_raises():
    with pytest.raises(SimplicialComplexError, match="at least one nonempty simplex"):
        SimplicialComplex([])


# ---------------------------------------------------------------------------
# SimplicialComplex.skeleton — line 74 (negative dimension raises)
# ---------------------------------------------------------------------------

def test_skeleton_negative_dimension_raises():
    sc = simplicial_complex([[1], [2], [1, 2]])
    with pytest.raises(SimplicialComplexError, match="nonnegative"):
        sc.skeleton(-1)


# ---------------------------------------------------------------------------
# SimplicialComplex.skeleton — line 77 (no simplexes at requested dimension)
# ---------------------------------------------------------------------------

def test_skeleton_no_simplexes_at_dimension_raises():
    # Complex with only 1-simplexes (edges), no 0-simplexes (vertices),
    # require_face_closed=False skips the closure check
    sc = SimplicialComplex([[1, 2], [2, 3]], require_face_closed=False)
    with pytest.raises(SimplicialComplexError, match="no nonempty simplexes"):
        sc.skeleton(0)


# ---------------------------------------------------------------------------
# simplicial_complex — line 138 (convenience constructor return)
# ---------------------------------------------------------------------------

def test_simplicial_complex_convenience_constructor():
    sc = simplicial_complex([[1], [2], [1, 2]])
    assert sc is not None
    assert len(sc.simplexes) == 3
