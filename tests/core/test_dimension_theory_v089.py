def test_dimension_theory_api_v089():
    try:
        from pytop.dimension_theory import Ind, dim, ind
        assert callable(ind)
        assert callable(Ind)
        assert callable(dim)
    except ImportError:
        pass
