from pytop.examples import finite_chain_space, naturals_cofinite
from pytop.infinite_image_preimage import SymbolicSubset
from pytop.predicates import is_clopen_subset, is_closed_subset, is_dense_subset, is_nowhere_dense_subset, is_open_subset


def test_finite_open_and_closed_subset_are_detected_exactly():
    space = finite_chain_space(3)
    open_result = is_open_subset(space, {1, 2})
    closed_result = is_closed_subset(space, {3})
    assert open_result.is_true and open_result.is_exact
    assert closed_result.is_true and closed_result.is_exact


def test_finite_subset_can_fail_to_be_clopen():
    space = finite_chain_space(3)
    result = is_clopen_subset(space, {1})
    assert result.is_false and result.is_exact


def test_finite_dense_subset_is_detected_exactly():
    space = finite_chain_space(3)
    result = is_dense_subset(space, {1})
    assert result.is_true and result.is_exact


def test_symbolic_subset_tags_drive_symbolic_subset_predicates():
    space = naturals_cofinite()
    subset = SymbolicSubset(space, 'A', tags={'open', 'dense'})
    assert is_open_subset(space, subset).is_true
    assert is_dense_subset(space, subset).is_true


def test_nowhere_dense_tag_or_exact_result_is_available():
    space = finite_chain_space(3)
    result = is_nowhere_dense_subset(space, {2})
    assert result.is_true and result.is_exact
