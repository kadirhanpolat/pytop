"""Tests for uniform_spaces.py."""

import pytest
from pytop.uniform_spaces import (
    entourage_system,
    is_cauchy_filter,
    is_uniform_space,
    is_uniformly_complete,
    is_uniformly_continuous,
)


# ---------------------------------------------------------------------------
# Helpers: lightweight space/mapping descriptors
# ---------------------------------------------------------------------------

def _space(**kwargs):
    return kwargs

def _space_with_tags(*tags):
    return {"tags": set(tags)}

def _space_with_entourages(entourages):
    return {"entourages": entourages}

def _space_with_explicit(key, value):
    return {key: value}

def _space_with_meta(**meta):
    return {"metadata": meta}


# ---------------------------------------------------------------------------
# is_uniform_space
# ---------------------------------------------------------------------------

class TestIsUniformSpace:
    def test_explicit_true_flag(self):
        assert is_uniform_space(_space_with_explicit("is_uniform_space", True))

    def test_explicit_false_flag(self):
        assert not is_uniform_space(_space_with_explicit("is_uniform_space", False))

    def test_entourages_list_present(self):
        assert is_uniform_space(_space_with_entourages(["e1", "e2"]))

    def test_empty_entourages_list_not_sufficient(self):
        assert not is_uniform_space(_space_with_entourages([]))

    def test_uniform_space_tag(self):
        assert is_uniform_space(_space_with_tags("uniform_space"))

    def test_metric_tag(self):
        assert is_uniform_space(_space_with_tags("metric"))

    def test_metrizable_tag(self):
        assert is_uniform_space(_space_with_tags("metrizable"))

    def test_discrete_uniformity_tag(self):
        assert is_uniform_space(_space_with_tags("discrete_uniformity"))

    def test_complete_metric_tag(self):
        assert is_uniform_space(_space_with_tags("complete_metric"))

    def test_no_tags_gives_false(self):
        assert not is_uniform_space(_space(**{}))

    def test_irrelevant_tag_gives_false(self):
        assert not is_uniform_space(_space_with_tags("connected"))

    def test_explicit_via_metadata(self):
        assert is_uniform_space(_space_with_meta(is_uniform_space=True))

    def test_explicit_false_via_metadata(self):
        assert not is_uniform_space(_space_with_meta(is_uniform_space=False))


# ---------------------------------------------------------------------------
# entourage_system
# ---------------------------------------------------------------------------

class TestEntourageSystem:
    def test_explicit_entourages_returned(self):
        e = ["e1", "e2"]
        result = entourage_system(_space_with_entourages(e))
        assert result == e

    def test_discrete_uniformity_tag(self):
        result = entourage_system(_space_with_tags("discrete_uniformity"))
        assert isinstance(result, list)
        assert len(result) > 0

    def test_metric_tag_returns_epsilon_entourages(self):
        result = entourage_system(_space_with_tags("metric"))
        assert "epsilon_ball_entourages" in result

    def test_metric_uniformity_tag(self):
        result = entourage_system(_space_with_tags("metric_uniformity"))
        assert "epsilon_ball_entourages" in result

    def test_complete_metric_tag(self):
        result = entourage_system(_space_with_tags("complete_metric"))
        assert "epsilon_ball_entourages" in result

    def test_uniform_space_tag_returns_symbolic(self):
        result = entourage_system(_space_with_tags("uniform_space"))
        assert "symbolic_entourage_basis" in result

    def test_no_uniformity_returns_none(self):
        result = entourage_system(_space(**{}))
        assert result is None

    def test_tuple_entourages_converted_to_list(self):
        space = {"entourages": ("e1", "e2")}
        result = entourage_system(space)
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# is_uniformly_continuous
# ---------------------------------------------------------------------------

class TestIsUniformlyContinuous:
    def test_explicit_true(self):
        assert is_uniformly_continuous({"is_uniformly_continuous": True})

    def test_explicit_false(self):
        assert not is_uniformly_continuous({"is_uniformly_continuous": False})

    def test_uniformly_continuous_tag(self):
        assert is_uniformly_continuous({"tags": {"uniformly_continuous"}})

    def test_not_uniformly_continuous_tag(self):
        assert not is_uniformly_continuous({"tags": {"not_uniformly_continuous"}})

    def test_lipschitz_constant_dict(self):
        assert is_uniformly_continuous({"lipschitz_constant": 2.0})

    def test_identity_map_type(self):
        assert is_uniformly_continuous({"map_type": "identity"})

    def test_constant_map_type(self):
        assert is_uniformly_continuous({"map_type": "constant"})

    def test_lipschitz_in_metadata(self):
        assert is_uniformly_continuous(_space_with_meta(lipschitz_constant=1.0))

    def test_identity_in_metadata(self):
        assert is_uniformly_continuous(_space_with_meta(map_type="identity"))

    def test_no_info_gives_false(self):
        assert not is_uniformly_continuous({})


# ---------------------------------------------------------------------------
# is_cauchy_filter
# ---------------------------------------------------------------------------

class TestIsCauchyFilter:
    def setup_method(self):
        self.uniform_space = _space_with_tags("metric")

    def test_explicit_true_flag(self):
        f = {"is_cauchy_filter": True}
        assert is_cauchy_filter(f, self.uniform_space)

    def test_explicit_false_flag(self):
        f = {"is_cauchy_filter": False}
        assert not is_cauchy_filter(f, self.uniform_space)

    def test_non_uniform_space_always_false(self):
        f = {"filter_type": "principal"}
        assert not is_cauchy_filter(f, {})  # no tags → not uniform

    def test_principal_filter_type_in_dict(self):
        f = {"filter_type": "principal"}
        assert is_cauchy_filter(f, self.uniform_space)

    def test_meets_every_entourage_flag(self):
        f = {"meets_every_entourage": True}
        assert is_cauchy_filter(f, self.uniform_space)

    def test_principal_filter_in_metadata(self):
        f = {"metadata": {"filter_type": "principal"}}
        assert is_cauchy_filter(f, self.uniform_space)

    def test_meets_entourage_in_metadata(self):
        f = {"metadata": {"meets_every_entourage": True}}
        assert is_cauchy_filter(f, self.uniform_space)

    def test_no_info_gives_false(self):
        assert not is_cauchy_filter({}, self.uniform_space)


# ---------------------------------------------------------------------------
# is_uniformly_complete
# ---------------------------------------------------------------------------

class TestIsUniformlyComplete:
    def test_explicit_true(self):
        assert is_uniformly_complete({"is_uniformly_complete": True})

    def test_explicit_false(self):
        assert not is_uniformly_complete({"is_uniformly_complete": False})

    def test_non_uniform_space_gives_false(self):
        assert not is_uniformly_complete({})  # no uniform tags

    def test_complete_metric_tag(self):
        assert is_uniformly_complete(_space_with_tags("complete_metric"))

    def test_discrete_uniformity_tag(self):
        assert is_uniformly_complete(_space_with_tags("discrete_uniformity"))

    def test_finite_uniform_space_tag(self):
        # finite_uniform_space is in COMPLETE tags but not UNIFORM_TRUE_TAGS,
        # so the space must also carry a uniform-space recognition tag
        sp = {"tags": {"finite_uniform_space", "uniform_space"}}
        assert is_uniformly_complete(sp)

    def test_metric_space_type_in_dict(self):
        sp = {"tags": {"metric"}, "space_type": "Metric Uniformity"}
        assert is_uniformly_complete(sp)

    def test_discrete_space_type_in_dict(self):
        sp = {"tags": {"metric"}, "space_type": "Discrete Uniformity"}
        assert is_uniformly_complete(sp)

    def test_metric_space_type_in_metadata(self):
        sp = {"tags": {"metric"}, "metadata": {"space_type": "Metric Uniformity"}}
        assert is_uniformly_complete(sp)

    def test_discrete_space_type_in_metadata(self):
        sp = {"tags": {"metric"}, "metadata": {"space_type": "Discrete Uniformity"}}
        assert is_uniformly_complete(sp)

    def test_uniform_space_without_completion_tags_false(self):
        # Has uniform_space tag (so is recognized as uniform space) but no completion evidence
        sp = {"tags": {"uniform_space"}}
        assert not is_uniformly_complete(sp)
