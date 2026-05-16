"""Coverage-targeted tests for predicates.py (v0.5.1)."""
import pytest
from pytop.predicates import PredicateError, _finite_predicate_result
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# _finite_predicate_result — line 210 (unsupported predicate name raises)
# ---------------------------------------------------------------------------

def test_finite_predicate_result_unsupported_name_raises():
    space = FiniteTopologicalSpace(
        carrier=frozenset({1, 2}),
        topology=frozenset([frozenset(), frozenset({1, 2})]),
    )
    with pytest.raises(PredicateError, match="Unexpected"):
        _finite_predicate_result(space, "perfect", {1})
