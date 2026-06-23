"""Tests for topos_theory.py (v0.5.16)."""

import pytest

from pytop.result import Result
from pytop.spaces import TopologicalSpace
from pytop.topos_theory import (
    BOOLEAN_TOPOS_TAGS,
    ELEMENTARY_TOPOS_TAGS,
    ENOUGH_POINTS_TAGS,
    GEOMETRIC_MORPHISM_TAGS,
    GROTHENDIECK_TOPOS_TAGS,
    LOCALIC_TOPOS_TAGS,
    NOT_BOOLEAN_TOPOS_TAGS,
    NOT_GROTHENDIECK_TAGS,
    ToposProfile,
    classify_topos,
    get_named_topos_profiles,
    has_enough_points_topos,
    is_boolean_topos,
    is_grothendieck_topos,
    is_localic_topos,
    topos_chapter_index,
    topos_layer_summary,
    topos_profile,
    topos_type_index,
)


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_grothendieck_contains_grothendieck_topos(self):
        assert "grothendieck_topos" in GROTHENDIECK_TOPOS_TAGS

    def test_grothendieck_contains_sheaves_on_site(self):
        assert "sheaves_on_site" in GROTHENDIECK_TOPOS_TAGS

    def test_grothendieck_contains_sheaves_on_space(self):
        assert "sheaves_on_space" in GROTHENDIECK_TOPOS_TAGS

    def test_grothendieck_contains_presheaf_topos(self):
        assert "presheaf_topos" in GROTHENDIECK_TOPOS_TAGS

    def test_grothendieck_contains_localic_topos(self):
        assert "localic_topos" in GROTHENDIECK_TOPOS_TAGS

    def test_grothendieck_contains_etale_topos(self):
        assert "etale_topos" in GROTHENDIECK_TOPOS_TAGS

    def test_elementary_contains_elementary_topos(self):
        assert "elementary_topos" in ELEMENTARY_TOPOS_TAGS

    def test_elementary_contains_subobject_classifier(self):
        assert "subobject_classifier" in ELEMENTARY_TOPOS_TAGS

    def test_elementary_contains_effective_topos(self):
        assert "effective_topos" in ELEMENTARY_TOPOS_TAGS

    def test_boolean_contains_boolean_topos(self):
        assert "boolean_topos" in BOOLEAN_TOPOS_TAGS

    def test_boolean_contains_presheaf_topos(self):
        assert "presheaf_topos" in BOOLEAN_TOPOS_TAGS

    def test_boolean_contains_set_topos(self):
        assert "set_topos" in BOOLEAN_TOPOS_TAGS

    def test_boolean_contains_g_sets_topos(self):
        assert "g_sets_topos" in BOOLEAN_TOPOS_TAGS

    def test_localic_contains_localic_topos(self):
        assert "localic_topos" in LOCALIC_TOPOS_TAGS

    def test_localic_contains_sheaves_on_locale(self):
        assert "sheaves_on_locale" in LOCALIC_TOPOS_TAGS

    def test_localic_contains_sheaves_on_space(self):
        assert "sheaves_on_space" in LOCALIC_TOPOS_TAGS

    def test_enough_points_contains_presheaf_topos(self):
        assert "presheaf_topos" in ENOUGH_POINTS_TAGS

    def test_enough_points_contains_set_topos(self):
        assert "set_topos" in ENOUGH_POINTS_TAGS

    def test_not_boolean_contains_etale_topos(self):
        assert "etale_topos" in NOT_BOOLEAN_TOPOS_TAGS

    def test_not_boolean_contains_effective_topos(self):
        assert "effective_topos" in NOT_BOOLEAN_TOPOS_TAGS

    def test_not_grothendieck_contains_effective_topos(self):
        assert "effective_topos" in NOT_GROTHENDIECK_TAGS

    def test_not_grothendieck_contains_realizability_topos(self):
        assert "realizability_topos" in NOT_GROTHENDIECK_TAGS

    def test_geometric_morphism_contains_geometric_morphism(self):
        assert "geometric_morphism" in GEOMETRIC_MORPHISM_TAGS

    def test_all_tag_constants_are_sets(self):
        for s in [GROTHENDIECK_TOPOS_TAGS, ELEMENTARY_TOPOS_TAGS, BOOLEAN_TOPOS_TAGS,
                  LOCALIC_TOPOS_TAGS, ENOUGH_POINTS_TAGS, NOT_BOOLEAN_TOPOS_TAGS,
                  NOT_GROTHENDIECK_TAGS, GEOMETRIC_MORPHISM_TAGS]:
            assert isinstance(s, frozenset)

    def test_effective_not_in_grothendieck_positive(self):
        # effective_topos is in elementary but NOT in grothendieck_topos positive tags
        assert "effective_topos" not in GROTHENDIECK_TOPOS_TAGS


# ---------------------------------------------------------------------------
# ToposProfile dataclass
# ---------------------------------------------------------------------------

class TestToposProfileDataclass:
    def test_profile_is_frozen(self):
        p = ToposProfile(
            key="t", display_name="T", topos_type="grothendieck_topos",
            is_grothendieck=True, is_elementary=True,
            is_boolean=False, is_localic=True,
            has_natural_number_object=True, has_enough_points=True,
            presentation_layer="main_text", focus="test",
            chapter_targets=("11",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields_accessible(self):
        p = ToposProfile(
            key="k", display_name="K", topos_type="boolean_topos",
            is_grothendieck=True, is_elementary=True,
            is_boolean=True, is_localic=False,
            has_natural_number_object=True, has_enough_points=True,
            presentation_layer="main_text", focus="presheaf",
            chapter_targets=("11", "29"),
        )
        assert p.key == "k"
        assert p.is_boolean is True
        assert p.is_localic is False
        assert p.has_enough_points is True
        assert p.chapter_targets == ("11", "29")

    def test_profile_equality(self):
        kwargs = dict(
            key="a", display_name="A", topos_type="elementary_topos",
            is_grothendieck=False, is_elementary=True,
            is_boolean=False, is_localic=False,
            has_natural_number_object=True, has_enough_points=False,
            presentation_layer="selected_block", focus="f",
            chapter_targets=("11",),
        )
        assert ToposProfile(**kwargs) == ToposProfile(**kwargs)


# ---------------------------------------------------------------------------
# Named profiles
# ---------------------------------------------------------------------------

class TestNamedToposProfiles:
    def setup_method(self):
        self.profiles = get_named_topos_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_five_profiles(self):
        assert len(self.profiles) >= 5

    def test_all_are_topos_profiles(self):
        for p in self.profiles:
            assert isinstance(p, ToposProfile)

    def test_keys_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_set_topos_exists(self):
        assert "set_topos" in {p.key for p in self.profiles}

    def test_sheaves_topological_space_exists(self):
        assert "sheaves_topological_space" in {p.key for p in self.profiles}

    def test_presheaf_topos_exists(self):
        assert "presheaf_topos" in {p.key for p in self.profiles}

    def test_classifying_topos_bg_exists(self):
        assert "classifying_topos_bg" in {p.key for p in self.profiles}

    def test_etale_topos_exists(self):
        assert "etale_topos" in {p.key for p in self.profiles}

    def test_effective_topos_exists(self):
        assert "effective_topos" in {p.key for p in self.profiles}

    def test_set_topos_is_grothendieck(self):
        p = next(x for x in self.profiles if x.key == "set_topos")
        assert p.is_grothendieck is True

    def test_set_topos_is_boolean(self):
        p = next(x for x in self.profiles if x.key == "set_topos")
        assert p.is_boolean is True

    def test_set_topos_is_localic(self):
        p = next(x for x in self.profiles if x.key == "set_topos")
        assert p.is_localic is True

    def test_set_topos_has_enough_points(self):
        p = next(x for x in self.profiles if x.key == "set_topos")
        assert p.has_enough_points is True

    def test_sheaves_space_is_grothendieck(self):
        p = next(x for x in self.profiles if x.key == "sheaves_topological_space")
        assert p.is_grothendieck is True

    def test_sheaves_space_is_localic(self):
        p = next(x for x in self.profiles if x.key == "sheaves_topological_space")
        assert p.is_localic is True

    def test_sheaves_space_not_boolean(self):
        p = next(x for x in self.profiles if x.key == "sheaves_topological_space")
        assert p.is_boolean is False

    def test_sheaves_space_has_nno(self):
        p = next(x for x in self.profiles if x.key == "sheaves_topological_space")
        assert p.has_natural_number_object is True

    def test_presheaf_is_grothendieck(self):
        p = next(x for x in self.profiles if x.key == "presheaf_topos")
        assert p.is_grothendieck is True

    def test_presheaf_is_boolean(self):
        p = next(x for x in self.profiles if x.key == "presheaf_topos")
        assert p.is_boolean is True

    def test_presheaf_not_localic(self):
        p = next(x for x in self.profiles if x.key == "presheaf_topos")
        assert p.is_localic is False

    def test_presheaf_has_enough_points(self):
        p = next(x for x in self.profiles if x.key == "presheaf_topos")
        assert p.has_enough_points is True

    def test_bg_is_grothendieck(self):
        p = next(x for x in self.profiles if x.key == "classifying_topos_bg")
        assert p.is_grothendieck is True

    def test_bg_is_boolean(self):
        p = next(x for x in self.profiles if x.key == "classifying_topos_bg")
        assert p.is_boolean is True

    def test_bg_not_localic(self):
        p = next(x for x in self.profiles if x.key == "classifying_topos_bg")
        assert p.is_localic is False

    def test_etale_is_grothendieck(self):
        p = next(x for x in self.profiles if x.key == "etale_topos")
        assert p.is_grothendieck is True

    def test_etale_not_boolean(self):
        p = next(x for x in self.profiles if x.key == "etale_topos")
        assert p.is_boolean is False

    def test_etale_not_localic(self):
        p = next(x for x in self.profiles if x.key == "etale_topos")
        assert p.is_localic is False

    def test_etale_not_enough_points(self):
        p = next(x for x in self.profiles if x.key == "etale_topos")
        assert p.has_enough_points is False

    def test_effective_not_grothendieck(self):
        p = next(x for x in self.profiles if x.key == "effective_topos")
        assert p.is_grothendieck is False

    def test_effective_is_elementary(self):
        p = next(x for x in self.profiles if x.key == "effective_topos")
        assert p.is_elementary is True

    def test_effective_not_boolean(self):
        p = next(x for x in self.profiles if x.key == "effective_topos")
        assert p.is_boolean is False

    def test_effective_has_nno(self):
        p = next(x for x in self.profiles if x.key == "effective_topos")
        assert p.has_natural_number_object is True

    def test_effective_not_enough_points(self):
        p = next(x for x in self.profiles if x.key == "effective_topos")
        assert p.has_enough_points is False

    def test_grothendieck_implies_elementary(self):
        for p in self.profiles:
            if p.is_grothendieck:
                assert p.is_elementary is True

    def test_all_have_nonempty_focus(self):
        for p in self.profiles:
            assert len(p.focus) > 30

    def test_all_have_chapter_targets(self):
        for p in self.profiles:
            assert len(p.chapter_targets) >= 1

    def test_all_presentation_layers_valid(self):
        valid = {"main_text", "selected_block", "appendix", "exercise"}
        for p in self.profiles:
            assert p.presentation_layer in valid


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(topos_layer_summary(), dict)

    def test_layer_summary_sum_equals_profile_count(self):
        total = sum(topos_layer_summary().values())
        assert total == len(get_named_topos_profiles())

    def test_layer_summary_has_main_text(self):
        assert "main_text" in topos_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in topos_layer_summary()

    def test_chapter_index_returns_dict(self):
        assert isinstance(topos_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in topos_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_contains_chapter_11(self):
        assert "11" in topos_chapter_index()

    def test_chapter_index_contains_chapter_29(self):
        assert "29" in topos_chapter_index()

    def test_set_topos_in_chapter_53(self):
        assert "set_topos" in topos_chapter_index()["53"]

    def test_type_index_returns_dict(self):
        assert isinstance(topos_type_index(), dict)

    def test_type_index_has_boolean_topos(self):
        assert "boolean_topos" in topos_type_index()

    def test_type_index_has_localic_topos(self):
        assert "localic_topos" in topos_type_index()

    def test_type_index_has_elementary_topos(self):
        assert "elementary_topos" in topos_type_index()

    def test_type_index_all_types_in_profiles(self):
        all_types = {p.topos_type for p in get_named_topos_profiles()}
        assert set(topos_type_index().keys()) == all_types


# ---------------------------------------------------------------------------
# is_grothendieck_topos
# ---------------------------------------------------------------------------

class TestIsGrothendieckTopos:
    def test_grothendieck_topos_tag_true(self):
        assert is_grothendieck_topos(_sp("grothendieck_topos")).is_true

    def test_sheaves_on_site_true(self):
        assert is_grothendieck_topos(_sp("sheaves_on_site")).is_true

    def test_sheaves_on_space_true(self):
        assert is_grothendieck_topos(_sp("sheaves_on_space")).is_true

    def test_sheaves_on_locale_true(self):
        assert is_grothendieck_topos(_sp("sheaves_on_locale")).is_true

    def test_presheaf_topos_true(self):
        assert is_grothendieck_topos(_sp("presheaf_topos")).is_true

    def test_localic_topos_true(self):
        assert is_grothendieck_topos(_sp("localic_topos")).is_true

    def test_classifying_topos_true(self):
        assert is_grothendieck_topos(_sp("classifying_topos")).is_true

    def test_etale_topos_true(self):
        assert is_grothendieck_topos(_sp("etale_topos")).is_true

    def test_set_topos_true(self):
        assert is_grothendieck_topos(_sp("set_topos")).is_true

    def test_effective_topos_false(self):
        assert is_grothendieck_topos(_sp("effective_topos")).is_false

    def test_realizability_topos_false(self):
        assert is_grothendieck_topos(_sp("realizability_topos")).is_false

    def test_not_grothendieck_false(self):
        assert is_grothendieck_topos(_sp("not_grothendieck_topos")).is_false

    def test_empty_unknown(self):
        assert is_grothendieck_topos(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_grothendieck_topos(_sp("grothendieck_topos")), Result)

    def test_true_has_justification(self):
        r = is_grothendieck_topos(_sp("sheaves_on_site"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_grothendieck_topos(_sp("effective_topos"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_boolean_topos
# ---------------------------------------------------------------------------

class TestIsBooleanTopos:
    def test_boolean_topos_tag_true(self):
        assert is_boolean_topos(_sp("boolean_topos")).is_true

    def test_classical_logic_topos_true(self):
        assert is_boolean_topos(_sp("classical_logic_topos")).is_true

    def test_presheaf_topos_true(self):
        assert is_boolean_topos(_sp("presheaf_topos")).is_true

    def test_set_topos_true(self):
        assert is_boolean_topos(_sp("set_topos")).is_true

    def test_g_sets_topos_true(self):
        assert is_boolean_topos(_sp("g_sets_topos")).is_true

    def test_sheaves_boolean_space_true(self):
        assert is_boolean_topos(_sp("sheaves_boolean_space")).is_true

    def test_atomic_topos_true(self):
        assert is_boolean_topos(_sp("atomic_topos")).is_true

    def test_etale_topos_false(self):
        assert is_boolean_topos(_sp("etale_topos")).is_false

    def test_zariski_topos_false(self):
        assert is_boolean_topos(_sp("zariski_topos")).is_false

    def test_effective_topos_false(self):
        assert is_boolean_topos(_sp("effective_topos")).is_false

    def test_not_boolean_topos_false(self):
        assert is_boolean_topos(_sp("not_boolean_topos")).is_false

    def test_intuitionistic_topos_false(self):
        assert is_boolean_topos(_sp("intuitionistic_topos")).is_false

    def test_empty_unknown(self):
        assert is_boolean_topos(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_boolean_topos(_sp("boolean_topos")), Result)

    def test_true_has_justification(self):
        r = is_boolean_topos(_sp("presheaf_topos"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_boolean_topos(_sp("etale_topos"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_localic_topos
# ---------------------------------------------------------------------------

class TestIsLocalicTopos:
    def test_localic_topos_tag_true(self):
        assert is_localic_topos(_sp("localic_topos")).is_true

    def test_sheaves_on_locale_true(self):
        assert is_localic_topos(_sp("sheaves_on_locale")).is_true

    def test_sheaves_on_space_true(self):
        assert is_localic_topos(_sp("sheaves_on_space")).is_true

    def test_spatial_topos_true(self):
        assert is_localic_topos(_sp("spatial_topos")).is_true

    def test_set_topos_true(self):
        assert is_localic_topos(_sp("set_topos")).is_true

    def test_presheaf_topos_false(self):
        assert is_localic_topos(_sp("presheaf_topos")).is_false

    def test_g_sets_topos_false(self):
        assert is_localic_topos(_sp("g_sets_topos")).is_false

    def test_classifying_topos_false(self):
        assert is_localic_topos(_sp("classifying_topos")).is_false

    def test_etale_topos_false(self):
        assert is_localic_topos(_sp("etale_topos")).is_false

    def test_empty_unknown(self):
        assert is_localic_topos(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_localic_topos(_sp("localic_topos")), Result)

    def test_true_has_justification(self):
        r = is_localic_topos(_sp("sheaves_on_space"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_localic_topos(_sp("presheaf_topos"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# has_enough_points_topos
# ---------------------------------------------------------------------------

class TestHasEnoughPointsTopos:
    def test_enough_points_tag_true(self):
        assert has_enough_points_topos(_sp("enough_points_topos")).is_true

    def test_set_valued_points_true(self):
        assert has_enough_points_topos(_sp("set_valued_points")).is_true

    def test_presheaf_topos_true(self):
        assert has_enough_points_topos(_sp("presheaf_topos")).is_true

    def test_set_topos_true(self):
        assert has_enough_points_topos(_sp("set_topos")).is_true

    def test_g_sets_topos_true(self):
        assert has_enough_points_topos(_sp("g_sets_topos")).is_true

    def test_sheaves_hausdorff_true(self):
        assert has_enough_points_topos(_sp("sheaves_hausdorff_space")).is_true

    def test_effective_topos_false(self):
        assert has_enough_points_topos(_sp("effective_topos")).is_false

    def test_realizability_false(self):
        assert has_enough_points_topos(_sp("realizability_topos")).is_false

    def test_not_enough_points_false(self):
        assert has_enough_points_topos(_sp("not_enough_points")).is_false

    def test_empty_unknown(self):
        assert has_enough_points_topos(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(has_enough_points_topos(_sp("presheaf_topos")), Result)

    def test_true_has_justification(self):
        r = has_enough_points_topos(_sp("presheaf_topos"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = has_enough_points_topos(_sp("effective_topos"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# classify_topos
# ---------------------------------------------------------------------------

class TestClassifyTopos:
    def test_returns_dict(self):
        assert isinstance(classify_topos(_sp()), dict)

    def test_has_topos_class_key(self):
        assert "topos_class" in classify_topos(_sp())

    def test_has_is_grothendieck_key(self):
        assert "is_grothendieck_topos" in classify_topos(_sp())

    def test_has_is_boolean_key(self):
        assert "is_boolean_topos" in classify_topos(_sp())

    def test_has_is_localic_key(self):
        assert "is_localic_topos" in classify_topos(_sp())

    def test_has_enough_points_key(self):
        assert "has_enough_points_topos" in classify_topos(_sp())

    def test_has_key_properties_key(self):
        assert "key_properties" in classify_topos(_sp())

    def test_key_properties_is_list(self):
        assert isinstance(classify_topos(_sp())["key_properties"], list)

    def test_set_class(self):
        r = classify_topos(_sp("set_topos"))
        assert r["topos_class"] == "set"

    def test_boolean_grothendieck_class(self):
        r = classify_topos(_sp("presheaf_topos"))
        assert r["topos_class"] == "boolean_grothendieck"

    def test_localic_class(self):
        r = classify_topos(_sp("sheaves_on_space"))
        assert r["topos_class"] == "localic"

    def test_grothendieck_class(self):
        r = classify_topos(_sp("etale_topos"))
        assert r["topos_class"] == "grothendieck"

    def test_elementary_class(self):
        r = classify_topos(_sp("effective_topos"))
        assert r["topos_class"] == "elementary"

    def test_unknown_class_empty(self):
        r = classify_topos(_sp())
        assert r["topos_class"] == "unknown"

    def test_grothendieck_in_key_props(self):
        r = classify_topos(_sp("sheaves_on_site"))
        assert "grothendieck" in r["key_properties"]

    def test_boolean_in_key_props(self):
        r = classify_topos(_sp("presheaf_topos"))
        assert "boolean" in r["key_properties"]

    def test_intuitionistic_in_key_props(self):
        r = classify_topos(_sp("etale_topos"))
        assert "intuitionistic" in r["key_properties"]

    def test_localic_in_key_props(self):
        r = classify_topos(_sp("sheaves_on_space"))
        assert "localic" in r["key_properties"]

    def test_enough_points_in_key_props(self):
        r = classify_topos(_sp("presheaf_topos"))
        assert "enough_points" in r["key_properties"]

    def test_not_grothendieck_in_key_props(self):
        r = classify_topos(_sp("effective_topos"))
        assert "not_grothendieck" in r["key_properties"]

    def test_nno_in_key_props_for_grothendieck(self):
        r = classify_topos(_sp("sheaves_on_site"))
        assert "natural_number_object" in r["key_properties"]

    def test_representation_in_output(self):
        assert "representation" in classify_topos(_sp())

    def test_tags_is_list(self):
        assert isinstance(classify_topos(_sp("presheaf_topos"))["tags"], list)


# ---------------------------------------------------------------------------
# topos_profile
# ---------------------------------------------------------------------------

class TestToposProfile:
    def test_returns_dict(self):
        assert isinstance(topos_profile(_sp()), dict)

    def test_has_classification_key(self):
        assert "classification" in topos_profile(_sp())

    def test_has_named_profiles_key(self):
        assert "named_profiles" in topos_profile(_sp())

    def test_has_layer_summary_key(self):
        assert "layer_summary" in topos_profile(_sp())

    def test_named_profiles_is_tuple(self):
        assert isinstance(topos_profile(_sp())["named_profiles"], tuple)

    def test_classification_has_topos_class(self):
        p = topos_profile(_sp("presheaf_topos"))
        assert "topos_class" in p["classification"]

    def test_layer_summary_is_dict(self):
        assert isinstance(topos_profile(_sp())["layer_summary"], dict)

    def test_set_classification_correct(self):
        p = topos_profile(_sp("set_topos"))
        assert p["classification"]["topos_class"] == "set"

    def test_elementary_classification_correct(self):
        p = topos_profile(_sp("effective_topos"))
        assert p["classification"]["topos_class"] == "elementary"
