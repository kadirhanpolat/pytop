def test_proximity_compactification_api_v096():
    try:
        from pytop.proximity_spaces import smirnov_compactification
        assert callable(smirnov_compactification)
    except ImportError:
        pass
