"""
test_cilt3_function_spaces_v058.py
===================================
Test suite for src/pytop/function_spaces.py  (v0.1.58)

Covers:
  - pointwise_topology_profile
  - uniform_topology_profile
  - compact_open_topology_profile
  - function_space_profile
  - analyze_function_space
  - FunctionSpaceError existence
  - finite space behaviour
  - symbolic / tagged space behaviour
"""

import importlib.util
import sys
import os
import pytest

# ---------------------------------------------------------------------------
# Load function_spaces from source (bypass stale .pyc cache)
# ---------------------------------------------------------------------------

_BASE = os.path.join(
    os.path.dirname(__file__), "..", "..", "src", "pytop"
)

def _load(name, rel):
    path = os.path.normpath(os.path.join(_BASE, rel))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "pytop"
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

# Warm up the full package first so all sub-dependencies are in sys.modules
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
import pytop as _pytop_pkg  # noqa: E402

_fs_mod = _load("pytop.function_spaces", "function_spaces.py")

FiniteTopologicalSpace      = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace
pointwise_topology_profile  = _fs_mod.pointwise_topology_profile
uniform_topology_profile    = _fs_mod.uniform_topology_profile
compact_open_topology_profile = _fs_mod.compact_open_topology_profile
function_space_profile      = _fs_mod.function_space_profile
analyze_function_space      = _fs_mod.analyze_function_space
FunctionSpaceError          = _fs_mod.FunctionSpaceError


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_finite(n: int) -> FiniteTopologicalSpace:
    """Return a finite discrete space with n points."""
    carrier = list(range(n))
    # Discrete topology: all subsets
    topology = [frozenset(s) for s in _powerset(carrier)]
    return FiniteTopologicalSpace(carrier=frozenset(carrier), topology=frozenset(topology))


def _powerset(lst):
    from itertools import chain, combinations
    return chain.from_iterable(combinations(lst, r) for r in range(len(lst)+1))


class _Tagged:
    """Minimal space with metadata tags and a representation."""
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}
        self.representation = representation


class _CompactTagged(_Tagged):
    def __init__(self):
        super().__init__(tags=["compact", "hausdorff", "second_countable"])


class _LocallyCompactTagged(_Tagged):
    def __init__(self):
        super().__init__(tags=["locally_compact", "locally_compact_hausdorff"])


class _UncountableTagged(_Tagged):
    def __init__(self):
        super().__init__(tags=["uncountable", "non_second_countable"])


# ---------------------------------------------------------------------------
# FunctionSpaceError
# ---------------------------------------------------------------------------

def test_function_space_error_is_exception():
    assert issubclass(FunctionSpaceError, Exception)


def test_function_space_error_can_be_raised():
    with pytest.raises(FunctionSpaceError, match="test"):
        raise FunctionSpaceError("test")


# ---------------------------------------------------------------------------
# pointwise_topology_profile — finite spaces
# ---------------------------------------------------------------------------

def test_pointwise_finite_hausdorff():
    space = make_finite(3)
    p = pointwise_topology_profile(space)
    assert p["hausdorff"] is True


def test_pointwise_finite_first_countable():
    space = make_finite(3)
    p = pointwise_topology_profile(space)
    assert p["first_countable"] is True


def test_pointwise_finite_representation():
    space = make_finite(4)
    p = pointwise_topology_profile(space)
    assert p["representation"] == "finite"


def test_pointwise_finite_second_countable_mentions_finite():
    space = make_finite(2)
    p = pointwise_topology_profile(space)
    assert "finite" in p["second_countable_condition"].lower()


def test_pointwise_finite_metrizability_product():
    space = make_finite(3)
    p = pointwise_topology_profile(space)
    assert "metrizable" in p["metrizability_note"].lower()


def test_pointwise_finite_basis_mentions_n():
    space = make_finite(5)
    p = pointwise_topology_profile(space)
    # basis description should mention the carrier size
    assert "5" in p["basis_description"]


# ---------------------------------------------------------------------------
# pointwise_topology_profile — tagged spaces
# ---------------------------------------------------------------------------

def test_pointwise_second_countable_tag():
    space = _Tagged(tags=["second_countable"])
    p = pointwise_topology_profile(space)
    assert "second countable" in p["second_countable_condition"].lower()


def test_pointwise_uncountable_tag():
    space = _UncountableTagged()
    p = pointwise_topology_profile(space)
    assert "not" in p["second_countable_condition"].lower()


def test_pointwise_symbolic_default_metrizability():
    space = _Tagged()
    p = pointwise_topology_profile(space)
    assert "countable" in p["metrizability_note"].lower()


# ---------------------------------------------------------------------------
# uniform_topology_profile — finite spaces
# ---------------------------------------------------------------------------

def test_uniform_finite_metrizable():
    space = make_finite(3)
    u = uniform_topology_profile(space)
    assert u["metrizable"] is True


def test_uniform_finite_complete():
    space = make_finite(3)
    u = uniform_topology_profile(space)
    assert "complete" in u["complete"].lower()


def test_uniform_finite_separable():
    space = make_finite(2)
    u = uniform_topology_profile(space)
    assert "separable" in u["separable"].lower() or "yes" in u["separable"].lower()


def test_uniform_finite_metric_desc_mentions_max():
    space = make_finite(4)
    u = uniform_topology_profile(space)
    assert "max" in u["metric_description"].lower() or "d_∞" in u["metric_description"]


def test_uniform_comparison_with_pointwise_present():
    space = make_finite(3)
    u = uniform_topology_profile(space)
    assert "pointwise" in u["comparison_with_pointwise"].lower()


# ---------------------------------------------------------------------------
# uniform_topology_profile — tagged spaces
# ---------------------------------------------------------------------------

def test_uniform_compact_tag_complete():
    space = _CompactTagged()
    u = uniform_topology_profile(space)
    assert "compact" in u["complete"].lower() or "complete" in u["complete"].lower()


def test_uniform_compact_metrizable_tag_separable():
    space = _Tagged(tags=["compact_metrizable"])
    u = uniform_topology_profile(space)
    assert "separable" in u["separable"].lower() or "yes" in u["separable"].lower()


# ---------------------------------------------------------------------------
# compact_open_topology_profile — finite spaces
# ---------------------------------------------------------------------------

def test_compact_open_finite_coincides_uniform():
    space = make_finite(3)
    co = compact_open_topology_profile(space)
    assert "finite" in co["coincides_with_uniform"].lower()


def test_compact_open_finite_exponential_law():
    space = make_finite(2)
    co = compact_open_topology_profile(space)
    assert "exponential" in co["exponential_law"].lower() or "holds" in co["exponential_law"].lower()


def test_compact_open_hausdorff_finite():
    space = make_finite(3)
    co = compact_open_topology_profile(space)
    assert "hausdorff" in str(co["hausdorff"]).lower() or co["hausdorff"] is True or "yes" in str(co["hausdorff"]).lower()


def test_compact_open_basis_description_present():
    space = make_finite(2)
    co = compact_open_topology_profile(space)
    assert "V(K" in co["basis_description"] or "compact" in co["basis_description"].lower()


# ---------------------------------------------------------------------------
# compact_open_topology_profile — tagged spaces
# ---------------------------------------------------------------------------

def test_compact_open_compact_tag_coincides():
    space = _CompactTagged()
    co = compact_open_topology_profile(space)
    assert "compact" in co["coincides_with_uniform"].lower()


def test_compact_open_locally_compact_tag():
    space = _LocallyCompactTagged()
    co = compact_open_topology_profile(space)
    assert "locally compact" in co["coincides_with_uniform"].lower()


def test_compact_open_exponential_locally_compact():
    space = _LocallyCompactTagged()
    co = compact_open_topology_profile(space)
    assert "exponential" in co["exponential_law"].lower() or "locally compact" in co["exponential_law"].lower()


# ---------------------------------------------------------------------------
# function_space_profile
# ---------------------------------------------------------------------------

def test_function_space_profile_keys():
    space = make_finite(3)
    prof = function_space_profile(space)
    assert set(prof.keys()) == {"domain_representation", "pointwise", "uniform", "compact_open"}


def test_function_space_profile_representation_finite():
    space = make_finite(2)
    prof = function_space_profile(space)
    assert prof["domain_representation"] == "finite"


def test_function_space_profile_symbolic():
    space = _Tagged()
    prof = function_space_profile(space)
    assert prof["domain_representation"] == "symbolic_general"


# ---------------------------------------------------------------------------
# analyze_function_space — Result contract
# ---------------------------------------------------------------------------

def test_analyze_function_space_returns_result():
    space = make_finite(3)
    r = analyze_function_space(space)
    assert hasattr(r, "status")


def test_analyze_function_space_status_true():
    space = make_finite(3)
    r = analyze_function_space(space)
    assert r.status == "true"


def test_analyze_function_space_mode_exact_for_finite():
    space = make_finite(2)
    r = analyze_function_space(space)
    assert r.mode == "exact"


def test_analyze_function_space_mode_theorem_for_symbolic():
    space = _Tagged()
    r = analyze_function_space(space)
    assert r.mode == "theorem"


def test_analyze_function_space_value_is_profile():
    space = make_finite(3)
    r = analyze_function_space(space)
    assert isinstance(r.value, dict)
    assert "pointwise" in r.value


def test_analyze_function_space_justification_nonempty():
    space = make_finite(3)
    r = analyze_function_space(space)
    assert len(r.justification) > 0


def test_analyze_function_space_metadata_version():
    space = make_finite(3)
    r = analyze_function_space(space)
    assert r.metadata.get("version") == "0.1.58"


def test_analyze_function_space_metadata_carrier_size():
    space = make_finite(4)
    r = analyze_function_space(space)
    assert r.metadata.get("carrier_size") == 4


def test_analyze_function_space_compact_tagged():
    space = _CompactTagged()
    r = analyze_function_space(space)
    assert r.status == "true"
    assert r.mode == "theorem"


def test_analyze_finite_justification_mentions_n():
    space = make_finite(3)
    r = analyze_function_space(space)
    justification_str = " ".join(r.justification)
    assert "3" in justification_str or "finite" in justification_str.lower()
