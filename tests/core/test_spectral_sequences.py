"""Tests for pytop.spectral_sequences."""

from __future__ import annotations

import pytest

from pytop.spectral_sequences import (
    ADAMS_SS_TAGS,
    ATIYAH_HIRZEBRUCH_SS_TAGS,
    CONVERGENCE_TAGS,
    DIFFERENTIAL_TAGS,
    EILENBERG_MOORE_SS_TAGS,
    FILTRATION_TAGS,
    LERAY_SS_TAGS,
    SERRE_SS_TAGS,
    SpectralSequenceProfile,
    classify_spectral_sequence,
    converges_strongly,
    get_named_spectral_sequence_profiles,
    has_collapse_at_e2,
    is_first_quadrant_spectral_sequence,
    is_multiplicative_spectral_sequence,
    spectral_sequence_chapter_index,
    spectral_sequence_layer_summary,
    spectral_sequence_profile,
    spectral_sequence_type_index,
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
# TestTagConstants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_serre_ss_tags_nonempty(self):
        assert len(SERRE_SS_TAGS) >= 4

    def test_adams_ss_tags_nonempty(self):
        assert len(ADAMS_SS_TAGS) >= 4

    def test_eilenberg_moore_ss_tags_nonempty(self):
        assert len(EILENBERG_MOORE_SS_TAGS) >= 4

    def test_atiyah_hirzebruch_ss_tags_nonempty(self):
        assert len(ATIYAH_HIRZEBRUCH_SS_TAGS) >= 4

    def test_leray_ss_tags_nonempty(self):
        assert len(LERAY_SS_TAGS) >= 4

    def test_convergence_tags_nonempty(self):
        assert len(CONVERGENCE_TAGS) >= 4

    def test_differential_tags_nonempty(self):
        assert len(DIFFERENTIAL_TAGS) >= 4

    def test_filtration_tags_nonempty(self):
        assert len(FILTRATION_TAGS) >= 4

    # serre
    def test_serre_spectral_sequence_in_serre_tags(self):
        assert "serre_spectral_sequence" in SERRE_SS_TAGS

    def test_serre_ss_in_serre_tags(self):
        assert "serre_ss" in SERRE_SS_TAGS

    def test_transgression_in_serre_tags(self):
        assert "transgression" in SERRE_SS_TAGS

    def test_gysin_sequence_in_serre_tags(self):
        assert "gysin_sequence" in SERRE_SS_TAGS

    # adams
    def test_adams_spectral_sequence_in_adams_tags(self):
        assert "adams_spectral_sequence" in ADAMS_SS_TAGS

    def test_adams_ss_in_adams_tags(self):
        assert "adams_ss" in ADAMS_SS_TAGS

    def test_steenrod_algebra_in_adams_tags(self):
        assert "steenrod_algebra" in ADAMS_SS_TAGS

    def test_hopf_invariant_in_adams_tags(self):
        assert "hopf_invariant" in ADAMS_SS_TAGS

    # eilenberg-moore
    def test_eilenberg_moore_ss_in_em_tags(self):
        assert "eilenberg_moore_ss" in EILENBERG_MOORE_SS_TAGS

    def test_tor_functor_ss_in_em_tags(self):
        assert "tor_functor_ss" in EILENBERG_MOORE_SS_TAGS

    def test_loop_space_ss_in_em_tags(self):
        assert "loop_space_ss" in EILENBERG_MOORE_SS_TAGS

    # atiyah-hirzebruch
    def test_ahss_in_atiyah_hirzebruch_tags(self):
        assert "ahss" in ATIYAH_HIRZEBRUCH_SS_TAGS

    def test_k_theory_ss_in_atiyah_hirzebruch_tags(self):
        assert "k_theory_ss" in ATIYAH_HIRZEBRUCH_SS_TAGS

    def test_atiyah_hirzebruch_ss_in_tags(self):
        assert "atiyah_hirzebruch_ss" in ATIYAH_HIRZEBRUCH_SS_TAGS

    # leray
    def test_leray_hirsch_in_leray_tags(self):
        assert "leray_hirsch" in LERAY_SS_TAGS

    def test_grothendieck_ss_in_leray_tags(self):
        assert "grothendieck_ss" in LERAY_SS_TAGS

    # convergence
    def test_strong_convergence_in_convergence_tags(self):
        assert "strong_convergence" in CONVERGENCE_TAGS

    def test_first_quadrant_ss_in_convergence_tags(self):
        assert "first_quadrant_ss" in CONVERGENCE_TAGS

    def test_e_infinity_page_in_convergence_tags(self):
        assert "e_infinity_page" in CONVERGENCE_TAGS

    # differentials
    def test_differential_d_r_in_differential_tags(self):
        assert "differential_d_r" in DIFFERENTIAL_TAGS

    def test_d2_differential_in_differential_tags(self):
        assert "d2_differential" in DIFFERENTIAL_TAGS

    # filtrations
    def test_filtration_in_filtration_tags(self):
        assert "filtration" in FILTRATION_TAGS

    def test_bockstein_ss_in_filtration_tags(self):
        assert "bockstein_ss" in FILTRATION_TAGS

    def test_all_tag_constants_are_frozensets(self):
        for tagset in [
            SERRE_SS_TAGS, ADAMS_SS_TAGS, EILENBERG_MOORE_SS_TAGS,
            ATIYAH_HIRZEBRUCH_SS_TAGS, LERAY_SS_TAGS,
            CONVERGENCE_TAGS, DIFFERENTIAL_TAGS, FILTRATION_TAGS,
        ]:
            assert isinstance(tagset, frozenset)

    def test_all_tags_contain_strings_only(self):
        for tagset in [SERRE_SS_TAGS, ADAMS_SS_TAGS, CONVERGENCE_TAGS]:
            for tag in tagset:
                assert isinstance(tag, str)

    def test_serre_and_adams_disjoint(self):
        assert len(SERRE_SS_TAGS & ADAMS_SS_TAGS) == 0

    def test_atiyah_hirzebruch_and_leray_disjoint(self):
        assert len(ATIYAH_HIRZEBRUCH_SS_TAGS & LERAY_SS_TAGS) == 0


# ---------------------------------------------------------------------------
# TestNamedSpectralSequenceProfiles
# ---------------------------------------------------------------------------

class TestNamedSpectralSequenceProfiles:
    def setup_method(self):
        self.profiles = get_named_spectral_sequence_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_six_profiles(self):
        assert len(self.profiles) >= 6

    def test_exactly_eight_profiles(self):
        assert len(self.profiles) == 8

    def test_all_are_spectral_sequence_profile_instances(self):
        for p in self.profiles:
            assert isinstance(p, SpectralSequenceProfile)

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
            assert isinstance(p.focus, str) and len(p.focus) >= 300

    def test_all_chapter_targets_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.chapter_targets, tuple) and len(p.chapter_targets) >= 1

    def test_all_chapter_targets_contain_30_42_58(self):
        for p in self.profiles:
            assert "30" in p.chapter_targets
            assert "42" in p.chapter_targets
            assert "58" in p.chapter_targets

    def test_serre_fibration_ss_exists(self):
        assert any(p.key == "serre_fibration_ss" for p in self.profiles)

    def test_adams_ss_exists(self):
        assert any(p.key == "adams_ss_stable_homotopy" for p in self.profiles)

    def test_eilenberg_moore_ss_exists(self):
        assert any(p.key == "eilenberg_moore_ss" for p in self.profiles)

    def test_atiyah_hirzebruch_ss_exists(self):
        assert any(p.key == "atiyah_hirzebruch_ss" for p in self.profiles)

    def test_leray_hirsch_exists(self):
        assert any(p.key == "leray_hirsch_theorem" for p in self.profiles)

    def test_lhs_group_extension_exists(self):
        assert any(p.key == "lhs_group_extension" for p in self.profiles)

    def test_bockstein_ss_exists(self):
        assert any(p.key == "bockstein_ss" for p in self.profiles)

    def test_grothendieck_ss_exists(self):
        assert any(p.key == "grothendieck_ss" for p in self.profiles)

    def test_serre_fibration_fields(self):
        p = next(x for x in self.profiles if x.key == "serre_fibration_ss")
        assert p.sequence_type == "serre"
        assert p.is_multiplicative is True
        assert p.is_first_quadrant is True
        assert p.collapses_at_e2 is False
        assert p.is_conditionally_convergent is False
        assert p.converges_to == "H*(total_space)"

    def test_adams_ss_fields(self):
        p = next(x for x in self.profiles if x.key == "adams_ss_stable_homotopy")
        assert p.sequence_type == "adams"
        assert p.is_conditionally_convergent is True
        assert p.collapses_at_e2 is False

    def test_leray_hirsch_collapses_at_e2(self):
        p = next(x for x in self.profiles if x.key == "leray_hirsch_theorem")
        assert p.collapses_at_e2 is True
        assert p.is_conditionally_convergent is False

    def test_bockstein_not_multiplicative(self):
        p = next(x for x in self.profiles if x.key == "bockstein_ss")
        assert p.is_multiplicative is False
        assert p.collapses_at_e2 is True

    def test_eilenberg_moore_not_first_quadrant(self):
        p = next(x for x in self.profiles if x.key == "eilenberg_moore_ss")
        assert p.is_first_quadrant is False
        assert p.is_conditionally_convergent is True

    def test_profiles_are_frozen(self):
        p = self.profiles[0]
        with pytest.raises((AttributeError, TypeError)):
            p.key = "modified"  # type: ignore[misc]

    def test_sequence_types_valid(self):
        valid = {"serre", "adams", "eilenberg_moore", "atiyah_hirzebruch",
                 "leray", "lyndon_hochschild_serre", "bockstein", "mayer_vietoris"}
        for p in self.profiles:
            assert p.sequence_type in valid


# ---------------------------------------------------------------------------
# TestSummaryFunctions
# ---------------------------------------------------------------------------

class TestSummaryFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(spectral_sequence_layer_summary(), dict)

    def test_layer_summary_positive_counts(self):
        for v in spectral_sequence_layer_summary().values():
            assert v > 0

    def test_layer_summary_total_matches_profiles(self):
        assert sum(spectral_sequence_layer_summary().values()) == len(get_named_spectral_sequence_profiles())

    def test_chapter_index_returns_dict(self):
        assert isinstance(spectral_sequence_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in spectral_sequence_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_keys_sorted(self):
        keys = list(spectral_sequence_chapter_index().keys())
        assert keys == sorted(keys)

    def test_chapter_index_contains_chapter_30(self):
        assert "30" in spectral_sequence_chapter_index()

    def test_chapter_index_contains_chapter_42(self):
        assert "42" in spectral_sequence_chapter_index()

    def test_chapter_index_contains_chapter_58(self):
        assert "58" in spectral_sequence_chapter_index()

    def test_type_index_returns_dict(self):
        assert isinstance(spectral_sequence_type_index(), dict)

    def test_type_index_values_are_tuples(self):
        for v in spectral_sequence_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_keys_sorted(self):
        keys = list(spectral_sequence_type_index().keys())
        assert keys == sorted(keys)

    def test_type_index_contains_serre(self):
        assert "serre" in spectral_sequence_type_index()

    def test_type_index_contains_adams(self):
        assert "adams" in spectral_sequence_type_index()

    def test_type_index_total_matches_profiles(self):
        assert sum(len(v) for v in spectral_sequence_type_index().values()) == len(
            get_named_spectral_sequence_profiles()
        )


# ---------------------------------------------------------------------------
# TestIsMultiplicativeSpectralSequence
# ---------------------------------------------------------------------------

class TestIsMultiplicativeSpectralSequence:
    def test_serre_spectral_sequence_tag(self):
        s = _space("serre_spectral_sequence")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_serre_ss_tag(self):
        s = _space("serre_ss")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_gysin_sequence_tag(self):
        s = _space("gysin_sequence")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_adams_spectral_sequence_tag(self):
        s = _space("adams_spectral_sequence")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_adams_ss_tag(self):
        s = _space("adams_ss")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_steenrod_algebra_tag(self):
        s = _space("steenrod_algebra")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_ahss_tag(self):
        s = _space("ahss")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_k_theory_ss_tag(self):
        s = _space("k_theory_ss")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_leray_hirsch_tag(self):
        s = _space("leray_hirsch")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_grothendieck_ss_tag(self):
        s = _space("grothendieck_ss")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_multiplicative_ss_tag(self):
        s = _space("multiplicative_ss")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_transgression_tag(self):
        s = _space("transgression")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_bockstein_ss_tag_false(self):
        s = _space("bockstein_ss")
        assert is_multiplicative_spectral_sequence(s).is_false

    def test_non_multiplicative_ss_tag_false(self):
        s = _space("non_multiplicative_ss")
        assert is_multiplicative_spectral_sequence(s).is_false

    def test_not_multiplicative_ss_tag_false(self):
        s = _space("not_multiplicative_ss")
        assert is_multiplicative_spectral_sequence(s).is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = is_multiplicative_spectral_sequence(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("compact_manifold")
        r = is_multiplicative_spectral_sequence(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("serre_ss")
        r = is_multiplicative_spectral_sequence(s)
        assert len(r.justification) >= 1

    def test_result_metadata_has_criterion(self):
        s = _space("adams_ss")
        r = is_multiplicative_spectral_sequence(s)
        assert "criterion" in r.metadata

    def test_edge_homomorphism_tag(self):
        s = _space("edge_homomorphism")
        assert is_multiplicative_spectral_sequence(s).is_true

    def test_path_space_fibration_tag(self):
        s = _space("path_space_fibration")
        assert is_multiplicative_spectral_sequence(s).is_true


# ---------------------------------------------------------------------------
# TestConvergesStrongly
# ---------------------------------------------------------------------------

class TestConvergesStrongly:
    def test_strong_convergence_tag(self):
        s = _space("strong_convergence")
        assert converges_strongly(s).is_true

    def test_first_quadrant_ss_tag(self):
        s = _space("first_quadrant_ss")
        assert converges_strongly(s).is_true

    def test_serre_spectral_sequence_tag(self):
        s = _space("serre_spectral_sequence")
        assert converges_strongly(s).is_true

    def test_serre_fibration_tag(self):
        s = _space("serre_fibration")
        assert converges_strongly(s).is_true

    def test_gysin_sequence_tag(self):
        s = _space("gysin_sequence")
        assert converges_strongly(s).is_true

    def test_ahss_tag(self):
        s = _space("ahss")
        assert converges_strongly(s).is_true

    def test_atiyah_hirzebruch_ss_tag(self):
        s = _space("atiyah_hirzebruch_ss")
        assert converges_strongly(s).is_true

    def test_leray_hirsch_tag(self):
        s = _space("leray_hirsch")
        assert converges_strongly(s).is_true

    def test_leray_ss_tag(self):
        s = _space("leray_ss")
        assert converges_strongly(s).is_true

    def test_lyndon_hochschild_serre_tag(self):
        s = _space("lyndon_hochschild_serre")
        assert converges_strongly(s).is_true

    def test_lhs_ss_tag(self):
        s = _space("lhs_ss")
        assert converges_strongly(s).is_true

    def test_grothendieck_ss_tag(self):
        s = _space("grothendieck_ss")
        assert converges_strongly(s).is_true

    def test_adams_ss_not_strongly_convergent(self):
        s = _space("adams_ss")
        assert converges_strongly(s).is_false

    def test_adams_spectral_sequence_not_strongly(self):
        s = _space("adams_spectral_sequence")
        assert converges_strongly(s).is_false

    def test_eilenberg_moore_ss_not_strongly(self):
        s = _space("eilenberg_moore_ss")
        assert converges_strongly(s).is_false

    def test_conditional_convergence_tag_false(self):
        s = _space("conditional_convergence")
        assert converges_strongly(s).is_false

    def test_conditionally_convergent_tag_false(self):
        s = _space("conditionally_convergent")
        assert converges_strongly(s).is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = converges_strongly(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("smooth_manifold")
        r = converges_strongly(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("serre_ss")
        r = converges_strongly(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("strong_convergence")
        r = converges_strongly(s)
        assert "criterion" in r.metadata

    def test_loop_space_ss_not_strongly(self):
        s = _space("loop_space_ss")
        assert converges_strongly(s).is_false


# ---------------------------------------------------------------------------
# TestHasCollapseAtE2
# ---------------------------------------------------------------------------

class TestHasCollapseAtE2:
    def test_collapses_at_e2_tag(self):
        s = _space("collapses_at_e2")
        assert has_collapse_at_e2(s).is_true

    def test_e2_degeneration_tag(self):
        s = _space("e2_degeneration")
        assert has_collapse_at_e2(s).is_true

    def test_e2_collapse_tag(self):
        s = _space("e2_collapse")
        assert has_collapse_at_e2(s).is_true

    def test_e2_page_collapses_tag(self):
        s = _space("e2_page_collapses")
        assert has_collapse_at_e2(s).is_true

    def test_ss_degenerates_at_e2_tag(self):
        s = _space("ss_degenerates_at_e2")
        assert has_collapse_at_e2(s).is_true

    def test_leray_hirsch_tag(self):
        s = _space("leray_hirsch")
        assert has_collapse_at_e2(s).is_true

    def test_trivial_fibration_tag(self):
        s = _space("trivial_fibration")
        assert has_collapse_at_e2(s).is_true

    def test_product_fibration_tag(self):
        s = _space("product_fibration")
        assert has_collapse_at_e2(s).is_true

    def test_bockstein_ss_collapses(self):
        s = _space("bockstein_ss")
        assert has_collapse_at_e2(s).is_true

    def test_leray_ss_tag(self):
        s = _space("leray_ss")
        assert has_collapse_at_e2(s).is_true

    def test_d3_differential_no_collapse(self):
        s = _space("d3_differential")
        assert has_collapse_at_e2(s).is_false

    def test_non_trivial_differential_no_collapse(self):
        s = _space("non_trivial_differential")
        assert has_collapse_at_e2(s).is_false

    def test_does_not_collapse_tag(self):
        s = _space("does_not_collapse")
        assert has_collapse_at_e2(s).is_false

    def test_adams_ss_no_collapse(self):
        s = _space("adams_ss")
        assert has_collapse_at_e2(s).is_false

    def test_adams_spectral_sequence_no_collapse(self):
        s = _space("adams_spectral_sequence")
        assert has_collapse_at_e2(s).is_false

    def test_eilenberg_moore_no_collapse(self):
        s = _space("eilenberg_moore_ss")
        assert has_collapse_at_e2(s).is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = has_collapse_at_e2(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("tychonoff_theorem")
        r = has_collapse_at_e2(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("leray_hirsch")
        r = has_collapse_at_e2(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("e2_collapse")
        r = has_collapse_at_e2(s)
        assert "criterion" in r.metadata

    def test_grothendieck_ss_tag(self):
        s = _space("grothendieck_ss")
        assert has_collapse_at_e2(s).is_true


# ---------------------------------------------------------------------------
# TestIsFirstQuadrantSpectralSequence
# ---------------------------------------------------------------------------

class TestIsFirstQuadrantSpectralSequence:
    def test_first_quadrant_ss_tag(self):
        s = _space("first_quadrant_ss")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_strong_convergence_tag(self):
        s = _space("strong_convergence")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_serre_spectral_sequence_tag(self):
        s = _space("serre_spectral_sequence")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_serre_ss_tag(self):
        s = _space("serre_ss")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_serre_fibration_tag(self):
        s = _space("serre_fibration")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_atiyah_hirzebruch_ss_tag(self):
        s = _space("atiyah_hirzebruch_ss")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_ahss_tag(self):
        s = _space("ahss")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_k_theory_ss_tag(self):
        s = _space("k_theory_ss")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_lyndon_hochschild_serre_tag(self):
        s = _space("lyndon_hochschild_serre")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_lhs_ss_tag(self):
        s = _space("lhs_ss")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_grothendieck_ss_tag(self):
        s = _space("grothendieck_ss")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_leray_ss_tag(self):
        s = _space("leray_ss")
        assert is_first_quadrant_spectral_sequence(s).is_true

    def test_adams_ss_not_first_quadrant(self):
        s = _space("adams_ss")
        assert is_first_quadrant_spectral_sequence(s).is_false

    def test_adams_spectral_sequence_not_first_quadrant(self):
        s = _space("adams_spectral_sequence")
        assert is_first_quadrant_spectral_sequence(s).is_false

    def test_eilenberg_moore_ss_not_first_quadrant(self):
        s = _space("eilenberg_moore_ss")
        assert is_first_quadrant_spectral_sequence(s).is_false

    def test_tor_functor_ss_not_first_quadrant(self):
        s = _space("tor_functor_ss")
        assert is_first_quadrant_spectral_sequence(s).is_false

    def test_loop_space_ss_not_first_quadrant(self):
        s = _space("loop_space_ss")
        assert is_first_quadrant_spectral_sequence(s).is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = is_first_quadrant_spectral_sequence(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("borsuk_ulam")
        r = is_first_quadrant_spectral_sequence(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("serre_ss")
        r = is_first_quadrant_spectral_sequence(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("first_quadrant_ss")
        r = is_first_quadrant_spectral_sequence(s)
        assert "criterion" in r.metadata

    def test_inflation_restriction_tag(self):
        s = _space("inflation_restriction")
        assert is_first_quadrant_spectral_sequence(s).is_true


# ---------------------------------------------------------------------------
# TestClassifySpectralSequence
# ---------------------------------------------------------------------------

class TestClassifySpectralSequence:
    def test_returns_dict(self):
        assert isinstance(classify_spectral_sequence(_space()), dict)

    def test_has_four_keys(self):
        assert len(classify_spectral_sequence(_space())) == 4

    def test_has_is_multiplicative_key(self):
        assert "is_multiplicative_spectral_sequence" in classify_spectral_sequence(_space())

    def test_has_converges_strongly_key(self):
        assert "converges_strongly" in classify_spectral_sequence(_space())

    def test_has_collapse_at_e2_key(self):
        assert "has_collapse_at_e2" in classify_spectral_sequence(_space())

    def test_has_first_quadrant_key(self):
        assert "is_first_quadrant_spectral_sequence" in classify_spectral_sequence(_space())

    def test_serre_ss_full_classification(self):
        s = _space("serre_ss", "first_quadrant_ss")
        r = classify_spectral_sequence(s)
        assert r["is_multiplicative_spectral_sequence"].is_true
        assert r["converges_strongly"].is_true
        assert r["is_first_quadrant_spectral_sequence"].is_true

    def test_adams_ss_full_classification(self):
        s = _space("adams_ss")
        r = classify_spectral_sequence(s)
        assert r["converges_strongly"].is_false
        assert r["has_collapse_at_e2"].is_false
        assert r["is_first_quadrant_spectral_sequence"].is_false

    def test_empty_space_all_unknown(self):
        s = _space()
        for r in classify_spectral_sequence(s).values():
            assert not r.is_true and not r.is_false

    def test_leray_hirsch_collapses_and_converges(self):
        s = _space("leray_hirsch")
        r = classify_spectral_sequence(s)
        assert r["has_collapse_at_e2"].is_true
        assert r["converges_strongly"].is_true


# ---------------------------------------------------------------------------
# TestSpectralSequenceProfile
# ---------------------------------------------------------------------------

class TestSpectralSequenceProfile:
    def test_returns_dict(self):
        assert isinstance(spectral_sequence_profile(_space()), dict)

    def test_has_space_key(self):
        assert "space" in spectral_sequence_profile(_space())

    def test_has_tags_key(self):
        assert "tags" in spectral_sequence_profile(_space("serre_ss"))

    def test_has_representation_key(self):
        assert "representation" in spectral_sequence_profile(_space())

    def test_has_classification_key(self):
        assert "classification" in spectral_sequence_profile(_space())

    def test_has_summary_key(self):
        assert "summary" in spectral_sequence_profile(_space())

    def test_tags_is_sorted_list(self):
        s = _space("serre_ss", "ahss")
        result = spectral_sequence_profile(s)
        tags = result["tags"]
        assert isinstance(tags, list) and tags == sorted(tags)

    def test_summary_has_four_entries(self):
        assert len(spectral_sequence_profile(_space())["summary"]) == 4

    def test_summary_values_are_strings(self):
        s = _space("serre_ss")
        for v in spectral_sequence_profile(s)["summary"].values():
            assert isinstance(v, str)

    def test_space_attribute_preserved(self):
        s = _space("adams_ss")
        result = spectral_sequence_profile(s)
        assert result["space"] is s
