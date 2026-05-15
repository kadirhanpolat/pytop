from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from pytop import (  # noqa: E402
    CardinalFunctionExampleError,
    analyze_cardinal_function_examples,
    cardinal_function_comparison_exercises,
    cardinal_function_example,
    cardinal_function_notebook_route_alignment,
)


def test_v072_comparison_routes_are_exposed_and_not_empty():
    routes = cardinal_function_comparison_exercises()
    assert len(routes) >= 5
    ids = {route["route_id"] for route in routes}
    assert {
        "weight_vs_density",
        "character_vs_weight",
        "density_vs_cellularity_spread",
        "metric_second_countable_guard",
        "compactness_vs_small_cardinals",
    } <= ids


def test_v072_weight_density_route_links_examples_and_notebooks():
    route = cardinal_function_comparison_exercises("weight_vs_density")
    assert route["comparison_pair"] == ["weight", "density"]
    assert "finite_discrete_n" in route["example_keys"]
    assert "uncountable_discrete_kappa" in route["example_keys"]
    assert route["notebook_route"]["exploration"].endswith("22_cardinal_functions_framework.ipynb")
    assert route["notebook_route"]["teaching"].endswith("lesson_11_cardinal_functions_framework.ipynb")
    assert any("d(X) <= w(X)" in prompt for prompt in route["task_prompts"])


def test_v072_routes_reference_existing_example_records():
    for route in cardinal_function_comparison_exercises():
        assert route["example_keys"], route["route_id"]
        for key in route["example_keys"]:
            row = cardinal_function_example(key)
            assert row["key"] == key


def test_v072_notebook_alignment_is_compact_and_consistent():
    aligned = cardinal_function_notebook_route_alignment()
    assert len(aligned) == len(cardinal_function_comparison_exercises())
    first = aligned[0]
    assert {
        "route_id",
        "comparison_pair",
        "exploration_notebook",
        "teaching_notebook",
        "examples_bank",
        "manuscript_chapter",
        "student_checkpoint",
        "teacher_checkpoint",
    } <= set(first)
    assert all(row["exploration_notebook"].startswith("notebooks/exploration/") for row in aligned)
    assert all(row["teaching_notebook"].startswith("notebooks/teaching/") for row in aligned)


def test_v072_analyzer_includes_comparison_and_route_metadata():
    result = analyze_cardinal_function_examples()
    assert result.metadata["version"] == "0.1.72"
    assert result.metadata["comparison_route_count"] >= 5
    assert "comparison_exercises" in result.value
    assert "notebook_route_alignment" in result.value
    finite = analyze_cardinal_function_examples("computable_finite")
    assert finite.value["comparison_exercises"]


def test_v072_unknown_comparison_route_raises():
    try:
        cardinal_function_comparison_exercises("missing_route")
    except CardinalFunctionExampleError:
        pass
    else:  # pragma: no cover - explicit failure branch
        raise AssertionError("missing comparison route did not raise")
