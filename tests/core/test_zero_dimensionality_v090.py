def test_zero_dimensionality_api_v090():
    try:
        from pytop.dimension_theory import (
            has_clopen_base,
            is_totally_disconnected,
            is_zero_dimensional,
        )
        assert callable(is_zero_dimensional)
        assert callable(has_clopen_base)
        assert callable(is_totally_disconnected)
    except ImportError:
        pass
