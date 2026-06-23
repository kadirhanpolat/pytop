# Profile Report: pytop Baseline Performance (Phase 17 P17.1 - all)

## Metadata
- **Generated:** 2026-06-23T19:37:14.169110
- **Total Runtime:** 0.0000 seconds
- **Peak Memory:** 0.00 MB
- **Python Version:** Python 3.14.4

## Function Breakdown

| Name | Time (s) | Calls | Memory (MB) |
|------|----------|-------|------------|

## Top Bottlenecks

(No functions to report)


## Benchmark Run Details

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
