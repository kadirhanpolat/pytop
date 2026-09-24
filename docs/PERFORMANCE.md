# Profile Report: pytop Baseline Performance (Phase 17 P17.1)

> **What this file is.** A short, honest baseline for the one workload the Phase 17
> target is written against — Vietoris–Rips persistence at 500 points. It is
> deliberately not a full profile table. Earlier revisions of this file were an
> empty generated shell (`Total Runtime: 0.0000 seconds`, `Peak Memory: 0.00 MB`,
> `(No functions to report)`); the harness had run but collected nothing, and the
> zeros were an artefact, not a measurement.

## Metadata

- **Baseline measured:** 2026-09-24
- **Shell originally generated:** 2026-06-23T19:37:14
- **Python version:** Python 3.14.4
- **Platform:** win32, single machine, no parallelism

## Measured baseline — Vietoris–Rips, n = 500

| Workload | Total | Breakdown |
|----------|-------|-----------|
| `max_dimension=1` | **0.996 s** | — |
| `max_dimension=2`, `max_scale=1.0` | **9.06 s** | 950 914 simplices — 2.24 s build + 6.82 s reduce |

## Against the Phase 17 target

The Phase 17 target is stated as **"Rips n=500 in <1 s (current ~5 s), memory
linear in simplex count."** Measured against that:

- **The time target is met at `max_dimension=1` only** — 0.996 s, which clears 1 s
  by 4 ms. At `max_dimension=2` the same 500 points take **9.06 s**, roughly nine
  times the target. The target does not name a dimension, so read it as met for
  the dim-1 case and open for dim 2.
- **The memory half of the target has never been measured.** No run has recorded
  peak memory against simplex count, so "memory linear in simplex count" is an
  unverified claim, not a result. `tracemalloc` hooks exist in the P17.1 profiling
  infrastructure; nothing has used them on this workload.

The dim-2 cost splits roughly 25 % filtration build / 75 % column reduction, which
matches the profile noted in `docs/COMPLEXITY.md`: the reduction, not the build,
is where the remaining time is.

## Appendix: profiling harness smoke run

The eight benchmark-marked tests below confirm the P17.1 profiling infrastructure
runs; they are smoke tests on small inputs and are **not** the baseline above.

### Command

```
python -m pytest tests/profiling/ -v -m benchmark
```

### Status

**Status:** [PASS] All benchmarks passed

### Raw Output

```
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- C:\Python314\python.exe
rootdir: E:\PYTHON\pytop
configfile: pytest.ini (WARNING: ignoring pytest config in pyproject.toml!)
plugins: anyio-4.13.0, Faker-40.19.1, langsmith-0.8.3, locust-2.44.4, asyncio-1.4.0, typeguard-4.5.2, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 86 items / 78 deselected / 8 selected

tests/profiling/test_profile_homology.py::TestProfileHomology::test_profile_torus_homology PASSED [ 12%]
tests/profiling/test_profile_homology.py::TestProfileHomology::test_profile_klein_homology PASSED [ 25%]
tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[20] PASSED [ 37%]
tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[50] PASSED [ 50%]
tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[100] PASSED [ 62%]
tests/profiling/test_profile_homology.py::TestProfileKhovanov::test_profile_unknot_khovanov PASSED [ 75%]
tests/profiling/test_profile_homology.py::TestProfileKhovanov::test_profile_hopf_link_khovanov PASSED [ 87%]
tests/profiling/test_profile_homology.py::TestProfileSimplicialComplex::test_profile_sphere_complex_construction PASSED [100%]

====================== 8 passed, 78 deselected in 0.39s =======================

```
