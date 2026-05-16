"""Coverage-targeted tests for infinite_separation.py (v0.5.1)."""
from pytop.infinite_separation import analyze_infinite_separation, infinite_separation_report


class _Obj:
    tags: set = set()
    metadata: dict = {}


# ---------------------------------------------------------------------------
# analyze_infinite_separation — line 59 (non-InfiniteTopologicalSpace delegates)
# ---------------------------------------------------------------------------

def test_analyze_infinite_separation_non_infinite_delegates():
    result = analyze_infinite_separation(_Obj(), "hausdorff")
    assert result is not None


# ---------------------------------------------------------------------------
# infinite_separation_report — line 129 (non-InfiniteTopologicalSpace delegates)
# ---------------------------------------------------------------------------

def test_infinite_separation_report_non_infinite_delegates():
    result = infinite_separation_report(_Obj())
    assert isinstance(result, dict)
