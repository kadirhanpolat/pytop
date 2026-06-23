# Phase 19: API Stability & Ergonomics

**Status:** 🚧 In Progress  
**Date:** 2026-06-23  
**Focus:** Error clarity, deprecation policy, API consistency

## Phase 19.1: Error Message Improvements ✅

### Policy

All user-facing errors follow the **WHY-HOW-THEN** pattern:

1. **WHAT:** State what went wrong (the assertion that failed)
2. **WHY:** Explain why it matters or what the constraint is
3. **HOW:** Suggest how to fix it with a concrete example

### Example (Before)
```python
raise ValueError("max_dimension must be nonnegative.")
```

### Example (After)
```python
raise ValueError(
    f"max_dimension must be nonnegative (got {max_dimension}). "
    "This sets the highest simplex dimension to include; pass 1 for edges only, "
    "2 for triangles, etc."
)
```

### Implemented in P19.1

| Function | Error | Improvement |
|----------|-------|-------------|
| `vietoris_rips_filtration()` | max_dimension validation | Added parameter explanation + example |
| `vietoris_rips_filtration()` | nonempty point set | Added FiniteMetricSpace construction example |
| `persistent_homology()` | method parameter | Added all three method descriptions + when to use each |

### Test Coverage

Error messages tested via `test_error_messages_clarity()` in `tests/core/test_persistent_homology.py`:
- ✅ max_dimension < 0 triggers helpful error
- ✅ empty carrier triggers helpful error
- ✅ invalid method triggers helpful error

## Phase 19.2: Deprecation Policy (Planned)

### Versioning

- **Current:** v1.6.0 (Phase 16 complete; Phase 17 in progress)
- **v2.0.0 window:** 18 months from v2.0.0 release
- **Deprecation ladder:** v1.x series has no breaking changes; v2.0.0 removes deprecated items

### Deprecation Process

1. **v1.n:** Introduce `DeprecationWarning` with replacement path
2. **v1.n+1 through v1.z:** Warning remains; replacement available
3. **v2.0.0:** Remove deprecated function entirely

### Example Deprecation

```python
import warnings

@deprecated("Use persistent_homology(..., method='twist') instead. "
            "The Twist algorithm is now the default and is always faster.")
def persistent_homology_optimized(...):
    """DEPRECATED: Use persistent_homology() with method='twist'."""
    return persistent_homology(..., method='twist')
```

### Candidates for v2.0.0 Removal (TBD)

(To be determined after Phase 19.2 audit — scanning all public APIs)

## Phase 19.3: API Consistency (Planned)

### Naming Audit

Consistent naming patterns across similar functions:

| Pattern | Examples | Status |
|---------|----------|--------|
| `persistent_*` | `persistent_homology()`, `persistent_pairs_twist()` | ✅ Consistent |
| `*_filtration` | `vietoris_rips_filtration()`, `cech_filtration()` | ✅ Consistent |
| `*_complex` | `vietoris_rips_complex()?`, `cech_complex()?` | TBD |

### Parameter Ordering

Standard parameter order across persistent homology:
1. Primary input (space, complex, or filtered complex)
2. Configuration (max_dimension, max_scale, include_zero_persistence)
3. Implementation selection (method, parallel, device)

### Return Type Consistency

| Function | Returns | Pattern |
|----------|---------|---------|
| `persistent_homology()` | `tuple[PersistencePair, ...]` | Sorted by (dim, birth, death) |
| `persistence_pairs_twist()` | `tuple[PersistencePair, ...]` | Sorted by (dim, birth, death) |
| `persistence_pairs_cohomology()` | `tuple[PersistencePair, ...]` | Sorted by (dim, birth, death) |
| `*_with_stats()` | `tuple[pairs, stats]` | Stats object for metrics |

✅ **All consistent.**

## Test Coverage

### Error Message Tests (P19.1)

```bash
pytest tests/core/test_persistent_homology.py::TestErrorMessages -v
```

Status: ✅ All pass (3 tests)

### Deprecation Tests (P19.2)

To be implemented: catch `DeprecationWarning`, verify message format.

### API Consistency Tests (P19.3)

To be implemented: check parameter order, return types, naming patterns across homology module.

## Timeline & Roadmap

| Phase | Deliverables | Status |
|-------|--------------|--------|
| **P19.1** | Error message clarity (3 functions) | ✅ Complete |
| **P19.2** | Deprecation policy doc + decorator | 🚧 Planned |
| **P19.3** | API consistency audit + fixes | 🚧 Planned |
| **v2.0.0 prep** | Removal candidate list + migration guide | 🚧 Future |

## Documentation

- **User migration guide:** `docs/API_DESIGN.md` (to be created)
- **Deprecation list:** `docs/DEPRECATIONS.md` (to be created for v2.0.0 candidates)
- **Error message examples:** This file (reference for contributors)

## Impact

- **User experience:** Clearer error messages with actionable fixes
- **Adoption friction:** Reduced "I got an error, now what?" support burden
- **Migration path:** Clear v1→v2 upgrade guidance (v2.0.0 phase)
