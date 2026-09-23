"""Tests for :mod:`pytop.experimental.snappy_bridge`.

Most tests need no Docker. Round trips are opt-in via ``PYTOP_SNAPPY_BRIDGE=1``
and need the ``pytop-snappy`` image (Dockerfile in
``tests/core/test_snappy_oracle.py``).
"""

from __future__ import annotations

import os

import pytest

from pytop.experimental.snappy_bridge import (
    SNAPPY_MANIFOLDS,
    SnappySession,
    SnappyTimeout,
    SnappyUnavailableError,
    _check_coefficient,
    _check_manifold,
    _info_script,
    _optional_float,
    _require_sentinel,
    _surgery_script,
    snappy_available,
    snappy_manifold_info,
    snappy_surgery_homology,
    snappy_version,
)

requires_snappy = pytest.mark.skipif(
    os.environ.get("PYTOP_SNAPPY_BRIDGE") != "1",
    reason="set PYTOP_SNAPPY_BRIDGE=1 and build pytop-snappy to run this",
)

SENTINEL = "@@PYTOP_SNAPPY_OK@@"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def test_manifold_names_come_from_an_allowlist() -> None:
    payload = "4_1'); __import__('os').system('id'); snappy.Manifold('4_1"
    with pytest.raises(ValueError, match="unknown manifold"):
        _check_manifold(payload)
    with pytest.raises(ValueError, match="unknown manifold"):
        _check_manifold("4_1 ")
    assert _check_manifold("4_1") == "4_1"


@pytest.mark.parametrize("bad", [1.0, "5", None, True, False, complex(1, 0)])
def test_non_integer_coefficients_are_rejected(bad: object) -> None:
    with pytest.raises(ValueError, match="must be an int"):
        _check_coefficient(bad, "p")


def test_absurd_coefficient_is_rejected() -> None:
    with pytest.raises(ValueError, match="magnitude"):
        _check_coefficient(10**9, "q")


def test_every_allowlisted_manifold_generates_a_script() -> None:
    for name in SNAPPY_MANIFOLDS:
        assert repr(name) in _info_script(name)


# ---------------------------------------------------------------------------
# Generated scripts
# ---------------------------------------------------------------------------


def test_scripts_end_with_the_sentinel() -> None:
    for script in (_info_script("4_1"), _surgery_script("4_1", 5, 1)):
        assert script.rstrip().endswith(f"print('{SENTINEL}')")


def test_scripts_catch_exceptions() -> None:
    assert "except Exception" in _info_script("4_1")


def test_surgery_script_interpolates_only_integers() -> None:
    assert "dehn_fill((-5, 2))" in _surgery_script("4_1", -5, 2)


def test_volume_failure_is_tolerated_in_the_script() -> None:
    """Not every manifold in the allowlist is hyperbolic."""
    assert "VOLUME=none" in _info_script("4_1")


# ---------------------------------------------------------------------------
# Response handling
# ---------------------------------------------------------------------------


def test_missing_sentinel_is_a_failure() -> None:
    with pytest.raises(ValueError, match="sentinel"):
        _require_sentinel("HOMOLOGY=Z\n")


def test_error_line_is_surfaced() -> None:
    with pytest.raises(ValueError, match="ValueError"):
        _require_sentinel(f"ERROR=ValueError: bad\n{SENTINEL}\n")


def test_optional_float() -> None:
    assert _optional_float("none") is None
    assert _optional_float("2.029883") == pytest.approx(2.029883)


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


def test_snappy_available_never_raises() -> None:
    assert isinstance(snappy_available(), bool)


def test_session_rejects_use_before_start() -> None:
    with pytest.raises(SnappyUnavailableError, match="not running"):
        SnappySession().evaluate("print(1)")


def test_error_types() -> None:
    assert issubclass(SnappyUnavailableError, RuntimeError)
    assert issubclass(SnappyTimeout, RuntimeError)


# ---------------------------------------------------------------------------
# Opt-in round trips
# ---------------------------------------------------------------------------


@requires_snappy
def test_version() -> None:
    with SnappySession() as session:
        assert snappy_version(session=session).startswith("3.")


@requires_snappy
def test_figure_eight_volume_and_identification() -> None:
    with SnappySession() as session:
        info = snappy_manifold_info("4_1", session=session)
    assert info.volume == pytest.approx(2.029883, abs=1e-5)
    assert info.homology == "Z"
    assert any("m004" in x for x in info.identifications)


@requires_snappy
def test_surgery_homology_agrees_with_pytop() -> None:
    """SnapPy fills a triangulation; pytop reduces a linking matrix.

    Only coefficients valid in both conventions are compared: pytop reads (p, q)
    as the fraction p/q and rejects q = 0, where SnapPy reads (1, 0) as a
    meridian filling.
    """
    from pytop import first_homology_of_surgery

    with SnappySession() as session:
        for p in (2, 3, 5, 7):
            theirs = snappy_surgery_homology("4_1", p, 1, session=session)
            ours = str(first_homology_of_surgery([(p, 1)], [[0]]))
            assert str(p) in theirs, (p, theirs)
            assert str(p) in ours, (p, ours)


@requires_snappy
def test_timeout_leaves_no_orphan_interpreter() -> None:
    spin = "import time\ntry:\n    time.sleep(600)\nexcept Exception:\n    pass\n"
    with SnappySession() as session:
        with pytest.raises(SnappyTimeout):
            session.evaluate(spin, timeout=2.0)
        assert session.running_python_processes() == 0
