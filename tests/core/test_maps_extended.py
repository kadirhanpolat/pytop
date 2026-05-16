"""Extended tests for maps.py — branches not covered by test_maps.py."""

import pytest
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_maps import ContinuousMap
from pytop.infinite_spaces import InfiniteTopologicalSpace
from pytop.maps import (
    FiniteMap,
    analyze_map_property,
    continuity_via_codomain_basis,
    continuity_via_codomain_subbasis,
    identity_map,
    image_of_subset,
    initial_topology_from_maps,
    is_bijective_map,
    is_closed_map,
    is_continuous_at_point,
    is_continuous_map,
    is_embedding_map,
    is_homeomorphism_map,
    is_injective_map,
    is_open_map,
    is_quotient_map,
    is_sequentially_continuous_at_point,
    is_surjective_map,
    map_report,
    map_taxonomy_profile,
    normalize_map_property,
    preimage_of_subset,
    render_map_taxonomy_report,
    satisfies_closure_image_inclusion,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _discrete(*pts):
    pts = list(pts)
    n = len(pts)
    opens = [frozenset(pts[i] for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]
    return FiniteTopologicalSpace(carrier=tuple(pts), topology=opens)


def _indiscrete(*pts):
    return FiniteTopologicalSpace(carrier=tuple(pts), topology=[set(), set(pts)])


def _sierpinski():
    return FiniteTopologicalSpace(carrier=(1, 2), topology=[set(), {1}, {1, 2}])


def _symbolic_map():
    dom = InfiniteTopologicalSpace(carrier="X", metadata={"representation": "infinite_T2"})
    cod = InfiniteTopologicalSpace(carrier="Y", metadata={"representation": "infinite_T2"})
    return ContinuousMap(domain=dom, codomain=cod, name="f")


# ---------------------------------------------------------------------------
# FiniteMap callable mapping branch (lines 63-65, 69)
# ---------------------------------------------------------------------------

class TestCallableMapping:
    def test_image_of_point_dict(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 2, 2: 1}, name="swap")
        assert f.image_of_point(1) == 2

    def test_image_of_point_callable(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping=lambda x: x, name="id_lam")
        assert f.image_of_point(1) == 1
        assert f.image_of_point(2) == 2

    def test_graph_dict_callable(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping=lambda x: x, name="id_lam")
        assert f.graph_dict() == {1: 1, 2: 2}

    def test_analyze_with_callable_mapping(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping=lambda x: x, name="id_lam")
        assert analyze_map_property(f, "continuous").is_true


# ---------------------------------------------------------------------------
# normalize_map_property (line 84)
# ---------------------------------------------------------------------------

class TestNormalizeMapProperty:
    def test_unknown_property_raises(self):
        with pytest.raises(ValueError, match="Unsupported"):
            normalize_map_property("teleport")

    def test_alias_one_to_one(self):
        assert normalize_map_property("one_to_one") == "injective"

    def test_alias_onto(self):
        assert normalize_map_property("onto") == "surjective"

    def test_alias_open_map(self):
        assert normalize_map_property("open_map") == "open"

    def test_alias_closed_map(self):
        assert normalize_map_property("closed_map") == "closed"

    def test_alias_quotient_map(self):
        assert normalize_map_property("quotient_map") == "quotient"


# ---------------------------------------------------------------------------
# Individual is_*_map shortcuts (lines 98-134)
# ---------------------------------------------------------------------------

class TestIsContinuousMap:
    def test_is_continuous_map_identity(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        assert is_continuous_map(f).is_true

    def test_is_continuous_map_indiscrete_to_discrete(self):
        ind = _indiscrete(1, 2)
        disc = _discrete(1, 2)
        f = FiniteMap(domain=ind, codomain=disc, mapping={1: 1, 2: 2}, name="i_to_d")
        assert is_continuous_map(f).is_false


class TestMapShortcuts:
    def setup_method(self):
        self.X = _discrete(1, 2)
        self.f_id = FiniteMap(domain=self.X, codomain=self.X,
                               mapping={1: 1, 2: 2}, name="id")
        self.f_const = FiniteMap(domain=self.X, codomain=self.X,
                                  mapping={1: 1, 2: 1}, name="const")

    def test_is_open_map_true(self):
        assert is_open_map(self.f_id).is_true

    def test_is_open_map_false(self):
        ind = _indiscrete(1, 2)
        disc = _discrete(1, 2)
        f = FiniteMap(domain=disc, codomain=ind, mapping={1: 1, 2: 2}, name="d_to_i")
        assert is_open_map(f).is_false

    def test_is_closed_map_true(self):
        assert is_closed_map(self.f_id).is_true

    def test_is_injective_map_true(self):
        assert is_injective_map(self.f_id).is_true

    def test_is_injective_map_false(self):
        assert is_injective_map(self.f_const).is_false

    def test_is_surjective_map_true(self):
        assert is_surjective_map(self.f_id).is_true

    def test_is_surjective_map_false(self):
        assert is_surjective_map(self.f_const).is_false

    def test_is_bijective_map_true(self):
        assert is_bijective_map(self.f_id).is_true

    def test_is_bijective_map_false(self):
        assert is_bijective_map(self.f_const).is_false

    def test_is_embedding_map_identity(self):
        assert is_embedding_map(self.f_id).is_true

    def test_is_quotient_map_identity(self):
        assert is_quotient_map(self.f_id).is_true

    def test_is_homeomorphism_map_identity(self):
        assert is_homeomorphism_map(self.f_id).is_true

    def test_map_report_returns_all_properties(self):
        r = map_report(self.f_id)
        expected = {"continuous", "open", "closed", "bijective",
                    "injective", "surjective", "embedding", "quotient", "homeomorphism"}
        assert expected == set(r.keys())


# ---------------------------------------------------------------------------
# identity_map (lines 138-141)
# ---------------------------------------------------------------------------

class TestIdentityMap:
    def test_finite_space_returns_finite_map(self):
        X = _discrete(1, 2, 3)
        id_ = identity_map(X)
        assert isinstance(id_, FiniteMap)

    def test_finite_identity_has_homeomorphism_tag(self):
        X = _discrete(1, 2)
        id_ = identity_map(X)
        assert "homeomorphism" in id_.tags

    def test_finite_identity_custom_name(self):
        X = _discrete(1, 2)
        assert identity_map(X, name="iota").name == "iota"

    def test_non_finite_space_returns_symbolic(self):
        space = InfiniteTopologicalSpace(carrier="X", metadata={"representation": "infinite_T2"})
        id_ = identity_map(space)
        assert not isinstance(id_, FiniteMap)


# ---------------------------------------------------------------------------
# preimage_of_subset / image_of_subset ValueError (lines 149, 157)
# ---------------------------------------------------------------------------

class TestSubsetOpsRaiseForSymbolic:
    def test_preimage_raises(self):
        with pytest.raises(ValueError, match="finite"):
            preimage_of_subset(_symbolic_map(), {1})

    def test_image_raises(self):
        with pytest.raises(ValueError, match="finite"):
            image_of_subset(_symbolic_map(), {1})


# ---------------------------------------------------------------------------
# is_continuous_at_point edge cases (lines 169, 181, 195)
# ---------------------------------------------------------------------------

class TestContinuousAtPointEdgeCases:
    def test_point_not_in_domain_returns_false(self):
        X = _sierpinski()
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        r = is_continuous_at_point(f, 99)
        assert r.is_false

    def test_discontinuous_at_point_returns_false(self):
        ind = _indiscrete(1, 2)
        disc = _discrete(1, 2)
        f = FiniteMap(domain=ind, codomain=disc, mapping={1: 1, 2: 2}, name="i_to_d")
        r = is_continuous_at_point(f, 1)
        assert r.is_false

    def test_symbolic_map_returns_unknown(self):
        r = is_continuous_at_point(_symbolic_map(), "x")
        assert not r.is_true
        assert not r.is_false


# ---------------------------------------------------------------------------
# is_sequentially_continuous_at_point (lines 216-225)
# ---------------------------------------------------------------------------

class TestSequentiallyContinuousEdgeCases:
    def test_discontinuous_implies_not_sequential(self):
        ind = _indiscrete(1, 2)
        disc = _discrete(1, 2)
        f = FiniteMap(domain=ind, codomain=disc, mapping={1: 1, 2: 2}, name="i_to_d")
        r = is_sequentially_continuous_at_point(f, 1)
        assert r.is_false

    def test_symbolic_returns_unknown(self):
        r = is_sequentially_continuous_at_point(_symbolic_map(), "x")
        assert not r.is_true
        assert not r.is_false


# ---------------------------------------------------------------------------
# continuity_via_codomain_basis (lines 236, 243)
# ---------------------------------------------------------------------------

class TestContinuityViaBasisEdgeCases:
    def test_symbolic_returns_unknown(self):
        r = continuity_via_codomain_basis(_symbolic_map(), [{1}])
        assert not r.is_true
        assert not r.is_false

    def test_not_a_basis_returns_false(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        r = continuity_via_codomain_basis(f, [{1, 2}])
        assert r.is_false


# ---------------------------------------------------------------------------
# continuity_via_codomain_subbasis (lines 258, 267)
# ---------------------------------------------------------------------------

class TestContinuityViaSubbasisEdgeCases:
    def test_symbolic_returns_unknown(self):
        r = continuity_via_codomain_subbasis(_symbolic_map(), [{1}])
        assert not r.is_true
        assert not r.is_false

    def test_subbasis_not_generating_codomain_returns_false(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        r = continuity_via_codomain_subbasis(f, [{1, 2}])
        assert r.is_false


# ---------------------------------------------------------------------------
# satisfies_closure_image_inclusion symbolic (line 282)
# ---------------------------------------------------------------------------

class TestClosureImageInclusionSymbolic:
    def test_symbolic_returns_unknown(self):
        r = satisfies_closure_image_inclusion(_symbolic_map(), {1})
        assert not r.is_true
        assert not r.is_false


# ---------------------------------------------------------------------------
# initial_topology_from_maps error paths (lines 309, 314, 317)
# ---------------------------------------------------------------------------

class TestInitialTopologyErrors:
    def test_empty_maps_list_raises(self):
        with pytest.raises(ValueError, match="at least one"):
            initial_topology_from_maps({1, 2}, [])

    def test_non_finite_map_raises(self):
        with pytest.raises(ValueError, match="explicit finite"):
            initial_topology_from_maps({1, 2}, [_symbolic_map()])

    def test_wrong_carrier_raises(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        with pytest.raises(ValueError, match="same finite domain carrier"):
            initial_topology_from_maps({3, 4}, [f])


# ---------------------------------------------------------------------------
# map_taxonomy_profile (line 341)
# ---------------------------------------------------------------------------

class TestMapTaxonomyProfile:
    def test_identity_all_true(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        p = map_taxonomy_profile(f)
        assert p["continuous"] is True
        assert p["open"] is True
        assert p["bijective"] is True
        assert p["homeomorphism"] is True

    def test_constant_bijective_false(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 1}, name="const")
        p = map_taxonomy_profile(f)
        assert p["bijective"] is False


# ---------------------------------------------------------------------------
# render_map_taxonomy_report (lines 357, 373-374, 377)
# ---------------------------------------------------------------------------

class TestRenderMapTaxonomyReport:
    def test_map_name_in_report(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="mymap")
        assert "mymap" in render_map_taxonomy_report(f)

    def test_yes_for_continuous_homeomorphism(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        report = render_map_taxonomy_report(f)
        assert "continuous: yes" in report
        assert "homeomorphism: yes" in report

    def test_continuous_bijection_warning(self):
        # disc → ind: bijective+continuous but not homeomorphism (not open)
        disc = _discrete(1, 2)
        ind = _indiscrete(1, 2)
        f = FiniteMap(domain=disc, codomain=ind, mapping={1: 1, 2: 2}, name="d_to_i")
        assert "warning-line" in render_map_taxonomy_report(f)

    def test_openness_without_continuity_warning(self):
        # ind → disc: trivially open (only ∅ and full set map to open sets) but not continuous
        ind = _indiscrete(1, 2)
        disc = _discrete(1, 2)
        f = FiniteMap(domain=ind, codomain=disc, mapping={1: 1, 2: 2}, name="i_to_d")
        assert "warning-line" in render_map_taxonomy_report(f)

    def test_broken_callable_falls_through_gracefully(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping=lambda x: [][0], name="broken")
        report = render_map_taxonomy_report(f)
        assert "broken" in report


# ---------------------------------------------------------------------------
# Embedding analysis (lines 414-421)
# ---------------------------------------------------------------------------

class TestEmbeddingAnalysis:
    def test_inclusion_into_discrete_is_embedding(self):
        dom = _discrete(1, 2)
        cod = _discrete(1, 2, 3)
        f = FiniteMap(domain=dom, codomain=cod, mapping={1: 1, 2: 2}, name="incl")
        assert is_embedding_map(f).is_true

    def test_non_injective_is_not_embedding(self):
        dom = _discrete(1, 2)
        cod = _discrete(1, 2, 3)
        f = FiniteMap(domain=dom, codomain=cod, mapping={1: 1, 2: 1}, name="non_inj")
        assert is_embedding_map(f).is_false

    def test_continuous_injective_not_open_onto_subspace_is_not_embedding(self):
        # Sierpinski domain {1,2} → indiscrete codomain {1,2,3}
        # continuous (only ∅ and full set need preimages open) and injective,
        # but subspace topology on {1,2} from indiscrete {1,2,3} is indiscrete,
        # so image of Sierpinski open {1} = {1} is not open in that subspace
        sier = _sierpinski()
        ind3 = _indiscrete(1, 2, 3)
        f = FiniteMap(domain=sier, codomain=ind3, mapping={1: 1, 2: 2}, name="sier_to_ind")
        assert is_embedding_map(f).is_false


# ---------------------------------------------------------------------------
# Quotient map analysis (lines 433, 437, 468)
# ---------------------------------------------------------------------------

class TestQuotientAnalysis:
    def test_non_surjective_is_not_quotient(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 1}, name="const")
        assert is_quotient_map(f).is_false

    def test_surjective_non_quotient_map(self):
        # disc {1,2} → ind {1,2}: surjective but preimage({1}) = {1} is open
        # while {1} is not open in indiscrete → fails quotient criterion
        disc = _discrete(1, 2)
        ind = _indiscrete(1, 2)
        f = FiniteMap(domain=disc, codomain=ind, mapping={1: 1, 2: 2}, name="d_to_i")
        assert is_quotient_map(f).is_false

    def test_identity_on_discrete_is_quotient(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        assert is_quotient_map(f).is_true


# ---------------------------------------------------------------------------
# Incomplete mapping domain coverage (line 377)
# ---------------------------------------------------------------------------

class TestIncompleteMappingDomain:
    def test_mapping_missing_key_returns_unknown(self):
        X = _discrete(1, 2, 3)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="partial")
        r = analyze_map_property(f, "continuous")
        assert not r.is_true and not r.is_false


# ---------------------------------------------------------------------------
# _space_is_finite exception branch (lines 487-488)
# ---------------------------------------------------------------------------

class TestSpaceIsFiniteException:
    def test_object_without_is_finite_gives_symbolic_result(self):
        class NoFiniteMethod:
            carrier = (1, 2)

        result = identity_map(NoFiniteMethod())
        assert result is not None
        assert not isinstance(result, FiniteMap)
