"""Tests for pytop.noncommutative_topology."""

from __future__ import annotations

import pytest

from pytop.noncommutative_topology import (
    COMMUTATIVE_CSTAR_TAGS,
    GELFAND_DUAL_TAGS,
    KTHEORY_TAGS,
    MORITA_EQUIVALENCE_TAGS,
    NONCOMMUTATIVE_CSTAR_TAGS,
    NOT_GELFAND_TAGS,
    NUCLEAR_CSTAR_TAGS,
    SIMPLE_CSTAR_TAGS,
    SPECTRAL_TRIPLE_TAGS,
    NoncommutativeProfile,
    classify_noncommutative,
    has_gelfand_dual,
    has_spectral_triple,
    is_commutative_cstar,
    is_nuclear_cstar,
    is_simple_cstar,
    noncommutative_chapter_index,
    noncommutative_layer_summary,
    noncommutative_profile,
    noncommutative_type_index,
    get_named_noncommutative_profiles,
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
    def test_commutative_tags_nonempty(self):
        assert len(COMMUTATIVE_CSTAR_TAGS) >= 4

    def test_noncommutative_tags_nonempty(self):
        assert len(NONCOMMUTATIVE_CSTAR_TAGS) >= 5

    def test_nuclear_tags_nonempty(self):
        assert len(NUCLEAR_CSTAR_TAGS) >= 4

    def test_simple_tags_nonempty(self):
        assert len(SIMPLE_CSTAR_TAGS) >= 3

    def test_spectral_triple_tags_nonempty(self):
        assert len(SPECTRAL_TRIPLE_TAGS) >= 3

    def test_gelfand_dual_tags_nonempty(self):
        assert len(GELFAND_DUAL_TAGS) >= 3

    def test_not_gelfand_tags_nonempty(self):
        assert len(NOT_GELFAND_TAGS) >= 4

    def test_morita_tags_nonempty(self):
        assert len(MORITA_EQUIVALENCE_TAGS) >= 3

    def test_ktheory_tags_nonempty(self):
        assert len(KTHEORY_TAGS) >= 3

    def test_commutative_in_commutative_tags(self):
        assert "commutative_cstar" in COMMUTATIVE_CSTAR_TAGS

    def test_c_of_x_in_commutative_tags(self):
        assert "c_of_x" in COMMUTATIVE_CSTAR_TAGS

    def test_matrix_algebra_in_not_gelfand(self):
        assert "matrix_algebra" in NOT_GELFAND_TAGS

    def test_cuntz_in_simple_tags(self):
        assert "cuntz_algebra" in SIMPLE_CSTAR_TAGS

    def test_af_algebra_in_nuclear_tags(self):
        assert "af_algebra" in NUCLEAR_CSTAR_TAGS

    def test_dirac_in_spectral_tags(self):
        assert "dirac_operator" in SPECTRAL_TRIPLE_TAGS

    def test_irrational_rotation_in_simple_tags(self):
        assert "irrational_rotation_algebra" in SIMPLE_CSTAR_TAGS

    def test_commutative_in_gelfand_tags(self):
        assert "commutative_cstar" in GELFAND_DUAL_TAGS

    def test_gelfand_commutative_nuclear_overlap(self):
        # commutative algebras are always nuclear
        assert "commutative_cstar" in NUCLEAR_CSTAR_TAGS

    def test_all_tag_sets_contain_strings(self):
        for tag_set in [
            COMMUTATIVE_CSTAR_TAGS, NONCOMMUTATIVE_CSTAR_TAGS, NUCLEAR_CSTAR_TAGS,
            SIMPLE_CSTAR_TAGS, SPECTRAL_TRIPLE_TAGS, GELFAND_DUAL_TAGS,
            NOT_GELFAND_TAGS, MORITA_EQUIVALENCE_TAGS, KTHEORY_TAGS,
        ]:
            assert all(isinstance(t, str) for t in tag_set)


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_noncommutative_profiles(), tuple)

    def test_at_least_six_profiles(self):
        assert len(get_named_noncommutative_profiles()) >= 6

    def test_all_noncommutative_profile_instances(self):
        for p in get_named_noncommutative_profiles():
            assert isinstance(p, NoncommutativeProfile)

    def test_keys_unique(self):
        keys = [p.key for p in get_named_noncommutative_profiles()]
        assert len(keys) == len(set(keys))

    def test_display_names_nonempty(self):
        for p in get_named_noncommutative_profiles():
            assert p.display_name.strip()

    def test_focus_nonempty(self):
        for p in get_named_noncommutative_profiles():
            assert p.focus.strip()

    def test_chapter_targets_nonempty(self):
        for p in get_named_noncommutative_profiles():
            assert len(p.chapter_targets) >= 1

    def test_presentation_layers_known(self):
        known = {"main_text", "selected_block", "appendix"}
        for p in get_named_noncommutative_profiles():
            assert p.presentation_layer in known

    def test_k0_k1_are_strings(self):
        for p in get_named_noncommutative_profiles():
            assert isinstance(p.k0_group, str)
            assert isinstance(p.k1_group, str)

    # c_of_compact_space
    def test_c_of_x_present(self):
        assert "c_of_compact_space" in {p.key for p in get_named_noncommutative_profiles()}

    def test_c_of_x_commutative(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "c_of_compact_space")
        assert p.is_commutative is True

    def test_c_of_x_nuclear(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "c_of_compact_space")
        assert p.is_nuclear is True

    def test_c_of_x_has_gelfand_dual(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "c_of_compact_space")
        assert p.has_classical_gelfand_dual is True

    def test_c_of_x_not_simple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "c_of_compact_space")
        assert p.is_simple is False

    # matrix_algebra
    def test_matrix_algebra_present(self):
        assert "matrix_algebra" in {p.key for p in get_named_noncommutative_profiles()}

    def test_matrix_not_commutative(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "matrix_algebra")
        assert p.is_commutative is False

    def test_matrix_nuclear(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "matrix_algebra")
        assert p.is_nuclear is True

    def test_matrix_simple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "matrix_algebra")
        assert p.is_simple is True

    def test_matrix_no_gelfand_dual(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "matrix_algebra")
        assert p.has_classical_gelfand_dual is False

    def test_matrix_k0_z(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "matrix_algebra")
        assert "Z" in p.k0_group

    def test_matrix_k1_zero(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "matrix_algebra")
        assert "0" in p.k1_group

    def test_matrix_has_spectral_triple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "matrix_algebra")
        assert p.has_spectral_triple is True

    # noncommutative_torus
    def test_nc_torus_present(self):
        assert "noncommutative_torus" in {p.key for p in get_named_noncommutative_profiles()}

    def test_nc_torus_not_commutative(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "noncommutative_torus")
        assert p.is_commutative is False

    def test_nc_torus_nuclear(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "noncommutative_torus")
        assert p.is_nuclear is True

    def test_nc_torus_simple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "noncommutative_torus")
        assert p.is_simple is True

    def test_nc_torus_no_gelfand_dual(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "noncommutative_torus")
        assert p.has_classical_gelfand_dual is False

    def test_nc_torus_k0_z2(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "noncommutative_torus")
        assert "Z^2" in p.k0_group or "Z2" in p.k0_group

    def test_nc_torus_has_spectral_triple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "noncommutative_torus")
        assert p.has_spectral_triple is True

    # cuntz_algebra
    def test_cuntz_present(self):
        assert "cuntz_algebra" in {p.key for p in get_named_noncommutative_profiles()}

    def test_cuntz_not_commutative(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "cuntz_algebra")
        assert p.is_commutative is False

    def test_cuntz_nuclear(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "cuntz_algebra")
        assert p.is_nuclear is True

    def test_cuntz_simple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "cuntz_algebra")
        assert p.is_simple is True

    def test_cuntz_k0_torsion(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "cuntz_algebra")
        assert "Z" in p.k0_group

    # compact_operators
    def test_compact_operators_present(self):
        assert "compact_operators" in {p.key for p in get_named_noncommutative_profiles()}

    def test_compact_operators_not_commutative(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "compact_operators")
        assert p.is_commutative is False

    def test_compact_operators_nuclear(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "compact_operators")
        assert p.is_nuclear is True

    def test_compact_operators_simple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "compact_operators")
        assert p.is_simple is True

    # af_algebra
    def test_af_algebra_present(self):
        assert "af_algebra" in {p.key for p in get_named_noncommutative_profiles()}

    def test_af_not_commutative(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "af_algebra")
        assert p.is_commutative is False

    def test_af_nuclear(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "af_algebra")
        assert p.is_nuclear is True

    def test_af_not_simple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "af_algebra")
        assert p.is_simple is False

    def test_af_k1_zero(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "af_algebra")
        assert "0" in p.k1_group

    # group_cstar_algebra
    def test_group_cstar_present(self):
        assert "group_cstar_algebra" in {p.key for p in get_named_noncommutative_profiles()}

    def test_group_cstar_not_commutative(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "group_cstar_algebra")
        assert p.is_commutative is False

    def test_group_cstar_not_nuclear(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "group_cstar_algebra")
        assert p.is_nuclear is False

    def test_group_cstar_not_simple(self):
        p = next(p for p in get_named_noncommutative_profiles() if p.key == "group_cstar_algebra")
        assert p.is_simple is False


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_dict(self):
        assert isinstance(noncommutative_layer_summary(), dict)

    def test_layer_summary_main_text(self):
        assert "main_text" in noncommutative_layer_summary()

    def test_layer_summary_selected_block(self):
        assert "selected_block" in noncommutative_layer_summary()

    def test_layer_summary_total(self):
        profiles = get_named_noncommutative_profiles()
        assert sum(noncommutative_layer_summary().values()) == len(profiles)

    def test_chapter_index_dict(self):
        assert isinstance(noncommutative_chapter_index(), dict)

    def test_chapter_index_sorted(self):
        ch = noncommutative_chapter_index()
        assert list(ch.keys()) == sorted(ch.keys())

    def test_chapter_index_tuples(self):
        for v in noncommutative_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_nonempty_values(self):
        for v in noncommutative_chapter_index().values():
            assert len(v) >= 1

    def test_type_index_dict(self):
        assert isinstance(noncommutative_type_index(), dict)

    def test_type_index_has_commutative(self):
        assert "commutative_cstar" in noncommutative_type_index()

    def test_type_index_tuples(self):
        for v in noncommutative_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_total(self):
        total = sum(len(v) for v in noncommutative_type_index().values())
        assert total == len(get_named_noncommutative_profiles())


# ---------------------------------------------------------------------------
# is_commutative_cstar
# ---------------------------------------------------------------------------

class TestIsCommutativeCstar:
    def test_commutative_cstar_tag_true(self):
        assert is_commutative_cstar(_space("commutative_cstar")).is_true

    def test_c_of_x_tag_true(self):
        assert is_commutative_cstar(_space("c_of_x")).is_true

    def test_abelian_cstar_true(self):
        assert is_commutative_cstar(_space("abelian_cstar")).is_true

    def test_gelfand_dual_true(self):
        assert is_commutative_cstar(_space("gelfand_dual")).is_true

    def test_function_algebra_true(self):
        assert is_commutative_cstar(_space("function_algebra")).is_true

    def test_c_of_compact_space_true(self):
        assert is_commutative_cstar(_space("c_of_compact_space")).is_true

    def test_matrix_algebra_false(self):
        assert is_commutative_cstar(_space("matrix_algebra")).is_false

    def test_noncommutative_cstar_false(self):
        assert is_commutative_cstar(_space("noncommutative_cstar")).is_false

    def test_noncommutative_torus_false(self):
        assert is_commutative_cstar(_space("noncommutative_torus")).is_false

    def test_cuntz_algebra_false(self):
        assert is_commutative_cstar(_space("cuntz_algebra")).is_false

    def test_compact_operators_false(self):
        assert is_commutative_cstar(_space("compact_operators")).is_false

    def test_b_of_h_false(self):
        assert is_commutative_cstar(_space("b_of_h")).is_false

    def test_no_gelfand_false(self):
        assert is_commutative_cstar(_space("no_gelfand_dual")).is_false

    def test_unknown_empty(self):
        r = is_commutative_cstar(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert is_commutative_cstar(_space("commutative_cstar")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_commutative_cstar(_space("matrix_algebra")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert is_commutative_cstar(_space()).mode == "symbolic"

    def test_criterion_explicit(self):
        r = is_commutative_cstar(_space("commutative_cstar"))
        assert r.metadata.get("criterion") == "explicit_commutative"

    def test_criterion_noncommutative(self):
        r = is_commutative_cstar(_space("matrix_algebra"))
        assert r.metadata.get("criterion") == "noncommutative"

    def test_reduced_group_cstar_false(self):
        assert is_commutative_cstar(_space("reduced_group_cstar")).is_false

    def test_car_algebra_false(self):
        assert is_commutative_cstar(_space("car_algebra")).is_false

    def test_von_neumann_false(self):
        assert is_commutative_cstar(_space("von_neumann_algebra")).is_false


# ---------------------------------------------------------------------------
# is_nuclear_cstar
# ---------------------------------------------------------------------------

class TestIsNuclearCstar:
    def test_nuclear_cstar_true(self):
        assert is_nuclear_cstar(_space("nuclear_cstar")).is_true

    def test_commutative_cstar_nuclear(self):
        assert is_nuclear_cstar(_space("commutative_cstar")).is_true

    def test_af_algebra_nuclear(self):
        assert is_nuclear_cstar(_space("af_algebra")).is_true

    def test_car_algebra_nuclear(self):
        assert is_nuclear_cstar(_space("car_algebra")).is_true

    def test_cuntz_algebra_nuclear(self):
        assert is_nuclear_cstar(_space("cuntz_algebra")).is_true

    def test_amenable_group_nuclear(self):
        assert is_nuclear_cstar(_space("amenable_group_cstar")).is_true

    def test_abelian_cstar_nuclear(self):
        assert is_nuclear_cstar(_space("abelian_cstar")).is_true

    def test_b_of_h_not_nuclear(self):
        assert is_nuclear_cstar(_space("b_of_h")).is_false

    def test_non_nuclear_cstar_false(self):
        assert is_nuclear_cstar(_space("non_nuclear_cstar")).is_false

    def test_free_group_cstar_false(self):
        assert is_nuclear_cstar(_space("free_group_cstar")).is_false

    def test_non_amenable_group_false(self):
        assert is_nuclear_cstar(_space("non_amenable_group_cstar")).is_false

    def test_unknown_empty(self):
        r = is_nuclear_cstar(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit_nuclear(self):
        r = is_nuclear_cstar(_space("nuclear_cstar"))
        assert r.metadata.get("criterion") == "explicit_nuclear"

    def test_criterion_not_nuclear(self):
        r = is_nuclear_cstar(_space("b_of_h"))
        assert r.metadata.get("criterion") == "not_nuclear"

    def test_approximately_finite_nuclear(self):
        assert is_nuclear_cstar(_space("approximately_finite")).is_true

    def test_inductive_limit_nuclear(self):
        assert is_nuclear_cstar(_space("inductive_limit")).is_true


# ---------------------------------------------------------------------------
# is_simple_cstar
# ---------------------------------------------------------------------------

class TestIsSimpleCstar:
    def test_simple_cstar_tag_true(self):
        assert is_simple_cstar(_space("simple_cstar")).is_true

    def test_irrational_rotation_simple(self):
        assert is_simple_cstar(_space("irrational_rotation_algebra")).is_true

    def test_cuntz_simple(self):
        assert is_simple_cstar(_space("cuntz_algebra")).is_true

    def test_car_algebra_simple(self):
        assert is_simple_cstar(_space("car_algebra")).is_true

    def test_purely_infinite_simple(self):
        assert is_simple_cstar(_space("purely_infinite_simple")).is_true

    def test_noncommutative_torus_irrational_simple(self):
        assert is_simple_cstar(_space("noncommutative_torus_irrational")).is_true

    def test_commutative_cstar_not_simple(self):
        assert is_simple_cstar(_space("commutative_cstar")).is_false

    def test_c_of_x_not_simple(self):
        assert is_simple_cstar(_space("c_of_x")).is_false

    def test_af_algebra_not_simple(self):
        assert is_simple_cstar(_space("af_algebra")).is_false

    def test_group_cstar_not_simple(self):
        assert is_simple_cstar(_space("group_cstar_algebra")).is_false

    def test_toeplitz_not_simple(self):
        assert is_simple_cstar(_space("toeplitz_algebra")).is_false

    def test_not_simple_tag_false(self):
        assert is_simple_cstar(_space("not_simple_cstar")).is_false

    def test_unknown_empty(self):
        r = is_simple_cstar(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit_simple(self):
        r = is_simple_cstar(_space("simple_cstar"))
        assert r.metadata.get("criterion") == "explicit_simple"

    def test_criterion_not_simple(self):
        r = is_simple_cstar(_space("af_algebra"))
        assert r.metadata.get("criterion") == "not_simple"

    def test_inductive_limit_not_simple(self):
        assert is_simple_cstar(_space("inductive_limit")).is_false

    def test_reduced_group_cstar_not_simple(self):
        assert is_simple_cstar(_space("reduced_group_cstar")).is_false


# ---------------------------------------------------------------------------
# has_gelfand_dual
# ---------------------------------------------------------------------------

class TestHasGelfandDual:
    def test_gelfand_dual_tag_true(self):
        assert has_gelfand_dual(_space("gelfand_dual")).is_true

    def test_commutative_cstar_true(self):
        assert has_gelfand_dual(_space("commutative_cstar")).is_true

    def test_c_of_x_true(self):
        assert has_gelfand_dual(_space("c_of_x")).is_true

    def test_abelian_cstar_true(self):
        assert has_gelfand_dual(_space("abelian_cstar")).is_true

    def test_character_space_true(self):
        assert has_gelfand_dual(_space("character_space")).is_true

    def test_maximal_ideal_space_true(self):
        assert has_gelfand_dual(_space("maximal_ideal_space")).is_true

    def test_matrix_algebra_no_gelfand(self):
        assert has_gelfand_dual(_space("matrix_algebra")).is_false

    def test_b_of_h_no_gelfand(self):
        assert has_gelfand_dual(_space("b_of_h")).is_false

    def test_compact_operators_no_gelfand(self):
        assert has_gelfand_dual(_space("compact_operators")).is_false

    def test_noncommutative_cstar_false(self):
        assert has_gelfand_dual(_space("noncommutative_cstar")).is_false

    def test_cuntz_no_gelfand(self):
        assert has_gelfand_dual(_space("cuntz_algebra")).is_false

    def test_no_gelfand_tag_false(self):
        assert has_gelfand_dual(_space("no_gelfand_dual")).is_false

    def test_unknown_empty(self):
        r = has_gelfand_dual(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit_gelfand(self):
        r = has_gelfand_dual(_space("gelfand_dual"))
        assert r.metadata.get("criterion") == "explicit_gelfand"

    def test_criterion_no_gelfand(self):
        r = has_gelfand_dual(_space("matrix_algebra"))
        assert r.metadata.get("criterion") == "no_gelfand_dual"

    def test_car_algebra_no_gelfand(self):
        assert has_gelfand_dual(_space("car_algebra")).is_false

    def test_irrational_rotation_no_gelfand(self):
        assert has_gelfand_dual(_space("irrational_rotation_algebra")).is_false

    def test_von_neumann_no_gelfand(self):
        assert has_gelfand_dual(_space("von_neumann_algebra")).is_false


# ---------------------------------------------------------------------------
# has_spectral_triple
# ---------------------------------------------------------------------------

class TestHasSpectralTriple:
    def test_spectral_triple_tag_true(self):
        assert has_spectral_triple(_space("spectral_triple")).is_true

    def test_dirac_operator_true(self):
        assert has_spectral_triple(_space("dirac_operator")).is_true

    def test_noncommutative_manifold_true(self):
        assert has_spectral_triple(_space("noncommutative_manifold")).is_true

    def test_connes_spectral_triple_true(self):
        assert has_spectral_triple(_space("connes_spectral_triple")).is_true

    def test_matrix_algebra_class_true(self):
        assert has_spectral_triple(_space("matrix_algebra")).is_true

    def test_noncommutative_torus_class_true(self):
        assert has_spectral_triple(_space("noncommutative_torus")).is_true

    def test_irrational_rotation_true(self):
        assert has_spectral_triple(_space("irrational_rotation_algebra")).is_true

    def test_c_of_compact_space_true(self):
        assert has_spectral_triple(_space("c_of_compact_space")).is_true

    def test_spinc_manifold_true(self):
        assert has_spectral_triple(_space("spinc_manifold")).is_true

    def test_cuntz_no_spectral_triple(self):
        assert has_spectral_triple(_space("cuntz_algebra")).is_false

    def test_af_algebra_no_spectral_triple(self):
        assert has_spectral_triple(_space("af_algebra")).is_false

    def test_group_cstar_no_spectral_triple(self):
        assert has_spectral_triple(_space("group_cstar_algebra")).is_false

    def test_no_spectral_triple_tag_false(self):
        assert has_spectral_triple(_space("no_spectral_triple")).is_false

    def test_purely_infinite_no_trace_false(self):
        assert has_spectral_triple(_space("purely_infinite_no_trace")).is_false

    def test_unknown_empty(self):
        r = has_spectral_triple(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit(self):
        r = has_spectral_triple(_space("spectral_triple"))
        assert r.metadata.get("criterion") == "explicit_spectral_triple"

    def test_criterion_known_class(self):
        r = has_spectral_triple(_space("matrix_algebra"))
        assert r.metadata.get("criterion") == "known_spectral_triple_class"

    def test_criterion_no_spectral_triple(self):
        r = has_spectral_triple(_space("cuntz_algebra"))
        assert r.metadata.get("criterion") == "no_spectral_triple"

    def test_riemannian_manifold_algebra_true(self):
        assert has_spectral_triple(_space("riemannian_manifold_algebra")).is_true

    def test_finitely_summable_triple_true(self):
        assert has_spectral_triple(_space("finitely_summable_triple")).is_true


# ---------------------------------------------------------------------------
# classify_noncommutative
# ---------------------------------------------------------------------------

class TestClassifyNoncommutative:
    def test_returns_dict(self):
        assert isinstance(classify_noncommutative(_space()), dict)

    def test_required_keys(self):
        r = classify_noncommutative(_space())
        assert {
            "algebra_class", "is_commutative", "is_nuclear", "is_simple",
            "has_gelfand_dual", "has_spectral_triple", "key_properties",
            "representation", "tags",
        } <= r.keys()

    def test_commutative_class(self):
        r = classify_noncommutative(_space("commutative_cstar"))
        assert r["algebra_class"] == "commutative"

    def test_simple_nuclear_class(self):
        r = classify_noncommutative(_space("irrational_rotation_algebra", "nuclear_cstar"))
        assert r["algebra_class"] == "simple_nuclear"

    def test_nuclear_class(self):
        r = classify_noncommutative(_space("af_algebra"))
        assert r["algebra_class"] == "nuclear"

    def test_simple_class(self):
        # simple but NOT detected as nuclear via tags
        r = classify_noncommutative(_space("simple_cstar"))
        # simple_cstar is not in nuclear tags, so nuclear is unknown
        assert r["algebra_class"] in {"simple", "simple_nuclear", "unknown", "general"}

    def test_commutative_in_properties(self):
        r = classify_noncommutative(_space("commutative_cstar"))
        assert "commutative" in r["key_properties"]

    def test_nuclear_in_properties(self):
        r = classify_noncommutative(_space("af_algebra"))
        assert "nuclear" in r["key_properties"]

    def test_simple_in_properties(self):
        r = classify_noncommutative(_space("cuntz_algebra"))
        assert "simple" in r["key_properties"]

    def test_gelfand_dual_in_properties(self):
        r = classify_noncommutative(_space("commutative_cstar"))
        assert "gelfand_dual_exists" in r["key_properties"]

    def test_spectral_triple_in_properties(self):
        r = classify_noncommutative(_space("matrix_algebra"))
        assert "spectral_triple" in r["key_properties"]

    def test_ktheory_in_properties(self):
        r = classify_noncommutative(_space("k0_nontrivial"))
        assert "ktheory_nontrivial" in r["key_properties"]

    def test_morita_in_properties(self):
        r = classify_noncommutative(_space("morita_equivalent"))
        assert "morita_context" in r["key_properties"]

    def test_noncommutative_in_properties(self):
        r = classify_noncommutative(_space("matrix_algebra"))
        assert "noncommutative" in r["key_properties"]

    def test_no_gelfand_in_properties(self):
        r = classify_noncommutative(_space("matrix_algebra"))
        assert "no_gelfand_dual" in r["key_properties"]

    def test_tags_sorted(self):
        r = classify_noncommutative(_space("cuntz_algebra", "nuclear_cstar"))
        assert r["tags"] == sorted(r["tags"])

    def test_representation_passthrough(self):
        r = classify_noncommutative(_space("commutative_cstar", rep="test_rep"))
        assert r["representation"] == "test_rep"

    def test_general_class_b_of_h(self):
        r = classify_noncommutative(_space("b_of_h"))
        # noncommutative, not nuclear -> general
        assert r["algebra_class"] in {"general", "unknown"}


# ---------------------------------------------------------------------------
# noncommutative_profile
# ---------------------------------------------------------------------------

class TestNoncommutativeProfile:
    def test_returns_dict(self):
        assert isinstance(noncommutative_profile(_space()), dict)

    def test_has_classification(self):
        assert "classification" in noncommutative_profile(_space())

    def test_has_named_profiles(self):
        assert "named_profiles" in noncommutative_profile(_space())

    def test_has_layer_summary(self):
        assert "layer_summary" in noncommutative_profile(_space())

    def test_classification_is_dict(self):
        assert isinstance(noncommutative_profile(_space())["classification"], dict)

    def test_named_profiles_is_tuple(self):
        assert isinstance(noncommutative_profile(_space())["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        assert isinstance(noncommutative_profile(_space())["layer_summary"], dict)

    def test_named_profiles_nonempty(self):
        assert len(noncommutative_profile(_space())["named_profiles"]) >= 6


# ---------------------------------------------------------------------------
# NoncommutativeProfile dataclass
# ---------------------------------------------------------------------------

class TestNoncommutativeProfileDataclass:
    def test_frozen(self):
        p = NoncommutativeProfile(
            key="t", display_name="T", algebra_type="commutative_cstar",
            is_commutative=True, is_nuclear=True, is_simple=False,
            has_classical_gelfand_dual=True, has_spectral_triple=False,
            k0_group="Z", k1_group="0", presentation_layer="main_text",
            focus="f", chapter_targets=("1",),
        )
        with pytest.raises(Exception):
            p.key = "other"  # type: ignore[misc]

    def test_equality_by_value(self):
        kwargs = dict(
            key="t", display_name="T", algebra_type="commutative_cstar",
            is_commutative=True, is_nuclear=True, is_simple=False,
            has_classical_gelfand_dual=True, has_spectral_triple=False,
            k0_group="Z", k1_group="0", presentation_layer="main_text",
            focus="f", chapter_targets=("1",),
        )
        assert NoncommutativeProfile(**kwargs) == NoncommutativeProfile(**kwargs)

    def test_all_fields_accessible(self):
        p = NoncommutativeProfile(
            key="x", display_name="X", algebra_type="matrix_algebra",
            is_commutative=False, is_nuclear=True, is_simple=True,
            has_classical_gelfand_dual=False, has_spectral_triple=True,
            k0_group="Z", k1_group="0", presentation_layer="main_text",
            focus="matrix", chapter_targets=("1", "2"),
        )
        assert p.algebra_type == "matrix_algebra"
        assert p.k0_group == "Z"
        assert p.chapter_targets == ("1", "2")
