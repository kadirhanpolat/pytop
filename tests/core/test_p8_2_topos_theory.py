"""Tests for P8.2: topos_theory computational engines.

Functions tested: site_from_finite_topology, sheaf_on_site,
sheafification_finite, topos_check
"""
import pytest
from pytop import (
    site_from_finite_topology,
    sheaf_on_site,
    sheafification_finite,
    topos_check,
)


_EMPTY = frozenset()
_U0 = frozenset({0})
_U01 = frozenset({0, 1})
_SIMP_OPENS = [_EMPTY, _U0, _U01]
_SIMP_UNIV = _U01

_DISCRETE = [_EMPTY, frozenset({0}), frozenset({1}), frozenset({0, 1})]
_INDISCRETE = [_EMPTY, frozenset({0, 1})]


# ---------------------------------------------------------------------------
# site_from_finite_topology
# ---------------------------------------------------------------------------

class TestSiteFromFiniteTopology:
    def test_n_objects_correct(self):
        site = site_from_finite_topology(_SIMP_OPENS, _SIMP_UNIV)
        assert site["n_objects"] == 3

    def test_topology_valid_for_valid_input(self):
        site = site_from_finite_topology(_SIMP_OPENS, _SIMP_UNIV)
        assert site["topology_valid"] is True

    def test_topology_invalid_without_empty_set(self):
        site = site_from_finite_topology([frozenset({0}), frozenset({0, 1})],
                                          frozenset({0, 1}))
        assert site["topology_valid"] is False

    def test_objects_are_frozensets(self):
        site = site_from_finite_topology(_SIMP_OPENS, _SIMP_UNIV)
        for o in site["objects"]:
            assert isinstance(o, frozenset)

    def test_coverings_key_present(self):
        site = site_from_finite_topology(_SIMP_OPENS, _SIMP_UNIV)
        assert "coverings" in site

    def test_coverings_contains_all_objects(self):
        site = site_from_finite_topology(_SIMP_OPENS, _SIMP_UNIV)
        for u in site["objects"]:
            assert u in site["coverings"]

    def test_n_morphisms_correct(self):
        site = site_from_finite_topology(_SIMP_OPENS, _SIMP_UNIV)
        # Morphisms: ∅<{0}, ∅<{0,1}, {0}<{0,1} → 3 pairs
        assert site["n_morphisms"] == 3

    def test_discrete_topology_valid(self):
        site = site_from_finite_topology(_DISCRETE, frozenset({0, 1}))
        assert site["topology_valid"] is True

    def test_indiscrete_topology_valid(self):
        site = site_from_finite_topology(_INDISCRETE, frozenset({0, 1}))
        assert site["topology_valid"] is True

    def test_single_point_topology(self):
        site = site_from_finite_topology([_EMPTY, frozenset({0})], frozenset({0}))
        assert site["topology_valid"] is True
        assert site["n_objects"] == 2


# ---------------------------------------------------------------------------
# sheaf_on_site
# ---------------------------------------------------------------------------

class TestSheafOnSite:
    def _site(self):
        return site_from_finite_topology(_SIMP_OPENS, _SIMP_UNIV)

    def test_constant_assignment_is_sheaf(self):
        site = self._site()
        assignment = {u: 1 for u in site["objects"]}
        result = sheaf_on_site(site, assignment)
        assert result["is_sheaf"] is True

    def test_locality_ok_for_constant(self):
        site = self._site()
        assignment = {u: 42 for u in site["objects"]}
        result = sheaf_on_site(site, assignment)
        assert result["locality_ok"] is True

    def test_gluing_ok_for_constant(self):
        site = self._site()
        assignment = {u: 7 for u in site["objects"]}
        result = sheaf_on_site(site, assignment)
        assert result["gluing_ok"] is True

    def test_failures_empty_for_sheaf(self):
        site = self._site()
        assignment = {u: 5 for u in site["objects"]}
        result = sheaf_on_site(site, assignment)
        assert result["failures"] == []

    def test_inconsistent_assignment_not_sheaf(self):
        site = self._site()
        # Assign different values: F({0})=1 but F({0,1})=99
        assignment = {_EMPTY: 0, _U0: 1, _U01: 99}
        result = sheaf_on_site(site, assignment)
        assert result["is_sheaf"] is False

    def test_return_keys_present(self):
        site = self._site()
        result = sheaf_on_site(site, {})
        for key in ("locality_ok", "gluing_ok", "is_sheaf", "failures"):
            assert key in result

    def test_zero_value_constant_is_sheaf(self):
        site = self._site()
        assignment = {u: 0 for u in site["objects"]}
        assert sheaf_on_site(site, assignment)["is_sheaf"] is True


# ---------------------------------------------------------------------------
# sheafification_finite
# ---------------------------------------------------------------------------

class TestSheafificationFinite:
    def _site(self):
        return site_from_finite_topology(_SIMP_OPENS, _SIMP_UNIV)

    def test_constant_presheaf_already_sheaf(self):
        site = self._site()
        presheaf = {u: 7 for u in site["objects"]}
        result = sheafification_finite(site, presheaf)
        assert result["already_sheaf"] is True

    def test_n_corrections_zero_for_sheaf(self):
        site = self._site()
        presheaf = {u: 3 for u in site["objects"]}
        result = sheafification_finite(site, presheaf)
        assert result["n_corrections"] == 0

    def test_return_keys_present(self):
        site = self._site()
        result = sheafification_finite(site, {})
        for key in ("sheafification", "already_sheaf", "n_corrections", "is_sheaf_after"):
            assert key in result

    def test_inconsistent_value_gets_corrected(self):
        site = self._site()
        # F(∅)=1, F({0})=1 → cover of {0,1} agrees on 1 → sheafification corrects {0,1}→1
        presheaf = {_EMPTY: 1, _U0: 1, _U01: 99}
        result = sheafification_finite(site, presheaf)
        assert result["n_corrections"] >= 1
        # After sheafification the result should be a sheaf
        assert result["is_sheaf_after"] is True

    def test_output_sheafification_is_dict(self):
        site = self._site()
        presheaf = {u: 5 for u in site["objects"]}
        result = sheafification_finite(site, presheaf)
        assert isinstance(result["sheafification"], dict)


# ---------------------------------------------------------------------------
# topos_check
# ---------------------------------------------------------------------------

class TestToposCheck:
    def test_valid_topology_is_topos(self):
        result = topos_check(_SIMP_OPENS, _SIMP_UNIV)
        assert result["is_grothendieck_topos"] is True

    def test_discrete_topology_is_topos(self):
        result = topos_check(_DISCRETE, frozenset({0, 1}))
        assert result["is_grothendieck_topos"] is True

    def test_has_terminal_object(self):
        result = topos_check(_SIMP_OPENS, _SIMP_UNIV)
        assert result["has_terminal"] is True

    def test_has_fiber_products(self):
        result = topos_check(_SIMP_OPENS, _SIMP_UNIV)
        assert result["has_fiber_products"] is True

    def test_has_subobject_classifier(self):
        result = topos_check(_SIMP_OPENS, _SIMP_UNIV)
        assert result["has_subobject_classifier"] is True

    def test_n_objects_in_result(self):
        result = topos_check(_SIMP_OPENS, _SIMP_UNIV)
        assert result["n_objects"] == 3
