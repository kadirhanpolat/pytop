def test_inverse_systems_api_v097():
    try:
        from pytop.inverse_systems import inverse_limit, inverse_system
        assert callable(inverse_system)
        assert callable(inverse_limit)
    except ImportError:
        pass
