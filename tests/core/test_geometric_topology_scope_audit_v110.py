from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_v110_geometric_scope_audit_records_required_topic_families():
    route_map = (
        REPO_ROOT / "docs" / "roadmap" / "geometric_topology_route_map.md"
    ).read_text(encoding="utf-8")

    for topic in (
        "Metric spaces",
        "Polyhedra",
        "Homotopy",
        "Euclidean topology",
        "Manifolds",
        "Metric spaces II",
        "General topology",
    ):
        assert f"| {topic} |" in route_map

    assert "Scope audit decision" in route_map
    normalized = " ".join(route_map.split())
    assert "should not rewrite the existing general topology core" in normalized
    assert "v0.1.110: geometric topology scope audit. DONE" in route_map


def test_v110_scope_audit_keeps_geometric_implementation_deferred():
    src = REPO_ROOT / "src" / "pytop"
    deferred_modules = (
        "geometric_foundations.py",
        "metric_map_taxonomy.py",
        "simplices.py",
        "simplicial_complexes.py",
        "homotopy.py",
        "manifolds.py",
        "surfaces.py",
        "retracts.py",
    )

    assert all(not (src / module).exists() for module in deferred_modules)


def test_v110_roadmap_points_to_route_id_integration_next():
    current = (REPO_ROOT / "docs" / "roadmap" / "current_roadmap.md").read_text(
        encoding="utf-8"
    )
    backlog = (REPO_ROOT / "docs" / "roadmap" / "backlog.md").read_text(
        encoding="utf-8"
    )

    assert "v0.1.111: `GEO-01`--`GEO-08` route ID integration" in current
    assert "v0.1.111: `GEO-01`--`GEO-08` route ID integration" in backlog
