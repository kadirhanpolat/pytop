from pytop_questionbank.proximity_spaces_families import build_proximity_questionbank_routes, proximity_questionbank_items, proximity_questionbank_summary, render_proximity_questionbank_report

def test_proximity_questionbank_seed_has_enough_items_and_families() -> None:
    routes = build_proximity_questionbank_routes()
    items = proximity_questionbank_items()
    summary = proximity_questionbank_summary()
    assert len(routes) == 1
    assert len(items) == 10
    assert summary["problem_family_count"] == 10
    assert summary["example_key_count"] == 3
    assert summary["ready_route_count"] == 1
    assert "no copied" in summary["source_use_policy"]

def test_proximity_questionbank_report_names_key_surfaces() -> None:
    rendered = render_proximity_questionbank_report()
    assert "PROX-Q01" in rendered
    assert "PROX-Q10" in rendered
    assert "Proximity-spaces" in rendered
