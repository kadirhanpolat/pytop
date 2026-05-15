# Retracts, AR and ANR Examples -- GEO-08

This page is a conservative teaching bridge for retracts, deformation retracts,
absolute retracts (AR) and absolute neighbourhood retracts (ANR).  The package
records safe profiles and standard examples; it does not decide whether an
arbitrary space is a retract, AR or ANR.

## Retract versus deformation retract

A retraction profile records the shape of a map `r: X -> A` that fixes the
subspace `A`.  A deformation-retraction profile adds homotopy information and is
therefore stronger.  The code keeps these assertions as explicit metadata rather
than silently upgrading one notion to the other.

```python
from pytop import certified_retraction_profile, retraction_summary

profile = certified_retraction_profile(
    "annulus_to_core_circle",
    "annulus",
    "core circle",
    retraction_label="radial projection to the core circle",
    deformation_available=True,
    strong_deformation=True,
    related_profiles=("surfaces", "homotopy"),
)

assert retraction_summary(profile)["is_certified"] is True
```

## Absolute retract examples

Registered AR examples include the one-point space, the closed interval and the
closed disk/ball model.  These are registry entries with certification notes;
they are not the result of an automatic theorem prover.

```python
from pytop import known_absolute_retract_profile, absolute_retract_summary

interval = known_absolute_retract_profile("unit interval")
assert absolute_retract_summary(interval)["is_certified_ar"] is True
```

## ANR examples and previews

Finite polyhedra and the circle are recorded as certified standard ANR examples.
Metrizable topological manifolds are represented as a preview profile because the
package does not verify all atlas or metrizability hypotheses.

```python
from pytop import known_anr_profile, anr_summary

circle = known_anr_profile("S1")
manifold_preview = known_anr_profile("manifold")

assert anr_summary(circle)["is_certified_anr"] is True
assert manifold_preview.status == "preview"
```

## Guardrail

`unknown` is deliberately not a negative theorem. It means only that the current
registry does not contain a certificate for the requested model.
