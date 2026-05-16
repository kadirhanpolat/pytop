"""Coverage-targeted tests for cardinal_function_examples.py (v0.5.1)."""
import pytest
from pytop.cardinal_function_examples import (
    CardinalFunctionExampleError,
    CardinalFunctionComparisonRoute,
    cardinal_function_examples_by_layer,
    _validate_route_examples,
)


# ---------------------------------------------------------------------------
# cardinal_function_examples_by_layer — line 504 (unknown layer raises)
# ---------------------------------------------------------------------------

def test_cardinal_function_examples_by_layer_unknown_raises():
    with pytest.raises(CardinalFunctionExampleError, match="Unknown cardinal-function example layer"):
        cardinal_function_examples_by_layer("bad_nonexistent_layer")


def test_cardinal_function_examples_by_layer_valid():
    # Grab a layer from one of the existing examples
    from pytop.cardinal_function_examples import cardinal_function_examples_catalog
    catalog = cardinal_function_examples_catalog()
    if catalog:
        layer = catalog[0]["layer"]
        result = cardinal_function_examples_by_layer(layer)
        assert isinstance(result, tuple)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# _validate_route_examples — line 545 (route references unknown examples)
# ---------------------------------------------------------------------------

def test_validate_route_examples_unknown_key_raises():
    route = CardinalFunctionComparisonRoute(
        route_id="test_route",
        title="Test Route",
        comparison_pair=("weight", "density"),
        objective="test",
        example_keys=("nonexistent_key_xyz",),
        exploration_notebook="nb.ipynb",
        teaching_notebook="teach.ipynb",
        examples_bank="bank.md",
        manuscript_chapter="ch1",
        task_prompts=("task1",),
        expected_distinctions=("dist1",),
    )
    with pytest.raises(CardinalFunctionExampleError, match="references unknown examples"):
        _validate_route_examples(route)
