"""Tests for src/pytop/random_functions.py."""

import pytest

from pytop.random_functions import (
    _check_closed_map,
    _check_continuous,
    _check_open_map,
    random_bijection,
    random_closed_map,
    random_continuous_function,
    random_homeomorphism,
    random_injective_function,
    random_open_map,
    random_surjective_function,
)
from pytop.random_generators import RandomGeneratorError
from pytop.random_generators import random_topology
from pytop.topology_builders import discrete_topology, indiscrete_topology


# ===========================================================================
# random_injective_function
# ===========================================================================

class TestRandomInjectiveFunction:
    def test_all_values_distinct(self):
        f = random_injective_function([1, 2, 3], [10, 20, 30, 40, 50], seed=0)
        assert len(set(f.values())) == 3

    def test_keys_equal_domain(self):
        domain = [1, 2, 3, 4]
        f = random_injective_function(domain, list(range(10)), seed=1)
        assert set(f.keys()) == set(domain)

    def test_values_in_codomain(self):
        codomain = ["a", "b", "c", "d", "e"]
        f = random_injective_function([1, 2], codomain, seed=2)
        assert all(v in codomain for v in f.values())

    def test_seed_reproducible(self):
        f1 = random_injective_function([1, 2, 3], [10, 20, 30, 40], seed=42)
        f2 = random_injective_function([1, 2, 3], [10, 20, 30, 40], seed=42)
        assert f1 == f2

    def test_raises_when_codomain_too_small(self):
        with pytest.raises(RandomGeneratorError):
            random_injective_function([1, 2, 3, 4], [10, 20], seed=0)

    def test_empty_domain_returns_empty_dict(self):
        f = random_injective_function([], [1, 2, 3], seed=0)
        assert f == {}

    def test_equal_sizes_is_bijection(self):
        domain = [1, 2, 3]
        codomain = [10, 20, 30]
        f = random_injective_function(domain, codomain, seed=5)
        assert set(f.values()) == set(codomain)


# ===========================================================================
# random_surjective_function
# ===========================================================================

class TestRandomSurjectiveFunction:
    def test_every_codomain_element_hit(self):
        domain = list(range(10))
        codomain = ["a", "b", "c"]
        f = random_surjective_function(domain, codomain, seed=0)
        assert set(f.values()) == set(codomain)

    def test_keys_equal_domain(self):
        domain = [1, 2, 3, 4, 5]
        f = random_surjective_function(domain, [10, 20], seed=1)
        assert set(f.keys()) == set(domain)

    def test_seed_reproducible(self):
        f1 = random_surjective_function([1, 2, 3, 4], [10, 20], seed=7)
        f2 = random_surjective_function([1, 2, 3, 4], [10, 20], seed=7)
        assert f1 == f2

    def test_raises_when_domain_too_small(self):
        with pytest.raises(RandomGeneratorError):
            random_surjective_function([1, 2], [10, 20, 30], seed=0)

    def test_raises_when_codomain_empty(self):
        with pytest.raises(RandomGeneratorError):
            random_surjective_function([1, 2, 3], [], seed=0)

    def test_equal_sizes_is_bijection(self):
        domain = [1, 2, 3]
        codomain = [10, 20, 30]
        f = random_surjective_function(domain, codomain, seed=9)
        assert set(f.values()) == set(codomain)
        assert len(set(f.values())) == len(codomain)


# ===========================================================================
# random_bijection
# ===========================================================================

class TestRandomBijection:
    def test_is_injective(self):
        f = random_bijection([1, 2, 3, 4], [10, 20, 30, 40], seed=0)
        assert len(set(f.values())) == 4

    def test_is_surjective(self):
        codomain = [10, 20, 30, 40]
        f = random_bijection([1, 2, 3, 4], codomain, seed=1)
        assert set(f.values()) == set(codomain)

    def test_seed_reproducible(self):
        f1 = random_bijection([1, 2, 3], [10, 20, 30], seed=42)
        f2 = random_bijection([1, 2, 3], [10, 20, 30], seed=42)
        assert f1 == f2

    def test_raises_on_size_mismatch(self):
        with pytest.raises(RandomGeneratorError):
            random_bijection([1, 2, 3], [10, 20], seed=0)

    def test_empty_domain_and_codomain(self):
        f = random_bijection([], [], seed=0)
        assert f == {}

    def test_single_element(self):
        f = random_bijection([1], [99], seed=0)
        assert f == {1: 99}


# ===========================================================================
# random_continuous_function
# ===========================================================================

class TestRandomContinuousFunction:
    def setup_method(self):
        self.X = random_topology([1, 2, 3], seed=0)
        self.Y = random_topology([10, 20], seed=1)

    def test_result_is_continuous(self):
        for seed in range(10):
            f = random_continuous_function(self.X, self.Y, seed=seed)
            assert _check_continuous(f, self.X, self.Y), \
                f"Not continuous at seed={seed}"

    def test_seed_reproducible(self):
        f1 = random_continuous_function(self.X, self.Y, seed=42)
        f2 = random_continuous_function(self.X, self.Y, seed=42)
        assert f1 == f2

    def test_keys_equal_domain_carrier(self):
        f = random_continuous_function(self.X, self.Y, seed=5)
        assert set(f.keys()) == set(self.X.carrier)

    def test_values_in_codomain_carrier(self):
        f = random_continuous_function(self.X, self.Y, seed=5)
        assert all(v in self.Y.carrier for v in f.values())

    def test_discrete_domain_always_succeeds(self):
        # Any function from discrete space is continuous
        X = discrete_topology(1, 2, 3)
        Y = random_topology([10, 20], seed=2)
        f = random_continuous_function(X, Y, seed=0)
        assert _check_continuous(f, X, Y)

    def test_indiscrete_codomain_always_succeeds(self):
        # Any function to indiscrete space is continuous
        X = random_topology([1, 2, 3], seed=0)
        Y = indiscrete_topology(10, 20, 30)
        f = random_continuous_function(X, Y, seed=0)
        assert _check_continuous(f, X, Y)

    def test_raises_when_codomain_empty(self):
        X = random_topology([1, 2], seed=0)
        Y = random_topology([], seed=0)
        with pytest.raises(RandomGeneratorError):
            random_continuous_function(X, Y, seed=0)

    def test_lazy_topology_domain(self):
        from pytop.random_generators import LazyTopology
        X = LazyTopology(
            carrier=frozenset({1, 2, 3, 4, 5, 6}),
            subbasis=frozenset([frozenset({1, 2}), frozenset({3, 4})]),
        )
        Y = random_topology([10, 20], seed=0)
        f = random_continuous_function(X, Y, seed=0)
        assert _check_continuous(f, X, Y)


# ===========================================================================
# random_open_map
# ===========================================================================

class TestRandomOpenMap:
    def setup_method(self):
        # Discrete codomain: every subset is open, so any function is an open map
        self.X = random_topology([1, 2, 3], seed=0)
        self.Y = discrete_topology(10, 20, 30)

    def test_result_is_open_map(self):
        for seed in range(10):
            f = random_open_map(self.X, self.Y, seed=seed)
            assert _check_open_map(f, self.X, self.Y), \
                f"Not open map at seed={seed}"

    def test_seed_reproducible(self):
        f1 = random_open_map(self.X, self.Y, seed=3)
        f2 = random_open_map(self.X, self.Y, seed=3)
        assert f1 == f2

    def test_discrete_codomain_always_succeeds(self):
        # Image of any set lands in discrete codomain (every set is open)
        X = random_topology([1, 2, 3], seed=0)
        Y = discrete_topology(10, 20, 30)
        f = random_open_map(X, Y, seed=0)
        assert _check_open_map(f, X, Y)

    def test_raises_when_codomain_empty(self):
        X = random_topology([1, 2], seed=0)
        Y = random_topology([], seed=0)
        with pytest.raises(RandomGeneratorError):
            random_open_map(X, Y, seed=0)


# ===========================================================================
# random_closed_map
# ===========================================================================

class TestRandomClosedMap:
    def setup_method(self):
        self.X = random_topology([1, 2, 3], seed=0)
        self.Y = random_topology([10, 20, 30], seed=1)

    def test_result_is_closed_map(self):
        for seed in range(10):
            f = random_closed_map(self.X, self.Y, seed=seed)
            assert _check_closed_map(f, self.X, self.Y), \
                f"Not closed map at seed={seed}"

    def test_seed_reproducible(self):
        f1 = random_closed_map(self.X, self.Y, seed=8)
        f2 = random_closed_map(self.X, self.Y, seed=8)
        assert f1 == f2

    def test_discrete_codomain_always_succeeds(self):
        X = random_topology([1, 2, 3], seed=0)
        Y = discrete_topology(10, 20, 30)
        f = random_closed_map(X, Y, seed=0)
        assert _check_closed_map(f, X, Y)

    def test_raises_when_codomain_empty(self):
        X = random_topology([1, 2], seed=0)
        Y = random_topology([], seed=0)
        with pytest.raises(RandomGeneratorError):
            random_closed_map(X, Y, seed=0)


# ===========================================================================
# random_homeomorphism
# ===========================================================================

class TestRandomHomeomorphism:
    def test_two_discrete_spaces_same_size(self):
        X = discrete_topology(1, 2, 3)
        Y = discrete_topology(10, 20, 30)
        f = random_homeomorphism(X, Y, seed=0)
        assert _check_continuous(f, X, Y)
        assert _check_open_map(f, X, Y)
        assert len(set(f.values())) == 3  # bijective

    def test_two_indiscrete_spaces_same_size(self):
        X = indiscrete_topology(1, 2, 3)
        Y = indiscrete_topology(10, 20, 30)
        f = random_homeomorphism(X, Y, seed=0)
        assert _check_continuous(f, X, Y)
        assert _check_open_map(f, X, Y)

    def test_seed_reproducible(self):
        X = discrete_topology(1, 2, 3)
        Y = discrete_topology(10, 20, 30)
        f1 = random_homeomorphism(X, Y, seed=77)
        f2 = random_homeomorphism(X, Y, seed=77)
        assert f1 == f2

    def test_raises_on_carrier_size_mismatch(self):
        X = discrete_topology(1, 2, 3)
        Y = discrete_topology(10, 20)
        with pytest.raises(RandomGeneratorError):
            random_homeomorphism(X, Y, seed=0)

    def test_result_is_bijective(self):
        X = discrete_topology(1, 2, 3)
        Y = discrete_topology(10, 20, 30)
        f = random_homeomorphism(X, Y, seed=5)
        assert len(set(f.values())) == len(X.carrier)

    def test_non_homeomorphic_spaces_raises(self):
        # Discrete 3-point space vs indiscrete 3-point space: not homeomorphic
        # (discrete is T1, indiscrete is not T1 for n>=2)
        X = discrete_topology(1, 2, 3)
        Y = indiscrete_topology(10, 20, 30)
        with pytest.raises(RandomGeneratorError):
            random_homeomorphism(X, Y, seed=0, max_attempts=200)
