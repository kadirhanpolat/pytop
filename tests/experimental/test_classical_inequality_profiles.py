from pytop_experimental.classical_inequality_profiles import (
    get_named_classical_inequality_profiles,
)


def test_classical_inequality_registry_has_expected_keys():
    profiles = get_named_classical_inequality_profiles()
    keys = {profile.key for profile in profiles}
    assert "hausdorff_density_character_code" in keys
    assert "countable_network_continuum_line" in keys
    assert "hereditary_local_warning_line" in keys


def test_classical_inequality_registry_layers_are_curated():
    profiles = get_named_classical_inequality_profiles()
    layers = {profile.writing_layer for profile in profiles}
    assert layers == {"main_text", "selected_block", "advanced_note"}
