"""Coverage-targeted tests for sequences.py (v0.5.1)."""
from pytop.sequences import _minimal_open_neighborhood


# ---------------------------------------------------------------------------
# _minimal_open_neighborhood — line 328 (no neighborhoods → return frozenset())
# ---------------------------------------------------------------------------

def test_minimal_open_neighborhood_no_neighborhoods():
    # point 1 is not in any open set → neighborhoods=() → line 328
    data = {"opens": [frozenset(), frozenset({2, 3})], "points": frozenset({1, 2, 3})}
    result = _minimal_open_neighborhood(data, 1)
    assert result == frozenset()
