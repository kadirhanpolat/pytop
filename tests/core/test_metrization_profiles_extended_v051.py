"""Coverage-targeted tests for metrization_profiles.py (v0.5.1)."""
from pytop.metrization_profiles import is_metrizable


class _MetaReprSpace:
    tags: set = set()
    metadata: dict = {"representation": "metric_space"}


class _AttrReprSpace:
    tags: set = set()
    metadata: dict = {}
    representation = "custom_attr"


# ---------------------------------------------------------------------------
# _representation_of — line 114 (metadata has "representation" key)
# ---------------------------------------------------------------------------

def test_is_metrizable_representation_from_metadata():
    result = is_metrizable(_MetaReprSpace())
    assert result is not None


# ---------------------------------------------------------------------------
# _representation_of — line 117 (space has .representation attribute)
# ---------------------------------------------------------------------------

def test_is_metrizable_representation_from_attr():
    result = is_metrizable(_AttrReprSpace())
    assert result is not None
