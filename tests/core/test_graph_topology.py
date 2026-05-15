"""pytop.graph_topology icin GTOP-01 testleri."""

from pytop.graph_topology import (
    ChemicalGraphProfile,
    GraphCrossingThicknessProfile,
    GraphEmbeddingProfile,
    GraphPlanarityProfile,
    TopologicalGraphProfile,
    chemical_graph_molecule_summary,
    get_chemical_graph_profiles,
    get_graph_crossing_thickness_profiles,
    get_graph_embedding_profiles,
    get_graph_planarity_profiles,
    get_topological_graph_profiles,
    graph_embedding_ambient_summary,
    graph_euler_characteristic_summary,
    graph_planarity_summary,
    graph_topology_profile_registry,
)


def test_topological_graph_profiles_cover_basic_models():
    profiles = get_topological_graph_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(profile, TopologicalGraphProfile) for profile in profiles)
    keys = {profile.key for profile in profiles}
    assert {"interval_graph_arc", "cycle_graph_circle", "theta_graph"}.issubset(keys)


def test_topological_graph_profiles_have_euler_data():
    profiles = get_topological_graph_profiles()
    assert all("Adams & Franzosa" in profile.source_section for profile in profiles)
    assert all(profile.vertex_count >= 0 for profile in profiles)
    assert all(profile.edge_count >= 0 for profile in profiles)
    summary = graph_euler_characteristic_summary()
    assert summary["interval_graph_arc"] == 1
    assert summary["cycle_graph_circle"] == 0
    assert summary["theta_graph"] == -1


def test_graph_embedding_profiles_cover_plane_and_line():
    profiles = get_graph_embedding_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(profile, GraphEmbeddingProfile) for profile in profiles)
    ambient_spaces = {profile.ambient_space for profile in profiles}
    assert {"plane", "line"}.issubset(ambient_spaces)


def test_graph_embedding_profiles_reference_graph_profiles():
    graph_keys = {profile.key for profile in get_topological_graph_profiles()}
    embeddings = get_graph_embedding_profiles()
    assert all(profile.graph_key in graph_keys for profile in embeddings)
    by_key = {profile.key: profile for profile in embeddings}
    assert by_key["cycle_graph_plane_embedding"].face_count == 2
    assert by_key["interval_graph_line_embedding"].face_count is None


def test_graph_embedding_ambient_summary_groups_profiles():
    summary = graph_embedding_ambient_summary()
    assert "cycle_graph_plane_embedding" in summary["plane"]
    assert "theta_graph_plane_embedding" in summary["plane"]
    assert "interval_graph_line_embedding" in summary["line"]


def test_graph_topology_registry_counts_match_getters():
    registry = graph_topology_profile_registry()
    assert registry["topological_graph_profiles"] == len(
        get_topological_graph_profiles()
    )
    assert registry["graph_embedding_profiles"] == len(get_graph_embedding_profiles())
    assert registry["graph_planarity_profiles"] == len(get_graph_planarity_profiles())
    assert registry["chemical_graph_profiles"] == len(get_chemical_graph_profiles())
    assert registry["graph_crossing_thickness_profiles"] == len(
        get_graph_crossing_thickness_profiles()
    )
    assert sum(registry.values()) >= 14


def test_graph_planarity_profiles_cover_kuratowski_examples():
    profiles = get_graph_planarity_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(profile, GraphPlanarityProfile) for profile in profiles)
    summary = graph_planarity_summary()
    assert summary["k5_nonplanar_profile"] is False
    assert summary["k33_nonplanar_profile"] is False
    assert summary["cycle_graph_planar_profile"] is True


def test_chemical_graph_profiles_capture_molecular_models():
    profiles = get_chemical_graph_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(profile, ChemicalGraphProfile) for profile in profiles)
    molecules = chemical_graph_molecule_summary()
    assert molecules["benzene_cycle_graph"] == "Benzen halkasi"
    assert "Izomer" in profiles[1].display_name


def test_crossing_thickness_profiles_link_planarity_to_chemistry():
    profiles = get_graph_crossing_thickness_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(profile, GraphCrossingThicknessProfile) for profile in profiles)
    by_key = {profile.key: profile for profile in profiles}
    assert "gecis" in by_key["k5_crossing_thickness_signal"].crossing_number_signal
    assert "3B" in by_key["molecular_bond_graph_crossing_warning"].teaching_note
