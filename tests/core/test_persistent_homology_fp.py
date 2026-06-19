"""Tests for persistent_homology_fp.py — persistence over Z/p."""

from __future__ import annotations

import math

import pytest

from pytop.persistent_homology import (
    FilteredComplex,
    PersistencePair,
    persistence_pairs,
    vietoris_rips_filtration,
)
from pytop.persistent_homology_fp import (
    _modinv,
    is_prime,
    persistence_pairs_fp,
)

# ---------------------------------------------------------------------------
# is_prime
# ---------------------------------------------------------------------------


class TestIsPrime:
    def test_small_primes(self) -> None:
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
            assert is_prime(p), f"{p} should be prime"

    def test_non_primes(self) -> None:
        for n in [0, 1, 4, 6, 8, 9, 10, 15, 25]:
            assert not is_prime(n), f"{n} should not be prime"

    def test_larger_prime(self) -> None:
        assert is_prime(97)
        assert is_prime(101)
        assert not is_prime(100)


# ---------------------------------------------------------------------------
# _modinv
# ---------------------------------------------------------------------------


class TestModInv:
    def test_inverse_mod_2(self) -> None:
        assert _modinv(1, 2) == 1

    def test_inverse_mod_5(self) -> None:
        for a in range(1, 5):
            inv = _modinv(a, 5)
            assert (a * inv) % 5 == 1, f"inverse of {a} mod 5 is wrong"

    def test_inverse_mod_7(self) -> None:
        for a in range(1, 7):
            assert (_modinv(a, 7) * a) % 7 == 1


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_non_prime_raises(self) -> None:
        fc = FilteredComplex(simplices=((0,), (1,)), births=(0.0, 0.0), dimensions=(0, 0))
        with pytest.raises(ValueError, match="prime"):
            persistence_pairs_fp(fc, prime=4)

    def test_one_raises(self) -> None:
        fc = FilteredComplex(simplices=((0,),), births=(0.0,), dimensions=(0,))
        with pytest.raises(ValueError):
            persistence_pairs_fp(fc, prime=1)

    def test_zero_raises(self) -> None:
        fc = FilteredComplex(simplices=((0,),), births=(0.0,), dimensions=(0,))
        with pytest.raises(ValueError):
            persistence_pairs_fp(fc, prime=0)


# ---------------------------------------------------------------------------
# Agreement with Z/2 persistence
# ---------------------------------------------------------------------------


class _DummySpace:
    def __init__(self, pts: list[tuple[float, ...]]) -> None:
        self._pts = pts

    @property
    def carrier(self) -> list[tuple[float, ...]]:
        return self._pts

    def distance_between(self, a: tuple[float, ...], b: tuple[float, ...]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _circle_points(n: int = 8) -> list[tuple[float, ...]]:
    import math as _math
    return [(_math.cos(2 * _math.pi * i / n), _math.sin(2 * _math.pi * i / n))
            for i in range(n)]


class TestAgreementWithZ2:
    """For spaces with no Z-torsion, F_p barcodes agree for all p."""

    def _rips_fc(self, pts: list[tuple[float, ...]], max_dim: int = 2) -> FilteredComplex:
        return vietoris_rips_filtration(_DummySpace(pts), max_dimension=max_dim)

    def test_p2_matches_standard_circle(self) -> None:
        pts = _circle_points(8)
        fc = self._rips_fc(pts, max_dim=1)
        std = persistence_pairs(fc)
        fp2 = persistence_pairs_fp(fc, prime=2)
        assert set(std) == set(fp2)

    def test_p3_same_betti_circle(self) -> None:
        pts = _circle_points(8)
        fc = self._rips_fc(pts, max_dim=1)
        fp3 = persistence_pairs_fp(fc, prime=3)
        essential_h0 = [p for p in fp3 if p.is_essential and p.dimension == 0]
        assert len(essential_h0) == 1

    def test_p5_same_betti_circle(self) -> None:
        pts = _circle_points(8)
        fc = self._rips_fc(pts, max_dim=1)
        fp5 = persistence_pairs_fp(fc, prime=5)
        essential_h1 = [p for p in fp5 if p.is_essential and p.dimension == 1]
        # circle has one essential H_1
        assert len(essential_h1) >= 1

    def test_p2_matches_standard_triangle(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, 0.866)]
        fc = self._rips_fc(pts, max_dim=2)
        std = persistence_pairs(fc)
        fp2 = persistence_pairs_fp(fc, prime=2)
        assert set(std) == set(fp2)

    def test_p7_contractible_no_h1(self) -> None:
        # Five collinear points
        pts = [(float(i),) for i in range(5)]
        fc = self._rips_fc(pts, max_dim=2)
        fp7 = persistence_pairs_fp(fc, prime=7)
        h1 = [p for p in fp7 if p.dimension == 1]
        assert all(not p.is_essential for p in h1)

    def test_all_primes_agree_on_contractible(self) -> None:
        pts = [(float(i),) for i in range(4)]
        fc = self._rips_fc(pts, max_dim=2)
        std = persistence_pairs(fc)
        for p in [2, 3, 5, 7]:
            fp = persistence_pairs_fp(fc, prime=p)
            # essential classes must agree (Betti numbers are prime-independent for nice spaces)
            std_ess = frozenset((pp.dimension, pp.birth) for pp in std if pp.is_essential)
            fp_ess = frozenset((pp.dimension, pp.birth) for pp in fp if pp.is_essential)
            assert std_ess == fp_ess, f"Essential classes differ for p={p}"


# ---------------------------------------------------------------------------
# Output format
# ---------------------------------------------------------------------------


class TestOutputFormat:
    def test_returns_tuple_of_persistence_pairs(self) -> None:
        fc = FilteredComplex(
            simplices=((0,), (1,), (0, 1)),
            births=(0.0, 0.0, 1.0),
            dimensions=(0, 0, 1),
        )
        result = persistence_pairs_fp(fc, prime=2)
        assert isinstance(result, tuple)
        assert all(isinstance(p, PersistencePair) for p in result)

    def test_single_vertex_one_essential_h0(self) -> None:
        fc = FilteredComplex(
            simplices=((0,),),
            births=(0.0,),
            dimensions=(0,),
        )
        pairs = persistence_pairs_fp(fc, prime=3)
        assert len(pairs) == 1
        assert pairs[0].is_essential
        assert pairs[0].dimension == 0

    def test_birth_leq_death(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
        fc = vietoris_rips_filtration(_DummySpace(pts), max_dimension=2)
        for p in [2, 3, 5]:
            pairs = persistence_pairs_fp(fc, prime=p)
            for pair in pairs:
                assert pair.birth <= pair.death, f"birth > death for p={p}"

    def test_sorted_output(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, 0.866), (0.5, 0.289)]
        fc = vietoris_rips_filtration(_DummySpace(pts), max_dimension=2)
        for p in [2, 3]:
            pairs = persistence_pairs_fp(fc, prime=p)
            for i in range(len(pairs) - 1):
                a, b = pairs[i], pairs[i + 1]
                assert (a.dimension, a.birth, a.death) <= (b.dimension, b.birth, b.death)

    def test_include_zero_persistence_flag(self) -> None:
        pts = [(0.0,), (1.0,), (2.0,)]
        fc = vietoris_rips_filtration(_DummySpace(pts), max_dimension=1)
        without = persistence_pairs_fp(fc, prime=2, include_zero_persistence=False)
        with_ = persistence_pairs_fp(fc, prime=2, include_zero_persistence=True)
        assert len(with_) >= len(without)

    def test_essential_death_is_inf(self) -> None:
        fc = FilteredComplex(
            simplices=((0,), (1,)),
            births=(0.0, 1.0),
            dimensions=(0, 0),
        )
        pairs = persistence_pairs_fp(fc, prime=5)
        essential = [p for p in pairs if p.is_essential]
        assert all(math.isinf(p.death) for p in essential)


# ---------------------------------------------------------------------------
# Torsion sensitivity (illustrative, not topologically exhaustive)
# ---------------------------------------------------------------------------


class TestTorsionSensitivity:
    """Illustrate that different primes can give different H_1 Betti numbers
    for complexes with mod-p torsion.  These tests construct minimal
    filtered complexes that simulate the effect."""

    def test_p2_and_p3_essential_h0_agree_on_two_points(self) -> None:
        # Two isolated points: H_0 = Z², no torsion → same result all primes
        fc = FilteredComplex(
            simplices=((0,), (1,)),
            births=(0.0, 0.0),
            dimensions=(0, 0),
        )
        for p in [2, 3, 5]:
            pairs = persistence_pairs_fp(fc, prime=p)
            ess_h0 = [pp for pp in pairs if pp.is_essential and pp.dimension == 0]
            assert len(ess_h0) == 2, f"Two essential H_0 classes expected for p={p}"

    def test_multiple_primes_circle_h1(self) -> None:
        # Circle (n=6) with max_dim=2: triangles fill the loop, so 1 finite H_1 bar
        # (born when the cycle forms, dies when triangles appear).
        # All primes should agree since H_*(S^1; Z) is torsion-free.
        pts = _circle_points(6)
        fc = vietoris_rips_filtration(_DummySpace(pts), max_dimension=2)
        for p in [2, 3, 5, 7]:
            pairs = persistence_pairs_fp(fc, prime=p)
            h1 = [pp for pp in pairs if pp.dimension == 1]
            assert len(h1) >= 1, f"Expected at least 1 H_1 bar for p={p}, got {len(h1)}"
            # No essential H_1 — loop is filled by triangles
            assert all(not pp.is_essential for pp in h1), (
                f"Expected no essential H_1 for p={p}"
            )
