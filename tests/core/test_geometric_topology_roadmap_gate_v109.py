from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_v109_geometric_topology_gate_is_recorded_as_non_blocking():
    route_map = (
        REPO_ROOT / "docs" / "roadmap" / "geometric_topology_route_map.md"
    ).read_text(encoding="utf-8")
    current = (REPO_ROOT / "docs" / "roadmap" / "current_roadmap.md").read_text(
        encoding="utf-8"
    )
    backlog = (REPO_ROOT / "docs" / "roadmap" / "backlog.md").read_text(
        encoding="utf-8"
    )

    assert "Maintenance gate decision" in route_map
    assert "non-blocking" in route_map
    assert "`GEO-01`" in route_map
    assert "`GEO-08`" in route_map
    assert "v0.1.110: geometric topology scope audit" in current
    assert "advanced quick-check/questionbank/notebook support backlog" in backlog


def test_v109_gate_does_not_open_geometric_core_modules_yet():
    src = REPO_ROOT / "src" / "pytop"
    deferred_modules = (
        "geometric_foundations.py",
        "metric_map_taxonomy.py",
        "simplices.py",
        "simplicial_complexes.py",
        "homotopy_profiles.py",
    )

    assert all(not (src / module).exists() for module in deferred_modules)
