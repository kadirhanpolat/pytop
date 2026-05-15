from pytop.comparison import compare_invariants, compare_spaces, finite_homeomorphism_result
from pytop.examples import sierpinski_space, two_point_discrete_space


def test_compare_spaces_reports_cardinality_and_profiles():
    left = two_point_discrete_space()
    right = sierpinski_space()
    report = compare_spaces(left, right)
    assert report['same_cardinality'] is True
    assert 'weight' in report['left_profile']
    assert 'weight' in report['right_profile']


def test_finite_homeomorphism_detects_equal_discrete_spaces():
    left = two_point_discrete_space()
    right = two_point_discrete_space()
    result = finite_homeomorphism_result(left, right)
    assert result.is_true and result.is_exact


def test_finite_homeomorphism_rejects_nonhomeomorphic_pair():
    left = two_point_discrete_space()
    right = sierpinski_space()
    result = finite_homeomorphism_result(left, right)
    assert result.is_false and result.is_exact


def test_compare_invariants_returns_aligned_pairs():
    left = two_point_discrete_space()
    right = sierpinski_space()
    comparison = compare_invariants(left, right)
    assert 'weight' in comparison
    assert isinstance(comparison['weight'], tuple)
