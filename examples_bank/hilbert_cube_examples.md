# Hilbert Cube Examples -- GEO-08 Preview

This page records a light bridge to the Hilbert cube without turning the package
into a functional-analysis or infinite-product proof engine.

## Teaching model

The Hilbert cube may be viewed as a countable product of compact intervals with a
compatible product metric model. For the purposes of this package it is a
standard registered example of a compact connected metric continuum.

The v0.1.127 profile is intentionally modest:

- it records compactness, connectedness and metrizability metadata;
- it connects the example to metric spaces II, products and compactness;
- it avoids proving the Tychonoff theorem or building an infinite-dimensional
  recognition engine;
- it avoids using the Hilbert cube as a black-box answer for arbitrary continua.

## Minimal Python use

```python
from pytop import hilbert_cube_profile, continuum_condition_report

cube = hilbert_cube_profile()
report = continuum_condition_report(cube)
assert report["verdict"] == "continuum"
assert cube.metadata["standard_notation"] == "I^omega"
```
