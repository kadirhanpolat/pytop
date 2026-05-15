from pytop.infinite_spaces import BasisDefinedSpace, MetricLikeSpace
from pytop.theorem_engine import infer_feature


def test_metric_space_infers_tightness_with_profile_metadata():
    space = MetricLikeSpace(carrier='R', metadata={'description': 'the real line'})
    result = infer_feature('tightness', space)
    assert result.is_true
    assert result.value == 'aleph_0'
    assert 'character_controls_tightness' in result.metadata['matched_profile_keys']
    assert 'tightness_network' in result.metadata['matched_profile_families']


def test_second_countable_space_infers_network_weight_alignment():
    space = BasisDefinedSpace(carrier='R', metadata={'basis_size': 'aleph_0'})
    result = infer_feature('network_weight_alignment', space)
    assert result.is_true
    assert result.value == {'network': 'aleph_0', 'weight': 'aleph_0'}
    assert 'network_vs_weight_control' in result.metadata['matched_profile_keys']


def test_second_countable_space_infers_hereditary_smallness_safe_region():
    space = BasisDefinedSpace(carrier='R', metadata={'basis_size': 'aleph_0'})
    result = infer_feature('hereditary_smallness', space)
    assert result.is_true
    assert result.value == 'hereditarily_lindelof_and_separable'
    assert 'second_countable_safe_region' in result.metadata['matched_profile_keys']
    assert '33' in result.metadata['matched_chapter_targets']


def test_compact_lindelof_transition_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["compact", "lindelof"]}
    result = infer_feature('compactness_transition', obj)
    assert result.is_true
    assert result.value == 'compact_collapse_visible'
    assert 'compactness_strengthened' in result.metadata['matched_profile_families']
    assert 'compact_lindelof_collapse' in result.metadata['matched_profile_keys']


def test_compact_hausdorff_first_countable_safe_zone_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["compact", "hausdorff", "first_countable"]}
    result = infer_feature('compactness_size_bound', obj)
    assert result.is_true
    assert result.value == 'continuum_bound'
    assert 'compact_hausdorff_first_countable_continuum' in result.metadata['matched_profile_keys']


def test_one_point_compactification_bridge_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["locally_compact", "hausdorff", "noncompact"]}
    result = infer_feature('compactification_bridge', obj)
    assert result.is_true
    assert result.value == 'one_point_compactification_available'
    assert 'one_point_compactification_bridge' in result.metadata['matched_profile_keys']
    assert '22' in result.metadata['matched_chapter_targets']


def test_urysohn_metrization_route_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["second_countable", "regular", "hausdorff"]}
    result = infer_feature('metrizable', obj)
    assert result.is_true
    assert result.value == 'metrizable'
    assert 'metrization' in result.metadata['matched_profile_families']
    assert 'urysohn_second_countable_regular_route' in result.metadata['matched_profile_keys']


def test_compact_second_countable_metrization_route_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["compact", "hausdorff", "second_countable"]}
    result = infer_feature('metrizable', obj)
    assert result.is_true
    assert result.value == 'metrizable'
    assert 'compact_hausdorff_second_countable_route' in result.metadata['matched_profile_keys']


def test_moore_metrization_route_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["regular", "developable", "hausdorff"]}
    result = infer_feature('metrizable', obj)
    assert result.is_true
    assert result.value == 'metrizable'
    assert 'moore_developable_regular_route' in result.metadata['matched_profile_keys']
    assert '36' in result.metadata['matched_chapter_targets']


def test_safe_zone_bridge_route_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["compact", "hausdorff", "first_countable"]}
    result = infer_feature('research_bridge', obj)
    assert result.is_true
    assert result.value == 'safe_zone_sharpness_route'
    assert 'research_bridge' in result.metadata['matched_profile_families']
    assert 'safe_zone_sharpness_route' in result.metadata['matched_profile_keys']


def test_compactification_bridge_route_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["locally_compact", "hausdorff", "noncompact"]}
    result = infer_feature('research_bridge', obj)
    assert result.is_true
    assert result.value == 'compactification_upgrade_route'
    assert 'compactification_upgrade_route' in result.metadata['matched_profile_keys']
    assert '22' in result.metadata['matched_chapter_targets']


def test_hereditary_local_warning_bridge_route_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["local_small_global_large"]}
    result = infer_feature('research_bridge', obj)
    assert result.is_true
    assert result.value == 'hereditary_local_warning_route'
    assert 'hereditary_local_warning_route' in result.metadata['matched_profile_keys']
    assert '36' in result.metadata['matched_chapter_targets']



def test_hypothesis_sensitivity_research_path_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["compact", "hausdorff", "first_countable"]}
    result = infer_feature('research_path', obj)
    assert result.is_true
    assert result.value == 'hypothesis_sensitivity_of_size_bounds'
    assert 'research_path' in result.metadata['matched_profile_families']
    assert 'hypothesis_sensitivity_of_size_bounds' in result.metadata['matched_profile_keys']


def test_fine_cardinal_warning_research_path_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["local_small_global_large"]}
    result = infer_feature('research_path', obj)
    assert result.is_true
    assert result.value == 'fine_cardinal_warning_lines'
    assert 'fine_cardinal_warning_lines' in result.metadata['matched_profile_keys']
    assert '36' in result.metadata['matched_chapter_targets']


def test_registry_alignment_research_path_is_visible_through_theorem_metadata():
    obj = {"representation": "basis_defined", "tags": ["registry_alignment"]}
    result = infer_feature('research_path', obj)
    assert result.is_true
    assert result.value == 'module_and_research_inventory'
    assert 'module_and_research_inventory' in result.metadata['matched_profile_keys']
