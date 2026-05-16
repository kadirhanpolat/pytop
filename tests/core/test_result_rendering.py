"""Tests for result_rendering.py."""

import pytest

from pytop.result import Result
from pytop.result_rendering import (
    explain_result,
    normalize_result_source,
    render_result,
    render_result_collection,
    result_mode_label,
    result_status_label,
)


def _true_result(value="x"):
    return Result.true(mode="exact", value=value, justification=["It holds."])


def _false_result():
    return Result.false(mode="theorem", value="y", justification=["It fails."])


def _unknown_result():
    return Result.unknown(mode="symbolic")


class _ContractLike:
    def to_result(self) -> Result:
        return _true_result()


class _BadContract:
    def to_result(self):
        return "not a result"


# ---------------------------------------------------------------------------
# normalize_result_source
# ---------------------------------------------------------------------------

class TestNormalizeResultSource:
    def test_result_passes_through(self):
        r = _true_result()
        assert normalize_result_source(r) is r

    def test_contract_like_is_unwrapped(self):
        r = normalize_result_source(_ContractLike())
        assert isinstance(r, Result)
        assert r.is_true

    def test_bad_contract_raises_type_error(self):
        with pytest.raises(TypeError):
            normalize_result_source(_BadContract())

    def test_unknown_object_raises_type_error(self):
        with pytest.raises(TypeError):
            normalize_result_source(42)


# ---------------------------------------------------------------------------
# result_status_label / result_mode_label
# ---------------------------------------------------------------------------

class TestLabels:
    def test_true_status_label(self):
        assert result_status_label(_true_result()) == "TRUE"

    def test_false_status_label(self):
        assert result_status_label(_false_result()) == "FALSE"

    def test_unknown_status_label(self):
        assert result_status_label(_unknown_result()) == "UNKNOWN"

    def test_exact_mode_label(self):
        assert result_mode_label(_true_result()) == "exact"

    def test_theorem_mode_label(self):
        assert result_mode_label(_false_result()) == "theorem-based"


# ---------------------------------------------------------------------------
# explain_result
# ---------------------------------------------------------------------------

class TestExplainResult:
    def test_status_and_mode_match(self):
        e = explain_result(_true_result())
        assert e.status == "true"
        assert e.mode == "exact"

    def test_headline_populated(self):
        e = explain_result(_true_result())
        assert "holds" in e.headline

    def test_label_trimmed(self):
        e = explain_result(_true_result(), label="  my label  ")
        assert e.label == "my label"

    def test_empty_label_becomes_none(self):
        e = explain_result(_true_result(), label="   ")
        assert e.label is None

    def test_justification_propagated(self):
        e = explain_result(_true_result())
        assert "It holds." in e.justification

    def test_metadata_excluded_by_default(self):
        r = Result.true(mode="exact", value="v", metadata={"k": "val"})
        e = explain_result(r)
        assert e.metadata == {}

    def test_metadata_included_when_flag_set(self):
        r = Result.true(mode="exact", value="v", metadata={"k": "val"})
        e = explain_result(r, include_metadata=True)
        assert e.metadata["k"] == "val"

    def test_badge_format(self):
        e = explain_result(_true_result())
        assert e.badge == "[TRUE/exact]"

    def test_unknown_gets_default_justification(self):
        e = explain_result(_unknown_result())
        assert len(e.justification) > 0


# ---------------------------------------------------------------------------
# ResultExplanation.to_dict / plain_lines / markdown_lines
# ---------------------------------------------------------------------------

class TestResultExplanation:
    def test_to_dict_keys(self):
        e = explain_result(_true_result(), label="lbl")
        d = e.to_dict()
        for key in ("status", "mode", "label", "badge", "headline", "value",
                    "assumptions", "justification", "proof_outline", "metadata"):
            assert key in d

    def test_plain_lines_include_badge(self):
        e = explain_result(_true_result())
        lines = e.plain_lines()
        assert any("[TRUE" in line for line in lines)

    def test_plain_lines_include_justification(self):
        e = explain_result(_true_result())
        lines = e.plain_lines()
        assert any("It holds." in line for line in lines)

    def test_markdown_lines_include_heading(self):
        e = explain_result(_true_result(), label="MyLabel")
        lines = e.markdown_lines()
        assert any("###" in line for line in lines)

    def test_plain_lines_with_metadata(self):
        r = Result.true(mode="exact", value="v", metadata={"k": 1})
        e = explain_result(r, include_metadata=True)
        lines = e.plain_lines(include_metadata=True)
        assert any("metadata" in line for line in lines)

    def test_markdown_lines_with_metadata(self):
        r = Result.true(mode="exact", value="v", metadata={"k": 1})
        e = explain_result(r, include_metadata=True)
        lines = e.markdown_lines(include_metadata=True)
        assert any("Metadata" in line for line in lines)


# ---------------------------------------------------------------------------
# render_result
# ---------------------------------------------------------------------------

class TestRenderResult:
    def test_plain_style_returns_string(self):
        s = render_result(_true_result())
        assert isinstance(s, str)
        assert "[TRUE" in s

    def test_markdown_style_returns_string(self):
        s = render_result(_true_result(), style="markdown")
        assert "###" in s

    def test_unknown_style_raises(self):
        with pytest.raises(ValueError):
            render_result(_true_result(), style="html")

    def test_label_appears_in_output(self):
        s = render_result(_true_result(), label="TestLabel")
        assert "TestLabel" in s


# ---------------------------------------------------------------------------
# render_result_collection
# ---------------------------------------------------------------------------

class TestRenderResultCollection:
    def test_two_results_are_separated(self):
        s = render_result_collection([_true_result(), _false_result()])
        assert "---" in s

    def test_label_mismatch_raises(self):
        with pytest.raises(ValueError):
            render_result_collection([_true_result()], labels=["a", "b"])

    def test_markdown_separator(self):
        s = render_result_collection([_true_result(), _unknown_result()], style="markdown")
        assert "---" in s

    def test_empty_collection(self):
        s = render_result_collection([])
        assert s == ""
