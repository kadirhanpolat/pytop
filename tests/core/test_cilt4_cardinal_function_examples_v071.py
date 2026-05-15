from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from pytop import (  # noqa: E402
    CardinalFunctionExampleError,
    analyze_cardinal_function_examples,
    cardinal_function_example,
    cardinal_function_examples_by_layer,
    cardinal_function_examples_catalog,
    cardinal_function_workbook_tasks,
)


def test_v071_cardinal_function_examples_catalog_has_required_layers():
    catalog = cardinal_function_examples_catalog()
    assert len(catalog) >= 9
    keys = {row["key"] for row in catalog}
    assert {
        "finite_discrete_n",
        "finite_indiscrete_n",
        "second_countable_metric_safe",
        "uncountable_discrete_kappa",
        "sorgenfrey_line_warning",
    } <= keys
    assert {
        "computable_finite",
        "metric_safe_pattern",
        "global_local_warning",
        "classical_reference",
    } <= set(cardinal_function_examples_by_layer())


def test_v071_finite_discrete_record_is_computable_and_not_size_only():
    row = cardinal_function_example("finite_discrete_n")
    assert row["layer"] == "computable_finite"
    assert row["invariant_values"]["weight"] == "n"
    assert row["invariant_values"]["density"] == "n"
    assert any("not answer only |X|" in warning for warning in row["warnings"])


def test_v071_metric_example_keeps_second_countability_explicit():
    row = cardinal_function_example("second_countable_metric_safe")
    assumptions = " ".join(row["assumptions"]).lower()
    warnings = " ".join(row["warnings"]).lower()
    assert "second-countable" in assumptions
    assert "metric does not automatically" in warnings
    assert row["invariant_values"]["weight"] == "aleph_0"


def test_v071_workbook_tasks_flatten_with_source_keys():
    tasks = cardinal_function_workbook_tasks()
    assert len(tasks) >= 20
    assert all("example_key" in task and "task_id" in task for task in tasks)
    finite_tasks = cardinal_function_workbook_tasks("computable_finite")
    assert finite_tasks
    assert all(task["layer"] == "computable_finite" for task in finite_tasks)


def test_v071_v072_analyzer_returns_versioned_result_and_rejects_unknowns():
    result = analyze_cardinal_function_examples()
    assert result.mode == "mixed"
    assert result.metadata["version"] == "0.1.72"
    assert result.metadata["example_count"] >= 9
    assert result.metadata["task_count"] >= 20
    assert analyze_cardinal_function_examples("computable_finite").mode == "exact"
    try:
        cardinal_function_example("missing_example")
    except CardinalFunctionExampleError:
        pass
    else:  # pragma: no cover - explicit failure branch
        raise AssertionError("missing example did not raise")
