# Phase 17 P17.3: Scaling (Construction Optimization + Auto Reduction Routing)

**Status:** ✅ Core scaling wins shipped — **(1)** inductive Rips construction (build phase)
and **(2)** size-aware auto reduction routing (reduce phase, now the default).  
**Date:** 2026-06-24  
**Target:** Rips n=500 in <1s (current ~5.1s with n=350)  
**Challenge:** Reduction algorithms are inherently sequential — addressed by *choosing*
the right sequential algorithm per input size rather than parallelizing one.

## Shipped: size-aware auto reduction routing (`method="auto"`, now default)

Profiling overturned the planned Strategy 3 (scipy CSR sparse acceleration): the
Z/2 reduction already uses a **bigint bitmask** column representation whose XOR is
a native C-level integer op, so a SciPy CSR layer adds overhead without beating it.
The genuine win was already in the codebase but off the default path — the de Silva
dual **cohomology** reduction performs *hundreds* of cochain additions where Twist
performs *millions* of column XORs on Rips filtrations:

| m (simplices) | Twist XORs | cohomology XORs | reduce speedup |
|---------------|-----------|-----------------|----------------|
| 7,273  (n=100) | 47,247 | 151 | 1.51× |
| 55,333 (n=200) | 789,091 | 331 | 2.81× |
| 107,615 (n=250)| 1,807,781 | 399 | 3.83× |

Twist still wins on *tiny* complexes (lower constant factor): measured crossover is
broad and flat between m≈520 (Twist faster) and m≈2,850 (cohomology faster). So
`persistence_pairs_auto` routes on materialized complex size with a threshold of
**1,024 simplices** (`AUTO_COHOMOLOGY_THRESHOLD`), and `persistent_homology(method="auto")`
is now the **default**. Output is **byte-identical** to Twist / cohomology / standard
on every input — a universal cross-validation test enforces this, and the full suite
(11,921 tests) plus the GUDHI parity validation suite pass unchanged.

**Measured end-to-end speedup (old `method="twist"` → new `method="auto"`, identical output):**

| n   | twist (old default) | auto (new default) | speedup |
|-----|---------------------|--------------------|---------|
| 150 | 147 ms | 85 ms | 1.7× |
| 250 | 1,411 ms | 422 ms | 3.3× |
| 350 | 22,426 ms | 1,843 ms | **12.2×** |

New public API: `persistence_pairs_auto`, `select_reduction_method`,
`AUTO_COHOMOLOGY_THRESHOLD` (`pytop.persistent_homology_optimized`).

**Remaining bottleneck:** for very dense, high-`n` complexes the *filtration build*
becomes co-dominant again (e.g. n=500 dense: build 2.3 s of 5.6 s total). Pushing
n=500 fully under 1 s at high density needs either cheaper construction or the GPU
cohomology path (Strategy 2) — tracked for P17.4 / future phases.

## Earlier win: inductive Vietoris–Rips construction (filtration build, not reduction)

## Shipped: Inductive Vietoris–Rips construction (filtration build, not reduction)

Profiling the end-to-end pipeline split the wall-clock between two phases and
**overturned the earlier assumption that reduction is the sole bottleneck**: in
the truncated-filtration regime (a finite `max_scale`, the usual TDA case) the
*filtration construction* dominated.

| n   | old build (C(n,k+1) enum) | reduction | construction share |
|-----|---------------------------|-----------|--------------------|
| 100 | 0.171s | 0.014s | 92% |
| 150 | 0.621s | 0.090s | 87% |
| 200 | 1.355s | 0.240s | 85% |

The old `vietoris_rips_filtration` enumerated **every** `C(n, k+1)` vertex subset
up to `max_dimension` and computed each diameter before discarding those past
`max_scale`. Replaced with **inductive clique expansion** (Zomorodian 2010): build
the neighborhood graph of edges within `max_scale`, then grow each simplex exactly
once by intersecting lower-neighbor sets, carrying the diameter incrementally. Work
now scales with the size of the *materialized* complex, not `C(n, k+1)`.

**Measured speedup (build only, `max_dimension=2`, `max_scale=1.0`, Gaussian cloud):**

| n   | old build | new build | speedup |
|-----|-----------|-----------|---------|
| 100 | 0.173s | 0.009s | 18.9× |
| 200 | 1.389s | 0.071s | 19.5× |
| 300 | 5.148s | 0.358s | 14.4× |
| 500 | 22.703s | 1.649s | 13.8× |

Output is **byte-identical** to the previous construction (same simplices, births,
dimensions, and sort order) — verified against a brute-force reference across
`max_dimension ∈ {0,1,2,3}` and `max_scale ∈ {0.8, 1.5, None}` in
`tests/core/test_persistent_homology_engine.py`, and confirmed by the full 11,874
test suite. No API change.

**Remaining bottleneck:** for dense, high-`n` complexes the **Z/2 reduction** is now
the dominant cost (and is inherently sequential, as analyzed below). The next P17.3
increment targets the reduction via the strategies below.

## Current Performance Baseline

Single-threaded Rips persistent homology (Twist + bigint bitmask):

| Points | Time | Simplices | Complexity Notes |
|--------|------|-----------|-----------------|
| 100 | 0.162s | 5,050 | O(m²) regime |
| 200 | 0.599s | 20,100 | O(m²) → O(m³) transition |
| 250 | 1.003s | 31,375 | O(m³) scaling visible |
| 300 | 1.823s | 45,150 | O(m³) super-cubic |
| 350 | 5.133s | 61,075 | m³ dominance (~5 seconds) |

**Analysis:** Wall-clock time is dominated by Z/2 reduction, which is **inherently sequential**:
- Left-to-right pivot-seeking (finding low(j) for each column)
- Each column reduce depends on prior columns
- Cannot parallelize reduction loop without significant architectural changes

## Parallelization Strategies: Trade-offs

### Strategy 1: Dimension Decomposition (Limited Benefit)
Compute H₀, H₁, H₂ independently per dimension:
- **Pro:** No algorithmic changes; straightforward ProcessPoolExecutor mapping
- **Con:** Modest speedup (~1.5–2×) since H₁ is the bottleneck on 2D Rips
- **Overhead:** Process spawn + IPC for large matrices

### Strategy 2: GPU Cohomology (Requires CuPy)
Incremental cocycle algorithm maps to GPU:
- **Pro:** Cocycle updates are parallel element-wise operations
- **Con:** Requires CuPy + CUDA; only effective for very large complexes (>100K simplices)
- **Overhead:** GPU memory transfer, kernel launch

### Strategy 3: Sparse Matrix Acceleration (Recommended for P17.3)
Pre-optimize matrix representation:
- Use CSR (Compressed Sparse Row) format for boundary matrix
- Parallelize sparse matrix × vector products
- Leverage NumPy/SciPy optimized BLAS
- **Effect:** 2–3× speedup without changing algorithm

**Decision for P17.3:** ~~Implement Strategy 3 (sparse optimization)~~ **— superseded.**
Profiling showed the bigint-bitmask Twist kernel already beats a SciPy CSR layer (native
integer XOR), so Strategy 3 was dropped in favor of **size-aware auto routing to the de
Silva dual cohomology reduction** (see the "size-aware auto reduction routing" section at
the top of this document — the actual shipped work). Strategies 1 & 2 remain documented for
future phases.

## P17.3 Deliverables

### 1. Sparse Matrix Infrastructure
Add optional CSR format for boundary operators:

```python
from pytop.persistent_homology_optimized import persistence_pairs_sparse

# Use sparse matrix representation (automatic if >1000 simplices)
pairs = persistence_pairs_sparse(filtered, use_sparse=True)
```

**Implementation plan:**
- Detect dense vs sparse regime (threshold: ~500 simplices)
- Build CSR matrix in `_build_columns_sparse()`
- Reuse same Twist reduction kernel with sparse operations
- Fall back to dense for small complexes

### 2. Multi-Core Benchmark Framework
Harness to measure scaling efficiency:

```python
from pytop._internal.benchmark_runner import parallel_benchmark

results = parallel_benchmark(
    n_points_range=[100, 200, 300, 400],
    n_cores=[1, 2, 4, 8],
    n_trials=3
)
# → CSV with: (n_points, n_cores, wall_time, memory, speedup)
```

### 3. Scaling Reports
Generate before/after plots:
- Wall-clock vs cores (1–8 cores)
- Memory overhead per core
- Speedup vs theoretical max
- Identify saturation point

### 4. GPU Infrastructure (Skeleton)
Placeholder for future CuPy integration:

```python
# pytop/persistent_homology_gpu.py
def persistence_pairs_cohomology_gpu(
    filtered: FilteredComplex,
    device: str = "cuda:0"
) -> tuple[PersistencePair, ...]:
    """Persistent cohomology on GPU via CuPy (requires [gpu] extra)."""
    try:
        import cupy as cp
    except ImportError:
        raise RuntimeError(
            "GPU cohomology requires pytop[gpu]; install with: "
            "pip install pytop[gpu]"
        )
    # Implementation skeleton for future phases
```

## Realistic Scaling Target

Given the sequential nature of column reduction:

**Conservative estimate (Twist + sparse):
- 1-core baseline (n=350): 5.1s
- 2-core (dimension decomp): ~3–4s (1.3–1.7× speedup)
- 4-core (fine-grained): ~2–3s (realistic plateau)
- GPU (cohomology): ~0.5–1s on large complexes

**P17.3 Goal:** Demonstrate infrastructure; achieve 1.5–2× speedup through sparse optimization.

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Reduction inherently sequential | Hard ceiling on parallelization | Document; use for complex-building instead |
| IPC overhead > speedup | Negative scaling on small n | Hybrid: serial for n < 200, parallel for n > 300 |
| GPU memory limits | OOM on very large complexes | Fall back to CPU; batch by dimension |
| NumPy/SciPy version conflicts | CSR format incompatibility | Pin scipy >= 1.9; test on 3.11–3.14 |

## Next Phase (P17.4 & Beyond)

1. **P17.4:** Profile-driven optimization (identify remaining hotspots via cProfile)
2. **GPU acceleration:** Implement CuPy cohomology for n > 500
3. **Algorithm research:** Investigate more parallelizable reduction methods

## Code Locations

- Sparse infrastructure: `src/pytop/persistent_homology.py` (section: "Sparse matrix support")
- Benchmarks: `tests/profiling/test_p17_3_scaling.py` (planned)
- Reports: `docs/P17_3_SCALING_BENCHMARKS.json` (generated)
