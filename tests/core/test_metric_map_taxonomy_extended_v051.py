"""Coverage-targeted tests for metric_map_taxonomy.py (v0.5.1)."""
import pytest
from pytop.metric_map_taxonomy import (
    MetricMapProfile,
    MetricMapping,
    classify_finite_metric_map,
    metric_map_profile,
    render_metric_map_taxonomy,
    _finite_carrier,
    _require_valid_metric,
    _normalize_graph,
    _finite_similarity_ratio,
)
from pytop.metric_spaces import FiniteMetricSpace


# ---------------------------------------------------------------------------
# Helpers — simple finite metric spaces
# ---------------------------------------------------------------------------

def _discrete_metric(points):
    """Discrete metric: d(x,y) = 0 if x==y, 1 otherwise."""
    d = {}
    for x in points:
        for y in points:
            d[(x, y)] = 0.0 if x == y else 1.0
    return d


def _two_point():
    pts = [1, 2]
    return FiniteMetricSpace(carrier=pts, distance=_discrete_metric(pts))


def _one_point():
    pts = [1]
    return FiniteMetricSpace(carrier=pts, distance=_discrete_metric(pts))


def _three_point():
    pts = [1, 2, 3]
    return FiniteMetricSpace(carrier=pts, distance=_discrete_metric(pts))


# ---------------------------------------------------------------------------
# render_metric_map_taxonomy — unknown label (line 154) and similarity_ratio (164)
# ---------------------------------------------------------------------------

def test_render_with_none_values_hits_unknown_label():
    profile = MetricMapProfile(name="f", non_expansive=None, lipschitz=None)
    text = render_metric_map_taxonomy(profile)
    assert "unknown" in text
    assert "f" in text


def test_render_with_similarity_ratio():
    profile = MetricMapProfile(
        name="g",
        similarity_ratio=2.0,
        lipschitz_constant=2.0,
        non_expansive=False,
        lipschitz=True,
    )
    text = render_metric_map_taxonomy(profile)
    assert "similarity_ratio" in text
    assert "2" in text


def test_render_with_notes():
    profile = MetricMapProfile(name="h", notes=("note1",))
    text = render_metric_map_taxonomy(profile)
    assert "note1" in text


# ---------------------------------------------------------------------------
# _finite_carrier — TypeError path (lines 176-177)
# ---------------------------------------------------------------------------

def test_finite_carrier_none_carrier_raises():
    class NullCarrier:
        carrier = None
    with pytest.raises(ValueError, match="explicit finite carrier"):
        _finite_carrier(NullCarrier(), "domain")


def test_finite_carrier_valid():
    space = _two_point()
    pts = _finite_carrier(space, "domain")
    assert set(pts) == {1, 2}


# ---------------------------------------------------------------------------
# _require_valid_metric — is_false path (line 186) and is_unknown (188)
# ---------------------------------------------------------------------------

def test_require_valid_metric_unknown_raises():
    # SymbolicMetricSpace has no explicit finite carrier → validate_metric returns unknown
    from pytop.metric_spaces import SymbolicMetricSpace
    space = SymbolicMetricSpace(carrier="R", tags={"metric"})
    with pytest.raises(ValueError, match="not explicitly finite"):
        _require_valid_metric(space, "domain", 1e-12)


def test_require_valid_metric_false_raises():
    # Create a metric space that fails validation (negative distance)
    bad_d = {(1, 1): 0.0, (1, 2): -1.0, (2, 1): -1.0, (2, 2): 0.0}
    space = FiniteMetricSpace(carrier=[1, 2], distance=bad_d)
    with pytest.raises(ValueError, match="failed finite metric validation"):
        _require_valid_metric(space, "domain", 1e-12)


# ---------------------------------------------------------------------------
# _normalize_graph — callable mapping (line 197)
# ---------------------------------------------------------------------------

def test_normalize_graph_callable():
    pts = (1, 2)
    codomain_pts = (1, 2)
    graph = _normalize_graph(pts, codomain_pts, lambda x: x)
    assert graph == {1: 1, 2: 2}


def test_normalize_graph_dict():
    pts = (1, 2)
    codomain_pts = (1, 2)
    graph = _normalize_graph(pts, codomain_pts, {1: 2, 2: 1})
    assert graph == {1: 2, 2: 1}


def test_normalize_graph_missing_domain_point_raises():
    pts = (1, 2)
    codomain_pts = (1, 2)
    with pytest.raises(ValueError, match="exactly one image"):
        _normalize_graph(pts, codomain_pts, {1: 1})  # missing 2


def test_normalize_graph_image_outside_codomain_raises():
    pts = (1, 2)
    codomain_pts = (1, 2)
    with pytest.raises(ValueError, match="belong to the codomain"):
        _normalize_graph(pts, codomain_pts, {1: 1, 2: 99})  # 99 not in codomain


# ---------------------------------------------------------------------------
# _finite_similarity_ratio — single point → return 1.0 (line 256)
# ---------------------------------------------------------------------------

def test_finite_similarity_ratio_single_point():
    space = _one_point()
    graph = {1: 1}
    result = _finite_similarity_ratio(space, space, graph, (1,), 1e-12)
    assert result == 1.0


def test_finite_similarity_ratio_isometry():
    space = _two_point()
    graph = {1: 1, 2: 2}
    result = _finite_similarity_ratio(space, space, graph, (1, 2), 1e-12)
    assert result is not None
    assert abs(result - 1.0) < 1e-9


def test_finite_similarity_ratio_inconsistent_returns_none():
    # Two different codomain spaces with different scales → inconsistent ratios
    d_domain = {(1, 1): 0.0, (1, 2): 1.0, (2, 1): 1.0, (2, 2): 0.0,
                (1, 3): 2.0, (3, 1): 2.0, (2, 3): 1.0, (3, 2): 1.0,
                (3, 3): 0.0}
    d_codomain = {(1, 1): 0.0, (1, 2): 1.0, (2, 1): 1.0, (2, 2): 0.0,
                  (1, 3): 3.0, (3, 1): 3.0, (2, 3): 2.0, (3, 2): 2.0,
                  (3, 3): 0.0}
    dom = FiniteMetricSpace(carrier=[1, 2, 3], distance=d_domain)
    cod = FiniteMetricSpace(carrier=[1, 2, 3], distance=d_codomain)
    graph = {1: 1, 2: 2, 3: 3}
    result = _finite_similarity_ratio(dom, cod, graph, (1, 2, 3), 1e-12)
    assert result is None


# ---------------------------------------------------------------------------
# classify_finite_metric_map — full integration
# ---------------------------------------------------------------------------

def test_classify_identity_map():
    space = _two_point()
    profile = classify_finite_metric_map(space, space, {1: 1, 2: 2})
    assert profile.isometry is True
    assert profile.bijective is True
    assert profile.homeomorphism is True
    assert profile.certification == "exact-finite"


def test_classify_with_callable_mapping():
    space = _two_point()
    profile = classify_finite_metric_map(space, space, lambda x: x)
    assert profile.bijective is True


def test_classify_non_bijective():
    space = _two_point()
    profile = classify_finite_metric_map(space, space, {1: 1, 2: 1})
    assert profile.bijective is False
    assert profile.homeomorphism is False


def test_classify_non_expansive():
    space = _two_point()
    profile = classify_finite_metric_map(space, space, {1: 1, 2: 2})
    assert profile.non_expansive is True
    assert profile.lipschitz is True
    assert profile.uniformly_continuous is True
    assert profile.continuous is True


# ---------------------------------------------------------------------------
# metric_map_profile — symbolic
# ---------------------------------------------------------------------------

def test_metric_map_profile_symbolic():
    profile = metric_map_profile(name="f", isometry=True, bijective=True)
    assert profile.certification == "symbolic-profile"
    assert profile.isometry is True
    assert profile.bijective is True
    assert len(profile.notes) >= 2
