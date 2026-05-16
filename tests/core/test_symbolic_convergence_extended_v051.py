"""Coverage-targeted tests for symbolic_convergence.py (v0.5.1)."""
from pytop.symbolic_convergence import _tags_of


class _MetaTagObj:
    tags: set = set()
    metadata: dict = {"tags": ["hausdorff", "compact"]}


# ---------------------------------------------------------------------------
# _tags_of — line 46 (metadata tags loop fires)
# ---------------------------------------------------------------------------

def test_tags_of_metadata_tags():
    result = _tags_of(_MetaTagObj())
    assert "hausdorff" in result
    assert "compact" in result
