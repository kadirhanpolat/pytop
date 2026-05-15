import pytest

from pytop.sets import (
    SetOperationError,
    are_disjoint,
    cartesian_product,
    complement,
    equal_sets,
    indexed_intersection,
    indexed_union,
    is_proper_subset,
    is_subset,
    power_set,
    set_difference,
    set_intersection,
    set_union,
)


def test_subset_and_equality_helpers_match_basic_set_theory():
    assert equal_sets({1, 2}, {2, 1})
    assert is_subset({1}, {1, 2})
    assert is_proper_subset({1}, {1, 2})
    assert not is_proper_subset({1, 2}, {1, 2})


def test_power_set_of_two_points_has_four_members():
    result = power_set({'a', 'b'})
    assert len(result) == 4
    assert frozenset() in result
    assert frozenset({'a', 'b'}) in result


def test_power_set_deduplicates_input_and_matches_two_power_n():
    result = power_set(['a', 'a', 'b', 'c'])
    assert len(result) == 8
    assert frozenset({'a', 'c'}) in result


def test_basic_set_operations_and_disjointness_work_as_expected():
    assert set_union({1, 2}, {2, 3}) == {1, 2, 3}
    assert set_intersection({1, 2}, {2, 3}) == {2}
    assert set_difference({1, 2, 3}, {2}) == {1, 3}
    assert complement({1, 2}, {1, 2, 3, 4}) == {3, 4}
    assert are_disjoint({1, 2}, {3, 4})
    assert not are_disjoint({1, 2}, {2, 3})


def test_set_algebra_laws_hold_on_small_finite_example():
    a = {1, 2}
    b = {2, 3}
    c = {2, 4}
    assert set_union(a, b) == set_union(b, a)
    assert set_intersection(a, b) == set_intersection(b, a)
    assert set_union(set_union(a, b), c) == set_union(a, set_union(b, c))
    assert set_intersection(set_intersection(a, b), c) == set_intersection(a, set_intersection(b, c))
    assert set_intersection(a, set_union(b, c)) == set_union(set_intersection(a, b), set_intersection(a, c))
    assert set_union(a, set_intersection(b, c)) == set_intersection(set_union(a, b), set_union(a, c))


def test_de_morgan_and_subset_criteria_hold_relative_to_a_fixed_universe():
    universe = {1, 2, 3, 4, 5}
    a = {1, 2, 3}
    b = {3, 4}
    left = complement(set_union(a, b), universe)
    right = set_intersection(complement(a, universe), complement(b, universe))
    assert left == right
    left = complement(set_intersection(a, b), universe)
    right = set_union(complement(a, universe), complement(b, universe))
    assert left == right
    assert is_subset(a, universe)
    assert set_intersection(a, universe) == a
    assert set_union(a, universe) == universe
    assert set_difference(a, universe) == set()
    assert is_subset(complement(universe, universe), complement(a, universe))


def test_complement_rejects_non_subset_of_universe():
    with pytest.raises(SetOperationError):
        complement({1, 4}, {1, 2, 3})


def test_indexed_union_and_intersection_accept_mappings():
    family = {
        'U1': {1, 2, 3},
        'U2': {2, 3},
        'U3': {3, 4},
    }
    assert indexed_union(family) == {1, 2, 3, 4}
    assert indexed_intersection(family) == {3}


def test_indexed_operators_accept_plain_iterables_and_empty_families():
    family = [{1, 2}, {2, 3}, {2, 4}]
    assert indexed_union(family) == {1, 2, 3, 4}
    assert indexed_intersection(family) == {2}
    assert indexed_union([]) == set()
    assert indexed_intersection([]) == set()


def test_cartesian_product_is_explicit():
    assert cartesian_product({1, 2}, {'x'}) == {(1, 'x'), (2, 'x')}
