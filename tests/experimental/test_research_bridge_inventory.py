from pytop.experimental.research_bridge_inventory import (
    build_research_bridge_inventory,
    inventory_layer_summary,
)


def test_research_bridge_inventory_has_expected_routes():
    inventory = build_research_bridge_inventory()
    keys = {entry.key for entry in inventory}
    assert "safe_zone_sharpness_route" in keys
    assert "compactification_upgrade_route" in keys
    assert "future_threshold_release_route" in keys


def test_research_bridge_inventory_layers_match_bridge_registry():
    summary = inventory_layer_summary()
    assert summary == {"main_text": 2, "selected_block": 2, "advanced_note": 1}
