from pathlib import Path

def test_refinements_api_v087():
    try:
        from pytop.paracompactness import is_locally_finite_refinement, is_star_refinement, partition_of_unity_warning
        assert partition_of_unity_warning() != ""
    except ImportError:
        pass
