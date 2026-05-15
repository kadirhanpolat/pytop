from pytop.metric_map_taxonomy import (
    classify_finite_metric_map,
    metric_map_profile,
    render_metric_map_taxonomy,
)
from pytop.metric_spaces import FiniteMetricSpace


def _line(points):
    return FiniteMetricSpace(carrier=tuple(points), distance=lambda x, y: abs(x - y))


def test_identity_map_is_certified_as_isometry_and_homeomorphism():
    line = _line((0, 1, 2))
    profile = classify_finite_metric_map(line, line, {0: 0, 1: 1, 2: 2}, name="id")

    assert profile.certification == "exact-finite"
    assert profile.lipschitz_constant == 1
    assert profile.similarity_ratio == 1
    assert profile.non_expansive is True
    assert profile.lipschitz is True
    assert profile.uniformly_continuous is True
    assert profile.continuous is True
    assert profile.isometry is True
    assert profile.similarity is True
    assert profile.bijective is True
    assert profile.homeomorphism is True


def test_similarity_can_fail_non_expansive_when_ratio_is_large():
    domain = _line((0, 1, 2))
    codomain = _line((0, 2, 4))

    profile = classify_finite_metric_map(domain, codomain, {0: 0, 1: 2, 2: 4}, name="double")

    assert profile.lipschitz_constant == 2
    assert profile.similarity_ratio == 2
    assert profile.similarity is True
    assert profile.isometry is False
    assert profile.non_expansive is False
    assert profile.homeomorphism is True


def test_constant_map_is_lipschitz_but_not_a_homeomorphism():
    domain = FiniteMetricSpace(carrier=("a", "b"), distance=lambda x, y: 0 if x == y else 1)
    codomain = FiniteMetricSpace(carrier=("p", "q"), distance=lambda x, y: 0 if x == y else 1)

    profile = classify_finite_metric_map(domain, codomain, {"a": "p", "b": "p"}, name="constant")

    assert profile.lipschitz_constant == 0
    assert profile.non_expansive is True
    assert profile.lipschitz is True
    assert profile.isometry is False
    assert profile.similarity is False
    assert profile.bijective is False
    assert profile.homeomorphism is False


def test_symbolic_profile_does_not_overclaim_unsupplied_labels():
    profile = metric_map_profile(name="symbolic", lipschitz=True, lipschitz_constant=3)

    assert profile.certification == "symbolic-profile"
    assert profile.lipschitz is True
    assert profile.continuous is None
    assert profile.uniformly_continuous is None
    assert profile.homeomorphism is None
    assert "continuous: unknown" in render_metric_map_taxonomy(profile)
