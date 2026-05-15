"""Tests for examples.py — finite and infinite space factories."""

import pytest
from pytop.examples import (
    empty_space,
    examples_catalog,
    finite_chain_space,
    finite_examples_catalog,
    partition_space,
    sierpinski_space,
    singleton_space,
    two_point_discrete_space,
    two_point_indiscrete_space,
)
from pytop.finite_spaces import FiniteTopologicalSpace


class TestEmptySpace:
    def test_returns_finite_topological_space(self):
        assert isinstance(empty_space(), FiniteTopologicalSpace)

    def test_carrier_is_empty(self):
        assert len(empty_space().carrier) == 0

    def test_topology_contains_empty_set(self):
        topo = [frozenset(s) for s in empty_space().topology]
        assert frozenset() in topo


class TestSingletonSpace:
    def test_default_label_x(self):
        assert "x" in singleton_space().carrier

    def test_custom_label(self):
        assert "p" in singleton_space("p").carrier

    def test_carrier_has_one_point(self):
        assert len(singleton_space("a").carrier) == 1

    def test_topology_has_two_opens(self):
        topo = [frozenset(s) for s in singleton_space().topology]
        assert len(topo) == 2


class TestTwoPointDiscreteSpace:
    def test_carrier_has_two_points(self):
        assert len(two_point_discrete_space().carrier) == 2

    def test_topology_has_four_opens(self):
        topo = list({frozenset(s) for s in two_point_discrete_space().topology})
        assert len(topo) == 4


class TestTwoPointIndiscreteSpace:
    def test_carrier_has_two_points(self):
        assert len(two_point_indiscrete_space().carrier) == 2

    def test_topology_has_two_opens(self):
        topo = list({frozenset(s) for s in two_point_indiscrete_space().topology})
        assert len(topo) == 2


class TestSierpinskiSpace:
    def test_carrier_is_0_1(self):
        assert set(sierpinski_space().carrier) == {0, 1}

    def test_topology_has_three_opens(self):
        topo = list({frozenset(s) for s in sierpinski_space().topology})
        assert len(topo) == 3

    def test_singleton_1_is_open(self):
        topo = [frozenset(s) for s in sierpinski_space().topology]
        assert frozenset({1}) in topo

    def test_singleton_0_not_open(self):
        topo = [frozenset(s) for s in sierpinski_space().topology]
        assert frozenset({0}) not in topo


class TestFiniteChainSpace:
    def test_n3_carrier_size(self):
        assert len(finite_chain_space(3).carrier) == 3

    def test_n1_minimal(self):
        assert len(finite_chain_space(1).carrier) == 1

    def test_n5_carrier(self):
        assert set(finite_chain_space(5).carrier) == {1, 2, 3, 4, 5}

    def test_topology_contains_empty(self):
        topo = [frozenset(s) for s in finite_chain_space(3).topology]
        assert frozenset() in topo

    def test_topology_contains_full_set(self):
        sp = finite_chain_space(3)
        topo = [frozenset(s) for s in sp.topology]
        assert frozenset(sp.carrier) in topo

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            finite_chain_space(0)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            finite_chain_space(-1)


class TestPartitionSpace:
    def test_two_blocks_carrier(self):
        assert set(partition_space([[1, 2], [3]]).carrier) == {1, 2, 3}

    def test_singleton_blocks(self):
        assert len(partition_space([[1], [2], [3]]).carrier) == 3

    def test_topology_contains_empty(self):
        topo = [frozenset(s) for s in partition_space([[1, 2], [3]]).topology]
        assert frozenset() in topo

    def test_topology_contains_each_block(self):
        topo = [frozenset(s) for s in partition_space([[1, 2], [3]]).topology]
        assert frozenset({1, 2}) in topo
        assert frozenset({3}) in topo

    def test_returns_finite_topological_space(self):
        assert isinstance(partition_space([[1], [2]]), FiniteTopologicalSpace)

    def test_no_duplicate_opens(self):
        sp = partition_space([[1, 2], [3]])
        topo = [frozenset(s) for s in sp.topology]
        assert len(topo) == len(set(topo))

    def test_single_block(self):
        sp = partition_space([[1, 2, 3]])
        topo = [frozenset(s) for s in sp.topology]
        assert frozenset({1, 2, 3}) in topo


class TestFiniteExamplesCatalog:
    def test_returns_dict(self):
        assert isinstance(finite_examples_catalog(), dict)

    def test_expected_keys_present(self):
        cat = finite_examples_catalog()
        for key in ("empty_space", "singleton_space", "two_point_discrete_space",
                    "sierpinski_space", "finite_chain_space", "partition_space"):
            assert key in cat

    def test_each_entry_has_constructor(self):
        for entry in finite_examples_catalog().values():
            assert callable(entry["constructor"])

    def test_each_entry_has_description(self):
        for entry in finite_examples_catalog().values():
            assert "description" in entry


class TestExamplesCatalog:
    def test_has_finite_and_infinite_keys(self):
        cat = examples_catalog()
        assert "finite" in cat and "infinite" in cat

    def test_finite_section_nonempty(self):
        assert len(examples_catalog()["finite"]) > 0

    def test_infinite_section_nonempty(self):
        assert len(examples_catalog()["infinite"]) > 0
