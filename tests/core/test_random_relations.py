"""Tests for src/pytop/random_relations.py."""

import pytest

from pytop.random_generators import RandomGeneratorError
from pytop.random_relations import (
    random_equivalence_relation,
    random_partial_order,
    random_reflexive_relation,
    random_symmetric_relation,
    random_total_order,
    random_transitive_relation,
)
from pytop.relations import (
    is_equivalence_relation,
    is_partial_order,
    is_reflexive,
    is_symmetric,
    is_total_order,
    is_transitive,
)

# ===========================================================================
# random_reflexive_relation
# ===========================================================================

class TestRandomReflexiveRelation:
    def setup_method(self):
        self.carrier = [1, 2, 3, 4]

    def test_is_reflexive_for_many_seeds(self):
        for seed in range(20):
            r = random_reflexive_relation(self.carrier, seed=seed)
            assert is_reflexive(self.carrier, r), f"Not reflexive at seed={seed}"

    def test_density_zero_gives_only_diagonal(self):
        r = random_reflexive_relation(self.carrier, density=0.0, seed=0)
        expected = {(x, x) for x in self.carrier}
        assert r == expected

    def test_density_one_gives_full_relation(self):
        r = random_reflexive_relation(self.carrier, density=1.0, seed=0)
        expected = {(x, y) for x in self.carrier for y in self.carrier}
        assert r == expected

    def test_seed_reproducible(self):
        r1 = random_reflexive_relation(self.carrier, seed=42)
        r2 = random_reflexive_relation(self.carrier, seed=42)
        assert r1 == r2

    def test_diagonal_always_present(self):
        for seed in range(10):
            r = random_reflexive_relation(self.carrier, density=0.0, seed=seed)
            for x in self.carrier:
                assert (x, x) in r

    def test_invalid_density_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_reflexive_relation(self.carrier, density=1.5)

    def test_empty_carrier(self):
        r = random_reflexive_relation([], seed=0)
        assert r == set()


# ===========================================================================
# random_symmetric_relation
# ===========================================================================

class TestRandomSymmetricRelation:
    def setup_method(self):
        self.carrier = [1, 2, 3, 4]

    def test_is_symmetric_for_many_seeds(self):
        for seed in range(20):
            r = random_symmetric_relation(self.carrier, seed=seed)
            assert is_symmetric(self.carrier, r), f"Not symmetric at seed={seed}"

    def test_density_zero_gives_empty(self):
        r = random_symmetric_relation(self.carrier, density=0.0, seed=0)
        assert r == set()

    def test_density_one_contains_all_pairs(self):
        r = random_symmetric_relation(self.carrier, density=1.0, seed=0)
        for x in self.carrier:
            for y in self.carrier:
                assert (x, y) in r

    def test_seed_reproducible(self):
        r1 = random_symmetric_relation(self.carrier, seed=7)
        r2 = random_symmetric_relation(self.carrier, seed=7)
        assert r1 == r2

    def test_pairs_are_mirrored(self):
        for seed in range(10):
            r = random_symmetric_relation(self.carrier, seed=seed)
            for (x, y) in r:
                assert (y, x) in r

    def test_invalid_density_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_symmetric_relation(self.carrier, density=-0.1)

    def test_single_element(self):
        r = random_symmetric_relation([42], density=1.0, seed=0)
        assert (42, 42) in r


# ===========================================================================
# random_transitive_relation
# ===========================================================================

class TestRandomTransitiveRelation:
    def setup_method(self):
        self.carrier = [1, 2, 3, 4]

    def test_is_transitive_for_many_seeds(self):
        for seed in range(20):
            r = random_transitive_relation(self.carrier, seed=seed)
            assert is_transitive(self.carrier, r), f"Not transitive at seed={seed}"

    def test_density_zero_gives_empty(self):
        r = random_transitive_relation(self.carrier, density=0.0, seed=0)
        assert r == set()

    def test_density_one_gives_full(self):
        r = random_transitive_relation(self.carrier, density=1.0, seed=0)
        expected = {(x, y) for x in self.carrier for y in self.carrier}
        assert r == expected

    def test_seed_reproducible(self):
        r1 = random_transitive_relation(self.carrier, seed=99)
        r2 = random_transitive_relation(self.carrier, seed=99)
        assert r1 == r2

    def test_invalid_density_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_transitive_relation(self.carrier, density=2.0)

    def test_all_pairs_in_carrier(self):
        r = random_transitive_relation(self.carrier, seed=5)
        for (x, y) in r:
            assert x in self.carrier and y in self.carrier


# ===========================================================================
# random_partial_order
# ===========================================================================

class TestRandomPartialOrder:
    def setup_method(self):
        self.carrier = [1, 2, 3, 4]

    def test_is_partial_order_for_many_seeds(self):
        for seed in range(20):
            r = random_partial_order(self.carrier, seed=seed)
            assert is_partial_order(self.carrier, r), f"Not partial order at seed={seed}"

    def test_diagonal_always_present(self):
        for seed in range(10):
            r = random_partial_order(self.carrier, seed=seed)
            for x in self.carrier:
                assert (x, x) in r

    def test_density_zero_gives_diagonal_only(self):
        r = random_partial_order(self.carrier, density=0.0, seed=0)
        assert r == {(x, x) for x in self.carrier}

    def test_seed_reproducible(self):
        r1 = random_partial_order(self.carrier, seed=11)
        r2 = random_partial_order(self.carrier, seed=11)
        assert r1 == r2

    def test_single_element(self):
        r = random_partial_order([7], seed=0)
        assert r == {(7, 7)}

    def test_invalid_density_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_partial_order(self.carrier, density=-0.5)


# ===========================================================================
# random_total_order
# ===========================================================================

class TestRandomTotalOrder:
    def setup_method(self):
        self.carrier = [1, 2, 3, 4]

    def test_is_total_order_for_many_seeds(self):
        for seed in range(20):
            r = random_total_order(self.carrier, seed=seed)
            assert is_total_order(self.carrier, r), f"Not total order at seed={seed}"

    def test_size_is_n_times_n_plus_1_over_2(self):
        # n=4: reflexive total order has 4 + 4*3/2 = 10 pairs? No: n(n+1)/2 = 10
        n = len(self.carrier)
        r = random_total_order(self.carrier, seed=0)
        assert len(r) == n * (n + 1) // 2

    def test_seed_reproducible(self):
        r1 = random_total_order(self.carrier, seed=55)
        r2 = random_total_order(self.carrier, seed=55)
        assert r1 == r2

    def test_different_seeds_give_different_orders(self):
        results = {frozenset(random_total_order(self.carrier, seed=i)) for i in range(10)}
        assert len(results) > 1

    def test_single_element(self):
        r = random_total_order([5], seed=0)
        assert r == {(5, 5)}

    def test_all_pairs_in_carrier(self):
        r = random_total_order(self.carrier, seed=0)
        for (x, y) in r:
            assert x in self.carrier and y in self.carrier


# ===========================================================================
# random_equivalence_relation
# ===========================================================================

class TestRandomEquivalenceRelation:
    def setup_method(self):
        self.carrier = [1, 2, 3, 4]

    def test_is_equivalence_for_many_seeds(self):
        for seed in range(20):
            r = random_equivalence_relation(self.carrier, seed=seed)
            assert is_equivalence_relation(self.carrier, r), \
                f"Not equivalence at seed={seed}"

    def test_diagonal_always_present(self):
        for seed in range(10):
            r = random_equivalence_relation(self.carrier, seed=seed)
            for x in self.carrier:
                assert (x, x) in r

    def test_seed_reproducible(self):
        r1 = random_equivalence_relation(self.carrier, seed=0)
        r2 = random_equivalence_relation(self.carrier, seed=0)
        assert r1 == r2

    def test_single_element(self):
        r = random_equivalence_relation([9], seed=0)
        assert r == {(9, 9)}

    def test_empty_carrier(self):
        r = random_equivalence_relation([], seed=0)
        assert r == set()

    def test_different_seeds_can_produce_different_partitions(self):
        results = {frozenset(random_equivalence_relation(self.carrier, seed=i))
                   for i in range(20)}
        assert len(results) > 1
