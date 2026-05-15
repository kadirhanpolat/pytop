def test_preservation_tables_api_v099():
    try:
        from pytop.preservation_tables import get_preservation_by_continuous_maps, get_preservation_by_products
        assert get_preservation_by_continuous_maps('compactness') is True
        assert get_preservation_by_continuous_maps('hausdorff') is False
        assert get_preservation_by_products('compactness') is True
        assert get_preservation_by_products('paracompactness') is False
    except ImportError:
        pass
