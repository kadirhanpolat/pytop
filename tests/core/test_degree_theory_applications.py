"""Tests for pytop.degree_theory_applications -- DEG-02."""

from pytop.degree_theory_applications import (
    FundamentalTheoremAlgebraProfile,
    HeartbeatDegreeModelProfile,
    degree_theory_applications_registry,
    fta_profile_summary,
    get_fundamental_theorem_algebra_profiles,
    get_heartbeat_degree_model_profiles,
    heartbeat_degree_summary,
)


def test_fta_profiles_return_turkish_records():
    profiles = get_fundamental_theorem_algebra_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(p, FundamentalTheoremAlgebraProfile) for p in profiles)
    assert any("polinom" in p.display_name.lower() for p in profiles)


def test_fta_profiles_have_unique_keys_and_degree_argument():
    profiles = get_fundamental_theorem_algebra_profiles()
    keys = [p.key for p in profiles]
    assert len(keys) == len(set(keys))
    assert all("derece" in p.degree_argument.lower() for p in profiles)


def test_monic_polynomial_profile_states_fta_conclusion():
    profiles = {p.key: p for p in get_fundamental_theorem_algebra_profiles()}
    profile = profiles["fta_monic_polynomial_degree_n"]
    assert "karmaşık polinom" in profile.conclusion
    assert "homotopi" in profile.teaching_note
    assert "Adams & Franzosa" in profile.source_section


def test_heartbeat_profiles_return_turkish_records():
    profiles = get_heartbeat_degree_model_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(p, HeartbeatDegreeModelProfile) for p in profiles)
    assert all("kalp" in p.display_name.lower() or "ritim" in p.display_name.lower()
               for p in profiles)


def test_heartbeat_profiles_are_conceptual_not_medical_diagnosis():
    profiles = {p.key: p for p in get_heartbeat_degree_model_profiles()}
    profile = profiles["heartbeat_phase_return_map"]
    assert "tıbbi tanı" in profile.teaching_note
    assert "derece 1" in profile.degree_signal


def test_heartbeat_arrhythmia_contrast_mentions_model_assumptions():
    profiles = {p.key: p for p in get_heartbeat_degree_model_profiles()}
    profile = profiles["heartbeat_arrhythmia_contrast"]
    assert "varsayımlar" in profile.degree_signal
    assert "topolojik" in profile.interpretation.lower()


def test_application_summaries_match_getters():
    assert fta_profile_summary()["fundamental_theorem_algebra_profiles"] == len(
        get_fundamental_theorem_algebra_profiles()
    )
    assert heartbeat_degree_summary()["heartbeat_degree_model_profiles"] == len(
        get_heartbeat_degree_model_profiles()
    )


def test_degree_theory_applications_registry_counts_all_profiles():
    registry = degree_theory_applications_registry()
    assert registry["fundamental_theorem_algebra_profiles"] >= 2
    assert registry["heartbeat_degree_model_profiles"] >= 2
    assert sum(registry.values()) >= 4
