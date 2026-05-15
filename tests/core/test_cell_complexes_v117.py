from pytop.cell_complexes import (
    Cell,
    CellComplexError,
    cell,
    cell_complex_profile,
    cell_complex_summary,
    simplex_as_cell_profile,
    validate_finite_cell_profile,
)


def test_cell_complex_profile_records_dimension_counts_and_attaching_text():
    profile = cell_complex_profile(
        "disk_like",
        [
            cell("v", 0, "base 0-cell"),
            cell("e", 1, "1-cell attached with both ends at v"),
            cell("d", 2, "2-cell attached along e"),
        ],
        relation_to_simplicial_complex="filled triangle complex as a disk-like picture",
    )

    assert profile.dimension == 2
    assert profile.cell_count == 3
    assert profile.cell_counts_by_dimension() == {0: 1, 1: 1, 2: 1}
    assert profile.attaching_descriptions()["d"] == "2-cell attached along e"
    assert validate_finite_cell_profile(profile) is True


def test_duplicate_cell_names_are_rejected():
    try:
        cell_complex_profile("bad", [cell("x", 0), cell("x", 1)])
    except CellComplexError:
        pass
    else:
        raise AssertionError("duplicate cell names should be rejected")


def test_negative_dimension_is_rejected():
    try:
        Cell("bad", -1)
    except CellComplexError:
        pass
    else:
        raise AssertionError("negative dimensions should be rejected")


def test_simplex_as_cell_profile_is_teaching_mnemonic_not_validator():
    profile = simplex_as_cell_profile(3)
    summary = cell_complex_summary(profile)

    assert profile.dimension == 3
    assert profile.cell_count == 4
    assert summary["cell_counts_by_dimension"] == {0: 1, 1: 1, 2: 1, 3: 1}
    assert "not a CW validation theorem" in profile.relation_to_simplicial_complex
    assert summary["certification"] == "teaching-profile"


def test_cell_complex_examples_document_scope_and_simplicial_relation():
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    text = (root / "examples_bank" / "cell_complexes_examples.md").read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "not a full CW-complex validator" in text
    assert "Relationship to simplicial complexes" in text
    assert "does not compute homology" in normalized
