"""Tests for pytop.foliations."""

from __future__ import annotations

import pytest

from pytop.foliations import (
    COMPACT_LEAF_TAGS,
    FROBENIUS_THEOREM_TAGS,
    GODBILLON_VEY_TAGS,
    HOLONOMY_TAGS,
    LEAF_SPACE_TAGS,
    REEB_FOLIATION_TAGS,
    TAUT_FOLIATION_TAGS,
    TRANSVERSE_GEOMETRY_TAGS,
    FoliationProfile,
    classify_foliation,
    foliation_chapter_index,
    foliation_layer_summary,
    foliation_profile,
    foliation_type_index,
    get_named_foliation_profiles,
    has_compact_leaf,
    has_trivial_holonomy,
    is_frobenius_integrable,
    is_taut_foliation,
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
    def test_frobenius_tags_nonempty(self):
        assert len(FROBENIUS_THEOREM_TAGS) >= 4

    def test_compact_leaf_tags_nonempty(self):
        assert len(COMPACT_LEAF_TAGS) >= 4

    def test_reeb_foliation_tags_nonempty(self):
        assert len(REEB_FOLIATION_TAGS) >= 4

    def test_transverse_geometry_tags_nonempty(self):
        assert len(TRANSVERSE_GEOMETRY_TAGS) >= 4

    def test_holonomy_tags_nonempty(self):
        assert len(HOLONOMY_TAGS) >= 4

    def test_taut_foliation_tags_nonempty(self):
        assert len(TAUT_FOLIATION_TAGS) >= 4

    def test_godbillon_vey_tags_nonempty(self):
        assert len(GODBILLON_VEY_TAGS) >= 4

    def test_leaf_space_tags_nonempty(self):
        assert len(LEAF_SPACE_TAGS) >= 4

    def test_frobenius_theorem_in_frobenius_tags(self):
        assert "frobenius_theorem" in FROBENIUS_THEOREM_TAGS

    def test_involutive_distribution_in_frobenius_tags(self):
        assert "involutive_distribution" in FROBENIUS_THEOREM_TAGS

    def test_compact_leaf_in_compact_tags(self):
        assert "compact_leaf" in COMPACT_LEAF_TAGS

    def test_novikov_theorem_in_compact_tags(self):
        assert "novikov_theorem" in COMPACT_LEAF_TAGS

    def test_reeb_foliation_in_reeb_tags(self):
        assert "reeb_foliation" in REEB_FOLIATION_TAGS

    def test_reeb_component_in_reeb_tags(self):
        assert "reeb_component" in REEB_FOLIATION_TAGS

    def test_riemannian_foliation_in_transverse_tags(self):
        assert "riemannian_foliation" in TRANSVERSE_GEOMETRY_TAGS

    def test_molino_theorem_in_transverse_tags(self):
        assert "molino_theorem" in TRANSVERSE_GEOMETRY_TAGS

    def test_trivial_holonomy_in_holonomy_tags(self):
        assert "trivial_holonomy" in HOLONOMY_TAGS

    def test_holonomy_group_in_holonomy_tags(self):
        assert "holonomy_group" in HOLONOMY_TAGS

    def test_taut_foliation_in_taut_tags(self):
        assert "taut_foliation" in TAUT_FOLIATION_TAGS

    def test_closed_transversal_in_taut_tags(self):
        assert "closed_transversal" in TAUT_FOLIATION_TAGS

    def test_godbillon_vey_in_gv_tags(self):
        assert "godbillon_vey" in GODBILLON_VEY_TAGS

    def test_secondary_characteristic_class_in_gv_tags(self):
        assert "secondary_characteristic_class" in GODBILLON_VEY_TAGS

    def test_leaf_space_in_leaf_space_tags(self):
        assert "leaf_space" in LEAF_SPACE_TAGS

    def test_foliation_groupoid_in_leaf_space_tags(self):
        assert "foliation_groupoid" in LEAF_SPACE_TAGS

    def test_all_tag_sets_contain_strings(self):
        for tag_set in [
            FROBENIUS_THEOREM_TAGS, COMPACT_LEAF_TAGS, REEB_FOLIATION_TAGS,
            TRANSVERSE_GEOMETRY_TAGS, HOLONOMY_TAGS, TAUT_FOLIATION_TAGS,
            GODBILLON_VEY_TAGS, LEAF_SPACE_TAGS,
        ]:
            assert all(isinstance(t, str) for t in tag_set)

    def test_reeb_and_taut_disjoint(self):
        assert REEB_FOLIATION_TAGS.isdisjoint(TAUT_FOLIATION_TAGS)

    def test_compact_and_taut_disjoint(self):
        assert COMPACT_LEAF_TAGS.isdisjoint(TAUT_FOLIATION_TAGS)


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_foliation_profiles(), tuple)

    def test_at_least_six_profiles(self):
        assert len(get_named_foliation_profiles()) >= 6

    def test_exactly_seven_profiles(self):
        assert len(get_named_foliation_profiles()) == 7

    def test_all_foliation_profile_instances(self):
        for p in get_named_foliation_profiles():
            assert isinstance(p, FoliationProfile)

    def test_keys_unique(self):
        keys = [p.key for p in get_named_foliation_profiles()]
        assert len(keys) == len(set(keys))

    def test_display_names_nonempty(self):
        for p in get_named_foliation_profiles():
            assert p.display_name.strip()

    def test_focus_nonempty(self):
        for p in get_named_foliation_profiles():
            assert p.focus.strip()

    def test_chapter_targets_nonempty(self):
        for p in get_named_foliation_profiles():
            assert len(p.chapter_targets) >= 1

    def test_presentation_layers_known(self):
        known = {"main_text", "selected_block", "appendix"}
        for p in get_named_foliation_profiles():
            assert p.presentation_layer in known

    def test_codimension_strings(self):
        for p in get_named_foliation_profiles():
            assert isinstance(p.codimension, str)

    def test_is_taut_bool(self):
        for p in get_named_foliation_profiles():
            assert isinstance(p.is_taut, bool)

    def test_has_compact_leaf_bool(self):
        for p in get_named_foliation_profiles():
            assert isinstance(p.has_compact_leaf, bool)

    # reeb_foliation_s3
    def test_reeb_s3_present(self):
        assert "reeb_foliation_s3" in {p.key for p in get_named_foliation_profiles()}

    def test_reeb_s3_has_compact_leaf(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "reeb_foliation_s3")
        assert p.has_compact_leaf is True

    def test_reeb_s3_not_taut(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "reeb_foliation_s3")
        assert p.is_taut is False

    def test_reeb_s3_codimension(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "reeb_foliation_s3")
        assert p.codimension == "1"

    def test_reeb_s3_non_trivial_holonomy(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "reeb_foliation_s3")
        assert p.holonomy_type == "non_trivial"

    # frobenius_integrable
    def test_frobenius_integrable_present(self):
        assert "frobenius_integrable" in {p.key for p in get_named_foliation_profiles()}

    def test_frobenius_integrable_no_compact_leaf(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "frobenius_integrable")
        assert p.has_compact_leaf is False

    # kronecker_foliation_torus
    def test_kronecker_present(self):
        assert "kronecker_foliation_torus" in {p.key for p in get_named_foliation_profiles()}

    def test_kronecker_no_compact_leaf(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "kronecker_foliation_torus")
        assert p.has_compact_leaf is False

    def test_kronecker_is_taut(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "kronecker_foliation_torus")
        assert p.is_taut is True

    def test_kronecker_trivial_holonomy(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "kronecker_foliation_torus")
        assert p.holonomy_type == "trivial"

    # taut_foliation_3manifold
    def test_taut_3manifold_present(self):
        assert "taut_foliation_3manifold" in {p.key for p in get_named_foliation_profiles()}

    def test_taut_3manifold_is_taut(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "taut_foliation_3manifold")
        assert p.is_taut is True

    def test_taut_3manifold_no_compact_leaf(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "taut_foliation_3manifold")
        assert p.has_compact_leaf is False

    # riemannian_foliation
    def test_riemannian_present(self):
        assert "riemannian_foliation" in {p.key for p in get_named_foliation_profiles()}

    def test_riemannian_trivial_holonomy(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "riemannian_foliation")
        assert p.holonomy_type == "trivial"

    def test_riemannian_type(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "riemannian_foliation")
        assert p.foliation_type == "riemannian"

    # godbillon_vey_example
    def test_gv_present(self):
        assert "godbillon_vey_example" in {p.key for p in get_named_foliation_profiles()}

    def test_gv_codimension_1(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "godbillon_vey_example")
        assert p.codimension == "1"

    def test_gv_non_trivial_holonomy(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "godbillon_vey_example")
        assert p.holonomy_type == "non_trivial"

    # haefliger_classifying_space
    def test_haefliger_present(self):
        assert "haefliger_classifying_space" in {p.key for p in get_named_foliation_profiles()}

    def test_haefliger_classifying_type(self):
        p = next(p for p in get_named_foliation_profiles() if p.key == "haefliger_classifying_space")
        assert p.foliation_type == "classifying"


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_is_dict(self):
        assert isinstance(foliation_layer_summary(), dict)

    def test_layer_summary_has_main_text(self):
        assert "main_text" in foliation_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in foliation_layer_summary()

    def test_layer_summary_total(self):
        profiles = get_named_foliation_profiles()
        assert sum(foliation_layer_summary().values()) == len(profiles)

    def test_chapter_index_is_dict(self):
        assert isinstance(foliation_chapter_index(), dict)

    def test_chapter_index_sorted(self):
        ch = foliation_chapter_index()
        assert list(ch.keys()) == sorted(ch.keys())

    def test_chapter_index_tuples(self):
        for v in foliation_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_nonempty_values(self):
        for v in foliation_chapter_index().values():
            assert len(v) >= 1

    def test_type_index_is_dict(self):
        assert isinstance(foliation_type_index(), dict)

    def test_type_index_has_reeb(self):
        assert "reeb" in foliation_type_index()

    def test_type_index_has_riemannian(self):
        assert "riemannian" in foliation_type_index()

    def test_type_index_tuples(self):
        for v in foliation_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_total(self):
        total = sum(len(v) for v in foliation_type_index().values())
        assert total == len(get_named_foliation_profiles())


# ---------------------------------------------------------------------------
# is_frobenius_integrable
# ---------------------------------------------------------------------------

class TestIsFrobeniusIntegrable:
    def test_frobenius_theorem_tag_true(self):
        assert is_frobenius_integrable(_space("frobenius_theorem")).is_true

    def test_involutive_distribution_true(self):
        assert is_frobenius_integrable(_space("involutive_distribution")).is_true

    def test_integrable_distribution_true(self):
        assert is_frobenius_integrable(_space("integrable_distribution")).is_true

    def test_frobenius_integrability_true(self):
        assert is_frobenius_integrable(_space("frobenius_integrability")).is_true

    def test_cartan_frobenius_true(self):
        assert is_frobenius_integrable(_space("cartan_frobenius")).is_true

    def test_lie_bracket_closed_true(self):
        assert is_frobenius_integrable(_space("lie_bracket_closed")).is_true

    def test_foliation_tag_true(self):
        assert is_frobenius_integrable(_space("foliation")).is_true

    def test_taut_foliation_tag_true(self):
        assert is_frobenius_integrable(_space("taut_foliation")).is_true

    def test_reeb_foliation_tag_true(self):
        assert is_frobenius_integrable(_space("reeb_foliation")).is_true

    def test_riemannian_foliation_tag_true(self):
        assert is_frobenius_integrable(_space("riemannian_foliation")).is_true

    def test_linear_foliation_true(self):
        assert is_frobenius_integrable(_space("linear_foliation")).is_true

    def test_kronecker_foliation_true(self):
        assert is_frobenius_integrable(_space("kronecker_foliation")).is_true

    def test_godbillon_vey_true(self):
        assert is_frobenius_integrable(_space("godbillon_vey")).is_true

    def test_contact_distribution_false(self):
        assert is_frobenius_integrable(_space("contact_distribution")).is_false

    def test_contact_structure_false(self):
        assert is_frobenius_integrable(_space("contact_structure")).is_false

    def test_non_integrable_false(self):
        assert is_frobenius_integrable(_space("non_integrable")).is_false

    def test_maximally_non_integrable_false(self):
        assert is_frobenius_integrable(_space("maximally_non_integrable")).is_false

    def test_sub_riemannian_false(self):
        assert is_frobenius_integrable(_space("sub_riemannian")).is_false

    def test_unknown_empty(self):
        r = is_frobenius_integrable(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert is_frobenius_integrable(_space("frobenius_theorem")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_frobenius_integrable(_space("contact_structure")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert is_frobenius_integrable(_space()).mode == "symbolic"

    def test_criterion_explicit_frobenius(self):
        r = is_frobenius_integrable(_space("frobenius_theorem"))
        assert r.metadata.get("criterion") == "explicit_frobenius"

    def test_criterion_foliation_implies_integrable(self):
        r = is_frobenius_integrable(_space("foliation"))
        assert r.metadata.get("criterion") == "foliation_implies_integrable"

    def test_criterion_not_integrable(self):
        r = is_frobenius_integrable(_space("contact_distribution"))
        assert r.metadata.get("criterion") == "not_integrable"

    def test_distribution_integrable_tag_true(self):
        assert is_frobenius_integrable(_space("distribution_integrable")).is_true

    def test_fibration_foliation_true(self):
        assert is_frobenius_integrable(_space("fibration_foliation")).is_true


# ---------------------------------------------------------------------------
# has_compact_leaf
# ---------------------------------------------------------------------------

class TestHasCompactLeaf:
    def test_compact_leaf_tag_true(self):
        assert has_compact_leaf(_space("compact_leaf")).is_true

    def test_closed_leaf_true(self):
        assert has_compact_leaf(_space("closed_leaf")).is_true

    def test_novikov_theorem_true(self):
        assert has_compact_leaf(_space("novikov_theorem")).is_true

    def test_compact_torus_leaf_true(self):
        assert has_compact_leaf(_space("compact_torus_leaf")).is_true

    def test_closed_surface_leaf_true(self):
        assert has_compact_leaf(_space("closed_surface_leaf")).is_true

    def test_novikov_compact_true(self):
        assert has_compact_leaf(_space("novikov_compact")).is_true

    def test_reeb_foliation_true(self):
        assert has_compact_leaf(_space("reeb_foliation")).is_true

    def test_reeb_component_true(self):
        assert has_compact_leaf(_space("reeb_component")).is_true

    def test_reeb_s3_true(self):
        assert has_compact_leaf(_space("reeb_s3")).is_true

    def test_reeb_torus_leaf_true(self):
        assert has_compact_leaf(_space("reeb_torus_leaf")).is_true

    def test_no_compact_leaf_false(self):
        assert has_compact_leaf(_space("no_compact_leaf")).is_false

    def test_all_leaves_dense_false(self):
        assert has_compact_leaf(_space("all_leaves_dense")).is_false

    def test_irrational_kronecker_false(self):
        assert has_compact_leaf(_space("irrational_kronecker")).is_false

    def test_all_leaves_noncompact_false(self):
        assert has_compact_leaf(_space("all_leaves_noncompact")).is_false

    def test_dense_leaves_false(self):
        assert has_compact_leaf(_space("dense_leaves")).is_false

    def test_unknown_empty(self):
        r = has_compact_leaf(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert has_compact_leaf(_space("compact_leaf")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert has_compact_leaf(_space("no_compact_leaf")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert has_compact_leaf(_space()).mode == "symbolic"

    def test_criterion_explicit_compact_leaf(self):
        r = has_compact_leaf(_space("compact_leaf"))
        assert r.metadata.get("criterion") == "explicit_compact_leaf"

    def test_criterion_reeb_compact_torus(self):
        r = has_compact_leaf(_space("reeb_foliation"))
        assert r.metadata.get("criterion") == "reeb_compact_torus"

    def test_criterion_no_compact_leaf(self):
        r = has_compact_leaf(_space("no_compact_leaf"))
        assert r.metadata.get("criterion") == "no_compact_leaf"

    def test_spiraling_leaves_true(self):
        assert has_compact_leaf(_space("spiraling_leaves")).is_true

    def test_heegaard_foliation_true(self):
        assert has_compact_leaf(_space("heegaard_foliation")).is_true


# ---------------------------------------------------------------------------
# is_taut_foliation
# ---------------------------------------------------------------------------

class TestIsTautFoliation:
    def test_taut_foliation_tag_true(self):
        assert is_taut_foliation(_space("taut_foliation")).is_true

    def test_closed_transversal_true(self):
        assert is_taut_foliation(_space("closed_transversal")).is_true

    def test_sullivan_taut_true(self):
        assert is_taut_foliation(_space("sullivan_taut")).is_true

    def test_thurston_norm_true(self):
        assert is_taut_foliation(_space("thurston_norm")).is_true

    def test_volume_minimizing_leaf_true(self):
        assert is_taut_foliation(_space("volume_minimizing_leaf")).is_true

    def test_gabai_taut_true(self):
        assert is_taut_foliation(_space("gabai_taut")).is_true

    def test_homologically_nontrivial_leaf_true(self):
        assert is_taut_foliation(_space("homologically_nontrivial_leaf")).is_true

    def test_kronecker_foliation_true(self):
        assert is_taut_foliation(_space("kronecker_foliation")).is_true

    def test_linear_foliation_true(self):
        assert is_taut_foliation(_space("linear_foliation")).is_true

    def test_irrational_slope_true(self):
        assert is_taut_foliation(_space("irrational_slope")).is_true

    def test_reeb_foliation_false(self):
        assert is_taut_foliation(_space("reeb_foliation")).is_false

    def test_reeb_component_false(self):
        assert is_taut_foliation(_space("reeb_component")).is_false

    def test_reeb_s3_false(self):
        assert is_taut_foliation(_space("reeb_s3")).is_false

    def test_spiraling_leaves_false(self):
        assert is_taut_foliation(_space("spiraling_leaves")).is_false

    def test_not_taut_false(self):
        assert is_taut_foliation(_space("not_taut")).is_false

    def test_unknown_empty(self):
        r = is_taut_foliation(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert is_taut_foliation(_space("taut_foliation")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_taut_foliation(_space("reeb_foliation")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert is_taut_foliation(_space()).mode == "symbolic"

    def test_criterion_explicit_taut(self):
        r = is_taut_foliation(_space("taut_foliation"))
        assert r.metadata.get("criterion") == "explicit_taut"

    def test_criterion_kronecker_taut(self):
        r = is_taut_foliation(_space("kronecker_foliation"))
        assert r.metadata.get("criterion") == "kronecker_taut"

    def test_criterion_reeb_not_taut(self):
        r = is_taut_foliation(_space("reeb_foliation"))
        assert r.metadata.get("criterion") == "reeb_not_taut"

    def test_heegaard_foliation_not_true(self):
        assert not is_taut_foliation(_space("heegaard_foliation")).is_true


# ---------------------------------------------------------------------------
# has_trivial_holonomy
# ---------------------------------------------------------------------------

class TestHasTrivialHolonomy:
    def test_trivial_holonomy_tag_true(self):
        assert has_trivial_holonomy(_space("trivial_holonomy")).is_true

    def test_riemannian_foliation_true(self):
        assert has_trivial_holonomy(_space("riemannian_foliation")).is_true

    def test_transversely_riemannian_true(self):
        assert has_trivial_holonomy(_space("transversely_riemannian")).is_true

    def test_molino_theorem_true(self):
        assert has_trivial_holonomy(_space("molino_theorem")).is_true

    def test_holonomy_invariant_metric_true(self):
        assert has_trivial_holonomy(_space("holonomy_invariant_metric")).is_true

    def test_transverse_metric_true(self):
        assert has_trivial_holonomy(_space("transverse_metric")).is_true

    def test_kronecker_foliation_true(self):
        assert has_trivial_holonomy(_space("kronecker_foliation")).is_true

    def test_linear_foliation_true(self):
        assert has_trivial_holonomy(_space("linear_foliation")).is_true

    def test_irrational_kronecker_true(self):
        assert has_trivial_holonomy(_space("irrational_kronecker")).is_true

    def test_irrational_slope_true(self):
        assert has_trivial_holonomy(_space("irrational_slope")).is_true

    def test_non_trivial_holonomy_false(self):
        assert has_trivial_holonomy(_space("non_trivial_holonomy")).is_false

    def test_holonomy_germ_false(self):
        assert has_trivial_holonomy(_space("holonomy_germ")).is_false

    def test_reeb_foliation_false(self):
        assert has_trivial_holonomy(_space("reeb_foliation")).is_false

    def test_reeb_component_false(self):
        assert has_trivial_holonomy(_space("reeb_component")).is_false

    def test_reeb_s3_false(self):
        assert has_trivial_holonomy(_space("reeb_s3")).is_false

    def test_spiraling_leaves_false(self):
        assert has_trivial_holonomy(_space("spiraling_leaves")).is_false

    def test_unknown_empty(self):
        r = has_trivial_holonomy(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert has_trivial_holonomy(_space("trivial_holonomy")).mode == "theorem"

    def test_mode_theorem_riemannian(self):
        assert has_trivial_holonomy(_space("riemannian_foliation")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert has_trivial_holonomy(_space("reeb_foliation")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert has_trivial_holonomy(_space()).mode == "symbolic"

    def test_criterion_explicit_trivial_holonomy(self):
        r = has_trivial_holonomy(_space("trivial_holonomy"))
        assert r.metadata.get("criterion") == "explicit_trivial_holonomy"

    def test_criterion_riemannian_trivial_holonomy(self):
        r = has_trivial_holonomy(_space("riemannian_foliation"))
        assert r.metadata.get("criterion") == "riemannian_trivial_holonomy"

    def test_criterion_kronecker_trivial_holonomy(self):
        r = has_trivial_holonomy(_space("kronecker_foliation"))
        assert r.metadata.get("criterion") == "kronecker_trivial_holonomy"

    def test_criterion_non_trivial_holonomy(self):
        r = has_trivial_holonomy(_space("reeb_foliation"))
        assert r.metadata.get("criterion") == "non_trivial_holonomy"

    def test_transversely_flat_true(self):
        assert has_trivial_holonomy(_space("transversely_flat")).is_true

    def test_transversely_projective_true(self):
        assert has_trivial_holonomy(_space("transversely_projective")).is_true


# ---------------------------------------------------------------------------
# classify_foliation
# ---------------------------------------------------------------------------

class TestClassifyFoliation:
    def test_returns_dict(self):
        assert isinstance(classify_foliation(_space()), dict)

    def test_required_keys(self):
        r = classify_foliation(_space())
        assert {
            "foliation_class", "is_frobenius_integrable", "has_compact_leaf",
            "is_taut_foliation", "has_trivial_holonomy",
            "key_properties", "representation", "tags",
        } <= r.keys()

    def test_taut_trivial_holonomy_class(self):
        r = classify_foliation(_space("taut_foliation", "trivial_holonomy"))
        assert r["foliation_class"] == "taut_trivial_holonomy"

    def test_riemannian_class(self):
        r = classify_foliation(_space("riemannian_foliation"))
        assert r["foliation_class"] == "riemannian"

    def test_reeb_type_class(self):
        r = classify_foliation(_space("reeb_foliation"))
        assert r["foliation_class"] == "reeb_type"

    def test_compact_leaf_nontrivial_class(self):
        r = classify_foliation(_space("compact_leaf", "non_trivial_holonomy"))
        assert r["foliation_class"] == "compact_leaf_nontrivial"

    def test_general_foliation_class(self):
        r = classify_foliation(_space("frobenius_theorem"))
        assert r["foliation_class"] == "general_foliation"

    def test_frobenius_integrable_in_properties(self):
        r = classify_foliation(_space("frobenius_theorem"))
        assert "frobenius_integrable" in r["key_properties"]

    def test_compact_leaf_in_properties(self):
        r = classify_foliation(_space("compact_leaf"))
        assert "compact_leaf" in r["key_properties"]

    def test_no_compact_leaf_in_properties(self):
        r = classify_foliation(_space("no_compact_leaf"))
        assert "no_compact_leaf" in r["key_properties"]

    def test_taut_in_properties(self):
        r = classify_foliation(_space("taut_foliation"))
        assert "taut" in r["key_properties"]

    def test_not_taut_in_properties(self):
        r = classify_foliation(_space("reeb_foliation"))
        assert "not_taut" in r["key_properties"]

    def test_trivial_holonomy_in_properties(self):
        r = classify_foliation(_space("trivial_holonomy"))
        assert "trivial_holonomy" in r["key_properties"]

    def test_non_trivial_holonomy_in_properties(self):
        r = classify_foliation(_space("non_trivial_holonomy"))
        assert "non_trivial_holonomy" in r["key_properties"]

    def test_riemannian_in_properties(self):
        r = classify_foliation(_space("riemannian_foliation"))
        assert "riemannian_foliation" in r["key_properties"]

    def test_godbillon_vey_in_properties(self):
        r = classify_foliation(_space("godbillon_vey"))
        assert "godbillon_vey" in r["key_properties"]

    def test_leaf_space_in_properties(self):
        r = classify_foliation(_space("leaf_space"))
        assert "leaf_space_structure" in r["key_properties"]

    def test_reeb_component_in_properties(self):
        r = classify_foliation(_space("reeb_component"))
        assert "reeb_component" in r["key_properties"]

    def test_tags_sorted(self):
        r = classify_foliation(_space("reeb_foliation", "compact_leaf"))
        assert r["tags"] == sorted(r["tags"])

    def test_representation_passthrough(self):
        r = classify_foliation(_space("foliation", rep="my_rep"))
        assert r["representation"] == "my_rep"

    def test_kronecker_taut_trivial(self):
        r = classify_foliation(_space("kronecker_foliation"))
        assert r["foliation_class"] == "taut_trivial_holonomy"

    def test_transversely_riemannian_class(self):
        r = classify_foliation(_space("transversely_riemannian"))
        assert r["foliation_class"] == "riemannian"


# ---------------------------------------------------------------------------
# foliation_profile
# ---------------------------------------------------------------------------

class TestFoliationProfile:
    def test_returns_dict(self):
        assert isinstance(foliation_profile(_space()), dict)

    def test_has_classification(self):
        assert "classification" in foliation_profile(_space())

    def test_has_named_profiles(self):
        assert "named_profiles" in foliation_profile(_space())

    def test_has_layer_summary(self):
        assert "layer_summary" in foliation_profile(_space())

    def test_classification_is_dict(self):
        assert isinstance(foliation_profile(_space())["classification"], dict)

    def test_named_profiles_is_tuple(self):
        assert isinstance(foliation_profile(_space())["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        assert isinstance(foliation_profile(_space())["layer_summary"], dict)

    def test_named_profiles_nonempty(self):
        assert len(foliation_profile(_space())["named_profiles"]) >= 6


# ---------------------------------------------------------------------------
# FoliationProfile dataclass
# ---------------------------------------------------------------------------

class TestFoliationProfileDataclass:
    def test_frozen(self):
        p = FoliationProfile(
            key="t", display_name="T", foliation_type="reeb",
            codimension="1", leaf_dimension="2",
            has_compact_leaf=True, is_taut=False, holonomy_type="non_trivial",
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        with pytest.raises(Exception):
            p.key = "other"  # type: ignore[misc]

    def test_equality_by_value(self):
        kwargs = dict(
            key="t", display_name="T", foliation_type="reeb",
            codimension="1", leaf_dimension="2",
            has_compact_leaf=True, is_taut=False, holonomy_type="non_trivial",
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        assert FoliationProfile(**kwargs) == FoliationProfile(**kwargs)

    def test_all_fields_accessible(self):
        p = FoliationProfile(
            key="x", display_name="X", foliation_type="taut",
            codimension="1", leaf_dimension="2",
            has_compact_leaf=False, is_taut=True, holonomy_type="trivial",
            presentation_layer="selected_block", focus="taut", chapter_targets=("14", "24"),
        )
        assert p.is_taut is True
        assert p.has_compact_leaf is False
        assert p.chapter_targets == ("14", "24")

    def test_inequality_on_different_keys(self):
        def _make(key: str) -> FoliationProfile:
            return FoliationProfile(
                key=key, display_name="T", foliation_type="reeb",
                codimension="1", leaf_dimension="2",
                has_compact_leaf=True, is_taut=False, holonomy_type="non_trivial",
                presentation_layer="main_text", focus="f", chapter_targets=("1",),
            )
        assert _make("a") != _make("b")
