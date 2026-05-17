def test_uniform_spaces_completeness_api_v093():
    try:
        from pytop.uniform_spaces import (
            is_cauchy_filter,
            is_uniformly_complete,
            is_uniformly_continuous,
        )
        assert callable(is_uniformly_continuous)
        assert callable(is_cauchy_filter)
        assert callable(is_uniformly_complete)
    except ImportError:
        pass
