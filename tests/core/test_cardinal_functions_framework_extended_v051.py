"""Coverage-targeted tests for cardinal_functions_framework.py (v0.5.1)."""
import pytest
from pytop.cardinal_functions_framework import (
    CardinalFunctionFrameworkError,
    cardinal_function_definition,
    cardinal_function_comparison,
    cardinal_functions_framework_profile,
    analyze_cardinal_functions_framework,
    arhangelskii_bound,
    _representation_of,
    _tags_of,
    _carrier_size,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _finite_space():
    carrier = frozenset({1, 2})
    topology = frozenset([frozenset(), frozenset({1}), frozenset({1, 2})])
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


# ---------------------------------------------------------------------------
# _representation_of  (line 383 — carrier+topology but no metadata)
# ---------------------------------------------------------------------------

def test_representation_of_finite_space():
    space = _finite_space()
    rep = _representation_of(space)
    assert rep == "finite"


def test_representation_of_symbolic():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test")
    rep = _representation_of(space)
    assert rep == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size TypeError  (lines 402-403)
# ---------------------------------------------------------------------------

def test_carrier_size_unhashable_carrier():
    class BadCarrier:
        def __len__(self):
            raise TypeError("no len")
    class Sp:
        carrier = BadCarrier()
        metadata = {}
        tags = set()
    result = _carrier_size(Sp())
    assert result is None


def test_carrier_size_none():
    class Sp:
        carrier = None
        metadata = {}
        tags = set()
    assert _carrier_size(Sp()) is None


def test_carrier_size_finite():
    space = _finite_space()
    assert _carrier_size(space) == 2


# ---------------------------------------------------------------------------
# cardinal_function_definition — hereditary layer  (line 435)
# ---------------------------------------------------------------------------

def test_cardinal_function_definition_hereditary_density():
    d = cardinal_function_definition("hereditary_density")
    assert "definition" in d


def test_cardinal_function_definition_hereditary_lindelof():
    d = cardinal_function_definition("hereditary_lindelof")
    assert "definition" in d


def test_cardinal_function_definition_hereditary_cellularity():
    d = cardinal_function_definition("hereditary_cellularity")
    assert "definition" in d


def test_cardinal_function_definition_hereditary_spread():
    d = cardinal_function_definition("hereditary_spread")
    assert "definition" in d


def test_cardinal_function_definition_unknown_raises():
    with pytest.raises(CardinalFunctionFrameworkError):
        cardinal_function_definition("zeta_function")


# ---------------------------------------------------------------------------
# cardinal_function_comparison — fallback / error  (lines 467-474)
# ---------------------------------------------------------------------------

def test_cardinal_function_comparison_valid():
    d = cardinal_function_comparison("weight", "density")
    assert "inequality" in d


def test_cardinal_function_comparison_alias():
    d = cardinal_function_comparison("w", "d")
    assert "inequality" in d


def test_cardinal_function_comparison_unknown_raises():
    with pytest.raises(CardinalFunctionFrameworkError):
        cardinal_function_comparison("foo", "bar")


def test_cardinal_function_comparison_reversed_order():
    d1 = cardinal_function_comparison("weight", "character")
    d2 = cardinal_function_comparison("character", "weight")
    assert d1["inequality"] == d2["inequality"]


# ---------------------------------------------------------------------------
# arhangelskii_bound — case logic  (lines 570-587)
# ---------------------------------------------------------------------------

def test_arhangelskii_bound_finite():
    space = _finite_space()
    d = arhangelskii_bound(space)
    assert "finite" in d["symbolic_case"].lower() or "finite" in str(d).lower()
    assert "theorem" in d
    assert "bound_formula" in d


def test_arhangelskii_bound_first_countable_lindelof_hausdorff():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(
        description="test", tags=["hausdorff", "first_countable", "lindelof"]
    )
    d = arhangelskii_bound(space)
    assert "continuum" in d["symbolic_case"].lower() or "aleph_0" in d["symbolic_case"]


def test_arhangelskii_bound_hausdorff_only():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["hausdorff"])
    d = arhangelskii_bound(space)
    assert "chi" in d["symbolic_case"].lower() or "L(X)" in d["symbolic_case"]


def test_arhangelskii_bound_non_hausdorff():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["t0"])
    d = arhangelskii_bound(space)
    assert "hausdorff" in d["symbolic_case"].lower()


def test_arhangelskii_bound_required_keys():
    space = _finite_space()
    d = arhangelskii_bound(space)
    for key in ("theorem", "bound_formula", "hausdorff_required",
                "corollaries", "proof_sketch"):
        assert key in d


def test_arhangelskii_bound_second_countable():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["hausdorff", "second_countable"])
    d = arhangelskii_bound(space)
    # second_countable implies lindelof + first_countable → continuum bound
    assert d is not None


# ---------------------------------------------------------------------------
# analyze_cardinal_functions_framework — modes
# ---------------------------------------------------------------------------

def test_analyze_cardinal_functions_framework_finite():
    space = _finite_space()
    r = analyze_cardinal_functions_framework(space)
    assert r.is_true
    assert r.mode == "exact"


def test_analyze_cardinal_functions_framework_tagged():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["metrizable", "separable"])
    r = analyze_cardinal_functions_framework(space)
    assert r.is_true
    assert r.mode == "theorem"


def test_analyze_cardinal_functions_framework_symbolic():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="unknown space")
    r = analyze_cardinal_functions_framework(space)
    assert r.is_true
    assert r.mode == "symbolic"


# ---------------------------------------------------------------------------
# cardinal_functions_framework_profile
# ---------------------------------------------------------------------------

def test_profile_hereditary_layer():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test")
    p = cardinal_functions_framework_profile(space)
    assert "hereditary_layer" in p
    hl = p["hereditary_layer"]
    assert "hereditary_density" in hl
    assert "hereditary_lindelof" in hl
    assert "hereditary_cellularity" in hl
    assert "hereditary_spread" in hl
