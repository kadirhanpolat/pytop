# Continua Examples -- GEO-08

This examples page introduces the v0.1.127 continuum bridge. A continuum is
recorded here in the standard entry-level sense: a nonempty compact connected
metric space. The package stores conservative profiles for familiar examples; it
does not attempt to decide continuum status for arbitrary spaces.

## Certified standard continua

| Profile | Compact | Connected | Metric | Teaching role |
|---|---:|---:|---:|---|
| `closed_interval_I` | yes | yes | yes | first compact connected metric example |
| `circle_S1` | yes | yes | yes | loop/fundamental-group bridge |
| `closed_disk_D2` | yes | yes | yes | Euclidean disk and boundary bridge |
| `hilbert_cube_I_omega` | yes | yes | yes | advanced metric-spaces-II preview |

## Counterexample and preview examples

- `cantor_set` is compact and metric but not connected; the profile records it
  as a non-continuum counterexample.
- `topologist_sine_curve_closure` is kept as a preview example. It is useful for
  teaching that connected compact metric examples can have subtle local behavior,
  but this package does not prove the full theorem.

## Minimal Python use

```python
from pytop import known_continuum_profile, continuum_profile_summary

circle = known_continuum_profile("circle")
summary = continuum_profile_summary(circle)
assert summary["continuum"] is True
assert summary["compact"] is True
```

Unknown examples intentionally remain unknown rather than being guessed.
