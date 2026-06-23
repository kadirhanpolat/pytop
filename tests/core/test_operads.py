"""Tests for pytop.operads."""

from __future__ import annotations

import pytest

from pytop.operads import (
    ASSOC_OPERAD_TAGS,
    BAR_COBAR_TAGS,
    COMM_OPERAD_TAGS,
    INFINITY_ALGEBRA_TAGS,
    KOSZUL_DUALITY_TAGS,
    LIE_OPERAD_TAGS,
    LITTLE_DISKS_TAGS,
    TREE_COMPOSITION_TAGS,
    OperadProfile,
    admits_koszul_dual,
    classify_operad,
    get_named_operad_profiles,
    has_infinity_algebra_structure,
    is_binary_quadratic_operad,
    is_koszul_operad,
    operad_chapter_index,
    operad_layer_summary,
    operad_profile_report,
    operad_type_index,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

class _Space:
    def __init__(self, tags: set[str], representation: str = "test") -> None:
        self.tags = tags
        self.representation = representation


def _space(*tags: str, rep: str = "test") -> _Space:
    return _Space(set(tags), rep)


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_assoc_operad_tags_nonempty(self):
        assert len(ASSOC_OPERAD_TAGS) >= 4

    def test_comm_operad_tags_nonempty(self):
        assert len(COMM_OPERAD_TAGS) >= 4

    def test_lie_operad_tags_nonempty(self):
        assert len(LIE_OPERAD_TAGS) >= 4

    def test_koszul_duality_tags_nonempty(self):
        assert len(KOSZUL_DUALITY_TAGS) >= 4

    def test_infinity_algebra_tags_nonempty(self):
        assert len(INFINITY_ALGEBRA_TAGS) >= 4

    def test_little_disks_tags_nonempty(self):
        assert len(LITTLE_DISKS_TAGS) >= 4

    def test_tree_composition_tags_nonempty(self):
        assert len(TREE_COMPOSITION_TAGS) >= 4

    def test_bar_cobar_tags_nonempty(self):
        assert len(BAR_COBAR_TAGS) >= 4

    def test_assoc_operad_in_assoc_tags(self):
        assert "assoc_operad" in ASSOC_OPERAD_TAGS

    def test_a_infinity_in_assoc_tags(self):
        assert "a_infinity" in ASSOC_OPERAD_TAGS

    def test_stasheff_associahedra_in_assoc_tags(self):
        assert "stasheff_associahedra" in ASSOC_OPERAD_TAGS

    def test_comm_operad_in_comm_tags(self):
        assert "comm_operad" in COMM_OPERAD_TAGS

    def test_e_infinity_in_comm_tags(self):
        assert "e_infinity" in COMM_OPERAD_TAGS

    def test_cdga_in_comm_tags(self):
        assert "cdga" in COMM_OPERAD_TAGS

    def test_lie_operad_in_lie_tags(self):
        assert "lie_operad" in LIE_OPERAD_TAGS

    def test_l_infinity_in_lie_tags(self):
        assert "l_infinity" in LIE_OPERAD_TAGS

    def test_maurer_cartan_in_lie_tags(self):
        assert "maurer_cartan" in LIE_OPERAD_TAGS

    def test_koszul_duality_in_koszul_tags(self):
        assert "koszul_duality" in KOSZUL_DUALITY_TAGS

    def test_ginzburg_kapranov_in_koszul_tags(self):
        assert "ginzburg_kapranov" in KOSZUL_DUALITY_TAGS

    def test_binary_quadratic_in_koszul_tags(self):
        assert "binary_quadratic" in KOSZUL_DUALITY_TAGS

    def test_infinity_algebra_in_infinity_tags(self):
        assert "infinity_algebra" in INFINITY_ALGEBRA_TAGS

    def test_homotopy_transfer_in_infinity_tags(self):
        assert "homotopy_transfer" in INFINITY_ALGEBRA_TAGS

    def test_little_disks_operad_in_little_disks_tags(self):
        assert "little_disks_operad" in LITTLE_DISKS_TAGS

    def test_e_n_operad_in_little_disks_tags(self):
        assert "e_n_operad" in LITTLE_DISKS_TAGS

    def test_factorization_homology_in_little_disks_tags(self):
        assert "factorization_homology" in LITTLE_DISKS_TAGS

    def test_tree_composition_in_tree_tags(self):
        assert "tree_composition" in TREE_COMPOSITION_TAGS

    def test_operadic_composition_in_tree_tags(self):
        assert "operadic_composition" in TREE_COMPOSITION_TAGS

    def test_bar_construction_in_bar_cobar_tags(self):
        assert "bar_construction" in BAR_COBAR_TAGS

    def test_cobar_construction_in_bar_cobar_tags(self):
        assert "cobar_construction" in BAR_COBAR_TAGS

    def test_all_tags_are_frozensets(self):
        for tagset in [
            ASSOC_OPERAD_TAGS, COMM_OPERAD_TAGS, LIE_OPERAD_TAGS,
            KOSZUL_DUALITY_TAGS, INFINITY_ALGEBRA_TAGS, LITTLE_DISKS_TAGS,
            TREE_COMPOSITION_TAGS, BAR_COBAR_TAGS,
        ]:
            assert isinstance(tagset, frozenset)

    def test_tags_contain_strings_only(self):
        for tagset in [ASSOC_OPERAD_TAGS, COMM_OPERAD_TAGS, LIE_OPERAD_TAGS]:
            for tag in tagset:
                assert isinstance(tag, str)


# ---------------------------------------------------------------------------
# Named profiles
# ---------------------------------------------------------------------------

class TestNamedOperadProfiles:
    def setup_method(self):
        self.profiles = get_named_operad_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_six_profiles(self):
        assert len(self.profiles) >= 6

    def test_all_are_operad_profile_instances(self):
        for p in self.profiles:
            assert isinstance(p, OperadProfile)

    def test_all_keys_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_all_keys_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.key, str) and len(p.key) > 0

    def test_all_display_names_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.display_name, str) and len(p.display_name) > 0

    def test_all_focus_strings_long(self):
        for p in self.profiles:
            assert isinstance(p.focus, str) and len(p.focus) > 50

    def test_all_chapter_targets_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.chapter_targets, tuple) and len(p.chapter_targets) >= 1

    def test_assoc_operad_exists(self):
        assert any(p.key == "assoc_operad" for p in self.profiles)

    def test_comm_operad_exists(self):
        assert any(p.key == "comm_operad" for p in self.profiles)

    def test_lie_operad_exists(self):
        assert any(p.key == "lie_operad" for p in self.profiles)

    def test_a_infinity_operad_exists(self):
        assert any(p.key == "a_infinity_operad" for p in self.profiles)

    def test_l_infinity_operad_exists(self):
        assert any(p.key == "l_infinity_operad" for p in self.profiles)

    def test_little_disks_e2_exists(self):
        assert any(p.key == "little_disks_e2" for p in self.profiles)

    def test_koszul_duality_example_exists(self):
        assert any(p.key == "koszul_duality_example" for p in self.profiles)

    def test_colored_operad_exists(self):
        assert any(p.key == "colored_operad" for p in self.profiles)

    def test_assoc_operad_fields(self):
        p = next(x for x in self.profiles if x.key == "assoc_operad")
        assert p.is_koszul is True
        assert p.has_koszul_dual is True
        assert p.is_binary_quadratic is True
        assert p.is_self_dual is True
        assert p.admits_infinity_version is True
        assert p.algebra_type == "associative"

    def test_comm_operad_fields(self):
        p = next(x for x in self.profiles if x.key == "comm_operad")
        assert p.is_koszul is True
        assert p.has_koszul_dual is True
        assert p.is_binary_quadratic is True
        assert p.is_self_dual is False
        assert p.algebra_type == "commutative"

    def test_lie_operad_fields(self):
        p = next(x for x in self.profiles if x.key == "lie_operad")
        assert p.is_koszul is True
        assert p.has_koszul_dual is True
        assert p.is_binary_quadratic is True
        assert p.is_self_dual is False
        assert p.algebra_type == "lie"

    def test_a_infinity_operad_fields(self):
        p = next(x for x in self.profiles if x.key == "a_infinity_operad")
        assert p.is_koszul is False
        assert p.is_binary_quadratic is False
        assert p.algebra_type == "a_infinity"

    def test_l_infinity_operad_fields(self):
        p = next(x for x in self.profiles if x.key == "l_infinity_operad")
        assert p.is_koszul is False
        assert p.is_binary_quadratic is False
        assert p.algebra_type == "l_infinity"

    def test_little_disks_e2_fields(self):
        p = next(x for x in self.profiles if x.key == "little_disks_e2")
        assert p.is_koszul is True
        assert p.operad_type == "topological"
        assert p.algebra_type == "e_n"

    def test_colored_operad_fields(self):
        p = next(x for x in self.profiles if x.key == "colored_operad")
        assert p.operad_type == "colored"
        assert p.is_binary_quadratic is False

    def test_profiles_are_frozen(self):
        p = self.profiles[0]
        with pytest.raises((AttributeError, TypeError)):
            p.key = "modified"  # type: ignore[misc]

    def test_operad_types_are_valid(self):
        valid = {"symmetric", "nonsymmetric", "cyclic", "modular",
                 "colored", "infinity", "topological"}
        for p in self.profiles:
            assert p.operad_type in valid

    def test_algebra_types_are_strings(self):
        for p in self.profiles:
            assert isinstance(p.algebra_type, str) and len(p.algebra_type) > 0


# ---------------------------------------------------------------------------
# Summary functions
# ---------------------------------------------------------------------------

class TestSummaryFunctions:
    def test_operad_layer_summary_returns_dict(self):
        assert isinstance(operad_layer_summary(), dict)

    def test_operad_layer_summary_positive_counts(self):
        for v in operad_layer_summary().values():
            assert v > 0

    def test_operad_layer_summary_total_matches_profiles(self):
        assert sum(operad_layer_summary().values()) == len(get_named_operad_profiles())

    def test_operad_chapter_index_returns_dict(self):
        assert isinstance(operad_chapter_index(), dict)

    def test_operad_chapter_index_values_are_tuples(self):
        for v in operad_chapter_index().values():
            assert isinstance(v, tuple)

    def test_operad_chapter_index_keys_sorted(self):
        keys = list(operad_chapter_index().keys())
        assert keys == sorted(keys)

    def test_operad_chapter_index_contains_chapter_55(self):
        assert "55" in operad_chapter_index()

    def test_operad_type_index_returns_dict(self):
        assert isinstance(operad_type_index(), dict)

    def test_operad_type_index_values_are_tuples(self):
        for v in operad_type_index().values():
            assert isinstance(v, tuple)

    def test_operad_type_index_keys_sorted(self):
        keys = list(operad_type_index().keys())
        assert keys == sorted(keys)

    def test_operad_type_index_contains_symmetric(self):
        assert "symmetric" in operad_type_index()

    def test_operad_type_index_contains_topological(self):
        assert "topological" in operad_type_index()

    def test_operad_type_index_total_matches_profiles(self):
        assert sum(len(v) for v in operad_type_index().values()) == len(get_named_operad_profiles())


# ---------------------------------------------------------------------------
# is_koszul_operad
# ---------------------------------------------------------------------------

class TestIsKoszulOperad:
    def test_koszul_duality_tag(self):
        s = _space("koszul_duality")
        assert is_koszul_operad(s).is_true

    def test_koszul_operad_tag(self):
        s = _space("koszul_operad")
        assert is_koszul_operad(s).is_true

    def test_koszul_complex_tag(self):
        s = _space("koszul_complex")
        assert is_koszul_operad(s).is_true

    def test_ginzburg_kapranov_tag(self):
        s = _space("ginzburg_kapranov")
        assert is_koszul_operad(s).is_true

    def test_koszul_resolution_tag(self):
        s = _space("koszul_resolution")
        assert is_koszul_operad(s).is_true

    def test_assoc_operad_tag(self):
        s = _space("assoc_operad")
        assert is_koszul_operad(s).is_true

    def test_comm_operad_tag(self):
        s = _space("comm_operad")
        assert is_koszul_operad(s).is_true

    def test_lie_operad_tag(self):
        s = _space("lie_operad")
        assert is_koszul_operad(s).is_true

    def test_e_n_operad_tag(self):
        s = _space("e_n_operad")
        assert is_koszul_operad(s).is_true

    def test_little_disks_operad_tag(self):
        s = _space("little_disks_operad")
        assert is_koszul_operad(s).is_true

    def test_homotopy_associative_tag(self):
        s = _space("homotopy_associative")
        assert is_koszul_operad(s).is_true

    def test_non_koszul_tag(self):
        s = _space("non_koszul")
        assert is_koszul_operad(s).is_false

    def test_non_quadratic_operad_tag(self):
        s = _space("non_quadratic_operad")
        assert is_koszul_operad(s).is_false

    def test_not_koszul_tag(self):
        s = _space("not_koszul")
        assert is_koszul_operad(s).is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = is_koszul_operad(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("compact_manifold")
        r = is_koszul_operad(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("assoc_operad")
        r = is_koszul_operad(s)
        assert len(r.justification) >= 1

    def test_result_metadata_has_criterion(self):
        s = _space("koszul_duality")
        r = is_koszul_operad(s)
        assert "criterion" in r.metadata

    def test_poisson_operad_tag(self):
        s = _space("poisson_operad")
        assert is_koszul_operad(s).is_true

    def test_a_infinity_tag(self):
        s = _space("a_infinity")
        assert is_koszul_operad(s).is_true


# ---------------------------------------------------------------------------
# has_infinity_algebra_structure
# ---------------------------------------------------------------------------

class TestHasInfinityAlgebraStructure:
    def test_infinity_algebra_tag(self):
        s = _space("infinity_algebra")
        assert has_infinity_algebra_structure(s).is_true

    def test_homotopy_algebra_tag(self):
        s = _space("homotopy_algebra")
        assert has_infinity_algebra_structure(s).is_true

    def test_a_infinity_tag(self):
        s = _space("a_infinity")
        assert has_infinity_algebra_structure(s).is_true

    def test_l_infinity_tag(self):
        s = _space("l_infinity")
        assert has_infinity_algebra_structure(s).is_true

    def test_homotopy_transfer_tag(self):
        s = _space("homotopy_transfer")
        assert has_infinity_algebra_structure(s).is_true

    def test_minimal_model_tag(self):
        s = _space("minimal_model")
        assert has_infinity_algebra_structure(s).is_true

    def test_bar_cobar_tag(self):
        s = _space("bar_cobar")
        assert has_infinity_algebra_structure(s).is_true

    def test_bar_construction_tag(self):
        s = _space("bar_construction")
        assert has_infinity_algebra_structure(s).is_true

    def test_twisting_morphism_tag(self):
        s = _space("twisting_morphism")
        assert has_infinity_algebra_structure(s).is_true

    def test_assoc_operad_implies_infinity(self):
        s = _space("assoc_operad")
        assert has_infinity_algebra_structure(s).is_true

    def test_comm_operad_implies_infinity(self):
        s = _space("comm_operad")
        assert has_infinity_algebra_structure(s).is_true

    def test_lie_operad_implies_infinity(self):
        s = _space("lie_operad")
        assert has_infinity_algebra_structure(s).is_true

    def test_associative_algebra_implies_infinity(self):
        s = _space("associative_algebra")
        assert has_infinity_algebra_structure(s).is_true

    def test_strict_algebra_only_false(self):
        s = _space("strict_algebra_only")
        assert has_infinity_algebra_structure(s).is_false

    def test_no_higher_operations_false(self):
        s = _space("no_higher_operations")
        assert has_infinity_algebra_structure(s).is_false

    def test_not_homotopy_algebra_false(self):
        s = _space("not_homotopy_algebra")
        assert has_infinity_algebra_structure(s).is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = has_infinity_algebra_structure(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("darboux_theorem")
        r = has_infinity_algebra_structure(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("a_infinity")
        r = has_infinity_algebra_structure(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("bar_construction")
        r = has_infinity_algebra_structure(s)
        assert "criterion" in r.metadata

    def test_c_infinity_tag(self):
        s = _space("c_infinity")
        assert has_infinity_algebra_structure(s).is_true

    def test_maurer_cartan_tag(self):
        s = _space("maurer_cartan")
        assert has_infinity_algebra_structure(s).is_true


# ---------------------------------------------------------------------------
# admits_koszul_dual
# ---------------------------------------------------------------------------

class TestAdmitsKoszulDual:
    def test_koszul_duality_tag(self):
        s = _space("koszul_duality")
        assert admits_koszul_dual(s).is_true

    def test_koszul_dual_tag(self):
        s = _space("koszul_dual")
        assert admits_koszul_dual(s).is_true

    def test_quadratic_dual_tag(self):
        s = _space("quadratic_dual")
        assert admits_koszul_dual(s).is_true

    def test_assoc_operad_has_dual(self):
        s = _space("assoc_operad")
        assert admits_koszul_dual(s).is_true

    def test_comm_operad_has_dual(self):
        s = _space("comm_operad")
        assert admits_koszul_dual(s).is_true

    def test_lie_operad_has_dual(self):
        s = _space("lie_operad")
        assert admits_koszul_dual(s).is_true

    def test_binary_quadratic_tag(self):
        s = _space("binary_quadratic")
        assert admits_koszul_dual(s).is_true

    def test_poisson_operad_has_dual(self):
        s = _space("poisson_operad")
        assert admits_koszul_dual(s).is_true

    def test_pre_lie_operad_has_dual(self):
        s = _space("pre_lie_operad")
        assert admits_koszul_dual(s).is_true

    def test_zinbiel_operad_has_dual(self):
        s = _space("zinbiel_operad")
        assert admits_koszul_dual(s).is_true

    def test_colored_operad_no_dual(self):
        s = _space("colored_operad")
        assert admits_koszul_dual(s).is_false

    def test_modular_operad_no_dual(self):
        s = _space("modular_operad")
        assert admits_koszul_dual(s).is_false

    def test_prop_operad_no_dual(self):
        s = _space("prop_operad")
        assert admits_koszul_dual(s).is_false

    def test_non_binary_no_dual(self):
        s = _space("non_binary")
        assert admits_koszul_dual(s).is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = admits_koszul_dual(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("kahler_manifold")
        r = admits_koszul_dual(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("comm_operad")
        r = admits_koszul_dual(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("koszul_duality")
        r = admits_koszul_dual(s)
        assert "criterion" in r.metadata

    def test_zinbiel_with_binary_quadratic_tag(self):
        s = _space("zinbiel_operad", "binary_quadratic")
        assert admits_koszul_dual(s).is_true


# ---------------------------------------------------------------------------
# is_binary_quadratic_operad
# ---------------------------------------------------------------------------

class TestIsBinaryQuadraticOperad:
    def test_binary_quadratic_tag(self):
        s = _space("binary_quadratic")
        assert is_binary_quadratic_operad(s).is_true

    def test_quadratic_operad_tag(self):
        s = _space("quadratic_operad")
        assert is_binary_quadratic_operad(s).is_true

    def test_tree_composition_tag(self):
        s = _space("tree_composition")
        assert is_binary_quadratic_operad(s).is_true

    def test_operadic_composition_tag(self):
        s = _space("operadic_composition")
        assert is_binary_quadratic_operad(s).is_true

    def test_symmetric_sequence_tag(self):
        s = _space("symmetric_sequence")
        assert is_binary_quadratic_operad(s).is_true

    def test_assoc_operad_is_binary_quadratic(self):
        s = _space("assoc_operad")
        assert is_binary_quadratic_operad(s).is_true

    def test_comm_operad_is_binary_quadratic(self):
        s = _space("comm_operad")
        assert is_binary_quadratic_operad(s).is_true

    def test_lie_operad_is_binary_quadratic(self):
        s = _space("lie_operad")
        assert is_binary_quadratic_operad(s).is_true

    def test_poisson_operad_is_binary_quadratic(self):
        s = _space("poisson_operad")
        assert is_binary_quadratic_operad(s).is_true

    def test_pre_lie_is_binary_quadratic(self):
        s = _space("pre_lie_operad")
        assert is_binary_quadratic_operad(s).is_true

    def test_colored_operad_not_binary_quadratic(self):
        s = _space("colored_operad")
        assert is_binary_quadratic_operad(s).is_false

    def test_a_infinity_operad_not_binary_quadratic(self):
        s = _space("a_infinity_operad")
        assert is_binary_quadratic_operad(s).is_false

    def test_l_infinity_operad_not_binary_quadratic(self):
        s = _space("l_infinity_operad")
        assert is_binary_quadratic_operad(s).is_false

    def test_modular_operad_not_binary_quadratic(self):
        s = _space("modular_operad")
        assert is_binary_quadratic_operad(s).is_false

    def test_higher_arity_not_binary_quadratic(self):
        s = _space("higher_arity")
        assert is_binary_quadratic_operad(s).is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = is_binary_quadratic_operad(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("nisnevich_topology")
        r = is_binary_quadratic_operad(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("assoc_operad")
        r = is_binary_quadratic_operad(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("binary_quadratic")
        r = is_binary_quadratic_operad(s)
        assert "criterion" in r.metadata

    def test_dendriform_is_binary_quadratic(self):
        s = _space("dendriform_operad")
        assert is_binary_quadratic_operad(s).is_true


# ---------------------------------------------------------------------------
# classify_operad
# ---------------------------------------------------------------------------

class TestClassifyOperad:
    def test_returns_dict(self):
        assert isinstance(classify_operad(_space()), dict)

    def test_has_four_keys(self):
        assert len(classify_operad(_space())) == 4

    def test_has_is_koszul_operad_key(self):
        assert "is_koszul_operad" in classify_operad(_space())

    def test_has_has_infinity_algebra_structure_key(self):
        assert "has_infinity_algebra_structure" in classify_operad(_space())

    def test_has_admits_koszul_dual_key(self):
        assert "admits_koszul_dual" in classify_operad(_space())

    def test_has_is_binary_quadratic_operad_key(self):
        assert "is_binary_quadratic_operad" in classify_operad(_space())

    def test_assoc_operad_space(self):
        s = _space("assoc_operad", "a_infinity", "binary_quadratic")
        r = classify_operad(s)
        assert r["is_koszul_operad"].is_true
        assert r["has_infinity_algebra_structure"].is_true
        assert r["admits_koszul_dual"].is_true
        assert r["is_binary_quadratic_operad"].is_true

    def test_colored_operad_space(self):
        s = _space("colored_operad", "non_binary")
        r = classify_operad(s)
        assert r["admits_koszul_dual"].is_false
        assert r["is_binary_quadratic_operad"].is_false

    def test_empty_space_all_unknown(self):
        s = _space()
        for r in classify_operad(s).values():
            assert not r.is_true and not r.is_false


# ---------------------------------------------------------------------------
# operad_profile_report
# ---------------------------------------------------------------------------

class TestOperadProfileReport:
    def test_returns_dict(self):
        assert isinstance(operad_profile_report(_space()), dict)

    def test_has_space_key(self):
        assert "space" in operad_profile_report(_space())

    def test_has_tags_key(self):
        assert "tags" in operad_profile_report(_space("assoc_operad"))

    def test_has_representation_key(self):
        assert "representation" in operad_profile_report(_space())

    def test_has_classification_key(self):
        assert "classification" in operad_profile_report(_space())

    def test_has_summary_key(self):
        assert "summary" in operad_profile_report(_space())

    def test_tags_is_sorted_list(self):
        s = _space("comm_operad", "assoc_operad")
        result = operad_profile_report(s)
        tags = result["tags"]
        assert isinstance(tags, list) and tags == sorted(tags)

    def test_summary_has_four_entries(self):
        assert len(operad_profile_report(_space())["summary"]) == 4

    def test_summary_values_are_strings(self):
        s = _space("assoc_operad")
        for v in operad_profile_report(s)["summary"].values():
            assert isinstance(v, str)

    def test_space_attribute_preserved(self):
        s = _space("lie_operad")
        result = operad_profile_report(s)
        assert result["space"] is s
