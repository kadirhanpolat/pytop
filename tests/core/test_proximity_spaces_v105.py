from pytop.proximity_spaces import is_close, is_proximity_space, smirnov_compactification


class _Tagged:
    def __init__(self, *tags, **metadata):
        self.tags = set(tags)
        self.metadata = {"tags": list(tags), **metadata}


def test_proximity_space_explicit_closeness_map_v105():
    space = {
        "closeness_map": {
            ("A", "B"): True,
            ("A", "C"): False,
        }
    }
    assert is_proximity_space(space) is True
    assert is_close("A", "B", space) is True
    assert is_close("A", "C", space) is False


def test_metric_proximity_benchmark_v105():
    space = {"space_type": "Metric Proximity", "tags": ["metric_proximity"]}
    assert is_proximity_space(space) is True
    assert is_close({1}, {2}, space) is True
    compactification = smirnov_compactification(space)
    assert compactification["compactification_type"] == "Smirnov compactification"
    assert compactification["version"] == "0.1.105"


def test_non_proximity_space_stays_negative_v105():
    mystery = {"space_type": "plain symbolic space"}
    assert is_proximity_space(mystery) is False
    assert is_close("A", "B", mystery) is False
    assert smirnov_compactification(mystery) is None


def test_explicit_smirnov_descriptor_is_preserved_v105():
    space = _Tagged(
        "proximity_space",
        smirnov_compactification={
            "compactification_type": "Smirnov compactification",
            "carrier_hint": "beta-like envelope",
        },
    )
    compactification = smirnov_compactification(space)
    assert compactification["carrier_hint"] == "beta-like envelope"
    assert compactification["version"] == "0.1.105"
