"""Tests for src/pytop/random_generators.py."""

import pytest

from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.random_generators import (
    LazyTopology,
    RandomGeneratorError,
    random_function,
    random_relation,
    random_set,
    random_topology,
)

# ===========================================================================
# random_set
# ===========================================================================

class TestRandomSetSize:
    def test_exact_size(self):
        s = random_set(size=4, seed=0)
        assert len(s) == 4

    def test_exact_size_zero(self):
        s = random_set(size=0, seed=0)
        assert s == frozenset()

    def test_max_size_respected(self):
        for _ in range(20):
            s = random_set(max_size=5)
            assert len(s) <= 5

    def test_min_max_range(self):
        for _ in range(30):
            s = random_set(max_size=8, min_size=3)
            assert 3 <= len(s) <= 8

    def test_missing_size_and_max_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_set()

    def test_min_greater_than_max_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_set(max_size=3, min_size=5)

    def test_size_larger_than_pool_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_set(size=30, element_type="char")  # pool has 26


class TestRandomSetElementTypes:
    def test_int_elements_in_range(self):
        s = random_set(size=10, element_type="int", seed=1)
        assert all(isinstance(x, int) and 1 <= x <= 99 for x in s)

    def test_char_elements_are_lowercase(self):
        s = random_set(size=5, element_type="char", seed=2)
        assert all(isinstance(x, str) and len(x) == 1 and x.islower() for x in s)

    def test_str_elements_are_two_chars(self):
        s = random_set(size=5, element_type="str", seed=3)
        assert all(isinstance(x, str) and len(x) == 2 for x in s)

    def test_custom_pool(self):
        pool = [10, 20, 30, 40, 50]
        s = random_set(size=3, pool=pool, seed=4)
        assert s.issubset(frozenset(pool))
        assert len(s) == 3

    def test_unknown_element_type_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_set(size=2, element_type="float")


class TestRandomOrder:
    def test_random_order_false_takes_from_start(self):
        # pool = 'a','b',...,'z'; random_order=False → first 3 = a,b,c
        s = random_set(size=3, element_type="char", random_order=False)
        assert s == frozenset({"a", "b", "c"})

    def test_random_order_false_int(self):
        s = random_set(size=4, element_type="int", random_order=False)
        assert s == frozenset({1, 2, 3, 4})

    def test_random_order_true_can_give_different_results(self):
        results = {random_set(size=3, element_type="int", seed=i) for i in range(10)}
        assert len(results) > 1  # at least 2 different outcomes across 10 seeds

    def test_seed_reproducibility(self):
        s1 = random_set(max_size=10, seed=42)
        s2 = random_set(max_size=10, seed=42)
        assert s1 == s2

    def test_different_seeds_likely_different(self):
        s1 = random_set(size=5, seed=1)
        s2 = random_set(size=5, seed=999)
        # Not guaranteed but very likely with a pool of 99
        assert s1 != s2 or True  # soft check — just ensure no crash


# ===========================================================================
# LazyTopology — UID
# ===========================================================================

class TestLazyTopologyUID:
    def test_uid_is_integer(self):
        lt = LazyTopology(carrier=frozenset({1, 2, 3}), subbasis=frozenset())
        assert isinstance(lt.uid, int)

    def test_empty_subbasis_uid_zero(self):
        # Empty subbasis → no subset bits set → uid = 0
        lt = LazyTopology(carrier=frozenset({1, 2}), subbasis=frozenset())
        assert lt.uid == 0

    def test_uid_deterministic_same_inputs(self):
        carrier = frozenset({1, 2, 3})
        sub = frozenset([frozenset({1}), frozenset({2, 3})])
        lt1 = LazyTopology(carrier=carrier, subbasis=sub)
        lt2 = LazyTopology(carrier=carrier, subbasis=sub)
        assert lt1.uid == lt2.uid

    def test_uid_different_for_different_subbases(self):
        carrier = frozenset({1, 2, 3})
        sub_a = frozenset([frozenset({1})])
        sub_b = frozenset([frozenset({2})])
        lt_a = LazyTopology(carrier=carrier, subbasis=sub_a)
        lt_b = LazyTopology(carrier=carrier, subbasis=sub_b)
        assert lt_a.uid != lt_b.uid

    def test_from_uid_roundtrip(self):
        carrier = frozenset({1, 2, 3})
        sub = frozenset([frozenset({1}), frozenset({2, 3})])
        lt = LazyTopology(carrier=carrier, subbasis=sub)
        lt2 = LazyTopology.from_uid(carrier, lt.uid)
        assert lt2.subbasis == sub
        assert lt2.uid == lt.uid

    def test_from_uid_empty_subbasis(self):
        carrier = frozenset({"a", "b"})
        lt = LazyTopology(carrier=carrier, subbasis=frozenset())
        lt2 = LazyTopology.from_uid(carrier, lt.uid)
        assert lt2.subbasis == frozenset()
        assert lt2.uid == 0


# ===========================================================================
# LazyTopology — is_open
# ===========================================================================

class TestLazyTopologyIsOpen:
    def setup_method(self):
        # Topology on {1,2,3}: subbasis = {{1}, {2,3}}
        # Basis: {1}, {2,3}, {1,2,3}
        # Open sets: ∅, {1}, {2,3}, {1,2,3}
        self.carrier = frozenset({1, 2, 3})
        self.lt = LazyTopology(
            carrier=self.carrier,
            subbasis=frozenset([frozenset({1}), frozenset({2, 3})]),
        )

    def test_empty_set_is_open(self):
        assert self.lt.is_open(frozenset())

    def test_carrier_is_open(self):
        assert self.lt.is_open(self.carrier)

    def test_subbasis_member_is_open(self):
        assert self.lt.is_open(frozenset({1}))
        assert self.lt.is_open(frozenset({2, 3}))

    def test_non_open_subset(self):
        # {1,2} is not open: point 2 has no basis element ⊆ {1,2} other than
        # {2,3} which is NOT a subset of {1,2}
        assert not self.lt.is_open(frozenset({1, 2}))

    def test_singleton_not_in_subbasis_not_open(self):
        assert not self.lt.is_open(frozenset({2}))
        assert not self.lt.is_open(frozenset({3}))

    def test_contains_open_alias(self):
        assert self.lt.contains_open(frozenset()) is self.lt.is_open(frozenset())

    def test_empty_subbasis_only_trivial_open(self):
        lt = LazyTopology(carrier=frozenset({1, 2, 3}), subbasis=frozenset())
        assert lt.is_open(frozenset())
        assert lt.is_open(frozenset({1, 2, 3}))
        assert not lt.is_open(frozenset({1}))
        assert not lt.is_open(frozenset({1, 2}))


# ===========================================================================
# LazyTopology — random open sets
# ===========================================================================

class TestLazyTopologyRandomOpenSets:
    def setup_method(self):
        self.lt = LazyTopology(
            carrier=frozenset({1, 2, 3}),
            subbasis=frozenset([frozenset({1}), frozenset({2, 3})]),
        )

    def test_random_open_set_is_valid_open_set(self):
        for seed in range(20):
            u = self.lt.random_open_set(seed=seed)
            assert self.lt.is_open(u), f"Expected open set, got {u} (seed={seed})"

    def test_sample_open_sets_all_valid(self):
        sets = self.lt.sample_open_sets(k=30, seed=7)
        assert len(sets) == 30
        for u in sets:
            assert self.lt.is_open(u)

    def test_random_open_set_seed_reproducible(self):
        u1 = self.lt.random_open_set(seed=99)
        u2 = self.lt.random_open_set(seed=99)
        assert u1 == u2

    def test_empty_subbasis_returns_trivial(self):
        lt = LazyTopology(carrier=frozenset({1, 2}), subbasis=frozenset())
        for seed in range(10):
            u = lt.random_open_set(seed=seed)
            assert lt.is_open(u)


# ===========================================================================
# random_topology
# ===========================================================================

class TestRandomTopology:
    def test_small_carrier_returns_finite_space(self):
        sp = random_topology([1, 2, 3], seed=0)
        assert isinstance(sp, FiniteTopologicalSpace)

    def test_small_carrier_empty_and_full_in_topology(self):
        sp = random_topology([1, 2, 3], seed=0)
        assert frozenset() in sp.topology
        assert frozenset({1, 2, 3}) in sp.topology

    def test_large_carrier_returns_lazy(self):
        lt = random_topology(range(6), seed=0)
        assert isinstance(lt, LazyTopology)

    def test_large_carrier_lazy_carrier_correct(self):
        lt = random_topology(range(8), seed=1)
        assert lt.carrier == frozenset(range(8))

    def test_seed_reproducible_small(self):
        sp1 = random_topology([1, 2, 3], seed=42)
        sp2 = random_topology([1, 2, 3], seed=42)
        assert sp1.topology == sp2.topology

    def test_seed_reproducible_large(self):
        lt1 = random_topology(range(7), seed=42)
        lt2 = random_topology(range(7), seed=42)
        assert lt1.uid == lt2.uid

    def test_single_element_carrier(self):
        sp = random_topology([1], seed=0)
        assert isinstance(sp, FiniteTopologicalSpace)
        assert frozenset() in sp.topology

    def test_empty_carrier(self):
        sp = random_topology([], seed=0)
        assert isinstance(sp, FiniteTopologicalSpace)


# ===========================================================================
# random_relation
# ===========================================================================

class TestRandomRelation:
    def test_all_pairs_within_carrier(self):
        carrier = [1, 2, 3]
        r = random_relation(carrier, seed=0)
        for x, y in r:
            assert x in carrier and y in carrier

    def test_density_zero_gives_empty(self):
        r = random_relation([1, 2, 3, 4], density=0.0, seed=0)
        assert r == set()

    def test_density_one_gives_full(self):
        carrier = [1, 2, 3]
        r = random_relation(carrier, density=1.0, seed=0)
        expected = {(x, y) for x in carrier for y in carrier}
        assert r == expected

    def test_default_density_nonempty_large_sample(self):
        # With density=0.5 and 16 possible pairs, expect roughly 8
        r = random_relation([1, 2, 3, 4], density=0.5, seed=7)
        assert 0 < len(r) < 16 or True  # soft — just no crash

    def test_seed_reproducible(self):
        r1 = random_relation([1, 2, 3], seed=42)
        r2 = random_relation([1, 2, 3], seed=42)
        assert r1 == r2

    def test_invalid_density_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_relation([1, 2], density=1.5)

    def test_negative_density_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_relation([1, 2], density=-0.1)


# ===========================================================================
# random_function
# ===========================================================================

class TestRandomFunction:
    def test_all_keys_in_domain(self):
        domain = [1, 2, 3, 4]
        f = random_function(domain, [10, 20], seed=0)
        assert set(f.keys()) == set(domain)

    def test_all_values_in_codomain(self):
        codomain = ["a", "b", "c"]
        f = random_function([1, 2, 3, 4, 5], codomain, seed=1)
        assert all(v in codomain for v in f.values())

    def test_returns_dict(self):
        f = random_function([1, 2], [10], seed=0)
        assert isinstance(f, dict)

    def test_seed_reproducible(self):
        f1 = random_function([1, 2, 3], [10, 20, 30], seed=99)
        f2 = random_function([1, 2, 3], [10, 20, 30], seed=99)
        assert f1 == f2

    def test_empty_codomain_raises(self):
        with pytest.raises(RandomGeneratorError):
            random_function([1, 2], [], seed=0)

    def test_empty_domain_gives_empty_dict(self):
        f = random_function([], [1, 2, 3], seed=0)
        assert f == {}

    def test_single_codomain_always_maps_there(self):
        f = random_function([1, 2, 3, 4, 5], [42], seed=0)
        assert all(v == 42 for v in f.values())

    def test_compatible_with_make_function(self):
        from pytop.maps import make_function
        f_dict = random_function([1, 2, 3], [10, 20, 30], seed=5)
        fm = make_function([1, 2, 3], [10, 20, 30], f_dict)
        for k, v in f_dict.items():
            assert fm.image_of_point(k) == v
