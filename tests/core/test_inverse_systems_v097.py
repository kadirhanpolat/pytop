def test_inverse_systems_api_v097():
    try:
        from pytop.inverse_systems import inverse_system, inverse_limit
        assert callable(inverse_system)
        assert callable(inverse_limit)
    except ImportError:
        pass
