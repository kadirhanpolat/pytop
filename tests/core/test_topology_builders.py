"""Tests for src/pytop/topology_builders.py."""


from pytop.topology_builders import (
    cofinite_topology,
    discrete_topology,
    indiscrete_topology,
    make_topology,
    sierpinski_space,
    topology_from_basis,
    topology_from_subbasis,
)

# ---------------------------------------------------------------------------
# make_topology
# ---------------------------------------------------------------------------

class TestMakeTopology:
    def test_empty_open_sets_gives_indiscrete(self):
        sp = make_topology({1, 2, 3})
        assert frozenset() in sp.topology
        assert frozenset({1, 2, 3}) in sp.topology
        assert len(sp.topology) == 2

    def test_adds_empty_and_x(self):
        sp = make_topology({1, 2, 3}, {1})
        assert frozenset() in sp.topology
        assert frozenset({1, 2, 3}) in sp.topology
        assert frozenset({1}) in sp.topology

    def test_carrier_and_topology_match(self):
        sp = make_topology({0, 1}, {0})
        assert sp.carrier == frozenset({0, 1})

    def test_duplicate_open_sets_deduplicated(self):
        sp = make_topology({1, 2}, {1}, {1})
        sizes = len(sp.topology)
        assert sizes == 3  # ∅, {1}, {1,2}

    def test_set_and_frozenset_open_sets(self):
        sp = make_topology([1, 2, 3], frozenset({1}), {2, 3})
        assert frozenset({1}) in sp.topology
        assert frozenset({2, 3}) in sp.topology

    def test_empty_carrier(self):
        sp = make_topology([])
        assert sp.carrier == frozenset()
        # τ = {∅, ∅} → deduplicates to 1 element
        assert frozenset() in sp.topology


# ---------------------------------------------------------------------------
# discrete_topology
# ---------------------------------------------------------------------------

class TestDiscreteTopology:
    def test_zero_elements(self):
        sp = discrete_topology()
        assert sp.carrier == frozenset()

    def test_one_element(self):
        sp = discrete_topology("a")
        # P({a}) = {∅, {a}}
        assert len(sp.topology) == 2
        assert frozenset({"a"}) in sp.topology

    def test_two_elements(self):
        sp = discrete_topology(1, 2)
        # P({1,2}) = {∅,{1},{2},{1,2}}
        assert len(sp.topology) == 4

    def test_three_elements(self):
        sp = discrete_topology(1, 2, 3)
        assert len(sp.topology) == 8  # 2^3

    def test_carrier_correct(self):
        sp = discrete_topology("x", "y")
        assert sp.carrier == frozenset({"x", "y"})

    def test_every_subset_open(self):
        sp = discrete_topology(1, 2, 3)
        assert frozenset({1}) in sp.topology
        assert frozenset({2, 3}) in sp.topology

    def test_tags_include_discrete(self):
        sp = discrete_topology(1, 2)
        assert sp.has_tag("discrete")


# ---------------------------------------------------------------------------
# indiscrete_topology
# ---------------------------------------------------------------------------

class TestIndiscreteTopology:
    def test_two_open_sets(self):
        sp = indiscrete_topology(1, 2, 3)
        assert len(sp.topology) == 2

    def test_only_empty_and_x(self):
        sp = indiscrete_topology("a", "b")
        assert frozenset() in sp.topology
        assert frozenset({"a", "b"}) in sp.topology

    def test_singleton_subset_not_open(self):
        sp = indiscrete_topology(1, 2, 3)
        assert frozenset({1}) not in sp.topology

    def test_carrier(self):
        sp = indiscrete_topology(10, 20)
        assert sp.carrier == frozenset({10, 20})

    def test_tags_include_indiscrete(self):
        sp = indiscrete_topology(1, 2)
        assert sp.has_tag("indiscrete")

    def test_zero_elements(self):
        sp = indiscrete_topology()
        assert sp.carrier == frozenset()


# ---------------------------------------------------------------------------
# cofinite_topology
# ---------------------------------------------------------------------------

class TestCofiniteTopology:
    def test_all_subsets_open_for_finite_x(self):
        sp = cofinite_topology(1, 2, 3)
        assert len(sp.topology) == 8  # same as discrete for finite X

    def test_tags_include_cofinite(self):
        sp = cofinite_topology(1, 2, 3)
        assert sp.has_tag("cofinite")

    def test_carrier(self):
        sp = cofinite_topology("a", "b")
        assert sp.carrier == frozenset({"a", "b"})


# ---------------------------------------------------------------------------
# sierpinski_space
# ---------------------------------------------------------------------------

class TestSierpinskiSpace:
    def test_carrier(self):
        sp = sierpinski_space()
        assert sp.carrier == frozenset({0, 1})

    def test_topology(self):
        sp = sierpinski_space()
        assert frozenset() in sp.topology
        assert frozenset({1}) in sp.topology
        assert frozenset({0, 1}) in sp.topology
        assert len(sp.topology) == 3

    def test_point_0_not_open(self):
        sp = sierpinski_space()
        assert frozenset({0}) not in sp.topology

    def test_tags(self):
        sp = sierpinski_space()
        assert sp.has_tag("t0")


# ---------------------------------------------------------------------------
# topology_from_basis
# ---------------------------------------------------------------------------

class TestTopologyFromBasis:
    def test_basis_generates_correct_topology(self):
        # Basis: {{1}, {2}, {3}} generates discrete on {1,2,3}
        sp = topology_from_basis([1, 2, 3], [{1}, {2}, {3}])
        assert frozenset({1}) in sp.topology
        assert frozenset({2, 3}) in sp.topology

    def test_basis_three_singletons(self):
        # Basis: {{1}, {2}, {3}} generates discrete on {1,2,3}
        sp = topology_from_basis([1, 2, 3], [{1}, {2}, {3}])
        assert frozenset({1}) in sp.topology
        assert frozenset({2, 3}) in sp.topology
        assert frozenset({1, 2, 3}) in sp.topology


# ---------------------------------------------------------------------------
# topology_from_subbasis
# ---------------------------------------------------------------------------

class TestTopologyFromSubbasis:
    def test_subbasis_single_set(self):
        sp = topology_from_subbasis([1, 2, 3], [{1}])
        # Generated topology: at minimum ∅, {1}, {1,2,3}
        assert frozenset({1}) in sp.topology
        assert frozenset() in sp.topology
        assert frozenset({1, 2, 3}) in sp.topology

    def test_subbasis_two_sets(self):
        sp = topology_from_subbasis([1, 2, 3], [{1, 2}, {2, 3}])
        # Intersection: {2} is also in topology
        assert frozenset({2}) in sp.topology
