"""Tests for pytop.motivic_homotopy."""

from __future__ import annotations

import pytest

from pytop.motivic_homotopy import (
    A1_HOMOTOPY_TAGS,
    ALGEBRAIC_K_THEORY_TAGS,
    MILNOR_K_THEORY_TAGS,
    MOTIVIC_COHOMOLOGY_TAGS,
    MOTIVIC_SPHERE_TAGS,
    NISNEVICH_TOPOLOGY_TAGS,
    STABLE_MOTIVIC_TAGS,
    VOEVODSKY_TAGS,
    MotivicHomotopyProfile,
    classify_motivic,
    get_named_motivic_profiles,
    has_algebraic_k_theory_structure,
    has_nisnevich_descent,
    is_a1_invariant,
    is_motivic_cohomology_theory,
    motivic_chapter_index,
    motivic_layer_summary,
    motivic_profile,
    motivic_type_index,
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
    def test_a1_homotopy_tags_nonempty(self):
        assert len(A1_HOMOTOPY_TAGS) >= 4

    def test_nisnevich_topology_tags_nonempty(self):
        assert len(NISNEVICH_TOPOLOGY_TAGS) >= 4

    def test_motivic_cohomology_tags_nonempty(self):
        assert len(MOTIVIC_COHOMOLOGY_TAGS) >= 4

    def test_algebraic_k_theory_tags_nonempty(self):
        assert len(ALGEBRAIC_K_THEORY_TAGS) >= 4

    def test_milnor_k_theory_tags_nonempty(self):
        assert len(MILNOR_K_THEORY_TAGS) >= 4

    def test_stable_motivic_tags_nonempty(self):
        assert len(STABLE_MOTIVIC_TAGS) >= 4

    def test_voevodsky_tags_nonempty(self):
        assert len(VOEVODSKY_TAGS) >= 4

    def test_motivic_sphere_tags_nonempty(self):
        assert len(MOTIVIC_SPHERE_TAGS) >= 4

    def test_a1_homotopy_in_a1_tags(self):
        assert "a1_homotopy" in A1_HOMOTOPY_TAGS

    def test_a1_invariant_in_a1_tags(self):
        assert "a1_invariant" in A1_HOMOTOPY_TAGS

    def test_morel_voevodsky_in_a1_tags(self):
        assert "morel_voevodsky" in A1_HOMOTOPY_TAGS

    def test_nisnevich_topology_in_nisnevich_tags(self):
        assert "nisnevich_topology" in NISNEVICH_TOPOLOGY_TAGS

    def test_nisnevich_sheaf_in_nisnevich_tags(self):
        assert "nisnevich_sheaf" in NISNEVICH_TOPOLOGY_TAGS

    def test_brown_gersten_in_nisnevich_tags(self):
        assert "brown_gersten" in NISNEVICH_TOPOLOGY_TAGS

    def test_motivic_cohomology_in_motivic_tags(self):
        assert "motivic_cohomology" in MOTIVIC_COHOMOLOGY_TAGS

    def test_chow_group_in_motivic_tags(self):
        assert "chow_group" in MOTIVIC_COHOMOLOGY_TAGS

    def test_hz_spectrum_in_motivic_tags(self):
        assert "hz_spectrum" in MOTIVIC_COHOMOLOGY_TAGS

    def test_algebraic_k_theory_in_k_tags(self):
        assert "algebraic_k_theory" in ALGEBRAIC_K_THEORY_TAGS

    def test_kgl_spectrum_in_k_tags(self):
        assert "kgl_spectrum" in ALGEBRAIC_K_THEORY_TAGS

    def test_milnor_k_theory_in_milnor_tags(self):
        assert "milnor_k_theory" in MILNOR_K_THEORY_TAGS

    def test_steinberg_relation_in_milnor_tags(self):
        assert "steinberg_relation" in MILNOR_K_THEORY_TAGS

    def test_sh_k_in_stable_tags(self):
        assert "sh_k" in STABLE_MOTIVIC_TAGS

    def test_motivic_spectrum_in_stable_tags(self):
        assert "motivic_spectrum" in STABLE_MOTIVIC_TAGS

    def test_voevodsky_in_voevodsky_tags(self):
        assert "voevodsky" in VOEVODSKY_TAGS

    def test_dm_category_in_voevodsky_tags(self):
        assert "dm_category" in VOEVODSKY_TAGS

    def test_s11_sphere_in_sphere_tags(self):
        assert "s11_sphere" in MOTIVIC_SPHERE_TAGS

    def test_motivic_sphere_in_sphere_tags(self):
        assert "motivic_sphere" in MOTIVIC_SPHERE_TAGS

    def test_all_tags_are_frozensets(self):
        for tagset in [
            A1_HOMOTOPY_TAGS, NISNEVICH_TOPOLOGY_TAGS, MOTIVIC_COHOMOLOGY_TAGS,
            ALGEBRAIC_K_THEORY_TAGS, MILNOR_K_THEORY_TAGS, STABLE_MOTIVIC_TAGS,
            VOEVODSKY_TAGS, MOTIVIC_SPHERE_TAGS,
        ]:
            assert isinstance(tagset, frozenset)

    def test_tags_contain_strings(self):
        for tagset in [A1_HOMOTOPY_TAGS, NISNEVICH_TOPOLOGY_TAGS, MOTIVIC_COHOMOLOGY_TAGS]:
            for tag in tagset:
                assert isinstance(tag, str)


# ---------------------------------------------------------------------------
# Named profiles
# ---------------------------------------------------------------------------

class TestNamedMotivicProfiles:
    def setup_method(self):
        self.profiles = get_named_motivic_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_six_profiles(self):
        assert len(self.profiles) >= 6

    def test_all_are_motivic_profile_instances(self):
        for p in self.profiles:
            assert isinstance(p, MotivicHomotopyProfile)

    def test_all_keys_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_all_keys_nonempty_strings(self):
        for p in self.profiles:
            assert isinstance(p.key, str) and len(p.key) > 0

    def test_all_display_names_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.display_name, str) and len(p.display_name) > 0

    def test_all_focus_strings_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.focus, str) and len(p.focus) > 30

    def test_all_chapter_targets_are_tuples(self):
        for p in self.profiles:
            assert isinstance(p.chapter_targets, tuple)

    def test_all_chapter_targets_nonempty(self):
        for p in self.profiles:
            assert len(p.chapter_targets) >= 1

    def test_a1_homotopy_space_exists(self):
        keys = [p.key for p in self.profiles]
        assert "a1_homotopy_space" in keys

    def test_nisnevich_sheaf_exists(self):
        keys = [p.key for p in self.profiles]
        assert "nisnevich_sheaf" in keys

    def test_motivic_cohomology_hz_exists(self):
        keys = [p.key for p in self.profiles]
        assert "motivic_cohomology_hz" in keys

    def test_algebraic_k_theory_kgl_exists(self):
        keys = [p.key for p in self.profiles]
        assert "algebraic_k_theory_kgl" in keys

    def test_milnor_k_theory_exists(self):
        keys = [p.key for p in self.profiles]
        assert "milnor_k_theory" in keys

    def test_stable_motivic_sphere_exists(self):
        keys = [p.key for p in self.profiles]
        assert "stable_motivic_sphere_s11" in keys

    def test_chow_group_exists(self):
        keys = [p.key for p in self.profiles]
        assert "chow_group" in keys

    def test_a1_homotopy_profile_fields(self):
        p = next(x for x in self.profiles if x.key == "a1_homotopy_space")
        assert p.motivic_type == "a1_homotopy"
        assert p.is_a1_invariant is True
        assert p.has_nisnevich_descent is True

    def test_nisnevich_sheaf_profile_fields(self):
        p = next(x for x in self.profiles if x.key == "nisnevich_sheaf")
        assert p.motivic_type == "nisnevich"
        assert p.has_nisnevich_descent is True

    def test_motivic_cohomology_hz_fields(self):
        p = next(x for x in self.profiles if x.key == "motivic_cohomology_hz")
        assert p.motivic_type == "motivic_cohomology"
        assert p.is_stable is True
        assert p.has_transfers is True
        assert p.is_a1_invariant is True

    def test_algebraic_k_theory_kgl_fields(self):
        p = next(x for x in self.profiles if x.key == "algebraic_k_theory_kgl")
        assert p.motivic_type == "algebraic_k_theory"
        assert p.is_stable is True
        assert p.is_a1_invariant is True

    def test_milnor_k_theory_profile_fields(self):
        p = next(x for x in self.profiles if x.key == "milnor_k_theory")
        assert p.motivic_type == "milnor_k_theory"
        assert p.has_transfers is True
        assert p.is_a1_invariant is True

    def test_stable_motivic_sphere_fields(self):
        p = next(x for x in self.profiles if x.key == "stable_motivic_sphere_s11")
        assert p.motivic_type == "stable_motivic"
        assert p.is_stable is True
        assert p.is_a1_invariant is False  # Gm is not A¹-invariant as a presheaf

    def test_chow_group_profile_fields(self):
        p = next(x for x in self.profiles if x.key == "chow_group")
        assert p.motivic_type == "motivic_cohomology"
        assert p.has_transfers is True

    def test_profiles_are_frozen(self):
        p = self.profiles[0]
        with pytest.raises((AttributeError, TypeError)):
            p.key = "modified"  # type: ignore[misc]

    def test_motivic_types_are_valid_strings(self):
        valid_types = {
            "a1_homotopy", "stable_motivic", "motivic_cohomology",
            "algebraic_k_theory", "milnor_k_theory", "nisnevich",
        }
        for p in self.profiles:
            assert p.motivic_type in valid_types

    def test_base_fields_are_strings(self):
        for p in self.profiles:
            assert isinstance(p.base_field, str) and len(p.base_field) > 0


# ---------------------------------------------------------------------------
# Summary functions
# ---------------------------------------------------------------------------

class TestSummaryFunctions:
    def test_motivic_layer_summary_returns_dict(self):
        result = motivic_layer_summary()
        assert isinstance(result, dict)

    def test_motivic_layer_summary_has_positive_counts(self):
        result = motivic_layer_summary()
        assert all(v > 0 for v in result.values())

    def test_motivic_layer_summary_count_matches_profiles(self):
        result = motivic_layer_summary()
        profiles = get_named_motivic_profiles()
        assert sum(result.values()) == len(profiles)

    def test_motivic_chapter_index_returns_dict(self):
        result = motivic_chapter_index()
        assert isinstance(result, dict)

    def test_motivic_chapter_index_values_are_tuples(self):
        result = motivic_chapter_index()
        for v in result.values():
            assert isinstance(v, tuple)

    def test_motivic_chapter_index_keys_are_sorted(self):
        result = motivic_chapter_index()
        keys = list(result.keys())
        assert keys == sorted(keys)

    def test_motivic_chapter_index_contains_chapter_40(self):
        result = motivic_chapter_index()
        assert "40" in result

    def test_motivic_type_index_returns_dict(self):
        result = motivic_type_index()
        assert isinstance(result, dict)

    def test_motivic_type_index_values_are_tuples(self):
        result = motivic_type_index()
        for v in result.values():
            assert isinstance(v, tuple)

    def test_motivic_type_index_keys_are_sorted(self):
        result = motivic_type_index()
        keys = list(result.keys())
        assert keys == sorted(keys)

    def test_motivic_type_index_contains_a1_homotopy(self):
        result = motivic_type_index()
        assert "a1_homotopy" in result

    def test_motivic_type_index_contains_motivic_cohomology(self):
        result = motivic_type_index()
        assert "motivic_cohomology" in result

    def test_motivic_type_index_contains_algebraic_k_theory(self):
        result = motivic_type_index()
        assert "algebraic_k_theory" in result

    def test_motivic_type_index_total_matches_profiles(self):
        result = motivic_type_index()
        profiles = get_named_motivic_profiles()
        assert sum(len(v) for v in result.values()) == len(profiles)


# ---------------------------------------------------------------------------
# is_a1_invariant
# ---------------------------------------------------------------------------

class TestIsA1Invariant:
    def test_explicit_a1_invariant_tag(self):
        s = _space("a1_invariant")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_a1_homotopy_tag(self):
        s = _space("a1_homotopy")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_motivic_homotopy_tag(self):
        s = _space("motivic_homotopy")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_a1_local_tag(self):
        s = _space("a1_local")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_a1_weak_equivalence_tag(self):
        s = _space("a1_weak_equivalence")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_morel_voevodsky_tag(self):
        s = _space("morel_voevodsky")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_algebraic_k_theory_tag(self):
        s = _space("algebraic_k_theory")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_kgl_spectrum_tag(self):
        s = _space("kgl_spectrum")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_motivic_cohomology_tag(self):
        s = _space("motivic_cohomology")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_hz_spectrum_tag(self):
        s = _space("hz_spectrum")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_stable_motivic_tag(self):
        s = _space("sh_k")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_milnor_k_theory_tag(self):
        s = _space("milnor_k_theory")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_algebraic_cobordism_tag(self):
        s = _space("algebraic_cobordism")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_mgl_spectrum_tag(self):
        s = _space("mgl_spectrum")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_non_a1_invariant_tag(self):
        s = _space("non_a1_invariant")
        r = is_a1_invariant(s)
        assert r.is_false

    def test_not_a1_local_tag(self):
        s = _space("not_a1_local")
        r = is_a1_invariant(s)
        assert r.is_false

    def test_a1_non_invariant_tag(self):
        s = _space("a1_non_invariant")
        r = is_a1_invariant(s)
        assert r.is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = is_a1_invariant(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("compact_manifold")
        r = is_a1_invariant(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("a1_invariant")
        r = is_a1_invariant(s)
        assert len(r.justification) >= 1

    def test_result_has_metadata(self):
        s = _space("algebraic_k_theory")
        r = is_a1_invariant(s)
        assert "criterion" in r.metadata

    def test_chow_group_tag_is_a1_invariant(self):
        s = _space("chow_group")
        r = is_a1_invariant(s)
        assert r.is_true

    def test_oriented_spectrum_is_a1_invariant(self):
        s = _space("oriented_spectrum")
        r = is_a1_invariant(s)
        assert r.is_true


# ---------------------------------------------------------------------------
# has_nisnevich_descent
# ---------------------------------------------------------------------------

class TestHasNisnevichDescent:
    def test_nisnevich_topology_tag(self):
        s = _space("nisnevich_topology")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_nisnevich_sheaf_tag(self):
        s = _space("nisnevich_sheaf")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_brown_gersten_tag(self):
        s = _space("brown_gersten")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_nisnevich_descent_tag(self):
        s = _space("nisnevich_descent")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_nisnevich_local_tag(self):
        s = _space("nisnevich_local")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_algebraic_k_theory_tag(self):
        s = _space("algebraic_k_theory")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_motivic_cohomology_tag(self):
        s = _space("motivic_cohomology")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_hz_spectrum_tag(self):
        s = _space("hz_spectrum")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_voevodsky_tag(self):
        s = _space("voevodsky")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_dm_category_tag(self):
        s = _space("dm_category")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_motivic_space_tag(self):
        s = _space("motivic_space")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_a1_local_implies_nisnevich_descent(self):
        s = _space("a1_local")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_stable_motivic_tag(self):
        s = _space("sh_k")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_mgl_spectrum_tag(self):
        s = _space("mgl_spectrum")
        r = has_nisnevich_descent(s)
        assert r.is_true

    def test_zariski_only_no_descent(self):
        s = _space("zariski_only")
        r = has_nisnevich_descent(s)
        assert r.is_false

    def test_fails_nisnevich_descent_tag(self):
        s = _space("fails_nisnevich_descent")
        r = has_nisnevich_descent(s)
        assert r.is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = has_nisnevich_descent(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("symplectic_manifold")
        r = has_nisnevich_descent(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("nisnevich_topology")
        r = has_nisnevich_descent(s)
        assert len(r.justification) >= 1

    def test_result_has_metadata_criterion(self):
        s = _space("algebraic_k_theory")
        r = has_nisnevich_descent(s)
        assert "criterion" in r.metadata


# ---------------------------------------------------------------------------
# is_motivic_cohomology_theory
# ---------------------------------------------------------------------------

class TestIsMotivicCohomologyTheory:
    def test_motivic_cohomology_tag(self):
        s = _space("motivic_cohomology")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_hz_spectrum_tag(self):
        s = _space("hz_spectrum")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_chow_group_tag(self):
        s = _space("chow_group")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_motivic_complex_tag(self):
        s = _space("motivic_complex")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_bigraded_cohomology_tag(self):
        s = _space("bigraded_cohomology")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_voevodsky_complex_tag(self):
        s = _space("voevodsky_complex")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_milnor_k_theory_tag(self):
        s = _space("milnor_k_theory")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_k_milnor_tag(self):
        s = _space("k_milnor")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_algebraic_cycles_tag(self):
        s = _space("algebraic_cycles")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_bloch_cycle_complex_tag(self):
        s = _space("bloch_cycle_complex")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_higher_chow_tag(self):
        s = _space("higher_chow")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true

    def test_singular_cohomology_not_motivic(self):
        s = _space("singular_cohomology")
        r = is_motivic_cohomology_theory(s)
        assert r.is_false

    def test_de_rham_only_not_motivic(self):
        s = _space("de_rham_only")
        r = is_motivic_cohomology_theory(s)
        assert r.is_false

    def test_topological_only_not_motivic(self):
        s = _space("topological_only")
        r = is_motivic_cohomology_theory(s)
        assert r.is_false

    def test_no_bigrading_not_motivic(self):
        s = _space("no_bigrading")
        r = is_motivic_cohomology_theory(s)
        assert r.is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = is_motivic_cohomology_theory(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("hamiltonian_vector_field")
        r = is_motivic_cohomology_theory(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("motivic_cohomology")
        r = is_motivic_cohomology_theory(s)
        assert len(r.justification) >= 1

    def test_result_metadata_has_criterion(self):
        s = _space("chow_group")
        r = is_motivic_cohomology_theory(s)
        assert "criterion" in r.metadata

    def test_bloch_kato_tag(self):
        s = _space("bloch_kato")
        r = is_motivic_cohomology_theory(s)
        assert r.is_true


# ---------------------------------------------------------------------------
# has_algebraic_k_theory_structure
# ---------------------------------------------------------------------------

class TestHasAlgebraicKTheoryStructure:
    def test_algebraic_k_theory_tag(self):
        s = _space("algebraic_k_theory")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_kgl_spectrum_tag(self):
        s = _space("kgl_spectrum")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_k_theory_spectrum_tag(self):
        s = _space("k_theory_spectrum")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_quillen_k_theory_tag(self):
        s = _space("quillen_k_theory")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_higher_k_theory_tag(self):
        s = _space("higher_k_theory")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_k0_group_tag(self):
        s = _space("k0_group")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_grothendieck_group_tag(self):
        s = _space("grothendieck_group")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_g_theory_tag(self):
        s = _space("g_theory")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_bott_periodicity_algebraic_tag(self):
        s = _space("bott_periodicity_algebraic")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_quillen_construction_tag(self):
        s = _space("quillen_construction")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_waldhausen_construction_tag(self):
        s = _space("waldhausen_construction")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_vector_bundles_tag(self):
        s = _space("vector_bundles")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_bass_quillen_tag(self):
        s = _space("bass_quillen")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_true

    def test_no_k_theory_tag(self):
        s = _space("no_k_theory")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_false

    def test_non_additive_tag(self):
        s = _space("non_additive")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_false

    def test_topological_k_only_tag(self):
        s = _space("topological_k_only")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_false

    def test_non_k_theory_tag(self):
        s = _space("non_k_theory")
        r = has_algebraic_k_theory_structure(s)
        assert r.is_false

    def test_empty_tags_unknown(self):
        s = _space()
        r = has_algebraic_k_theory_structure(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("darboux_theorem")
        r = has_algebraic_k_theory_structure(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("algebraic_k_theory")
        r = has_algebraic_k_theory_structure(s)
        assert len(r.justification) >= 1

    def test_result_metadata_has_criterion(self):
        s = _space("kgl_spectrum")
        r = has_algebraic_k_theory_structure(s)
        assert "criterion" in r.metadata


# ---------------------------------------------------------------------------
# classify_motivic
# ---------------------------------------------------------------------------

class TestClassifyMotivic:
    def test_returns_dict(self):
        s = _space("a1_invariant")
        result = classify_motivic(s)
        assert isinstance(result, dict)

    def test_has_four_keys(self):
        s = _space()
        result = classify_motivic(s)
        assert len(result) == 4

    def test_has_is_a1_invariant_key(self):
        s = _space()
        result = classify_motivic(s)
        assert "is_a1_invariant" in result

    def test_has_has_nisnevich_descent_key(self):
        s = _space()
        result = classify_motivic(s)
        assert "has_nisnevich_descent" in result

    def test_has_is_motivic_cohomology_theory_key(self):
        s = _space()
        result = classify_motivic(s)
        assert "is_motivic_cohomology_theory" in result

    def test_has_has_algebraic_k_theory_structure_key(self):
        s = _space()
        result = classify_motivic(s)
        assert "has_algebraic_k_theory_structure" in result

    def test_algebraic_k_theory_space_results(self):
        s = _space("algebraic_k_theory", "algebraic_k_theory")
        result = classify_motivic(s)
        assert result["is_a1_invariant"].is_true
        assert result["has_nisnevich_descent"].is_true
        assert result["has_algebraic_k_theory_structure"].is_true

    def test_motivic_cohomology_space_results(self):
        s = _space("motivic_cohomology", "hz_spectrum")
        result = classify_motivic(s)
        assert result["is_motivic_cohomology_theory"].is_true
        assert result["is_a1_invariant"].is_true

    def test_empty_space_all_unknown(self):
        s = _space()
        result = classify_motivic(s)
        for r in result.values():
            assert not r.is_true and not r.is_false

    def test_non_motivic_space_false_results(self):
        s = _space("singular_cohomology", "no_k_theory", "non_a1_invariant")
        result = classify_motivic(s)
        assert result["is_motivic_cohomology_theory"].is_false
        assert result["has_algebraic_k_theory_structure"].is_false
        assert result["is_a1_invariant"].is_false


# ---------------------------------------------------------------------------
# motivic_profile
# ---------------------------------------------------------------------------

class TestMotivicProfile:
    def test_returns_dict(self):
        s = _space("a1_invariant")
        result = motivic_profile(s)
        assert isinstance(result, dict)

    def test_has_space_key(self):
        s = _space()
        result = motivic_profile(s)
        assert "space" in result

    def test_has_tags_key(self):
        s = _space("a1_invariant")
        result = motivic_profile(s)
        assert "tags" in result

    def test_has_representation_key(self):
        s = _space()
        result = motivic_profile(s)
        assert "representation" in result

    def test_has_classification_key(self):
        s = _space()
        result = motivic_profile(s)
        assert "classification" in result

    def test_has_summary_key(self):
        s = _space()
        result = motivic_profile(s)
        assert "summary" in result

    def test_tags_is_sorted_list(self):
        s = _space("motivic_cohomology", "algebraic_k_theory")
        result = motivic_profile(s)
        tags = result["tags"]
        assert isinstance(tags, list)
        assert tags == sorted(tags)

    def test_summary_has_four_entries(self):
        s = _space()
        result = motivic_profile(s)
        assert len(result["summary"]) == 4

    def test_summary_values_are_strings(self):
        s = _space("algebraic_k_theory")
        result = motivic_profile(s)
        for v in result["summary"].values():
            assert isinstance(v, str)

    def test_space_attribute_preserved(self):
        s = _space("a1_invariant")
        result = motivic_profile(s)
        assert result["space"] is s
