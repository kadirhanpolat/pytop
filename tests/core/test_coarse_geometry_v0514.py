"""Tests for coarse_geometry.py (v0.5.14)."""

import pytest

from pytop.coarse_geometry import (
    EXPONENTIAL_GROWTH_TAGS,
    FINITE_ASYMPTOTIC_DIM_TAGS,
    HYPERBOLIC_TAGS,
    INFINITE_ENDS_TAGS,
    NOT_PROPERTY_A_TAGS,
    ONE_END_TAGS,
    POLYNOMIAL_GROWTH_TAGS,
    PROPERTY_A_TAGS,
    TWO_ENDS_TAGS,
    CoarseGeometryProfile,
    classify_coarse_geometry,
    coarse_geometry_chapter_index,
    coarse_geometry_layer_summary,
    coarse_geometry_profile,
    coarse_geometry_type_index,
    coarsely_embeds_in_hilbert,
    get_named_coarse_geometry_profiles,
    has_finite_asymptotic_dimension,
    has_property_a,
    is_gromov_hyperbolic,
    is_quasi_isometric_to_euclidean,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_finite_asdim_contains_virtually_abelian(self):
        assert "virtually_abelian" in FINITE_ASYMPTOTIC_DIM_TAGS

    def test_finite_asdim_contains_free_group(self):
        assert "free_group" in FINITE_ASYMPTOTIC_DIM_TAGS

    def test_finite_asdim_contains_hyperbolic_group(self):
        assert "hyperbolic_group" in FINITE_ASYMPTOTIC_DIM_TAGS

    def test_finite_asdim_contains_z_lattice(self):
        assert "z_lattice" in FINITE_ASYMPTOTIC_DIM_TAGS

    def test_finite_asdim_contains_euclidean_lattice(self):
        assert "euclidean_lattice" in FINITE_ASYMPTOTIC_DIM_TAGS

    def test_property_a_contains_property_a(self):
        assert "property_a" in PROPERTY_A_TAGS

    def test_property_a_contains_amenable_group(self):
        assert "amenable_group" in PROPERTY_A_TAGS

    def test_property_a_contains_hyperbolic_group(self):
        assert "hyperbolic_group" in PROPERTY_A_TAGS

    def test_property_a_contains_free_group(self):
        assert "free_group" in PROPERTY_A_TAGS

    def test_property_a_contains_linear_group(self):
        assert "linear_group" in PROPERTY_A_TAGS

    def test_hyperbolic_contains_gromov_hyperbolic(self):
        assert "gromov_hyperbolic" in HYPERBOLIC_TAGS

    def test_hyperbolic_contains_free_group(self):
        assert "free_group" in HYPERBOLIC_TAGS

    def test_hyperbolic_contains_hyperbolic_space(self):
        assert "hyperbolic_space" in HYPERBOLIC_TAGS

    def test_hyperbolic_contains_cat_negative_curvature(self):
        assert "cat_negative_curvature" in HYPERBOLIC_TAGS

    def test_polynomial_growth_contains_virtually_nilpotent(self):
        assert "virtually_nilpotent" in POLYNOMIAL_GROWTH_TAGS

    def test_polynomial_growth_contains_heisenberg_group(self):
        assert "heisenberg_group" in POLYNOMIAL_GROWTH_TAGS

    def test_polynomial_growth_contains_z_lattice(self):
        assert "z_lattice" in POLYNOMIAL_GROWTH_TAGS

    def test_exponential_growth_contains_free_group(self):
        assert "free_group" in EXPONENTIAL_GROWTH_TAGS

    def test_exponential_growth_contains_hyperbolic_group(self):
        assert "hyperbolic_group" in EXPONENTIAL_GROWTH_TAGS

    def test_two_ends_contains_virtually_z(self):
        assert "virtually_z" in TWO_ENDS_TAGS

    def test_two_ends_contains_integer_group(self):
        assert "integer_group" in TWO_ENDS_TAGS

    def test_infinite_ends_contains_free_group(self):
        assert "free_group" in INFINITE_ENDS_TAGS

    def test_infinite_ends_contains_free_product_nontrivial(self):
        assert "free_product_nontrivial" in INFINITE_ENDS_TAGS

    def test_one_end_contains_one_end(self):
        assert "one_end" in ONE_END_TAGS

    def test_one_end_contains_heisenberg_group(self):
        assert "heisenberg_group" in ONE_END_TAGS

    def test_not_property_a_contains_expander_graph(self):
        assert "expander_graph" in NOT_PROPERTY_A_TAGS

    def test_not_property_a_contains_expander_family(self):
        assert "expander_family" in NOT_PROPERTY_A_TAGS

    def test_not_property_a_contains_no_coarse_embedding_hilbert(self):
        assert "no_coarse_embedding_hilbert" in NOT_PROPERTY_A_TAGS

    def test_all_tag_constants_are_sets(self):
        for s in [FINITE_ASYMPTOTIC_DIM_TAGS, PROPERTY_A_TAGS, HYPERBOLIC_TAGS,
                  POLYNOMIAL_GROWTH_TAGS, EXPONENTIAL_GROWTH_TAGS, TWO_ENDS_TAGS,
                  INFINITE_ENDS_TAGS, ONE_END_TAGS, NOT_PROPERTY_A_TAGS]:
            assert isinstance(s, frozenset)

    def test_not_property_a_and_property_a_disjoint(self):
        # expander_family is in NOT_PROPERTY_A but not in PROPERTY_A
        assert "expander_family" not in PROPERTY_A_TAGS


# ---------------------------------------------------------------------------
# CoarseGeometryProfile dataclass
# ---------------------------------------------------------------------------

class TestCoarseGeometryProfileDataclass:
    def test_profile_is_frozen(self):
        p = CoarseGeometryProfile(
            key="t", display_name="Test", geometry_type="euclidean",
            asymptotic_dimension="1", number_of_ends="2",
            has_property_a=True, is_gromov_hyperbolic=True,
            is_quasi_isometric_to_euclidean=True,
            presentation_layer="main_text", focus="test focus",
            chapter_targets=("9",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields_accessible(self):
        p = CoarseGeometryProfile(
            key="k", display_name="K", geometry_type="hyperbolic",
            asymptotic_dimension="1", number_of_ends="infinite",
            has_property_a=True, is_gromov_hyperbolic=True,
            is_quasi_isometric_to_euclidean=False,
            presentation_layer="main_text", focus="free group",
            chapter_targets=("9", "27", "51"),
        )
        assert p.key == "k"
        assert p.geometry_type == "hyperbolic"
        assert p.has_property_a is True
        assert p.is_gromov_hyperbolic is True
        assert p.is_quasi_isometric_to_euclidean is False
        assert p.chapter_targets == ("9", "27", "51")

    def test_profile_equality(self):
        kwargs = dict(
            key="a", display_name="A", geometry_type="euclidean",
            asymptotic_dimension="n", number_of_ends="1",
            has_property_a=True, is_gromov_hyperbolic=False,
            is_quasi_isometric_to_euclidean=True,
            presentation_layer="main_text", focus="f",
            chapter_targets=("9",),
        )
        assert CoarseGeometryProfile(**kwargs) == CoarseGeometryProfile(**kwargs)


# ---------------------------------------------------------------------------
# Named profiles
# ---------------------------------------------------------------------------

class TestNamedCoarseGeometryProfiles:
    def setup_method(self):
        self.profiles = get_named_coarse_geometry_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_five_profiles(self):
        assert len(self.profiles) >= 5

    def test_all_are_coarse_geometry_profiles(self):
        for p in self.profiles:
            assert isinstance(p, CoarseGeometryProfile)

    def test_keys_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_integer_line_exists(self):
        assert "integer_line" in {p.key for p in self.profiles}

    def test_euclidean_lattice_exists(self):
        assert "euclidean_lattice" in {p.key for p in self.profiles}

    def test_free_group_rank2_exists(self):
        assert "free_group_rank2" in {p.key for p in self.profiles}

    def test_hyperbolic_plane_exists(self):
        assert "hyperbolic_plane" in {p.key for p in self.profiles}

    def test_heisenberg_group_exists(self):
        assert "heisenberg_group" in {p.key for p in self.profiles}

    def test_expander_family_exists(self):
        assert "expander_family" in {p.key for p in self.profiles}

    def test_integer_line_geometry_type(self):
        p = next(x for x in self.profiles if x.key == "integer_line")
        assert p.geometry_type == "euclidean"

    def test_integer_line_asdim(self):
        p = next(x for x in self.profiles if x.key == "integer_line")
        assert p.asymptotic_dimension == "1"

    def test_integer_line_ends(self):
        p = next(x for x in self.profiles if x.key == "integer_line")
        assert p.number_of_ends == "2"

    def test_integer_line_has_property_a(self):
        p = next(x for x in self.profiles if x.key == "integer_line")
        assert p.has_property_a is True

    def test_integer_line_is_gromov_hyperbolic(self):
        p = next(x for x in self.profiles if x.key == "integer_line")
        assert p.is_gromov_hyperbolic is True

    def test_integer_line_qi_euclidean(self):
        p = next(x for x in self.profiles if x.key == "integer_line")
        assert p.is_quasi_isometric_to_euclidean is True

    def test_euclidean_lattice_geometry_type(self):
        p = next(x for x in self.profiles if x.key == "euclidean_lattice")
        assert p.geometry_type == "euclidean"

    def test_euclidean_lattice_not_hyperbolic(self):
        p = next(x for x in self.profiles if x.key == "euclidean_lattice")
        assert p.is_gromov_hyperbolic is False

    def test_euclidean_lattice_qi_euclidean(self):
        p = next(x for x in self.profiles if x.key == "euclidean_lattice")
        assert p.is_quasi_isometric_to_euclidean is True

    def test_euclidean_lattice_one_end(self):
        p = next(x for x in self.profiles if x.key == "euclidean_lattice")
        assert p.number_of_ends == "1"

    def test_free_group_geometry_type(self):
        p = next(x for x in self.profiles if x.key == "free_group_rank2")
        assert p.geometry_type == "hyperbolic"

    def test_free_group_infinite_ends(self):
        p = next(x for x in self.profiles if x.key == "free_group_rank2")
        assert p.number_of_ends == "infinite"

    def test_free_group_is_hyperbolic(self):
        p = next(x for x in self.profiles if x.key == "free_group_rank2")
        assert p.is_gromov_hyperbolic is True

    def test_free_group_not_qi_euclidean(self):
        p = next(x for x in self.profiles if x.key == "free_group_rank2")
        assert p.is_quasi_isometric_to_euclidean is False

    def test_free_group_has_property_a(self):
        p = next(x for x in self.profiles if x.key == "free_group_rank2")
        assert p.has_property_a is True

    def test_hyperbolic_plane_is_hyperbolic(self):
        p = next(x for x in self.profiles if x.key == "hyperbolic_plane")
        assert p.is_gromov_hyperbolic is True

    def test_hyperbolic_plane_asdim(self):
        p = next(x for x in self.profiles if x.key == "hyperbolic_plane")
        assert p.asymptotic_dimension == "2"

    def test_hyperbolic_plane_not_qi_euclidean(self):
        p = next(x for x in self.profiles if x.key == "hyperbolic_plane")
        assert p.is_quasi_isometric_to_euclidean is False

    def test_heisenberg_geometry_type(self):
        p = next(x for x in self.profiles if x.key == "heisenberg_group")
        assert p.geometry_type == "nilpotent"

    def test_heisenberg_not_hyperbolic(self):
        p = next(x for x in self.profiles if x.key == "heisenberg_group")
        assert p.is_gromov_hyperbolic is False

    def test_heisenberg_not_qi_euclidean(self):
        p = next(x for x in self.profiles if x.key == "heisenberg_group")
        assert p.is_quasi_isometric_to_euclidean is False

    def test_heisenberg_has_property_a(self):
        p = next(x for x in self.profiles if x.key == "heisenberg_group")
        assert p.has_property_a is True

    def test_heisenberg_asdim(self):
        p = next(x for x in self.profiles if x.key == "heisenberg_group")
        assert p.asymptotic_dimension == "4"

    def test_expander_no_property_a(self):
        p = next(x for x in self.profiles if x.key == "expander_family")
        assert p.has_property_a is False

    def test_expander_geometry_type(self):
        p = next(x for x in self.profiles if x.key == "expander_family")
        assert p.geometry_type == "expander"

    def test_expander_not_hyperbolic(self):
        p = next(x for x in self.profiles if x.key == "expander_family")
        assert p.is_gromov_hyperbolic is False

    def test_expander_not_qi_euclidean(self):
        p = next(x for x in self.profiles if x.key == "expander_family")
        assert p.is_quasi_isometric_to_euclidean is False

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

    def test_property_a_implies_no_expander_geometry(self):
        for p in self.profiles:
            if not p.has_property_a:
                assert p.geometry_type == "expander"


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(coarse_geometry_layer_summary(), dict)

    def test_layer_summary_sum_equals_profile_count(self):
        total = sum(coarse_geometry_layer_summary().values())
        assert total == len(get_named_coarse_geometry_profiles())

    def test_layer_summary_has_main_text(self):
        assert "main_text" in coarse_geometry_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in coarse_geometry_layer_summary()

    def test_chapter_index_returns_dict(self):
        assert isinstance(coarse_geometry_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in coarse_geometry_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_contains_chapter_9(self):
        assert "9" in coarse_geometry_chapter_index()

    def test_chapter_index_contains_chapter_27(self):
        assert "27" in coarse_geometry_chapter_index()

    def test_integer_line_in_chapter_9(self):
        assert "integer_line" in coarse_geometry_chapter_index()["9"]

    def test_free_group_in_chapter_51(self):
        assert "free_group_rank2" in coarse_geometry_chapter_index()["51"]

    def test_type_index_returns_dict(self):
        assert isinstance(coarse_geometry_type_index(), dict)

    def test_type_index_has_euclidean(self):
        assert "euclidean" in coarse_geometry_type_index()

    def test_type_index_has_hyperbolic(self):
        assert "hyperbolic" in coarse_geometry_type_index()

    def test_type_index_has_nilpotent(self):
        assert "nilpotent" in coarse_geometry_type_index()

    def test_type_index_has_expander(self):
        assert "expander" in coarse_geometry_type_index()

    def test_type_index_all_types_in_profiles(self):
        all_types = {p.geometry_type for p in get_named_coarse_geometry_profiles()}
        assert set(coarse_geometry_type_index().keys()) == all_types


# ---------------------------------------------------------------------------
# has_finite_asymptotic_dimension
# ---------------------------------------------------------------------------

class TestHasFiniteAsymptoticDimension:
    def test_virtually_abelian_true(self):
        assert has_finite_asymptotic_dimension(_sp("virtually_abelian")).is_true

    def test_z_lattice_true(self):
        assert has_finite_asymptotic_dimension(_sp("z_lattice")).is_true

    def test_euclidean_lattice_true(self):
        assert has_finite_asymptotic_dimension(_sp("euclidean_lattice")).is_true

    def test_finite_group_true(self):
        assert has_finite_asymptotic_dimension(_sp("finite_group")).is_true

    def test_asdim_finite_true(self):
        assert has_finite_asymptotic_dimension(_sp("asdim_finite")).is_true

    def test_asdim_one_true(self):
        assert has_finite_asymptotic_dimension(_sp("asdim_one")).is_true

    def test_hyperbolic_group_true(self):
        assert has_finite_asymptotic_dimension(_sp("hyperbolic_group")).is_true

    def test_free_group_true(self):
        assert has_finite_asymptotic_dimension(_sp("free_group")).is_true

    def test_gromov_hyperbolic_true(self):
        assert has_finite_asymptotic_dimension(_sp("gromov_hyperbolic")).is_true

    def test_coxeter_group_true(self):
        assert has_finite_asymptotic_dimension(_sp("coxeter_group")).is_true

    def test_right_angled_artin_group_true(self):
        assert has_finite_asymptotic_dimension(_sp("right_angled_artin_group")).is_true

    def test_mapping_class_group_true(self):
        assert has_finite_asymptotic_dimension(_sp("mapping_class_group")).is_true

    def test_expander_family_false(self):
        assert has_finite_asymptotic_dimension(_sp("expander_family")).is_false

    def test_not_property_a_false(self):
        assert has_finite_asymptotic_dimension(_sp("not_property_a")).is_false

    def test_gromov_monster_false(self):
        assert has_finite_asymptotic_dimension(_sp("gromov_monster")).is_false

    def test_empty_unknown(self):
        assert has_finite_asymptotic_dimension(_sp()).is_unknown

    def test_irrelevant_tags_unknown(self):
        assert has_finite_asymptotic_dimension(_sp("compact", "connected")).is_unknown

    def test_returns_result(self):
        assert isinstance(has_finite_asymptotic_dimension(_sp("free_group")), Result)

    def test_true_has_justification(self):
        r = has_finite_asymptotic_dimension(_sp("euclidean_lattice"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = has_finite_asymptotic_dimension(_sp("expander_family"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# has_property_a
# ---------------------------------------------------------------------------

class TestHasPropertyA:
    def test_property_a_tag_true(self):
        assert has_property_a(_sp("property_a")).is_true

    def test_coarsely_amenable_true(self):
        assert has_property_a(_sp("coarsely_amenable")).is_true

    def test_exact_group_true(self):
        assert has_property_a(_sp("exact_group")).is_true

    def test_amenable_group_true(self):
        assert has_property_a(_sp("amenable_group")).is_true

    def test_virtually_abelian_true(self):
        assert has_property_a(_sp("virtually_abelian")).is_true

    def test_finite_group_true(self):
        assert has_property_a(_sp("finite_group")).is_true

    def test_nilpotent_group_true(self):
        assert has_property_a(_sp("nilpotent_group")).is_true

    def test_hyperbolic_group_true(self):
        assert has_property_a(_sp("hyperbolic_group")).is_true

    def test_free_group_true(self):
        assert has_property_a(_sp("free_group")).is_true

    def test_linear_group_true(self):
        assert has_property_a(_sp("linear_group")).is_true

    def test_right_angled_artin_group_true(self):
        assert has_property_a(_sp("right_angled_artin_group")).is_true

    def test_expander_family_false(self):
        assert has_property_a(_sp("expander_family")).is_false

    def test_not_property_a_false(self):
        assert has_property_a(_sp("not_property_a")).is_false

    def test_gromov_monster_false(self):
        assert has_property_a(_sp("gromov_monster")).is_false

    def test_empty_unknown(self):
        assert has_property_a(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(has_property_a(_sp("amenable_group")), Result)

    def test_true_has_justification(self):
        r = has_property_a(_sp("hyperbolic_group"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = has_property_a(_sp("expander_family"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_gromov_hyperbolic
# ---------------------------------------------------------------------------

class TestIsGromovHyperbolic:
    def test_hyperbolic_group_true(self):
        assert is_gromov_hyperbolic(_sp("hyperbolic_group")).is_true

    def test_gromov_hyperbolic_true(self):
        assert is_gromov_hyperbolic(_sp("gromov_hyperbolic")).is_true

    def test_delta_hyperbolic_true(self):
        assert is_gromov_hyperbolic(_sp("delta_hyperbolic")).is_true

    def test_free_group_true(self):
        assert is_gromov_hyperbolic(_sp("free_group")).is_true

    def test_hyperbolic_space_true(self):
        assert is_gromov_hyperbolic(_sp("hyperbolic_space")).is_true

    def test_cat_negative_curvature_true(self):
        assert is_gromov_hyperbolic(_sp("cat_negative_curvature")).is_true

    def test_tree_group_true(self):
        assert is_gromov_hyperbolic(_sp("tree_group")).is_true

    def test_euclidean_lattice_false(self):
        assert is_gromov_hyperbolic(_sp("euclidean_lattice")).is_false

    def test_heisenberg_group_false(self):
        assert is_gromov_hyperbolic(_sp("heisenberg_group")).is_false

    def test_polynomial_growth_false(self):
        assert is_gromov_hyperbolic(_sp("polynomial_growth")).is_false

    def test_virtually_nilpotent_false(self):
        assert is_gromov_hyperbolic(_sp("virtually_nilpotent")).is_false

    def test_expander_family_false(self):
        assert is_gromov_hyperbolic(_sp("expander_family")).is_false

    def test_empty_unknown(self):
        assert is_gromov_hyperbolic(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_gromov_hyperbolic(_sp("free_group")), Result)

    def test_true_has_justification(self):
        r = is_gromov_hyperbolic(_sp("hyperbolic_group"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_gromov_hyperbolic(_sp("euclidean_lattice"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_quasi_isometric_to_euclidean
# ---------------------------------------------------------------------------

class TestIsQuasiIsometricToEuclidean:
    def test_virtually_abelian_true(self):
        assert is_quasi_isometric_to_euclidean(_sp("virtually_abelian")).is_true

    def test_z_lattice_true(self):
        assert is_quasi_isometric_to_euclidean(_sp("z_lattice")).is_true

    def test_euclidean_lattice_true(self):
        assert is_quasi_isometric_to_euclidean(_sp("euclidean_lattice")).is_true

    def test_virtually_z_true(self):
        assert is_quasi_isometric_to_euclidean(_sp("virtually_z")).is_true

    def test_integer_group_true(self):
        assert is_quasi_isometric_to_euclidean(_sp("integer_group")).is_true

    def test_infinite_cyclic_true(self):
        assert is_quasi_isometric_to_euclidean(_sp("infinite_cyclic")).is_true

    def test_qi_euclidean_tag_true(self):
        assert is_quasi_isometric_to_euclidean(_sp("quasi_isometric_to_euclidean")).is_true

    def test_free_group_false(self):
        assert is_quasi_isometric_to_euclidean(_sp("free_group")).is_false

    def test_hyperbolic_group_false(self):
        assert is_quasi_isometric_to_euclidean(_sp("hyperbolic_group")).is_false

    def test_exponential_growth_false(self):
        assert is_quasi_isometric_to_euclidean(_sp("exponential_growth")).is_false

    def test_heisenberg_group_false(self):
        assert is_quasi_isometric_to_euclidean(_sp("heisenberg_group")).is_false

    def test_nilpotent_group_false(self):
        assert is_quasi_isometric_to_euclidean(_sp("nilpotent_group")).is_false

    def test_expander_family_false(self):
        assert is_quasi_isometric_to_euclidean(_sp("expander_family")).is_false

    def test_empty_unknown(self):
        assert is_quasi_isometric_to_euclidean(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_quasi_isometric_to_euclidean(_sp("euclidean_lattice")), Result)

    def test_true_has_justification(self):
        r = is_quasi_isometric_to_euclidean(_sp("virtually_abelian"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_quasi_isometric_to_euclidean(_sp("heisenberg_group"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# coarsely_embeds_in_hilbert
# ---------------------------------------------------------------------------

class TestCoarselyEmbedsInHilbert:
    def test_property_a_true(self):
        assert coarsely_embeds_in_hilbert(_sp("property_a")).is_true

    def test_coarsely_amenable_true(self):
        assert coarsely_embeds_in_hilbert(_sp("coarsely_amenable")).is_true

    def test_amenable_group_true(self):
        assert coarsely_embeds_in_hilbert(_sp("amenable_group")).is_true

    def test_hyperbolic_group_true(self):
        assert coarsely_embeds_in_hilbert(_sp("hyperbolic_group")).is_true

    def test_free_group_true(self):
        assert coarsely_embeds_in_hilbert(_sp("free_group")).is_true

    def test_virtually_abelian_true(self):
        assert coarsely_embeds_in_hilbert(_sp("virtually_abelian")).is_true

    def test_linear_group_true(self):
        assert coarsely_embeds_in_hilbert(_sp("linear_group")).is_true

    def test_expander_family_false(self):
        assert coarsely_embeds_in_hilbert(_sp("expander_family")).is_false

    def test_not_property_a_false(self):
        assert coarsely_embeds_in_hilbert(_sp("not_property_a")).is_false

    def test_no_coarse_embedding_hilbert_false(self):
        assert coarsely_embeds_in_hilbert(_sp("no_coarse_embedding_hilbert")).is_false

    def test_gromov_monster_false(self):
        assert coarsely_embeds_in_hilbert(_sp("gromov_monster")).is_false

    def test_empty_unknown(self):
        assert coarsely_embeds_in_hilbert(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(coarsely_embeds_in_hilbert(_sp("property_a")), Result)

    def test_true_has_justification(self):
        r = coarsely_embeds_in_hilbert(_sp("property_a"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = coarsely_embeds_in_hilbert(_sp("expander_family"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# classify_coarse_geometry
# ---------------------------------------------------------------------------

class TestClassifyCoarseGeometry:
    def test_returns_dict(self):
        assert isinstance(classify_coarse_geometry(_sp()), dict)

    def test_has_geometry_class_key(self):
        assert "geometry_class" in classify_coarse_geometry(_sp())

    def test_has_finite_asdim_key(self):
        assert "has_finite_asymptotic_dimension" in classify_coarse_geometry(_sp())

    def test_has_property_a_key(self):
        assert "has_property_a" in classify_coarse_geometry(_sp())

    def test_has_gromov_hyperbolic_key(self):
        assert "is_gromov_hyperbolic" in classify_coarse_geometry(_sp())

    def test_has_qi_euclidean_key(self):
        assert "is_quasi_isometric_to_euclidean" in classify_coarse_geometry(_sp())

    def test_has_hilbert_key(self):
        assert "coarsely_embeds_in_hilbert" in classify_coarse_geometry(_sp())

    def test_has_key_properties_key(self):
        assert "key_properties" in classify_coarse_geometry(_sp())

    def test_key_properties_is_list(self):
        assert isinstance(classify_coarse_geometry(_sp())["key_properties"], list)

    def test_expander_class(self):
        r = classify_coarse_geometry(_sp("expander_family"))
        assert r["geometry_class"] == "expander"

    def test_euclidean_class(self):
        r = classify_coarse_geometry(_sp("euclidean_lattice"))
        assert r["geometry_class"] == "euclidean"

    def test_hyperbolic_class(self):
        r = classify_coarse_geometry(_sp("hyperbolic_group", "gromov_hyperbolic"))
        assert r["geometry_class"] == "hyperbolic"

    def test_nilpotent_class(self):
        r = classify_coarse_geometry(_sp("heisenberg_group", "nilpotent_group"))
        assert r["geometry_class"] == "nilpotent"

    def test_unknown_class_empty(self):
        r = classify_coarse_geometry(_sp())
        assert r["geometry_class"] == "unknown"

    def test_euclidean_key_props_contains_qi_euclidean(self):
        r = classify_coarse_geometry(_sp("euclidean_lattice"))
        assert "quasi_isometric_euclidean" in r["key_properties"]

    def test_hyperbolic_key_props_contains_gromov_hyperbolic(self):
        r = classify_coarse_geometry(_sp("free_group"))
        assert "gromov_hyperbolic" in r["key_properties"]

    def test_property_a_in_key_props(self):
        r = classify_coarse_geometry(_sp("amenable_group"))
        assert "property_a" in r["key_properties"]

    def test_no_property_a_in_key_props(self):
        r = classify_coarse_geometry(_sp("expander_family"))
        assert "no_property_a" in r["key_properties"]

    def test_two_ends_in_key_props(self):
        r = classify_coarse_geometry(_sp("integer_group"))
        assert "two_ends" in r["key_properties"]

    def test_infinite_ends_in_key_props(self):
        r = classify_coarse_geometry(_sp("free_group"))
        assert "infinite_ends" in r["key_properties"]

    def test_one_end_in_key_props(self):
        r = classify_coarse_geometry(_sp("heisenberg_group"))
        assert "one_end" in r["key_properties"]

    def test_representation_in_output(self):
        assert "representation" in classify_coarse_geometry(_sp())

    def test_tags_is_list(self):
        assert isinstance(classify_coarse_geometry(_sp("free_group"))["tags"], list)

    def test_finite_asdim_in_key_props(self):
        r = classify_coarse_geometry(_sp("free_group"))
        assert "finite_asymptotic_dimension" in r["key_properties"]

    def test_infinite_asdim_in_key_props(self):
        r = classify_coarse_geometry(_sp("expander_family"))
        assert "infinite_asymptotic_dimension" in r["key_properties"]

    def test_hilbert_embedding_in_key_props(self):
        r = classify_coarse_geometry(_sp("property_a"))
        assert "coarse_hilbert_embedding" in r["key_properties"]

    def test_no_hilbert_embedding_in_key_props(self):
        r = classify_coarse_geometry(_sp("expander_family"))
        assert "no_hilbert_embedding" in r["key_properties"]


# ---------------------------------------------------------------------------
# coarse_geometry_profile
# ---------------------------------------------------------------------------

class TestCoarseGeometryProfile:
    def test_returns_dict(self):
        assert isinstance(coarse_geometry_profile(_sp()), dict)

    def test_has_classification_key(self):
        assert "classification" in coarse_geometry_profile(_sp())

    def test_has_named_profiles_key(self):
        assert "named_profiles" in coarse_geometry_profile(_sp())

    def test_has_layer_summary_key(self):
        assert "layer_summary" in coarse_geometry_profile(_sp())

    def test_named_profiles_is_tuple(self):
        assert isinstance(coarse_geometry_profile(_sp())["named_profiles"], tuple)

    def test_classification_has_geometry_class(self):
        p = coarse_geometry_profile(_sp("free_group"))
        assert "geometry_class" in p["classification"]

    def test_layer_summary_is_dict(self):
        assert isinstance(coarse_geometry_profile(_sp())["layer_summary"], dict)

    def test_expander_classification_correct(self):
        p = coarse_geometry_profile(_sp("expander_family"))
        assert p["classification"]["geometry_class"] == "expander"

    def test_euclidean_classification_correct(self):
        p = coarse_geometry_profile(_sp("euclidean_lattice"))
        assert p["classification"]["geometry_class"] == "euclidean"
