from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_v112_geometric_foundations_examples_cover_required_concepts():
    examples = (REPO_ROOT / "examples_bank" / "geometric_foundations_examples.md").read_text(
        encoding="utf-8"
    )

    for concept in (
        "Affine Hull",
        "Affine Independence",
        "Convex Hull",
        "Barycentric Coordinates",
        "Balls, Spheres, And Disks",
        "Projective-Space Intuition",
    ):
        assert f"## {concept}" in examples

    normalized = " ".join(examples.split())
    assert "Route: `GEO-01`" in examples
    assert "not copied from any source text" in normalized
    assert "Full projective classification" in examples


def test_v112_route_map_marks_geo01_active_and_metric_taxonomy_next():
    route_map = (
        REPO_ROOT / "docs" / "roadmap" / "geometric_topology_route_map.md"
    ).read_text(encoding="utf-8")
    current = (REPO_ROOT / "docs" / "roadmap" / "current_roadmap.md").read_text(
        encoding="utf-8"
    )
    backlog = (REPO_ROOT / "docs" / "roadmap" / "backlog.md").read_text(
        encoding="utf-8"
    )

    assert "`GEO-01` | `examples_bank/geometric_foundations_examples.md` | active examples bridge" in route_map
    assert "v0.1.112: geometric foundations bridge. DONE" in route_map
    assert "v0.1.113: metric map taxonomy" in current
    assert "v0.1.113: metric map taxonomy" in backlog


def test_v112_geometric_core_modules_remain_deferred():
    src = REPO_ROOT / "src" / "pytop"
    deferred_modules = (
        "geometric_foundations.py",
        "metric_map_taxonomy.py",
        "simplices.py",
        "simplicial_complexes.py",
        "paths.py",
        "homotopy.py",
        "manifolds.py",
        "surfaces.py",
    )

    assert all(not (src / module).exists() for module in deferred_modules)
