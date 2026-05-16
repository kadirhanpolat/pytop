"""Coverage-targeted tests for theorem_engine.py (v0.5.1)."""
import pytest
from pytop.theorem_engine import (
    TheoremRule,
    TheoremEngine,
    theorem_result,
    extract_tags,
    extract_representation,
    _merged_rule_value,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _Obj:
    def __init__(self, tags=(), metadata=None):
        self.tags = set(tags)
        self.metadata = metadata or {}


# ---------------------------------------------------------------------------
# TheoremEngine.infer — status="false" (lines 87-88, 121-136)
# ---------------------------------------------------------------------------

def test_infer_status_false():
    engine = TheoremEngine([
        TheoremRule(
            name="not_compact_rule",
            feature="compactness",
            conclusion=False,
            requires_all={"not_compact"},
            justification=["Tagged not_compact."],
        )
    ])
    obj = _Obj(tags={"not_compact"})
    result = engine.infer("compactness", obj)
    assert result.is_false
    assert result.mode == "theorem"


# ---------------------------------------------------------------------------
# TheoremEngine.infer — status="conditional" (lines 89-90)
# ---------------------------------------------------------------------------

def test_infer_status_conditional():
    engine = TheoremEngine([
        TheoremRule(name="r_true", feature="prop_x", conclusion=True,
                    requires_all={"tag_a"}, justification=["True path."]),
        TheoremRule(name="r_false", feature="prop_x", conclusion=False,
                    requires_all={"tag_b"}, justification=["False path."]),
    ])
    obj = _Obj(tags={"tag_a", "tag_b"})
    result = engine.infer("prop_x", obj)
    # mixed conclusions → conditional
    assert result.mode == "theorem"
    assert not result.is_true
    assert not result.is_false


# ---------------------------------------------------------------------------
# theorem_result — backward-compatible helper (line 298)
# ---------------------------------------------------------------------------

def test_theorem_result_basic():
    result = theorem_result("X is compact.", assumptions=["X is metrizable."])
    assert result.is_true
    assert result.mode == "theorem"


def test_theorem_result_no_assumptions():
    result = theorem_result("Y is connected.")
    assert result.is_true
    assert result.assumptions == []


# ---------------------------------------------------------------------------
# extract_tags — is_finite() raises (lines 338-339)
# ---------------------------------------------------------------------------

def test_extract_tags_is_finite_raises():
    class FiniteRaises:
        tags = {"metrizable"}
        metadata = {}
        def is_finite(self):
            raise RuntimeError("broken is_finite")

    tags = extract_tags(FiniteRaises())
    assert "metrizable" in tags
    assert "finite" not in tags  # exception swallowed


# ---------------------------------------------------------------------------
# extract_representation — "finite" via tags (line 352)
# ---------------------------------------------------------------------------

def test_extract_representation_via_finite_tag():
    obj = _Obj(tags={"finite"})
    rep = extract_representation(obj)
    assert rep == "finite"


def test_extract_representation_via_metadata():
    obj = _Obj(metadata={"representation": "infinite_metric"})
    rep = extract_representation(obj)
    assert rep == "infinite_metric"


# ---------------------------------------------------------------------------
# _merged_rule_value — inconsistent values (line 375)
# ---------------------------------------------------------------------------

def test_merged_rule_value_inconsistent():
    rules = [
        TheoremRule(name="r1", feature="f", result_value="val_a"),
        TheoremRule(name="r2", feature="f", result_value="val_b"),
    ]
    result = _merged_rule_value(rules, "default")
    assert result == ["val_a", "val_b"]


def test_merged_rule_value_consistent():
    rules = [
        TheoremRule(name="r1", feature="f", result_value="same"),
        TheoremRule(name="r2", feature="f", result_value="same"),
    ]
    result = _merged_rule_value(rules, "default")
    assert result == "same"


def test_merged_rule_value_all_none():
    rules = [
        TheoremRule(name="r1", feature="f", result_value=None),
    ]
    result = _merged_rule_value(rules, "default_val")
    assert result == "default_val"


# ---------------------------------------------------------------------------
# extract_tags — dict input path
# ---------------------------------------------------------------------------

def test_extract_tags_from_dict():
    obj = {"tags": ["compact", "hausdorff"], "representation": "finite"}
    tags = extract_tags(obj)
    assert "compact" in tags
    assert "finite" in tags


# ---------------------------------------------------------------------------
# TheoremEngine.infer — no matched rules → unknown
# ---------------------------------------------------------------------------

def test_infer_no_match_returns_unknown():
    engine = TheoremEngine([
        TheoremRule(name="r", feature="prop", conclusion=True,
                    requires_all={"special_tag"}),
    ])
    obj = _Obj(tags={"other_tag"})
    result = engine.infer("prop", obj)
    assert result.is_unknown
