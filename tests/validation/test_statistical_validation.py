"""
P16.3 Statistical Validation: random complexes vs an external oracle.

Generates random Erdős–Rényi 1-skeleta (5–50 vertices, edge probability 0.1–0.8),
computes H₀/H₁ with pytop, and cross-validates against **GUDHI** (whose
``SimplexTree`` ingests abstract simplicial complexes directly). Ripser is *not*
applicable here -- it consumes point clouds / distance matrices, not abstract
complexes -- so Ripser parity lives in ``test_betti_parity.py`` on genuine point
clouds instead.

Two tests:
- ``test_500_random_complexes_gudhi_parity`` runs by default and asserts pytop ==
  GUDHI on 500 complexes whenever GUDHI is installed (skipped otherwise). This is
  the always-on cross-validation guard.
- ``test_10k_random_complexes_vs_oracles`` is the opt-in heavy run (10K complexes)
  that also writes ``statistical_validation_report.json``.

Produces statistical parity report, residual error distribution, and outlier analysis.

Usage (opt-in heavy run, CPU-intensive):
    PYTOP_STATISTICAL_VALIDATION=1 pytest tests/validation/test_statistical_validation.py -v --tb=short
"""

from __future__ import annotations

import json
import os
import random
import time
from dataclasses import dataclass, field
from typing import NamedTuple, Optional

import pytest

from pytop import SimplicialComplex, simplicial_homology


class HomologyPair(NamedTuple):
    """Homology groups H₀ and H₁."""
    h0_betti: int
    h0_torsion: tuple[int, ...]
    h1_betti: int
    h1_torsion: tuple[int, ...]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HomologyPair):
            return NotImplemented
        return (
            self.h0_betti == other.h0_betti
            and self.h0_torsion == other.h0_torsion
            and self.h1_betti == other.h1_betti
            and self.h1_torsion == other.h1_torsion
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "h0_betti": self.h0_betti,
            "h0_torsion": list(self.h0_torsion),
            "h1_betti": self.h1_betti,
            "h1_torsion": list(self.h1_torsion),
        }


@dataclass(frozen=True)
class RandomComplexResult:
    """Statistical validation result for one random complex."""

    complex_id: int
    num_vertices: int
    num_edges: int
    num_simplices: int
    pytop: HomologyPair
    gudhi: Optional[HomologyPair] = None
    ripser: Optional[HomologyPair] = None
    agrees_gudhi: Optional[bool] = None
    agrees_ripser: Optional[bool] = None
    computation_time_ms: float = 0.0

    def to_dict(self) -> dict[str, object]:
        result = {
            "complex_id": self.complex_id,
            "num_vertices": self.num_vertices,
            "num_edges": self.num_edges,
            "num_simplices": self.num_simplices,
            "pytop": self.pytop.to_dict(),
            "computation_time_ms": self.computation_time_ms,
        }
        if self.gudhi is not None:
            result["gudhi"] = self.gudhi.to_dict()
            result["agrees_gudhi"] = self.agrees_gudhi
        if self.ripser is not None:
            result["ripser"] = self.ripser.to_dict()
            result["agrees_ripser"] = self.agrees_ripser
        return result


@dataclass
class StatisticalReport:
    """Aggregated statistical validation report."""

    total_complexes: int
    num_with_gudhi: int = 0
    num_with_ripser: int = 0
    gudhi_parity_pct: float = 0.0
    ripser_parity_pct: float = 0.0
    outliers_gudhi: list[int] = field(default_factory=list)
    outliers_ripser: list[int] = field(default_factory=list)
    vertex_count_stats: dict[str, float] = field(default_factory=dict)
    edge_count_stats: dict[str, float] = field(default_factory=dict)
    computation_time_stats_ms: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "total_complexes": self.total_complexes,
            "num_with_gudhi": self.num_with_gudhi,
            "num_with_ripser": self.num_with_ripser,
            "gudhi_parity_pct": round(self.gudhi_parity_pct, 1),
            "ripser_parity_pct": round(self.ripser_parity_pct, 1),
            "outliers_gudhi_count": len(self.outliers_gudhi),
            "outliers_ripser_count": len(self.outliers_ripser),
            "vertex_count_stats": {
                k: round(v, 1) for k, v in self.vertex_count_stats.items()
            },
            "edge_count_stats": {
                k: round(v, 1) for k, v in self.edge_count_stats.items()
            },
            "computation_time_stats_ms": {
                k: round(v, 2) for k, v in self.computation_time_stats_ms.items()
            },
        }


def generate_erdos_renyi_1skeleton(
    num_vertices: int, edge_probability: float, seed: Optional[int] = None
) -> list[list[int]]:
    """
    Generate a random Erdős–Rényi 1-skeleton (vertices + edges).

    Args:
        num_vertices: Number of vertices (typically 5–50).
        edge_probability: Probability of edge inclusion (typically 0.1–0.8).
        seed: Optional random seed for reproducibility.

    Returns:
        List of simplices (1-simplices, i.e., vertices and edges).
    """
    if seed is not None:
        random.seed(seed)

    simplices: list[list[int]] = [[v] for v in range(num_vertices)]

    for u in range(num_vertices):
        for v in range(u + 1, num_vertices):
            if random.random() < edge_probability:
                simplices.append([u, v])

    return simplices


def compute_gudhi_homology(
    simplices: list[list[int]],
) -> Optional[HomologyPair]:
    """
    Compute homology using GUDHI oracle (if available).

    Args:
        simplices: List of simplices.

    Returns:
        HomologyPair if GUDHI is available and computation succeeds, None otherwise.
    """
    try:
        import gudhi  # noqa: F401
    except ImportError:
        return None

    try:
        import gudhi

        sc = gudhi.SimplexTree()
        for simplex in simplices:
            sc.insert(simplex)

        # persistence_dim_max=True is REQUIRED so GUDHI computes homology in the
        # complex's *top* dimension. For a 1-skeleton that top dimension is H1 --
        # with the default persistence_dim_max=False GUDHI silently skips the top
        # dimension and reports H1 = 0, disagreeing with pytop on every graph
        # that contains a cycle. betti_numbers() then returns the static Betti
        # numbers of the whole complex (essential classes have infinite bars).
        sc.compute_persistence(persistence_dim_max=True)
        betti = sc.betti_numbers()

        return HomologyPair(
            h0_betti=betti[0] if len(betti) > 0 else 0,
            h0_torsion=(),
            h1_betti=betti[1] if len(betti) > 1 else 0,
            h1_torsion=(),
        )
    except Exception:
        return None


def compute_ripser_homology(
    simplices: list[list[int]],
) -> Optional[HomologyPair]:
    """
    Ripser is NOT an applicable oracle for an abstract 1-skeleton.

    Ripser computes Vietoris-Rips persistent homology from a *point cloud* or a
    *distance matrix*; it has no API to ingest a hand-built abstract simplicial
    complex. Forcing the random ER graph into a distance matrix would change the
    space (the Rips complex of that matrix is not the original 1-skeleton), so
    the comparison would be meaningless. We therefore return None here and rely
    on GUDHI's SimplexTree (which *does* accept abstract complexes) for the
    1-skeleton cross-check. Ripser parity against pytop on genuine point clouds
    lives in ``betti_parity.py`` / ``test_betti_parity.py`` instead.

    Returns:
        Always None (not applicable).
    """
    return None


class TestStatisticalValidation:
    """P16.3: 10K random Erdős–Rényi 1-skeleta vs GUDHI/Ripser."""

    @pytest.mark.skipif(
        os.environ.get("PYTOP_STATISTICAL_VALIDATION") != "1",
        reason="Set PYTOP_STATISTICAL_VALIDATION=1 to run (10K complexes, ~10–30 min)",
    )
    def test_10k_random_complexes_vs_oracles(self) -> None:
        """Generate 10K random ER 1-skeleta, validate pytop homology vs GUDHI/Ripser."""
        num_complexes = 10000
        results: list[RandomComplexResult] = []

        start_time = time.perf_counter()

        for i in range(num_complexes):
            num_vertices = random.randint(5, 50)
            edge_prob = random.uniform(0.1, 0.8)

            simplices = generate_erdos_renyi_1skeleton(num_vertices, edge_prob)
            num_edges = len([s for s in simplices if len(s) == 2])

            cplx_start = time.perf_counter()
            sc = SimplicialComplex(simplices)
            h0_result = simplicial_homology(sc, degree=0)
            h1_result = simplicial_homology(sc, degree=1)
            cplx_elapsed = (time.perf_counter() - cplx_start) * 1000

            pytop_pair = HomologyPair(
                h0_betti=h0_result.betti,
                h0_torsion=h0_result.torsion,
                h1_betti=h1_result.betti,
                h1_torsion=h1_result.torsion,
            )

            gudhi_pair = compute_gudhi_homology(simplices)
            ripser_pair = compute_ripser_homology(simplices)

            agrees_gudhi = (
                gudhi_pair == pytop_pair if gudhi_pair is not None else None
            )
            agrees_ripser = (
                ripser_pair == pytop_pair if ripser_pair is not None else None
            )

            result = RandomComplexResult(
                complex_id=i,
                num_vertices=num_vertices,
                num_edges=num_edges,
                num_simplices=len(simplices),
                pytop=pytop_pair,
                gudhi=gudhi_pair,
                ripser=ripser_pair,
                agrees_gudhi=agrees_gudhi,
                agrees_ripser=agrees_ripser,
                computation_time_ms=cplx_elapsed,
            )
            results.append(result)

            if (i + 1) % 1000 == 0:
                elapsed = time.perf_counter() - start_time
                print(
                    f"\n  [{i+1}/{num_complexes}] {elapsed:.1f}s elapsed, "
                    f"GUDHI={'OK' if gudhi_pair else '--'}, "
                    f"Ripser={'OK' if ripser_pair else '--'}"
                )

        total_elapsed = time.perf_counter() - start_time

        with_gudhi = [r for r in results if r.agrees_gudhi is not None]
        with_ripser = [r for r in results if r.agrees_ripser is not None]

        gudhi_agree = sum(1 for r in with_gudhi if r.agrees_gudhi)
        ripser_agree = sum(1 for r in with_ripser if r.agrees_ripser)

        gudhi_pct = (gudhi_agree / len(with_gudhi) * 100) if with_gudhi else 0.0
        ripser_pct = (ripser_agree / len(with_ripser) * 100) if with_ripser else 0.0

        outliers_gudhi = [r.complex_id for r in with_gudhi if not r.agrees_gudhi]
        outliers_ripser = [r.complex_id for r in with_ripser if not r.agrees_ripser]

        vertex_counts = [r.num_vertices for r in results]
        edge_counts = [r.num_edges for r in results]
        comp_times = [r.computation_time_ms for r in results]

        report = StatisticalReport(
            total_complexes=num_complexes,
            num_with_gudhi=len(with_gudhi),
            num_with_ripser=len(with_ripser),
            gudhi_parity_pct=gudhi_pct,
            ripser_parity_pct=ripser_pct,
            outliers_gudhi=outliers_gudhi[:10],
            outliers_ripser=outliers_ripser[:10],
            vertex_count_stats={
                "min": min(vertex_counts),
                "max": max(vertex_counts),
                "mean": sum(vertex_counts) / len(vertex_counts),
            },
            edge_count_stats={
                "min": min(edge_counts),
                "max": max(edge_counts),
                "mean": sum(edge_counts) / len(edge_counts),
            },
            computation_time_stats_ms={
                "min": min(comp_times),
                "max": max(comp_times),
                "mean": sum(comp_times) / len(comp_times),
            },
        )

        print("\n" + "=" * 70)
        print("P16.3 STATISTICAL VALIDATION REPORT")
        print("=" * 70)
        print(f"\nTotal random ER 1-skeleta: {num_complexes:,}")
        print(f"Total elapsed time: {total_elapsed:.1f}s")
        print("\nOracleAvailability:")
        print(f"  GUDHI: {len(with_gudhi):,}/{num_complexes} ({len(with_gudhi)/num_complexes*100:.1f}%)")
        print(f"  Ripser: {len(with_ripser):,}/{num_complexes} ({len(with_ripser)/num_complexes*100:.1f}%)")
        print("\nParity (pytop = oracle):")
        print(f"  GUDHI: {gudhi_agree}/{len(with_gudhi)} ({gudhi_pct:.1f}%)")
        print(f"  Ripser: {ripser_agree}/{len(with_ripser)} ({ripser_pct:.1f}%)")
        print(f"\nOutliers (first 10 of {len(outliers_gudhi)} GUDHI, {len(outliers_ripser)} Ripser):")
        print(f"  GUDHI: {outliers_gudhi}")
        print(f"  Ripser: {outliers_ripser}")
        print("\nComplex statistics:")
        print(f"  Vertices: min={report.vertex_count_stats['min']}, "
              f"max={report.vertex_count_stats['max']}, "
              f"mean={report.vertex_count_stats['mean']:.1f}")
        print(f"  Edges: min={report.edge_count_stats['min']}, "
              f"max={report.edge_count_stats['max']}, "
              f"mean={report.edge_count_stats['mean']:.1f}")
        print(f"  Computation time: min={report.computation_time_stats_ms['min']:.2f}ms, "
              f"max={report.computation_time_stats_ms['max']:.2f}ms, "
              f"mean={report.computation_time_stats_ms['mean']:.2f}ms")
        print("=" * 70)

        report_dict = report.to_dict()
        report_path = "tests/validation/statistical_validation_report.json"
        with open(report_path, "w") as f:
            json.dump(report_dict, f, indent=2)
        print(f"\nReport saved to: {report_path}")

        assert (
            gudhi_pct >= 95.0 or len(with_gudhi) == 0
        ), f"GUDHI parity {gudhi_pct:.1f}% < 95% threshold"
        assert (
            ripser_pct >= 95.0 or len(with_ripser) == 0
        ), f"Ripser parity {ripser_pct:.1f}% < 95% threshold"

    def test_500_random_complexes_gudhi_parity(self) -> None:
        """Always-on cross-validation: pytop H₀/H₁ == GUDHI on 500 random ER 1-skeleta.

        Skipped only when GUDHI is not installed. This is the real external-oracle
        guard that was previously "pending" (the heavy 10K run had num_with_gudhi=0).
        """
        pytest.importorskip("gudhi")

        rng = random.Random(20260623)
        num_complexes = 500
        checked = 0
        disagreements: list[tuple[int, HomologyPair, HomologyPair]] = []

        for i in range(num_complexes):
            num_vertices = rng.randint(5, 50)
            edge_prob = rng.uniform(0.1, 0.8)
            # Deterministic per-complex seed so failures are reproducible.
            random.seed(i * 7919 + 13)
            simplices = generate_erdos_renyi_1skeleton(num_vertices, edge_prob)

            sc = SimplicialComplex(simplices)
            h0 = simplicial_homology(sc, degree=0)
            h1 = simplicial_homology(sc, degree=1)
            pytop_pair = HomologyPair(h0.betti, h0.torsion, h1.betti, h1.torsion)

            gudhi_pair = compute_gudhi_homology(simplices)
            assert gudhi_pair is not None, "GUDHI importable but returned None"
            checked += 1
            if gudhi_pair != pytop_pair:
                disagreements.append((i, pytop_pair, gudhi_pair))

        assert checked == num_complexes
        assert not disagreements, (
            f"pytop vs GUDHI disagreed on {len(disagreements)}/{num_complexes} "
            f"complexes; first few: {disagreements[:5]}"
        )

    def test_small_sample_validation(self) -> None:
        """Quick smoke test: 10 random complexes with pytop only."""
        results: list[RandomComplexResult] = []

        for i in range(10):
            num_vertices = random.randint(5, 20)
            edge_prob = random.uniform(0.2, 0.7)

            simplices = generate_erdos_renyi_1skeleton(num_vertices, edge_prob)

            sc = SimplicialComplex(simplices)
            h0_result = simplicial_homology(sc, degree=0)
            h1_result = simplicial_homology(sc, degree=1)

            pytop_pair = HomologyPair(
                h0_betti=h0_result.betti,
                h0_torsion=h0_result.torsion,
                h1_betti=h1_result.betti,
                h1_torsion=h1_result.torsion,
            )

            result = RandomComplexResult(
                complex_id=i,
                num_vertices=num_vertices,
                num_edges=len([s for s in simplices if len(s) == 2]),
                num_simplices=len(simplices),
                pytop=pytop_pair,
            )
            results.append(result)

        assert len(results) == 10
        for r in results:
            assert r.num_vertices >= 5
            assert r.num_simplices >= r.num_edges + r.num_vertices


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
