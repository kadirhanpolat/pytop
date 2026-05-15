"""Tests for finite_map_engine.py."""

import pytest
from pytop.finite_map_engine import (
    FiniteMapAnalysis,
    FiniteMapData,
    FiniteMapEngineError,
    analyze_finite_map,
    continuity_checks_by_opens,
    continuity_via_codomain_basis_finite,
    finite_map_engine_capabilities,
    finite_map_table,
    image_of_subset_finite,
    is_bijective_finite_map,
    is_continuous_finite_map,
    is_injective_finite_map,
    is_surjective_finite_map,
    normalize_finite_map_data,
    preimage_of_subset_finite,
)

X3 = [1, 2, 3]
DISCRETE = [set(), {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}]
INDISCRETE = [set(), {1,2,3}]
SIER = [set(), {1}, {1,2}, {1,2,3}]

# Identity map
ID_MAP = {1: 1, 2: 2, 3: 3}
# Constant map: everything → 1
CONST_MAP = {1: 1, 2: 1, 3: 1}
# Injective non-surjective: 1→1, 2→2, 3→2 (NOT injective)
NON_INJ = {1: 1, 2: 2, 3: 2}
# Bijection: 1→2, 2→3, 3→1
PERM_MAP = {1: 2, 2: 3, 3: 1}


# ---------------------------------------------------------------------------
# normalize_finite_map_data
# ---------------------------------------------------------------------------

class TestNormalizeFiniteMapData:
    def test_identity_is_well_defined(self):
        md = normalize_finite_map_data(X3, X3, ID_MAP)
        assert isinstance(md, FiniteMapData)
        assert md.domain == frozenset(X3)
        assert md.codomain == frozenset(X3)

    def test_missing_domain_point_raises(self):
        with pytest.raises(FiniteMapEngineError):
            normalize_finite_map_data(X3, X3, {1: 1, 2: 2})  # 3 missing

    def test_extra_key_raises(self):
        with pytest.raises(FiniteMapEngineError):
            normalize_finite_map_data([1, 2], X3, {1: 1, 2: 2, 3: 3})

    def test_value_outside_codomain_raises(self):
        with pytest.raises(FiniteMapEngineError):
            normalize_finite_map_data(X3, [1, 2], {1: 1, 2: 2, 3: 99})

    def test_graph_property(self):
        md = normalize_finite_map_data(X3, X3, ID_MAP)
        assert set(md.graph) == {(1,1),(2,2),(3,3)}

    def test_image_of_point(self):
        md = normalize_finite_map_data(X3, X3, ID_MAP)
        assert md.image_of_point(1) == 1

    def test_image_of_point_not_in_domain_raises(self):
        md = normalize_finite_map_data(X3, X3, ID_MAP)
        with pytest.raises(FiniteMapEngineError):
            md.image_of_point(99)


# ---------------------------------------------------------------------------
# image_of_subset_finite / preimage_of_subset_finite
# ---------------------------------------------------------------------------

class TestImagePreimage:
    def setup_method(self):
        self.md = normalize_finite_map_data(X3, X3, PERM_MAP)

    def test_image_of_full_domain(self):
        img = image_of_subset_finite(self.md, X3)
        assert img == frozenset(X3)

    def test_image_of_singleton(self):
        img = image_of_subset_finite(self.md, [1])
        assert img == frozenset({2})

    def test_preimage_of_singleton(self):
        pre = preimage_of_subset_finite(self.md, [2])
        assert pre == frozenset({1})

    def test_preimage_of_empty(self):
        pre = preimage_of_subset_finite(self.md, [])
        assert pre == frozenset()

    def test_image_subset_not_in_domain_raises(self):
        with pytest.raises(FiniteMapEngineError):
            image_of_subset_finite(self.md, [99])

    def test_preimage_subset_not_in_codomain_raises(self):
        with pytest.raises(FiniteMapEngineError):
            preimage_of_subset_finite(self.md, [99])


# ---------------------------------------------------------------------------
# finite_map_table
# ---------------------------------------------------------------------------

class TestFiniteMapTable:
    def test_table_has_expected_keys(self):
        t = finite_map_table(X3, X3, ID_MAP)
        for key in ("domain","codomain","graph","image"):
            assert key in t

    def test_image_equals_full_domain_for_bijection(self):
        t = finite_map_table(X3, X3, PERM_MAP)
        assert t["image"] == frozenset(X3)


# ---------------------------------------------------------------------------
# is_injective / surjective / bijective
# ---------------------------------------------------------------------------

class TestInjectiveSurjectiveBijective:
    def setup_method(self):
        self.id_md = normalize_finite_map_data(X3, X3, ID_MAP)
        self.const_md = normalize_finite_map_data(X3, X3, CONST_MAP)
        self.non_inj_md = normalize_finite_map_data(X3, X3, NON_INJ)
        self.perm_md = normalize_finite_map_data(X3, X3, PERM_MAP)

    def test_identity_is_injective(self):
        assert is_injective_finite_map(self.id_md)

    def test_constant_map_not_injective(self):
        assert not is_injective_finite_map(self.const_md)

    def test_non_injective_map(self):
        assert not is_injective_finite_map(self.non_inj_md)

    def test_constant_map_not_surjective(self):
        assert not is_surjective_finite_map(self.const_md)

    def test_identity_is_surjective(self):
        assert is_surjective_finite_map(self.id_md)

    def test_permutation_is_bijective(self):
        assert is_bijective_finite_map(self.perm_md)

    def test_constant_map_not_bijective(self):
        assert not is_bijective_finite_map(self.const_md)


# ---------------------------------------------------------------------------
# continuity_checks_by_opens
# ---------------------------------------------------------------------------

class TestContinuityChecksByOpens:
    def test_identity_discrete_to_discrete_is_continuous(self):
        checks = continuity_checks_by_opens(X3, DISCRETE, X3, DISCRETE, ID_MAP)
        assert all(item[2] for item in checks)

    def test_identity_indiscrete_to_indiscrete_is_continuous(self):
        checks = continuity_checks_by_opens(X3, INDISCRETE, X3, INDISCRETE, ID_MAP)
        assert all(item[2] for item in checks)

    def test_checks_are_triples(self):
        checks = continuity_checks_by_opens(X3, DISCRETE, X3, DISCRETE, ID_MAP)
        assert all(len(item) == 3 for item in checks)

    def test_invalid_domain_topology_raises(self):
        not_top = [set(), {1}, {2}, {1,2,3}]  # missing {1,2}
        with pytest.raises(FiniteMapEngineError):
            continuity_checks_by_opens(X3, not_top, X3, DISCRETE, ID_MAP)


# ---------------------------------------------------------------------------
# is_continuous_finite_map
# ---------------------------------------------------------------------------

class TestIsContinuousFiniteMap:
    def test_identity_discrete_continuous(self):
        assert is_continuous_finite_map(X3, DISCRETE, X3, DISCRETE, ID_MAP)

    def test_identity_indiscrete_continuous(self):
        assert is_continuous_finite_map(X3, INDISCRETE, X3, INDISCRETE, ID_MAP)

    def test_const_map_to_indiscrete_is_continuous(self):
        # Constant map X3→{1}: any map to indiscrete is continuous
        assert is_continuous_finite_map(X3, DISCRETE, X3, INDISCRETE, CONST_MAP)

    def test_id_from_indiscrete_to_discrete_not_continuous(self):
        # id: (X3, indiscrete) → (X3, discrete) not continuous (preimage of {1} not open)
        assert not is_continuous_finite_map(X3, INDISCRETE, X3, DISCRETE, ID_MAP)


# ---------------------------------------------------------------------------
# continuity_via_codomain_basis_finite
# ---------------------------------------------------------------------------

class TestContinuityViaCodomainBasis:
    def test_identity_is_continuous_via_basis(self):
        basis = [{1}, {2}, {3}]
        result = continuity_via_codomain_basis_finite(X3, DISCRETE, basis, ID_MAP)
        assert result["is_continuous_via_basis"] is True

    def test_result_has_checks(self):
        basis = [{1}, {2}, {3}]
        result = continuity_via_codomain_basis_finite(X3, DISCRETE, basis, ID_MAP)
        assert "checks" in result


# ---------------------------------------------------------------------------
# analyze_finite_map
# ---------------------------------------------------------------------------

class TestAnalyzeFiniteMap:
    def test_identity_analysis(self):
        a = analyze_finite_map(X3, DISCRETE, X3, DISCRETE, ID_MAP)
        assert isinstance(a, FiniteMapAnalysis)
        assert a.is_continuous
        assert a.is_bijective
        assert a.is_homeomorphism_candidate

    def test_const_map_analysis(self):
        a = analyze_finite_map(X3, DISCRETE, X3, DISCRETE, CONST_MAP)
        assert not a.is_injective
        assert not a.is_surjective

    def test_as_dict_keys(self):
        a = analyze_finite_map(X3, DISCRETE, X3, DISCRETE, ID_MAP)
        d = a.as_dict()
        for key in ("domain","codomain","graph","image","is_total","is_well_defined",
                    "is_injective","is_surjective","is_bijective","is_continuous",
                    "continuity_checks","is_homeomorphism_candidate"):
            assert key in d

    def test_homeomorphism_candidate_bijective_continuous(self):
        a = analyze_finite_map(X3, DISCRETE, X3, DISCRETE, PERM_MAP)
        assert a.is_bijective
        assert a.is_continuous
        assert a.is_homeomorphism_candidate


# ---------------------------------------------------------------------------
# finite_map_engine_capabilities
# ---------------------------------------------------------------------------

class TestCapabilities:
    def test_returns_dict(self):
        caps = finite_map_engine_capabilities()
        assert isinstance(caps, dict)

    def test_known_capabilities_present(self):
        caps = finite_map_engine_capabilities()
        assert "analyze_finite_map" in caps
        assert "continuity_checks_by_opens" in caps
