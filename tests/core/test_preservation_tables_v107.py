from pytop.preservation_tables import (
    PreservationError,
    get_preservation_by_continuous_maps,
    get_preservation_by_products,
)


def test_continuous_image_benchmarks_v107():
    assert get_preservation_by_continuous_maps("compactness") is True
    assert get_preservation_by_continuous_maps("connectedness") is True
    assert get_preservation_by_continuous_maps("hausdorff") is False


def test_arbitrary_product_benchmarks_v107():
    assert get_preservation_by_products("compactness") is True
    assert get_preservation_by_products("connectedness") is True
    assert get_preservation_by_products("normality") is False


def test_query_helpers_remain_case_insensitive_v107():
    assert get_preservation_by_continuous_maps("COMPACTNESS") is True
    assert get_preservation_by_products("Paracompactness") is False


def test_query_helpers_raise_on_unknown_property_v107():
    try:
        get_preservation_by_continuous_maps("totally_fake_property")
    except PreservationError:
        pass
    else:
        raise AssertionError("Expected PreservationError for unknown property")
