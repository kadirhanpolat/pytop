from pytop.dimension_theory import (
    Ind,
    dim,
    has_clopen_base,
    ind,
    is_totally_disconnected,
    is_zero_dimensional,
)


class _TaggedSpace:
    def __init__(self, *tags, representation="symbolic_general", name="space", **metadata):
        self.tags = set(tags)
        self.metadata = {"tags": list(tags), "representation": representation, "name": name, **metadata}
        self.representation = representation
        self.name = name


def test_dimension_functions_use_explicit_numeric_fields_v103():
    space = {"space_type": "R^3", "ind": 3, "Ind": 3, "dim": 3}
    assert ind(space) == 3
    assert Ind(space) == 3
    assert dim(space) == 3


def test_dimension_functions_read_examples_bank_shapes_v103():
    space = {"space_type": "Cantor Set", "ind": 0, "Ind": 0, "dim": 0, "is_zero_dimensional": True}
    assert ind(space) == 0
    assert Ind(space) == 0
    assert dim(space) == 0


def test_dimension_functions_can_infer_from_space_type_v103():
    assert ind({"space_type": "R^2"}) == 2
    assert dim({"space_type": "Cantor Set"}) == 0


def test_zero_dimensionality_positive_corridor_v103():
    space = _TaggedSpace("cantor_set", "zero_dimensional", representation="benchmark_space", name="Cantor")
    assert has_clopen_base(space) is True
    assert is_zero_dimensional(space) is True
    assert is_totally_disconnected(space) is True


def test_zero_dimensionality_explicit_negative_tag_v103():
    space = _TaggedSpace("not_zero_dimensional", representation="benchmark_space", name="R")
    assert has_clopen_base(space) is False
    assert is_zero_dimensional(space) is False


def test_totally_disconnected_explicit_flag_v103():
    space = {"is_totally_disconnected": True, "representation": "symbolic_general"}
    assert is_totally_disconnected(space) is True


def test_unknown_dimension_stays_none_v103():
    space = _TaggedSpace("metrizable", representation="symbolic_general", name="mystery")
    assert ind(space) is None
    assert Ind(space) is None
    assert dim(space) is None
