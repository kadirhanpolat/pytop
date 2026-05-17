"""Tests for fiber_bundles.py (v0.5.12)."""

import pytest

from pytop.fiber_bundles import (
    LOCALLY_TRIVIAL_TAGS,
    NOT_NOWHERE_ZERO_SECTION_TAGS,
    NOT_TRIVIAL_TAGS,
    NOWHERE_ZERO_SECTION_TAGS,
    ORIENTABLE_BUNDLE_TAGS,
    PRINCIPAL_BUNDLE_TAGS,
    TRIVIAL_BUNDLE_TAGS,
    VECTOR_BUNDLE_TAGS,
    FiberBundleProfile,
    classify_bundle,
    fiber_bundle_chapter_index,
    fiber_bundle_layer_summary,
    fiber_bundle_profile,
    fiber_bundle_type_index,
    get_named_fiber_bundle_profiles,
    has_nowhere_zero_section,
    is_locally_trivial,
    is_orientable_bundle,
    is_trivial_bundle,
    is_vector_bundle,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_locally_trivial_contains_fiber_bundle(self):
        assert "fiber_bundle" in LOCALLY_TRIVIAL_TAGS

    def test_locally_trivial_contains_vector_bundle(self):
        assert "vector_bundle" in LOCALLY_TRIVIAL_TAGS

    def test_locally_trivial_contains_principal_bundle(self):
        assert "principal_bundle" in LOCALLY_TRIVIAL_TAGS

    def test_locally_trivial_contains_mobius_band(self):
        assert "mobius_band" in LOCALLY_TRIVIAL_TAGS

    def test_locally_trivial_contains_tangent_bundle(self):
        assert "tangent_bundle" in LOCALLY_TRIVIAL_TAGS

    def test_locally_trivial_contains_hopf_bundle(self):
        assert "hopf_bundle" in LOCALLY_TRIVIAL_TAGS

    def test_vector_bundle_contains_vector_bundle(self):
        assert "vector_bundle" in VECTOR_BUNDLE_TAGS

    def test_vector_bundle_contains_line_bundle(self):
        assert "line_bundle" in VECTOR_BUNDLE_TAGS

    def test_vector_bundle_contains_tangent_bundle(self):
        assert "tangent_bundle" in VECTOR_BUNDLE_TAGS

    def test_vector_bundle_contains_mobius_band(self):
        assert "mobius_band" in VECTOR_BUNDLE_TAGS

    def test_principal_bundle_contains_principal_bundle(self):
        assert "principal_bundle" in PRINCIPAL_BUNDLE_TAGS

    def test_principal_bundle_contains_frame_bundle(self):
        assert "frame_bundle" in PRINCIPAL_BUNDLE_TAGS

    def test_principal_bundle_contains_hopf_bundle(self):
        assert "hopf_bundle" in PRINCIPAL_BUNDLE_TAGS

    def test_trivial_bundle_contains_trivial_bundle(self):
        assert "trivial_bundle" in TRIVIAL_BUNDLE_TAGS

    def test_trivial_bundle_contains_product_bundle(self):
        assert "product_bundle" in TRIVIAL_BUNDLE_TAGS

    def test_trivial_bundle_contains_parallelizable(self):
        assert "parallelizable" in TRIVIAL_BUNDLE_TAGS

    def test_nowhere_zero_contains_parallelizable(self):
        assert "parallelizable" in NOWHERE_ZERO_SECTION_TAGS

    def test_nowhere_zero_contains_trivial_bundle(self):
        assert "trivial_bundle" in NOWHERE_ZERO_SECTION_TAGS

    def test_orientable_contains_complex_vector_bundle(self):
        assert "complex_vector_bundle" in ORIENTABLE_BUNDLE_TAGS

    def test_orientable_contains_trivial_bundle(self):
        assert "trivial_bundle" in ORIENTABLE_BUNDLE_TAGS

    def test_not_trivial_contains_mobius_band(self):
        assert "mobius_band" in NOT_TRIVIAL_TAGS

    def test_not_trivial_contains_hopf_bundle(self):
        assert "hopf_bundle" in NOT_TRIVIAL_TAGS

    def test_not_trivial_contains_tautological_bundle(self):
        assert "tautological_bundle" in NOT_TRIVIAL_TAGS

    def test_not_nowhere_zero_contains_mobius_band(self):
        assert "mobius_band" in NOT_NOWHERE_ZERO_SECTION_TAGS

    def test_not_nowhere_zero_contains_even_sphere(self):
        assert "even_sphere_tangent" in NOT_NOWHERE_ZERO_SECTION_TAGS

    def test_not_nowhere_zero_contains_sphere_s2(self):
        assert "sphere_s2_tangent" in NOT_NOWHERE_ZERO_SECTION_TAGS

    def test_tag_sets_are_sets(self):
        for s in [LOCALLY_TRIVIAL_TAGS, VECTOR_BUNDLE_TAGS, PRINCIPAL_BUNDLE_TAGS,
                  TRIVIAL_BUNDLE_TAGS, NOWHERE_ZERO_SECTION_TAGS, ORIENTABLE_BUNDLE_TAGS,
                  NOT_TRIVIAL_TAGS, NOT_NOWHERE_ZERO_SECTION_TAGS]:
            assert isinstance(s, set)

    def test_hopf_bundle_not_in_vector_bundle_tags(self):
        assert "hopf_bundle" not in VECTOR_BUNDLE_TAGS

    def test_principal_bundle_not_in_trivial_tags(self):
        assert "principal_bundle" not in TRIVIAL_BUNDLE_TAGS


# ---------------------------------------------------------------------------
# FiberBundleProfile dataclass
# ---------------------------------------------------------------------------

class TestFiberBundleProfileDataclass:
    def test_profile_is_frozen(self):
        p = FiberBundleProfile(
            key="t", display_name="T", bundle_type="trivial",
            is_locally_trivial=True, is_vector_bundle=True, is_principal=False,
            is_trivial=True, has_nowhere_zero_section=True, is_orientable=True,
            presentation_layer="main_text", focus="f", chapter_targets=("7",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields_accessible(self):
        p = FiberBundleProfile(
            key="k", display_name="D", bundle_type="line_bundle",
            is_locally_trivial=True, is_vector_bundle=True, is_principal=False,
            is_trivial=False, has_nowhere_zero_section=False, is_orientable=False,
            presentation_layer="main_text", focus="f", chapter_targets=("7", "25"),
        )
        assert p.key == "k"
        assert p.is_vector_bundle is True
        assert p.is_trivial is False
        assert p.chapter_targets == ("7", "25")

    def test_profile_equality(self):
        kwargs = dict(
            key="a", display_name="A", bundle_type="trivial",
            is_locally_trivial=True, is_vector_bundle=True, is_principal=False,
            is_trivial=True, has_nowhere_zero_section=True, is_orientable=True,
            presentation_layer="main_text", focus="f", chapter_targets=("7",),
        )
        assert FiberBundleProfile(**kwargs) == FiberBundleProfile(**kwargs)


# ---------------------------------------------------------------------------
# Named profiles
# ---------------------------------------------------------------------------

class TestNamedFiberBundleProfiles:
    def setup_method(self):
        self.profiles = get_named_fiber_bundle_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_five_profiles(self):
        assert len(self.profiles) >= 5

    def test_all_are_fiber_bundle_profiles(self):
        for p in self.profiles:
            assert isinstance(p, FiberBundleProfile)

    def test_keys_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_product_bundle_exists(self):
        keys = {p.key for p in self.profiles}
        assert "product_bundle" in keys

    def test_mobius_band_exists(self):
        keys = {p.key for p in self.profiles}
        assert "mobius_band" in keys

    def test_tangent_bundle_even_sphere_exists(self):
        keys = {p.key for p in self.profiles}
        assert "tangent_bundle_even_sphere" in keys

    def test_hopf_fibration_exists(self):
        keys = {p.key for p in self.profiles}
        assert "hopf_fibration" in keys

    def test_frame_bundle_exists(self):
        keys = {p.key for p in self.profiles}
        assert "frame_bundle" in keys

    def test_tautological_bundle_exists(self):
        keys = {p.key for p in self.profiles}
        assert "tautological_bundle" in keys

    def test_product_bundle_is_trivial(self):
        p = next(x for x in self.profiles if x.key == "product_bundle")
        assert p.is_trivial is True

    def test_product_bundle_is_vector_bundle(self):
        p = next(x for x in self.profiles if x.key == "product_bundle")
        assert p.is_vector_bundle is True

    def test_product_bundle_has_nowhere_zero_section(self):
        p = next(x for x in self.profiles if x.key == "product_bundle")
        assert p.has_nowhere_zero_section is True

    def test_product_bundle_is_orientable(self):
        p = next(x for x in self.profiles if x.key == "product_bundle")
        assert p.is_orientable is True

    def test_mobius_band_not_trivial(self):
        p = next(x for x in self.profiles if x.key == "mobius_band")
        assert p.is_trivial is False

    def test_mobius_band_is_vector_bundle(self):
        p = next(x for x in self.profiles if x.key == "mobius_band")
        assert p.is_vector_bundle is True

    def test_mobius_band_no_nowhere_zero_section(self):
        p = next(x for x in self.profiles if x.key == "mobius_band")
        assert p.has_nowhere_zero_section is False

    def test_mobius_band_not_orientable(self):
        p = next(x for x in self.profiles if x.key == "mobius_band")
        assert p.is_orientable is False

    def test_tangent_even_sphere_no_nowhere_zero_section(self):
        p = next(x for x in self.profiles if x.key == "tangent_bundle_even_sphere")
        assert p.has_nowhere_zero_section is False

    def test_tangent_even_sphere_is_vector_bundle(self):
        p = next(x for x in self.profiles if x.key == "tangent_bundle_even_sphere")
        assert p.is_vector_bundle is True

    def test_tangent_even_sphere_not_trivial(self):
        p = next(x for x in self.profiles if x.key == "tangent_bundle_even_sphere")
        assert p.is_trivial is False

    def test_tangent_even_sphere_is_orientable(self):
        p = next(x for x in self.profiles if x.key == "tangent_bundle_even_sphere")
        assert p.is_orientable is True

    def test_hopf_fibration_is_principal(self):
        p = next(x for x in self.profiles if x.key == "hopf_fibration")
        assert p.is_principal is True

    def test_hopf_fibration_not_trivial(self):
        p = next(x for x in self.profiles if x.key == "hopf_fibration")
        assert p.is_trivial is False

    def test_hopf_fibration_not_vector_bundle(self):
        p = next(x for x in self.profiles if x.key == "hopf_fibration")
        assert p.is_vector_bundle is False

    def test_frame_bundle_is_principal(self):
        p = next(x for x in self.profiles if x.key == "frame_bundle")
        assert p.is_principal is True

    def test_frame_bundle_not_vector_bundle(self):
        p = next(x for x in self.profiles if x.key == "frame_bundle")
        assert p.is_vector_bundle is False

    def test_tautological_bundle_not_trivial(self):
        p = next(x for x in self.profiles if x.key == "tautological_bundle")
        assert p.is_trivial is False

    def test_tautological_bundle_is_vector_bundle(self):
        p = next(x for x in self.profiles if x.key == "tautological_bundle")
        assert p.is_vector_bundle is True

    def test_all_locally_trivial(self):
        for p in self.profiles:
            assert p.is_locally_trivial is True

    def test_all_have_nonempty_focus(self):
        for p in self.profiles:
            assert len(p.focus) > 20

    def test_all_have_chapter_targets(self):
        for p in self.profiles:
            assert len(p.chapter_targets) >= 1

    def test_trivial_implies_locally_trivial(self):
        for p in self.profiles:
            if p.is_trivial:
                assert p.is_locally_trivial

    def test_trivial_implies_nowhere_zero_section(self):
        for p in self.profiles:
            if p.is_trivial:
                assert p.has_nowhere_zero_section


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(fiber_bundle_layer_summary(), dict)

    def test_layer_summary_values_are_ints(self):
        for v in fiber_bundle_layer_summary().values():
            assert isinstance(v, int)

    def test_layer_summary_sum_equals_profile_count(self):
        total = sum(fiber_bundle_layer_summary().values())
        assert total == len(get_named_fiber_bundle_profiles())

    def test_layer_summary_has_main_text(self):
        assert "main_text" in fiber_bundle_layer_summary()

    def test_chapter_index_returns_dict(self):
        assert isinstance(fiber_bundle_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in fiber_bundle_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_contains_chapter_7(self):
        assert "7" in fiber_bundle_chapter_index()

    def test_chapter_index_contains_chapter_25(self):
        assert "25" in fiber_bundle_chapter_index()

    def test_chapter_index_product_bundle_in_chapter_7(self):
        assert "product_bundle" in fiber_bundle_chapter_index()["7"]

    def test_type_index_returns_dict(self):
        assert isinstance(fiber_bundle_type_index(), dict)

    def test_type_index_has_trivial(self):
        assert "trivial" in fiber_bundle_type_index()

    def test_type_index_has_principal_bundle(self):
        assert "principal_bundle" in fiber_bundle_type_index()

    def test_type_index_has_line_bundle(self):
        assert "line_bundle" in fiber_bundle_type_index()

    def test_type_index_all_types_in_profiles(self):
        all_types = {p.bundle_type for p in get_named_fiber_bundle_profiles()}
        assert set(fiber_bundle_type_index().keys()) == all_types


# ---------------------------------------------------------------------------
# is_locally_trivial
# ---------------------------------------------------------------------------

class TestIsLocallyTrivial:
    def test_fiber_bundle_tag_true(self):
        r = is_locally_trivial(_sp("fiber_bundle"))
        assert r.is_true

    def test_locally_trivial_tag_true(self):
        r = is_locally_trivial(_sp("locally_trivial"))
        assert r.is_true

    def test_vector_bundle_true(self):
        r = is_locally_trivial(_sp("vector_bundle"))
        assert r.is_true

    def test_line_bundle_true(self):
        r = is_locally_trivial(_sp("line_bundle"))
        assert r.is_true

    def test_tangent_bundle_true(self):
        r = is_locally_trivial(_sp("tangent_bundle"))
        assert r.is_true

    def test_principal_bundle_true(self):
        r = is_locally_trivial(_sp("principal_bundle"))
        assert r.is_true

    def test_frame_bundle_true(self):
        r = is_locally_trivial(_sp("frame_bundle"))
        assert r.is_true

    def test_hopf_bundle_true(self):
        r = is_locally_trivial(_sp("hopf_bundle"))
        assert r.is_true

    def test_mobius_band_true(self):
        r = is_locally_trivial(_sp("mobius_band"))
        assert r.is_true

    def test_trivial_bundle_true(self):
        r = is_locally_trivial(_sp("trivial_bundle"))
        assert r.is_true

    def test_tautological_bundle_true(self):
        r = is_locally_trivial(_sp("tautological_bundle"))
        assert r.is_true

    def test_normal_bundle_true(self):
        r = is_locally_trivial(_sp("normal_bundle"))
        assert r.is_true

    def test_empty_tags_unknown(self):
        r = is_locally_trivial(_sp())
        assert r.is_unknown

    def test_irrelevant_tags_unknown(self):
        r = is_locally_trivial(_sp("compact", "hausdorff"))
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(is_locally_trivial(_sp("vector_bundle")), Result)

    def test_true_has_justification(self):
        r = is_locally_trivial(_sp("vector_bundle"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_vector_bundle
# ---------------------------------------------------------------------------

class TestIsVectorBundle:
    def test_vector_bundle_tag_true(self):
        r = is_vector_bundle(_sp("vector_bundle"))
        assert r.is_true

    def test_line_bundle_true(self):
        r = is_vector_bundle(_sp("line_bundle"))
        assert r.is_true

    def test_real_vector_bundle_true(self):
        r = is_vector_bundle(_sp("real_vector_bundle"))
        assert r.is_true

    def test_complex_vector_bundle_true(self):
        r = is_vector_bundle(_sp("complex_vector_bundle"))
        assert r.is_true

    def test_tangent_bundle_true(self):
        r = is_vector_bundle(_sp("tangent_bundle"))
        assert r.is_true

    def test_cotangent_bundle_true(self):
        r = is_vector_bundle(_sp("cotangent_bundle"))
        assert r.is_true

    def test_mobius_band_true(self):
        r = is_vector_bundle(_sp("mobius_band"))
        assert r.is_true

    def test_tautological_bundle_true(self):
        r = is_vector_bundle(_sp("tautological_bundle"))
        assert r.is_true

    def test_normal_bundle_true(self):
        r = is_vector_bundle(_sp("normal_bundle"))
        assert r.is_true

    def test_hopf_bundle_false(self):
        r = is_vector_bundle(_sp("hopf_bundle"))
        assert r.is_false

    def test_principal_bundle_false(self):
        r = is_vector_bundle(_sp("principal_bundle"))
        assert r.is_false

    def test_frame_bundle_false(self):
        r = is_vector_bundle(_sp("frame_bundle"))
        assert r.is_false

    def test_principal_u1_bundle_false(self):
        r = is_vector_bundle(_sp("principal_u1_bundle"))
        assert r.is_false

    def test_empty_tags_unknown(self):
        r = is_vector_bundle(_sp())
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(is_vector_bundle(_sp("tangent_bundle")), Result)


# ---------------------------------------------------------------------------
# is_trivial_bundle
# ---------------------------------------------------------------------------

class TestIsTrivialBundle:
    def test_trivial_bundle_tag_true(self):
        r = is_trivial_bundle(_sp("trivial_bundle"))
        assert r.is_true

    def test_product_bundle_true(self):
        r = is_trivial_bundle(_sp("product_bundle"))
        assert r.is_true

    def test_parallelizable_true(self):
        r = is_trivial_bundle(_sp("parallelizable"))
        assert r.is_true

    def test_contractible_base_true(self):
        r = is_trivial_bundle(_sp("contractible_base"))
        assert r.is_true

    def test_mobius_band_false(self):
        r = is_trivial_bundle(_sp("mobius_band"))
        assert r.is_false

    def test_hopf_bundle_false(self):
        r = is_trivial_bundle(_sp("hopf_bundle"))
        assert r.is_false

    def test_tautological_bundle_false(self):
        r = is_trivial_bundle(_sp("tautological_bundle"))
        assert r.is_false

    def test_nontrivial_bundle_false(self):
        r = is_trivial_bundle(_sp("nontrivial_bundle"))
        assert r.is_false

    def test_non_parallelizable_tangent_false(self):
        r = is_trivial_bundle(_sp("non_parallelizable_tangent"))
        assert r.is_false

    def test_empty_tags_unknown(self):
        r = is_trivial_bundle(_sp())
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(is_trivial_bundle(_sp("trivial_bundle")), Result)

    def test_true_has_justification(self):
        r = is_trivial_bundle(_sp("trivial_bundle"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# has_nowhere_zero_section
# ---------------------------------------------------------------------------

class TestHasNowhereZeroSection:
    def test_trivial_bundle_true(self):
        r = has_nowhere_zero_section(_sp("trivial_bundle"))
        assert r.is_true

    def test_product_bundle_true(self):
        r = has_nowhere_zero_section(_sp("product_bundle"))
        assert r.is_true

    def test_parallelizable_true(self):
        r = has_nowhere_zero_section(_sp("parallelizable"))
        assert r.is_true

    def test_odd_sphere_tangent_true(self):
        r = has_nowhere_zero_section(_sp("odd_sphere_tangent"))
        assert r.is_true

    def test_sphere_s1_tangent_true(self):
        r = has_nowhere_zero_section(_sp("sphere_s1_tangent"))
        assert r.is_true

    def test_sphere_s3_tangent_true(self):
        r = has_nowhere_zero_section(_sp("sphere_s3_tangent"))
        assert r.is_true

    def test_sphere_s7_tangent_true(self):
        r = has_nowhere_zero_section(_sp("sphere_s7_tangent"))
        assert r.is_true

    def test_even_sphere_tangent_false(self):
        r = has_nowhere_zero_section(_sp("even_sphere_tangent"))
        assert r.is_false

    def test_sphere_s2_tangent_false(self):
        r = has_nowhere_zero_section(_sp("sphere_s2_tangent"))
        assert r.is_false

    def test_sphere_s4_tangent_false(self):
        r = has_nowhere_zero_section(_sp("sphere_s4_tangent"))
        assert r.is_false

    def test_mobius_band_false(self):
        r = has_nowhere_zero_section(_sp("mobius_band"))
        assert r.is_false

    def test_no_section_tag_false(self):
        r = has_nowhere_zero_section(_sp("no_nowhere_zero_section"))
        assert r.is_false

    def test_nonzero_euler_class_false(self):
        r = has_nowhere_zero_section(_sp("nonzero_euler_class"))
        assert r.is_false

    def test_empty_tags_unknown(self):
        r = has_nowhere_zero_section(_sp())
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(has_nowhere_zero_section(_sp("trivial_bundle")), Result)

    def test_hairy_ball_justification_contains_keyword(self):
        r = has_nowhere_zero_section(_sp("even_sphere_tangent"))
        assert any("ball" in j.lower() or "chi" in j.lower() or "Poincare" in j
                   or "chi" in j for j in r.justification)


# ---------------------------------------------------------------------------
# is_orientable_bundle
# ---------------------------------------------------------------------------

class TestIsOrientableBundle:
    def test_complex_vector_bundle_true(self):
        r = is_orientable_bundle(_sp("complex_vector_bundle"))
        assert r.is_true

    def test_trivial_bundle_true(self):
        r = is_orientable_bundle(_sp("trivial_bundle"))
        assert r.is_true

    def test_product_bundle_true(self):
        r = is_orientable_bundle(_sp("product_bundle"))
        assert r.is_true

    def test_orientable_bundle_tag_true(self):
        r = is_orientable_bundle(_sp("orientable_bundle"))
        assert r.is_true

    def test_w1_zero_true(self):
        r = is_orientable_bundle(_sp("w1_zero"))
        assert r.is_true

    def test_sphere_tangent_bundle_true(self):
        r = is_orientable_bundle(_sp("sphere_tangent_bundle"))
        assert r.is_true

    def test_mobius_band_false(self):
        r = is_orientable_bundle(_sp("mobius_band"))
        assert r.is_false

    def test_w1_nonzero_false(self):
        r = is_orientable_bundle(_sp("w1_nonzero"))
        assert r.is_false

    def test_non_orientable_bundle_false(self):
        r = is_orientable_bundle(_sp("non_orientable_bundle"))
        assert r.is_false

    def test_empty_tags_unknown(self):
        r = is_orientable_bundle(_sp())
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(is_orientable_bundle(_sp("trivial_bundle")), Result)

    def test_true_has_justification(self):
        r = is_orientable_bundle(_sp("complex_vector_bundle"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# classify_bundle
# ---------------------------------------------------------------------------

class TestClassifyBundle:
    def test_returns_dict(self):
        assert isinstance(classify_bundle(_sp()), dict)

    def test_has_bundle_class_key(self):
        assert "bundle_class" in classify_bundle(_sp())

    def test_has_is_locally_trivial_key(self):
        assert "is_locally_trivial" in classify_bundle(_sp())

    def test_has_is_vector_bundle_key(self):
        assert "is_vector_bundle" in classify_bundle(_sp())

    def test_has_is_trivial_bundle_key(self):
        assert "is_trivial_bundle" in classify_bundle(_sp())

    def test_has_has_nowhere_zero_section_key(self):
        assert "has_nowhere_zero_section" in classify_bundle(_sp())

    def test_has_is_orientable_bundle_key(self):
        assert "is_orientable_bundle" in classify_bundle(_sp())

    def test_has_key_properties(self):
        assert "key_properties" in classify_bundle(_sp())

    def test_key_properties_is_list(self):
        assert isinstance(classify_bundle(_sp())["key_properties"], list)

    def test_trivial_bundle_class(self):
        r = classify_bundle(_sp("trivial_bundle"))
        assert r["bundle_class"] == "trivial"

    def test_vector_bundle_class(self):
        r = classify_bundle(_sp("tangent_bundle"))
        assert r["bundle_class"] == "vector_bundle"

    def test_principal_bundle_class_hopf(self):
        r = classify_bundle(_sp("hopf_bundle"))
        assert r["bundle_class"] == "principal"

    def test_principal_bundle_class_frame(self):
        r = classify_bundle(_sp("frame_bundle"))
        assert r["bundle_class"] == "principal"

    def test_unknown_class_empty(self):
        r = classify_bundle(_sp())
        assert r["bundle_class"] == "unknown"

    def test_trivial_key_properties_contains_trivial(self):
        r = classify_bundle(_sp("trivial_bundle"))
        assert "trivial" in r["key_properties"]

    def test_trivial_key_properties_contains_locally_trivial(self):
        r = classify_bundle(_sp("trivial_bundle"))
        assert "locally_trivial" in r["key_properties"]

    def test_mobius_key_properties_contains_non_trivial(self):
        r = classify_bundle(_sp("mobius_band"))
        assert "non_trivial" in r["key_properties"]

    def test_mobius_key_properties_contains_non_orientable(self):
        r = classify_bundle(_sp("mobius_band"))
        assert "non_orientable" in r["key_properties"]

    def test_representation_in_output(self):
        assert "representation" in classify_bundle(_sp())

    def test_tags_in_output(self):
        assert "tags" in classify_bundle(_sp("vector_bundle"))

    def test_tags_is_list(self):
        assert isinstance(classify_bundle(_sp("tangent_bundle"))["tags"], list)

    def test_principal_bundle_in_key_props_for_frame(self):
        r = classify_bundle(_sp("frame_bundle"))
        assert "principal_bundle" in r["key_properties"]


# ---------------------------------------------------------------------------
# fiber_bundle_profile
# ---------------------------------------------------------------------------

class TestFiberBundleProfile:
    def test_returns_dict(self):
        assert isinstance(fiber_bundle_profile(_sp()), dict)

    def test_has_classification_key(self):
        assert "classification" in fiber_bundle_profile(_sp())

    def test_has_named_profiles_key(self):
        assert "named_profiles" in fiber_bundle_profile(_sp())

    def test_has_layer_summary_key(self):
        assert "layer_summary" in fiber_bundle_profile(_sp())

    def test_named_profiles_is_tuple(self):
        p = fiber_bundle_profile(_sp())
        assert isinstance(p["named_profiles"], tuple)

    def test_classification_has_bundle_class(self):
        p = fiber_bundle_profile(_sp("vector_bundle"))
        assert "bundle_class" in p["classification"]

    def test_layer_summary_is_dict(self):
        assert isinstance(fiber_bundle_profile(_sp())["layer_summary"], dict)

    def test_trivial_classification_correct(self):
        p = fiber_bundle_profile(_sp("trivial_bundle"))
        assert p["classification"]["bundle_class"] == "trivial"

    def test_vector_bundle_classification_correct(self):
        p = fiber_bundle_profile(_sp("tangent_bundle"))
        assert p["classification"]["bundle_class"] == "vector_bundle"
