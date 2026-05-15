"""Tests for the v0.1.47 Cilt II completeness corridor record.

These tests verify that:
- Chapter 15 (advanced lane) carries the completeness corridor table tokens;
- the pytop API exposes the four new completeness helpers;
- the examples banks carry the v0.1.47 note;
- the corridor demo notebook cells exist in both target notebooks;
- the roadmap/status/changelog surfaces carry the v0.1.47 record.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Chapter 15 manuscript tokens
# ---------------------------------------------------------------------------

def test_chapter15_completeness_corridor_table_tokens():
    chapter = _read("manuscript/volume_1/chapters/15_metric_spaces.tex")
    for token in (
        "v0.1.47",
        "completeness corridor table",
        "totally bounded witness",
        "metric compactness equivalence",
        "is_complete",
        "is_totally_bounded",
        "metric_compactness_check",
        "analyze_metric_completeness",
    ):
        assert token in chapter, f"{token!r} not found in chapter 15"


def test_chapter15_completeness_corridor_section_exists():
    chapter = _read("manuscript/volume_1/chapters/15_metric_spaces.tex")
    assert "v0.1.47 ileri metrik hat" in chapter
    assert "tamlık" in chapter
    assert "total sınırlılık" in chapter


# ---------------------------------------------------------------------------
# pytop API surface
# ---------------------------------------------------------------------------

def test_pytop_api_exposes_completeness_helpers():
    import pytop
    for name in (
        "is_complete",
        "is_totally_bounded",
        "metric_compactness_check",
        "analyze_metric_completeness",
        "MetricCompletenessError",
    ):
        assert hasattr(pytop, name), f"pytop.{name} not found"
        assert name in pytop.__all__, f"{name!r} not in pytop.__all__"


def test_is_complete_returns_true_for_finite_metric_space():
    from pytop import is_complete
    from pytop.metric_spaces import FiniteMetricSpace

    space = FiniteMetricSpace(
        carrier=[1, 2, 3],
        distance={(1, 2): 1.0, (2, 3): 1.0, (1, 3): 2.0},
    )
    result = is_complete(space)
    assert result.is_true and result.is_exact
    assert result.metadata["operator"] == "is_complete"


def test_is_totally_bounded_returns_true_for_finite_metric_space():
    from pytop import is_totally_bounded
    from pytop.metric_spaces import FiniteMetricSpace

    space = FiniteMetricSpace(
        carrier=[1, 2, 3],
        distance={(1, 2): 1.0, (2, 3): 1.0, (1, 3): 2.0},
    )
    result = is_totally_bounded(space)
    assert result.is_true and result.is_exact
    assert result.metadata["operator"] == "is_totally_bounded"


def test_is_totally_bounded_with_epsilon_records_net():
    from pytop import is_totally_bounded
    from pytop.metric_spaces import FiniteMetricSpace

    space = FiniteMetricSpace(
        carrier=["a", "b"],
        distance={("a", "b"): 1.5},
    )
    result = is_totally_bounded(space, epsilon=0.5)
    assert result.is_true and result.is_exact
    assert result.metadata["epsilon"] == 0.5
    assert result.metadata["net_size"] == 2


def test_metric_compactness_check_links_all_three_conditions():
    from pytop import metric_compactness_check
    from pytop.metric_spaces import FiniteMetricSpace

    space = FiniteMetricSpace(
        carrier=[0, 1],
        distance={(0, 1): 1.0},
    )
    result = metric_compactness_check(space)
    assert result.is_true and result.is_exact
    assert result.metadata["complete"] is True
    assert result.metadata["totally_bounded"] is True
    assert result.metadata["compact"] is True
    assert "cilt_ii_corridor" in result.metadata


def test_analyze_metric_completeness_returns_corridor_record():
    from pytop import analyze_metric_completeness
    from pytop.metric_spaces import FiniteMetricSpace

    space = FiniteMetricSpace(
        carrier=["x", "y", "z"],
        distance={("x", "y"): 1.0, ("y", "z"): 2.0, ("x", "z"): 3.0},
    )
    result = analyze_metric_completeness(space)
    assert result.is_true
    assert result.value["is_complete"] is True
    assert result.value["is_totally_bounded"] is True
    assert result.value["metric_compact"] is True
    assert result.metadata["v0_1_47_corridor_record"] is True


def test_is_complete_returns_symbolic_for_non_metric_space():
    from pytop import is_complete

    class FakeSpace:
        pass

    result = is_complete(FakeSpace())
    assert not result.is_true
    assert result.metadata["operator"] == "is_complete"


# ---------------------------------------------------------------------------
# Examples bank tokens
# ---------------------------------------------------------------------------

def test_complete_metric_examples_carries_v047_note():
    text = _read("examples_bank/complete_metric_examples.md")
    assert "v0.1.47" in text
    assert "completeness corridor table" in text
    assert "is_complete" in text
    assert "is_totally_bounded" in text
    assert "analyze_metric_completeness" in text


def test_basic_invariants_examples_carries_v047_note():
    text = _read("examples_bank/basic_invariants_examples.md")
    assert "v0.1.47" in text
    assert "is_complete" in text
    assert "analyze_metric_completeness" in text


# ---------------------------------------------------------------------------
# Notebook corridor demo cells
# ---------------------------------------------------------------------------

def test_invariant_experiments_notebook_has_v047_cells():
    text = _read("notebooks/research/invariant_experiments.ipynb")
    assert "v0.1.47" in text
    assert "completeness corridor" in text
    assert "analyze_metric_completeness" in text


def test_lesson_06c_notebook_has_v047_cells():
    text = _read("notebooks/teaching/lesson_06c_sequences_and_completeness.ipynb")
    assert "v0.1.47" in text
    assert "completeness corridor" in text
    assert "analyze_metric_completeness" in text


# ---------------------------------------------------------------------------
# Roadmap / status / changelog surfaces
# ---------------------------------------------------------------------------

def test_current_roadmap_records_v047():
    text = _read("docs/roadmap/current_roadmap.md")
    assert "v0.1.47" in text
    assert "completeness corridor table" in text


def test_project_roadmap_records_v047_completed():
    text = _read("PROJECT_ROADMAP.md")
    assert "v0.1.47" in text
    assert "completeness corridor" in text


def test_changelog_records_v047():
    text = _read("CHANGELOG.md")
    assert "v0.1.47" in text
    assert "is_complete" in text
    assert "is_totally_bounded" in text
    assert "metric_compactness_check" in text
    assert "analyze_metric_completeness" in text


def test_pedagogical_volume_map_records_v047():
    text = _read("docs/roadmap/pedagogical_volume_reorganization_map.md")
    assert "v0.1.47 Cilt II completeness corridor record" in text
    assert "is_complete" in text
    assert "analyze_metric_completeness" in text


def test_engelking_roadmap_records_v047_activation():
    text = _read("docs/roadmap/level_based_engelking_integration_roadmap.md")
    assert "v0.1.47" in text
    assert "completeness corridor" in text
