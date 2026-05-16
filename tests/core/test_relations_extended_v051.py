"""Coverage-targeted tests for relations.py (v0.5.1)."""
from pytop.relations import is_linear_order


# ---------------------------------------------------------------------------
# is_linear_order — line 143 (not a partial order → return False)
# ---------------------------------------------------------------------------

def test_is_linear_order_not_partial_order_returns_false():
    # [(1, 2)] is not reflexive, so not a partial order → line 143
    result = is_linear_order([1, 2], [(1, 2)])
    assert result is False
