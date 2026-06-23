# Profiling Infrastructure User Guide

This guide covers `pytop`'s profiling infrastructure (Phase 17 P17.1), which provides decorators and context managers for measuring function performance, call counts, and memory usage.

## Quick Start

### Example 1: Using the `@profile_call` Decorator

Profile a function with the decorator to automatically collect performance statistics:

```python
from pytop._internal.profiling import profile_call

@profile_call(track_memory=True)
def compute_homology(simplices: list) -> dict:
    """Compute persistent homology."""
    # Your expensive computation here
    return result

# Call the decorated function
result, stats = compute_homology(simplices)

# Access profiling results
print(f"Total time: {stats.total_time:.4f} seconds")
print(f"Call count: {stats.call_count}")
print(f"Peak memory: {stats.peak_memory_mb:.2f} MB")
print(f"Top 5 slowest callers:")
for caller in stats.top_5_callers:
    print(f"  - {caller}")
```

**Key Points:**
- The decorated function returns a tuple: `(result, ProfileStats)`
- `track_memory=True` enables memory profiling via `tracemalloc`
- Use `enable_by_default=False` to conditionally enable profiling

### Example 2: Using the `context_profile` Context Manager

Profile a code block without writing a separate function:

```python
from pytop._internal.profiling import context_profile

with context_profile("rips_filtration", track_memory=True) as prof:
    # Your code block here
    rips_complex = build_rips_filtration(points, max_dim=2)
    persistence = compute_persistence(rips_complex)

# Access results after the context exits
stats = prof.stats
print(f"Rips filtration took {stats.total_time:.4f}s")
print(f"Peak memory: {stats.peak_memory_mb:.2f} MB")
```

**Key Points:**
- Use for profiling code blocks that don't warrant a separate function
- The context manager automatically enables/disables profiling
- `prof.stats` is populated only after exiting the context

### Example 3: Generating a Markdown Report

Export profiling results to a structured Markdown file:

```python
from pytop._internal.profiling import profile_call, ProfileStats

# Run profiled function
result, stats = expensive_function(input_data)

# Example structure for a report
report_lines = [
    "# Performance Report",
    "",
    f"## {stats.function_name}",
    f"- **Total Time:** {stats.total_time:.4f} seconds",
    f"- **Call Count:** {stats.call_count}",
    f"- **Peak Memory:** {stats.peak_memory_mb:.2f} MB",
    "",
    "### Top 5 Slowest Functions",
]

for i, caller in enumerate(stats.top_5_callers, 1):
    report_lines.append(f"{i}. {caller}")

# Write to file
with open("performance_report.md", "w") as f:
    f.write("\n".join(report_lines))
```

---

## Running Benchmarks

### Manual Profiling of Core Operations

Run profiling on key operations to establish performance baselines:

```bash
# Run profiling tests
py -3.14 -m pytest tests/profiling/ -v

# Run with profiling and benchmark markers
py -3.14 -m pytest tests/profiling/ -m benchmark -v

# Run with coverage
py -3.14 -m pytest tests/profiling/ --cov=pytop --cov-report=term-missing
```

### Custom Profiling Script

Create a custom benchmarking script to profile specific operations:

```python
from pytop._internal.profiling import profile_call, context_profile
from pytop.homology import simplicial_homology
from pytop.persistent_homology import persistent_homology_rips

# Define test data
def create_test_simplices(n: int) -> list:
    """Create a test simplicial complex."""
    return [[i, i+1] for i in range(n-1)] + [[i] for i in range(n)]

# Profile individual functions
@profile_call(track_memory=True)
def bench_homology():
    simplices = create_test_simplices(100)
    h0, h1 = simplicial_homology(simplices)
    return h0, h1

# Profile a sequence of operations
def bench_tda_pipeline():
    with context_profile("complete_tda", track_memory=True) as prof:
        # 1. Build Rips complex
        with context_profile("rips_construction") as rips_prof:
            from pytop.persistent_homology import rips_filtration
            points = [[i, i**2] for i in range(50)]
            rips = rips_filtration(points, max_dim=2)
        
        # 2. Compute persistence
        with context_profile("persistence_computation") as pers_prof:
            pairs = persistent_homology_rips(points, max_dim=2)
        
        print(f"Rips: {rips_prof.stats.total_time:.4f}s")
        print(f"Persistence: {pers_prof.stats.total_time:.4f}s")
    
    return prof.stats

# Run benchmarks
if __name__ == "__main__":
    h0, h1, stats = bench_homology()
    print(f"\nHomology benchmark:")
    print(f"  Time: {stats.total_time:.4f}s")
    print(f"  Calls: {stats.call_count}")
    print(f"  Memory: {stats.peak_memory_mb:.2f} MB")
    
    tda_stats = bench_tda_pipeline()
    print(f"\nTDA pipeline:")
    print(f"  Time: {tda_stats.total_time:.4f}s")
    print(f"  Memory: {tda_stats.peak_memory_mb:.2f} MB")
```

### Running the Full Benchmark Suite

Establish performance baselines across multiple functions:

```bash
# Run all benchmarks
py -3.14 -m pytest tests/profiling/ -v --tb=short

# Run with timing output
py -3.14 -m pytest tests/profiling/ -v --durations=10
```

---

## Interpreting Results

### ProfileStats Fields

`ProfileStats` provides the following measurements:

| Field | Meaning | Notes |
|-------|---------|-------|
| `function_name` | Name of the profiled function/block | Extracted from function `__name__` or passed as argument |
| `total_time` | Total wall-clock time in seconds | Maximum cumulative time from cProfile; represents the longest call chain |
| `call_count` | Aggregate number of function calls | Includes all internal calls (e.g., recursive calls count multiple times) |
| `peak_memory_mb` | Peak memory usage in megabytes | Only tracked if `track_memory=True`; 0.0 if disabled |
| `top_5_callers` | List of 5 slowest caller functions | Sorted by cumulative time (slowest first); helps identify hotspots |
| `raw_profile_data` | Raw cProfile statistics dictionary | Advanced use; contains full `pstats.Stats` data |

### Example Interpretation

```python
from pytop._internal.profiling import profile_call

@profile_call(track_memory=True)
def example_function():
    # Expensive operation
    pass

result, stats = example_function()

# Interpret the results
print(f"Benchmark: {stats.function_name}")
print(f"├─ Duration: {stats.total_time:.4f}s")
print(f"├─ Functions called: {stats.call_count}")
print(f"├─ Memory peak: {stats.peak_memory_mb:.2f} MB")
print(f"└─ Top bottleneck: {stats.top_5_callers[0] if stats.top_5_callers else 'N/A'}")

# Performance assessment
if stats.total_time > 1.0:
    print("⚠️  WARNING: Function exceeds 1-second threshold")
if stats.peak_memory_mb > 100:
    print("⚠️  WARNING: Memory usage exceeds 100 MB")
```

### Wall-Clock Timing Notes

- **cProfile measure:** Total time includes all function calls made during execution
- **Nested calls:** If function A calls function B 1000 times, call_count reflects both A and all B invocations
- **System variation:** Wall-clock times vary with system load; run multiple times for averages
- **External I/O:** File I/O, network calls, and other external operations are included in timings

### Memory Peak Definition

- **Peak memory:** Maximum bytes allocated during profiling (not including cleanup)
- **Reported as:** MB (megabytes), calculated as `max(stat.size) / (1024 * 1024)`
- **Tracking overhead:** Memory tracking itself adds ~5–10% overhead
- **Baseline:** Disable tracking if memory profiling is not needed

---

## Advanced Usage

### Conditional Profiling with `enable_by_default`

Disable profiling by default and enable only when needed:

```python
from pytop._internal.profiling import profile_call

# Profiling disabled by default (returns empty stats)
@profile_call(track_memory=False, enable_by_default=False)
def rarely_profiled_function(x):
    return x ** 2

result, stats = rarely_profiled_function(5)
print(f"Profiling active: {stats.call_count > 0}")  # False
```

This is useful for expensive operations where profiling overhead matters.

### Memory Tracking Enabled/Disabled

```python
# With memory tracking (slower, more detail)
@profile_call(track_memory=True)
def memory_intensive_operation():
    data = [list(range(1000)) for _ in range(1000)]
    return len(data)

result, stats = memory_intensive_operation()
print(f"Peak memory: {stats.peak_memory_mb:.2f} MB")  # Populated

# Without memory tracking (faster)
@profile_call(track_memory=False)
def cpu_bound_operation():
    total = sum(i**2 for i in range(100000))
    return total

result, stats = cpu_bound_operation()
print(f"Peak memory: {stats.peak_memory_mb:.2f} MB")  # 0.0
```

### Nesting Context Managers

Profile nested operations to identify which step is slowest:

```python
from pytop._internal.profiling import context_profile

with context_profile("full_pipeline") as full:
    with context_profile("preprocessing") as prep:
        data = preprocess_points(raw_points)
    
    with context_profile("complex_construction") as construct:
        rips = build_rips(data)
    
    with context_profile("persistence") as persist:
        barcode = compute_persistence(rips)

# Summary of nested operations
print(f"Preprocessing: {prep.stats.total_time:.4f}s")
print(f"Construction: {construct.stats.total_time:.4f}s")
print(f"Persistence: {persist.stats.total_time:.4f}s")
print(f"Total: {full.stats.total_time:.4f}s")
```

### Combining Decorator and Context Manager

Use both together for fine-grained profiling:

```python
from pytop._internal.profiling import profile_call, context_profile

@profile_call(track_memory=True)
def complete_analysis(data):
    with context_profile("step_1_validation") as v:
        validate(data)
    
    with context_profile("step_2_computation") as c:
        result = compute(data)
    
    with context_profile("step_3_export") as e:
        export(result)
    
    return result

result, overall_stats = complete_analysis(input_data)
print(f"Overall: {overall_stats.total_time:.4f}s")
print(f"Memory: {overall_stats.peak_memory_mb:.2f} MB")
```

---

## Best Practices

### 1. Profile in Realistic Conditions

```python
# Good: Use realistic data sizes
@profile_call(track_memory=True)
def test_large_complex():
    points = [[i, i**2] for i in range(1000)]  # Realistic scale
    return persistent_homology_rips(points)

# Avoid: Micro-benchmarks on tiny inputs
@profile_call(track_memory=True)
def test_tiny_complex():
    return persistent_homology_rips([[1, 2]])  # Too small, noise-prone
```

### 2. Run Multiple Samples

```python
import statistics

times = []
for _ in range(5):
    _, stats = expensive_function(data)
    times.append(stats.total_time)

avg_time = statistics.mean(times)
std_dev = statistics.stdev(times)
print(f"Time: {avg_time:.4f}s ± {std_dev:.4f}s")
```

### 3. Compare Before/After Optimizations

```python
# Before optimization
_, stats_old = old_algorithm(data)
print(f"Old: {stats_old.total_time:.4f}s")

# After optimization
_, stats_new = new_algorithm(data)
print(f"New: {stats_new.total_time:.4f}s")

# Calculate improvement
speedup = stats_old.total_time / stats_new.total_time
print(f"Speedup: {speedup:.2f}x")
```

### 4. Use Top Callers to Find Hotspots

```python
@profile_call()
def find_bottleneck():
    # Complex operation
    pass

_, stats = find_bottleneck()

print("Slowest functions:")
for i, caller in enumerate(stats.top_5_callers, 1):
    print(f"{i}. {caller}")
```

---

## Next Steps: Phase 17.2–17.3

The profiling infrastructure is designed to support future optimization phases:

- **Phase 17.2 (Algorithm Optimization):** Use profiling to identify sparse matrix operations and Clearing Lemma thresholds; target 2–5× speedup
- **Phase 17.3 (Parallel Scaling):** Profile on multi-core systems to measure ProcessPoolExecutor and GPU acceleration impact; benchmark on Rips n=100–500

For detailed performance targets and optimization roadmap, see `docs/COMPLEXITY.md`.

---

## Troubleshooting

### "ProfileStats was not initialized" Error

This occurs if the context manager fails to exit properly. Ensure you use proper `try/finally` or `with` statements:

```python
# Correct: Use context manager
with context_profile("operation") as prof:
    do_work()
# prof.stats is accessible here

# Incorrect: Don't access stats outside context
with context_profile("operation") as prof:
    do_work()
# Don't try to access prof.stats here without exiting context first
```

### High Memory Reporting When Track Memory Is False

If `track_memory=False` but you see high `peak_memory_mb` values, it's likely the value is stuck from a previous profiling run. Disable memory tracking explicitly:

```python
@profile_call(track_memory=False)  # Explicitly disable
def my_function():
    pass
```

### Profiler Overhead

cProfile adds ~5–10% overhead. For minimal overhead, disable memory tracking and use `enable_by_default=False` when profiling is optional.

---

## See Also

- **`ProfileStats` API:** `src/pytop/_internal/profiling.py`
- **Test examples:** `tests/profiling/`
- **Performance targets:** `docs/COMPLEXITY.md`
- **Optimization roadmap:** Phase 17 in `CLAUDE.md`
