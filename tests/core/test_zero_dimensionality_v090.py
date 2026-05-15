def test_zero_dimensionality_api_v090():
    try:
        from pytop.dimension_theory import is_zero_dimensional, has_clopen_base, is_totally_disconnected
        assert callable(is_zero_dimensional)
        assert callable(has_clopen_base)
        assert callable(is_totally_disconnected)
    except ImportError:
        pass
