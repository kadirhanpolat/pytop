from pytop.experimental.chapter_experimental_registry import (
    build_chapter_experimental_registry,
    chapter_registry_summary,
    chapter_route_summary,
)


def test_chapter_experimental_registry_covers_volume_iii_band():
    entries = build_chapter_experimental_registry()
    chapters = [entry.chapter_number for entry in entries]
    assert chapters == ["32", "33", "34", "35", "36"]
    assert entries[0].primary_experimental_module == "tightness_network_profiles.py"
    assert entries[-1].primary_experimental_module == "research_bridge_profiles.py"


def test_chapter_registry_summary_tracks_primary_modules_once():
    summary = chapter_registry_summary()
    assert len(summary) == 5
    assert summary["classical_inequality_profiles.py"] == 1
    assert summary["research_bridge_profiles.py"] == 1


def test_chapter_route_summary_mentions_phase_l_bridge_routes():
    summary = chapter_route_summary()
    assert summary["safe_zone_sharpness_route"] == 3
    assert summary["future_threshold_release_route"] == 1
