from examples_bank.inverse_systems_examples import (
    example_cantor_binary_tower,
    example_interval_tower,
    example_non_chain_diagnostic,
    inverse_systems_example_api_summary,
    inverse_systems_example_catalog,
)

def test_inverse_system_examples_are_api_compatible() -> None:
    records = inverse_systems_example_catalog()
    assert len(records) == 3
    assert all(record["system"]["system_type"] == "inverse_system" for record in records)
    assert all(record["limit"]["limit_type"] == "inverse_limit" for record in records)
    assert example_interval_tower()["system"]["is_chain_like"] is True
    assert example_cantor_binary_tower()["system"]["space_count"] == 4
    assert example_non_chain_diagnostic()["system"]["is_chain_like"] is False

def test_inverse_system_example_summary_is_actionable() -> None:
    summary = inverse_systems_example_api_summary()
    assert summary["version"] == "0.3.95"
    assert summary["record_count"] == 3
    assert summary["inverse_system_record_count"] == 3
    assert summary["inverse_limit_descriptor_count"] == 3
    assert summary["chain_like_record_count"] == 2
    assert summary["non_chain_record_count"] == 1
    assert "binary-prefix-tower" in summary["catalog_keys"]
