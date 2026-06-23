"""Tests for the internal ``@deprecated`` decorator (P19.2)."""

from __future__ import annotations

import warnings

import pytest

from pytop._deprecation import deprecated, deprecation_message


def test_message_why_how_then():
    msg = deprecation_message(
        "old_fn", since="1.7.0", removed_in="2.0.0", alternative="new_fn"
    )
    assert "old_fn is deprecated since pytop 1.7.0" in msg
    assert "will be removed in 2.0.0" in msg
    assert "Use new_fn instead." in msg


def test_message_without_alternative():
    msg = deprecation_message("old_fn", since="1.7.0", removed_in="2.0.0")
    assert "Use" not in msg
    assert msg.endswith("removed in 2.0.0.")


def test_message_with_reason():
    msg = deprecation_message(
        "old_fn", since="1.7.0", removed_in="2.0.0", reason="It double-counts torsion."
    )
    assert msg.endswith("It double-counts torsion.")


def test_function_warns_on_call():
    @deprecated(since="1.7.0", removed_in="2.0.0", alternative="new_fn")
    def old_fn(x):
        return x * 2

    with pytest.warns(DeprecationWarning, match="old_fn is deprecated"):
        assert old_fn(21) == 42  # behavior preserved


def test_function_does_not_warn_until_called():
    @deprecated(since="1.7.0", removed_in="2.0.0")
    def old_fn():
        return 1

    with warnings.catch_warnings():
        warnings.simplefilter("error")  # any warning would raise
        # decorating must not warn; only calling does

    with pytest.warns(DeprecationWarning):
        old_fn()


def test_function_preserves_metadata_and_docstring():
    @deprecated(since="1.7.0", removed_in="2.0.0", alternative="new_fn")
    def old_fn():
        """Original docstring."""
        return 1

    assert old_fn.__name__ == "old_fn"
    assert "Original docstring." in old_fn.__doc__
    assert ".. deprecated:: 1.7.0" in old_fn.__doc__
    assert old_fn.__deprecated__ == {
        "since": "1.7.0",
        "removed_in": "2.0.0",
        "alternative": "new_fn",
    }


def test_class_warns_on_instantiation():
    @deprecated(since="1.7.0", removed_in="2.0.0", alternative="NewClass")
    class OldClass:
        def __init__(self, value):
            self.value = value

    with pytest.warns(DeprecationWarning, match="OldClass is deprecated"):
        obj = OldClass(7)
    assert obj.value == 7  # construction still works
    assert ".. deprecated:: 1.7.0" in OldClass.__doc__


def test_stacklevel_points_at_caller():
    @deprecated(since="1.7.0", removed_in="2.0.0")
    def old_fn():
        return 1

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        old_fn()
    assert len(caught) == 1
    # The warning should be attributed to this test file (the caller), not the
    # decorator's wrapper frame.
    assert caught[0].filename == __file__
