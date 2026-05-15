from pytop.uniform_spaces import (
    entourage_system,
    is_cauchy_filter,
    is_uniform_space,
    is_uniformly_complete,
    is_uniformly_continuous,
)


class _Tagged:
    def __init__(self, *tags, **metadata):
        self.tags = set(tags)
        self.metadata = {"tags": list(tags), **metadata}


def test_uniform_space_explicit_entourage_descriptor_v104():
    space = {"entourages": ["epsilon_ball_entourages"], "representation": "metric_uniformity"}
    assert is_uniform_space(space) is True
    assert entourage_system(space) == ["epsilon_ball_entourages"]


def test_uniform_space_metric_benchmark_v104():
    space = {"space_type": "Metric Uniformity", "tags": ["metric_uniformity", "complete_metric"]}
    assert is_uniform_space(space) is True
    assert "epsilon_ball_entourages" in entourage_system(space)
    assert is_uniformly_complete(space) is True


def test_uniform_space_discrete_benchmark_v104():
    space = _Tagged("discrete_uniformity", space_type="Discrete Uniformity")
    assert is_uniform_space(space) is True
    assert is_uniformly_complete(space) is True
    assert entourage_system(space)[0] == "diagonal_subset"


def test_uniformly_continuous_lipschitz_map_v104():
    mapping = {"lipschitz_constant": 3, "representation": "symbolic_map"}
    assert is_uniformly_continuous(mapping) is True


def test_uniformly_continuous_negative_tag_v104():
    mapping = _Tagged("not_uniformly_continuous", representation="symbolic_map")
    assert is_uniformly_continuous(mapping) is False


def test_principal_filter_is_cauchy_in_uniform_space_v104():
    filter_obj = {"filter_type": "principal"}
    uniform_space = {"tags": ["metric_uniformity"]}
    assert is_cauchy_filter(filter_obj, uniform_space) is True


def test_nonuniform_space_cannot_host_cauchy_filter_v104():
    assert is_cauchy_filter({"filter_type": "principal"}, None) is False


def test_unknown_uniform_space_stays_negative_v104():
    mystery = {"representation": "symbolic_general"}
    assert is_uniform_space(mystery) is False
    assert entourage_system(mystery) is None
    assert is_uniformly_complete(mystery) is False
