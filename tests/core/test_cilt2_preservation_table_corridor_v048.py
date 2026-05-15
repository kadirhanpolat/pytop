"""Tests for the v0.1.48 Cilt II basic preservation table corridor record."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Chapter 10 manuscript tokens
# ---------------------------------------------------------------------------

def test_chapter10_preservation_table_tokens():
    chapter = _read("manuscript/volume_1/chapters/10_topological_properties_and_invariants.tex")
    for token in (
        "v0.1.48",
        "basic preservation table",
        "preservation corridor",
        "preservation_table_lookup",
        "preservation_table_row",
        "preservation_table_column",
        "analyze_preservation_table",
    ):
        assert token in chapter, f"{token!r} not found in chapter 10"


# ---------------------------------------------------------------------------
# pytop API surface
# ---------------------------------------------------------------------------

def test_pytop_api_exposes_preservation_table_helpers():
    import pytop
    for name in (
        "preservation_table_lookup",
        "preservation_table_row",
        "preservation_table_column",
        "analyze_preservation_table",
    ):
        assert hasattr(pytop, name), f"pytop.{name} not found"
        assert name in pytop.__all__, f"{name!r} not in pytop.__all__"


def test_preservation_table_lookup_compactness_continuous_image():
    from pytop import preservation_table_lookup
    r = preservation_table_lookup("compactness", "continuous_image")
    assert r.is_true and r.is_exact
    assert r.value is True
    assert r.metadata["property"] == "compactness"
    assert r.metadata["construction"] == "continuous_image"


def test_preservation_table_lookup_hausdorff_quotient_false():
    from pytop import preservation_table_lookup
    r = preservation_table_lookup("hausdorff", "quotient")
    assert r.is_false and r.is_exact
    assert r.value is False


def test_preservation_table_lookup_compactness_subspace_conditional():
    from pytop import preservation_table_lookup
    r = preservation_table_lookup("compactness", "subspace")
    assert r.is_exact
    assert r.value == "conditional"
    assert r.metadata.get("condition_required") is True


def test_preservation_table_lookup_connectedness_row_all_true_except_subspace():
    from pytop import preservation_table_lookup
    constructions = ["finite_product", "countable_product", "quotient", "continuous_image"]
    for cons in constructions:
        r = preservation_table_lookup("connectedness", cons)
        assert r.is_true, f"connectedness/{cons} should be preserved"
    r_sub = preservation_table_lookup("connectedness", "subspace")
    assert r_sub.is_false, "connectedness/subspace should NOT be preserved in general"


def test_preservation_table_lookup_hausdorff_subspace_true():
    from pytop import preservation_table_lookup
    r = preservation_table_lookup("hausdorff", "subspace")
    assert r.is_true and r.is_exact


def test_preservation_table_row_returns_all_constructions():
    from pytop import preservation_table_row
    r = preservation_table_row("compactness")
    assert r.is_true and r.is_exact
    assert set(r.value.keys()) == {"subspace", "finite_product", "countable_product", "quotient", "continuous_image"}
    assert r.value["continuous_image"] is True
    assert r.value["subspace"] == "conditional"


def test_preservation_table_column_returns_all_properties():
    from pytop import preservation_table_column
    r = preservation_table_column("subspace")
    assert r.is_true and r.is_exact
    assert set(r.value.keys()) == {"connectedness", "compactness", "hausdorff", "t1", "second_countability"}
    assert r.value["hausdorff"] is True
    assert r.value["connectedness"] is False


def test_analyze_preservation_table_full_summary():
    from pytop import analyze_preservation_table
    r = analyze_preservation_table()
    assert r.is_true
    assert r.metadata["v0_1_48_corridor_record"] is True
    assert "connectedness" in r.value
    assert "hausdorff" in r.value["compactness"] or "continuous_image" in r.value["compactness"]


def test_analyze_preservation_table_single_cell():
    from pytop import analyze_preservation_table
    r = analyze_preservation_table("hausdorff", "subspace")
    assert r.is_true and r.value is True


def test_analyze_preservation_table_row_only():
    from pytop import analyze_preservation_table
    r = analyze_preservation_table("t1")
    assert r.is_true
    assert "quotient" in r.value


def test_analyze_preservation_table_column_only():
    from pytop import analyze_preservation_table
    r = analyze_preservation_table(construction="continuous_image")
    assert r.is_true
    assert "compactness" in r.value


def test_preservation_table_lookup_aliases():
    from pytop import preservation_table_lookup
    # "compact" should alias to "compactness"
    r = preservation_table_lookup("compact", "continuous_image")
    assert r.is_true
    # "t2" should alias to "hausdorff"
    r2 = preservation_table_lookup("t2", "subspace")
    assert r2.is_true


# ---------------------------------------------------------------------------
# Examples bank tokens
# ---------------------------------------------------------------------------

def test_preservation_table_examples_file_exists_with_tokens():
    text = _read("examples_bank/preservation_table_examples.md")
    for token in ("v0.1.48", "basic preservation table", "preservation_table_lookup",
                  "analyze_preservation_table"):
        assert token in text, f"{token!r} not found"


def test_basic_invariants_examples_carries_v048_note():
    text = _read("examples_bank/basic_invariants_examples.md")
    assert "v0.1.48" in text
    assert "preservation_table_lookup" in text


# ---------------------------------------------------------------------------
# Notebook corridor demo cells
# ---------------------------------------------------------------------------

def test_invariant_experiments_notebook_has_v048_cells():
    text = _read("notebooks/research/invariant_experiments.ipynb")
    assert "v0.1.48" in text
    assert "analyze_preservation_table" in text


def test_lesson_03b_notebook_has_v048_cells():
    text = _read("notebooks/teaching/lesson_03b_subspaces_products_quotients.ipynb")
    assert "v0.1.48" in text
    assert "analyze_preservation_table" in text


# ---------------------------------------------------------------------------
# Roadmap / status / changelog surfaces
# ---------------------------------------------------------------------------

def test_current_roadmap_records_v048():
    text = _read("docs/roadmap/current_roadmap.md")
    assert "v0.1.48" in text
    assert "basic preservation table" in text


def test_project_roadmap_records_v048_completed():
    text = _read("PROJECT_ROADMAP.md")
    assert "v0.1.48" in text
    assert "preservation table" in text


def test_changelog_records_v048():
    text = _read("CHANGELOG.md")
    assert "v0.1.48" in text
    assert "preservation_table_lookup" in text
    assert "analyze_preservation_table" in text


def test_pedagogical_volume_map_records_v048():
    text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    assert "v0.1.48 Cilt II basic preservation table corridor record" in text
    assert "preservation_table_lookup" in text


def test_engelking_roadmap_records_v048():
    text = _read("docs/roadmap/level_based_engelking_integration_roadmap.md")
    assert "v0.1.48" in text
