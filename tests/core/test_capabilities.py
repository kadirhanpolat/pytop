from pytop.capabilities import DEFAULT_REGISTRY, explain_capability, normalize_feature_name


def test_alias_normalization_maps_compactness_to_compact():
    assert normalize_feature_name("compactness") == "compact"


def test_finite_capability_is_exact_for_compact():
    capability = DEFAULT_REGISTRY.support_for("finite", "compact")
    assert capability.support == "exact"


def test_infinite_metric_capability_explanation_mentions_theorem_support():
    text = explain_capability("infinite_metric", "compactness")
    assert "theorem" in text.lower()
