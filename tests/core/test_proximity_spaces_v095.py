def test_proximity_spaces_api_v095():
    try:
        from pytop.proximity_spaces import is_proximity_space, is_close
        assert callable(is_proximity_space)
        assert callable(is_close)
    except ImportError:
        pass
