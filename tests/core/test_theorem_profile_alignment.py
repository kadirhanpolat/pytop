from pytop.theorem_profile_alignment import (
    get_promoted_theorem_profile_alignments,
    theorem_profile_alignment_summary,
    theorem_profile_family_summary,
    theorem_profile_feature_index,
    theorem_profile_index_by_profile_key,
)


def test_promoted_theorem_profile_alignments_cover_expected_features_and_families():
    alignments = get_promoted_theorem_profile_alignments()
    keys = {alignment.key for alignment in alignments}
    assert 'metric_countable_tightness' in keys
    assert 'second_countable_network_weight' in keys
    assert 'compact_hausdorff_continuum_bound' in keys
    assert 'urysohn_metrization_route' in keys
    assert 'safe_zone_sharpness_bridge_route' in keys
    assert 'hypothesis_sensitivity_research_path' in keys
    assert theorem_profile_alignment_summary() == {
        'compactification_bridge': 1,
        'compactness_size_bound': 1,
        'compactness_transition': 1,
        'hereditary_smallness': 1,
        'metrizable': 3,
        'network_weight_alignment': 1,
        'research_bridge': 3,
        'research_path': 5,
        'tightness': 2,
    }
    assert theorem_profile_family_summary() == {
        'compactness_strengthened': 3,
        'hereditary_local': 1,
        'metrization': 3,
        'research_bridge': 3,
        'research_path': 5,
        'tightness_network': 3,
    }


def test_promoted_theorem_profile_indexes_expose_profile_links():
    feature_index = theorem_profile_feature_index()
    assert 'metric_countable_tightness' in feature_index['tightness']
    profile_index = theorem_profile_index_by_profile_key()
    assert 'second_countable_network_weight' in profile_index['network_vs_weight_control']
    assert 'second_countable_hereditary_smallness' in profile_index['second_countable_safe_region']
    assert 'compact_lindelof_transition' in profile_index['compact_lindelof_collapse']
    assert 'urysohn_metrization_route' in profile_index['urysohn_second_countable_regular_route']
    assert 'safe_zone_sharpness_bridge_route' in profile_index['safe_zone_sharpness_route']
    assert 'hypothesis_sensitivity_research_path' in profile_index['hypothesis_sensitivity_of_size_bounds']
