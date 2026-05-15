from pytop import SurfaceProfileError, annulus_surface_profile, as_manifold_profile, disk_surface_profile, double_torus_surface_profile, klein_bottle_surface_profile, known_surface_profile, mobius_band_surface_profile, projective_plane_surface_profile, sphere_surface_profile, surface_profile, surface_profile_summary, torus_surface_profile

def _assert_raises(error_type, callback, *args, **kwargs):
    try: callback(*args, **kwargs)
    except error_type: return
    raise AssertionError(f"{error_type.__name__} was not raised")

def test_closed_orientable_surface_profiles_record_genus():
    sphere=sphere_surface_profile(); torus=torus_surface_profile(); double_torus=double_torus_surface_profile()
    assert sphere.dimension == 2 and sphere.genus == 0 and sphere.is_closed_surface
    assert torus.genus == 1 and torus.gluing_word == "a b a^-1 b^-1"
    assert double_torus.genus == 2 and "genus 2" in double_torus.classification_label

def test_surfaces_with_boundary_record_boundary_components():
    disk=disk_surface_profile(); annulus=annulus_surface_profile(); mobius=mobius_band_surface_profile()
    assert disk.has_boundary and disk.boundary_component_count == 1 and disk.metadata["boundary_model"] == "S^1"
    assert annulus.boundary_component_count == 2
    assert mobius.orientability == "nonorientable" and mobius.nonorientable_genus == 1 and mobius.has_boundary

def test_nonorientable_standard_profiles_are_separate_from_orientable_genus():
    rp2=projective_plane_surface_profile(); klein=klein_bottle_surface_profile()
    assert rp2.genus is None and rp2.nonorientable_genus == 1 and rp2.orientability == "nonorientable"
    assert klein.nonorientable_genus == 2 and klein.is_closed_surface
    assert any("recognition" in w.lower() or "classification" in w.lower() for w in klein.warnings)

def test_registry_summary_and_manifold_bridge():
    torus=known_surface_profile("torus T2"); unknown=known_surface_profile("wild polygon quotient"); summary=surface_profile_summary(torus); manifold_view=as_manifold_profile(torus)
    assert torus.name == "torus_T2" and summary["classification_label"] == "orientable genus 1 surface"
    assert manifold_view.dimension == 2 and manifold_view.local_model == "R^2"
    assert manifold_view.metadata["source_surface_profile"] == "torus_T2"
    assert unknown.status == "unknown" and unknown.orientability == "unknown"

def test_surface_profile_validation_guardrails():
    _assert_raises(SurfaceProfileError, surface_profile, "bad", orientability="maybe")
    _assert_raises(SurfaceProfileError, surface_profile, "bad", genus=-1, orientability="orientable")
    _assert_raises(SurfaceProfileError, surface_profile, "bad", nonorientable_genus=0, orientability="nonorientable")
    _assert_raises(SurfaceProfileError, surface_profile, "bad", boundary_component_count=-1)
    _assert_raises(SurfaceProfileError, surface_profile, "bad", orientability="orientable", genus=1, nonorientable_genus=1)
    _assert_raises(SurfaceProfileError, surface_profile, "bad", orientability="nonorientable", genus=1, nonorientable_genus=2)
