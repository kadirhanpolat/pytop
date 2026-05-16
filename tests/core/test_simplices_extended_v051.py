"""Coverage-targeted tests for simplices.py (v0.5.1)."""
import pytest
from pytop.simplices import (
    Simplex,
    SimplexError,
    simplex,
    validate_simplex,
    simplex_boundary_vertices,
    simplex_summary,
)


# ---------------------------------------------------------------------------
# faces(include_empty=True) → SimplexError  (line 52)
# ---------------------------------------------------------------------------

def test_faces_include_empty_raises():
    s = Simplex([1, 2, 3])
    with pytest.raises(SimplexError, match="empty face"):
        s.faces(include_empty=True)


# ---------------------------------------------------------------------------
# boundary_faces of 0-simplex → empty set  (line 71)
# ---------------------------------------------------------------------------

def test_boundary_faces_vertex_simplex():
    s = Simplex([1])
    assert s.dimension == 0
    assert s.boundary_faces() == set()


def test_boundary_faces_1_simplex():
    s = Simplex([1, 2])
    bf = s.boundary_faces()
    assert len(bf) == 2  # {1} and {2}


def test_boundary_faces_2_simplex():
    s = Simplex([1, 2, 3])
    bf = s.boundary_faces()
    assert len(bf) == 3  # {1,2}, {1,3}, {2,3}


# ---------------------------------------------------------------------------
# simplex() convenience constructor  (line 91)
# ---------------------------------------------------------------------------

def test_simplex_constructor_function():
    s = simplex([1, 2, 3])
    assert isinstance(s, Simplex)
    assert s.dimension == 2


def test_simplex_with_metadata():
    s = simplex([1, 2], metadata={"label": "edge"})
    assert isinstance(s, Simplex)
    assert s.metadata["label"] == "edge"


# ---------------------------------------------------------------------------
# validate_simplex — Simplex instance path (line 98)
# ---------------------------------------------------------------------------

def test_validate_simplex_with_simplex_instance():
    s = Simplex([1, 2])
    assert validate_simplex(s) is True


def test_validate_simplex_with_iterable():
    assert validate_simplex([1, 2, 3]) is True


def test_validate_simplex_empty_iterable():
    assert validate_simplex([]) is False


# ---------------------------------------------------------------------------
# validate_simplex — TypeError path (lines 101-102)
# ---------------------------------------------------------------------------

def test_validate_simplex_unhashable_raises_false():
    # [[1,2]] — nested list is unhashable → frozenset raises TypeError
    assert validate_simplex([[1, 2]]) is False


def test_validate_simplex_non_iterable_raises_false():
    assert validate_simplex(42) is False


# ---------------------------------------------------------------------------
# Existing Simplex functionality — edge cases for full coverage
# ---------------------------------------------------------------------------

def test_simplex_empty_vertices_raises():
    with pytest.raises(SimplexError):
        Simplex([])


def test_simplex_dimension():
    assert Simplex([1]).dimension == 0
    assert Simplex([1, 2]).dimension == 1
    assert Simplex([1, 2, 3]).dimension == 2


def test_simplex_vertex_count():
    s = Simplex([1, 2, 3])
    assert s.vertex_count == 3


def test_simplex_faces_tetrahedron():
    s = Simplex([1, 2, 3, 4])
    # Faces include: itself + triangles + edges + vertices = 1+4+6+4 = 15
    faces = s.faces()
    assert len(faces) == 15


def test_simplex_proper_faces():
    s = Simplex([1, 2, 3])
    proper = s.proper_faces()
    # Should not include the triangle itself
    assert s not in proper
    assert Simplex([1, 2]) in proper


def test_simplex_contains_face_true():
    s = Simplex([1, 2, 3])
    assert s.contains_face(Simplex([1, 2])) is True


def test_simplex_contains_face_false():
    s = Simplex([1, 2])
    assert s.contains_face(Simplex([3])) is False


def test_simplex_face_dimensions():
    s = Simplex([1, 2, 3])
    fd = s.face_dimensions()
    assert fd[0] == 3  # 3 vertices
    assert fd[1] == 3  # 3 edges
    assert fd[2] == 1  # 1 triangle


def test_simplex_boundary_vertices():
    s = Simplex([1, 2, 3])
    bv = simplex_boundary_vertices(s)
    assert frozenset({1, 2}) in bv
    assert frozenset({1, 3}) in bv
    assert frozenset({2, 3}) in bv


def test_simplex_summary_keys():
    s = Simplex([1, 2, 3])
    summary = simplex_summary(s)
    for key in ("vertices", "dimension", "vertex_count", "face_count",
                "proper_face_count", "boundary_face_count", "face_dimensions"):
        assert key in summary
