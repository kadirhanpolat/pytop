from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _route_map() -> str:
    return (REPO_ROOT / "docs" / "roadmap" / "geometric_topology_route_map.md").read_text(
        encoding="utf-8"
    )


def test_v111_route_metadata_registry_has_all_geo_routes():
    route_map = _route_map()

    assert "## Route metadata registry" in route_map
    for route_id in (
        "GEO-01",
        "GEO-02",
        "GEO-03",
        "GEO-04",
        "GEO-05",
        "GEO-06",
        "GEO-07",
        "GEO-08",
    ):
        assert f"| `{route_id}` |" in route_map


def test_v111_route_metadata_covers_required_fields_and_guardrails():
    route_map = _route_map()

    for heading in (
        "Aim",
        "Target level",
        "Connected existing surfaces",
        "Planned durable surfaces",
        "Test expectation",
        "Deferred heavy topics",
    ):
        assert heading in route_map

    assert "route IDs are durable names, not version labels" in route_map
    assert "general homotopy decision procedures" in route_map
    assert "full surface-classification proof" in route_map
    assert "general AR/ANR recognition" in route_map


def test_v111_route_metadata_keeps_implementation_modules_deferred():
    src = REPO_ROOT / "src" / "pytop"
    deferred_modules = (
        "geometric_foundations.py",
        "metric_map_taxonomy.py",
        "simplices.py",
        "simplicial_complexes.py",
        "paths.py",
        "homotopy.py",
        "fundamental_groups.py",
        "euclidean_topology.py",
        "spheres.py",
        "manifolds.py",
        "surfaces.py",
        "surface_gluing.py",
        "continua.py",
        "retracts.py",
    )

    assert all(not (src / module).exists() for module in deferred_modules)


def test_v111_fixed_roadmap_points_to_geometric_foundations_next():
    current = (REPO_ROOT / "docs" / "roadmap" / "current_roadmap.md").read_text(
        encoding="utf-8"
    )
    backlog = (REPO_ROOT / "docs" / "roadmap" / "backlog.md").read_text(
        encoding="utf-8"
    )

    assert "v0.1.112: geometric foundations bridge" in current
    assert "v0.1.112: geometric foundations bridge" in backlog
