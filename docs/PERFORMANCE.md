# Profile Report: pytop Baseline Performance (Phase 17 P17.1 - all)

## Metadata
- **Generated:** 2026-06-23T18:18:48.610126
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

**Status:** [WARNING] Some benchmarks failed or errored

### Raw Output
```
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- C:\Python314\python.exe
rootdir: E:\PYTHON\pytop
configfile: pytest.ini (WARNING: ignoring pytest config in pyproject.toml!)
plugins: anyio-4.13.0, Faker-40.19.1, langsmith-0.8.3, locust-2.44.4, asyncio-1.4.0, typeguard-4.5.2, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 60 items / 52 deselected / 8 selected

tests/profiling/test_profile_homology.py::TestProfileHomology::test_profile_torus_homology FAILED [ 12%]
tests/profiling/test_profile_homology.py::TestProfileHomology::test_profile_klein_homology FAILED [ 25%]
tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[20] FAILED [ 37%]
tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[50] FAILED [ 50%]
tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[100] FAILED [ 62%]
tests/profiling/test_profile_homology.py::TestProfileKhovanov::test_profile_trefoil_khovanov FAILED [ 75%]
tests/profiling/test_profile_homology.py::TestProfileKhovanov::test_profile_figure_eight_khovanov FAILED [ 87%]
tests/profiling/test_profile_homology.py::TestProfileSimplicialComplex::test_profile_simplicial_complex_construction FAILED [100%]

================================== FAILURES ===================================
_______________ TestProfileHomology.test_profile_torus_homology _______________
tests\profiling\test_profile_homology.py:46: in test_profile_torus_homology
    homology_result, stats = compute_torus_homology()
                             ^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\_internal\profiling_fixtures.py:133: in wrapper
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
tests\profiling\test_profile_homology.py:44: in compute_torus_homology
    return simplicial_homology(torus)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: simplicial_homology() missing 1 required positional argument: 'degree'
_______________ TestProfileHomology.test_profile_klein_homology _______________
tests\profiling\test_profile_homology.py:71: in test_profile_klein_homology
    homology_result, stats = compute_klein_homology()
                             ^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\_internal\profiling_fixtures.py:133: in wrapper
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
tests\profiling\test_profile_homology.py:69: in compute_klein_homology
    return simplicial_homology(klein)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: simplicial_homology() missing 1 required positional argument: 'degree'
__________ TestProfilePersistence.test_profile_rips_persistence[20] ___________
tests\profiling\test_profile_homology.py:113: in test_profile_rips_persistence
    pairs, stats = compute_rips_persistence()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\_internal\profiling_fixtures.py:133: in wrapper
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
tests\profiling\test_profile_homology.py:110: in compute_rips_persistence
    pairs = persistent_homology(points, max_dimension=2)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\persistent_homology.py:1023: in persistent_homology
    filtered = vietoris_rips_filtration(space, max_dimension=max_dimension, max_scale=max_scale)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\persistent_homology.py:935: in vietoris_rips_filtration
    points = list(space.carrier)
                  ^^^^^^^^^^^^^
E   AttributeError: 'numpy.ndarray' object has no attribute 'carrier'
__________ TestProfilePersistence.test_profile_rips_persistence[50] ___________
tests\profiling\test_profile_homology.py:113: in test_profile_rips_persistence
    pairs, stats = compute_rips_persistence()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\_internal\profiling_fixtures.py:133: in wrapper
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
tests\profiling\test_profile_homology.py:110: in compute_rips_persistence
    pairs = persistent_homology(points, max_dimension=2)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\persistent_homology.py:1023: in persistent_homology
    filtered = vietoris_rips_filtration(space, max_dimension=max_dimension, max_scale=max_scale)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\persistent_homology.py:935: in vietoris_rips_filtration
    points = list(space.carrier)
                  ^^^^^^^^^^^^^
E   AttributeError: 'numpy.ndarray' object has no attribute 'carrier'
__________ TestProfilePersistence.test_profile_rips_persistence[100] __________
tests\profiling\test_profile_homology.py:113: in test_profile_rips_persistence
    pairs, stats = compute_rips_persistence()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\_internal\profiling_fixtures.py:133: in wrapper
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
tests\profiling\test_profile_homology.py:110: in compute_rips_persistence
    pairs = persistent_homology(points, max_dimension=2)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\persistent_homology.py:1023: in persistent_homology
    filtered = vietoris_rips_filtration(space, max_dimension=max_dimension, max_scale=max_scale)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\persistent_homology.py:935: in vietoris_rips_filtration
    points = list(space.carrier)
                  ^^^^^^^^^^^^^
E   AttributeError: 'numpy.ndarray' object has no attribute 'carrier'
______________ TestProfileKhovanov.test_profile_trefoil_khovanov ______________
tests\profiling\test_profile_homology.py:158: in test_profile_trefoil_khovanov
    kh_result, stats = compute_trefoil_khovanov()
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\_internal\profiling_fixtures.py:133: in wrapper
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
tests\profiling\test_profile_homology.py:155: in compute_trefoil_khovanov
    kh = khovanov_homology(crossings=crossings, orientations=orientations)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: khovanov_homology() got an unexpected keyword argument 'crossings'
___________ TestProfileKhovanov.test_profile_figure_eight_khovanov ____________
tests\profiling\test_profile_homology.py:197: in test_profile_figure_eight_khovanov
    kh_result, stats = compute_figure_eight_khovanov()
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\_internal\profiling_fixtures.py:133: in wrapper
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
tests\profiling\test_profile_homology.py:194: in compute_figure_eight_khovanov
    kh = khovanov_homology(crossings=crossings, orientations=orientations)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: khovanov_homology() got an unexpected keyword argument 'crossings'
__ TestProfileSimplicialComplex.test_profile_simplicial_complex_construction __
tests\profiling\test_profile_homology.py:252: in test_profile_simplicial_complex_construction
    complex_obj, stats = construct_random_complex()
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\_internal\profiling_fixtures.py:133: in wrapper
    result = func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^
tests\profiling\test_profile_homology.py:250: in construct_random_complex
    return SimplicialComplex(simplices)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\pytop\simplicial_complexes.py:47: in __init__
    raise SimplicialComplexError(
E   pytop.simplicial_complexes.SimplicialComplexError: The simplex family is not face-closed; inspect face_closure_diagnostic for missing faces.
============================== warnings summary ===============================
tests\profiling\test_profile_homology.py:26
  E:\PYTHON\pytop\tests\profiling\test_profile_homology.py:26: PytestUnknownMarkWarning: Unknown pytest.mark.benchmark - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.benchmark

tests\profiling\test_profile_homology.py:81
  E:\PYTHON\pytop\tests\profiling\test_profile_homology.py:81: PytestUnknownMarkWarning: Unknown pytest.mark.benchmark - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.benchmark

tests\profiling\test_profile_homology.py:128
  E:\PYTHON\pytop\tests\profiling\test_profile_homology.py:128: PytestUnknownMarkWarning: Unknown pytest.mark.benchmark - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.benchmark

tests\profiling\test_profile_homology.py:206
  E:\PYTHON\pytop\tests\profiling\test_profile_homology.py:206: PytestUnknownMarkWarning: Unknown pytest.mark.benchmark - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.benchmark

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ===========================
FAILED tests/profiling/test_profile_homology.py::TestProfileHomology::test_profile_torus_homology
FAILED tests/profiling/test_profile_homology.py::TestProfileHomology::test_profile_klein_homology
FAILED tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[20]
FAILED tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[50]
FAILED tests/profiling/test_profile_homology.py::TestProfilePersistence::test_profile_rips_persistence[100]
FAILED tests/profiling/test_profile_homology.py::TestProfileKhovanov::test_profile_trefoil_khovanov
FAILED tests/profiling/test_profile_homology.py::TestProfileKhovanov::test_profile_figure_eight_khovanov
FAILED tests/profiling/test_profile_homology.py::TestProfileSimplicialComplex::test_profile_simplicial_complex_construction
================ 8 failed, 52 deselected, 4 warnings in 0.36s =================

```
