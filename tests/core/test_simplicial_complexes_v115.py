from pytop.simplicial_complexes import (
    SimplicialComplex,
    SimplicialComplexError,
    face_closure_diagnostic,
    generated_subcomplex,
    simplicial_complex_summary,
)


def test_generated_triangle_complex_has_expected_faces_and_euler_characteristic():
    triangle = generated_subcomplex([["a", "b", "c"]])

    assert triangle.dimension == 2
    assert triangle.vertices == frozenset(["a", "b", "c"])
    assert triangle.f_vector() == (3, 3, 1)
    assert triangle.euler_characteristic() == 1
    assert len(triangle.facets()) == 1


def test_face_closure_diagnostic_reports_missing_faces():
    diagnostic = face_closure_diagnostic([["a", "b", "c"]])

    assert diagnostic.is_face_closed is False
    assert frozenset(["a"]) in diagnostic.missing_faces
    assert frozenset(["a", "b"]) in diagnostic.missing_faces


def test_non_face_closed_family_can_raise_or_be_inspected():
    try:
        SimplicialComplex([["a", "b", "c"]])
    except SimplicialComplexError:
        pass
    else:
        raise AssertionError("non-face-closed family should raise by default")

    inspected = SimplicialComplex([["a", "b", "c"]], require_face_closed=False)
    assert inspected.dimension == 2


def test_facets_skeleton_and_connectedness_preview_for_small_complex():
    complex_obj = generated_subcomplex([["a", "b", "c"], ["c", "d"]])

    assert {facet.vertices for facet in complex_obj.facets()} == {
        frozenset(["a", "b", "c"]),
        frozenset(["c", "d"]),
    }
    one_skeleton = complex_obj.skeleton(1)
    assert one_skeleton.dimension == 1
    assert one_skeleton.f_vector() == (4, 4)
    preview = complex_obj.connectedness_preview()
    assert preview["connected"] is True
    assert preview["components"] == (frozenset(["a", "b", "c", "d"]),)


def test_summary_records_f_vector_and_one_skeleton_edges():
    complex_obj = generated_subcomplex([["a", "b", "c"]])
    summary = simplicial_complex_summary(complex_obj)

    assert summary["f_vector"] == (3, 3, 1)
    assert summary["euler_characteristic"] == 1
    assert len(summary["one_skeleton_edges"]) == 3
