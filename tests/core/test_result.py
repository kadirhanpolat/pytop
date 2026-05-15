from pytop.result import Result, merge_results


def test_result_summary_contains_mode_and_status():
    result = Result.true(mode="exact", justification=["computed directly"])
    assert result.summary().startswith("true (exact)")


def test_result_to_from_dict_roundtrip():
    original = Result.conditional(
        mode="theorem",
        value="compact",
        assumptions=["X is a closed subspace of a compact space"],
        justification=["closed subspaces of compact spaces are compact"],
    )
    restored = Result.from_dict(original.to_dict())
    assert restored.status == "conditional"
    assert restored.mode == "theorem"
    assert restored.value == "compact"
    assert restored.assumptions == original.assumptions


def test_merge_results_becomes_conditional_on_conflict():
    left = Result.true(mode="exact", value=True)
    right = Result.false(mode="theorem", value=False)
    merged = merge_results(left, right)
    assert merged.status == "conditional"
    assert merged.mode == "mixed"
