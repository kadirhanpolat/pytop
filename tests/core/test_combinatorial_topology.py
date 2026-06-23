"""Tests for pytop.combinatorial_topology."""

from __future__ import annotations

import pytest

from pytop.combinatorial_topology import (
    ACYCLIC_TAGS,
    COLLAPSIBLE_TAGS,
    CONTRACTIBLE_TAGS,
    CW_COMPLEX_TAGS,
    EULER_CHARACTERISTIC_TAGS,
    NERVE_THEOREM_TAGS,
    NOT_COLLAPSIBLE_TAGS,
    SIMPLICIAL_COMPLEX_TAGS,
    TORSION_TAGS,
    CombinatorialProfile,
    classify_combinatorial,
    combinatorial_chapter_index,
    combinatorial_layer_summary,
    combinatorial_profile,
    combinatorial_type_index,
    get_named_combinatorial_profiles,
    has_torsion_homology,
    is_acyclic_complex,
    is_collapsible_complex,
    is_contractible_complex,
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
    def test_simplicial_complex_tags_nonempty(self):
        assert len(SIMPLICIAL_COMPLEX_TAGS) >= 5

    def test_cw_complex_tags_nonempty(self):
        assert len(CW_COMPLEX_TAGS) >= 3

    def test_contractible_tags_nonempty(self):
        assert len(CONTRACTIBLE_TAGS) >= 5

    def test_acyclic_tags_nonempty(self):
        assert len(ACYCLIC_TAGS) >= 4

    def test_torsion_tags_nonempty(self):
        assert len(TORSION_TAGS) >= 4

    def test_euler_characteristic_tags_nonempty(self):
        assert len(EULER_CHARACTERISTIC_TAGS) >= 3

    def test_nerve_theorem_tags_nonempty(self):
        assert len(NERVE_THEOREM_TAGS) >= 3

    def test_collapsible_tags_nonempty(self):
        assert len(COLLAPSIBLE_TAGS) >= 3

    def test_not_collapsible_tags_nonempty(self):
        assert len(NOT_COLLAPSIBLE_TAGS) >= 3

    def test_contractible_tags_are_strings(self):
        assert all(isinstance(t, str) for t in CONTRACTIBLE_TAGS)

    def test_torsion_tags_are_strings(self):
        assert all(isinstance(t, str) for t in TORSION_TAGS)

    def test_all_tag_sets_disjoint_where_expected(self):
        # collapsible and not_collapsible must be disjoint
        assert COLLAPSIBLE_TAGS.isdisjoint(NOT_COLLAPSIBLE_TAGS)

    def test_contractible_subset_of_acyclic(self):
        # contractible tags appear in acyclic tag set
        assert "contractible" in ACYCLIC_TAGS

    def test_contractible_in_contractible_tags(self):
        assert "contractible" in CONTRACTIBLE_TAGS

    def test_non_orientable_in_torsion_tags(self):
        assert "non_orientable" in TORSION_TAGS

    def test_nerve_complex_in_nerve_tags(self):
        assert "nerve_complex" in NERVE_THEOREM_TAGS

    def test_cw_complex_in_cw_tags(self):
        assert "cw_complex" in CW_COMPLEX_TAGS


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        profiles = get_named_combinatorial_profiles()
        assert isinstance(profiles, tuple)

    def test_at_least_six_profiles(self):
        assert len(get_named_combinatorial_profiles()) >= 6

    def test_all_combinatorial_profile_instances(self):
        for p in get_named_combinatorial_profiles():
            assert isinstance(p, CombinatorialProfile)

    def test_keys_are_unique(self):
        keys = [p.key for p in get_named_combinatorial_profiles()]
        assert len(keys) == len(set(keys))

    def test_all_have_nonempty_display_name(self):
        for p in get_named_combinatorial_profiles():
            assert p.display_name.strip()

    def test_all_have_nonempty_focus(self):
        for p in get_named_combinatorial_profiles():
            assert p.focus.strip()

    def test_all_have_chapter_targets(self):
        for p in get_named_combinatorial_profiles():
            assert len(p.chapter_targets) >= 1

    def test_presentation_layers_are_known(self):
        known = {"main_text", "selected_block", "appendix"}
        for p in get_named_combinatorial_profiles():
            assert p.presentation_layer in known

    def test_standard_simplex_present(self):
        keys = {p.key for p in get_named_combinatorial_profiles()}
        assert "standard_simplex" in keys

    def test_sphere_triangulation_present(self):
        keys = {p.key for p in get_named_combinatorial_profiles()}
        assert "sphere_triangulation" in keys

    def test_torus_triangulation_present(self):
        keys = {p.key for p in get_named_combinatorial_profiles()}
        assert "torus_triangulation" in keys

    def test_real_projective_plane_present(self):
        keys = {p.key for p in get_named_combinatorial_profiles()}
        assert "real_projective_plane" in keys

    def test_dunce_hat_present(self):
        keys = {p.key for p in get_named_combinatorial_profiles()}
        assert "dunce_hat" in keys

    def test_nerve_good_cover_present(self):
        keys = {p.key for p in get_named_combinatorial_profiles()}
        assert "nerve_good_cover" in keys

    def test_klein_bottle_present(self):
        keys = {p.key for p in get_named_combinatorial_profiles()}
        assert "klein_bottle_complex" in keys

    # Standard simplex properties
    def test_standard_simplex_contractible(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "standard_simplex")
        assert p.is_contractible is True

    def test_standard_simplex_acyclic(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "standard_simplex")
        assert p.is_acyclic is True

    def test_standard_simplex_collapsible(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "standard_simplex")
        assert p.is_collapsible is True

    def test_standard_simplex_no_torsion(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "standard_simplex")
        assert p.has_torsion_in_homology is False

    def test_standard_simplex_euler_one(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "standard_simplex")
        assert p.euler_characteristic == 1

    # Sphere properties
    def test_sphere_not_contractible(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "sphere_triangulation")
        assert p.is_contractible is False

    def test_sphere_not_collapsible(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "sphere_triangulation")
        assert p.is_collapsible is False

    def test_sphere_no_torsion(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "sphere_triangulation")
        assert p.has_torsion_in_homology is False

    def test_sphere_euler_two(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "sphere_triangulation")
        assert p.euler_characteristic == 2

    # Torus properties
    def test_torus_euler_zero(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "torus_triangulation")
        assert p.euler_characteristic == 0

    def test_torus_no_torsion(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "torus_triangulation")
        assert p.has_torsion_in_homology is False

    def test_torus_betti_numbers(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "torus_triangulation")
        assert p.betti_numbers == (1, 2, 1)

    # RP² properties
    def test_rp2_has_torsion(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "real_projective_plane")
        assert p.has_torsion_in_homology is True

    def test_rp2_euler_one(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "real_projective_plane")
        assert p.euler_characteristic == 1

    # Dunce hat properties
    def test_dunce_hat_contractible(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "dunce_hat")
        assert p.is_contractible is True

    def test_dunce_hat_not_collapsible(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "dunce_hat")
        assert p.is_collapsible is False

    def test_dunce_hat_acyclic(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "dunce_hat")
        assert p.is_acyclic is True

    # Klein bottle properties
    def test_klein_bottle_has_torsion(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "klein_bottle_complex")
        assert p.has_torsion_in_homology is True

    def test_klein_bottle_euler_zero(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "klein_bottle_complex")
        assert p.euler_characteristic == 0

    def test_klein_bottle_betti_numbers(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "klein_bottle_complex")
        assert p.betti_numbers == (1, 1, 0)

    # Nerve profile
    def test_nerve_profile_euler_none(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "nerve_good_cover")
        assert p.euler_characteristic is None

    def test_nerve_profile_no_torsion(self):
        p = next(p for p in get_named_combinatorial_profiles() if p.key == "nerve_good_cover")
        assert p.has_torsion_in_homology is False

    def test_all_betti_numbers_nonneg(self):
        for p in get_named_combinatorial_profiles():
            for b in p.betti_numbers:
                assert b >= 0


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(combinatorial_layer_summary(), dict)

    def test_layer_summary_has_main_text(self):
        assert "main_text" in combinatorial_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in combinatorial_layer_summary()

    def test_layer_summary_counts_match_profiles(self):
        profiles = get_named_combinatorial_profiles()
        summary = combinatorial_layer_summary()
        assert sum(summary.values()) == len(profiles)

    def test_chapter_index_returns_dict(self):
        assert isinstance(combinatorial_chapter_index(), dict)

    def test_chapter_index_keys_are_sorted(self):
        ch = combinatorial_chapter_index()
        assert list(ch.keys()) == sorted(ch.keys())

    def test_chapter_index_values_are_tuples(self):
        for v in combinatorial_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_no_empty_tuples(self):
        for v in combinatorial_chapter_index().values():
            assert len(v) >= 1

    def test_type_index_returns_dict(self):
        assert isinstance(combinatorial_type_index(), dict)

    def test_type_index_has_simplicial(self):
        assert "simplicial_complex" in combinatorial_type_index()

    def test_type_index_values_are_tuples(self):
        for v in combinatorial_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_covers_all_profiles(self):
        total = sum(len(v) for v in combinatorial_type_index().values())
        assert total == len(get_named_combinatorial_profiles())


# ---------------------------------------------------------------------------
# is_contractible_complex
# ---------------------------------------------------------------------------

class TestIsContractible:
    def test_contractible_tag_true(self):
        r = is_contractible_complex(_space("contractible"))
        assert r.is_true

    def test_cone_tag_true(self):
        r = is_contractible_complex(_space("cone"))
        assert r.is_true

    def test_collapsible_tag_true(self):
        r = is_contractible_complex(_space("collapsible"))
        assert r.is_true

    def test_tree_complex_tag_true(self):
        r = is_contractible_complex(_space("tree_complex"))
        assert r.is_true

    def test_star_tag_true(self):
        r = is_contractible_complex(_space("star"))
        assert r.is_true

    def test_sphere_false(self):
        r = is_contractible_complex(_space("sphere"))
        assert r.is_false

    def test_torus_false(self):
        r = is_contractible_complex(_space("torus"))
        assert r.is_false

    def test_projective_false(self):
        r = is_contractible_complex(_space("projective_space_complex"))
        assert r.is_false

    def test_non_contractible_tag_false(self):
        r = is_contractible_complex(_space("non_contractible"))
        assert r.is_false

    def test_non_trivial_pi1_false(self):
        r = is_contractible_complex(_space("non_trivial_fundamental_group"))
        assert r.is_false

    def test_unknown_empty_tags(self):
        r = is_contractible_complex(_space())
        assert not r.is_true and not r.is_false

    def test_unknown_irrelevant_tag(self):
        r = is_contractible_complex(_space("flag_complex"))
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        r = is_contractible_complex(_space("contractible"))
        assert r.justification

    def test_result_has_metadata(self):
        r = is_contractible_complex(_space("collapsible"))
        assert r.metadata is not None

    def test_mode_is_theorem_when_decided(self):
        r = is_contractible_complex(_space("contractible"))
        assert r.mode == "theorem"

    def test_mode_symbolic_when_unknown(self):
        r = is_contractible_complex(_space())
        assert r.mode == "symbolic"

    def test_npc_complex_contractible(self):
        r = is_contractible_complex(_space("npc_complex"))
        assert r.is_true

    def test_simply_connected_acyclic_contractible(self):
        r = is_contractible_complex(_space("simply_connected_acyclic"))
        assert r.is_true

    def test_closed_orientable_manifold_false(self):
        r = is_contractible_complex(_space("closed_orientable_manifold"))
        assert r.is_false

    def test_klein_bottle_false(self):
        r = is_contractible_complex(_space("klein_bottle_complex"))
        assert r.is_false


# ---------------------------------------------------------------------------
# is_acyclic_complex
# ---------------------------------------------------------------------------

class TestIsAcyclic:
    def test_acyclic_complex_tag_true(self):
        r = is_acyclic_complex(_space("acyclic_complex"))
        assert r.is_true

    def test_acyclic_homology_tag_true(self):
        r = is_acyclic_complex(_space("acyclic_homology"))
        assert r.is_true

    def test_trivial_reduced_homology_true(self):
        r = is_acyclic_complex(_space("trivial_reduced_homology"))
        assert r.is_true

    def test_contractible_implies_acyclic(self):
        r = is_acyclic_complex(_space("contractible"))
        assert r.is_true

    def test_collapsible_implies_acyclic(self):
        r = is_acyclic_complex(_space("collapsible"))
        assert r.is_true

    def test_cone_implies_acyclic(self):
        r = is_acyclic_complex(_space("cone"))
        assert r.is_true

    def test_sphere_false(self):
        r = is_acyclic_complex(_space("sphere"))
        assert r.is_false

    def test_torus_false(self):
        r = is_acyclic_complex(_space("torus"))
        assert r.is_false

    def test_projective_false(self):
        r = is_acyclic_complex(_space("projective_space_complex"))
        assert r.is_false

    def test_nontrivial_homology_false(self):
        r = is_acyclic_complex(_space("nontrivial_homology"))
        assert r.is_false

    def test_unknown_empty(self):
        r = is_acyclic_complex(_space())
        assert not r.is_true and not r.is_false

    def test_result_justification(self):
        r = is_acyclic_complex(_space("contractible"))
        assert "acyclic" in r.justification[0].lower()

    def test_explicit_criterion(self):
        r = is_acyclic_complex(_space("acyclic_complex"))
        assert r.metadata.get("criterion") == "explicit_acyclic"

    def test_contractible_criterion(self):
        r = is_acyclic_complex(_space("contractible"))
        assert r.metadata.get("criterion") == "contractible_implies_acyclic"

    def test_klein_bottle_false(self):
        r = is_acyclic_complex(_space("klein_bottle_complex"))
        assert r.is_false

    def test_sphere_triangulation_false(self):
        r = is_acyclic_complex(_space("sphere_triangulation"))
        assert r.is_false

    def test_torus_triangulation_false(self):
        r = is_acyclic_complex(_space("torus_triangulation"))
        assert r.is_false

    def test_star_implies_acyclic(self):
        r = is_acyclic_complex(_space("star"))
        assert r.is_true

    def test_tree_complex_implies_acyclic(self):
        r = is_acyclic_complex(_space("tree_complex"))
        assert r.is_true


# ---------------------------------------------------------------------------
# has_torsion_homology
# ---------------------------------------------------------------------------

class TestHasTorsionHomology:
    def test_torsion_homology_tag_true(self):
        r = has_torsion_homology(_space("torsion_homology"))
        assert r.is_true

    def test_z2_torsion_true(self):
        r = has_torsion_homology(_space("z2_torsion"))
        assert r.is_true

    def test_non_orientable_true(self):
        r = has_torsion_homology(_space("non_orientable"))
        assert r.is_true

    def test_projective_space_complex_true(self):
        r = has_torsion_homology(_space("projective_space_complex"))
        assert r.is_true

    def test_lens_space_complex_true(self):
        r = has_torsion_homology(_space("lens_space_complex"))
        assert r.is_true

    def test_klein_bottle_complex_true(self):
        r = has_torsion_homology(_space("klein_bottle_complex"))
        assert r.is_true

    def test_non_orientable_closed_true(self):
        r = has_torsion_homology(_space("non_orientable_closed"))
        assert r.is_true

    def test_sphere_false(self):
        r = has_torsion_homology(_space("sphere"))
        assert r.is_false

    def test_torus_false(self):
        r = has_torsion_homology(_space("torus"))
        assert r.is_false

    def test_orientable_surface_false(self):
        r = has_torsion_homology(_space("orientable_closed_surface"))
        assert r.is_false

    def test_contractible_false(self):
        r = has_torsion_homology(_space("contractible"))
        assert r.is_false

    def test_torsion_free_tag_false(self):
        r = has_torsion_homology(_space("torsion_free_homology"))
        assert r.is_false

    def test_unknown_empty(self):
        r = has_torsion_homology(_space())
        assert not r.is_true and not r.is_false

    def test_result_mode_theorem_when_decided(self):
        r = has_torsion_homology(_space("torsion_homology"))
        assert r.mode == "theorem"

    def test_torsion_criterion_explicit(self):
        r = has_torsion_homology(_space("torsion_homology"))
        assert r.metadata.get("criterion") == "explicit_torsion"

    def test_torsion_free_criterion(self):
        r = has_torsion_homology(_space("sphere"))
        assert r.metadata.get("criterion") == "torsion_free"

    def test_sphere_triangulation_false(self):
        r = has_torsion_homology(_space("sphere_triangulation"))
        assert r.is_false

    def test_torus_triangulation_false(self):
        r = has_torsion_homology(_space("torus_triangulation"))
        assert r.is_false

    def test_torsion_in_h1_true(self):
        r = has_torsion_homology(_space("torsion_in_h1"))
        assert r.is_true


# ---------------------------------------------------------------------------
# is_collapsible_complex
# ---------------------------------------------------------------------------

class TestIsCollapsible:
    def test_collapsible_tag_true(self):
        r = is_collapsible_complex(_space("collapsible"))
        assert r.is_true

    def test_shellable_tag_true(self):
        r = is_collapsible_complex(_space("shellable"))
        assert r.is_true

    def test_cone_tag_true(self):
        r = is_collapsible_complex(_space("cone"))
        assert r.is_true

    def test_star_tag_true(self):
        r = is_collapsible_complex(_space("star"))
        assert r.is_true

    def test_tree_complex_tag_true(self):
        r = is_collapsible_complex(_space("tree_complex"))
        assert r.is_true

    def test_dunce_hat_false(self):
        r = is_collapsible_complex(_space("dunce_hat"))
        assert r.is_false

    def test_not_collapsible_tag_false(self):
        r = is_collapsible_complex(_space("not_collapsible"))
        assert r.is_false

    def test_bing_house_false(self):
        r = is_collapsible_complex(_space("bing_house"))
        assert r.is_false

    def test_non_shellable_false(self):
        r = is_collapsible_complex(_space("non_shellable"))
        assert r.is_false

    def test_sphere_false_via_not_contractible(self):
        r = is_collapsible_complex(_space("sphere"))
        assert r.is_false

    def test_torus_false_via_not_contractible(self):
        r = is_collapsible_complex(_space("torus"))
        assert r.is_false

    def test_projective_false_via_not_contractible(self):
        r = is_collapsible_complex(_space("projective_space_complex"))
        assert r.is_false

    def test_unknown_empty(self):
        r = is_collapsible_complex(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit_collapsible(self):
        r = is_collapsible_complex(_space("collapsible"))
        assert r.metadata.get("criterion") == "explicit_collapsible"

    def test_criterion_not_collapsible(self):
        r = is_collapsible_complex(_space("dunce_hat"))
        assert r.metadata.get("criterion") == "not_collapsible"

    def test_criterion_not_contractible_not_collapsible(self):
        r = is_collapsible_complex(_space("sphere"))
        assert r.metadata.get("criterion") == "not_contractible_not_collapsible"

    def test_contractible_not_collapsible_tag_false(self):
        r = is_collapsible_complex(_space("contractible_not_collapsible"))
        assert r.is_false

    def test_convex_polytope_boundary_true(self):
        r = is_collapsible_complex(_space("convex_polytope_boundary"))
        assert r.is_true

    def test_non_contractible_tag_false(self):
        r = is_collapsible_complex(_space("non_contractible"))
        assert r.is_false


# ---------------------------------------------------------------------------
# classify_combinatorial
# ---------------------------------------------------------------------------

class TestClassifyCombinatorial:
    def test_returns_dict(self):
        r = classify_combinatorial(_space("contractible", "collapsible"))
        assert isinstance(r, dict)

    def test_required_keys_present(self):
        r = classify_combinatorial(_space())
        required = {
            "combinatorial_class", "is_contractible", "is_acyclic",
            "has_torsion", "is_collapsible", "key_properties",
            "representation", "tags",
        }
        assert required <= r.keys()

    def test_contractible_collapsible_class(self):
        r = classify_combinatorial(_space("contractible", "collapsible"))
        assert r["combinatorial_class"] == "contractible_collapsible"

    def test_contractible_not_collapsible_class(self):
        r = classify_combinatorial(_space("dunce_hat", "contractible"))
        assert r["combinatorial_class"] == "contractible_not_collapsible"

    def test_acyclic_class_from_tag(self):
        r = classify_combinatorial(_space("acyclic_complex"))
        assert r["combinatorial_class"] == "acyclic"

    def test_torsion_class(self):
        r = classify_combinatorial(_space("torsion_homology", "non_contractible"))
        assert r["combinatorial_class"] == "torsion"

    def test_key_properties_list(self):
        r = classify_combinatorial(_space("contractible", "collapsible"))
        assert "contractible" in r["key_properties"]
        assert "collapsible" in r["key_properties"]

    def test_torsion_in_key_properties(self):
        r = classify_combinatorial(_space("torsion_homology"))
        assert "torsion_homology" in r["key_properties"]

    def test_nerve_in_key_properties(self):
        r = classify_combinatorial(_space("nerve_complex"))
        assert "nerve_theorem_applicable" in r["key_properties"]

    def test_cw_in_key_properties(self):
        r = classify_combinatorial(_space("cw_complex"))
        assert "cw_structure" in r["key_properties"]

    def test_tags_sorted(self):
        r = classify_combinatorial(_space("sphere", "acyclic_complex"))
        assert r["tags"] == sorted(r["tags"])

    def test_representation_passthrough(self):
        r = classify_combinatorial(_space("contractible", rep="test_rep"))
        assert r["representation"] == "test_rep"

    def test_unknown_class_empty_tags(self):
        r = classify_combinatorial(_space("cw_complex"))
        assert r["combinatorial_class"] in {
            "contractible_collapsible", "contractible_not_collapsible",
            "acyclic", "torsion", "free_homology", "unknown",
        }

    def test_not_contractible_in_properties(self):
        r = classify_combinatorial(_space("sphere"))
        assert "not_contractible" in r["key_properties"]

    def test_torsion_free_in_properties(self):
        r = classify_combinatorial(_space("sphere"))
        assert "torsion_free" in r["key_properties"]


# ---------------------------------------------------------------------------
# combinatorial_profile
# ---------------------------------------------------------------------------

class TestCombinatorialProfile:
    def test_returns_dict(self):
        r = combinatorial_profile(_space("contractible"))
        assert isinstance(r, dict)

    def test_has_classification_key(self):
        r = combinatorial_profile(_space("contractible"))
        assert "classification" in r

    def test_has_named_profiles_key(self):
        r = combinatorial_profile(_space("contractible"))
        assert "named_profiles" in r

    def test_has_layer_summary_key(self):
        r = combinatorial_profile(_space("contractible"))
        assert "layer_summary" in r

    def test_classification_is_dict(self):
        r = combinatorial_profile(_space("contractible"))
        assert isinstance(r["classification"], dict)

    def test_named_profiles_is_tuple(self):
        r = combinatorial_profile(_space("contractible"))
        assert isinstance(r["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        r = combinatorial_profile(_space("contractible"))
        assert isinstance(r["layer_summary"], dict)

    def test_named_profiles_nonempty(self):
        r = combinatorial_profile(_space("contractible"))
        assert len(r["named_profiles"]) >= 6

    def test_classification_contains_class_key(self):
        r = combinatorial_profile(_space("contractible", "collapsible"))
        assert "combinatorial_class" in r["classification"]


# ---------------------------------------------------------------------------
# CombinatorialProfile dataclass
# ---------------------------------------------------------------------------

class TestCombinatorialProfileDataclass:
    def test_frozen(self):
        p = CombinatorialProfile(
            key="test", display_name="Test", complex_type="simplicial_complex",
            euler_characteristic=0, is_contractible=False, is_acyclic=False,
            has_torsion_in_homology=False, is_collapsible=False,
            betti_numbers=(1,), presentation_layer="main_text",
            focus="test focus", chapter_targets=("1",),
        )
        with pytest.raises(Exception):
            p.key = "other"  # type: ignore[misc]

    def test_equality_by_value(self):
        kwargs = dict(
            key="t", display_name="T", complex_type="simplicial_complex",
            euler_characteristic=1, is_contractible=True, is_acyclic=True,
            has_torsion_in_homology=False, is_collapsible=True,
            betti_numbers=(1,), presentation_layer="main_text",
            focus="f", chapter_targets=("1",),
        )
        assert CombinatorialProfile(**kwargs) == CombinatorialProfile(**kwargs)

    def test_euler_characteristic_can_be_none(self):
        p = CombinatorialProfile(
            key="n", display_name="N", complex_type="simplicial_complex",
            euler_characteristic=None, is_contractible=False, is_acyclic=False,
            has_torsion_in_homology=False, is_collapsible=False,
            betti_numbers=(), presentation_layer="main_text",
            focus="nerve", chapter_targets=("1",),
        )
        assert p.euler_characteristic is None

    def test_betti_numbers_empty_tuple(self):
        p = CombinatorialProfile(
            key="n", display_name="N", complex_type="simplicial_complex",
            euler_characteristic=None, is_contractible=False, is_acyclic=False,
            has_torsion_in_homology=False, is_collapsible=False,
            betti_numbers=(), presentation_layer="main_text",
            focus="nerve", chapter_targets=("1",),
        )
        assert p.betti_numbers == ()
