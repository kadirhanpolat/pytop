from examples_bank.proximity_spaces_examples import (
    example_discrete_proximity,
    example_metric_proximity,
    example_smirnov_descriptor,
    proximity_spaces_example_api_summary,
    proximity_spaces_example_catalog,
)
from pytop.proximity_spaces import is_close, is_proximity_space, smirnov_compactification

def test_proximity_examples_are_api_compatible() -> None:
    records = proximity_spaces_example_catalog()
    assert len(records) == 3
    assert all(is_proximity_space(record) for record in records)
    assert is_close({"a"}, {"a", "b"}, example_metric_proximity()) is True
    assert is_close({"0"}, {"1"}, example_discrete_proximity()) is False
    assert smirnov_compactification(example_smirnov_descriptor())["compactification_type"] == "Smirnov compactification"

def test_proximity_example_summary_is_actionable() -> None:
    summary = proximity_spaces_example_api_summary()
    assert summary["version"] == "0.3.89"
    assert summary["record_count"] == 3
    assert summary["proximity_record_count"] == 3
    assert summary["positive_closeness_checks"] >= 1
    assert summary["negative_closeness_checks"] >= 1
    assert summary["compactification_descriptor_count"] == 3
