from pytop_experimental.maturity_registry import (
    chapter_primary_maturity_summary,
    experimental_maturity_summary,
    get_experimental_maturity_profiles,
    lookup_experimental_maturity,
    preferred_home_summary,
    promoted_core_facade_modules,
    core_counterpart_index,
    retained_supported_experimental_modules,
    retained_research_draft_modules,
    consolidation_bucket_summary,
)


def test_experimental_maturity_registry_covers_all_shipped_modules():
    profiles = get_experimental_maturity_profiles()
    module_names = {profile.module_name for profile in profiles}
    assert len(profiles) == 16
    assert "advanced_metrization.py" in module_names
    assert "theorem_drafts.py" in module_names


def test_experimental_maturity_summary_matches_expected_split():
    assert experimental_maturity_summary() == {
        "core_candidate": 10,
        "supported_experimental": 4,
        "research_draft": 2,
    }
    assert preferred_home_summary() == {
        "pytop": 10,
        "pytop_experimental": 4,
        "manuscript_research": 2,
    }


def test_lookup_and_chapter_primary_summary_align_with_volume_three_registry():
    assert lookup_experimental_maturity("advanced_cardinal_functions.py").maturity_tier == "core_candidate"
    assert lookup_experimental_maturity("tightness_network_profiles.py").preferred_home == "pytop"
    assert lookup_experimental_maturity("theorem_drafts.py").preferred_home == "manuscript_research"
    assert chapter_primary_maturity_summary() == {"core_candidate": 4, "supported_experimental": 1}


def test_promoted_core_facade_modules_are_visible_in_registry():
    assert promoted_core_facade_modules() == (
        "advanced_cardinal_functions.py",
        "advanced_metrization.py",
        "compactness_cardinal_bridges.py",
        "experimental_inference.py",
        "compactness_strengthened_profiles.py",
        "hereditary_local_profiles.py",
        "research_bridge_profiles.py",
        "tightness_network_profiles.py",
        "research_path_registry.py",
        "special_example_spaces.py",
    )


def test_consolidation_cleanup_exposes_core_counterparts_and_retained_buckets():
    assert consolidation_bucket_summary() == {
        "core_counterpart_available": 10,
        "retained_supported_experimental": 4,
        "retained_research_draft": 2,
    }
    counterpart_index = core_counterpart_index()
    assert counterpart_index["advanced_cardinal_functions.py"] == "pytop.cardinal_function_profiles"
    assert counterpart_index["research_path_registry.py"] == "pytop.research_path_profiles"
    assert retained_supported_experimental_modules() == (
        "chapter_experimental_registry.py",
        "classical_inequality_profiles.py",
        "research_bridge_inventory.py",
        "research_notebook_registry.py",
    )
    assert retained_research_draft_modules() == (
        "research_notes.py",
        "theorem_drafts.py",
    )
