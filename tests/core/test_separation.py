from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import MetricLikeSpace
from pytop.separation import is_hausdorff, is_t0, is_t1


def test_finite_sierpinski_space_is_t0_not_t1():
    space = FiniteTopologicalSpace(carrier={0, 1}, topology=[set(), {1}, {0, 1}])
    t0 = is_t0(space)
    t1 = is_t1(space)
    assert t0.is_true and t0.is_exact
    assert t1.is_false and t1.is_exact


def test_finite_discrete_space_is_hausdorff():
    space = FiniteTopologicalSpace(carrier={1, 2}, topology=[set(), {1}, {2}, {1, 2}])
    result = is_hausdorff(space)
    assert result.is_true
    assert result.is_exact


def test_metric_space_is_hausdorff_by_theorem():
    space = MetricLikeSpace(carrier="R")
    result = is_hausdorff(space)
    assert result.is_true
    assert result.is_theorem_based


def test_metric_space_is_t1_by_theorem():
    space = MetricLikeSpace(carrier="R")
    result = is_t1(space)
    assert result.is_true
    assert result.is_theorem_based


def test_v055_finite_discrete_space_is_advanced_separation_positive():
    space = FiniteTopologicalSpace(carrier={1, 2}, topology=[set(), {1}, {2}, {1, 2}])
    from pytop.separation import is_regular, is_t3, is_normal, is_t4, is_tychonoff, separation_profile

    assert is_regular(space).is_true and is_regular(space).is_exact
    assert is_t3(space).is_true and is_t3(space).is_exact
    assert is_normal(space).is_true and is_normal(space).is_exact
    assert is_t4(space).is_true and is_t4(space).is_exact
    assert is_tychonoff(space).is_true and is_tychonoff(space).is_exact
    profile = separation_profile(space)
    assert profile["t0"].is_true
    assert profile["t4"].is_true


def test_v055_sierpinski_has_non_t1_advanced_distinctions():
    from pytop.separation import is_regular, is_t3, is_normal, is_t4, is_tychonoff

    space = FiniteTopologicalSpace(carrier={0, 1}, topology=[set(), {1}, {0, 1}])
    assert is_regular(space).is_false and is_regular(space).is_exact
    assert is_t3(space).is_false and is_t3(space).is_exact
    assert is_normal(space).is_true and is_normal(space).is_exact
    assert is_t4(space).is_false and is_t4(space).is_exact
    assert is_tychonoff(space).is_false and is_tychonoff(space).is_exact


def test_v055_metric_space_is_tychonoff_and_normal_by_theorem():
    from pytop.separation import is_normal, is_t4, is_completely_regular, is_tychonoff, advanced_separation_report

    space = MetricLikeSpace(carrier="R")
    assert is_completely_regular(space).is_true and is_completely_regular(space).is_theorem_based
    assert is_tychonoff(space).is_true and is_tychonoff(space).is_theorem_based
    assert is_normal(space).is_true and is_normal(space).is_theorem_based
    assert is_t4(space).is_true and is_t4(space).is_theorem_based
    report = advanced_separation_report(space)
    assert report["hausdorff"].is_true
    assert report["tychonoff"].is_true


def test_v055_cofinite_infinite_space_is_not_advanced_separated():
    from pytop.infinite_spaces import CofiniteSpace
    from pytop.infinite_separation import infinite_separation_report, is_regular_infinite, is_normal_infinite

    space = CofiniteSpace(carrier="N")
    assert is_regular_infinite(space).is_false and is_regular_infinite(space).is_exact
    assert is_normal_infinite(space).is_false and is_normal_infinite(space).is_exact
    report = infinite_separation_report(space)
    assert report["t1"].is_true
    assert report["hausdorff"].is_false
    assert report["t4"].is_false
