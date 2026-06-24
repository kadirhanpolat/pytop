"""Tests for size-aware auto reduction routing (P17.3).

`persistence_pairs_auto` must produce output *identical* to both the Twist and
the cohomology reductions on every input; it only chooses the empirically faster
one based on the materialized complex size. `persistent_homology(method="auto")`
routes through it and is the default.
"""

from __future__ import annotations

import math

import pytest

from pytop.metric_spaces import FiniteMetricSpace
from pytop.persistent_homology import (
    persistence_pairs,
    persistent_homology,
    vietoris_rips_filtration,
)
from pytop.persistent_homology_optimized import (
    AUTO_COHOMOLOGY_THRESHOLD,
    persistence_pairs_auto,
    persistence_pairs_cohomology,
    persistence_pairs_twist,
    select_reduction_method,
)


def _euclidean(a, b):
    return math.dist(a, b)


def _metric_space(points):
    return FiniteMetricSpace(carrier=tuple(points), distance=_euclidean)


def _circle(n):
    return _metric_space(
        [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
    )


def _gauss_cloud(n, seed=0):
    import random

    rng = random.Random(seed)
    return _metric_space([(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)])


# ---------------------------------------------------------------------------
# Routing decision
# ---------------------------------------------------------------------------

def test_threshold_is_positive_int():
    assert isinstance(AUTO_COHOMOLOGY_THRESHOLD, int)
    assert AUTO_COHOMOLOGY_THRESHOLD > 0


def test_select_below_threshold_picks_twist():
    assert select_reduction_method(AUTO_COHOMOLOGY_THRESHOLD - 1) == "twist"
    assert select_reduction_method(0) == "twist"


def test_select_at_or_above_threshold_picks_cohomology():
    assert select_reduction_method(AUTO_COHOMOLOGY_THRESHOLD) == "cohomology"
    assert select_reduction_method(AUTO_COHOMOLOGY_THRESHOLD + 50_000) == "cohomology"


# ---------------------------------------------------------------------------
# Output identity (the correctness contract)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n", [4, 8, 12])
def test_auto_matches_peers_small(n):
    filt = vietoris_rips_filtration(_circle(n), max_dimension=2, max_scale=2.5)
    expected = persistence_pairs(filt)
    assert persistence_pairs_auto(filt) == expected
    assert persistence_pairs_twist(filt) == expected
    assert persistence_pairs_cohomology(filt) == expected


def test_auto_matches_peers_large():
    # Large enough to cross the cohomology threshold.
    filt = vietoris_rips_filtration(_gauss_cloud(60), max_dimension=2, max_scale=1.2)
    assert filt.size() >= AUTO_COHOMOLOGY_THRESHOLD
    expected = persistence_pairs(filt)
    assert persistence_pairs_auto(filt) == expected
    assert persistence_pairs_cohomology(filt) == expected


def test_auto_routes_small_to_twist_result():
    filt = vietoris_rips_filtration(_circle(5), max_dimension=1, max_scale=2.5)
    assert filt.size() < AUTO_COHOMOLOGY_THRESHOLD
    assert persistence_pairs_auto(filt) == persistence_pairs_twist(filt)


def test_auto_include_zero_persistence_passthrough():
    filt = vietoris_rips_filtration(_circle(6), max_dimension=2, max_scale=2.5)
    with_zero = persistence_pairs_auto(filt, include_zero_persistence=True)
    without_zero = persistence_pairs_auto(filt, include_zero_persistence=False)
    assert with_zero == persistence_pairs_twist(filt, include_zero_persistence=True)
    assert len(with_zero) >= len(without_zero)


def test_auto_empty_complex():
    from pytop.persistent_homology import FilteredComplex

    empty = FilteredComplex(simplices=(), births=(), dimensions=())
    assert persistence_pairs_auto(empty) == ()


# ---------------------------------------------------------------------------
# persistent_homology(method="auto") wiring + default
# ---------------------------------------------------------------------------

def test_persistent_homology_auto_method_matches_twist():
    space = _circle(10)
    got = persistent_homology(space, max_dimension=2, max_scale=2.5, method="auto")
    expected = persistent_homology(space, max_dimension=2, max_scale=2.5, method="twist")
    assert got == expected


def test_persistent_homology_default_is_auto():
    import inspect

    sig = inspect.signature(persistent_homology)
    assert sig.parameters["method"].default == "auto"


def test_persistent_homology_default_matches_explicit_methods():
    space = _circle(12)
    default = persistent_homology(space, max_dimension=2, max_scale=2.5)
    twist = persistent_homology(space, max_dimension=2, max_scale=2.5, method="twist")
    coh = persistent_homology(space, max_dimension=2, max_scale=2.5, method="cohomology")
    assert default == twist == coh


def test_invalid_method_still_raises():
    with pytest.raises(ValueError, match="method must be one of"):
        persistent_homology(_circle(5), method="bogus")


def test_auto_in_namespace():
    import pytop

    assert hasattr(pytop, "persistence_pairs_auto")
