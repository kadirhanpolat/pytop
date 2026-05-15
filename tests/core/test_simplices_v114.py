from pytop.simplices import (
    Simplex,
    SimplexError,
    simplex_boundary_vertices,
    simplex_summary,
    validate_simplex,
)


def test_simplex_dimensions_for_zero_through_three_simplex():
    assert Simplex(["p"]).dimension == 0
    assert Simplex(["a", "b"]).dimension == 1
    assert Simplex(["a", "b", "c"]).dimension == 2
    assert Simplex(["a", "b", "c", "d"]).dimension == 3


def test_faces_and_boundary_faces_for_triangle_are_combinatorial():
    triangle = Simplex(["a", "b", "c"])

    faces = {face.vertices for face in triangle.faces()}
    proper = {face.vertices for face in triangle.proper_faces()}
    boundary = simplex_boundary_vertices(triangle)

    assert len(faces) == 7
    assert frozenset(["a", "b", "c"]) in faces
    assert frozenset(["a", "b", "c"]) not in proper
    assert boundary == {
        frozenset(["a", "b"]),
        frozenset(["a", "c"]),
        frozenset(["b", "c"]),
    }


def test_tetrahedron_summary_counts_faces_by_dimension():
    tetrahedron = Simplex(["a", "b", "c", "d"])
    summary = simplex_summary(tetrahedron)

    assert summary["dimension"] == 3
    assert summary["face_count"] == 15
    assert summary["boundary_face_count"] == 4
    assert summary["face_dimensions"] == {0: 4, 1: 6, 2: 4, 3: 1}


def test_simplex_equality_uses_vertex_set_not_input_order():
    assert Simplex(["a", "b", "c"]) == Simplex(["c", "a", "b"])
    assert Simplex(["a", "b"]).contains_face(["a"])
    assert not Simplex(["a", "b"]).contains_face([])


def test_validation_rejects_empty_vertex_data():
    assert validate_simplex(["x"]) is True
    assert validate_simplex([]) is False
    try:
        Simplex([])
    except SimplexError:
        pass
    else:
        raise AssertionError("empty vertex data should raise SimplexError")
