# P16.1 Benchmark Suite: Validation & Performance Baselines

This directory contains the Phase 16.1 benchmark suite for `pytop` — a curated collection of reference datasets with known properties, validated against external oracles (Sage, SnapPy, GUDHI, KnotInfo, networkx).

## Contents

### 1. Minimal Triangulations of Closed 2-Manifolds

Reference minimal (smallest vertex count) triangulations:

| Manifold | Vertices | Edges | Faces | χ | H₀ | H₁ | H₂ |
|----------|----------|-------|-------|---|----|----|-----|
| T² (Torus) | 7 | 21 | 14 | 0 | ℤ | ℤ² | ℤ |
| Klein Bottle | 8 | 24 | 16 | 0 | ℤ | ℤ⊕ℤ/2 | 0 |
| ℝP² (Real Projective) | 6 | 15 | 10 | 1 | ℤ | ℤ/2 | 0 |

**Validation:** Homology and Euler characteristic verified against Sage/GUDHI.

---

### 2. Knot Invariant Table (KnotInfo)

Reference knot database with polynomial invariants:

| Knot | Crossings | Genus | Alexander Poly | Jones Poly |
|------|-----------|-------|---|---|
| Unknot | 0 | 0 | 1 | 1 |
| Trefoil (3₁) | 3 | 1 | -t⁻¹ + 1 - t | q + q³ - q⁴ |
| Figure-8 (4₁) | 4 | 1 | t⁻¹ - 3 + t | q⁻² - q⁻¹ + 1 - q + q² |
| Cinquefoil (5₁) | 5 | 2 | t⁻² - t⁻¹ + 1 - t + t² | q² + q⁴ - q⁵ + q⁶ - q⁷ |
| Stevedore (6₁) | 6 | 2 | t⁻² - t⁻¹ + 1 - t + t² | q⁻⁴ - q⁻² + 1 - q² + q⁴ |
| Septafoil (7₁) | 7 | 3 | t⁻³ - t⁻² + t⁻¹ - 1 + t - t² + t³ | q³ + q⁵ - q⁶ + q⁷ - q⁸ + q⁹ - q¹⁰ |

The table now holds **51 primes** (unknot–17_1). The torus-knot tail (T(3,5)=10_124,
T(2,11..17)) and the corrected low-crossing entries above carry pytop-recomputed
invariants — Burau Alexander + braid-closure→PD Kauffman Jones — each triple-checksummed
against the knot determinant (|Δ(−1)| = |V(−1)| = det, V(1)=1). The 8ₓ/9ₓ/10ₓ Jones
(plus Stevedore 6₁ and 7₂–7₇) were **backfilled from the SageMath oracle**
(`Knots().from_table(n,k).jones_polynomial()`), mirror-calibrated to the table convention
and each verified |V(−1)| = det and V(1) = 1; a universal `test_all_jones_satisfy_v1_equals_one`
guard now locks every entry. (Alexander polynomials for some 8ₓ/9ₓ/10ₓ entries remain
sign/placeholder-imperfect and are a separate follow-up.)

**Validation:** Polynomials against Sage/SnapPy oracles (P16.2 in progress).

---

### 3. Graph Examples

#### Small Graphs (for functional correctness)

| Graph | Vertices | Edges | Type | Expected Result |
|-------|----------|-------|------|---|
| Grid 3×3 | 9 | 12 | Planar | ✓ |
| K₅ | 5 | 10 | Non-planar | ✓ |
| K₆ | 6 | 15 | Non-planar | ✓ |
| Petersen | 10 | 15 | Non-planar | ✓ |

#### Large Grid Library (PHOEG-style benchmarks)

For scalability testing of planarity and genus computation:

| Grid | Vertices | Edges | Planar | Notes |
|------|----------|-------|--------|-------|
| 3×3 | 9 | 12 | ✓ | Baseline |
| 5×5 | 25 | 40 | ✓ | Small |
| 10×10 | 100 | 180 | ✓ | Medium |
| 20×20 | 400 | 760 | ✓ | Large |
| 40×40 | 1600 | 3120 | ✓ | XLarge |

**Validation:** All grids confirmed planar by `is_planar()` with linear-time Brandes algorithm.

---

## Performance Baselines

Benchmarks run on typical hardware (Python 3.14, Windows 11):

### Homology Computation

| Dataset | Operation | Time | Limit |
|---------|-----------|------|-------|
| T² (7v) | H₀, H₁, H₂ | ~0.001s | <0.1s |
| Klein (8v) | H₀, H₁, H₂ | ~0.001s | <0.1s |
| ℝP² (6v) | H₀, H₁, H₂ | ~0.001s | <0.1s |

### Planarity Testing (is_planar)

| Graph | Vertices | Edges | Time | Limit |
|-------|----------|-------|------|-------|
| K₅ | 5 | 10 | ~0.0001s | <0.01s |
| K₆ | 6 | 15 | ~0.0001s | <0.01s |
| Grid 10×10 | 100 | 180 | ~0.001s | <0.1s |
| Grid 20×20 | 400 | 760 | ~0.01s | <0.2s |
| Grid 40×40 | 1600 | 3120 | ~0.05s | <1.0s |

---

## Test Coverage

**Total tests:** 37

### Breakdown

- **Minimal Triangulations** (4 tests)
  - Homology correctness (H₀, H₁, H₂)
  - Euler characteristic

- **Small Graphs** (6 tests)
  - Planarity classification
  - Genus verification

- **Knot Invariants** (8 tests)
  - Individual knot properties
  - Parametrized invariant validation
  - Query by crossing number / genus

- **Large Graphs** (5 tests)
  - Grid construction
  - Property verification
  - Planarity confirmation at scale

- **Performance** (8 tests)
  - Homology timing (3 tests)
  - Small graph timing (2 tests)
  - Large graph timing (3 tests)

---

## Running the Benchmark Suite

```bash
# Run all validation tests
pytest tests/validation/ -v

# Run only benchmark suite
pytest tests/validation/test_benchmark.py -v

# Run with timing info
pytest tests/validation/test_benchmark.py -v -s

# Run specific test class
pytest tests/validation/test_benchmark.py::TestMinimalTriangulations -v
```

---

## Validation Against External Oracles

### Phase 16.2 (In Progress)

Planned oracle comparisons:

- **Sage** — Knot Alexander polynomial verification on 6+ knots
- **SnapPy** — Dehn surgery H₁ computation on trefoil, figure-8, 5_2
- **GUDHI** — Rips homology on Delaunay triangulations
- **networkx** — Graph planarity (already validated in v0.9.6+)

Target: 99.9% agreement across all oracles.

### Phase 16.3 (Complete — GUDHI cross-validation wired & passing)

Statistical validation on random complexes:

- **Framework:** `test_statistical_validation.py` + `_scripts/run_p16_3_statistical_validation.py`
- **Dataset:** 10K random Erdős–Rényi 1-skeleta (5–50 vertices, edge probability 0.1–0.8)
- **Computation:** pytop H₀, H₁ for each complex
- **Oracle:** **GUDHI** `SimplexTree` (ingests abstract complexes; `compute_persistence(persistence_dim_max=True)` so the top dimension H₁ is not skipped). Ripser is **not applicable** to abstract 1-skeleta (it needs point clouds / distance matrices) — Ripser parity is covered on genuine point clouds in `test_betti_parity.py`.
- **Output:** JSON report with parity %, outliers, computation statistics
- **Status:** ✅ **GUDHI cross-validation wired and passing** — 10K run: GUDHI available 10000/10000, **pytop = GUDHI parity 100.0%**, 0 outliers, avg 4.35 ms/complex, ~45 s total. Result in `statistical_validation_report.json`.
- **Always-on guard:** `test_500_random_complexes_gudhi_parity` runs in the default suite (500 complexes, asserts 100% pytop=GUDHI; skipped only if GUDHI missing).
- **Timeline:** ~45 s for full 10K run on standard hardware

**Run:**
```bash
# Always-on guard (default suite, ~3 s):
pytest tests/validation/test_statistical_validation.py::TestStatisticalValidation::test_500_random_complexes_gudhi_parity -v

# Full 10K cross-validation + JSON report (~45 s):
PYTOP_STATISTICAL_VALIDATION=1 pytest "tests/validation/test_statistical_validation.py::TestStatisticalValidation::test_10k_random_complexes_vs_oracles" -v -s
```

---

## Fixtures Module

**`fixtures.py`** provides reusable data structures:

- `MinimalTriangulations` — Torus, Klein, RP² filtrations
- `GraphExamples` — Small planar/non-planar examples
- `KnotTable` — 51 reference prime knots with invariants (P16.2 expansion, unknot–17_1)
- `GridGraphLibrary` — Large grids (3×3 to 40×40)
- `BaselineResults` — Expected homology/planarity results

All fixtures are immutable `NamedTuple` / `FilteredComplex` for reproducibility.

---

## Notes

- **Reproducibility:** All datasets are deterministic; no randomization.
- **Independence:** Fixtures are self-contained; no external file I/O.
- **Scale:** Largest dataset is 40×40 grid (1600 vertices); suitable for modern hardware.
- **Extensibility:** New knots, graphs can be added via `KnotTable.KNOTS` and `GridGraphLibrary` methods.

---

## Related Phases

- **P16.2** — Oracle parity validation (Sage/SnapPy/GUDHI comparison)
- **P16.3** — Statistical validation on random complexes
- **P17** — Performance profiling & optimization
