"""Tests for pytop.derived_categories."""

from __future__ import annotations

import pytest

from pytop.derived_categories import (
    BONDAL_ORLOV_TAGS,
    DERIVED_CATEGORY_TAGS,
    DERIVED_FUNCTOR_TAGS,
    DG_ENHANCEMENT_TAGS,
    PERVERSE_SHEAF_TAGS,
    SEMIORTHOGONAL_TAGS,
    T_STRUCTURE_TAGS,
    TRIANGULATED_STRUCTURE_TAGS,
    DerivedCategoryProfile,
    classify_derived_category,
    derived_category_chapter_index,
    derived_category_layer_summary,
    derived_category_profile,
    derived_category_type_index,
    get_named_derived_category_profiles,
    has_semiorthogonal_decomposition,
    has_t_structure,
    is_dg_enhanced,
    is_triangulated,
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
    def test_derived_category_tags_nonempty(self):
        assert len(DERIVED_CATEGORY_TAGS) >= 4

    def test_triangulated_structure_tags_nonempty(self):
        assert len(TRIANGULATED_STRUCTURE_TAGS) >= 4

    def test_t_structure_tags_nonempty(self):
        assert len(T_STRUCTURE_TAGS) >= 4

    def test_derived_functor_tags_nonempty(self):
        assert len(DERIVED_FUNCTOR_TAGS) >= 4

    def test_semiorthogonal_tags_nonempty(self):
        assert len(SEMIORTHOGONAL_TAGS) >= 4

    def test_dg_enhancement_tags_nonempty(self):
        assert len(DG_ENHANCEMENT_TAGS) >= 4

    def test_bondal_orlov_tags_nonempty(self):
        assert len(BONDAL_ORLOV_TAGS) >= 4

    def test_perverse_sheaf_tags_nonempty(self):
        assert len(PERVERSE_SHEAF_TAGS) >= 4

    def test_derived_category_in_derived_tags(self):
        assert "derived_category" in DERIVED_CATEGORY_TAGS

    def test_db_coh_in_derived_tags(self):
        assert "db_coh" in DERIVED_CATEGORY_TAGS

    def test_triangulated_category_in_triang_tags(self):
        assert "triangulated_category" in TRIANGULATED_STRUCTURE_TAGS

    def test_distinguished_triangle_in_triang_tags(self):
        assert "distinguished_triangle" in TRIANGULATED_STRUCTURE_TAGS

    def test_shift_functor_in_triang_tags(self):
        assert "shift_functor" in TRIANGULATED_STRUCTURE_TAGS

    def test_t_structure_in_t_tags(self):
        assert "t_structure" in T_STRUCTURE_TAGS

    def test_heart_of_t_structure_in_t_tags(self):
        assert "heart_of_t_structure" in T_STRUCTURE_TAGS

    def test_perverse_t_structure_in_t_tags(self):
        assert "perverse_t_structure" in T_STRUCTURE_TAGS

    def test_rhom_in_derived_functor_tags(self):
        assert "rhom" in DERIVED_FUNCTOR_TAGS

    def test_derived_tensor_product_in_derived_functor_tags(self):
        assert "derived_tensor_product" in DERIVED_FUNCTOR_TAGS

    def test_semiorthogonal_decomposition_in_sod_tags(self):
        assert "semiorthogonal_decomposition" in SEMIORTHOGONAL_TAGS

    def test_exceptional_collection_in_sod_tags(self):
        assert "exceptional_collection" in SEMIORTHOGONAL_TAGS

    def test_beilinson_collection_in_sod_tags(self):
        assert "beilinson_collection" in SEMIORTHOGONAL_TAGS

    def test_dg_enhancement_in_dg_tags(self):
        assert "dg_enhancement" in DG_ENHANCEMENT_TAGS

    def test_dg_category_in_dg_tags(self):
        assert "dg_category" in DG_ENHANCEMENT_TAGS

    def test_fourier_mukai_in_bondal_tags(self):
        assert "fourier_mukai" in BONDAL_ORLOV_TAGS

    def test_tilting_generator_in_bondal_tags(self):
        assert "tilting_generator" in BONDAL_ORLOV_TAGS

    def test_perverse_sheaves_in_perverse_tags(self):
        assert "perverse_sheaves" in PERVERSE_SHEAF_TAGS

    def test_intersection_cohomology_in_perverse_tags(self):
        assert "intersection_cohomology" in PERVERSE_SHEAF_TAGS

    def test_bbd_in_perverse_tags(self):
        assert "bbd" in PERVERSE_SHEAF_TAGS

    def test_all_tag_sets_contain_strings(self):
        for tag_set in [
            DERIVED_CATEGORY_TAGS, TRIANGULATED_STRUCTURE_TAGS, T_STRUCTURE_TAGS,
            DERIVED_FUNCTOR_TAGS, SEMIORTHOGONAL_TAGS, DG_ENHANCEMENT_TAGS,
            BONDAL_ORLOV_TAGS, PERVERSE_SHEAF_TAGS,
        ]:
            assert all(isinstance(t, str) for t in tag_set)

    def test_sod_and_t_structure_disjoint(self):
        assert SEMIORTHOGONAL_TAGS.isdisjoint(T_STRUCTURE_TAGS)


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_derived_category_profiles(), tuple)

    def test_at_least_six_profiles(self):
        assert len(get_named_derived_category_profiles()) >= 6

    def test_exactly_seven_profiles(self):
        assert len(get_named_derived_category_profiles()) == 7

    def test_all_derived_category_profile_instances(self):
        for p in get_named_derived_category_profiles():
            assert isinstance(p, DerivedCategoryProfile)

    def test_keys_unique(self):
        keys = [p.key for p in get_named_derived_category_profiles()]
        assert len(keys) == len(set(keys))

    def test_display_names_nonempty(self):
        for p in get_named_derived_category_profiles():
            assert p.display_name.strip()

    def test_focus_nonempty(self):
        for p in get_named_derived_category_profiles():
            assert p.focus.strip()

    def test_chapter_targets_nonempty(self):
        for p in get_named_derived_category_profiles():
            assert len(p.chapter_targets) >= 1

    def test_presentation_layers_known(self):
        known = {"main_text", "selected_block", "appendix"}
        for p in get_named_derived_category_profiles():
            assert p.presentation_layer in known

    def test_has_t_structure_bool(self):
        for p in get_named_derived_category_profiles():
            assert isinstance(p.has_t_structure, bool)

    def test_is_enhanced_bool(self):
        for p in get_named_derived_category_profiles():
            assert isinstance(p.is_enhanced, bool)

    def test_has_semiorthogonal_decomp_bool(self):
        for p in get_named_derived_category_profiles():
            assert isinstance(p.has_semiorthogonal_decomp, bool)

    # derived_category_abelian
    def test_derived_abelian_present(self):
        assert "derived_category_abelian" in {p.key for p in get_named_derived_category_profiles()}

    def test_derived_abelian_has_t_structure(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "derived_category_abelian")
        assert p.has_t_structure is True

    def test_derived_abelian_not_enhanced(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "derived_category_abelian")
        assert p.is_enhanced is False

    def test_derived_abelian_no_sod(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "derived_category_abelian")
        assert p.has_semiorthogonal_decomp is False

    # bounded_derived_coherent
    def test_bounded_derived_present(self):
        assert "bounded_derived_coherent" in {p.key for p in get_named_derived_category_profiles()}

    def test_bounded_derived_has_t_structure(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "bounded_derived_coherent")
        assert p.has_t_structure is True

    def test_bounded_derived_is_enhanced(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "bounded_derived_coherent")
        assert p.is_enhanced is True

    def test_bounded_derived_has_sod(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "bounded_derived_coherent")
        assert p.has_semiorthogonal_decomp is True

    # perverse_sheaves_bbd
    def test_perverse_present(self):
        assert "perverse_sheaves_bbd" in {p.key for p in get_named_derived_category_profiles()}

    def test_perverse_has_t_structure(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "perverse_sheaves_bbd")
        assert p.has_t_structure is True

    def test_perverse_no_sod(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "perverse_sheaves_bbd")
        assert p.has_semiorthogonal_decomp is False

    def test_perverse_category_type(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "perverse_sheaves_bbd")
        assert p.category_type == "perverse"

    # exceptional_collection_projective_space
    def test_exceptional_present(self):
        assert "exceptional_collection_projective_space" in {
            p.key for p in get_named_derived_category_profiles()
        }

    def test_exceptional_has_sod(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "exceptional_collection_projective_space")
        assert p.has_semiorthogonal_decomp is True

    def test_exceptional_is_enhanced(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "exceptional_collection_projective_space")
        assert p.is_enhanced is True

    # fourier_mukai_transform
    def test_fourier_mukai_present(self):
        assert "fourier_mukai_transform" in {p.key for p in get_named_derived_category_profiles()}

    def test_fourier_mukai_is_enhanced(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "fourier_mukai_transform")
        assert p.is_enhanced is True

    def test_fourier_mukai_no_t_structure(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "fourier_mukai_transform")
        assert p.has_t_structure is False

    # semiorthogonal_decomposition
    def test_sod_profile_present(self):
        assert "semiorthogonal_decomposition" in {p.key for p in get_named_derived_category_profiles()}

    def test_sod_has_sod(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "semiorthogonal_decomposition")
        assert p.has_semiorthogonal_decomp is True

    # dg_enhancement_uniqueness
    def test_dg_enhancement_present(self):
        assert "dg_enhancement_uniqueness" in {p.key for p in get_named_derived_category_profiles()}

    def test_dg_enhancement_is_enhanced(self):
        p = next(p for p in get_named_derived_category_profiles()
                 if p.key == "dg_enhancement_uniqueness")
        assert p.is_enhanced is True


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_is_dict(self):
        assert isinstance(derived_category_layer_summary(), dict)

    def test_layer_summary_has_main_text(self):
        assert "main_text" in derived_category_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in derived_category_layer_summary()

    def test_layer_summary_total(self):
        profiles = get_named_derived_category_profiles()
        assert sum(derived_category_layer_summary().values()) == len(profiles)

    def test_chapter_index_is_dict(self):
        assert isinstance(derived_category_chapter_index(), dict)

    def test_chapter_index_sorted(self):
        ch = derived_category_chapter_index()
        assert list(ch.keys()) == sorted(ch.keys())

    def test_chapter_index_tuples(self):
        for v in derived_category_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_nonempty_values(self):
        for v in derived_category_chapter_index().values():
            assert len(v) >= 1

    def test_type_index_is_dict(self):
        assert isinstance(derived_category_type_index(), dict)

    def test_type_index_has_derived_category(self):
        assert "derived_category" in derived_category_type_index()

    def test_type_index_has_perverse(self):
        assert "perverse" in derived_category_type_index()

    def test_type_index_tuples(self):
        for v in derived_category_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_total(self):
        total = sum(len(v) for v in derived_category_type_index().values())
        assert total == len(get_named_derived_category_profiles())


# ---------------------------------------------------------------------------
# is_triangulated
# ---------------------------------------------------------------------------

class TestIsTriangulated:
    def test_triangulated_category_tag_true(self):
        assert is_triangulated(_space("triangulated_category")).is_true

    def test_distinguished_triangle_true(self):
        assert is_triangulated(_space("distinguished_triangle")).is_true

    def test_shift_functor_true(self):
        assert is_triangulated(_space("shift_functor")).is_true

    def test_octahedral_axiom_true(self):
        assert is_triangulated(_space("octahedral_axiom")).is_true

    def test_rotation_axiom_true(self):
        assert is_triangulated(_space("rotation_axiom")).is_true

    def test_triangulated_functor_true(self):
        assert is_triangulated(_space("triangulated_functor")).is_true

    def test_exact_triangle_true(self):
        assert is_triangulated(_space("exact_triangle")).is_true

    def test_derived_category_true(self):
        assert is_triangulated(_space("derived_category")).is_true

    def test_homotopy_category_true(self):
        assert is_triangulated(_space("homotopy_category")).is_true

    def test_db_coh_true(self):
        assert is_triangulated(_space("db_coh")).is_true

    def test_bounded_derived_true(self):
        assert is_triangulated(_space("bounded_derived")).is_true

    def test_chain_complexes_true(self):
        assert is_triangulated(_space("chain_complexes")).is_true

    def test_stable_infinity_category_true(self):
        assert is_triangulated(_space("stable_infinity_category")).is_true

    def test_abelian_category_false(self):
        assert is_triangulated(_space("abelian_category")).is_false

    def test_not_triangulated_false(self):
        assert is_triangulated(_space("not_triangulated")).is_false

    def test_additive_only_false(self):
        assert is_triangulated(_space("additive_only")).is_false

    def test_plain_module_category_false(self):
        assert is_triangulated(_space("plain_module_category")).is_false

    def test_unknown_empty(self):
        r = is_triangulated(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert is_triangulated(_space("triangulated_category")).mode == "theorem"

    def test_mode_theorem_derived(self):
        assert is_triangulated(_space("derived_category")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_triangulated(_space("abelian_category")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert is_triangulated(_space()).mode == "symbolic"

    def test_criterion_explicit_triangulated(self):
        r = is_triangulated(_space("triangulated_category"))
        assert r.metadata.get("criterion") == "explicit_triangulated"

    def test_criterion_derived_implies_triangulated(self):
        r = is_triangulated(_space("derived_category"))
        assert r.metadata.get("criterion") == "derived_implies_triangulated"

    def test_criterion_not_triangulated(self):
        r = is_triangulated(_space("abelian_category"))
        assert r.metadata.get("criterion") == "not_triangulated"

    def test_stable_model_category_true(self):
        assert is_triangulated(_space("stable_model_category")).is_true

    def test_unbounded_derived_true(self):
        assert is_triangulated(_space("unbounded_derived")).is_true


# ---------------------------------------------------------------------------
# has_t_structure
# ---------------------------------------------------------------------------

class TestHasTStructure:
    def test_t_structure_tag_true(self):
        assert has_t_structure(_space("t_structure")).is_true

    def test_heart_of_t_structure_true(self):
        assert has_t_structure(_space("heart_of_t_structure")).is_true

    def test_truncation_functor_true(self):
        assert has_t_structure(_space("truncation_functor")).is_true

    def test_perverse_t_structure_true(self):
        assert has_t_structure(_space("perverse_t_structure")).is_true

    def test_standard_t_structure_true(self):
        assert has_t_structure(_space("standard_t_structure")).is_true

    def test_bbd_t_structure_true(self):
        assert has_t_structure(_space("bbd_t_structure")).is_true

    def test_perverse_sheaves_true(self):
        assert has_t_structure(_space("perverse_sheaves")).is_true

    def test_bbd_tag_true(self):
        assert has_t_structure(_space("bbd")).is_true

    def test_intersection_cohomology_true(self):
        assert has_t_structure(_space("intersection_cohomology")).is_true

    def test_derived_category_true(self):
        assert has_t_structure(_space("derived_category")).is_true

    def test_db_coh_true(self):
        assert has_t_structure(_space("db_coh")).is_true

    def test_bounded_derived_true(self):
        assert has_t_structure(_space("bounded_derived")).is_true

    def test_no_t_structure_false(self):
        assert has_t_structure(_space("no_t_structure")).is_false

    def test_homotopy_category_only_false(self):
        assert has_t_structure(_space("homotopy_category_only")).is_false

    def test_unknown_empty(self):
        r = has_t_structure(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert has_t_structure(_space("t_structure")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert has_t_structure(_space("no_t_structure")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert has_t_structure(_space()).mode == "symbolic"

    def test_criterion_explicit_t_structure(self):
        r = has_t_structure(_space("t_structure"))
        assert r.metadata.get("criterion") == "explicit_t_structure"

    def test_criterion_perverse(self):
        r = has_t_structure(_space("perverse_sheaves"))
        assert r.metadata.get("criterion") == "perverse_t_structure"

    def test_criterion_standard_t_structure(self):
        r = has_t_structure(_space("derived_category"))
        assert r.metadata.get("criterion") == "standard_t_structure"

    def test_criterion_no_t_structure(self):
        r = has_t_structure(_space("no_t_structure"))
        assert r.metadata.get("criterion") == "no_t_structure"

    def test_ic_sheaf_true(self):
        assert has_t_structure(_space("ic_sheaf")).is_true

    def test_cohomological_functor_true(self):
        assert has_t_structure(_space("cohomological_functor")).is_true


# ---------------------------------------------------------------------------
# has_semiorthogonal_decomposition
# ---------------------------------------------------------------------------

class TestHasSemiorthogonalDecomposition:
    def test_sod_tag_true(self):
        assert has_semiorthogonal_decomposition(_space("semiorthogonal_decomposition")).is_true

    def test_exceptional_collection_true(self):
        assert has_semiorthogonal_decomposition(_space("exceptional_collection")).is_true

    def test_exceptional_object_true(self):
        assert has_semiorthogonal_decomposition(_space("exceptional_object")).is_true

    def test_full_exceptional_collection_true(self):
        assert has_semiorthogonal_decomposition(_space("full_exceptional_collection")).is_true

    def test_admissible_subcategory_true(self):
        assert has_semiorthogonal_decomposition(_space("admissible_subcategory")).is_true

    def test_beilinson_collection_true(self):
        assert has_semiorthogonal_decomposition(_space("beilinson_collection")).is_true

    def test_projective_space_true(self):
        assert has_semiorthogonal_decomposition(_space("projective_space")).is_true

    def test_fano_variety_true(self):
        assert has_semiorthogonal_decomposition(_space("fano_variety")).is_true

    def test_del_pezzo_surface_true(self):
        assert has_semiorthogonal_decomposition(_space("del_pezzo_surface")).is_true

    def test_line_bundle_collection_true(self):
        assert has_semiorthogonal_decomposition(_space("line_bundle_collection")).is_true

    def test_k3_surface_false(self):
        assert has_semiorthogonal_decomposition(_space("k3_surface")).is_false

    def test_calabi_yau_false(self):
        assert has_semiorthogonal_decomposition(_space("calabi_yau")).is_false

    def test_trivial_canonical_bundle_false(self):
        assert has_semiorthogonal_decomposition(_space("trivial_canonical_bundle")).is_false

    def test_abelian_variety_sheaves_false(self):
        assert has_semiorthogonal_decomposition(_space("abelian_variety_sheaves")).is_false

    def test_no_exceptional_objects_false(self):
        assert has_semiorthogonal_decomposition(_space("no_exceptional_objects")).is_false

    def test_unknown_empty(self):
        r = has_semiorthogonal_decomposition(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert has_semiorthogonal_decomposition(_space("exceptional_collection")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert has_semiorthogonal_decomposition(_space("k3_surface")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert has_semiorthogonal_decomposition(_space()).mode == "symbolic"

    def test_criterion_explicit_sod(self):
        r = has_semiorthogonal_decomposition(_space("semiorthogonal_decomposition"))
        assert r.metadata.get("criterion") == "explicit_sod"

    def test_criterion_fano_exceptional(self):
        r = has_semiorthogonal_decomposition(_space("projective_space"))
        assert r.metadata.get("criterion") == "fano_exceptional_collection"

    def test_criterion_no_sod_trivial_canonical(self):
        r = has_semiorthogonal_decomposition(_space("k3_surface"))
        assert r.metadata.get("criterion") == "no_sod_trivial_canonical"

    def test_mutation_exceptional_true(self):
        assert has_semiorthogonal_decomposition(_space("mutation_exceptional")).is_true


# ---------------------------------------------------------------------------
# is_dg_enhanced
# ---------------------------------------------------------------------------

class TestIsDgEnhanced:
    def test_dg_enhancement_tag_true(self):
        assert is_dg_enhanced(_space("dg_enhancement")).is_true

    def test_dg_category_true(self):
        assert is_dg_enhanced(_space("dg_category")).is_true

    def test_a_infinity_category_true(self):
        assert is_dg_enhanced(_space("a_infinity_category")).is_true

    def test_pretriangulated_dg_true(self):
        assert is_dg_enhanced(_space("pretriangulated_dg")).is_true

    def test_lunts_orlov_true(self):
        assert is_dg_enhanced(_space("lunts_orlov")).is_true

    def test_dg_algebra_true(self):
        assert is_dg_enhanced(_space("dg_algebra")).is_true

    def test_derived_category_true(self):
        assert is_dg_enhanced(_space("derived_category")).is_true

    def test_db_coh_true(self):
        assert is_dg_enhanced(_space("db_coh")).is_true

    def test_bounded_derived_true(self):
        assert is_dg_enhanced(_space("bounded_derived")).is_true

    def test_chain_complexes_true(self):
        assert is_dg_enhanced(_space("chain_complexes")).is_true

    def test_derived_module_category_true(self):
        assert is_dg_enhanced(_space("derived_module_category")).is_true

    def test_stable_homotopy_category_false(self):
        assert is_dg_enhanced(_space("stable_homotopy_category")).is_false

    def test_topological_sh_false(self):
        assert is_dg_enhanced(_space("topological_sh")).is_false

    def test_no_dg_enhancement_false(self):
        assert is_dg_enhanced(_space("no_dg_enhancement")).is_false

    def test_not_algebraic_triangulated_false(self):
        assert is_dg_enhanced(_space("not_algebraic_triangulated")).is_false

    def test_unknown_empty(self):
        r = is_dg_enhanced(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert is_dg_enhanced(_space("dg_enhancement")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_dg_enhanced(_space("stable_homotopy_category")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert is_dg_enhanced(_space()).mode == "symbolic"

    def test_criterion_explicit_dg(self):
        r = is_dg_enhanced(_space("dg_enhancement"))
        assert r.metadata.get("criterion") == "explicit_dg_enhancement"

    def test_criterion_algebraic_dg(self):
        r = is_dg_enhanced(_space("derived_category"))
        assert r.metadata.get("criterion") == "algebraic_dg_enhancement"

    def test_criterion_no_dg(self):
        r = is_dg_enhanced(_space("stable_homotopy_category"))
        assert r.metadata.get("criterion") == "no_dg_enhancement"

    def test_stable_infinity_category_true(self):
        assert is_dg_enhanced(_space("stable_infinity_category")).is_true


# ---------------------------------------------------------------------------
# classify_derived_category
# ---------------------------------------------------------------------------

class TestClassifyDerivedCategory:
    def test_returns_dict(self):
        assert isinstance(classify_derived_category(_space()), dict)

    def test_required_keys(self):
        r = classify_derived_category(_space())
        assert {
            "derived_class", "is_triangulated", "has_t_structure",
            "has_semiorthogonal_decomposition", "is_dg_enhanced",
            "key_properties", "representation", "tags",
        } <= r.keys()

    def test_full_geometric_class(self):
        r = classify_derived_category(
            _space("semiorthogonal_decomposition", "dg_enhancement", "t_structure")
        )
        assert r["derived_class"] == "full_geometric"

    def test_algebraic_enhanced_class(self):
        r = classify_derived_category(_space("derived_category", "t_structure"))
        assert r["derived_class"] == "algebraic_enhanced"

    def test_perverse_t_class(self):
        r = classify_derived_category(_space("perverse_sheaves"))
        assert r["derived_class"] == "perverse_t"

    def test_triangulated_basic_class(self):
        r = classify_derived_category(_space("triangulated_category", "t_structure"))
        assert r["derived_class"] == "triangulated_basic"

    def test_general_class(self):
        r = classify_derived_category(_space("triangulated_category"))
        assert r["derived_class"] == "general"

    def test_triangulated_in_properties(self):
        r = classify_derived_category(_space("triangulated_category"))
        assert "triangulated" in r["key_properties"]

    def test_t_structure_in_properties(self):
        r = classify_derived_category(_space("t_structure"))
        assert "t_structure" in r["key_properties"]

    def test_no_t_structure_in_properties(self):
        r = classify_derived_category(_space("no_t_structure"))
        assert "no_t_structure" in r["key_properties"]

    def test_sod_in_properties(self):
        r = classify_derived_category(_space("exceptional_collection"))
        assert "semiorthogonal_decomposition" in r["key_properties"]

    def test_no_full_exceptional_in_properties(self):
        r = classify_derived_category(_space("k3_surface"))
        assert "no_full_exceptional_collection" in r["key_properties"]

    def test_dg_enhanced_in_properties(self):
        r = classify_derived_category(_space("dg_enhancement"))
        assert "dg_enhanced" in r["key_properties"]

    def test_not_dg_enhanceable_in_properties(self):
        r = classify_derived_category(_space("stable_homotopy_category"))
        assert "not_dg_enhanceable" in r["key_properties"]

    def test_perverse_sheaves_in_properties(self):
        r = classify_derived_category(_space("perverse_sheaves"))
        assert "perverse_sheaves" in r["key_properties"]

    def test_derived_functors_in_properties(self):
        r = classify_derived_category(_space("rhom"))
        assert "derived_functors" in r["key_properties"]

    def test_fourier_mukai_in_properties(self):
        r = classify_derived_category(_space("fourier_mukai"))
        assert "fourier_mukai_equivalence" in r["key_properties"]

    def test_exceptional_collection_in_properties(self):
        r = classify_derived_category(_space("exceptional_collection"))
        assert "exceptional_collection" in r["key_properties"]

    def test_tags_sorted(self):
        r = classify_derived_category(_space("db_coh", "t_structure"))
        assert r["tags"] == sorted(r["tags"])

    def test_representation_passthrough(self):
        r = classify_derived_category(_space("derived_category", rep="my_rep"))
        assert r["representation"] == "my_rep"

    def test_db_coh_full_geometric(self):
        r = classify_derived_category(
            _space("db_coh", "semiorthogonal_decomposition", "dg_enhancement", "t_structure")
        )
        assert r["derived_class"] == "full_geometric"


# ---------------------------------------------------------------------------
# derived_category_profile
# ---------------------------------------------------------------------------

class TestDerivedCategoryProfile:
    def test_returns_dict(self):
        assert isinstance(derived_category_profile(_space()), dict)

    def test_has_classification(self):
        assert "classification" in derived_category_profile(_space())

    def test_has_named_profiles(self):
        assert "named_profiles" in derived_category_profile(_space())

    def test_has_layer_summary(self):
        assert "layer_summary" in derived_category_profile(_space())

    def test_classification_is_dict(self):
        assert isinstance(derived_category_profile(_space())["classification"], dict)

    def test_named_profiles_is_tuple(self):
        assert isinstance(derived_category_profile(_space())["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        assert isinstance(derived_category_profile(_space())["layer_summary"], dict)

    def test_named_profiles_nonempty(self):
        assert len(derived_category_profile(_space())["named_profiles"]) >= 6


# ---------------------------------------------------------------------------
# DerivedCategoryProfile dataclass
# ---------------------------------------------------------------------------

class TestDerivedCategoryProfileDataclass:
    def test_frozen(self):
        p = DerivedCategoryProfile(
            key="t", display_name="T", category_type="derived_category",
            base_category="abelian",
            has_t_structure=True, is_enhanced=False, has_semiorthogonal_decomp=False,
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        with pytest.raises(Exception):
            p.key = "other"  # type: ignore[misc]

    def test_equality_by_value(self):
        kwargs = dict(
            key="t", display_name="T", category_type="derived_category",
            base_category="abelian",
            has_t_structure=True, is_enhanced=False, has_semiorthogonal_decomp=False,
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        assert DerivedCategoryProfile(**kwargs) == DerivedCategoryProfile(**kwargs)

    def test_all_fields_accessible(self):
        p = DerivedCategoryProfile(
            key="x", display_name="X", category_type="perverse",
            base_category="constructible_sheaves",
            has_t_structure=True, is_enhanced=False, has_semiorthogonal_decomp=False,
            presentation_layer="selected_block", focus="perverse", chapter_targets=("23", "36"),
        )
        assert p.has_t_structure is True
        assert p.category_type == "perverse"
        assert p.chapter_targets == ("23", "36")

    def test_inequality_on_different_keys(self):
        def _make(key: str) -> DerivedCategoryProfile:
            return DerivedCategoryProfile(
                key=key, display_name="T", category_type="derived_category",
                base_category="abelian",
                has_t_structure=True, is_enhanced=False, has_semiorthogonal_decomp=False,
                presentation_layer="main_text", focus="f", chapter_targets=("1",),
            )
        assert _make("a") != _make("b")
