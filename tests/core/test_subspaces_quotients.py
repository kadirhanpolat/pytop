"""Tests for subspaces.py and quotients.py — unified construction modules."""

import pytest
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_maps import ContinuousMap, QuotientMap
from pytop.infinite_spaces import InfiniteTopologicalSpace
from pytop.maps import FiniteMap
from pytop.quotients import (
    analyze_quotient_map,
    make_quotient_map,
    quotient_space,
    quotient_space_from_map,
)
from pytop.subspaces import finite_subspace, subspace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _discrete(*pts):
    pts = list(pts)
    n = len(pts)
    opens = [frozenset(pts[i] for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]
    return FiniteTopologicalSpace(carrier=tuple(pts), topology=opens)


def _symbolic(carrier="X"):
    return InfiniteTopologicalSpace(carrier=carrier, metadata={"representation": "infinite_T2"})


# ===========================================================================
# subspaces.py
# ===========================================================================


class TestSubspaceFinite:
    def test_carrier_is_intersection(self):
        X = _discrete(1, 2, 3)
        S = subspace(X, {1, 2})
        assert set(S.carrier) == {1, 2}

    def test_topology_is_trace(self):
        X = _discrete(1, 2, 3)
        S = subspace(X, {1, 2})
        opens = {frozenset(U) for U in S.topology}
        assert frozenset({1}) in opens
        assert frozenset({2}) in opens
        assert frozenset({1, 2}) in opens

    def test_construction_key_in_metadata(self):
        X = _discrete(1, 2, 3)
        S = subspace(X, {1})
        assert S.metadata.get("construction") == "subspace"

    def test_custom_metadata_merged(self):
        X = _discrete(1, 2, 3)
        S = subspace(X, {1}, metadata={"note": "singleton"})
        assert S.metadata.get("note") == "singleton"

    def test_closed_flag_adds_tag(self):
        X = _discrete(1, 2, 3)
        S = subspace(X, {1, 2}, closed=True)
        assert "closed_subspace" in S.tags

    def test_open_flag_adds_tag(self):
        X = _discrete(1, 2, 3)
        S = subspace(X, {1, 2}, open=True)
        assert "open_subspace" in S.tags

    def test_dense_flag_adds_tag(self):
        X = _discrete(1, 2, 3)
        S = subspace(X, {1, 2}, dense=True)
        assert "dense_subspace" in S.tags

    def test_returns_finite_topological_space(self):
        X = _discrete(1, 2, 3)
        assert isinstance(subspace(X, {1}), FiniteTopologicalSpace)


class TestSubspaceSymbolic:
    def test_symbolic_space_returns_non_finite(self):
        S = subspace(_symbolic(), "A")
        assert not isinstance(S, FiniteTopologicalSpace)

    def test_space_without_is_finite_uses_symbolic_path(self):
        class BareSpace:
            carrier = (1, 2)
            topology = [set(), {1}, {2}, {1, 2}]

        S = subspace(BareSpace(), {1, 2})
        assert S is not None
        assert not isinstance(S, FiniteTopologicalSpace)


class TestFiniteSubspace:
    def test_returns_finite_space(self):
        X = _discrete(1, 2, 3)
        assert isinstance(finite_subspace(X, {2, 3}), FiniteTopologicalSpace)

    def test_raises_for_symbolic_space(self):
        with pytest.raises(TypeError, match="finite ambient"):
            finite_subspace(_symbolic(), "A")


# ===========================================================================
# quotients.py
# ===========================================================================


class TestQuotientSpaceFinite:
    def test_partition_collapses_two_points(self):
        X = _discrete(1, 2, 3)
        Q = quotient_space(X, [[1, 2], [3]])
        assert len(Q.carrier) == 2

    def test_quotient_space_tag_present(self):
        X = _discrete(1, 2, 3)
        Q = quotient_space(X, [[1, 2], [3]])
        assert "quotient_space" in Q.tags

    def test_construction_key_in_metadata(self):
        X = _discrete(1, 2, 3)
        Q = quotient_space(X, [[1], [2], [3]])
        assert Q.metadata.get("construction") == "quotient"

    def test_partition_size_recorded(self):
        X = _discrete(1, 2, 3)
        Q = quotient_space(X, [[1, 2], [3]])
        assert Q.metadata.get("partition_size") == 2

    def test_custom_metadata_merged(self):
        X = _discrete(1, 2, 3)
        Q = quotient_space(X, [[1, 2], [3]], metadata={"label": "Q"})
        assert Q.metadata.get("label") == "Q"

    def test_trivial_partition_is_identity(self):
        X = _discrete(1, 2)
        Q = quotient_space(X, [[1], [2]])
        assert len(Q.carrier) == 2


class TestQuotientSpaceSymbolic:
    def test_string_partition_returns_symbolic(self):
        X = _discrete(1, 2)
        Q = quotient_space(X, "equiv")
        assert not isinstance(Q, FiniteTopologicalSpace)

    def test_symbolic_space_returns_symbolic(self):
        Q = quotient_space(_symbolic(), [[1, 2]])
        assert not isinstance(Q, FiniteTopologicalSpace)

    def test_space_without_is_finite_returns_symbolic(self):
        class BareSpace:
            carrier = (1, 2, 3)
            topology = [set(), {1, 2, 3}]

        Q = quotient_space(BareSpace(), [[1, 2], [3]])
        assert not isinstance(Q, FiniteTopologicalSpace)


class TestQuotientSpaceFromMap:
    def test_finite_map_returns_finite_quotient(self):
        dom = _discrete(1, 2, 3)
        cod = _discrete(0, 1)
        f = FiniteMap(domain=dom, codomain=cod, mapping={1: 0, 2: 0, 3: 1}, name="q")
        Q = quotient_space_from_map(f)
        assert isinstance(Q, FiniteTopologicalSpace)

    def test_finite_quotient_has_quotient_space_tag(self):
        dom = _discrete(1, 2, 3)
        cod = _discrete(0, 1)
        f = FiniteMap(domain=dom, codomain=cod, mapping={1: 0, 2: 0, 3: 1}, name="q")
        assert "quotient_space" in quotient_space_from_map(f).tags

    def test_finite_quotient_construction_key(self):
        dom = _discrete(1, 2, 3)
        cod = _discrete(0, 1)
        f = FiniteMap(domain=dom, codomain=cod, mapping={1: 0, 2: 0, 3: 1}, name="q")
        Q = quotient_space_from_map(f)
        assert Q.metadata.get("construction") == "quotient_from_map"

    def test_custom_metadata_merged(self):
        dom = _discrete(1, 2)
        cod = _discrete(0,)
        f = FiniteMap(domain=dom, codomain=cod, mapping={1: 0, 2: 0}, name="q")
        Q = quotient_space_from_map(f, metadata={"fiber": "pair"})
        assert Q.metadata.get("fiber") == "pair"

    def test_symbolic_map_returns_symbolic(self):
        f = ContinuousMap(domain=_symbolic("X"), codomain=_symbolic("Y"), name="q")
        Q = quotient_space_from_map(f)
        assert not isinstance(Q, FiniteTopologicalSpace)


class TestMakeQuotientMap:
    def test_with_mapping_returns_finite_map(self):
        dom = _discrete(1, 2, 3)
        cod = _discrete(0, 1)
        qm = make_quotient_map(dom, cod, mapping={1: 0, 2: 0, 3: 1}, name="q")
        assert isinstance(qm, FiniteMap)

    def test_finite_map_has_surjective_tag(self):
        dom = _discrete(1, 2, 3)
        cod = _discrete(0, 1)
        qm = make_quotient_map(dom, cod, mapping={1: 0, 2: 0, 3: 1})
        assert "surjective" in qm.tags

    def test_no_mapping_returns_symbolic(self):
        dom = _discrete(1, 2)
        cod = _discrete(0,)
        qm = make_quotient_map(dom, cod, name="q")
        assert not isinstance(qm, FiniteMap)

    def test_symbolic_spaces_return_symbolic(self):
        qm = make_quotient_map(_symbolic("X"), _symbolic("Y"), name="q")
        assert not isinstance(qm, FiniteMap)

    def test_custom_name(self):
        dom = _discrete(1, 2, 3)
        cod = _discrete(0, 1)
        qm = make_quotient_map(dom, cod, mapping={1: 0, 2: 0, 3: 1}, name="pi")
        assert qm.name == "pi"


class TestAnalyzeQuotientMap:
    def test_finite_map_returns_exact_result(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        r = analyze_quotient_map(f)
        assert r.is_true or r.is_false

    def test_finite_identity_is_quotient(self):
        X = _discrete(1, 2)
        f = FiniteMap(domain=X, codomain=X, mapping={1: 1, 2: 2}, name="id")
        assert analyze_quotient_map(f).is_true

    def test_symbolic_quotient_map_returns_true(self):
        dom = _symbolic("X")
        cod = InfiniteTopologicalSpace(carrier="X/~", metadata={}, tags={"quotient_space"})
        qm = QuotientMap(domain=dom, codomain=cod, name="pi")
        assert analyze_quotient_map(qm).is_true

    def test_non_finite_map_dispatches_to_symbolic(self):
        f = ContinuousMap(domain=_symbolic("X"), codomain=_symbolic("Y"), name="f")
        r = analyze_quotient_map(f)
        assert r is not None
