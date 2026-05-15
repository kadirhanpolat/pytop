import importlib.util
import os
import sys


_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "src", "pytop")


def _load(name, rel):
    path = os.path.normpath(os.path.join(_BASE, rel))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "pytop"
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
import pytop as _pytop_pkg  # noqa: E402

_fs_mod = _load("pytop.function_spaces", "function_spaces.py")
FiniteTopologicalSpace = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace

function_space_topology_families = _fs_mod.function_space_topology_families
function_space_topology_selector = _fs_mod.function_space_topology_selector
render_function_space_topology_report = _fs_mod.render_function_space_topology_report
function_space_profile = _fs_mod.function_space_profile
analyze_function_space = _fs_mod.analyze_function_space
FunctionSpaceError = _fs_mod.FunctionSpaceError


def make_finite(n):
    from itertools import combinations

    c = list(range(n))
    t = [frozenset(s) for r in range(n + 1) for s in combinations(c, r)]
    return FiniteTopologicalSpace(carrier=frozenset(c), topology=frozenset(t))


class _Tagged:
    def __init__(self, tags=(), representation="symbolic_general"):
        self.metadata = {"tags": list(tags)}
        self.representation = representation


class _CompactTagged(_Tagged):
    def __init__(self):
        super().__init__(tags=["compact", "hausdorff", "second_countable"])


class _LocallyCompactTagged(_Tagged):
    def __init__(self):
        super().__init__(tags=["locally_compact", "locally_compact_hausdorff"])


def test_family_keys_and_lanes_v082():
    rows = function_space_topology_families(make_finite(3))
    assert [row["family_key"] for row in rows] == [
        "pointwise",
        "compact_open",
        "uniform",
    ]
    assert [row["lane"] for row in rows] == ["entry", "bridge", "advanced"]


def test_finite_family_ordering_note_v082():
    rows = function_space_topology_families(make_finite(2))
    assert all("finite" in row["ordering_note"] for row in rows)


def test_compact_family_ordering_note_v082():
    rows = function_space_topology_families(_CompactTagged())
    assert "coincide" in rows[0]["ordering_note"]


def test_locally_compact_warning_mentions_uniform_gap_v082():
    row = function_space_topology_selector(_LocallyCompactTagged(), "compact_open")
    assert "uniform" in row["warning_line"].lower()
    assert row["lane"] == "bridge"


def test_uniform_selector_returns_uniform_profile_v082():
    row = function_space_topology_selector(_Tagged(), "uniform")
    assert row["family_key"] == "uniform"
    assert row["profile"]["topology_name"] == "uniform convergence topology"


def test_selector_unknown_key_raises_v082():
    try:
        function_space_topology_selector(_Tagged(), "banana")
    except FunctionSpaceError as exc:
        assert "unknown function-space family key" in str(exc)
    else:
        raise AssertionError("FunctionSpaceError was not raised")


def test_profile_keeps_legacy_keyset_v082():
    profile = function_space_profile(_Tagged())
    assert set(profile.keys()) == {
        "domain_representation",
        "pointwise",
        "uniform",
        "compact_open",
    }


def test_render_report_mentions_all_three_topologies_v082():
    report = render_function_space_topology_report(_Tagged())
    assert "pointwise" in report
    assert "compact-open" in report
    assert "uniform" in report


def test_analyze_function_space_justification_mentions_report_v082():
    result = analyze_function_space(_LocallyCompactTagged())
    joined = " ".join(result.justification)
    assert "Function-space topology separation report" in joined
    assert "compact-open" in joined
