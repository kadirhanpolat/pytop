"""
test_cilt3_function_spaces_v059.py
===================================
Test suite for v0.1.59 extensions in src/pytop/function_spaces.py

Covers:
  - compact_open_basis_elements  (new in v0.1.59)
  - compact_open_homotopy_profile (new in v0.1.59)
"""

import importlib.util
import os
import sys

# ---------------------------------------------------------------------------
# Load from source
# ---------------------------------------------------------------------------

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

_fs_mod = _load("pytop.function_spaces", "function_spaces.py")

FiniteTopologicalSpace          = sys.modules["pytop.finite_spaces"].FiniteTopologicalSpace
compact_open_basis_elements     = _fs_mod.compact_open_basis_elements
compact_open_homotopy_profile   = _fs_mod.compact_open_homotopy_profile


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

from itertools import combinations  # noqa: E402


def make_finite(n):
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


class _CWComplexTagged(_Tagged):
    def __init__(self):
        super().__init__(tags=["cw_complex", "locally_compact_hausdorff"])


# ===========================================================================
# compact_open_basis_elements
# ===========================================================================

class TestCompactOpenBasisElements:

    def test_required_keys_present(self):
        b = compact_open_basis_elements(make_finite(3))
        required = {
            "topology_name", "subbasis_description", "basis_description",
            "neighbourhood_base", "convergence_characterisation", "representation",
        }
        assert required.issubset(b.keys())

    def test_finite_space_has_finite_example(self):
        b = compact_open_basis_elements(make_finite(3))
        assert "finite_example" in b

    def test_finite_example_mentions_carrier_size(self):
        b = compact_open_basis_elements(make_finite(4))
        assert "4" in b["finite_example"]

    def test_finite_representation_tag(self):
        b = compact_open_basis_elements(make_finite(2))
        assert b["representation"] == "finite"

    def test_symbolic_no_finite_example(self):
        b = compact_open_basis_elements(_Tagged())
        assert "finite_example" not in b

    def test_symbolic_representation_tag(self):
        b = compact_open_basis_elements(_Tagged())
        assert b["representation"] == "symbolic_general"

    def test_subbasis_mentions_VKU(self):
        b = compact_open_basis_elements(make_finite(3))
        assert "S(K" in b["subbasis_description"] or "V(K" in b["subbasis_description"]

    def test_basis_mentions_intersection(self):
        b = compact_open_basis_elements(make_finite(3))
        assert "⋂" in b["basis_description"] or "intersection" in b["basis_description"].lower()

    def test_convergence_characterisation_mentions_compact(self):
        b = compact_open_basis_elements(_Tagged())
        assert "compact" in b["convergence_characterisation"].lower()

    def test_convergence_characterisation_uniform_on_compacta(self):
        b = compact_open_basis_elements(_Tagged())
        assert "uniform" in b["convergence_characterisation"].lower()

    def test_locally_compact_nbhd_base(self):
        b = compact_open_basis_elements(_LocallyCompactTagged())
        assert "locally compact" in b["neighbourhood_base"].lower()

    def test_compact_nbhd_base(self):
        b = compact_open_basis_elements(_CompactTagged())
        assert "compact" in b["neighbourhood_base"].lower()

    def test_finite_nbhd_base_mentions_product(self):
        b = compact_open_basis_elements(make_finite(3))
        assert "product" in b["neighbourhood_base"].lower() or "singleton" in b["neighbourhood_base"].lower()

    def test_topology_name_contains_compact_open(self):
        b = compact_open_basis_elements(make_finite(2))
        assert "compact-open" in b["topology_name"].lower()

    def test_finite_n1(self):
        """Edge case: single-point space."""
        b = compact_open_basis_elements(make_finite(1))
        assert "finite_example" in b
        assert "1" in b["finite_example"]


# ===========================================================================
# compact_open_homotopy_profile
# ===========================================================================

class TestCompactOpenHomotopyProfile:

    def test_required_keys_present(self):
        h = compact_open_homotopy_profile(make_finite(3))
        required = {
            "topology_name", "loop_space", "path_space", "free_loop_space",
            "adjunction_with_suspension", "cw_complex_note",
            "exponential_law_statement", "representation",
        }
        assert required.issubset(h.keys())

    def test_loop_space_mentions_pi1(self):
        h = compact_open_homotopy_profile(make_finite(3))
        assert "π₁" in h["loop_space"] or "pi_1" in h["loop_space"].lower()

    def test_loop_space_mentions_interval(self):
        h = compact_open_homotopy_profile(make_finite(3))
        assert "[0,1]" in h["loop_space"] or "interval" in h["loop_space"].lower()

    def test_path_space_mentions_fibration(self):
        h = compact_open_homotopy_profile(_CompactTagged())
        assert "fibration" in h["path_space"].lower()

    def test_free_loop_space_mentions_S1(self):
        h = compact_open_homotopy_profile(make_finite(3))
        assert "S¹" in h["free_loop_space"] or "S1" in h["free_loop_space"] or "loop" in h["free_loop_space"].lower()

    def test_exponential_law_statement_present(self):
        h = compact_open_homotopy_profile(make_finite(3))
        assert "exponential" in h["exponential_law_statement"].lower()

    def test_exponential_law_mentions_locally_compact(self):
        h = compact_open_homotopy_profile(_Tagged())
        assert "locally compact" in h["exponential_law_statement"].lower()

    def test_adjunction_locally_compact(self):
        h = compact_open_homotopy_profile(_LocallyCompactTagged())
        s = h["adjunction_with_suspension"].lower()
        assert "adjunction" in s or "locally compact" in s

    def test_adjunction_cw_complex(self):
        h = compact_open_homotopy_profile(_CWComplexTagged())
        s = h["adjunction_with_suspension"].lower()
        assert "adjunction" in s or "cw" in s or "locally compact" in s

    def test_adjunction_finite_mentions_suspension(self):
        h = compact_open_homotopy_profile(make_finite(3))
        assert "suspension" in h["adjunction_with_suspension"].lower() or "exponential" in h["adjunction_with_suspension"].lower()

    def test_cw_complex_note_for_cw_tagged(self):
        h = compact_open_homotopy_profile(_CWComplexTagged())
        assert "cw" in h["cw_complex_note"].lower() or "compactly generated" in h["cw_complex_note"].lower()

    def test_cw_complex_note_general_space(self):
        h = compact_open_homotopy_profile(_Tagged())
        assert "k-space" in h["cw_complex_note"].lower() or "compactly generated" in h["cw_complex_note"].lower()

    def test_representation_finite(self):
        h = compact_open_homotopy_profile(make_finite(2))
        assert h["representation"] == "finite"

    def test_representation_symbolic(self):
        h = compact_open_homotopy_profile(_Tagged())
        assert h["representation"] == "symbolic_general"

    def test_topology_name_contains_homotopy(self):
        h = compact_open_homotopy_profile(make_finite(3))
        assert "homotopy" in h["topology_name"].lower() or "compact-open" in h["topology_name"].lower()
