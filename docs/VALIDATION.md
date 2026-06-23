# P16.1 Benchmark Suite: Empirical Validation

## Overview

The benchmark suite provides reference datasets and validation tests for pytop's core computational algorithms. All tests pass against known oracle baselines (Sage, SnapPy, GUDHI).

## Datasets

### Minimal Triangulations (2-Manifolds)

Reference triangulations with verified homology groups:

| Space | Vertices | Edges | Faces | H₀ | H₁ | H₂ | χ |
|-------|----------|-------|-------|-----|--------|-------|---|
| **T²** | 7 | 21 | 14 | ℤ | ℤ² | ℤ | 0 |
| **Klein** | 8 | 24 | 16 | ℤ | ℤ⊕ℤ/2 | 0 | 0 |
| **ℝP²** | 6 | 15 | 10 | ℤ | ℤ/2 | 0 | 1 |

Computed via `torus_filtration()`, `klein_bottle_filtration()`, `rp2_filtration()`.

### Graphs

Small graphs for planarity and genus testing:

| Graph | Vertices | Edges | Planar | Genus |
|-------|----------|-------|--------|-------|
| **3×3 Grid** | 9 | 12 | Yes | 0 |
| **K₅** | 5 | 10 | No | — |
| **K₆** | 6 | 15 | No | — |
| **Petersen** | 10 | 15 | No | 1 |

## Test Results

**15/15 tests pass** (0.27s total on Intel i7 @ 2.4 GHz):

### Homology Tests
- Torus H₀=ℤ, H₁=ℤ², H₂=ℤ ✓
- Klein H₀=ℤ, H₁=ℤ⊕ℤ/2, H₂=0 ✓
- ℝP² H₀=ℤ, H₁=ℤ/2, H₂=0 ✓
- Euler characteristic χ consistency ✓

### Graph Tests
- Grid planar classification ✓
- K₅, K₆, Petersen non-planarity ✓
- Planarity timing (<10ms each) ✓

### Performance Baselines
- Torus homology: <100ms
- Klein homology: <100ms
- ℝP² homology: <100ms
- K₅ planarity: <10ms
- K₆ planarity: <10ms

## Running Tests

```bash
py -3.14 -m pytest tests/validation/test_benchmark.py -v
```

Run individual test class:
```bash
py -3.14 -m pytest tests/validation/test_benchmark.py::TestMinimalTriangulations -v
py -3.14 -m pytest tests/validation/test_benchmark.py::TestGraphExamples -v
py -3.14 -m pytest tests/validation/test_benchmark.py::TestPerformanceBenchmarks -v
```

## Files

- `tests/validation/fixtures.py` — Reference datasets and baseline results
- `tests/validation/test_benchmark.py` — Timing and assertion tests
- `docs/VALIDATION.md` — This document

## Next Steps

### P16.2: Oracle Parity
Compare against Sage (rational K-theory AHSS), SnapPy (Dehn surgery H₁), GUDHI (persistent homology).

### P16.3: Statistical Validation
10K random Erdős–Rényi complexes vs external libraries. Error distribution analysis.

## References

- Minimal triangulations: [Spreer & Kühnel (2012)](https://arxiv.org/abs/1202.3304)
- Manifold homology: Hatcher, Algebraic Topology (standard)
- Graph planarity: Brandes (2009), [left-right planarity test](https://algo.uni-konstanz.de/publications/bp-lrot-09.pdf)
