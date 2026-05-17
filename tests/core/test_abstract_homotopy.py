"""Tests for pytop.abstract_homotopy."""

from __future__ import annotations

import pytest

from pytop.abstract_homotopy import (
    BOUSFIELD_LOCALIZATION_TAGS,
    COFIBRANT_FIBRANT_TAGS,
    HOMOTOPY_LIMIT_TAGS,
    INFINITY_CATEGORY_TAGS,
    MODEL_CATEGORY_TAGS,
    PROPER_MODEL_TAGS,
    QUILLEN_ADJUNCTION_TAGS,
    STABLE_HOMOTOPY_TAGS,
    AbstractHomotopyProfile,
    abstract_homotopy_chapter_index,
    abstract_homotopy_layer_summary,
    abstract_homotopy_profile,
    abstract_homotopy_type_index,
    admits_bousfield_localization,
    classify_abstract_homotopy,
    get_named_abstract_homotopy_profiles,
    has_homotopy_limits,
    is_proper_model_category,
    is_stable_model_category,
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
    def test_model_category_tags_nonempty(self):
        assert len(MODEL_CATEGORY_TAGS) >= 4

    def test_quillen_adjunction_tags_nonempty(self):
        assert len(QUILLEN_ADJUNCTION_TAGS) >= 4

    def test_homotopy_limit_tags_nonempty(self):
        assert len(HOMOTOPY_LIMIT_TAGS) >= 4

    def test_infinity_category_tags_nonempty(self):
        assert len(INFINITY_CATEGORY_TAGS) >= 4

    def test_stable_homotopy_tags_nonempty(self):
        assert len(STABLE_HOMOTOPY_TAGS) >= 4

    def test_bousfield_localization_tags_nonempty(self):
        assert len(BOUSFIELD_LOCALIZATION_TAGS) >= 4

    def test_cofibrant_fibrant_tags_nonempty(self):
        assert len(COFIBRANT_FIBRANT_TAGS) >= 4

    def test_proper_model_tags_nonempty(self):
        assert len(PROPER_MODEL_TAGS) >= 4

    def test_model_category_in_model_tags(self):
        assert "model_category" in MODEL_CATEGORY_TAGS

    def test_quillen_adjunction_in_quillen_tags(self):
        assert "quillen_adjunction" in QUILLEN_ADJUNCTION_TAGS

    def test_quillen_equivalence_in_quillen_tags(self):
        assert "quillen_equivalence" in QUILLEN_ADJUNCTION_TAGS

    def test_homotopy_pushout_in_limit_tags(self):
        assert "homotopy_pushout" in HOMOTOPY_LIMIT_TAGS

    def test_homotopy_pullback_in_limit_tags(self):
        assert "homotopy_pullback" in HOMOTOPY_LIMIT_TAGS

    def test_homotopy_limit_in_limit_tags(self):
        assert "homotopy_limit" in HOMOTOPY_LIMIT_TAGS

    def test_quasi_category_in_infinity_tags(self):
        assert "quasi_category" in INFINITY_CATEGORY_TAGS

    def test_kan_complex_in_infinity_tags(self):
        assert "kan_complex" in INFINITY_CATEGORY_TAGS

    def test_spectra_in_stable_tags(self):
        assert "spectra" in STABLE_HOMOTOPY_TAGS

    def test_stable_model_category_in_stable_tags(self):
        assert "stable_model_category" in STABLE_HOMOTOPY_TAGS

    def test_suspension_equivalence_in_stable_tags(self):
        assert "suspension_equivalence" in STABLE_HOMOTOPY_TAGS

    def test_bousfield_localization_in_bousfield_tags(self):
        assert "bousfield_localization" in BOUSFIELD_LOCALIZATION_TAGS

    def test_left_bousfield_in_bousfield_tags(self):
        assert "left_bousfield_localization" in BOUSFIELD_LOCALIZATION_TAGS

    def test_cofibrant_replacement_in_cofibrant_tags(self):
        assert "cofibrant_replacement" in COFIBRANT_FIBRANT_TAGS

    def test_fibrant_replacement_in_cofibrant_tags(self):
        assert "fibrant_replacement" in COFIBRANT_FIBRANT_TAGS

    def test_left_proper_in_proper_tags(self):
        assert "left_proper" in PROPER_MODEL_TAGS

    def test_right_proper_in_proper_tags(self):
        assert "right_proper" in PROPER_MODEL_TAGS

    def test_all_tag_sets_contain_strings(self):
        for tag_set in [
            MODEL_CATEGORY_TAGS, QUILLEN_ADJUNCTION_TAGS, HOMOTOPY_LIMIT_TAGS,
            INFINITY_CATEGORY_TAGS, STABLE_HOMOTOPY_TAGS, BOUSFIELD_LOCALIZATION_TAGS,
            COFIBRANT_FIBRANT_TAGS, PROPER_MODEL_TAGS,
        ]:
            assert all(isinstance(t, str) for t in tag_set)

    def test_stable_and_infinity_disjoint(self):
        assert STABLE_HOMOTOPY_TAGS.isdisjoint(INFINITY_CATEGORY_TAGS)

    def test_model_and_infinity_disjoint(self):
        assert MODEL_CATEGORY_TAGS.isdisjoint(INFINITY_CATEGORY_TAGS)


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_abstract_homotopy_profiles(), tuple)

    def test_at_least_six_profiles(self):
        assert len(get_named_abstract_homotopy_profiles()) >= 6

    def test_exactly_seven_profiles(self):
        assert len(get_named_abstract_homotopy_profiles()) == 7

    def test_all_abstract_homotopy_profile_instances(self):
        for p in get_named_abstract_homotopy_profiles():
            assert isinstance(p, AbstractHomotopyProfile)

    def test_keys_unique(self):
        keys = [p.key for p in get_named_abstract_homotopy_profiles()]
        assert len(keys) == len(set(keys))

    def test_display_names_nonempty(self):
        for p in get_named_abstract_homotopy_profiles():
            assert p.display_name.strip()

    def test_focus_nonempty(self):
        for p in get_named_abstract_homotopy_profiles():
            assert p.focus.strip()

    def test_chapter_targets_nonempty(self):
        for p in get_named_abstract_homotopy_profiles():
            assert len(p.chapter_targets) >= 1

    def test_presentation_layers_known(self):
        known = {"main_text", "selected_block", "appendix"}
        for p in get_named_abstract_homotopy_profiles():
            assert p.presentation_layer in known

    def test_category_types_are_strings(self):
        for p in get_named_abstract_homotopy_profiles():
            assert isinstance(p.category_type, str)

    def test_is_proper_bool(self):
        for p in get_named_abstract_homotopy_profiles():
            assert isinstance(p.is_proper, bool)

    def test_is_stable_bool(self):
        for p in get_named_abstract_homotopy_profiles():
            assert isinstance(p.is_stable, bool)

    def test_admits_localization_bool(self):
        for p in get_named_abstract_homotopy_profiles():
            assert isinstance(p.admits_localization, bool)

    # topological_spaces_quillen
    def test_top_quillen_present(self):
        assert "topological_spaces_quillen" in {p.key for p in get_named_abstract_homotopy_profiles()}

    def test_top_quillen_is_proper(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "topological_spaces_quillen")
        assert p.is_proper is True

    def test_top_quillen_not_stable(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "topological_spaces_quillen")
        assert p.is_stable is False

    def test_top_quillen_admits_localization(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "topological_spaces_quillen")
        assert p.admits_localization is True

    def test_top_quillen_category_type(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "topological_spaces_quillen")
        assert p.category_type == "model_category"

    # simplicial_sets_kan_quillen
    def test_sset_present(self):
        assert "simplicial_sets_kan_quillen" in {p.key for p in get_named_abstract_homotopy_profiles()}

    def test_sset_is_proper(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "simplicial_sets_kan_quillen")
        assert p.is_proper is True

    def test_sset_not_stable(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "simplicial_sets_kan_quillen")
        assert p.is_stable is False

    def test_sset_admits_localization(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "simplicial_sets_kan_quillen")
        assert p.admits_localization is True

    # chain_complexes_projective
    def test_chain_complexes_present(self):
        assert "chain_complexes_projective" in {p.key for p in get_named_abstract_homotopy_profiles()}

    def test_chain_complexes_is_stable(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "chain_complexes_projective")
        assert p.is_stable is True

    def test_chain_complexes_is_proper(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "chain_complexes_projective")
        assert p.is_proper is True

    def test_chain_complexes_admits_localization(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "chain_complexes_projective")
        assert p.admits_localization is True

    # quasi_categories_joyal
    def test_quasi_categories_present(self):
        assert "quasi_categories_joyal" in {p.key for p in get_named_abstract_homotopy_profiles()}

    def test_quasi_categories_not_proper(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "quasi_categories_joyal")
        assert p.is_proper is False

    def test_quasi_categories_not_stable(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "quasi_categories_joyal")
        assert p.is_stable is False

    def test_quasi_categories_type(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "quasi_categories_joyal")
        assert p.category_type == "infinity_category"

    # spectra_stable_model
    def test_spectra_present(self):
        assert "spectra_stable_model" in {p.key for p in get_named_abstract_homotopy_profiles()}

    def test_spectra_is_stable(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "spectra_stable_model")
        assert p.is_stable is True

    def test_spectra_is_proper(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "spectra_stable_model")
        assert p.is_proper is True

    def test_spectra_category_type(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "spectra_stable_model")
        assert p.category_type == "stable_model_category"

    # homotopy_pushout_cofibrant
    def test_homotopy_pushout_present(self):
        assert "homotopy_pushout_cofibrant" in {p.key for p in get_named_abstract_homotopy_profiles()}

    def test_homotopy_pushout_not_stable(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "homotopy_pushout_cofibrant")
        assert p.is_stable is False

    def test_homotopy_pushout_not_localization(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "homotopy_pushout_cofibrant")
        assert p.admits_localization is False

    # left_bousfield_localization
    def test_bousfield_present(self):
        assert "left_bousfield_localization" in {p.key for p in get_named_abstract_homotopy_profiles()}

    def test_bousfield_is_proper(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "left_bousfield_localization")
        assert p.is_proper is True

    def test_bousfield_admits_localization(self):
        p = next(p for p in get_named_abstract_homotopy_profiles()
                 if p.key == "left_bousfield_localization")
        assert p.admits_localization is True


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_is_dict(self):
        assert isinstance(abstract_homotopy_layer_summary(), dict)

    def test_layer_summary_has_main_text(self):
        assert "main_text" in abstract_homotopy_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in abstract_homotopy_layer_summary()

    def test_layer_summary_total(self):
        profiles = get_named_abstract_homotopy_profiles()
        assert sum(abstract_homotopy_layer_summary().values()) == len(profiles)

    def test_chapter_index_is_dict(self):
        assert isinstance(abstract_homotopy_chapter_index(), dict)

    def test_chapter_index_sorted(self):
        ch = abstract_homotopy_chapter_index()
        assert list(ch.keys()) == sorted(ch.keys())

    def test_chapter_index_tuples(self):
        for v in abstract_homotopy_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_nonempty_values(self):
        for v in abstract_homotopy_chapter_index().values():
            assert len(v) >= 1

    def test_type_index_is_dict(self):
        assert isinstance(abstract_homotopy_type_index(), dict)

    def test_type_index_has_model_category(self):
        assert "model_category" in abstract_homotopy_type_index()

    def test_type_index_has_stable_model_category(self):
        assert "stable_model_category" in abstract_homotopy_type_index()

    def test_type_index_has_infinity_category(self):
        assert "infinity_category" in abstract_homotopy_type_index()

    def test_type_index_tuples(self):
        for v in abstract_homotopy_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_total(self):
        total = sum(len(v) for v in abstract_homotopy_type_index().values())
        assert total == len(get_named_abstract_homotopy_profiles())


# ---------------------------------------------------------------------------
# is_proper_model_category
# ---------------------------------------------------------------------------

class TestIsProperModelCategory:
    def test_proper_model_tag_true(self):
        assert is_proper_model_category(_space("proper_model")).is_true

    def test_left_plus_right_proper_true(self):
        assert is_proper_model_category(_space("left_proper", "right_proper")).is_true

    def test_topological_spaces_true(self):
        assert is_proper_model_category(_space("topological_spaces")).is_true

    def test_simplicial_sets_true(self):
        assert is_proper_model_category(_space("simplicial_sets")).is_true

    def test_kan_quillen_true(self):
        assert is_proper_model_category(_space("kan_quillen")).is_true

    def test_chain_complexes_true(self):
        assert is_proper_model_category(_space("chain_complexes")).is_true

    def test_projective_model_true(self):
        assert is_proper_model_category(_space("projective_model")).is_true

    def test_quillen_top_true(self):
        assert is_proper_model_category(_space("quillen_top")).is_true

    def test_bousfield_friedlander_true(self):
        assert is_proper_model_category(_space("bousfield_friedlander")).is_true

    def test_gluing_lemma_true(self):
        assert is_proper_model_category(_space("gluing_lemma")).is_true

    def test_left_proper_alone_true(self):
        assert is_proper_model_category(_space("left_proper")).is_true

    def test_pushout_weak_equivalence_true(self):
        assert is_proper_model_category(_space("pushout_weak_equivalence")).is_true

    def test_not_proper_false(self):
        assert is_proper_model_category(_space("not_proper")).is_false

    def test_not_left_proper_false(self):
        assert is_proper_model_category(_space("not_left_proper")).is_false

    def test_not_right_proper_false(self):
        assert is_proper_model_category(_space("not_right_proper")).is_false

    def test_joyal_not_right_proper_false(self):
        assert is_proper_model_category(_space("joyal_not_right_proper")).is_false

    def test_unknown_empty(self):
        r = is_proper_model_category(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert is_proper_model_category(_space("proper_model")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_proper_model_category(_space("not_proper")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert is_proper_model_category(_space()).mode == "symbolic"

    def test_criterion_explicit_proper(self):
        r = is_proper_model_category(_space("proper_model"))
        assert r.metadata.get("criterion") == "explicit_proper"

    def test_criterion_canonical_proper(self):
        r = is_proper_model_category(_space("topological_spaces"))
        assert r.metadata.get("criterion") == "canonical_proper"

    def test_criterion_proper_tag(self):
        r = is_proper_model_category(_space("left_proper"))
        assert r.metadata.get("criterion") == "proper_tag"

    def test_criterion_not_proper(self):
        r = is_proper_model_category(_space("not_proper"))
        assert r.metadata.get("criterion") == "not_proper"

    def test_injective_model_true(self):
        assert is_proper_model_category(_space("injective_model")).is_true

    def test_pullback_weak_equivalence_true(self):
        assert is_proper_model_category(_space("pullback_weak_equivalence")).is_true


# ---------------------------------------------------------------------------
# has_homotopy_limits
# ---------------------------------------------------------------------------

class TestHasHomotopyLimits:
    def test_homotopy_limit_tag_true(self):
        assert has_homotopy_limits(_space("homotopy_limit")).is_true

    def test_homotopy_colimit_true(self):
        assert has_homotopy_limits(_space("homotopy_colimit")).is_true

    def test_homotopy_pushout_true(self):
        assert has_homotopy_limits(_space("homotopy_pushout")).is_true

    def test_homotopy_pullback_true(self):
        assert has_homotopy_limits(_space("homotopy_pullback")).is_true

    def test_derived_pushout_true(self):
        assert has_homotopy_limits(_space("derived_pushout")).is_true

    def test_derived_pullback_true(self):
        assert has_homotopy_limits(_space("derived_pullback")).is_true

    def test_homotopy_fiber_true(self):
        assert has_homotopy_limits(_space("homotopy_fiber")).is_true

    def test_homotopy_cofiber_true(self):
        assert has_homotopy_limits(_space("homotopy_cofiber")).is_true

    def test_mayer_vietoris_true(self):
        assert has_homotopy_limits(_space("mayer_vietoris")).is_true

    def test_model_category_tag_true(self):
        assert has_homotopy_limits(_space("model_category")).is_true

    def test_weak_equivalence_model_true(self):
        assert has_homotopy_limits(_space("weak_equivalence")).is_true

    def test_quillen_model_structure_true(self):
        assert has_homotopy_limits(_space("quillen_model_structure")).is_true

    def test_lifting_property_true(self):
        assert has_homotopy_limits(_space("lifting_property")).is_true

    def test_homotopy_category_true(self):
        assert has_homotopy_limits(_space("homotopy_category")).is_true

    def test_no_homotopy_limits_false(self):
        assert has_homotopy_limits(_space("no_homotopy_limits")).is_false

    def test_not_complete_false(self):
        assert has_homotopy_limits(_space("not_complete")).is_false

    def test_not_cocomplete_false(self):
        assert has_homotopy_limits(_space("not_cocomplete")).is_false

    def test_missing_factorization_false(self):
        assert has_homotopy_limits(_space("missing_factorization")).is_false

    def test_unknown_empty(self):
        r = has_homotopy_limits(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_holim(self):
        assert has_homotopy_limits(_space("homotopy_limit")).mode == "theorem"

    def test_mode_theorem_model(self):
        assert has_homotopy_limits(_space("model_category")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert has_homotopy_limits(_space()).mode == "symbolic"

    def test_criterion_explicit_homotopy_limit(self):
        r = has_homotopy_limits(_space("homotopy_pushout"))
        assert r.metadata.get("criterion") == "explicit_homotopy_limit"

    def test_criterion_model_category_has_holim(self):
        r = has_homotopy_limits(_space("model_category"))
        assert r.metadata.get("criterion") == "model_category_has_holim"

    def test_criterion_no_holim(self):
        r = has_homotopy_limits(_space("no_homotopy_limits"))
        assert r.metadata.get("criterion") == "no_holim"

    def test_factorization_axiom_true(self):
        assert has_homotopy_limits(_space("factorization_axiom")).is_true


# ---------------------------------------------------------------------------
# is_stable_model_category
# ---------------------------------------------------------------------------

class TestIsStableModelCategory:
    def test_stable_model_category_tag_true(self):
        assert is_stable_model_category(_space("stable_model_category")).is_true

    def test_suspension_equivalence_true(self):
        assert is_stable_model_category(_space("suspension_equivalence")).is_true

    def test_spectra_true(self):
        assert is_stable_model_category(_space("spectra")).is_true

    def test_loop_space_equivalence_true(self):
        assert is_stable_model_category(_space("loop_space_equivalence")).is_true

    def test_triangulated_homotopy_category_true(self):
        assert is_stable_model_category(_space("triangulated_homotopy_category")).is_true

    def test_stable_homotopy_category_true(self):
        assert is_stable_model_category(_space("stable_homotopy_category")).is_true

    def test_bousfield_friedlander_true(self):
        assert is_stable_model_category(_space("bousfield_friedlander")).is_true

    def test_symmetric_spectra_true(self):
        assert is_stable_model_category(_space("symmetric_spectra")).is_true

    def test_chain_complexes_true(self):
        assert is_stable_model_category(_space("chain_complexes")).is_true

    def test_derived_category_true(self):
        assert is_stable_model_category(_space("derived_category")).is_true

    def test_projective_model_true(self):
        assert is_stable_model_category(_space("projective_model")).is_true

    def test_injective_model_true(self):
        assert is_stable_model_category(_space("injective_model")).is_true

    def test_topological_spaces_false(self):
        assert is_stable_model_category(_space("topological_spaces")).is_false

    def test_simplicial_sets_false(self):
        assert is_stable_model_category(_space("simplicial_sets")).is_false

    def test_kan_quillen_false(self):
        assert is_stable_model_category(_space("kan_quillen")).is_false

    def test_quillen_top_false(self):
        assert is_stable_model_category(_space("quillen_top")).is_false

    def test_not_stable_model_false(self):
        assert is_stable_model_category(_space("not_stable_model")).is_false

    def test_unstable_homotopy_false(self):
        assert is_stable_model_category(_space("unstable_homotopy")).is_false

    def test_unknown_empty(self):
        r = is_stable_model_category(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_stable(self):
        assert is_stable_model_category(_space("stable_model_category")).mode == "theorem"

    def test_mode_theorem_chain(self):
        assert is_stable_model_category(_space("chain_complexes")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_stable_model_category(_space("topological_spaces")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert is_stable_model_category(_space()).mode == "symbolic"

    def test_criterion_explicit_stable(self):
        r = is_stable_model_category(_space("stable_model_category"))
        assert r.metadata.get("criterion") == "explicit_stable"

    def test_criterion_chain_complex_stable(self):
        r = is_stable_model_category(_space("chain_complexes"))
        assert r.metadata.get("criterion") == "chain_complex_stable"

    def test_criterion_not_stable(self):
        r = is_stable_model_category(_space("topological_spaces"))
        assert r.metadata.get("criterion") == "not_stable"


# ---------------------------------------------------------------------------
# admits_bousfield_localization
# ---------------------------------------------------------------------------

class TestAdmitsBousfieldLocalization:
    def test_bousfield_localization_tag_true(self):
        assert admits_bousfield_localization(_space("bousfield_localization")).is_true

    def test_left_bousfield_localization_true(self):
        assert admits_bousfield_localization(_space("left_bousfield_localization")).is_true

    def test_local_objects_true(self):
        assert admits_bousfield_localization(_space("local_objects")).is_true

    def test_local_equivalences_true(self):
        assert admits_bousfield_localization(_space("local_equivalences")).is_true

    def test_nullification_true(self):
        assert admits_bousfield_localization(_space("nullification")).is_true

    def test_combinatorial_and_left_proper_true(self):
        assert admits_bousfield_localization(
            _space("combinatorial_model", "left_proper")
        ).is_true

    def test_locally_presentable_and_proper_true(self):
        assert admits_bousfield_localization(
            _space("locally_presentable", "left_proper")
        ).is_true

    def test_cellular_and_proper_true(self):
        assert admits_bousfield_localization(
            _space("cellular_model", "left_proper")
        ).is_true

    def test_cellular_and_proper_model_true(self):
        assert admits_bousfield_localization(
            _space("cellular_cofibrations", "proper_model")
        ).is_true

    def test_cofibrantly_generated_and_left_proper_true(self):
        assert admits_bousfield_localization(
            _space("cofibrantly_generated", "left_proper")
        ).is_true

    def test_not_left_proper_false(self):
        assert admits_bousfield_localization(_space("not_left_proper")).is_false

    def test_not_combinatorial_false(self):
        assert admits_bousfield_localization(_space("not_combinatorial")).is_false

    def test_not_cellular_false(self):
        assert admits_bousfield_localization(_space("not_cellular")).is_false

    def test_no_bousfield_localization_false(self):
        assert admits_bousfield_localization(_space("no_bousfield_localization")).is_false

    def test_combinatorial_alone_unknown(self):
        r = admits_bousfield_localization(_space("combinatorial_model"))
        assert not r.is_true and not r.is_false

    def test_left_proper_alone_unknown(self):
        r = admits_bousfield_localization(_space("left_proper"))
        assert not r.is_true and not r.is_false

    def test_unknown_empty(self):
        r = admits_bousfield_localization(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert admits_bousfield_localization(_space("bousfield_localization")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert admits_bousfield_localization(_space("not_left_proper")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert admits_bousfield_localization(_space()).mode == "symbolic"

    def test_criterion_explicit_bousfield(self):
        r = admits_bousfield_localization(_space("bousfield_localization"))
        assert r.metadata.get("criterion") == "explicit_bousfield"

    def test_criterion_proper_cellular(self):
        r = admits_bousfield_localization(_space("combinatorial_model", "left_proper"))
        assert r.metadata.get("criterion") == "proper_cellular_combinatorial"

    def test_criterion_localization_fails(self):
        r = admits_bousfield_localization(_space("not_left_proper"))
        assert r.metadata.get("criterion") == "localization_fails"

    def test_right_bousfield_localization_true(self):
        assert admits_bousfield_localization(_space("right_bousfield_localization")).is_true


# ---------------------------------------------------------------------------
# classify_abstract_homotopy
# ---------------------------------------------------------------------------

class TestClassifyAbstractHomotopy:
    def test_returns_dict(self):
        assert isinstance(classify_abstract_homotopy(_space()), dict)

    def test_required_keys(self):
        r = classify_abstract_homotopy(_space())
        assert {
            "homotopy_class", "is_proper_model_category", "has_homotopy_limits",
            "is_stable_model_category", "admits_bousfield_localization",
            "key_properties", "representation", "tags",
        } <= r.keys()

    def test_stable_proper_class(self):
        r = classify_abstract_homotopy(
            _space("spectra", "proper_model", "bousfield_localization")
        )
        assert r["homotopy_class"] == "stable_proper"

    def test_stable_localizable_class(self):
        r = classify_abstract_homotopy(
            _space("stable_model_category", "bousfield_localization")
        )
        assert r["homotopy_class"] == "stable_localizable"

    def test_infinity_categorical_class(self):
        r = classify_abstract_homotopy(_space("quasi_category"))
        assert r["homotopy_class"] == "infinity_categorical"

    def test_unstable_proper_class(self):
        r = classify_abstract_homotopy(
            _space("proper_model", "homotopy_limit")
        )
        assert r["homotopy_class"] == "unstable_proper"

    def test_basic_model_class(self):
        r = classify_abstract_homotopy(_space("model_category"))
        assert r["homotopy_class"] == "basic_model"

    def test_proper_in_properties(self):
        r = classify_abstract_homotopy(_space("proper_model"))
        assert "proper" in r["key_properties"]

    def test_not_fully_proper_in_properties(self):
        r = classify_abstract_homotopy(_space("not_proper"))
        assert "not_fully_proper" in r["key_properties"]

    def test_homotopy_limits_in_properties(self):
        r = classify_abstract_homotopy(_space("homotopy_pushout"))
        assert "homotopy_limits_colimits" in r["key_properties"]

    def test_stable_in_properties(self):
        r = classify_abstract_homotopy(_space("stable_model_category"))
        assert "stable" in r["key_properties"]

    def test_unstable_in_properties(self):
        r = classify_abstract_homotopy(_space("topological_spaces"))
        assert "unstable" in r["key_properties"]

    def test_admits_localization_in_properties(self):
        r = classify_abstract_homotopy(_space("bousfield_localization"))
        assert "admits_localization" in r["key_properties"]

    def test_infinity_categorical_in_properties(self):
        r = classify_abstract_homotopy(_space("quasi_category"))
        assert "infinity_categorical" in r["key_properties"]

    def test_quillen_adjunction_in_properties(self):
        r = classify_abstract_homotopy(_space("quillen_adjunction"))
        assert "quillen_adjunction" in r["key_properties"]

    def test_cofibrant_fibrant_in_properties(self):
        r = classify_abstract_homotopy(_space("cofibrant_replacement"))
        assert "cofibrant_fibrant_replacement" in r["key_properties"]

    def test_tags_sorted(self):
        r = classify_abstract_homotopy(_space("spectra", "proper_model"))
        assert r["tags"] == sorted(r["tags"])

    def test_representation_passthrough(self):
        r = classify_abstract_homotopy(_space("model_category", rep="my_rep"))
        assert r["representation"] == "my_rep"

    def test_kan_complex_infinity_categorical(self):
        r = classify_abstract_homotopy(_space("kan_complex"))
        assert r["homotopy_class"] == "infinity_categorical"

    def test_joyal_model_infinity_categorical(self):
        r = classify_abstract_homotopy(_space("joyal_model"))
        assert r["homotopy_class"] == "infinity_categorical"


# ---------------------------------------------------------------------------
# abstract_homotopy_profile
# ---------------------------------------------------------------------------

class TestAbstractHomotopyProfile:
    def test_returns_dict(self):
        assert isinstance(abstract_homotopy_profile(_space()), dict)

    def test_has_classification(self):
        assert "classification" in abstract_homotopy_profile(_space())

    def test_has_named_profiles(self):
        assert "named_profiles" in abstract_homotopy_profile(_space())

    def test_has_layer_summary(self):
        assert "layer_summary" in abstract_homotopy_profile(_space())

    def test_classification_is_dict(self):
        assert isinstance(abstract_homotopy_profile(_space())["classification"], dict)

    def test_named_profiles_is_tuple(self):
        assert isinstance(abstract_homotopy_profile(_space())["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        assert isinstance(abstract_homotopy_profile(_space())["layer_summary"], dict)

    def test_named_profiles_nonempty(self):
        assert len(abstract_homotopy_profile(_space())["named_profiles"]) >= 6


# ---------------------------------------------------------------------------
# AbstractHomotopyProfile dataclass
# ---------------------------------------------------------------------------

class TestAbstractHomotopyProfileDataclass:
    def test_frozen(self):
        p = AbstractHomotopyProfile(
            key="t", display_name="T", category_type="model_category",
            weak_equivalences="we", fibrations="fib", cofibrations="cof",
            is_proper=True, is_stable=False, admits_localization=True,
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        with pytest.raises(Exception):
            p.key = "other"  # type: ignore[misc]

    def test_equality_by_value(self):
        kwargs = dict(
            key="t", display_name="T", category_type="model_category",
            weak_equivalences="we", fibrations="fib", cofibrations="cof",
            is_proper=True, is_stable=False, admits_localization=True,
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        assert AbstractHomotopyProfile(**kwargs) == AbstractHomotopyProfile(**kwargs)

    def test_all_fields_accessible(self):
        p = AbstractHomotopyProfile(
            key="x", display_name="X", category_type="stable_model_category",
            weak_equivalences="pi_* isos", fibrations="omega-fibrations",
            cofibrations="spec-cofibrations",
            is_proper=True, is_stable=True, admits_localization=True,
            presentation_layer="selected_block", focus="spectra",
            chapter_targets=("22", "35"),
        )
        assert p.is_stable is True
        assert p.category_type == "stable_model_category"
        assert p.chapter_targets == ("22", "35")

    def test_inequality_on_different_keys(self):
        def _make(key: str) -> AbstractHomotopyProfile:
            return AbstractHomotopyProfile(
                key=key, display_name="T", category_type="model_category",
                weak_equivalences="we", fibrations="fib", cofibrations="cof",
                is_proper=True, is_stable=False, admits_localization=True,
                presentation_layer="main_text", focus="f", chapter_targets=("1",),
            )
        assert _make("a") != _make("b")
