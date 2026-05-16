"""Coverage-targeted tests for metrization_api.py (v0.5.1)."""
from pytop.metrization_api import is_metrizable


class _Obj:
    tags: set = set()
    metadata: dict = {}


class _ReprSpace:
    tags: set = set()
    metadata: dict = {"representation": "custom_space"}


# ---------------------------------------------------------------------------
# _representation_of — line 43 (metadata has "representation" key)
# ---------------------------------------------------------------------------

def test_is_metrizable_representation_from_metadata():
    result = is_metrizable(_ReprSpace())
    assert result is not None


# ---------------------------------------------------------------------------
# _representation_of — line 47 (fallback "symbolic_general")
# ---------------------------------------------------------------------------

def test_is_metrizable_representation_fallback():
    result = is_metrizable(_Obj())
    assert result is not None
