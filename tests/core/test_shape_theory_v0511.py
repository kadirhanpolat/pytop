"""Tests for shape_theory.py (v0.5.11)."""

import pytest

from pytop.shape_theory import (
    ANR_POSITIVE_TAGS,
    CECH_COMPUTABLE_TAGS,
    FANR_POSITIVE_TAGS,
    MOVABLE_POSITIVE_TAGS,
    NOT_ANR_TAGS,
    NOT_FANR_TAGS,
    NOT_MOVABLE_TAGS,
    SHAPE_TRIVIAL_TAGS,
    ShapeProfile,
    cech_cohomology_applicable,
    classify_shape,
    get_named_shape_profiles,
    has_trivial_shape,
    is_anr,
    is_fanr,
    is_movable,
    shape_chapter_index,
    shape_layer_summary,
    shape_profile,
    shape_type_index,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_anr_tags_contains_anr(self):
        assert "anr" in ANR_POSITIVE_TAGS

    def test_anr_tags_contains_ar(self):
        assert "ar" in ANR_POSITIVE_TAGS

    def test_anr_tags_contains_compact_manifold(self):
        assert "compact_manifold" in ANR_POSITIVE_TAGS

    def test_anr_tags_contains_finite_cw_complex(self):
        assert "finite_cw_complex" in ANR_POSITIVE_TAGS

    def test_anr_tags_contains_compact_polyhedron(self):
        assert "compact_polyhedron" in ANR_POSITIVE_TAGS

    def test_anr_tags_contains_sphere(self):
        assert "sphere" in ANR_POSITIVE_TAGS

    def test_anr_tags_contains_torus(self):
        assert "torus" in ANR_POSITIVE_TAGS

    def test_fanr_tags_contains_fanr(self):
        assert "fanr" in FANR_POSITIVE_TAGS

    def test_fanr_tags_contains_anr(self):
        assert "anr" in FANR_POSITIVE_TAGS

    def test_fanr_tags_contains_compact_polyhedron(self):
        assert "compact_polyhedron" in FANR_POSITIVE_TAGS

    def test_movable_tags_contains_movable(self):
        assert "movable" in MOVABLE_POSITIVE_TAGS

    def test_movable_tags_contains_fanr(self):
        assert "fanr" in MOVABLE_POSITIVE_TAGS

    def test_movable_tags_contains_peano_continuum(self):
        assert "peano_continuum" in MOVABLE_POSITIVE_TAGS

    def test_movable_tags_contains_hawaiian_earring(self):
        assert "hawaiian_earring" in MOVABLE_POSITIVE_TAGS

    def test_shape_trivial_tags_contains_contractible(self):
        assert "contractible" in SHAPE_TRIVIAL_TAGS

    def test_shape_trivial_tags_contains_ar(self):
        assert "ar" in SHAPE_TRIVIAL_TAGS

    def test_shape_trivial_tags_contains_closed_ball(self):
        assert "closed_ball" in SHAPE_TRIVIAL_TAGS

    def test_shape_trivial_tags_contains_hilbert_cube(self):
        assert "hilbert_cube" in SHAPE_TRIVIAL_TAGS

    def test_cech_tags_contains_compact_metrizable(self):
        assert "compact_metrizable" in CECH_COMPUTABLE_TAGS

    def test_cech_tags_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in CECH_COMPUTABLE_TAGS

    def test_cech_tags_contains_compact_polyhedron(self):
        assert "compact_polyhedron" in CECH_COMPUTABLE_TAGS

    def test_not_anr_tags_contains_warsaw_circle(self):
        assert "warsaw_circle" in NOT_ANR_TAGS

    def test_not_anr_tags_contains_solenoid(self):
        assert "solenoid" in NOT_ANR_TAGS

    def test_not_anr_tags_contains_hawaiian_earring(self):
        assert "hawaiian_earring" in NOT_ANR_TAGS

    def test_not_fanr_tags_contains_solenoid(self):
        assert "solenoid" in NOT_FANR_TAGS

    def test_not_fanr_tags_contains_warsaw_circle(self):
        assert "warsaw_circle" in NOT_FANR_TAGS

    def test_not_fanr_tags_contains_hawaiian_earring(self):
        assert "hawaiian_earring" in NOT_FANR_TAGS

    def test_not_movable_tags_contains_warsaw_circle(self):
        assert "warsaw_circle" in NOT_MOVABLE_TAGS

    def test_not_movable_tags_contains_solenoid(self):
        assert "solenoid" in NOT_MOVABLE_TAGS

    def test_tag_sets_are_sets(self):
        for s in [ANR_POSITIVE_TAGS, FANR_POSITIVE_TAGS, MOVABLE_POSITIVE_TAGS,
                  SHAPE_TRIVIAL_TAGS, CECH_COMPUTABLE_TAGS,
                  NOT_ANR_TAGS, NOT_FANR_TAGS, NOT_MOVABLE_TAGS]:
            assert isinstance(s, set)

    def test_hawaiian_earring_not_in_anr_positive_tags(self):
        assert "hawaiian_earring" not in ANR_POSITIVE_TAGS

    def test_warsaw_circle_not_in_movable_tags(self):
        assert "warsaw_circle" not in MOVABLE_POSITIVE_TAGS

    def test_solenoid_not_in_movable_tags(self):
        assert "solenoid" not in MOVABLE_POSITIVE_TAGS


# ---------------------------------------------------------------------------
# ShapeProfile dataclass
# ---------------------------------------------------------------------------

class TestShapeProfileDataclass:
    def test_profile_is_frozen(self):
        p = ShapeProfile(
            key="test", display_name="Test", shape_type="anr",
            is_anr=True, is_fanr=True, is_movable=True, is_shape_trivial=False,
            presentation_layer="main_text", focus="test focus",
            chapter_targets=("6",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields_accessible(self):
        p = ShapeProfile(
            key="k", display_name="D", shape_type="movable",
            is_anr=False, is_fanr=False, is_movable=True, is_shape_trivial=False,
            presentation_layer="selected_block", focus="f",
            chapter_targets=("23", "48"),
        )
        assert p.key == "k"
        assert p.is_movable is True
        assert p.is_anr is False
        assert p.chapter_targets == ("23", "48")

    def test_profile_equality(self):
        kwargs = dict(
            key="a", display_name="A", shape_type="anr",
            is_anr=True, is_fanr=True, is_movable=True, is_shape_trivial=False,
            presentation_layer="main_text", focus="f", chapter_targets=("6",),
        )
        assert ShapeProfile(**kwargs) == ShapeProfile(**kwargs)


# ---------------------------------------------------------------------------
# Named profiles registry
# ---------------------------------------------------------------------------

class TestNamedShapeProfiles:
    def setup_method(self):
        self.profiles = get_named_shape_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_five_profiles(self):
        assert len(self.profiles) >= 5

    def test_all_are_shape_profiles(self):
        for p in self.profiles:
            assert isinstance(p, ShapeProfile)

    def test_keys_are_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_compact_polyhedron_profile_exists(self):
        keys = {p.key for p in self.profiles}
        assert "compact_polyhedron" in keys

    def test_compact_ar_profile_exists(self):
        keys = {p.key for p in self.profiles}
        assert "compact_ar" in keys

    def test_warsaw_circle_profile_exists(self):
        keys = {p.key for p in self.profiles}
        assert "warsaw_circle" in keys

    def test_solenoid_profile_exists(self):
        keys = {p.key for p in self.profiles}
        assert "solenoid" in keys

    def test_hawaiian_earring_profile_exists(self):
        keys = {p.key for p in self.profiles}
        assert "hawaiian_earring" in keys

    def test_compact_polyhedron_is_anr(self):
        p = next(x for x in self.profiles if x.key == "compact_polyhedron")
        assert p.is_anr is True

    def test_compact_polyhedron_is_fanr(self):
        p = next(x for x in self.profiles if x.key == "compact_polyhedron")
        assert p.is_fanr is True

    def test_compact_polyhedron_is_movable(self):
        p = next(x for x in self.profiles if x.key == "compact_polyhedron")
        assert p.is_movable is True

    def test_compact_ar_has_trivial_shape(self):
        p = next(x for x in self.profiles if x.key == "compact_ar")
        assert p.is_shape_trivial is True

    def test_compact_ar_is_anr(self):
        p = next(x for x in self.profiles if x.key == "compact_ar")
        assert p.is_anr is True

    def test_warsaw_circle_not_anr(self):
        p = next(x for x in self.profiles if x.key == "warsaw_circle")
        assert p.is_anr is False

    def test_warsaw_circle_not_fanr(self):
        p = next(x for x in self.profiles if x.key == "warsaw_circle")
        assert p.is_fanr is False

    def test_warsaw_circle_not_movable(self):
        p = next(x for x in self.profiles if x.key == "warsaw_circle")
        assert p.is_movable is False

    def test_solenoid_not_anr(self):
        p = next(x for x in self.profiles if x.key == "solenoid")
        assert p.is_anr is False

    def test_solenoid_not_fanr(self):
        p = next(x for x in self.profiles if x.key == "solenoid")
        assert p.is_fanr is False

    def test_solenoid_not_movable(self):
        p = next(x for x in self.profiles if x.key == "solenoid")
        assert p.is_movable is False

    def test_hawaiian_earring_not_anr(self):
        p = next(x for x in self.profiles if x.key == "hawaiian_earring")
        assert p.is_anr is False

    def test_hawaiian_earring_not_fanr(self):
        p = next(x for x in self.profiles if x.key == "hawaiian_earring")
        assert p.is_fanr is False

    def test_hawaiian_earring_is_movable(self):
        p = next(x for x in self.profiles if x.key == "hawaiian_earring")
        assert p.is_movable is True

    def test_hawaiian_earring_not_shape_trivial(self):
        p = next(x for x in self.profiles if x.key == "hawaiian_earring")
        assert p.is_shape_trivial is False

    def test_all_profiles_have_nonempty_focus(self):
        for p in self.profiles:
            assert len(p.focus) > 20

    def test_all_profiles_have_chapter_targets(self):
        for p in self.profiles:
            assert len(p.chapter_targets) >= 1

    def test_all_presentation_layers_valid(self):
        valid = {"main_text", "selected_block", "appendix", "exercise"}
        for p in self.profiles:
            assert p.presentation_layer in valid

    def test_anr_implies_fanr_in_profiles(self):
        for p in self.profiles:
            if p.is_anr:
                assert p.is_fanr

    def test_fanr_implies_movable_in_profiles(self):
        for p in self.profiles:
            if p.is_fanr:
                assert p.is_movable

    def test_shape_trivial_implies_anr_in_profiles(self):
        for p in self.profiles:
            if p.is_shape_trivial:
                assert p.is_anr


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(shape_layer_summary(), dict)

    def test_layer_summary_values_are_ints(self):
        for v in shape_layer_summary().values():
            assert isinstance(v, int)

    def test_layer_summary_sum_equals_profile_count(self):
        total = sum(shape_layer_summary().values())
        assert total == len(get_named_shape_profiles())

    def test_layer_summary_has_main_text(self):
        assert "main_text" in shape_layer_summary()

    def test_chapter_index_returns_dict(self):
        assert isinstance(shape_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in shape_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_contains_chapter_6(self):
        assert "6" in shape_chapter_index()

    def test_chapter_index_contains_chapter_23(self):
        assert "23" in shape_chapter_index()

    def test_chapter_index_compact_polyhedron_in_chapter_6(self):
        assert "compact_polyhedron" in shape_chapter_index()["6"]

    def test_type_index_returns_dict(self):
        assert isinstance(shape_type_index(), dict)

    def test_type_index_has_anr_key(self):
        assert "anr" in shape_type_index()

    def test_type_index_has_not_movable_key(self):
        assert "not_movable" in shape_type_index()

    def test_type_index_has_movable_key(self):
        assert "movable" in shape_type_index()

    def test_type_index_has_shape_trivial_key(self):
        assert "shape_trivial" in shape_type_index()

    def test_type_index_all_keys_appear_in_profiles(self):
        all_types = {p.shape_type for p in get_named_shape_profiles()}
        assert set(shape_type_index().keys()) == all_types


# ---------------------------------------------------------------------------
# is_anr
# ---------------------------------------------------------------------------

class TestIsAnr:
    def test_explicit_anr_tag_true(self):
        r = is_anr(_sp("anr"))
        assert r.is_true

    def test_explicit_ar_tag_true(self):
        r = is_anr(_sp("ar"))
        assert r.is_true

    def test_absolute_retract_tag_true(self):
        r = is_anr(_sp("absolute_retract"))
        assert r.is_true

    def test_compact_manifold_true(self):
        r = is_anr(_sp("compact_manifold"))
        assert r.is_true

    def test_sphere_true(self):
        r = is_anr(_sp("sphere"))
        assert r.is_true

    def test_torus_true(self):
        r = is_anr(_sp("torus"))
        assert r.is_true

    def test_compact_surface_true(self):
        r = is_anr(_sp("compact_surface"))
        assert r.is_true

    def test_finite_cw_complex_true(self):
        r = is_anr(_sp("finite_cw_complex"))
        assert r.is_true

    def test_compact_polyhedron_true(self):
        r = is_anr(_sp("compact_polyhedron"))
        assert r.is_true

    def test_locally_contractible_true(self):
        r = is_anr(_sp("locally_contractible"))
        assert r.is_true

    def test_locally_contractible_compact_true(self):
        r = is_anr(_sp("locally_contractible_compact"))
        assert r.is_true

    def test_warsaw_circle_false(self):
        r = is_anr(_sp("warsaw_circle"))
        assert r.is_false

    def test_solenoid_false(self):
        r = is_anr(_sp("solenoid"))
        assert r.is_false

    def test_hawaiian_earring_false(self):
        r = is_anr(_sp("hawaiian_earring"))
        assert r.is_false

    def test_not_locally_contractible_false(self):
        r = is_anr(_sp("not_locally_contractible"))
        assert r.is_false

    def test_empty_tags_unknown(self):
        r = is_anr(_sp())
        assert r.is_unknown

    def test_irrelevant_tags_unknown(self):
        r = is_anr(_sp("hausdorff", "metrizable"))
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(is_anr(_sp("anr")), Result)

    def test_true_result_has_justification(self):
        r = is_anr(_sp("compact_manifold"))
        assert len(r.justification) > 0

    def test_false_result_has_justification(self):
        r = is_anr(_sp("warsaw_circle"))
        assert len(r.justification) > 0

    def test_compact_lie_group_true(self):
        r = is_anr(_sp("compact_lie_group"))
        assert r.is_true

    def test_projective_space_true(self):
        r = is_anr(_sp("projective_space"))
        assert r.is_true


# ---------------------------------------------------------------------------
# is_fanr
# ---------------------------------------------------------------------------

class TestIsFanr:
    def test_fanr_tag_true(self):
        r = is_fanr(_sp("fanr"))
        assert r.is_true

    def test_anr_tag_true(self):
        r = is_fanr(_sp("anr"))
        assert r.is_true

    def test_ar_tag_true(self):
        r = is_fanr(_sp("ar"))
        assert r.is_true

    def test_compact_polyhedron_true(self):
        r = is_fanr(_sp("compact_polyhedron"))
        assert r.is_true

    def test_compact_manifold_true(self):
        r = is_fanr(_sp("compact_manifold"))
        assert r.is_true

    def test_finite_cw_complex_true(self):
        r = is_fanr(_sp("finite_cw_complex"))
        assert r.is_true

    def test_hawaiian_earring_false(self):
        r = is_fanr(_sp("hawaiian_earring"))
        assert r.is_false

    def test_solenoid_false(self):
        r = is_fanr(_sp("solenoid"))
        assert r.is_false

    def test_warsaw_circle_false(self):
        r = is_fanr(_sp("warsaw_circle"))
        assert r.is_false

    def test_not_fanr_tag_false(self):
        r = is_fanr(_sp("not_fanr"))
        assert r.is_false

    def test_empty_tags_unknown(self):
        r = is_fanr(_sp())
        assert r.is_unknown

    def test_peano_continuum_alone_unknown(self):
        # peano_continuum is movable but not explicitly FANR
        r = is_fanr(_sp("peano_continuum"))
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(is_fanr(_sp("anr")), Result)


# ---------------------------------------------------------------------------
# is_movable
# ---------------------------------------------------------------------------

class TestIsMovable:
    def test_movable_tag_true(self):
        r = is_movable(_sp("movable"))
        assert r.is_true

    def test_fanr_tag_true(self):
        r = is_movable(_sp("fanr"))
        assert r.is_true

    def test_anr_tag_true(self):
        r = is_movable(_sp("anr"))
        assert r.is_true

    def test_ar_tag_true(self):
        r = is_movable(_sp("ar"))
        assert r.is_true

    def test_compact_polyhedron_true(self):
        r = is_movable(_sp("compact_polyhedron"))
        assert r.is_true

    def test_compact_manifold_true(self):
        r = is_movable(_sp("compact_manifold"))
        assert r.is_true

    def test_sphere_true(self):
        r = is_movable(_sp("sphere"))
        assert r.is_true

    def test_torus_true(self):
        r = is_movable(_sp("torus"))
        assert r.is_true

    def test_peano_continuum_true(self):
        r = is_movable(_sp("peano_continuum"))
        assert r.is_true

    def test_hawaiian_earring_true(self):
        r = is_movable(_sp("hawaiian_earring"))
        assert r.is_true

    def test_locally_path_connected_compact_true(self):
        r = is_movable(_sp("locally_path_connected_compact"))
        assert r.is_true

    def test_warsaw_circle_false(self):
        r = is_movable(_sp("warsaw_circle"))
        assert r.is_false

    def test_solenoid_false(self):
        r = is_movable(_sp("solenoid"))
        assert r.is_false

    def test_dyadic_solenoid_false(self):
        r = is_movable(_sp("dyadic_solenoid"))
        assert r.is_false

    def test_not_movable_tag_false(self):
        r = is_movable(_sp("not_movable"))
        assert r.is_false

    def test_empty_tags_unknown(self):
        r = is_movable(_sp())
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(is_movable(_sp("movable")), Result)

    def test_compact_surface_true(self):
        r = is_movable(_sp("compact_surface"))
        assert r.is_true

    def test_true_result_has_justification(self):
        r = is_movable(_sp("peano_continuum"))
        assert "Borsuk" in r.justification[0] or "Peano" in r.justification[0]


# ---------------------------------------------------------------------------
# has_trivial_shape
# ---------------------------------------------------------------------------

class TestHasTrivialShape:
    def test_contractible_tag_true(self):
        r = has_trivial_shape(_sp("contractible"))
        assert r.is_true

    def test_ar_tag_true(self):
        r = has_trivial_shape(_sp("ar"))
        assert r.is_true

    def test_closed_ball_true(self):
        r = has_trivial_shape(_sp("closed_ball"))
        assert r.is_true

    def test_hilbert_cube_true(self):
        r = has_trivial_shape(_sp("hilbert_cube"))
        assert r.is_true

    def test_single_point_true(self):
        r = has_trivial_shape(_sp("single_point"))
        assert r.is_true

    def test_convex_compact_true(self):
        r = has_trivial_shape(_sp("convex_compact"))
        assert r.is_true

    def test_contractible_compact_true(self):
        r = has_trivial_shape(_sp("contractible_compact"))
        assert r.is_true

    def test_sphere_false(self):
        r = has_trivial_shape(_sp("sphere"))
        assert r.is_false

    def test_torus_false(self):
        r = has_trivial_shape(_sp("torus"))
        assert r.is_false

    def test_warsaw_circle_false(self):
        r = has_trivial_shape(_sp("warsaw_circle"))
        assert r.is_false

    def test_solenoid_false(self):
        r = has_trivial_shape(_sp("solenoid"))
        assert r.is_false

    def test_hawaiian_earring_false(self):
        r = has_trivial_shape(_sp("hawaiian_earring"))
        assert r.is_false

    def test_not_contractible_false(self):
        r = has_trivial_shape(_sp("not_contractible"))
        assert r.is_false

    def test_not_anr_false(self):
        r = has_trivial_shape(_sp("not_locally_contractible"))
        assert r.is_false

    def test_empty_tags_unknown(self):
        r = has_trivial_shape(_sp())
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(has_trivial_shape(_sp("ar")), Result)

    def test_projective_space_false(self):
        r = has_trivial_shape(_sp("projective_space"))
        assert r.is_false


# ---------------------------------------------------------------------------
# cech_cohomology_applicable
# ---------------------------------------------------------------------------

class TestCechCohomologyApplicable:
    def test_compact_polyhedron_true(self):
        r = cech_cohomology_applicable(_sp("compact_polyhedron"))
        assert r.is_true

    def test_compact_manifold_true(self):
        r = cech_cohomology_applicable(_sp("compact_manifold"))
        assert r.is_true

    def test_anr_tag_true(self):
        r = cech_cohomology_applicable(_sp("anr"))
        assert r.is_true

    def test_ar_tag_true(self):
        r = cech_cohomology_applicable(_sp("ar"))
        assert r.is_true

    def test_finite_cw_complex_true(self):
        r = cech_cohomology_applicable(_sp("finite_cw_complex"))
        assert r.is_true

    def test_compact_metrizable_true(self):
        r = cech_cohomology_applicable(_sp("compact_metrizable"))
        assert r.is_true

    def test_compact_metric_true(self):
        r = cech_cohomology_applicable(_sp("compact_metric"))
        assert r.is_true

    def test_compact_hausdorff_true(self):
        r = cech_cohomology_applicable(_sp("compact_hausdorff"))
        assert r.is_true

    def test_paracompact_hausdorff_true(self):
        r = cech_cohomology_applicable(_sp("paracompact_hausdorff"))
        assert r.is_true

    def test_locally_compact_hausdorff_true(self):
        r = cech_cohomology_applicable(_sp("locally_compact_hausdorff"))
        assert r.is_true

    def test_locally_compact_metrizable_true(self):
        r = cech_cohomology_applicable(_sp("locally_compact_metrizable"))
        assert r.is_true

    def test_empty_tags_unknown(self):
        r = cech_cohomology_applicable(_sp())
        assert r.is_unknown

    def test_returns_result_instance(self):
        assert isinstance(cech_cohomology_applicable(_sp("compact_metrizable")), Result)

    def test_true_result_has_justification(self):
        r = cech_cohomology_applicable(_sp("compact_polyhedron"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# classify_shape
# ---------------------------------------------------------------------------

class TestClassifyShape:
    def test_returns_dict(self):
        assert isinstance(classify_shape(_sp()), dict)

    def test_has_shape_class_key(self):
        assert "shape_class" in classify_shape(_sp("compact_polyhedron"))

    def test_has_is_anr_key(self):
        assert "is_anr" in classify_shape(_sp())

    def test_has_is_fanr_key(self):
        assert "is_fanr" in classify_shape(_sp())

    def test_has_is_movable_key(self):
        assert "is_movable" in classify_shape(_sp())

    def test_has_has_trivial_shape_key(self):
        assert "has_trivial_shape" in classify_shape(_sp())

    def test_has_cech_applicable_key(self):
        assert "cech_applicable" in classify_shape(_sp())

    def test_has_key_properties_key(self):
        assert "key_properties" in classify_shape(_sp())

    def test_key_properties_is_list(self):
        assert isinstance(classify_shape(_sp())["key_properties"], list)

    def test_compact_ar_class_shape_trivial(self):
        r = classify_shape(_sp("ar"))
        assert r["shape_class"] == "shape_trivial"

    def test_compact_polyhedron_class_anr(self):
        r = classify_shape(_sp("compact_polyhedron"))
        assert r["shape_class"] == "anr"

    def test_warsaw_circle_class_not_movable(self):
        r = classify_shape(_sp("warsaw_circle"))
        assert r["shape_class"] == "not_movable"

    def test_solenoid_class_not_movable(self):
        r = classify_shape(_sp("solenoid"))
        assert r["shape_class"] == "not_movable"

    def test_hawaiian_earring_class_movable(self):
        r = classify_shape(_sp("hawaiian_earring"))
        assert r["shape_class"] == "movable"

    def test_peano_continuum_class_movable(self):
        r = classify_shape(_sp("peano_continuum"))
        assert r["shape_class"] == "movable"

    def test_compact_ar_key_properties_contains_trivial_shape(self):
        r = classify_shape(_sp("ar"))
        assert "trivial_shape" in r["key_properties"]

    def test_compact_polyhedron_key_properties_contains_anr(self):
        r = classify_shape(_sp("compact_polyhedron"))
        assert "anr" in r["key_properties"]

    def test_warsaw_circle_key_properties_contains_not_movable(self):
        r = classify_shape(_sp("warsaw_circle"))
        assert "not_movable" in r["key_properties"]

    def test_hawaiian_earring_key_properties_contains_movable(self):
        r = classify_shape(_sp("hawaiian_earring"))
        assert "movable" in r["key_properties"]

    def test_unknown_class_for_empty_tags(self):
        r = classify_shape(_sp())
        assert r["shape_class"] == "unknown"

    def test_representation_in_output(self):
        assert "representation" in classify_shape(_sp())

    def test_tags_in_output(self):
        assert "tags" in classify_shape(_sp("compact_manifold"))

    def test_tags_is_list(self):
        assert isinstance(classify_shape(_sp("anr"))["tags"], list)

    def test_cech_applicable_in_key_properties_for_polyhedron(self):
        r = classify_shape(_sp("compact_polyhedron"))
        assert "cech_cohomology_applicable" in r["key_properties"]


# ---------------------------------------------------------------------------
# shape_profile
# ---------------------------------------------------------------------------

class TestShapeProfile:
    def test_returns_dict(self):
        assert isinstance(shape_profile(_sp()), dict)

    def test_has_classification_key(self):
        assert "classification" in shape_profile(_sp())

    def test_has_named_profiles_key(self):
        assert "named_profiles" in shape_profile(_sp())

    def test_has_layer_summary_key(self):
        assert "layer_summary" in shape_profile(_sp())

    def test_named_profiles_are_tuple(self):
        p = shape_profile(_sp())
        assert isinstance(p["named_profiles"], tuple)

    def test_classification_has_shape_class(self):
        p = shape_profile(_sp("compact_manifold"))
        assert "shape_class" in p["classification"]

    def test_layer_summary_is_dict(self):
        p = shape_profile(_sp())
        assert isinstance(p["layer_summary"], dict)

    def test_anr_space_classification_correct(self):
        p = shape_profile(_sp("compact_manifold"))
        assert p["classification"]["shape_class"] == "anr"

    def test_shape_trivial_classification_correct(self):
        p = shape_profile(_sp("contractible"))
        assert p["classification"]["shape_class"] == "shape_trivial"
