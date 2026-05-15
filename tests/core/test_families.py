from pytop.families import (
    is_cover,
    is_disjoint_family,
    is_pairwise_disjoint_family,
    is_partition,
    is_refinement,
    is_subcover,
    normalize_family,
)


def test_normalize_family_produces_frozenset_blocks():
    family = normalize_family([{1, 2}, {3}])
    assert family == (frozenset({1, 2}), frozenset({3}))


def test_cover_and_subcover_are_detected_correctly():
    universe = {1, 2, 3}
    family = [{1, 2}, {2, 3}, {3}]
    subfamily = [{1, 2}, {2, 3}]
    assert is_cover(universe, family)
    assert is_subcover(universe, subfamily, family)


def test_mapping_based_family_inputs_are_supported():
    universe = {1, 2, 3, 4}
    family = {'A': {1, 2}, 'B': {3}, 'C': {4}}
    assert is_cover(universe, family)
    assert is_pairwise_disjoint_family(family)
    assert is_partition(universe, family)


def test_negative_subcover_case_requires_membership_in_reference_family():
    universe = {1, 2, 3}
    family = [{1, 2}, {2, 3}]
    outsider = [{1, 3}, {2}]
    assert not is_subcover(universe, outsider, family)


def test_pairwise_disjoint_family_and_partition_are_distinguished():
    universe = {1, 2, 3, 4}
    partition = [{1, 2}, {3}, {4}]
    non_partition = [{1, 2}, {2, 3}, {4}]
    assert is_pairwise_disjoint_family(partition)
    assert is_disjoint_family(partition)
    assert is_partition(universe, partition)
    assert not is_partition(universe, non_partition)


def test_partition_rejects_empty_blocks_and_missing_coverage():
    universe = {1, 2, 3}
    with_empty_block = [{1}, set(), {2, 3}]
    missing_point = [{1}, {2}]
    assert not is_partition(universe, with_empty_block)
    assert not is_partition(universe, missing_point)


def test_refinement_detects_smaller_cover_blocks():
    candidate = [{1}, {2}, {3, 4}]
    reference = [{1, 2}, {3, 4, 5}]
    assert is_refinement(candidate, reference)
    assert not is_refinement(reference, candidate)


def test_empty_family_is_vacuously_a_refinement():
    assert is_refinement([], [{1, 2}])
