from pytop.experimental.experimental_inference import (
    get_promoted_theorem_profile_alignments,
    theorem_profile_alignment_summary,
    theorem_profile_feature_index,
)


def test_experimental_inference_wrapper_tracks_core_theorem_profile_alignment_surface():
    alignments = get_promoted_theorem_profile_alignments()
    assert len(alignments) == 18
    assert theorem_profile_alignment_summary()['tightness'] == 2
    assert 'second_countable_network_weight' in theorem_profile_feature_index()['network_weight_alignment']
    assert 'urysohn_metrization_route' in theorem_profile_feature_index()['metrizable']
    assert 'safe_zone_sharpness_bridge_route' in theorem_profile_feature_index()['research_bridge']
    assert 'hypothesis_sensitivity_research_path' in theorem_profile_feature_index()['research_path']


def test_experimental_inference_wrapper_surfaces_compactness_strengthened_features():
    summary = theorem_profile_alignment_summary()
    assert summary['compactness_transition'] == 1
    assert 'compact_hausdorff_continuum_bound' in theorem_profile_feature_index()['compactness_size_bound']
