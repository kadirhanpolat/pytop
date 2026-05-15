"""pytop.knots icin KNOT-01/KNOT-02/KNOT-03 testleri."""

from pytop.knots import (
    KnotProfile,
    LinkProfile,
    KnotInvariantProfile,
    KnotApplicationProfile,
    ReidemeisterMoveProfile,
    get_knot_application_profiles,
    get_knot_invariant_profiles,
    get_knot_profiles,
    get_link_profiles,
    get_reidemeister_move_profiles,
    knot_application_domain_summary,
    knot_crossing_summary,
    knot_invariant_kind_summary,
    knot_theory_profile_registry,
)


def test_knot_profiles_include_classical_baseline_examples():
    profiles = get_knot_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(profile, KnotProfile) for profile in profiles)
    keys = {profile.key for profile in profiles}
    assert {"unknot_baseline", "trefoil_knot", "figure_eight_knot"}.issubset(keys)


def test_knot_profiles_have_source_and_crossing_data():
    profiles = get_knot_profiles()
    assert all("Adams & Franzosa" in profile.source_section for profile in profiles)
    assert all(profile.crossing_count >= 0 for profile in profiles)
    crossing_summary = knot_crossing_summary()
    assert crossing_summary["unknot_baseline"] == 0
    assert crossing_summary["trefoil_knot"] == 3
    assert crossing_summary["figure_eight_knot"] == 4


def test_link_profiles_distinguish_unlink_and_hopf_link():
    profiles = get_link_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(profile, LinkProfile) for profile in profiles)
    by_key = {profile.key: profile for profile in profiles}
    assert by_key["unlink_two_components"].component_count == 2
    assert "dolan" in by_key["hopf_link"].basic_linking_signal.lower()


def test_reidemeister_profiles_cover_all_three_moves():
    profiles = get_reidemeister_move_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) == 3
    assert all(isinstance(profile, ReidemeisterMoveProfile) for profile in profiles)
    assert {profile.move_type for profile in profiles} == {"R1", "R2", "R3"}
    assert all(profile.preserves_knot_type for profile in profiles)


def test_knot_theory_registry_counts_match_getters():
    registry = knot_theory_profile_registry()
    assert registry["knot_profiles"] == len(get_knot_profiles())
    assert registry["link_profiles"] == len(get_link_profiles())
    assert registry["reidemeister_move_profiles"] == len(get_reidemeister_move_profiles())
    assert registry["knot_invariant_profiles"] == len(get_knot_invariant_profiles())
    assert registry["knot_application_profiles"] == len(get_knot_application_profiles())
    assert sum(registry.values()) >= 19


def test_knot_invariant_profiles_cover_linking_alexander_and_jones():
    profiles = get_knot_invariant_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 6
    assert all(isinstance(profile, KnotInvariantProfile) for profile in profiles)
    kinds = {profile.invariant_kind for profile in profiles}
    assert {"linking_number", "alexander_polynomial", "jones_polynomial"}.issubset(kinds)


def test_knot_invariant_profiles_include_baseline_values():
    profiles = {profile.key: profile for profile in get_knot_invariant_profiles()}
    assert profiles["unlink_linking_number_zero"].symbolic_value == "0"
    assert profiles["unknot_alexander_polynomial"].symbolic_value == "1"
    assert profiles["unknot_jones_polynomial"].symbolic_value == "1"
    assert "trefoil" in profiles["trefoil_alexander_polynomial"].applies_to


def test_knot_invariant_kind_summary_groups_profiles():
    summary = knot_invariant_kind_summary()
    assert "hopf_link_linking_number" in summary["linking_number"]
    assert "trefoil_alexander_polynomial" in summary["alexander_polynomial"]
    assert "trefoil_jones_polynomial" in summary["jones_polynomial"]


def test_knot_application_profiles_cover_dna_and_chemistry():
    profiles = get_knot_application_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(profile, KnotApplicationProfile) for profile in profiles)
    domains = {profile.application_domain for profile in profiles}
    assert {"dna_topology", "chemical_topology"}.issubset(domains)


def test_knot_application_profiles_have_source_and_signals():
    profiles = get_knot_application_profiles()
    assert all("Adams & Franzosa" in profile.source_section for profile in profiles)
    assert all(profile.application_signal for profile in profiles)
    assert all(profile.teaching_note for profile in profiles)
    by_key = {profile.key: profile for profile in profiles}
    assert "Reidemeister" in by_key["topoisomerase_strand_passage"].application_signal
    assert "kiralite" in by_key["synthetic_chemistry_chiral_knots"].teaching_note


def test_knot_application_domain_summary_groups_profiles():
    summary = knot_application_domain_summary()
    assert "dna_supercoiling_topology" in summary["dna_topology"]
    assert "topoisomerase_strand_passage" in summary["dna_topology"]
    assert "synthetic_chemistry_chiral_knots" in summary["chemical_topology"]
    assert "molecular_link_detection" in summary["chemical_topology"]
