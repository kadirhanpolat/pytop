"""WHY-HOW-THEN error-message guards (good-first-issue #7).

Extends the P19.1 trio: each validator must name the offending value *and* show a
concrete fix example (``docs/P19_API_STABILITY.md``). These tests lock the pattern
so the improved messages don't silently regress to terse one-liners.
"""

from __future__ import annotations

import pytest

from pytop import cech_filtration, signature_torus_knot


def test_cech_max_dimension_message():
    with pytest.raises(ValueError) as exc:
        cech_filtration([(0.0, 0.0), (1.0, 0.0)], max_dimension=-1)
    msg = str(exc.value)
    assert "-1" in msg            # names the offending value
    assert "max_dimension=1" in msg  # concrete fix example


def test_cech_empty_points_message():
    with pytest.raises(ValueError) as exc:
        cech_filtration([])
    msg = str(exc.value)
    assert "empty" in msg.lower()
    assert "cech_filtration([" in msg  # concrete fix example


def test_torus_knot_range_message():
    with pytest.raises(ValueError) as exc:
        signature_torus_knot(1, 3)
    msg = str(exc.value)
    assert "p=1" in msg
    assert "T(2,3)" in msg  # concrete fix example


def test_torus_knot_coprime_message():
    with pytest.raises(ValueError) as exc:
        signature_torus_knot(2, 4)
    msg = str(exc.value)
    assert "gcd(2,4)" in msg
    assert "T(" in msg  # concrete fix example
