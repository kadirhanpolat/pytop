"""Tests for pytop.persistent_homology."""

from __future__ import annotations

import pytest

from pytop.persistent_homology import (
    CECH_COMPLEX_TAGS,
    ESSENTIAL_CLASS_TAGS,
    FIELD_COEFFICIENTS_TAGS,
    PERSISTENCE_DIAGRAM_TAGS,
    STABLE_FILTRATION_TAGS,
    STRUCTURE_THEOREM_TAGS,
    SUBLEVEL_SET_TAGS,
    UNSTABLE_OR_SENSITIVE_TAGS,
    VIETORIS_RIPS_TAGS,
    PersistenceProfile,
    classify_persistence,
    get_named_persistence_profiles,
    has_essential_classes,
    has_finite_barcode,
    has_structure_theorem,
    is_stable_filtration,
    persistence_chapter_index,
    persistence_layer_summary,
    persistence_profile,
    persistence_type_index,
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
    def test_vietoris_rips_tags_nonempty(self):
        assert len(VIETORIS_RIPS_TAGS) >= 4

    def test_cech_complex_tags_nonempty(self):
        assert len(CECH_COMPLEX_TAGS) >= 4

    def test_persistence_diagram_tags_nonempty(self):
        assert len(PERSISTENCE_DIAGRAM_TAGS) >= 4

    def test_stable_filtration_tags_nonempty(self):
        assert len(STABLE_FILTRATION_TAGS) >= 4

    def test_unstable_tags_nonempty(self):
        assert len(UNSTABLE_OR_SENSITIVE_TAGS) >= 2

    def test_essential_class_tags_nonempty(self):
        assert len(ESSENTIAL_CLASS_TAGS) >= 4

    def test_sublevel_set_tags_nonempty(self):
        assert len(SUBLEVEL_SET_TAGS) >= 4

    def test_field_coefficients_tags_nonempty(self):
        assert len(FIELD_COEFFICIENTS_TAGS) >= 4

    def test_structure_theorem_tags_nonempty(self):
        assert len(STRUCTURE_THEOREM_TAGS) >= 4

    def test_vietoris_rips_in_vr_tags(self):
        assert "vietoris_rips" in VIETORIS_RIPS_TAGS

    def test_cech_complex_in_cech_tags(self):
        assert "cech_complex" in CECH_COMPLEX_TAGS

    def test_barcode_in_diagram_tags(self):
        assert "barcode" in PERSISTENCE_DIAGRAM_TAGS

    def test_stability_theorem_in_stable_tags(self):
        assert "stability_theorem" in STABLE_FILTRATION_TAGS

    def test_essential_class_in_essential_tags(self):
        assert "essential_class" in ESSENTIAL_CLASS_TAGS

    def test_sublevel_set_in_sublevel_tags(self):
        assert "sublevel_set_filtration" in SUBLEVEL_SET_TAGS

    def test_z2_coefficients_in_field_tags(self):
        assert "z2_coefficients" in FIELD_COEFFICIENTS_TAGS

    def test_structure_theorem_in_structure_tags(self):
        assert "structure_theorem" in STRUCTURE_THEOREM_TAGS

    def test_vr_in_sublevel_tags(self):
        assert "vr_filtration" in SUBLEVEL_SET_TAGS

    def test_cech_in_sublevel_tags(self):
        assert "cech_filtration" in SUBLEVEL_SET_TAGS

    def test_all_tag_sets_contain_strings(self):
        for tag_set in [
            VIETORIS_RIPS_TAGS, CECH_COMPLEX_TAGS, PERSISTENCE_DIAGRAM_TAGS,
            STABLE_FILTRATION_TAGS, UNSTABLE_OR_SENSITIVE_TAGS, ESSENTIAL_CLASS_TAGS,
            SUBLEVEL_SET_TAGS, FIELD_COEFFICIENTS_TAGS, STRUCTURE_THEOREM_TAGS,
        ]:
            assert all(isinstance(t, str) for t in tag_set)

    def test_stable_and_unstable_disjoint(self):
        assert STABLE_FILTRATION_TAGS.isdisjoint(UNSTABLE_OR_SENSITIVE_TAGS)


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_persistence_profiles(), tuple)

    def test_at_least_six_profiles(self):
        assert len(get_named_persistence_profiles()) >= 6

    def test_all_persistence_profile_instances(self):
        for p in get_named_persistence_profiles():
            assert isinstance(p, PersistenceProfile)

    def test_keys_unique(self):
        keys = [p.key for p in get_named_persistence_profiles()]
        assert len(keys) == len(set(keys))

    def test_display_names_nonempty(self):
        for p in get_named_persistence_profiles():
            assert p.display_name.strip()

    def test_focus_nonempty(self):
        for p in get_named_persistence_profiles():
            assert p.focus.strip()

    def test_chapter_targets_nonempty(self):
        for p in get_named_persistence_profiles():
            assert len(p.chapter_targets) >= 1

    def test_presentation_layers_known(self):
        known = {"main_text", "selected_block", "appendix"}
        for p in get_named_persistence_profiles():
            assert p.presentation_layer in known

    def test_filtration_types_are_strings(self):
        for p in get_named_persistence_profiles():
            assert isinstance(p.filtration_type, str)

    # vietoris_rips_point_cloud
    def test_vr_profile_present(self):
        assert "vietoris_rips_point_cloud" in {p.key for p in get_named_persistence_profiles()}

    def test_vr_has_finite_barcode(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "vietoris_rips_point_cloud")
        assert p.has_finite_barcode is True

    def test_vr_is_stable(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "vietoris_rips_point_cloud")
        assert p.is_stable is True

    def test_vr_computable_over_field(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "vietoris_rips_point_cloud")
        assert p.computable_over_field is True

    def test_vr_no_essential_classes(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "vietoris_rips_point_cloud")
        assert p.has_essential_classes is False

    # sublevel_set_filtration
    def test_sublevel_profile_present(self):
        assert "sublevel_set_filtration" in {p.key for p in get_named_persistence_profiles()}

    def test_sublevel_has_finite_barcode(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "sublevel_set_filtration")
        assert p.has_finite_barcode is True

    def test_sublevel_is_stable(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "sublevel_set_filtration")
        assert p.is_stable is True

    def test_sublevel_has_essential_classes(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "sublevel_set_filtration")
        assert p.has_essential_classes is True

    # persistence_diagram_bottleneck
    def test_diagram_profile_present(self):
        assert "persistence_diagram_bottleneck" in {p.key for p in get_named_persistence_profiles()}

    def test_diagram_is_stable(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "persistence_diagram_bottleneck")
        assert p.is_stable is True

    def test_diagram_finite_barcode(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "persistence_diagram_bottleneck")
        assert p.has_finite_barcode is True

    # structure_theorem_persistence_modules
    def test_structure_profile_present(self):
        assert "structure_theorem_persistence_modules" in {
            p.key for p in get_named_persistence_profiles()
        }

    def test_structure_finite_barcode(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "structure_theorem_persistence_modules")
        assert p.has_finite_barcode is True

    def test_structure_is_stable(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "structure_theorem_persistence_modules")
        assert p.is_stable is True

    def test_structure_computable(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "structure_theorem_persistence_modules")
        assert p.computable_over_field is True

    # cech_alpha_complex
    def test_cech_profile_present(self):
        assert "cech_alpha_complex" in {p.key for p in get_named_persistence_profiles()}

    def test_cech_is_stable(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "cech_alpha_complex")
        assert p.is_stable is True

    def test_cech_finite_barcode(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "cech_alpha_complex")
        assert p.has_finite_barcode is True

    # circle_point_cloud
    def test_circle_profile_present(self):
        assert "circle_point_cloud" in {p.key for p in get_named_persistence_profiles()}

    def test_circle_is_stable(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "circle_point_cloud")
        assert p.is_stable is True

    def test_circle_finite_barcode(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "circle_point_cloud")
        assert p.has_finite_barcode is True

    def test_circle_no_essential_classes(self):
        # as modeled: no_essential in VR of finite point cloud
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "circle_point_cloud")
        assert p.has_essential_classes is False

    # mapper_algorithm
    def test_mapper_profile_present(self):
        assert "mapper_algorithm" in {p.key for p in get_named_persistence_profiles()}

    def test_mapper_not_stable(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "mapper_algorithm")
        assert p.is_stable is False

    def test_mapper_no_finite_barcode(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "mapper_algorithm")
        assert p.has_finite_barcode is False

    def test_mapper_not_computable_over_field(self):
        p = next(p for p in get_named_persistence_profiles()
                 if p.key == "mapper_algorithm")
        assert p.computable_over_field is False


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_is_dict(self):
        assert isinstance(persistence_layer_summary(), dict)

    def test_layer_summary_has_main_text(self):
        assert "main_text" in persistence_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in persistence_layer_summary()

    def test_layer_summary_total(self):
        profiles = get_named_persistence_profiles()
        assert sum(persistence_layer_summary().values()) == len(profiles)

    def test_chapter_index_is_dict(self):
        assert isinstance(persistence_chapter_index(), dict)

    def test_chapter_index_sorted(self):
        ch = persistence_chapter_index()
        assert list(ch.keys()) == sorted(ch.keys())

    def test_chapter_index_tuples(self):
        for v in persistence_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_nonempty_values(self):
        for v in persistence_chapter_index().values():
            assert len(v) >= 1

    def test_type_index_is_dict(self):
        assert isinstance(persistence_type_index(), dict)

    def test_type_index_has_vr(self):
        assert "vietoris_rips" in persistence_type_index()

    def test_type_index_tuples(self):
        for v in persistence_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_total(self):
        total = sum(len(v) for v in persistence_type_index().values())
        assert total == len(get_named_persistence_profiles())


# ---------------------------------------------------------------------------
# has_finite_barcode
# ---------------------------------------------------------------------------

class TestHasFiniteBarcode:
    def test_barcode_tag_true(self):
        assert has_finite_barcode(_space("barcode")).is_true

    def test_persistence_diagram_true(self):
        assert has_finite_barcode(_space("persistence_diagram")).is_true

    def test_birth_death_pairs_true(self):
        assert has_finite_barcode(_space("birth_death_pairs")).is_true

    def test_vietoris_rips_true(self):
        assert has_finite_barcode(_space("vietoris_rips")).is_true

    def test_rips_filtration_true(self):
        assert has_finite_barcode(_space("rips_filtration")).is_true

    def test_cech_complex_true(self):
        assert has_finite_barcode(_space("cech_complex")).is_true

    def test_sublevel_set_filtration_true(self):
        assert has_finite_barcode(_space("sublevel_set_filtration")).is_true

    def test_morse_filtration_true(self):
        assert has_finite_barcode(_space("morse_filtration")).is_true

    def test_alpha_complex_true(self):
        assert has_finite_barcode(_space("alpha_complex")).is_true

    def test_non_tame_false(self):
        assert has_finite_barcode(_space("non_tame_function")).is_false

    def test_infinite_filtration_false(self):
        assert has_finite_barcode(_space("infinite_filtration")).is_false

    def test_not_stable_false(self):
        assert has_finite_barcode(_space("not_stable")).is_false

    def test_unknown_empty(self):
        r = has_finite_barcode(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert has_finite_barcode(_space("barcode")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert has_finite_barcode(_space("non_tame_function")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert has_finite_barcode(_space()).mode == "symbolic"

    def test_criterion_explicit_barcode(self):
        r = has_finite_barcode(_space("barcode"))
        assert r.metadata.get("criterion") == "explicit_barcode"

    def test_criterion_finite_filtration(self):
        r = has_finite_barcode(_space("vietoris_rips"))
        assert r.metadata.get("criterion") == "finite_filtration"

    def test_criterion_infinite_barcode(self):
        r = has_finite_barcode(_space("non_tame_function"))
        assert r.metadata.get("criterion") == "infinite_barcode"

    def test_rips_complex_true(self):
        assert has_finite_barcode(_space("rips_complex")).is_true

    def test_dgm_true(self):
        assert has_finite_barcode(_space("dgm")).is_true

    def test_diameter_filtration_true(self):
        assert has_finite_barcode(_space("diameter_filtration")).is_true

    def test_function_filtration_true(self):
        assert has_finite_barcode(_space("function_filtration")).is_true

    def test_distance_filtration_true(self):
        assert has_finite_barcode(_space("distance_filtration")).is_true


# ---------------------------------------------------------------------------
# is_stable_filtration
# ---------------------------------------------------------------------------

class TestIsStableFiltration:
    def test_stability_theorem_tag_true(self):
        assert is_stable_filtration(_space("stability_theorem")).is_true

    def test_stable_filtration_tag_true(self):
        assert is_stable_filtration(_space("stable_filtration")).is_true

    def test_bottleneck_stable_true(self):
        assert is_stable_filtration(_space("bottleneck_stable")).is_true

    def test_sublevel_set_filtration_true(self):
        assert is_stable_filtration(_space("sublevel_set_filtration")).is_true

    def test_morse_filtration_true(self):
        assert is_stable_filtration(_space("morse_filtration")).is_true

    def test_tame_function_true(self):
        assert is_stable_filtration(_space("tame_function")).is_true

    def test_vietoris_rips_true(self):
        assert is_stable_filtration(_space("vietoris_rips")).is_true

    def test_rips_filtration_true(self):
        assert is_stable_filtration(_space("rips_filtration")).is_true

    def test_cech_complex_true(self):
        assert is_stable_filtration(_space("cech_complex")).is_true

    def test_cech_filtration_true(self):
        assert is_stable_filtration(_space("cech_filtration")).is_true

    def test_not_stable_false(self):
        assert is_stable_filtration(_space("not_stable")).is_false

    def test_mapper_graph_false(self):
        assert is_stable_filtration(_space("mapper_graph")).is_false

    def test_cover_filtration_false(self):
        assert is_stable_filtration(_space("cover_filtration")).is_false

    def test_sensitive_to_noise_false(self):
        assert is_stable_filtration(_space("sensitive_to_noise")).is_false

    def test_unknown_empty(self):
        r = is_stable_filtration(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit_stable(self):
        r = is_stable_filtration(_space("stability_theorem"))
        assert r.metadata.get("criterion") == "explicit_stable"

    def test_criterion_rips_cech_stable(self):
        r = is_stable_filtration(_space("vietoris_rips"))
        assert r.metadata.get("criterion") == "rips_cech_stable"

    def test_criterion_not_stable(self):
        r = is_stable_filtration(_space("not_stable"))
        assert r.metadata.get("criterion") == "not_stable"

    def test_function_filtration_true(self):
        assert is_stable_filtration(_space("function_filtration")).is_true

    def test_height_filtration_true(self):
        assert is_stable_filtration(_space("height_filtration")).is_true

    def test_infinite_persistence_false(self):
        assert is_stable_filtration(_space("infinite_persistence")).is_false


# ---------------------------------------------------------------------------
# has_essential_classes
# ---------------------------------------------------------------------------

class TestHasEssentialClasses:
    def test_essential_homology_true(self):
        assert has_essential_classes(_space("essential_homology")).is_true

    def test_infinite_bar_true(self):
        assert has_essential_classes(_space("infinite_bar")).is_true

    def test_essential_class_tag_true(self):
        assert has_essential_classes(_space("essential_class")).is_true

    def test_non_contractible_component_true(self):
        assert has_essential_classes(_space("non_contractible_component")).is_true

    def test_essential_cycle_true(self):
        assert has_essential_classes(_space("essential_cycle")).is_true

    def test_unbounded_persistence_true(self):
        assert has_essential_classes(_space("unbounded_persistence")).is_true

    def test_non_contractible_true(self):
        assert has_essential_classes(_space("non_contractible")).is_true

    def test_circle_data_true(self):
        assert has_essential_classes(_space("circle_data")).is_true

    def test_torus_data_true(self):
        assert has_essential_classes(_space("torus_data")).is_true

    def test_sphere_data_true(self):
        assert has_essential_classes(_space("sphere_data")).is_true

    def test_closed_manifold_data_true(self):
        assert has_essential_classes(_space("closed_manifold_data")).is_true

    def test_contractible_data_false(self):
        assert has_essential_classes(_space("contractible_data")).is_false

    def test_convex_point_cloud_false(self):
        assert has_essential_classes(_space("convex_point_cloud")).is_false

    def test_tree_data_false(self):
        assert has_essential_classes(_space("tree_data")).is_false

    def test_no_essential_classes_false(self):
        assert has_essential_classes(_space("no_essential_classes")).is_false

    def test_contractible_full_complex_false(self):
        assert has_essential_classes(_space("contractible_full_complex")).is_false

    def test_unknown_empty(self):
        r = has_essential_classes(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit_essential(self):
        r = has_essential_classes(_space("essential_homology"))
        assert r.metadata.get("criterion") == "explicit_essential"

    def test_criterion_non_contractible(self):
        r = has_essential_classes(_space("non_contractible"))
        assert r.metadata.get("criterion") == "non_contractible_topology"

    def test_criterion_contractible(self):
        r = has_essential_classes(_space("contractible_data"))
        assert r.metadata.get("criterion") == "contractible_no_essential"

    def test_non_trivial_topology_true(self):
        assert has_essential_classes(_space("non_trivial_topology")).is_true


# ---------------------------------------------------------------------------
# has_structure_theorem
# ---------------------------------------------------------------------------

class TestHasStructureTheorem:
    def test_structure_theorem_tag_true(self):
        assert has_structure_theorem(_space("structure_theorem")).is_true

    def test_interval_decomposition_true(self):
        assert has_structure_theorem(_space("interval_decomposition")).is_true

    def test_persistence_module_true(self):
        assert has_structure_theorem(_space("persistence_module")).is_true

    def test_zomorodian_carlsson_true(self):
        assert has_structure_theorem(_space("zomorodian_carlsson")).is_true

    def test_pid_decomposition_true(self):
        assert has_structure_theorem(_space("pid_decomposition")).is_true

    def test_field_and_vr_true(self):
        assert has_structure_theorem(
            _space("z2_coefficients", "vietoris_rips")
        ).is_true

    def test_field_and_cech_true(self):
        assert has_structure_theorem(
            _space("field_coefficients", "cech_filtration")
        ).is_true

    def test_field_and_sublevel_true(self):
        assert has_structure_theorem(
            _space("f2_coefficients", "sublevel_set_filtration")
        ).is_true

    def test_field_and_persistence_module_true(self):
        assert has_structure_theorem(
            _space("rational_coefficients", "persistence_module")
        ).is_true

    def test_integer_coefficients_false(self):
        assert has_structure_theorem(_space("integer_coefficients")).is_false

    def test_z_coefficients_false(self):
        assert has_structure_theorem(_space("z_coefficients")).is_false

    def test_torsion_persistence_false(self):
        assert has_structure_theorem(_space("torsion_persistence")).is_false

    def test_non_field_false(self):
        assert has_structure_theorem(_space("non_field_coefficients")).is_false

    def test_infinite_filtration_false(self):
        assert has_structure_theorem(_space("infinite_filtration")).is_false

    def test_unknown_empty(self):
        r = has_structure_theorem(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit(self):
        r = has_structure_theorem(_space("structure_theorem"))
        assert r.metadata.get("criterion") == "explicit_structure_theorem"

    def test_criterion_field_coefficients(self):
        r = has_structure_theorem(_space("z2_coefficients", "vietoris_rips"))
        assert r.metadata.get("criterion") == "field_coefficients_structure"

    def test_criterion_no_structure(self):
        r = has_structure_theorem(_space("integer_coefficients"))
        assert r.metadata.get("criterion") == "no_structure_theorem"

    def test_graded_module_pid_true(self):
        assert has_structure_theorem(_space("graded_module_pid")).is_true

    def test_field_alone_unknown(self):
        r = has_structure_theorem(_space("field_coefficients"))
        # field coefficients alone, without filtration tag -> unknown
        assert not r.is_true and not r.is_false


# ---------------------------------------------------------------------------
# classify_persistence
# ---------------------------------------------------------------------------

class TestClassifyPersistence:
    def test_returns_dict(self):
        assert isinstance(classify_persistence(_space()), dict)

    def test_required_keys(self):
        r = classify_persistence(_space())
        assert {
            "persistence_class", "has_finite_barcode", "is_stable_filtration",
            "has_essential_classes", "has_structure_theorem",
            "key_properties", "representation", "tags",
        } <= r.keys()

    def test_stable_essential_class(self):
        r = classify_persistence(
            _space("stability_theorem", "barcode", "essential_class")
        )
        assert r["persistence_class"] == "stable_essential"

    def test_stable_finite_class(self):
        r = classify_persistence(_space("vietoris_rips", "barcode"))
        assert r["persistence_class"] == "stable_finite"

    def test_algebraic_class(self):
        r = classify_persistence(_space("structure_theorem", "barcode"))
        assert r["persistence_class"] == "algebraic"

    def test_qualitative_class_mapper(self):
        r = classify_persistence(_space("mapper_graph"))
        assert r["persistence_class"] == "qualitative"

    def test_finite_barcode_in_properties(self):
        r = classify_persistence(_space("barcode"))
        assert "finite_barcode" in r["key_properties"]

    def test_stable_in_properties(self):
        r = classify_persistence(_space("stability_theorem"))
        assert "stable" in r["key_properties"]

    def test_not_stable_in_properties(self):
        r = classify_persistence(_space("not_stable"))
        assert "not_stable" in r["key_properties"]

    def test_essential_classes_in_properties(self):
        r = classify_persistence(_space("essential_class"))
        assert "essential_classes" in r["key_properties"]

    def test_structure_theorem_in_properties(self):
        r = classify_persistence(_space("structure_theorem"))
        assert "structure_theorem" in r["key_properties"]

    def test_vietoris_rips_in_properties(self):
        r = classify_persistence(_space("vietoris_rips"))
        assert "vietoris_rips" in r["key_properties"]

    def test_cech_complex_in_properties(self):
        r = classify_persistence(_space("cech_complex"))
        assert "cech_complex" in r["key_properties"]

    def test_field_coefficients_in_properties(self):
        r = classify_persistence(_space("z2_coefficients"))
        assert "field_coefficients" in r["key_properties"]

    def test_mapper_qualitative_in_properties(self):
        r = classify_persistence(_space("mapper_graph"))
        assert "mapper_qualitative" in r["key_properties"]

    def test_tags_sorted(self):
        r = classify_persistence(_space("vietoris_rips", "barcode"))
        assert r["tags"] == sorted(r["tags"])

    def test_representation_passthrough(self):
        r = classify_persistence(_space("barcode", rep="my_rep"))
        assert r["representation"] == "my_rep"

    def test_cover_filtration_qualitative(self):
        r = classify_persistence(_space("cover_filtration"))
        assert r["persistence_class"] == "qualitative"


# ---------------------------------------------------------------------------
# persistence_profile
# ---------------------------------------------------------------------------

class TestPersistenceProfile:
    def test_returns_dict(self):
        assert isinstance(persistence_profile(_space()), dict)

    def test_has_classification(self):
        assert "classification" in persistence_profile(_space())

    def test_has_named_profiles(self):
        assert "named_profiles" in persistence_profile(_space())

    def test_has_layer_summary(self):
        assert "layer_summary" in persistence_profile(_space())

    def test_classification_is_dict(self):
        assert isinstance(persistence_profile(_space())["classification"], dict)

    def test_named_profiles_is_tuple(self):
        assert isinstance(persistence_profile(_space())["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        assert isinstance(persistence_profile(_space())["layer_summary"], dict)

    def test_named_profiles_nonempty(self):
        assert len(persistence_profile(_space())["named_profiles"]) >= 6


# ---------------------------------------------------------------------------
# PersistenceProfile dataclass
# ---------------------------------------------------------------------------

class TestPersistenceProfileDataclass:
    def test_frozen(self):
        p = PersistenceProfile(
            key="t", display_name="T", complex_type="vietoris_rips",
            filtration_type="diameter_filtration",
            has_finite_barcode=True, is_stable=True,
            has_essential_classes=False, computable_over_field=True,
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        with pytest.raises(Exception):
            p.key = "other"  # type: ignore[misc]

    def test_equality_by_value(self):
        kwargs = dict(
            key="t", display_name="T", complex_type="vietoris_rips",
            filtration_type="diameter_filtration",
            has_finite_barcode=True, is_stable=True,
            has_essential_classes=False, computable_over_field=True,
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        assert PersistenceProfile(**kwargs) == PersistenceProfile(**kwargs)

    def test_all_fields_accessible(self):
        p = PersistenceProfile(
            key="x", display_name="X", complex_type="abstract",
            filtration_type="general",
            has_finite_barcode=False, is_stable=False,
            has_essential_classes=True, computable_over_field=False,
            presentation_layer="selected_block", focus="mapper",
            chapter_targets=("9", "19"),
        )
        assert p.filtration_type == "general"
        assert p.has_finite_barcode is False
        assert p.chapter_targets == ("9", "19")
