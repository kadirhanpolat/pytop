"""Tests for tda_pipeline.py — high-level TDA pipeline API."""

from __future__ import annotations

import math

import pytest

from pytop.persistent_homology import FilteredComplex, PersistencePair
from pytop.tda_pipeline import TDAPipeline

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _circle_points(n: int = 8) -> list[tuple[float, float]]:
    return [
        (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]


def _line_points(n: int = 4) -> list[tuple[float,]]:
    return [(float(i),) for i in range(n)]


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_default_empty_pipeline(self) -> None:
        pipe = TDAPipeline()
        assert pipe.filtered is None
        assert pipe.computed_pairs is None

    def test_from_points_returns_pipeline(self) -> None:
        pipe = TDAPipeline.from_points(_circle_points())
        assert isinstance(pipe, TDAPipeline)
        assert pipe.filtered is None

    def test_from_filtration_has_filtered(self) -> None:
        fc = FilteredComplex(
            simplices=((0,), (1,), (0, 1)),
            births=(0.0, 0.0, 1.0),
            dimensions=(0, 0, 1),
        )
        pipe = TDAPipeline.from_filtration(fc)
        assert pipe.filtered is fc
        assert pipe.computed_pairs is None

    def test_immutability(self) -> None:
        pts = _circle_points(4)
        pipe1 = TDAPipeline()
        pipe2 = pipe1.rips(pts, max_dimension=1)
        assert pipe1.filtered is None
        assert pipe2.filtered is not None


# ---------------------------------------------------------------------------
# Filtration steps
# ---------------------------------------------------------------------------


class TestFiltration:
    def test_rips_builds_filtration(self) -> None:
        pts = _circle_points(6)
        pipe = TDAPipeline().rips(pts, max_dimension=1)
        assert pipe.filtered is not None
        assert pipe.filtered.size() > 0

    def test_cech_builds_filtration(self) -> None:
        pts = _circle_points(6)
        pipe = TDAPipeline().cech(pts, max_dimension=1)
        assert pipe.filtered is not None
        assert pipe.filtered.size() > 0

    def test_rips_no_points_raises(self) -> None:
        with pytest.raises(ValueError):
            TDAPipeline().rips()

    def test_cech_no_points_raises(self) -> None:
        with pytest.raises(ValueError):
            TDAPipeline().cech()

    def test_rips_respects_max_scale(self) -> None:
        pts = [(0.0,), (10.0,)]
        pipe = TDAPipeline().rips(pts, max_dimension=1, max_scale=3.0)
        assert pipe.filtered is not None
        assert pipe.filtered.size() == 2  # only vertices, no edge

    def test_cech_respects_max_scale(self) -> None:
        pts = [(0.0,), (10.0,)]
        pipe = TDAPipeline().cech(pts, max_dimension=1, max_scale=3.0)
        assert pipe.filtered is not None
        assert pipe.filtered.size() == 2


# ---------------------------------------------------------------------------
# Reduction steps
# ---------------------------------------------------------------------------


class TestReduction:
    def _rips_pipe(self, pts: list, max_dim: int = 1) -> TDAPipeline:
        return TDAPipeline().rips(pts, max_dimension=max_dim)

    def test_standard_reduction(self) -> None:
        pts = _circle_points(6)
        pipe = self._rips_pipe(pts).reduce("standard")
        assert pipe.computed_pairs is not None
        assert len(pipe.computed_pairs) > 0

    def test_twist_reduction(self) -> None:
        pts = _circle_points(6)
        pipe = self._rips_pipe(pts).reduce("twist")
        assert pipe.computed_pairs is not None

    def test_cohomology_reduction(self) -> None:
        pts = _circle_points(6)
        pipe = self._rips_pipe(pts).reduce("cohomology")
        assert pipe.computed_pairs is not None

    def test_fp_reduction_p2(self) -> None:
        pts = _circle_points(6)
        pipe = self._rips_pipe(pts).reduce("fp", prime=2)
        assert pipe.computed_pairs is not None

    def test_fp_reduction_p3(self) -> None:
        pts = _circle_points(6)
        pipe = self._rips_pipe(pts).reduce("fp", prime=3)
        assert pipe.computed_pairs is not None

    def test_fp_invalid_prime_raises(self) -> None:
        pts = _circle_points(4)
        pipe = self._rips_pipe(pts)
        with pytest.raises(ValueError):
            pipe.reduce("fp", prime=4)

    def test_unknown_method_raises(self) -> None:
        pts = _circle_points(4)
        pipe = self._rips_pipe(pts)
        with pytest.raises(ValueError):
            pipe.reduce("unknown")

    def test_reduce_without_filtration_raises(self) -> None:
        with pytest.raises(RuntimeError):
            TDAPipeline().reduce()

    def test_standard_and_twist_agree(self) -> None:
        pts = _circle_points(6)
        pipe = self._rips_pipe(pts)
        std = pipe.reduce("standard").pairs()
        twist = pipe.reduce("twist").pairs()
        assert set(std) == set(twist)

    def test_standard_and_fp2_agree(self) -> None:
        pts = _line_points(4)
        pipe = self._rips_pipe(pts, max_dim=2)
        std = pipe.reduce("standard").pairs()
        fp2 = pipe.reduce("fp", prime=2).pairs()
        assert set(std) == set(fp2)


# ---------------------------------------------------------------------------
# Output methods
# ---------------------------------------------------------------------------


class TestOutputMethods:
    def _reduced_pipe(self, pts: list, max_dim: int = 1) -> TDAPipeline:
        return TDAPipeline().rips(pts, max_dimension=max_dim).reduce()

    def test_pairs_returns_tuple_of_pairs(self) -> None:
        pipe = self._reduced_pipe(_circle_points(6))
        pairs = pipe.pairs()
        assert isinstance(pairs, tuple)
        assert all(isinstance(p, PersistencePair) for p in pairs)

    def test_pairs_dimension_filter(self) -> None:
        pipe = self._reduced_pipe(_circle_points(6))
        h0 = pipe.pairs(dimension=0)
        assert all(p.dimension == 0 for p in h0)

    def test_pairs_without_reduce_raises(self) -> None:
        pipe = TDAPipeline().rips(_circle_points(4), max_dimension=1)
        with pytest.raises(RuntimeError):
            pipe.pairs()

    def test_barcode_returns_tuples(self) -> None:
        pipe = self._reduced_pipe(_line_points(4), max_dim=2)
        bars = pipe.barcode()
        assert isinstance(bars, tuple)
        assert all(isinstance(b, tuple) and len(b) == 2 for b in bars)

    def test_barcode_dimension_filter(self) -> None:
        pipe = self._reduced_pipe(_circle_points(6))
        bars0 = pipe.barcode(dimension=0)
        bars1 = pipe.barcode(dimension=1)
        assert all(b[0] <= b[1] for b in bars0)
        assert all(b[0] <= b[1] for b in bars1)

    def test_diagram_returns_dict(self) -> None:
        pipe = self._reduced_pipe(_circle_points(6))
        diag = pipe.diagram()
        assert isinstance(diag, dict)
        assert all(isinstance(k, int) for k in diag)

    def test_diagram_without_reduce_raises(self) -> None:
        with pytest.raises(RuntimeError):
            TDAPipeline().rips(_circle_points(4), max_dimension=1).diagram()

    def test_entropy_returns_float(self) -> None:
        pipe = self._reduced_pipe(_line_points(4), max_dim=2)
        h = pipe.entropy()
        assert isinstance(h, float)
        assert h >= 0.0

    def test_entropy_by_dimension(self) -> None:
        pipe = self._reduced_pipe(_circle_points(6))
        h0 = pipe.entropy(dimension=0)
        assert isinstance(h0, float)

    def test_landscape_returns_landscape(self) -> None:
        from pytop.persistence_distances import PersistenceLandscape as PL

        pipe = self._reduced_pipe(_circle_points(6))
        ls = pipe.landscape(dimension=0, k=1, num_points=50)
        assert isinstance(ls, PL)

    def test_summary_is_string(self) -> None:
        pipe = self._reduced_pipe(_circle_points(6))
        s = pipe.summary()
        assert isinstance(s, str)
        assert "TDAPipeline" in s
        assert "filtration" in s
        assert "pairs" in s

    def test_summary_no_filtration(self) -> None:
        s = TDAPipeline().summary()
        assert "not yet built" in s

    def test_summary_no_pairs(self) -> None:
        pipe = TDAPipeline().rips(_circle_points(4), max_dimension=1)
        s = pipe.summary()
        assert "not yet reduced" in s


# ---------------------------------------------------------------------------
# Distances
# ---------------------------------------------------------------------------


class TestDistances:
    def _reduced_pipe(self, pts: list, max_dim: int = 1) -> TDAPipeline:
        return TDAPipeline().rips(pts, max_dimension=max_dim).reduce()

    def test_bottleneck_self_is_zero(self) -> None:
        pipe = self._reduced_pipe(_circle_points(6))
        d = pipe.bottleneck(pipe)
        assert d == pytest.approx(0.0, abs=1e-10)

    def test_wasserstein_self_is_zero(self) -> None:
        pipe = self._reduced_pipe(_circle_points(6))
        d = pipe.wasserstein(pipe)
        assert d == pytest.approx(0.0, abs=1e-10)

    def test_bottleneck_nonneg(self) -> None:
        p1 = self._reduced_pipe(_circle_points(6))
        p2 = self._reduced_pipe(_circle_points(8))
        assert p1.bottleneck(p2) >= 0.0

    def test_wasserstein_nonneg(self) -> None:
        p1 = self._reduced_pipe(_circle_points(6))
        p2 = self._reduced_pipe(_circle_points(8))
        assert p1.wasserstein(p2) >= 0.0

    def test_bottleneck_without_reduce_raises(self) -> None:
        pipe = TDAPipeline().rips(_circle_points(4), max_dimension=1)
        pipe2 = self._reduced_pipe(_circle_points(4))
        with pytest.raises(RuntimeError):
            pipe.bottleneck(pipe2)


# ---------------------------------------------------------------------------
# compare_primes
# ---------------------------------------------------------------------------


class TestComparePrimes:
    def test_returns_dict(self) -> None:
        pts = _circle_points(6)
        pipe = TDAPipeline().rips(pts, max_dimension=1)
        result = pipe.compare_primes([2, 3, 5])
        assert isinstance(result, dict)
        assert set(result.keys()) == {2, 3, 5}

    def test_each_value_is_pairs_tuple(self) -> None:
        pts = _circle_points(6)
        pipe = TDAPipeline().rips(pts, max_dimension=1)
        result = pipe.compare_primes([2, 3])
        for p_val in result.values():
            assert isinstance(p_val, tuple)
            assert all(isinstance(pp, PersistencePair) for pp in p_val)

    def test_without_filtration_raises(self) -> None:
        with pytest.raises(RuntimeError):
            TDAPipeline().compare_primes([2, 3])

    def test_all_primes_agree_on_torsion_free(self) -> None:
        # Contractible space: all primes give same essential H_0
        pts = _line_points(4)
        pipe = TDAPipeline().rips(pts, max_dimension=2)
        result = pipe.compare_primes([2, 3, 5, 7])
        ess_h0 = {
            p: len([pp for pp in pairs if pp.is_essential and pp.dimension == 0])
            for p, pairs in result.items()
        }
        assert all(v == 1 for v in ess_h0.values()), f"H_0 counts: {ess_h0}"
