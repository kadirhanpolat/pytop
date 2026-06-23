"""Tests for pytop.symplectic_topology."""

from __future__ import annotations

import pytest

from pytop.symplectic_topology import (
    COTANGENT_BUNDLE_TAGS,
    DARBOUX_THEOREM_TAGS,
    GROMOV_NONSQUEEZING_TAGS,
    HAMILTONIAN_TAGS,
    KAHLER_TAGS,
    LAGRANGIAN_TAGS,
    MOSER_THEOREM_TAGS,
    SYMPLECTOMORPHISM_TAGS,
    SymplecticProfile,
    admits_kahler_structure,
    classify_symplectic,
    get_named_symplectic_profiles,
    has_hamiltonian_structure,
    is_lagrangian_submanifold,
    is_symplectic_manifold,
    symplectic_chapter_index,
    symplectic_layer_summary,
    symplectic_profile,
    symplectic_type_index,
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
    def test_darboux_tags_nonempty(self):
        assert len(DARBOUX_THEOREM_TAGS) >= 4

    def test_hamiltonian_tags_nonempty(self):
        assert len(HAMILTONIAN_TAGS) >= 4

    def test_lagrangian_tags_nonempty(self):
        assert len(LAGRANGIAN_TAGS) >= 4

    def test_symplectomorphism_tags_nonempty(self):
        assert len(SYMPLECTOMORPHISM_TAGS) >= 4

    def test_kahler_tags_nonempty(self):
        assert len(KAHLER_TAGS) >= 4

    def test_moser_theorem_tags_nonempty(self):
        assert len(MOSER_THEOREM_TAGS) >= 4

    def test_gromov_nonsqueezing_tags_nonempty(self):
        assert len(GROMOV_NONSQUEEZING_TAGS) >= 4

    def test_cotangent_bundle_tags_nonempty(self):
        assert len(COTANGENT_BUNDLE_TAGS) >= 4

    def test_darboux_theorem_in_darboux_tags(self):
        assert "darboux_theorem" in DARBOUX_THEOREM_TAGS

    def test_darboux_chart_in_darboux_tags(self):
        assert "darboux_chart" in DARBOUX_THEOREM_TAGS

    def test_hamiltonian_vector_field_in_hamiltonian_tags(self):
        assert "hamiltonian_vector_field" in HAMILTONIAN_TAGS

    def test_poisson_bracket_in_hamiltonian_tags(self):
        assert "poisson_bracket" in HAMILTONIAN_TAGS

    def test_lagrangian_submanifold_in_lagrangian_tags(self):
        assert "lagrangian_submanifold" in LAGRANGIAN_TAGS

    def test_maslov_index_in_lagrangian_tags(self):
        assert "maslov_index" in LAGRANGIAN_TAGS

    def test_symplectomorphism_in_symp_tags(self):
        assert "symplectomorphism" in SYMPLECTOMORPHISM_TAGS

    def test_moser_stability_in_symp_tags(self):
        assert "moser_stability" in SYMPLECTOMORPHISM_TAGS

    def test_kahler_manifold_in_kahler_tags(self):
        assert "kahler_manifold" in KAHLER_TAGS

    def test_fubini_study_in_kahler_tags(self):
        assert "fubini_study" in KAHLER_TAGS

    def test_moser_theorem_in_moser_tags(self):
        assert "moser_theorem" in MOSER_THEOREM_TAGS

    def test_gromov_nonsqueezing_in_gromov_tags(self):
        assert "gromov_nonsqueezing" in GROMOV_NONSQUEEZING_TAGS

    def test_symplectic_width_in_gromov_tags(self):
        assert "symplectic_width" in GROMOV_NONSQUEEZING_TAGS

    def test_cotangent_bundle_in_cotangent_tags(self):
        assert "cotangent_bundle" in COTANGENT_BUNDLE_TAGS

    def test_tautological_form_in_cotangent_tags(self):
        assert "tautological_form" in COTANGENT_BUNDLE_TAGS

    def test_all_tag_sets_are_frozensets(self):
        for tag_set in [
            DARBOUX_THEOREM_TAGS, HAMILTONIAN_TAGS, LAGRANGIAN_TAGS,
            SYMPLECTOMORPHISM_TAGS, KAHLER_TAGS, MOSER_THEOREM_TAGS,
            GROMOV_NONSQUEEZING_TAGS, COTANGENT_BUNDLE_TAGS,
        ]:
            assert isinstance(tag_set, frozenset)


# ---------------------------------------------------------------------------
# Named profiles
# ---------------------------------------------------------------------------

class TestNamedSymplecticProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_symplectic_profiles(), tuple)

    def test_at_least_six_profiles(self):
        assert len(get_named_symplectic_profiles()) >= 6

    def test_all_are_symplectic_profile_instances(self):
        for p in get_named_symplectic_profiles():
            assert isinstance(p, SymplecticProfile)

    def test_all_keys_unique(self):
        keys = [p.key for p in get_named_symplectic_profiles()]
        assert len(keys) == len(set(keys))

    def test_all_display_names_nonempty(self):
        for p in get_named_symplectic_profiles():
            assert len(p.display_name) > 0

    def test_all_focus_fields_nonempty(self):
        for p in get_named_symplectic_profiles():
            assert len(p.focus) > 10

    def test_all_chapter_targets_nonempty(self):
        for p in get_named_symplectic_profiles():
            assert len(p.chapter_targets) >= 1

    def test_standard_r2n_exists(self):
        keys = [p.key for p in get_named_symplectic_profiles()]
        assert "standard_r2n" in keys

    def test_cotangent_bundle_profile_exists(self):
        keys = [p.key for p in get_named_symplectic_profiles()]
        assert "cotangent_bundle_tm" in keys

    def test_s2_area_form_exists(self):
        keys = [p.key for p in get_named_symplectic_profiles()]
        assert "s2_area_form" in keys

    def test_standard_r2n_is_exact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "standard_r2n")
        assert p.is_exact is True

    def test_standard_r2n_is_kahler(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "standard_r2n")
        assert p.is_kahler is True

    def test_standard_r2n_not_compact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "standard_r2n")
        assert p.is_compact is False

    def test_cotangent_bundle_is_exact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "cotangent_bundle_tm")
        assert p.is_exact is True

    def test_cotangent_bundle_has_lagrangian(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "cotangent_bundle_tm")
        assert p.has_lagrangian is True

    def test_cotangent_bundle_not_compact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "cotangent_bundle_tm")
        assert p.is_compact is False

    def test_s2_is_compact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "s2_area_form")
        assert p.is_compact is True

    def test_s2_is_not_exact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "s2_area_form")
        assert p.is_exact is False

    def test_s2_is_monotone(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "s2_area_form")
        assert p.is_monotone is True

    def test_cpn_is_kahler(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "cpn_fubini_study")
        assert p.is_kahler is True

    def test_cpn_is_compact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "cpn_fubini_study")
        assert p.is_compact is True

    def test_cpn_is_monotone(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "cpn_fubini_study")
        assert p.is_monotone is True

    def test_torus_is_compact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "torus_t2n")
        assert p.is_compact is True

    def test_torus_not_exact(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "torus_t2n")
        assert p.is_exact is False

    def test_torus_has_lagrangian(self):
        p = next(p for p in get_named_symplectic_profiles() if p.key == "torus_t2n")
        assert p.has_lagrangian is True

    def test_all_profiles_frozen(self):
        p = get_named_symplectic_profiles()[0]
        with pytest.raises((AttributeError, TypeError)):
            p.key = "mutated"  # type: ignore[misc]

    def test_presentation_layer_nonempty(self):
        for p in get_named_symplectic_profiles():
            assert p.presentation_layer != ""

    def test_symplectic_type_nonempty(self):
        for p in get_named_symplectic_profiles():
            assert p.symplectic_type != ""


# ---------------------------------------------------------------------------
# Summary and index functions
# ---------------------------------------------------------------------------

class TestSummaryFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(symplectic_layer_summary(), dict)

    def test_layer_summary_values_positive(self):
        for v in symplectic_layer_summary().values():
            assert v > 0

    def test_layer_summary_total_matches_profile_count(self):
        total = sum(symplectic_layer_summary().values())
        assert total == len(get_named_symplectic_profiles())

    def test_chapter_index_returns_dict(self):
        assert isinstance(symplectic_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in symplectic_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_keys_cover_all_chapters(self):
        all_chapters: set[str] = set()
        for p in get_named_symplectic_profiles():
            all_chapters.update(p.chapter_targets)
        index = symplectic_chapter_index()
        assert all_chapters == set(index.keys())

    def test_type_index_returns_dict(self):
        assert isinstance(symplectic_type_index(), dict)

    def test_type_index_covers_standard(self):
        assert "standard" in symplectic_type_index()

    def test_type_index_covers_cotangent(self):
        assert "cotangent" in symplectic_type_index()

    def test_type_index_covers_kahler(self):
        assert "kahler" in symplectic_type_index()

    def test_type_index_total_matches_profile_count(self):
        total = sum(len(v) for v in symplectic_type_index().values())
        assert total == len(get_named_symplectic_profiles())


# ---------------------------------------------------------------------------
# is_symplectic_manifold
# ---------------------------------------------------------------------------

class TestIsSymplecticManifold:
    def test_explicit_symplectic_manifold_tag(self):
        r = is_symplectic_manifold(_space("symplectic_manifold"))
        assert r.value == "symplectic_manifold"
        assert r.is_true

    def test_symplectic_form_tag(self):
        r = is_symplectic_manifold(_space("symplectic_form"))
        assert r.value == "symplectic_manifold"

    def test_darboux_chart_tag(self):
        r = is_symplectic_manifold(_space("darboux_chart"))
        assert r.value == "symplectic_manifold"

    def test_darboux_theorem_tag(self):
        r = is_symplectic_manifold(_space("darboux_theorem"))
        assert r.value == "symplectic_manifold"

    def test_hamiltonian_vector_field_tag(self):
        r = is_symplectic_manifold(_space("hamiltonian_vector_field"))
        assert r.value == "symplectic_manifold"

    def test_hamiltonian_flow_tag(self):
        r = is_symplectic_manifold(_space("hamiltonian_flow"))
        assert r.value == "symplectic_manifold"

    def test_poisson_bracket_tag(self):
        r = is_symplectic_manifold(_space("poisson_bracket"))
        assert r.value == "symplectic_manifold"

    def test_cotangent_bundle_tag(self):
        r = is_symplectic_manifold(_space("cotangent_bundle"))
        assert r.value == "symplectic_manifold"

    def test_kahler_manifold_tag(self):
        r = is_symplectic_manifold(_space("kahler_manifold"))
        assert r.value == "symplectic_manifold"

    def test_fubini_study_tag(self):
        r = is_symplectic_manifold(_space("fubini_study"))
        assert r.value == "symplectic_manifold"

    def test_coadjoint_orbit_tag(self):
        r = is_symplectic_manifold(_space("coadjoint_orbit"))
        assert r.value == "symplectic_manifold"

    def test_odd_dimensional_false(self):
        r = is_symplectic_manifold(_space("odd_dimensional"))
        assert r.is_false

    def test_degenerate_form_false(self):
        r = is_symplectic_manifold(_space("degenerate_form"))
        assert r.is_false

    def test_no_symplectic_structure_false(self):
        r = is_symplectic_manifold(_space("no_symplectic_structure"))
        assert r.is_false

    def test_unknown_tags_unknown(self):
        r = is_symplectic_manifold(_space("some_random_tag"))
        assert r.value == "unknown"

    def test_empty_tags_unknown(self):
        r = is_symplectic_manifold(_space())
        assert r.value == "unknown"

    def test_result_has_justification(self):
        r = is_symplectic_manifold(_space("symplectic_manifold"))
        assert len(r.justification) >= 1

    def test_result_metadata_has_tags(self):
        r = is_symplectic_manifold(_space("darboux_theorem"))
        assert "tags" in r.metadata

    def test_canonical_symplectic_tag(self):
        r = is_symplectic_manifold(_space("canonical_symplectic"))
        assert r.value == "symplectic_manifold"

    def test_liouville_theorem_tag(self):
        r = is_symplectic_manifold(_space("liouville_theorem"))
        assert r.value == "symplectic_manifold"

    def test_multiple_symplectic_tags(self):
        r = is_symplectic_manifold(_space("darboux_theorem", "hamiltonian_flow", "lagrangian"))
        assert r.value == "symplectic_manifold"


# ---------------------------------------------------------------------------
# is_lagrangian_submanifold
# ---------------------------------------------------------------------------

class TestIsLagrangianSubmanifold:
    def test_lagrangian_submanifold_tag(self):
        r = is_lagrangian_submanifold(_space("lagrangian_submanifold"))
        assert r.value == "lagrangian_submanifold"
        assert r.is_true

    def test_maslov_index_tag(self):
        r = is_lagrangian_submanifold(_space("maslov_index"))
        assert r.value == "lagrangian_submanifold"

    def test_lagrangian_grassmannian_tag(self):
        r = is_lagrangian_submanifold(_space("lagrangian_grassmannian"))
        assert r.value == "lagrangian_submanifold"

    def test_weinstein_neighborhood_tag(self):
        r = is_lagrangian_submanifold(_space("weinstein_neighborhood"))
        assert r.value == "lagrangian_submanifold"

    def test_floer_theory_tag(self):
        r = is_lagrangian_submanifold(_space("floer_theory"))
        assert r.value == "lagrangian_submanifold"

    def test_zero_section_lagrangian_tag(self):
        r = is_lagrangian_submanifold(_space("zero_section_lagrangian"))
        assert r.value == "lagrangian_submanifold"

    def test_cotangent_fiber_lagrangian_tag(self):
        r = is_lagrangian_submanifold(_space("cotangent_fiber_lagrangian"))
        assert r.value == "lagrangian_submanifold"

    def test_lagrangian_torus_tag(self):
        r = is_lagrangian_submanifold(_space("lagrangian_torus"))
        assert r.value == "lagrangian_submanifold"

    def test_lagrangian_fibration_tag(self):
        r = is_lagrangian_submanifold(_space("lagrangian_fibration"))
        assert r.value == "lagrangian_submanifold"

    def test_symplectic_submanifold_false(self):
        r = is_lagrangian_submanifold(_space("symplectic_submanifold"))
        assert r.is_false

    def test_symplectic_surface_false(self):
        r = is_lagrangian_submanifold(_space("symplectic_surface"))
        assert r.is_false

    def test_non_lagrangian_false(self):
        r = is_lagrangian_submanifold(_space("non_lagrangian"))
        assert r.is_false

    def test_unknown_returns_unknown(self):
        r = is_lagrangian_submanifold(_space("some_tag"))
        assert r.value == "unknown"

    def test_empty_returns_unknown(self):
        r = is_lagrangian_submanifold(_space())
        assert r.value == "unknown"

    def test_result_has_justification(self):
        r = is_lagrangian_submanifold(_space("lagrangian_submanifold"))
        assert len(r.justification) >= 1

    def test_lagrangian_intersection_tag(self):
        r = is_lagrangian_submanifold(_space("lagrangian_intersection"))
        assert r.value == "lagrangian_submanifold"

    def test_isotropic_submanifold_tag(self):
        r = is_lagrangian_submanifold(_space("isotropic_submanifold"))
        assert r.value == "lagrangian_submanifold"

    def test_coisotropic_only_false(self):
        r = is_lagrangian_submanifold(_space("coisotropic_only"))
        assert r.is_false


# ---------------------------------------------------------------------------
# has_hamiltonian_structure
# ---------------------------------------------------------------------------

class TestHasHamiltonianStructure:
    def test_hamiltonian_vector_field_tag(self):
        r = has_hamiltonian_structure(_space("hamiltonian_vector_field"))
        assert r.value == "hamiltonian_structure"
        assert r.is_true

    def test_hamiltonian_flow_tag(self):
        r = has_hamiltonian_structure(_space("hamiltonian_flow"))
        assert r.value == "hamiltonian_structure"

    def test_hamiltonian_system_tag(self):
        r = has_hamiltonian_structure(_space("hamiltonian_system"))
        assert r.value == "hamiltonian_structure"

    def test_poisson_bracket_tag(self):
        r = has_hamiltonian_structure(_space("poisson_bracket"))
        assert r.value == "hamiltonian_structure"

    def test_liouville_theorem_tag(self):
        r = has_hamiltonian_structure(_space("liouville_theorem"))
        assert r.value == "hamiltonian_structure"

    def test_symplectic_manifold_tag(self):
        r = has_hamiltonian_structure(_space("symplectic_manifold"))
        assert r.value == "hamiltonian_structure"

    def test_cotangent_bundle_tag(self):
        r = has_hamiltonian_structure(_space("cotangent_bundle"))
        assert r.value == "hamiltonian_structure"

    def test_kahler_manifold_tag(self):
        r = has_hamiltonian_structure(_space("kahler_manifold"))
        assert r.value == "hamiltonian_structure"

    def test_darboux_chart_tag(self):
        r = has_hamiltonian_structure(_space("darboux_chart"))
        assert r.value == "hamiltonian_structure"

    def test_canonical_symplectic_tag(self):
        r = has_hamiltonian_structure(_space("canonical_symplectic"))
        assert r.value == "hamiltonian_structure"

    def test_odd_dimensional_false(self):
        r = has_hamiltonian_structure(_space("odd_dimensional"))
        assert r.is_false

    def test_no_symplectic_structure_false(self):
        r = has_hamiltonian_structure(_space("no_symplectic_structure"))
        assert r.is_false

    def test_degenerate_form_false(self):
        r = has_hamiltonian_structure(_space("degenerate_form"))
        assert r.is_false

    def test_unknown_returns_unknown(self):
        r = has_hamiltonian_structure(_space("some_tag"))
        assert r.value == "unknown"

    def test_empty_returns_unknown(self):
        r = has_hamiltonian_structure(_space())
        assert r.value == "unknown"

    def test_result_has_justification(self):
        r = has_hamiltonian_structure(_space("hamiltonian_vector_field"))
        assert len(r.justification) >= 1

    def test_noether_theorem_tag(self):
        r = has_hamiltonian_structure(_space("noether_theorem"))
        assert r.value == "hamiltonian_structure"

    def test_conservation_law_tag(self):
        r = has_hamiltonian_structure(_space("conservation_law"))
        assert r.value == "hamiltonian_structure"

    def test_coadjoint_orbit_tag(self):
        r = has_hamiltonian_structure(_space("coadjoint_orbit"))
        assert r.value == "hamiltonian_structure"

    def test_symplectic_flow_tag(self):
        r = has_hamiltonian_structure(_space("symplectic_flow"))
        assert r.value == "hamiltonian_structure"


# ---------------------------------------------------------------------------
# admits_kahler_structure
# ---------------------------------------------------------------------------

class TestAdmitsKahlerStructure:
    def test_kahler_manifold_tag(self):
        r = admits_kahler_structure(_space("kahler_manifold"))
        assert r.value == "kahler_structure"
        assert r.is_true

    def test_kahler_form_tag(self):
        r = admits_kahler_structure(_space("kahler_form"))
        assert r.value == "kahler_structure"

    def test_fubini_study_tag(self):
        r = admits_kahler_structure(_space("fubini_study"))
        assert r.value == "kahler_structure"

    def test_hard_lefschetz_tag(self):
        r = admits_kahler_structure(_space("hard_lefschetz"))
        assert r.value == "kahler_structure"

    def test_hodge_decomposition_tag(self):
        r = admits_kahler_structure(_space("hodge_decomposition"))
        assert r.value == "kahler_structure"

    def test_complex_projective_tag(self):
        r = admits_kahler_structure(_space("complex_projective"))
        assert r.value == "kahler_structure"

    def test_riemann_surface_tag(self):
        r = admits_kahler_structure(_space("riemann_surface"))
        assert r.value == "kahler_structure"

    def test_coadjoint_orbit_tag(self):
        r = admits_kahler_structure(_space("coadjoint_orbit"))
        assert r.value == "kahler_structure"

    def test_kahler_potential_tag(self):
        r = admits_kahler_structure(_space("kahler_potential"))
        assert r.value == "kahler_structure"

    def test_non_kahler_tag_false(self):
        r = admits_kahler_structure(_space("non_kahler"))
        assert r.is_false

    def test_symplectic_non_kahler_false(self):
        r = admits_kahler_structure(_space("symplectic_non_kahler"))
        assert r.is_false

    def test_kodaira_thurston_false(self):
        r = admits_kahler_structure(_space("kodaira_thurston"))
        assert r.is_false

    def test_no_hard_lefschetz_false(self):
        r = admits_kahler_structure(_space("no_hard_lefschetz"))
        assert r.is_false

    def test_unknown_returns_unknown(self):
        r = admits_kahler_structure(_space("some_tag"))
        assert r.value == "unknown"

    def test_empty_returns_unknown(self):
        r = admits_kahler_structure(_space())
        assert r.value == "unknown"

    def test_result_has_justification(self):
        r = admits_kahler_structure(_space("kahler_manifold"))
        assert len(r.justification) >= 1

    def test_algebraic_variety_is_kahler(self):
        r = admits_kahler_structure(_space("algebraic_variety"))
        assert r.value == "kahler_structure"

    def test_kahler_torus_is_kahler(self):
        r = admits_kahler_structure(_space("kahler_torus"))
        assert r.value == "kahler_structure"

    def test_hermitian_metric_tag(self):
        r = admits_kahler_structure(_space("hermitian_metric"))
        assert r.value == "kahler_structure"


# ---------------------------------------------------------------------------
# classify_symplectic
# ---------------------------------------------------------------------------

class TestClassifySymplectic:
    def test_returns_dict(self):
        assert isinstance(classify_symplectic(_space("symplectic_manifold")), dict)

    def test_has_four_keys(self):
        result = classify_symplectic(_space("symplectic_manifold"))
        assert len(result) == 4

    def test_has_is_symplectic_key(self):
        assert "is_symplectic_manifold" in classify_symplectic(_space())

    def test_has_is_lagrangian_key(self):
        assert "is_lagrangian_submanifold" in classify_symplectic(_space())

    def test_has_has_hamiltonian_key(self):
        assert "has_hamiltonian_structure" in classify_symplectic(_space())

    def test_has_admits_kahler_key(self):
        assert "admits_kahler_structure" in classify_symplectic(_space())

    def test_symplectic_manifold_all_true_where_applicable(self):
        result = classify_symplectic(_space("symplectic_manifold"))
        assert result["is_symplectic_manifold"].is_true

    def test_kahler_manifold_both_symplectic_and_kahler(self):
        result = classify_symplectic(_space("kahler_manifold"))
        assert result["is_symplectic_manifold"].is_true
        assert result["admits_kahler_structure"].is_true

    def test_empty_space_all_unknown(self):
        result = classify_symplectic(_space())
        for v in result.values():
            assert v.value == "unknown"

    def test_non_symplectic_is_false(self):
        result = classify_symplectic(_space("odd_dimensional"))
        assert result["is_symplectic_manifold"].is_false

    def test_lagrangian_tag_marks_lagrangian(self):
        result = classify_symplectic(_space("lagrangian_submanifold"))
        assert result["is_lagrangian_submanifold"].is_true

    def test_non_kahler_marks_not_kahler(self):
        result = classify_symplectic(_space("non_kahler"))
        assert result["admits_kahler_structure"].is_false


# ---------------------------------------------------------------------------
# symplectic_profile
# ---------------------------------------------------------------------------

class TestSymplecticProfile:
    def test_returns_dict(self):
        assert isinstance(symplectic_profile(_space("symplectic_manifold")), dict)

    def test_has_space_key(self):
        sp = _space("symplectic_manifold")
        assert symplectic_profile(sp)["space"] is sp

    def test_has_tags_key(self):
        result = symplectic_profile(_space("symplectic_manifold"))
        assert "tags" in result

    def test_has_representation_key(self):
        result = symplectic_profile(_space("symplectic_manifold"))
        assert "representation" in result

    def test_has_classification_key(self):
        result = symplectic_profile(_space("symplectic_manifold"))
        assert "classification" in result

    def test_has_summary_key(self):
        result = symplectic_profile(_space("symplectic_manifold"))
        assert "summary" in result

    def test_tags_are_sorted(self):
        sp = _space("symplectic_manifold", "kahler_manifold")
        tags = symplectic_profile(sp)["tags"]
        assert tags == sorted(tags)

    def test_summary_has_four_keys(self):
        result = symplectic_profile(_space("symplectic_manifold"))
        assert len(result["summary"]) == 4

    def test_empty_space_tags_empty(self):
        result = symplectic_profile(_space())
        assert result["tags"] == []
