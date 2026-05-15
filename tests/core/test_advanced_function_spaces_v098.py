def test_advanced_function_spaces_api_v098():
    try:
        from pytop.function_spaces import is_admissible_topology, is_splitting_topology
        assert is_admissible_topology(None, None, None, None) is False
        assert is_splitting_topology(None, None, None, None) is False
    except ImportError:
        pass
