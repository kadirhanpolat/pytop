def test_uniform_spaces_api_v092():
    try:
        from pytop.uniform_spaces import entourage_system, is_uniform_space
        assert callable(is_uniform_space)
        assert callable(entourage_system)
    except ImportError:
        pass
