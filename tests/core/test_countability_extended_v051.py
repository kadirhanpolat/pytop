"""Coverage-targeted tests for countability.py (v0.5.1)."""
import pytest
from pytop.countability import (
    CountabilityError,
    normalize_countability_property,
    render_countability_report,
    _status_label,
    _space_name,
)
from pytop.result import Result


# ---------------------------------------------------------------------------
# normalize_countability_property — line 41 (unsupported raises)
# ---------------------------------------------------------------------------

def test_normalize_countability_property_unsupported_raises():
    with pytest.raises(CountabilityError, match="Unsupported countability property"):
        normalize_countability_property("bad_invariant_name")


def test_normalize_countability_property_alias():
    assert normalize_countability_property("first") == "first_countable"


def test_normalize_countability_property_second():
    assert normalize_countability_property("second") == "second_countable"


# ---------------------------------------------------------------------------
# _status_label — line 274 (conditional result)
# ---------------------------------------------------------------------------

def test_status_label_conditional():
    result = Result(status="conditional", mode="symbolic", value="some_condition")
    label = _status_label(result)
    assert label == "conditional"


def test_status_label_true():
    result = Result(status="true", mode="exact", value=True)
    label = _status_label(result)
    assert label == "yes"


# ---------------------------------------------------------------------------
# _space_name — line 283 (metadata has "name" key)
# ---------------------------------------------------------------------------

class _NamedMetaSpace:
    tags = ["first_countable"]
    metadata = {"name": "MySpace"}


def test_space_name_from_metadata_name():
    name = _space_name(_NamedMetaSpace())
    assert name == "MySpace"


class _LabelMetaSpace:
    tags = ["first_countable"]
    metadata = {"label": "LabelledSpace"}


def test_space_name_from_metadata_label():
    name = _space_name(_LabelMetaSpace())
    assert name == "LabelledSpace"


# ---------------------------------------------------------------------------
# render_countability_report — exercise _status_label and _space_name
# ---------------------------------------------------------------------------

def test_render_countability_report_named_space():
    result = render_countability_report(_NamedMetaSpace())
    assert isinstance(result, str)
    assert "MySpace" in result
