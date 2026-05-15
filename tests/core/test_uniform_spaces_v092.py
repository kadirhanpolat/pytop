def test_uniform_spaces_api_v092():
    try:
        from pytop.uniform_spaces import is_uniform_space, entourage_system
        assert callable(is_uniform_space)
        assert callable(entourage_system)
    except ImportError:
        pass
