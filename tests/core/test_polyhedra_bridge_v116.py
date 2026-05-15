from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_polyhedra_examples_connect_code_surfaces_and_core_terms():
    text = (ROOT / "examples_bank" / "polyhedra_examples.md").read_text(encoding="utf-8")

    required = [
        "Simplex",
        "SimplicialComplex",
        "polyhedron intuition",
        "subdivision",
        "geometric intuition",
        "Topological space versus combinatorial model",
        "generated_subcomplex",
        "f_vector",
        "euler_characteristic",
    ]
    for term in required:
        assert term in text


def test_polyhedra_bridge_keeps_deferred_topics_out_of_scope():
    text = (ROOT / "examples_bank" / "polyhedra_examples.md").read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "does not enter PL-topology classification or homology" in text
    assert "does not claim to decide when two complexes have homeomorphic realizations" in normalized
    assert "book text, exercises, examples, or proofs" in normalized


def test_manuscript_bridge_note_records_scope_and_deferred_topics():
    note = (ROOT / "manuscript" / "volume_6" / "geometric_polyhedra_bridge_note.md").read_text(encoding="utf-8")

    assert "src/pytop/simplices.py" in note
    assert "src/pytop/simplicial_complexes.py" in note
    assert "examples_bank/polyhedra_examples.md" in note
    assert "homology" in note
    assert "PL classification" in note


def test_polyhedra_examples_code_snippets_match_current_api():
    import sys

    sys.path.insert(0, str(ROOT / "src"))
    from pytop.simplicial_complexes import generated_subcomplex

    filled_triangle = generated_subcomplex([["a", "b", "c"]])
    boundary = generated_subcomplex([["a", "b"], ["b", "c"], ["a", "c"]])
    subdivided_edge = generated_subcomplex([["a", "m"], ["m", "b"]])

    assert filled_triangle.f_vector() == (3, 3, 1)
    assert boundary.f_vector() == (3, 3)
    assert boundary.connectedness_preview()["connected"] is True
    assert subdivided_edge.f_vector() == (3, 2)
