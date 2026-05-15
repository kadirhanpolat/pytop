from pytop.examples import closed_unit_interval_metric, naturals_discrete, naturals_cofinite, real_line_metric, real_plane_metric, reals_cocountable, reals_indiscrete
from pytop.infinite_compactness import is_compact_infinite, is_lindelof_infinite
from pytop.infinite_connectedness import is_connected_infinite, is_path_connected_infinite
from pytop.infinite_countability import is_first_countable_infinite, is_second_countable_infinite, is_separable_infinite
from pytop.infinite_separation import is_hausdorff_infinite, is_t1_infinite


def test_discrete_countable_example_has_exact_infinite_classification():
    space = naturals_discrete()
    assert is_hausdorff_infinite(space).is_exact and is_hausdorff_infinite(space).is_true
    assert is_compact_infinite(space).is_exact and is_compact_infinite(space).is_false
    assert is_second_countable_infinite(space).is_exact and is_second_countable_infinite(space).is_true


def test_indiscrete_example_is_exactly_compact_and_path_connected():
    space = reals_indiscrete()
    assert is_compact_infinite(space).is_exact and is_compact_infinite(space).is_true
    assert is_connected_infinite(space).is_exact and is_connected_infinite(space).is_true
    assert is_path_connected_infinite(space).is_exact and is_path_connected_infinite(space).is_true
    assert is_t1_infinite(space).is_exact and is_t1_infinite(space).is_false


def test_cofinite_example_is_exactly_compact_and_t1():
    space = naturals_cofinite()
    assert is_compact_infinite(space).is_exact and is_compact_infinite(space).is_true
    assert is_t1_infinite(space).is_exact and is_t1_infinite(space).is_true
    assert is_first_countable_infinite(space).is_exact and is_first_countable_infinite(space).is_true


def test_cocountable_example_is_exactly_noncompact_but_lindelof():
    space = reals_cocountable()
    assert is_compact_infinite(space).is_exact and is_compact_infinite(space).is_false
    assert is_lindelof_infinite(space).is_exact and is_lindelof_infinite(space).is_true
    assert is_separable_infinite(space).is_exact and is_separable_infinite(space).is_false


def test_metric_example_still_uses_theorem_mode_when_appropriate():
    space = real_line_metric()
    haus = is_hausdorff_infinite(space)
    sep = is_separable_infinite(space)
    assert haus.is_true
    assert haus.mode in {'exact', 'theorem', 'mixed'}
    assert sep.is_true


def test_closed_interval_and_plane_metric_examples_have_expected_infinite_classification():
    interval = closed_unit_interval_metric()
    plane = real_plane_metric()
    assert is_compact_infinite(interval).is_true
    assert is_second_countable_infinite(interval).is_true
    assert is_compact_infinite(plane).is_false
    assert is_path_connected_infinite(plane).is_true
