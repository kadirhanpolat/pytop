from pytop.advanced_compactifications import (
    advanced_compactness_profile,
    is_cech_complete,
    is_perfect_map,
    is_realcompact,
)


class _TaggedSpace:
    def __init__(self, *tags, representation="symbolic_general", name="space"):
        self.tags = set(tags)
        self.metadata = {"tags": list(tags), "representation": representation, "name": name}
        self.representation = representation
        self.name = name


def test_cech_complete_complete_metric_benchmark_v102():
    result = is_cech_complete(
        _TaggedSpace("complete_metric", "metrizable", representation="metric_symbolic", name="R")
    )
    assert result.status == "true"
    assert result.mode == "theorem"
    assert result.metadata["version"] == "0.1.102"


def test_cech_complete_metric_only_is_conditional_v102():
    result = is_cech_complete(
        _TaggedSpace("metric", "metrizable", representation="metric_symbolic", name="metric_x")
    )
    assert result.status == "conditional"


def test_realcompact_compact_hausdorff_benchmark_v102():
    result = is_realcompact(
        _TaggedSpace("compact_hausdorff", "hausdorff", representation="compact_symbolic", name="K")
    )
    assert result.status == "true"
    assert result.mode == "theorem"


def test_realcompact_explicit_negative_tag_v102():
    result = is_realcompact(
        _TaggedSpace("not_realcompact", "tychonoff", representation="symbolic_general", name="omega1")
    )
    assert result.status == "false"


def test_perfect_map_exact_positive_descriptor_v102():
    result = is_perfect_map(
        {
            "name": "quotient_projection",
            "representation": "symbolic_map",
            "continuous": True,
            "closed": True,
            "compact_fibers": True,
            "surjective": True,
        }
    )
    assert result.status == "true"
    assert result.mode == "exact"


def test_perfect_map_exact_negative_descriptor_v102():
    result = is_perfect_map(
        {
            "name": "open_embedding_like_map",
            "representation": "symbolic_map",
            "continuous": True,
            "closed": False,
            "compact_fibers": True,
            "surjective": True,
        }
    )
    assert result.status == "false"
    assert result.metadata["feature_map"]["closed"] is False


def test_perfect_map_partial_descriptor_is_conditional_v102():
    result = is_perfect_map(
        {
            "name": "partial_data_map",
            "representation": "symbolic_map",
            "continuous": True,
            "surjective": True,
        }
    )
    assert result.status == "conditional"


def test_advanced_compactness_profile_rolls_up_results_v102():
    profile = advanced_compactness_profile(
        _TaggedSpace("complete_metric", "compact_hausdorff", representation="benchmark_space", name="X")
    )
    assert profile["cech_complete"] is True
    assert profile["realcompact"] is True
    assert profile["benchmark_summary"]["shares_positive_corridor"] is True
    assert profile["cech_complete_result"].status == "true"
    assert profile["realcompact_result"].metadata["version"] == "0.1.102"
