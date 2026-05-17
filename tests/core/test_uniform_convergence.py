"""Tests for pytop.uniform_convergence."""

from __future__ import annotations

import pytest

from pytop.uniform_convergence import (
    ARZELA_ASCOLI_TAGS,
    COMPACT_OPEN_TAGS,
    DINI_THEOREM_TAGS,
    EQUICONTINUOUS_TAGS,
    NOT_EQUICONTINUOUS_TAGS,
    NOT_RELATIVELY_COMPACT_TAGS,
    POINTWISE_ONLY_TAGS,
    STONE_WEIERSTRASS_TAGS,
    UNIFORM_CONVERGENCE_TAGS,
    UniformConvergenceProfile,
    classify_uniform_convergence,
    get_named_uniform_convergence_profiles,
    is_equicontinuous,
    is_uniformly_convergent,
    satisfies_arzela_ascoli,
    satisfies_dini,
    uniform_convergence_chapter_index,
    uniform_convergence_layer_summary,
    uniform_convergence_profile,
    uniform_convergence_type_index,
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
    def test_uniform_tags_nonempty(self):
        assert len(UNIFORM_CONVERGENCE_TAGS) >= 4

    def test_pointwise_tags_nonempty(self):
        assert len(POINTWISE_ONLY_TAGS) >= 3

    def test_equicontinuous_tags_nonempty(self):
        assert len(EQUICONTINUOUS_TAGS) >= 4

    def test_not_equicontinuous_tags_nonempty(self):
        assert len(NOT_EQUICONTINUOUS_TAGS) >= 3

    def test_arzela_ascoli_tags_nonempty(self):
        assert len(ARZELA_ASCOLI_TAGS) >= 3

    def test_dini_tags_nonempty(self):
        assert len(DINI_THEOREM_TAGS) >= 2

    def test_stone_weierstrass_tags_nonempty(self):
        assert len(STONE_WEIERSTRASS_TAGS) >= 3

    def test_compact_open_tags_nonempty(self):
        assert len(COMPACT_OPEN_TAGS) >= 3

    def test_not_relatively_compact_tags_nonempty(self):
        assert len(NOT_RELATIVELY_COMPACT_TAGS) >= 3

    def test_uniform_convergence_in_uniform_tags(self):
        assert "uniform_convergence" in UNIFORM_CONVERGENCE_TAGS

    def test_pointwise_not_uniform_in_pointwise_tags(self):
        assert "pointwise_not_uniform" in POINTWISE_ONLY_TAGS

    def test_equicontinuous_in_equicontinuous_tags(self):
        assert "equicontinuous" in EQUICONTINUOUS_TAGS

    def test_lipschitz_family_in_equicontinuous_tags(self):
        assert "lipschitz_family" in EQUICONTINUOUS_TAGS

    def test_dini_theorem_in_dini_tags(self):
        assert "dini_theorem" in DINI_THEOREM_TAGS

    def test_arzela_ascoli_in_arzela_tags(self):
        assert "arzela_ascoli" in ARZELA_ASCOLI_TAGS

    def test_not_equicontinuous_in_not_equi_tags(self):
        assert "not_equicontinuous" in NOT_EQUICONTINUOUS_TAGS

    def test_power_function_in_pointwise_tags(self):
        assert "power_function_sequence" in POINTWISE_ONLY_TAGS

    def test_stone_weierstrass_in_sw_tags(self):
        assert "stone_weierstrass" in STONE_WEIERSTRASS_TAGS

    def test_compact_open_in_compact_open_tags(self):
        assert "compact_open_topology" in COMPACT_OPEN_TAGS

    def test_all_tag_sets_contain_strings(self):
        for tag_set in [
            UNIFORM_CONVERGENCE_TAGS, POINTWISE_ONLY_TAGS, EQUICONTINUOUS_TAGS,
            NOT_EQUICONTINUOUS_TAGS, ARZELA_ASCOLI_TAGS, DINI_THEOREM_TAGS,
            STONE_WEIERSTRASS_TAGS, COMPACT_OPEN_TAGS, NOT_RELATIVELY_COMPACT_TAGS,
        ]:
            assert all(isinstance(t, str) for t in tag_set)

    def test_uniform_and_pointwise_disjoint(self):
        assert UNIFORM_CONVERGENCE_TAGS.isdisjoint(POINTWISE_ONLY_TAGS)

    def test_equicontinuous_and_not_equicontinuous_disjoint(self):
        assert EQUICONTINUOUS_TAGS.isdisjoint(NOT_EQUICONTINUOUS_TAGS)


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_uniform_convergence_profiles(), tuple)

    def test_at_least_six_profiles(self):
        assert len(get_named_uniform_convergence_profiles()) >= 6

    def test_all_uniform_convergence_profile_instances(self):
        for p in get_named_uniform_convergence_profiles():
            assert isinstance(p, UniformConvergenceProfile)

    def test_keys_unique(self):
        keys = [p.key for p in get_named_uniform_convergence_profiles()]
        assert len(keys) == len(set(keys))

    def test_display_names_nonempty(self):
        for p in get_named_uniform_convergence_profiles():
            assert p.display_name.strip()

    def test_focus_nonempty(self):
        for p in get_named_uniform_convergence_profiles():
            assert p.focus.strip()

    def test_chapter_targets_nonempty(self):
        for p in get_named_uniform_convergence_profiles():
            assert len(p.chapter_targets) >= 1

    def test_presentation_layers_known(self):
        known = {"main_text", "selected_block", "appendix"}
        for p in get_named_uniform_convergence_profiles():
            assert p.presentation_layer in known

    def test_convergence_types_are_strings(self):
        for p in get_named_uniform_convergence_profiles():
            assert isinstance(p.convergence_type, str)

    # power_sequence_on_interval
    def test_power_sequence_present(self):
        keys = {p.key for p in get_named_uniform_convergence_profiles()}
        assert "power_sequence_on_interval" in keys

    def test_power_sequence_not_uniform(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "power_sequence_on_interval")
        assert p.is_uniform is False

    def test_power_sequence_not_equicontinuous(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "power_sequence_on_interval")
        assert p.is_equicontinuous is False

    def test_power_sequence_limit_discontinuous(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "power_sequence_on_interval")
        assert p.limit_is_continuous is False

    def test_power_sequence_not_relatively_compact(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "power_sequence_on_interval")
        assert p.is_relatively_compact is False

    def test_power_sequence_dini_fails(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "power_sequence_on_interval")
        assert p.satisfies_dini is False

    # geometric_series_uniform
    def test_geometric_series_present(self):
        keys = {p.key for p in get_named_uniform_convergence_profiles()}
        assert "geometric_series_uniform" in keys

    def test_geometric_series_uniform(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "geometric_series_uniform")
        assert p.is_uniform is True

    def test_geometric_series_equicontinuous(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "geometric_series_uniform")
        assert p.is_equicontinuous is True

    def test_geometric_series_continuous_limit(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "geometric_series_uniform")
        assert p.limit_is_continuous is True

    def test_geometric_series_relatively_compact(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "geometric_series_uniform")
        assert p.is_relatively_compact is True

    def test_geometric_series_dini(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "geometric_series_uniform")
        assert p.satisfies_dini is True

    # dini_theorem_monotone
    def test_dini_profile_present(self):
        keys = {p.key for p in get_named_uniform_convergence_profiles()}
        assert "dini_theorem_monotone" in keys

    def test_dini_profile_uniform(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "dini_theorem_monotone")
        assert p.is_uniform is True

    def test_dini_profile_satisfies_dini(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "dini_theorem_monotone")
        assert p.satisfies_dini is True

    def test_dini_profile_continuous_limit(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "dini_theorem_monotone")
        assert p.limit_is_continuous is True

    # arzela_ascoli_c_of_compact
    def test_ascoli_profile_present(self):
        keys = {p.key for p in get_named_uniform_convergence_profiles()}
        assert "arzela_ascoli_c_of_compact" in keys

    def test_ascoli_profile_uniform(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "arzela_ascoli_c_of_compact")
        assert p.is_uniform is True

    def test_ascoli_profile_equicontinuous(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "arzela_ascoli_c_of_compact")
        assert p.is_equicontinuous is True

    def test_ascoli_profile_relatively_compact(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "arzela_ascoli_c_of_compact")
        assert p.is_relatively_compact is True

    def test_ascoli_profile_dini_false(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "arzela_ascoli_c_of_compact")
        assert p.satisfies_dini is False

    # stone_weierstrass
    def test_stone_weierstrass_present(self):
        keys = {p.key for p in get_named_uniform_convergence_profiles()}
        assert "stone_weierstrass" in keys

    def test_sw_profile_uniform(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "stone_weierstrass")
        assert p.is_uniform is True

    def test_sw_profile_not_equicontinuous(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "stone_weierstrass")
        assert p.is_equicontinuous is False

    # compact_open_topology_cx
    def test_compact_open_present(self):
        keys = {p.key for p in get_named_uniform_convergence_profiles()}
        assert "compact_open_topology_cx" in keys

    def test_compact_open_not_uniform(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "compact_open_topology_cx")
        assert p.is_uniform is False

    def test_compact_open_continuous_limit(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "compact_open_topology_cx")
        assert p.limit_is_continuous is True

    # lipschitz_equicontinuous_family
    def test_lipschitz_present(self):
        keys = {p.key for p in get_named_uniform_convergence_profiles()}
        assert "lipschitz_equicontinuous_family" in keys

    def test_lipschitz_equicontinuous(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "lipschitz_equicontinuous_family")
        assert p.is_equicontinuous is True

    def test_lipschitz_relatively_compact(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "lipschitz_equicontinuous_family")
        assert p.is_relatively_compact is True

    def test_lipschitz_continuous_limit(self):
        p = next(p for p in get_named_uniform_convergence_profiles()
                 if p.key == "lipschitz_equicontinuous_family")
        assert p.limit_is_continuous is True


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_is_dict(self):
        assert isinstance(uniform_convergence_layer_summary(), dict)

    def test_layer_summary_has_main_text(self):
        assert "main_text" in uniform_convergence_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in uniform_convergence_layer_summary()

    def test_layer_summary_total(self):
        profiles = get_named_uniform_convergence_profiles()
        assert sum(uniform_convergence_layer_summary().values()) == len(profiles)

    def test_chapter_index_is_dict(self):
        assert isinstance(uniform_convergence_chapter_index(), dict)

    def test_chapter_index_sorted(self):
        ch = uniform_convergence_chapter_index()
        assert list(ch.keys()) == sorted(ch.keys())

    def test_chapter_index_values_tuples(self):
        for v in uniform_convergence_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_nonempty_values(self):
        for v in uniform_convergence_chapter_index().values():
            assert len(v) >= 1

    def test_type_index_is_dict(self):
        assert isinstance(uniform_convergence_type_index(), dict)

    def test_type_index_has_uniform(self):
        assert "uniform" in uniform_convergence_type_index()

    def test_type_index_has_pointwise_only(self):
        assert "pointwise_only" in uniform_convergence_type_index()

    def test_type_index_values_tuples(self):
        for v in uniform_convergence_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_total(self):
        total = sum(len(v) for v in uniform_convergence_type_index().values())
        assert total == len(get_named_uniform_convergence_profiles())


# ---------------------------------------------------------------------------
# is_uniformly_convergent
# ---------------------------------------------------------------------------

class TestIsUniformlyConvergent:
    def test_uniform_convergence_tag_true(self):
        assert is_uniformly_convergent(_space("uniform_convergence")).is_true

    def test_sup_norm_convergence_true(self):
        assert is_uniformly_convergent(_space("sup_norm_convergence")).is_true

    def test_uniform_limit_true(self):
        assert is_uniformly_convergent(_space("uniform_limit")).is_true

    def test_uniform_cauchy_true(self):
        assert is_uniformly_convergent(_space("uniform_cauchy")).is_true

    def test_uniform_approximation_true(self):
        assert is_uniformly_convergent(_space("uniform_approximation")).is_true

    def test_dini_theorem_implies_uniform(self):
        assert is_uniformly_convergent(_space("dini_theorem")).is_true

    def test_dini_monotone_implies_uniform(self):
        assert is_uniformly_convergent(_space("monotone_convergence_compact")).is_true

    def test_arzela_ascoli_implies_uniform(self):
        assert is_uniformly_convergent(_space("arzela_ascoli")).is_true

    def test_uniformly_bounded_equicontinuous_true(self):
        assert is_uniformly_convergent(_space("uniformly_bounded_equicontinuous")).is_true

    def test_pointwise_only_false(self):
        assert is_uniformly_convergent(_space("pointwise_only")).is_false

    def test_not_uniform_false(self):
        assert is_uniformly_convergent(_space("not_uniform")).is_false

    def test_power_function_sequence_false(self):
        assert is_uniformly_convergent(_space("power_function_sequence")).is_false

    def test_discontinuous_pointwise_limit_false(self):
        assert is_uniformly_convergent(_space("discontinuous_pointwise_limit")).is_false

    def test_pointwise_not_uniform_false(self):
        assert is_uniformly_convergent(_space("pointwise_not_uniform")).is_false

    def test_unknown_empty(self):
        r = is_uniformly_convergent(_space())
        assert not r.is_true and not r.is_false

    def test_mode_theorem_true(self):
        assert is_uniformly_convergent(_space("uniform_convergence")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_uniformly_convergent(_space("pointwise_only")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert is_uniformly_convergent(_space()).mode == "symbolic"

    def test_criterion_explicit_uniform(self):
        r = is_uniformly_convergent(_space("uniform_convergence"))
        assert r.metadata.get("criterion") == "explicit_uniform"

    def test_criterion_dini(self):
        r = is_uniformly_convergent(_space("dini_theorem"))
        assert r.metadata.get("criterion") == "dini_theorem"

    def test_criterion_arzela_ascoli(self):
        r = is_uniformly_convergent(_space("arzela_ascoli"))
        assert r.metadata.get("criterion") == "arzela_ascoli"

    def test_criterion_pointwise_only(self):
        r = is_uniformly_convergent(_space("pointwise_only"))
        assert r.metadata.get("criterion") == "pointwise_only"

    def test_result_has_justification(self):
        r = is_uniformly_convergent(_space("uniform_convergence"))
        assert r.justification

    def test_uniformly_convergent_sequence_tag_true(self):
        assert is_uniformly_convergent(_space("uniformly_convergent_sequence")).is_true


# ---------------------------------------------------------------------------
# is_equicontinuous
# ---------------------------------------------------------------------------

class TestIsEquicontinuous:
    def test_equicontinuous_tag_true(self):
        assert is_equicontinuous(_space("equicontinuous")).is_true

    def test_equicontinuous_family_true(self):
        assert is_equicontinuous(_space("equicontinuous_family")).is_true

    def test_lipschitz_family_true(self):
        assert is_equicontinuous(_space("lipschitz_family")).is_true

    def test_holder_family_true(self):
        assert is_equicontinuous(_space("holder_family")).is_true

    def test_bounded_derivative_family_true(self):
        assert is_equicontinuous(_space("bounded_derivative_family")).is_true

    def test_uniform_modulus_of_continuity_true(self):
        assert is_equicontinuous(_space("uniform_modulus_of_continuity")).is_true

    def test_uniformly_equicontinuous_true(self):
        assert is_equicontinuous(_space("uniformly_equicontinuous")).is_true

    def test_not_equicontinuous_tag_false(self):
        assert is_equicontinuous(_space("not_equicontinuous")).is_false

    def test_no_uniform_modulus_false(self):
        assert is_equicontinuous(_space("no_uniform_modulus")).is_false

    def test_power_function_sequence_false(self):
        assert is_equicontinuous(_space("power_function_sequence")).is_false

    def test_pointwise_only_false(self):
        assert is_equicontinuous(_space("pointwise_only")).is_false

    def test_unbounded_family_false(self):
        assert is_equicontinuous(_space("unbounded_family")).is_false

    def test_unknown_empty(self):
        r = is_equicontinuous(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit_equicontinuous(self):
        r = is_equicontinuous(_space("equicontinuous"))
        assert r.metadata.get("criterion") == "explicit_equicontinuous"

    def test_criterion_not_equicontinuous(self):
        r = is_equicontinuous(_space("not_equicontinuous"))
        assert r.metadata.get("criterion") == "not_equicontinuous"

    def test_justification_contains_lipschitz(self):
        r = is_equicontinuous(_space("lipschitz_family"))
        assert any("lipschitz" in j.lower() or "modulus" in j.lower() for j in r.justification)

    def test_mode_theorem_true(self):
        assert is_equicontinuous(_space("equicontinuous")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert is_equicontinuous(_space("not_equicontinuous")).mode == "theorem"


# ---------------------------------------------------------------------------
# satisfies_arzela_ascoli
# ---------------------------------------------------------------------------

class TestSatisfiesArzelaAscoli:
    def test_arzela_ascoli_tag_true(self):
        assert satisfies_arzela_ascoli(_space("arzela_ascoli")).is_true

    def test_relatively_compact_function_space_true(self):
        assert satisfies_arzela_ascoli(_space("relatively_compact_function_space")).is_true

    def test_compact_in_c_of_x_true(self):
        assert satisfies_arzela_ascoli(_space("compact_in_c_of_x")).is_true

    def test_uniformly_bounded_equicontinuous_true(self):
        assert satisfies_arzela_ascoli(_space("uniformly_bounded_equicontinuous")).is_true

    def test_ascoli_condition_true(self):
        assert satisfies_arzela_ascoli(_space("ascoli_condition")).is_true

    def test_equi_and_bounded_true(self):
        assert satisfies_arzela_ascoli(
            _space("equicontinuous", "uniformly_bounded")
        ).is_true

    def test_lipschitz_and_bounded_true(self):
        assert satisfies_arzela_ascoli(
            _space("lipschitz_family", "bounded_family")
        ).is_true

    def test_holder_and_bounded_true(self):
        assert satisfies_arzela_ascoli(
            _space("holder_family", "bounded_derivative_family")
        ).is_true

    def test_not_equicontinuous_false(self):
        assert satisfies_arzela_ascoli(_space("not_equicontinuous")).is_false

    def test_not_relatively_compact_false(self):
        assert satisfies_arzela_ascoli(_space("not_relatively_compact")).is_false

    def test_unbounded_family_false(self):
        assert satisfies_arzela_ascoli(_space("unbounded_family")).is_false

    def test_no_convergent_subsequence_false(self):
        assert satisfies_arzela_ascoli(_space("no_convergent_subsequence")).is_false

    def test_non_compact_function_family_false(self):
        assert satisfies_arzela_ascoli(_space("non_compact_function_family")).is_false

    def test_unknown_empty(self):
        r = satisfies_arzela_ascoli(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit(self):
        r = satisfies_arzela_ascoli(_space("arzela_ascoli"))
        assert r.metadata.get("criterion") == "explicit_arzela_ascoli"

    def test_criterion_equi_and_bounded(self):
        r = satisfies_arzela_ascoli(_space("equicontinuous", "uniformly_bounded"))
        assert r.metadata.get("criterion") == "equicontinuous_and_bounded"

    def test_criterion_not_arzela(self):
        r = satisfies_arzela_ascoli(_space("not_equicontinuous"))
        assert r.metadata.get("criterion") == "not_arzela_ascoli"

    def test_power_function_false(self):
        # power_function_sequence is in NOT_EQUICONTINUOUS_TAGS -> not_relatively_compact path
        r = satisfies_arzela_ascoli(_space("not_equicontinuous"))
        assert r.is_false

    def test_equicontinuous_alone_unknown(self):
        r = satisfies_arzela_ascoli(_space("equicontinuous"))
        # equicontinuous alone without bounded tag -> unknown
        assert not r.is_true and not r.is_false


# ---------------------------------------------------------------------------
# satisfies_dini
# ---------------------------------------------------------------------------

class TestSatisfiesDini:
    def test_dini_theorem_tag_true(self):
        assert satisfies_dini(_space("dini_theorem")).is_true

    def test_monotone_convergence_compact_true(self):
        assert satisfies_dini(_space("monotone_convergence_compact")).is_true

    def test_dini_condition_true(self):
        assert satisfies_dini(_space("dini_condition")).is_true

    def test_monotone_pointwise_uniform_true(self):
        assert satisfies_dini(_space("monotone_pointwise_uniform")).is_true

    def test_discontinuous_limit_false(self):
        assert satisfies_dini(_space("discontinuous_pointwise_limit")).is_false

    def test_non_compact_domain_false(self):
        assert satisfies_dini(_space("non_compact_domain")).is_false

    def test_not_monotone_false(self):
        assert satisfies_dini(_space("not_monotone_convergence")).is_false

    def test_power_function_false(self):
        assert satisfies_dini(_space("power_function_sequence")).is_false

    def test_pointwise_not_uniform_false(self):
        assert satisfies_dini(_space("pointwise_not_uniform")).is_false

    def test_unknown_empty(self):
        r = satisfies_dini(_space())
        assert not r.is_true and not r.is_false

    def test_criterion_explicit_dini(self):
        r = satisfies_dini(_space("dini_theorem"))
        assert r.metadata.get("criterion") == "explicit_dini"

    def test_criterion_dini_fails(self):
        r = satisfies_dini(_space("discontinuous_pointwise_limit"))
        assert r.metadata.get("criterion") == "dini_fails"

    def test_mode_theorem_true(self):
        assert satisfies_dini(_space("dini_theorem")).mode == "theorem"

    def test_mode_theorem_false(self):
        assert satisfies_dini(_space("non_compact_domain")).mode == "theorem"

    def test_mode_symbolic_unknown(self):
        assert satisfies_dini(_space()).mode == "symbolic"


# ---------------------------------------------------------------------------
# classify_uniform_convergence
# ---------------------------------------------------------------------------

class TestClassifyUniformConvergence:
    def test_returns_dict(self):
        assert isinstance(classify_uniform_convergence(_space()), dict)

    def test_required_keys(self):
        r = classify_uniform_convergence(_space())
        assert {
            "convergence_class", "is_uniformly_convergent", "is_equicontinuous",
            "satisfies_arzela_ascoli", "satisfies_dini", "key_properties",
            "representation", "tags",
        } <= r.keys()

    def test_dini_class(self):
        r = classify_uniform_convergence(_space("dini_theorem"))
        assert r["convergence_class"] == "dini"

    def test_arzela_ascoli_class(self):
        r = classify_uniform_convergence(_space("arzela_ascoli", "uniform_convergence"))
        assert r["convergence_class"] == "arzela_ascoli"

    def test_uniform_class(self):
        r = classify_uniform_convergence(_space("uniform_convergence"))
        assert r["convergence_class"] == "uniform"

    def test_pointwise_only_class(self):
        r = classify_uniform_convergence(_space("pointwise_only"))
        assert r["convergence_class"] == "pointwise_only"

    def test_equicontinuous_only_class(self):
        r = classify_uniform_convergence(_space("equicontinuous", "pointwise_only"))
        assert r["convergence_class"] == "equicontinuous_only"

    def test_uniform_in_properties(self):
        r = classify_uniform_convergence(_space("uniform_convergence"))
        assert "uniform_convergence" in r["key_properties"]

    def test_not_uniform_in_properties(self):
        r = classify_uniform_convergence(_space("pointwise_only"))
        assert "not_uniform" in r["key_properties"]

    def test_equicontinuous_in_properties(self):
        r = classify_uniform_convergence(_space("equicontinuous"))
        assert "equicontinuous" in r["key_properties"]

    def test_relatively_compact_in_properties(self):
        r = classify_uniform_convergence(_space("arzela_ascoli"))
        assert "relatively_compact" in r["key_properties"]

    def test_dini_applicable_in_properties(self):
        r = classify_uniform_convergence(_space("dini_theorem"))
        assert "dini_applicable" in r["key_properties"]

    def test_stone_weierstrass_in_properties(self):
        r = classify_uniform_convergence(_space("stone_weierstrass"))
        assert "stone_weierstrass" in r["key_properties"]

    def test_compact_open_in_properties(self):
        r = classify_uniform_convergence(_space("compact_open_topology"))
        assert "compact_open_topology" in r["key_properties"]

    def test_tags_sorted(self):
        r = classify_uniform_convergence(_space("equicontinuous", "uniform_convergence"))
        assert r["tags"] == sorted(r["tags"])

    def test_representation_passthrough(self):
        r = classify_uniform_convergence(_space("uniform_convergence", rep="my_rep"))
        assert r["representation"] == "my_rep"

    def test_not_equicontinuous_in_properties(self):
        r = classify_uniform_convergence(_space("not_equicontinuous"))
        assert "not_equicontinuous" in r["key_properties"]


# ---------------------------------------------------------------------------
# uniform_convergence_profile
# ---------------------------------------------------------------------------

class TestUniformConvergenceProfile:
    def test_returns_dict(self):
        assert isinstance(uniform_convergence_profile(_space()), dict)

    def test_has_classification(self):
        assert "classification" in uniform_convergence_profile(_space())

    def test_has_named_profiles(self):
        assert "named_profiles" in uniform_convergence_profile(_space())

    def test_has_layer_summary(self):
        assert "layer_summary" in uniform_convergence_profile(_space())

    def test_classification_is_dict(self):
        assert isinstance(uniform_convergence_profile(_space())["classification"], dict)

    def test_named_profiles_is_tuple(self):
        assert isinstance(uniform_convergence_profile(_space())["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        assert isinstance(uniform_convergence_profile(_space())["layer_summary"], dict)

    def test_named_profiles_nonempty(self):
        assert len(uniform_convergence_profile(_space())["named_profiles"]) >= 6


# ---------------------------------------------------------------------------
# UniformConvergenceProfile dataclass
# ---------------------------------------------------------------------------

class TestUniformConvergenceProfileDataclass:
    def test_frozen(self):
        p = UniformConvergenceProfile(
            key="t", display_name="T", convergence_type="uniform",
            is_uniform=True, is_equicontinuous=True, limit_is_continuous=True,
            is_relatively_compact=True, satisfies_dini=False,
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        with pytest.raises(Exception):
            p.key = "other"  # type: ignore[misc]

    def test_equality_by_value(self):
        kwargs = dict(
            key="t", display_name="T", convergence_type="uniform",
            is_uniform=True, is_equicontinuous=True, limit_is_continuous=True,
            is_relatively_compact=True, satisfies_dini=False,
            presentation_layer="main_text", focus="f", chapter_targets=("1",),
        )
        assert UniformConvergenceProfile(**kwargs) == UniformConvergenceProfile(**kwargs)

    def test_all_fields_accessible(self):
        p = UniformConvergenceProfile(
            key="x", display_name="X", convergence_type="pointwise_only",
            is_uniform=False, is_equicontinuous=False, limit_is_continuous=False,
            is_relatively_compact=False, satisfies_dini=False,
            presentation_layer="main_text", focus="power series", chapter_targets=("1", "2"),
        )
        assert p.convergence_type == "pointwise_only"
        assert p.is_uniform is False
        assert p.chapter_targets == ("1", "2")
