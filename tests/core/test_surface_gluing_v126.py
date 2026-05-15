from pytop import SurfaceGluingError, compare_gluing_to_surface_profile, edge_label_counts, gluing_profile_summary, known_surface_profile, normalized_edge_word, orientability_heuristic, parse_edge_token, polygon_gluing_profile, standard_gluing_profile, validate_edge_pairing

def _assert_raises(error_type, callback, *args, **kwargs):
    try: callback(*args, **kwargs)
    except error_type: return
    raise AssertionError(f"{error_type.__name__} was not raised")

def test_edge_token_parsing_and_normalization():
    assert parse_edge_token("a").label == "a"
    assert parse_edge_token("a^-1").orientation == -1
    assert parse_edge_token("a^{-1}").normalized_text() == "a^-1"
    assert parse_edge_token("-b").normalized_text() == "b^-1"
    assert normalized_edge_word("a b a^-1 b^{-1}") == ("a", "b", "a^-1", "b^-1")
    _assert_raises(SurfaceGluingError, parse_edge_token, "")

def test_edge_pairing_diagnostic_distinguishes_boundary_and_overused_labels():
    torus=validate_edge_pairing("a b a^-1 b^-1"); disk_like=validate_edge_pairing("a b a^-1", allow_boundary_edges=True); invalid=validate_edge_pairing("a a a")
    assert torus.is_valid and torus.paired_labels == ("a", "b")
    assert edge_label_counts("a b a^-1") == {"a": 2, "b": 1}
    assert disk_like.is_valid and disk_like.boundary_labels == ("b",)
    assert not invalid.is_valid and invalid.overused_labels == ("a",)

def test_orientability_heuristic_for_standard_words():
    assert orientability_heuristic("a a^-1") == "orientable"
    assert orientability_heuristic("a b a^-1 b^-1") == "orientable"
    assert orientability_heuristic("a a") == "nonorientable"
    assert orientability_heuristic("a b a^-1 b") == "nonorientable"
    assert orientability_heuristic("a b c") == "unknown"

def test_standard_gluing_profiles_and_summary():
    torus=standard_gluing_profile("torus"); rp2=standard_gluing_profile("RP2"); klein=standard_gluing_profile("klein bottle")
    summary=gluing_profile_summary(torus)
    assert summary["edge_word"] == ("a", "b", "a^-1", "b^-1") and summary["pairing_valid"]
    assert summary["orientability_hint"] == "orientable"
    assert rp2.orientability_hint == "nonorientable" and klein.expected_surface_key == "klein_bottle"

def test_gluing_surface_metadata_comparison_is_conservative():
    profile=standard_gluing_profile("torus"); comparison=compare_gluing_to_surface_profile(profile, known_surface_profile("torus")); unknown=standard_gluing_profile("not registered")
    assert comparison["orientability_matches"] and comparison["surface_name"] == "torus_T2" and comparison["pairing_valid"]
    assert unknown.status == "unknown" and "placeholder" in " ".join(unknown.warnings).lower()

def test_custom_profile_validation_and_boundary_option():
    profile=polygon_gluing_profile("annulus_style_teaching_word", "a b a^-1", allow_boundary_edges=True, status="heuristic")
    summary=gluing_profile_summary(profile)
    assert summary["pairing_valid"] and summary["boundary_labels"] == ("b",)
    _assert_raises(SurfaceGluingError, polygon_gluing_profile, "bad", "a", status="invalid-status")
