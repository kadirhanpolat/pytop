from pytop.order_lattice import covering_pairs, hasse_edges, hasse_profile, is_lattice, join, linear_extension, meet
from pytop.order_spaces import poset_space


DIAMOND = {
    (0, 1), (0, 2), (0, 3),
    (1, 3), (2, 3),
}


CHAIN = {
    (1, 2), (2, 3), (1, 3),
}


def test_chain_is_a_lattice_and_has_expected_meets_and_joins():
    space = poset_space((1, 2, 3), CHAIN)
    result = is_lattice(space)
    assert result.is_true
    assert meet(space, 2, 3) == 2
    assert join(space, 1, 2) == 2


def test_diamond_has_expected_covering_pairs_and_linear_extension():
    space = poset_space((0, 1, 2, 3), DIAMOND)
    assert is_lattice(space).is_true
    edges = hasse_edges(space)
    assert edges == {(0, 1), (0, 2), (1, 3), (2, 3)}
    ext = linear_extension(space)
    assert ext[0] == 0
    assert ext[-1] == 3


def test_non_lattice_pair_is_detected():
    space = poset_space((0, 1, 2), {(0, 1), (0, 2)})
    result = is_lattice(space)
    assert result.is_false
    assert result.metadata["failing_pair"] == (1, 2)


def test_covering_pairs_alias_matches_hasse_edges():
    space = poset_space((1, 2, 3), CHAIN)
    assert covering_pairs(space) == hasse_edges(space)


def test_hasse_profile_collects_cover_data_and_linear_extension():
    space = poset_space((0, 1, 2, 3), DIAMOND)
    profile = hasse_profile(space)
    assert profile['carrier_size'] == 4
    assert profile['cover_count'] == 4
    assert profile['covers'] == [(0, 1), (0, 2), (1, 3), (2, 3)]
    assert profile['linear_extension'][0] == 0
