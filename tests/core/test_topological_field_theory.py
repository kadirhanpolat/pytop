"""Tests for pytop.topological_field_theory module (~175 tests)."""

from __future__ import annotations

import pytest

from pytop.result import Result
from pytop.topological_field_theory import (
    ATIYAH_SEGAL_TAGS,
    CHERN_SIMONS_TAGS,
    COBORDISM_HYPOTHESIS_TAGS,
    DONALDSON_TAGS,
    EXTENDED_TFT_TAGS,
    FACTORIZATION_ALGEBRA_TAGS,
    FROBENIUS_ALGEBRA_TAGS,
    TOPOLOGICAL_STRING_TAGS,
    TFTProfile,
    admits_higher_categorical_formulation,
    classify_tft,
    get_named_tft_profiles,
    has_frobenius_algebra_structure,
    is_extended_tft,
    satisfies_atiyah_segal_axioms,
    tft_dimension_registry,
    tft_profile_report,
    tft_summary,
    tft_type_registry,
)


def _space(*tags: str) -> str:
    return " ".join(tags)


# ---------------------------------------------------------------------------
# TestTFTTagConstants
# ---------------------------------------------------------------------------

class TestTFTTagConstants:
    def test_atiyah_segal_tags_is_frozenset(self):
        assert isinstance(ATIYAH_SEGAL_TAGS, frozenset)

    def test_atiyah_segal_tags_nonempty(self):
        assert len(ATIYAH_SEGAL_TAGS) > 0

    def test_atiyah_segal_tags_contains_expected(self):
        assert "atiyah_segal" in ATIYAH_SEGAL_TAGS
        assert "cobordism_category" in ATIYAH_SEGAL_TAGS
        assert "gluing_axiom" in ATIYAH_SEGAL_TAGS

    def test_cobordism_hypothesis_tags_is_frozenset(self):
        assert isinstance(COBORDISM_HYPOTHESIS_TAGS, frozenset)

    def test_cobordism_hypothesis_tags_nonempty(self):
        assert len(COBORDISM_HYPOTHESIS_TAGS) > 0

    def test_cobordism_hypothesis_tags_contains_expected(self):
        assert "cobordism_hypothesis" in COBORDISM_HYPOTHESIS_TAGS
        assert "fully_dualizable" in COBORDISM_HYPOTHESIS_TAGS
        assert "lurie_classification" in COBORDISM_HYPOTHESIS_TAGS

    def test_frobenius_algebra_tags_is_frozenset(self):
        assert isinstance(FROBENIUS_ALGEBRA_TAGS, frozenset)

    def test_frobenius_algebra_tags_nonempty(self):
        assert len(FROBENIUS_ALGEBRA_TAGS) > 0

    def test_frobenius_algebra_tags_contains_expected(self):
        assert "frobenius_algebra" in FROBENIUS_ALGEBRA_TAGS
        assert "commutative_frobenius" in FROBENIUS_ALGEBRA_TAGS
        assert "two_dim_tft" in FROBENIUS_ALGEBRA_TAGS

    def test_extended_tft_tags_is_frozenset(self):
        assert isinstance(EXTENDED_TFT_TAGS, frozenset)

    def test_extended_tft_tags_nonempty(self):
        assert len(EXTENDED_TFT_TAGS) > 0

    def test_extended_tft_tags_contains_expected(self):
        assert "extended_tft" in EXTENDED_TFT_TAGS
        assert "fully_extended" in EXTENDED_TFT_TAGS
        assert "higher_categorical" in EXTENDED_TFT_TAGS

    def test_chern_simons_tags_is_frozenset(self):
        assert isinstance(CHERN_SIMONS_TAGS, frozenset)

    def test_chern_simons_tags_nonempty(self):
        assert len(CHERN_SIMONS_TAGS) > 0

    def test_chern_simons_tags_contains_expected(self):
        assert "chern_simons" in CHERN_SIMONS_TAGS
        assert "jones_polynomial" in CHERN_SIMONS_TAGS
        assert "modular_tensor_category" in CHERN_SIMONS_TAGS

    def test_factorization_algebra_tags_is_frozenset(self):
        assert isinstance(FACTORIZATION_ALGEBRA_TAGS, frozenset)

    def test_factorization_algebra_tags_nonempty(self):
        assert len(FACTORIZATION_ALGEBRA_TAGS) > 0

    def test_factorization_algebra_tags_contains_expected(self):
        assert "factorization_algebra" in FACTORIZATION_ALGEBRA_TAGS
        assert "costello_gwilliam" in FACTORIZATION_ALGEBRA_TAGS
        assert "ran_space" in FACTORIZATION_ALGEBRA_TAGS

    def test_donaldson_tags_is_frozenset(self):
        assert isinstance(DONALDSON_TAGS, frozenset)

    def test_donaldson_tags_nonempty(self):
        assert len(DONALDSON_TAGS) > 0

    def test_donaldson_tags_contains_expected(self):
        assert "donaldson_theory" in DONALDSON_TAGS
        assert "four_manifold" in DONALDSON_TAGS
        assert "seiberg_witten" in DONALDSON_TAGS

    def test_topological_string_tags_is_frozenset(self):
        assert isinstance(TOPOLOGICAL_STRING_TAGS, frozenset)

    def test_topological_string_tags_nonempty(self):
        assert len(TOPOLOGICAL_STRING_TAGS) > 0

    def test_topological_string_tags_contains_expected(self):
        assert "topological_string" in TOPOLOGICAL_STRING_TAGS
        assert "gromov_witten" in TOPOLOGICAL_STRING_TAGS
        assert "calabi_yau" in TOPOLOGICAL_STRING_TAGS

    def test_all_tag_constants_are_frozensets_of_str(self):
        for tagset in [
            ATIYAH_SEGAL_TAGS, COBORDISM_HYPOTHESIS_TAGS, FROBENIUS_ALGEBRA_TAGS,
            EXTENDED_TFT_TAGS, CHERN_SIMONS_TAGS, FACTORIZATION_ALGEBRA_TAGS,
            DONALDSON_TAGS, TOPOLOGICAL_STRING_TAGS,
        ]:
            assert isinstance(tagset, frozenset)
            for t in tagset:
                assert isinstance(t, str)

    def test_tag_constants_have_eight_elements_each(self):
        for tagset in [
            ATIYAH_SEGAL_TAGS, COBORDISM_HYPOTHESIS_TAGS, FROBENIUS_ALGEBRA_TAGS,
            EXTENDED_TFT_TAGS, CHERN_SIMONS_TAGS, FACTORIZATION_ALGEBRA_TAGS,
            DONALDSON_TAGS, TOPOLOGICAL_STRING_TAGS,
        ]:
            assert len(tagset) == 8


# ---------------------------------------------------------------------------
# TestTFTProfileDataclass
# ---------------------------------------------------------------------------

class TestTFTProfileDataclass:
    @pytest.fixture
    def profiles(self):
        return get_named_tft_profiles()

    def test_returns_tuple_of_eight(self, profiles):
        assert isinstance(profiles, tuple)
        assert len(profiles) == 8

    def test_all_profiles_are_tftprofile(self, profiles):
        for p in profiles:
            assert isinstance(p, TFTProfile)

    def test_atiyah_segal_tft_key(self, profiles):
        keys = [p.key for p in profiles]
        assert "atiyah_segal_tft" in keys

    def test_atiyah_segal_tft_type(self, profiles):
        p = next(x for x in profiles if x.key == "atiyah_segal_tft")
        assert p.tft_type == "atiyah_segal"

    def test_atiyah_segal_tft_dimension(self, profiles):
        p = next(x for x in profiles if x.key == "atiyah_segal_tft")
        assert p.dimension == 2

    def test_atiyah_segal_tft_not_extended(self, profiles):
        p = next(x for x in profiles if x.key == "atiyah_segal_tft")
        assert p.is_extended is False

    def test_atiyah_segal_tft_has_frobenius(self, profiles):
        p = next(x for x in profiles if x.key == "atiyah_segal_tft")
        assert p.has_frobenius_structure is True

    def test_cobordism_hypothesis_tft_extended(self, profiles):
        p = next(x for x in profiles if x.key == "cobordism_hypothesis_tft")
        assert p.is_extended is True

    def test_cobordism_hypothesis_tft_type(self, profiles):
        p = next(x for x in profiles if x.key == "cobordism_hypothesis_tft")
        assert p.tft_type == "extended_tft"

    def test_cobordism_hypothesis_tft_dimension(self, profiles):
        p = next(x for x in profiles if x.key == "cobordism_hypothesis_tft")
        assert p.dimension == 3

    def test_two_dim_frobenius_tft_type(self, profiles):
        p = next(x for x in profiles if x.key == "two_dim_frobenius_tft")
        assert p.tft_type == "frobenius"

    def test_two_dim_frobenius_tft_dimension(self, profiles):
        p = next(x for x in profiles if x.key == "two_dim_frobenius_tft")
        assert p.dimension == 2

    def test_chern_simons_has_anomaly(self, profiles):
        p = next(x for x in profiles if x.key == "chern_simons_tft")
        assert p.has_anomaly is True

    def test_chern_simons_dimension(self, profiles):
        p = next(x for x in profiles if x.key == "chern_simons_tft")
        assert p.dimension == 3

    def test_donaldson_tft_dimension(self, profiles):
        p = next(x for x in profiles if x.key == "donaldson_tft")
        assert p.dimension == 4

    def test_donaldson_tft_not_extended(self, profiles):
        p = next(x for x in profiles if x.key == "donaldson_tft")
        assert p.is_extended is False

    def test_factorization_algebra_tft_dimension(self, profiles):
        p = next(x for x in profiles if x.key == "factorization_algebra_tft")
        assert p.dimension == 4

    def test_factorization_algebra_tft_extended(self, profiles):
        p = next(x for x in profiles if x.key == "factorization_algebra_tft")
        assert p.is_extended is True

    def test_topological_string_tft_type(self, profiles):
        p = next(x for x in profiles if x.key == "topological_string_tft")
        assert p.tft_type == "topological_string"

    def test_topological_string_tft_dimension(self, profiles):
        p = next(x for x in profiles if x.key == "topological_string_tft")
        assert p.dimension == 2

    def test_all_profiles_have_300char_focus(self, profiles):
        for p in profiles:
            assert len(p.focus) >= 300, f"{p.key} focus too short: {len(p.focus)}"

    def test_all_profiles_frozen(self, profiles):
        p = profiles[0]
        with pytest.raises((TypeError, AttributeError)):
            p.key = "modified"  # type: ignore[misc]

    def test_once_extended_tft_presentation_layer(self, profiles):
        p = next(x for x in profiles if x.key == "once_extended_tft")
        assert p.presentation_layer == 3

    def test_two_dim_frobenius_presentation_layer_1(self, profiles):
        p = next(x for x in profiles if x.key == "two_dim_frobenius_tft")
        assert p.presentation_layer == 1

    def test_chapter_targets_are_lists(self, profiles):
        for p in profiles:
            assert isinstance(p.chapter_targets, list)


# ---------------------------------------------------------------------------
# TestSummaryFunctions
# ---------------------------------------------------------------------------

class TestSummaryFunctions:
    def test_tft_summary_returns_dict(self):
        result = tft_summary()
        assert isinstance(result, dict)

    def test_tft_summary_has_total_key(self):
        result = tft_summary()
        assert "total" in result

    def test_tft_summary_total_is_8(self):
        result = tft_summary()
        assert result["total"] == 8

    def test_tft_summary_has_by_type_key(self):
        result = tft_summary()
        assert "by_type" in result

    def test_tft_summary_has_by_dimension_key(self):
        result = tft_summary()
        assert "by_dimension" in result

    def test_tft_summary_by_type_is_dict(self):
        result = tft_summary()
        assert isinstance(result["by_type"], dict)

    def test_tft_summary_by_dimension_is_dict(self):
        result = tft_summary()
        assert isinstance(result["by_dimension"], dict)

    def test_tft_summary_by_type_counts_sum_to_8(self):
        result = tft_summary()
        assert sum(result["by_type"].values()) == 8  # type: ignore[union-attr]

    def test_tft_summary_by_dimension_counts_sum_to_8(self):
        result = tft_summary()
        assert sum(result["by_dimension"].values()) == 8  # type: ignore[union-attr]

    def test_tft_type_registry_returns_dict(self):
        reg = tft_type_registry()
        assert isinstance(reg, dict)

    def test_tft_type_registry_contains_atiyah_segal(self):
        reg = tft_type_registry()
        assert "atiyah_segal" in reg

    def test_tft_type_registry_contains_extended_tft(self):
        reg = tft_type_registry()
        assert "extended_tft" in reg

    def test_tft_type_registry_contains_frobenius(self):
        reg = tft_type_registry()
        assert "frobenius" in reg

    def test_tft_type_registry_all_keys_in_profiles(self):
        reg = tft_type_registry()
        profile_keys = {p.key for p in get_named_tft_profiles()}
        for v_list in reg.values():
            for k in v_list:
                assert k in profile_keys

    def test_tft_dimension_registry_returns_dict(self):
        reg = tft_dimension_registry()
        assert isinstance(reg, dict)

    def test_tft_dimension_registry_has_dim_2(self):
        reg = tft_dimension_registry()
        assert 2 in reg

    def test_tft_dimension_registry_has_dim_3(self):
        reg = tft_dimension_registry()
        assert 3 in reg

    def test_tft_dimension_registry_has_dim_4(self):
        reg = tft_dimension_registry()
        assert 4 in reg

    def test_tft_dimension_registry_dim2_multiple(self):
        reg = tft_dimension_registry()
        assert len(reg[2]) >= 2

    def test_tft_dimension_registry_totals_8(self):
        reg = tft_dimension_registry()
        assert sum(len(v) for v in reg.values()) == 8


# ---------------------------------------------------------------------------
# TestIsExtendedTft
# ---------------------------------------------------------------------------

class TestIsExtendedTft:
    def test_extended_tft_tag_returns_true(self):
        r = is_extended_tft(_space("extended_tft"))
        assert r.is_true

    def test_fully_extended_tag_returns_true(self):
        r = is_extended_tft(_space("fully_extended"))
        assert r.is_true

    def test_higher_categorical_tag_returns_true(self):
        r = is_extended_tft(_space("higher_categorical"))
        assert r.is_true

    def test_once_extended_tag_returns_true(self):
        r = is_extended_tft(_space("once_extended"))
        assert r.is_true

    def test_cobordism_hypothesis_tag_returns_true(self):
        r = is_extended_tft(_space("cobordism_hypothesis"))
        assert r.is_true

    def test_fully_dualizable_tag_returns_true(self):
        r = is_extended_tft(_space("fully_dualizable"))
        assert r.is_true

    def test_lurie_classification_tag_returns_true(self):
        r = is_extended_tft(_space("lurie_classification"))
        assert r.is_true

    def test_factorization_algebra_tag_returns_true(self):
        r = is_extended_tft(_space("factorization_algebra"))
        assert r.is_true

    def test_costello_gwilliam_tag_returns_true(self):
        r = is_extended_tft(_space("costello_gwilliam"))
        assert r.is_true

    def test_atiyah_segal_alone_returns_false(self):
        r = is_extended_tft(_space("atiyah_segal"))
        assert r.is_false

    def test_cobordism_category_alone_returns_false(self):
        r = is_extended_tft(_space("cobordism_category"))
        assert r.is_false

    def test_frobenius_algebra_alone_returns_false(self):
        r = is_extended_tft(_space("frobenius_algebra"))
        assert r.is_false

    def test_empty_returns_unknown(self):
        r = is_extended_tft("")
        assert r.is_unknown

    def test_irrelevant_text_returns_unknown(self):
        r = is_extended_tft("some random text without topology")
        assert r.is_unknown

    def test_returns_result_instance(self):
        r = is_extended_tft("extended_tft")
        assert isinstance(r, Result)

    def test_default_mode_symbolic(self):
        r = is_extended_tft("extended_tft")
        assert r.mode == "symbolic"

    def test_custom_mode_respected(self):
        r = is_extended_tft("extended_tft", mode="exact")
        assert r.mode == "exact"

    def test_justification_nonempty(self):
        r = is_extended_tft("extended_tft")
        assert len(r.justification) > 0

    def test_n_extended_tag_returns_true(self):
        r = is_extended_tft(_space("n_extended"))
        assert r.is_true

    def test_bordism_bicategory_tag_returns_true(self):
        r = is_extended_tft(_space("bordism_bicategory"))
        assert r.is_true

    def test_two_dim_tft_alone_returns_false(self):
        r = is_extended_tft(_space("two_dim_tft"))
        assert r.is_false

    def test_gluing_axiom_returns_false(self):
        r = is_extended_tft(_space("gluing_axiom"))
        assert r.is_false


# ---------------------------------------------------------------------------
# TestSatisfiesAtiyahSegalAxioms
# ---------------------------------------------------------------------------

class TestSatisfiesAtiyahSegalAxioms:
    def test_atiyah_segal_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("atiyah_segal"))
        assert r.is_true

    def test_cobordism_category_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("cobordism_category"))
        assert r.is_true

    def test_gluing_axiom_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("gluing_axiom"))
        assert r.is_true

    def test_partition_function_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("partition_function"))
        assert r.is_true

    def test_frobenius_algebra_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("frobenius_algebra"))
        assert r.is_true

    def test_two_dim_tft_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("two_dim_tft"))
        assert r.is_true

    def test_chern_simons_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("chern_simons"))
        assert r.is_true

    def test_jones_polynomial_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("jones_polynomial"))
        assert r.is_true

    def test_donaldson_theory_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("donaldson_theory"))
        assert r.is_true

    def test_yang_mills_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("yang_mills"))
        assert r.is_true

    def test_empty_returns_unknown(self):
        r = satisfies_atiyah_segal_axioms("")
        assert r.is_unknown

    def test_random_text_returns_unknown(self):
        r = satisfies_atiyah_segal_axioms("banana orange apple")
        assert r.is_unknown

    def test_returns_result_instance(self):
        r = satisfies_atiyah_segal_axioms("atiyah_segal")
        assert isinstance(r, Result)

    def test_default_mode_symbolic(self):
        r = satisfies_atiyah_segal_axioms("atiyah_segal")
        assert r.mode == "symbolic"

    def test_custom_mode_theorem(self):
        r = satisfies_atiyah_segal_axioms("atiyah_segal", mode="theorem")
        assert r.mode == "theorem"

    def test_justification_nonempty_for_true(self):
        r = satisfies_atiyah_segal_axioms("atiyah_segal")
        assert len(r.justification) > 0

    def test_justification_nonempty_for_unknown(self):
        r = satisfies_atiyah_segal_axioms("")
        assert len(r.justification) > 0

    def test_functor_from_cobordisms_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("functor_from_cobordisms"))
        assert r.is_true

    def test_symmetric_monoidal_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("symmetric_monoidal"))
        assert r.is_true

    def test_instanton_tag_returns_true(self):
        r = satisfies_atiyah_segal_axioms(_space("instanton"))
        assert r.is_true


# ---------------------------------------------------------------------------
# TestHasFrobeniusAlgebraStructure
# ---------------------------------------------------------------------------

class TestHasFrobeniusAlgebraStructure:
    def test_frobenius_algebra_tag_returns_true(self):
        r = has_frobenius_algebra_structure(_space("frobenius_algebra"))
        assert r.is_true

    def test_commutative_frobenius_tag_returns_true(self):
        r = has_frobenius_algebra_structure(_space("commutative_frobenius"))
        assert r.is_true

    def test_two_dim_tft_tag_returns_true(self):
        r = has_frobenius_algebra_structure(_space("two_dim_tft"))
        assert r.is_true

    def test_frobenius_relation_tag_returns_true(self):
        r = has_frobenius_algebra_structure(_space("frobenius_relation"))
        assert r.is_true

    def test_topological_string_tag_returns_true(self):
        r = has_frobenius_algebra_structure(_space("topological_string"))
        assert r.is_true

    def test_gromov_witten_tag_returns_true(self):
        r = has_frobenius_algebra_structure(_space("gromov_witten"))
        assert r.is_true

    def test_calabi_yau_tag_returns_true(self):
        r = has_frobenius_algebra_structure(_space("calabi_yau"))
        assert r.is_true

    def test_cobordism_hypothesis_returns_false(self):
        r = has_frobenius_algebra_structure(_space("cobordism_hypothesis"))
        assert r.is_false

    def test_fully_dualizable_returns_false(self):
        r = has_frobenius_algebra_structure(_space("fully_dualizable"))
        assert r.is_false

    def test_factorization_algebra_returns_false(self):
        r = has_frobenius_algebra_structure(_space("factorization_algebra"))
        assert r.is_false

    def test_ran_space_returns_false(self):
        r = has_frobenius_algebra_structure(_space("ran_space"))
        assert r.is_false

    def test_empty_returns_unknown(self):
        r = has_frobenius_algebra_structure("")
        assert r.is_unknown

    def test_random_text_returns_unknown(self):
        r = has_frobenius_algebra_structure("hello world")
        assert r.is_unknown

    def test_returns_result_instance(self):
        r = has_frobenius_algebra_structure("frobenius_algebra")
        assert isinstance(r, Result)

    def test_default_mode_symbolic(self):
        r = has_frobenius_algebra_structure("frobenius_algebra")
        assert r.mode == "symbolic"

    def test_pants_decomposition_returns_true(self):
        r = has_frobenius_algebra_structure(_space("pants_decomposition"))
        assert r.is_true

    def test_handle_decomposition_returns_true(self):
        r = has_frobenius_algebra_structure(_space("handle_decomposition"))
        assert r.is_true

    def test_a_model_returns_true(self):
        r = has_frobenius_algebra_structure(_space("a_model"))
        assert r.is_true

    def test_b_model_returns_true(self):
        r = has_frobenius_algebra_structure(_space("b_model"))
        assert r.is_true

    def test_bd_algebra_returns_false(self):
        r = has_frobenius_algebra_structure(_space("bd_algebra"))
        assert r.is_false

    def test_multiplication_comultiplication_returns_true(self):
        r = has_frobenius_algebra_structure(_space("multiplication_comultiplication"))
        assert r.is_true


# ---------------------------------------------------------------------------
# TestAdmitsHigherCategoricalFormulation
# ---------------------------------------------------------------------------

class TestAdmitsHigherCategoricalFormulation:
    def test_cobordism_hypothesis_returns_true(self):
        r = admits_higher_categorical_formulation(_space("cobordism_hypothesis"))
        assert r.is_true

    def test_baez_dolan_returns_true(self):
        r = admits_higher_categorical_formulation(_space("baez_dolan"))
        assert r.is_true

    def test_lurie_classification_returns_true(self):
        r = admits_higher_categorical_formulation(_space("lurie_classification"))
        assert r.is_true

    def test_extended_tft_returns_true(self):
        r = admits_higher_categorical_formulation(_space("extended_tft"))
        assert r.is_true

    def test_fully_extended_returns_true(self):
        r = admits_higher_categorical_formulation(_space("fully_extended"))
        assert r.is_true

    def test_higher_categorical_returns_true(self):
        r = admits_higher_categorical_formulation(_space("higher_categorical"))
        assert r.is_true

    def test_factorization_algebra_returns_true(self):
        r = admits_higher_categorical_formulation(_space("factorization_algebra"))
        assert r.is_true

    def test_costello_gwilliam_returns_true(self):
        r = admits_higher_categorical_formulation(_space("costello_gwilliam"))
        assert r.is_true

    def test_bd_algebra_returns_true(self):
        r = admits_higher_categorical_formulation(_space("bd_algebra"))
        assert r.is_true

    def test_frobenius_alone_returns_false(self):
        r = admits_higher_categorical_formulation(_space("frobenius_algebra"))
        assert r.is_false

    def test_two_dim_tft_alone_returns_false(self):
        r = admits_higher_categorical_formulation(_space("two_dim_tft"))
        assert r.is_false

    def test_pants_decomposition_alone_returns_false(self):
        r = admits_higher_categorical_formulation(_space("pants_decomposition"))
        assert r.is_false

    def test_empty_returns_unknown(self):
        r = admits_higher_categorical_formulation("")
        assert r.is_unknown

    def test_random_text_returns_unknown(self):
        r = admits_higher_categorical_formulation("metric space topology")
        assert r.is_unknown

    def test_returns_result_instance(self):
        r = admits_higher_categorical_formulation("cobordism_hypothesis")
        assert isinstance(r, Result)

    def test_default_mode_symbolic(self):
        r = admits_higher_categorical_formulation("cobordism_hypothesis")
        assert r.mode == "symbolic"

    def test_custom_mode_mixed(self):
        r = admits_higher_categorical_formulation("cobordism_hypothesis", mode="mixed")
        assert r.mode == "mixed"

    def test_infinity_categorical_tft_returns_true(self):
        r = admits_higher_categorical_formulation(_space("infinity_categorical_tft"))
        assert r.is_true

    def test_o_n_action_returns_true(self):
        r = admits_higher_categorical_formulation(_space("o_n_action"))
        assert r.is_true

    def test_once_extended_returns_true(self):
        r = admits_higher_categorical_formulation(_space("once_extended"))
        assert r.is_true

    def test_frobenius_structure_alone_returns_false(self):
        r = admits_higher_categorical_formulation(_space("frobenius_structure"))
        assert r.is_false


# ---------------------------------------------------------------------------
# TestClassifyTft
# ---------------------------------------------------------------------------

class TestClassifyTft:
    def test_returns_dict(self):
        result = classify_tft("atiyah_segal")
        assert isinstance(result, dict)

    def test_has_four_keys(self):
        result = classify_tft("atiyah_segal")
        assert len(result) == 4

    def test_has_is_extended_tft_key(self):
        result = classify_tft("atiyah_segal")
        assert "is_extended_tft" in result

    def test_has_satisfies_atiyah_segal_axioms_key(self):
        result = classify_tft("atiyah_segal")
        assert "satisfies_atiyah_segal_axioms" in result

    def test_has_frobenius_algebra_structure_key(self):
        result = classify_tft("atiyah_segal")
        assert "has_frobenius_algebra_structure" in result

    def test_has_admits_higher_categorical_key(self):
        result = classify_tft("atiyah_segal")
        assert "admits_higher_categorical_formulation" in result

    def test_all_values_are_result(self):
        result = classify_tft("atiyah_segal")
        for v in result.values():
            assert isinstance(v, Result)

    def test_extended_tft_tag_extended_is_true(self):
        result = classify_tft("extended_tft")
        assert result["is_extended_tft"].is_true

    def test_atiyah_segal_tag_satisfies_axioms_true(self):
        result = classify_tft("atiyah_segal")
        assert result["satisfies_atiyah_segal_axioms"].is_true

    def test_frobenius_tag_frobenius_true(self):
        result = classify_tft("frobenius_algebra")
        assert result["has_frobenius_algebra_structure"].is_true

    def test_cobordism_hypothesis_higher_cat_true(self):
        result = classify_tft("cobordism_hypothesis")
        assert result["admits_higher_categorical_formulation"].is_true

    def test_empty_all_unknown_or_false(self):
        result = classify_tft("")
        assert result["is_extended_tft"].is_unknown
        assert result["satisfies_atiyah_segal_axioms"].is_unknown

    def test_default_mode_symbolic(self):
        result = classify_tft("extended_tft")
        for v in result.values():
            assert v.mode == "symbolic"

    def test_custom_mode_propagated(self):
        result = classify_tft("extended_tft", mode="theorem")
        for v in result.values():
            assert v.mode == "theorem"

    def test_chern_simons_satisfies_axioms(self):
        result = classify_tft("chern_simons")
        assert result["satisfies_atiyah_segal_axioms"].is_true

    def test_factorization_extended_true(self):
        result = classify_tft("factorization_algebra")
        assert result["is_extended_tft"].is_true

    def test_donaldson_satisfies_axioms(self):
        result = classify_tft("donaldson_theory")
        assert result["satisfies_atiyah_segal_axioms"].is_true

    def test_frobenius_not_higher_cat(self):
        result = classify_tft("frobenius_algebra")
        assert result["admits_higher_categorical_formulation"].is_false

    def test_topological_string_has_frobenius(self):
        result = classify_tft("topological_string")
        assert result["has_frobenius_algebra_structure"].is_true

    def test_cobordism_hypothesis_extended_true(self):
        result = classify_tft("cobordism_hypothesis")
        assert result["is_extended_tft"].is_true


# ---------------------------------------------------------------------------
# TestTftProfileReport
# ---------------------------------------------------------------------------

class TestTftProfileReport:
    @pytest.fixture
    def profiles(self):
        return {p.key: p for p in get_named_tft_profiles()}

    def test_report_returns_dict(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert isinstance(report, dict)

    def test_report_has_key_field(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "key" in report

    def test_report_has_display_name(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "display_name" in report

    def test_report_has_tft_type(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "tft_type" in report

    def test_report_has_dimension(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "dimension" in report

    def test_report_has_is_extended(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "is_extended" in report

    def test_report_has_has_frobenius_structure(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "has_frobenius_structure" in report

    def test_report_has_is_oriented(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "is_oriented" in report

    def test_report_has_has_anomaly(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "has_anomaly" in report

    def test_report_has_admits_higher_cat(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "admits_higher_categorical_formulation" in report

    def test_report_has_analysis(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert "analysis" in report

    def test_report_analysis_is_dict(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert isinstance(report["analysis"], dict)

    def test_report_analysis_has_four_keys(self, profiles):
        report = tft_profile_report(profiles["atiyah_segal_tft"])
        assert len(report["analysis"]) == 4  # type: ignore[arg-type]

    def test_report_key_matches_profile(self, profiles):
        p = profiles["cobordism_hypothesis_tft"]
        report = tft_profile_report(p)
        assert report["key"] == "cobordism_hypothesis_tft"

    def test_report_dimension_correct(self, profiles):
        p = profiles["donaldson_tft"]
        report = tft_profile_report(p)
        assert report["dimension"] == 4

    def test_report_is_extended_correct(self, profiles):
        p = profiles["factorization_algebra_tft"]
        report = tft_profile_report(p)
        assert report["is_extended"] is True

    def test_report_has_anomaly_for_chern_simons(self, profiles):
        p = profiles["chern_simons_tft"]
        report = tft_profile_report(p)
        assert report["has_anomaly"] is True

    def test_report_analysis_values_are_result(self, profiles):
        p = profiles["atiyah_segal_tft"]
        report = tft_profile_report(p)
        for v in report["analysis"].values():  # type: ignore[union-attr]
            assert isinstance(v, Result)

    def test_all_profiles_generate_valid_report(self, profiles):
        for key, p in profiles.items():
            report = tft_profile_report(p)
            assert report["key"] == key
            assert isinstance(report["analysis"], dict)

    def test_report_tft_type_correct_for_topological_string(self, profiles):
        p = profiles["topological_string_tft"]
        report = tft_profile_report(p)
        assert report["tft_type"] == "topological_string"

    def test_report_default_mode_symbolic(self, profiles):
        p = profiles["atiyah_segal_tft"]
        report = tft_profile_report(p)
        for v in report["analysis"].values():  # type: ignore[union-attr]
            assert v.mode == "symbolic"  # type: ignore[union-attr]
