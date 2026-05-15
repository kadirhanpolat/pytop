from pytop_questionbank.inverse_systems_families import build_inverse_questionbank_routes, inverse_questionbank_items, inverse_questionbank_summary, render_inverse_questionbank_report
def test_inverse_questionbank_seed_has_enough_items_and_families() -> None:
    routes=build_inverse_questionbank_routes(); items=inverse_questionbank_items(); summary=inverse_questionbank_summary()
    assert len(routes)==1
    assert len(items)==10
    assert summary["problem_family_count"]==10
    assert summary["example_key_count"]==3
    assert summary["ready_route_count"]==1
    assert "no copied" in summary["source_use_policy"]
def test_inverse_questionbank_report_names_key_surfaces() -> None:
    rendered=render_inverse_questionbank_report()
    assert "INV-Q01" in rendered
    assert "INV-Q10" in rendered
    assert "Inverse-systems" in rendered
