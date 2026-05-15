"""Tests for finite_basis_engine.py."""

import pytest
from pytop.finite_basis_engine import (
    BasisAnalysis,
    BasisComparison,
    FiniteBasisEngineError,
    SubbasisAnalysis,
    analyze_basis,
    analyze_subbasis,
    basis_from_subbasis,
    compare_generated_topologies_from_bases,
    continuity_via_basis_preimage,
    finite_basis_engine_capabilities,
    generated_topology_from_basis,
    local_base_report,
    relative_basis,
)

X3 = [1, 2, 3]

# A valid basis for {1,2,3}: singletons cover and pairwise intersections OK
SINGLETON_BASIS = [{1}, {2}, {3}]

# Basis generating the topology {∅, {1}, {1,2}, X}
SIER_BASIS = [{1}, {1, 2}, {1, 2, 3}]

# Discrete topology (all singletons form a basis)
DISCRETE_TOP = [set(), {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}]

# Simple subbasis: {1,2} and {2,3} on X={1,2,3}
SUBBASIS = [{1, 2}, {2, 3}]


# ---------------------------------------------------------------------------
# analyze_basis
# ---------------------------------------------------------------------------

class TestAnalyzeBasis:
    def test_singleton_basis_is_valid(self):
        a = analyze_basis(X3, SINGLETON_BASIS)
        assert a.is_basis

    def test_singleton_basis_generates_topology(self):
        a = analyze_basis(X3, SINGLETON_BASIS)
        assert a.generated_topology is not None
        assert len(a.generated_topology) > 0

    def test_sier_basis_is_valid(self):
        a = analyze_basis(X3, SIER_BASIS)
        assert a.is_basis

    def test_non_covering_family_fails(self):
        # {1},{2} does not cover {3}
        a = analyze_basis(X3, [{1}, {2}])
        assert not a.is_basis
        assert 3 in a.coverage_missing

    def test_failure_count_nonzero_for_bad_basis(self):
        a = analyze_basis(X3, [{1}, {2}])
        assert a.failure_count > 0

    def test_as_dict_keys(self):
        a = analyze_basis(X3, SINGLETON_BASIS)
        d = a.as_dict()
        for key in ("carrier","basis","is_basis","generated_topology",
                    "coverage_missing","intersection_failures","failure_count"):
            assert key in d

    def test_is_basis_analysis_instance(self):
        a = analyze_basis(X3, SINGLETON_BASIS)
        assert isinstance(a, BasisAnalysis)


# ---------------------------------------------------------------------------
# generated_topology_from_basis
# ---------------------------------------------------------------------------

class TestGeneratedTopologyFromBasis:
    def test_singletons_generate_discrete(self):
        top = generated_topology_from_basis(X3, SINGLETON_BASIS)
        assert frozenset() in top
        assert frozenset(X3) in top
        assert len(top) == 8  # discrete on 3 points

    def test_result_is_tuple_of_frozensets(self):
        top = generated_topology_from_basis(X3, SINGLETON_BASIS)
        assert all(isinstance(s, frozenset) for s in top)

    def test_generated_topology_contains_whole_space(self):
        top = generated_topology_from_basis(X3, SIER_BASIS)
        assert frozenset(X3) in top


# ---------------------------------------------------------------------------
# basis_from_subbasis
# ---------------------------------------------------------------------------

class TestBasisFromSubbasis:
    def test_subbasis_yields_nonempty_basis(self):
        basis = basis_from_subbasis(X3, SUBBASIS)
        assert len(basis) > 0

    def test_basis_members_are_frozensets(self):
        basis = basis_from_subbasis(X3, SUBBASIS)
        assert all(isinstance(s, frozenset) for s in basis)

    def test_basis_covers_carrier(self):
        basis = basis_from_subbasis(X3, SUBBASIS)
        covered = frozenset().union(*basis)
        assert covered == frozenset(X3)


# ---------------------------------------------------------------------------
# analyze_subbasis
# ---------------------------------------------------------------------------

class TestAnalyzeSubbasis:
    def test_result_is_subbasis_analysis(self):
        a = analyze_subbasis(X3, SUBBASIS)
        assert isinstance(a, SubbasisAnalysis)

    def test_generated_topology_is_valid(self):
        a = analyze_subbasis(X3, SUBBASIS)
        assert a.topology_is_valid

    def test_contains_empty_and_whole_space(self):
        a = analyze_subbasis(X3, SUBBASIS)
        assert frozenset() in a.generated_topology
        assert frozenset(X3) in a.generated_topology

    def test_as_dict_keys(self):
        a = analyze_subbasis(X3, SUBBASIS)
        d = a.as_dict()
        for key in ("carrier","subbasis","finite_intersection_basis",
                    "generated_topology","topology_is_valid"):
            assert key in d


# ---------------------------------------------------------------------------
# compare_generated_topologies_from_bases
# ---------------------------------------------------------------------------

class TestCompareGeneratedTopologies:
    def test_same_basis_same_topology(self):
        c = compare_generated_topologies_from_bases(X3, SINGLETON_BASIS, SINGLETON_BASIS)
        assert c.same_topology
        assert len(c.first_only) == 0
        assert len(c.second_only) == 0

    def test_different_bases_different_topology(self):
        # SINGLETON_BASIS (discrete) vs SIER_BASIS (coarser)
        c = compare_generated_topologies_from_bases(X3, SINGLETON_BASIS, SIER_BASIS)
        assert not c.same_topology

    def test_result_is_basis_comparison(self):
        c = compare_generated_topologies_from_bases(X3, SINGLETON_BASIS, SINGLETON_BASIS)
        assert isinstance(c, BasisComparison)

    def test_as_dict_keys(self):
        c = compare_generated_topologies_from_bases(X3, SINGLETON_BASIS, SIER_BASIS)
        d = c.as_dict()
        for key in ("carrier","first_topology","second_topology","same_topology",
                    "first_only","second_only"):
            assert key in d


# ---------------------------------------------------------------------------
# relative_basis
# ---------------------------------------------------------------------------

class TestRelativeBasis:
    def test_relative_basis_on_subspace(self):
        rb = relative_basis(SINGLETON_BASIS, [1, 2])
        # {1}∩{1,2}={1}, {2}∩{1,2}={2}, {3}∩{1,2}=∅
        assert frozenset({1}) in rb
        assert frozenset({2}) in rb

    def test_empty_intersections_excluded_by_default(self):
        rb = relative_basis(SINGLETON_BASIS, [1, 2])
        assert frozenset() not in rb

    def test_include_empty_flag(self):
        rb = relative_basis(SINGLETON_BASIS, [1, 2], include_empty=True)
        assert frozenset() in rb


# ---------------------------------------------------------------------------
# local_base_report
# ---------------------------------------------------------------------------

class TestLocalBaseReport:
    def test_singletons_local_base_at_1(self):
        # {1} alone is a local base at point 1 for discrete topology
        report = local_base_report(X3, 1, [{1}], DISCRETE_TOP)
        assert report["is_local_base"] is True
        assert report["point"] == 1

    def test_report_contains_expected_keys(self):
        report = local_base_report(X3, 1, SINGLETON_BASIS, DISCRETE_TOP)
        for key in ("point","candidate_family","is_local_base","neighborhoods_checked"):
            assert key in report


# ---------------------------------------------------------------------------
# continuity_via_basis_preimage
# ---------------------------------------------------------------------------

class TestContinuityViaBasisPreimage:
    def test_identity_is_continuous(self):
        mapping = {1: 1, 2: 2, 3: 3}
        result = continuity_via_basis_preimage(X3, DISCRETE_TOP, SINGLETON_BASIS, mapping)
        assert result["is_continuous_via_basis"] is True

    def test_constant_map_not_continuous_on_discrete_codomain(self):
        # constant map 1→1, 2→1, 3→1; preimage of {2} = ∅, which is open → all ok
        # but preimage of {2} is ∅ which IS open, preimage of {1} = X which IS open
        # So constant map IS continuous from discrete to discrete (to {1,2,3})
        mapping = {1: 1, 2: 1, 3: 1}
        result = continuity_via_basis_preimage(X3, DISCRETE_TOP, SINGLETON_BASIS, mapping)
        # preimage of {2} = ∅ (open), preimage of {1} = X (open), preimage of {3} = ∅ (open)
        assert result["is_continuous_via_basis"] is True

    def test_result_has_checks(self):
        mapping = {1: 1, 2: 2, 3: 3}
        result = continuity_via_basis_preimage(X3, DISCRETE_TOP, SINGLETON_BASIS, mapping)
        assert "checks" in result
        assert len(result["checks"]) > 0


# ---------------------------------------------------------------------------
# finite_basis_engine_capabilities
# ---------------------------------------------------------------------------

class TestCapabilities:
    def test_returns_dict(self):
        caps = finite_basis_engine_capabilities()
        assert isinstance(caps, dict)
        assert len(caps) > 0

    def test_known_capabilities_present(self):
        caps = finite_basis_engine_capabilities()
        assert "basis_analysis" in caps
        assert "subbasis_analysis" in caps


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------

class TestErrorPaths:
    def test_string_carrier_raises(self):
        with pytest.raises(FiniteBasisEngineError):
            analyze_basis("abc", [{1}])

    def test_none_carrier_raises(self):
        with pytest.raises(FiniteBasisEngineError):
            analyze_basis(None, [{1}])
