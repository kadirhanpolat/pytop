# Phase 17 P17.3: Parallel Scaling (Planning & Infrastructure)

**Status:** 🚧 In Progress  
**Date:** 2026-06-23  
**Target:** Rips n=500 in <1s (current ~5.1s with n=350)  
**Challenge:** Reduction algorithms are inherently sequential

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

**Decision for P17.3:** Implement Strategy 3 (sparse optimization) + document Strategies 1 & 2 for future phases.

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
