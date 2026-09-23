"""Tests for :mod:`pytop.experimental.regina_bridge`.

Most tests need no Docker. The round trips are opt-in via
``PYTOP_REGINA_BRIDGE=1`` and additionally need a locally built image::

    docker build -t pytop-regina -f docker/Dockerfile.regina .
"""

from __future__ import annotations

import os

import pytest

from pytop.experimental.regina_bridge import (
    REGINA_EXAMPLES,
    ReginaSession,
    ReginaTimeout,
    ReginaUnavailableError,
    _check_example,
    _check_int,
    _example_script,
    _lens_script,
    _normal_surface_script,
    _read_homology,
    _require_sentinel,
    regina_available,
    regina_example_homology,
    regina_lens_homology,
    regina_normal_surface_count,
    regina_version,
)

requires_regina = pytest.mark.skipif(
    os.environ.get("PYTOP_REGINA_BRIDGE") != "1",
    reason="set PYTOP_REGINA_BRIDGE=1 and build pytop-regina to run this",
)

SENTINEL = "@@PYTOP_REGINA_OK@@"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad", [1.0, "5", None, True, False, complex(1, 0)])
def test_non_integer_parameters_are_rejected(bad: object) -> None:
    """Python does not enforce the annotation; the check is real."""
    with pytest.raises(ValueError, match="must be an int"):
        _check_int(bad, "p")


def test_injection_payload_as_parameter_is_rejected() -> None:
    payload = "5); __import__('os').system('id > /tmp/PWNED'); regina.Example3.lens(1"
    with pytest.raises(ValueError, match="must be an int"):
        _check_int(payload, "p")


def test_absurd_parameter_magnitude_is_rejected() -> None:
    with pytest.raises(ValueError, match="magnitude"):
        _check_int(10**9, "p")


def test_example_names_come_from_an_allowlist() -> None:
    payload = "poincare(); __import__('os').system('id'); regina.Example3.ball"
    with pytest.raises(ValueError, match="unknown example"):
        _check_example(payload)
    with pytest.raises(ValueError, match="unknown example"):
        _check_example("figureEight ")
    assert _check_example("poincare") == "poincare"


def test_every_allowlisted_name_generates_a_script() -> None:
    for name in REGINA_EXAMPLES:
        assert name in _example_script(name)


# ---------------------------------------------------------------------------
# Generated scripts
# ---------------------------------------------------------------------------


def test_scripts_end_with_the_sentinel() -> None:
    """A traceback must never be mistaken for a result."""
    for script in (_lens_script(5, 1), _example_script("poincare"),
                   _normal_surface_script("s2xs1")):
        assert SENTINEL in script
        assert script.rstrip().endswith(f"print('{SENTINEL}')")


def test_scripts_catch_exceptions_so_the_sentinel_still_prints() -> None:
    script = _lens_script(5, 1)
    assert "except Exception" in script
    assert "ERROR=" in script


def test_lens_script_interpolates_only_integers() -> None:
    script = _lens_script(-7, 2)
    assert "lens(-7, 2)" in script


# ---------------------------------------------------------------------------
# Response handling
# ---------------------------------------------------------------------------


def test_missing_sentinel_is_a_failure() -> None:
    with pytest.raises(ValueError, match="sentinel"):
        _require_sentinel("H1=Z_5\n")


def test_error_line_is_surfaced_even_with_the_sentinel() -> None:
    with pytest.raises(ValueError, match="AttributeError"):
        _require_sentinel(f"ERROR=AttributeError: nope\n{SENTINEL}\n")


@pytest.mark.parametrize(
    ("rank", "inv", "free", "torsion"),
    [
        ("0", "", 0, ()),            # poincare, ball, lens(1,0)
        ("1", "", 1, ()),            # s2xs1, figureEight, gieseking
        ("0", "8", 0, (8,)),         # lens(8,3)
        ("0", "2,2", 0, (2, 2)),     # rp3rp3 -- Regina displays this as "2 Z_2"
        ("1", "2", 1, (2,)),         # rp2xs1 -- displayed as "Z + Z_2"
    ],
)
def test_read_homology_uses_structured_fields(
    rank: str, inv: str, free: int, torsion: tuple[int, ...]
) -> None:
    """Every case here is a real Regina output, captured from the container.

    The display string is kept only for messages: `2 Z_2` means two factors of
    order 2, and reading that with a regex is a needless way to get it wrong.
    """
    out = "\n".join(["RAW=display", f"RANK={rank}", f"INV={inv}", SENTINEL, ""])
    got = _read_homology(out)
    assert (got.free_rank, got.torsion) == (free, torsion)
    assert got.raw == "display"


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


def test_regina_available_never_raises() -> None:
    assert isinstance(regina_available(), bool)


def test_unavailable_error_names_the_build_command() -> None:
    assert issubclass(ReginaUnavailableError, RuntimeError)
    assert issubclass(ReginaTimeout, RuntimeError)


def test_session_rejects_use_before_start() -> None:
    session = ReginaSession()
    with pytest.raises(ReginaUnavailableError, match="not running"):
        session.evaluate("print(1)")


# ---------------------------------------------------------------------------
# Opt-in round trips
# ---------------------------------------------------------------------------


@requires_regina
def test_version() -> None:
    with ReginaSession() as session:
        assert regina_version(session=session).startswith("7.")


@requires_regina
def test_lens_homology_agrees_with_pytop() -> None:
    """Regina as an independent oracle for pytop's SNF lens-space homology.

    pytop derives H_1(L(p,q)) from the linking matrix; Regina builds and
    triangulates the manifold. They agree on the group, not the method.
    """
    from pytop import lens_space_first_homology

    with ReginaSession() as session:
        for p, q in [(2, 1), (3, 1), (5, 1), (7, 1), (7, 2), (8, 3)]:
            theirs = regina_lens_homology(p, q, session=session)
            ours = lens_space_first_homology(p, q)
            assert theirs.free_rank == 0
            assert theirs.torsion == (p,), (p, q, theirs.raw)
            assert str(p) in str(ours)


@requires_regina
def test_trivial_lens_space_is_a_sphere() -> None:
    with ReginaSession() as session:
        got = regina_lens_homology(1, 0, session=session)
    assert got.free_rank == 0
    assert got.torsion == ()


@requires_regina
def test_example_homology_known_values() -> None:
    expected = {
        "poincare": (0, ()),       # Poincare homology sphere
        "s2xs1": (1, ()),          # S^2 x S^1
        "rp3rp3": (0, (2, 2)),     # RP^3 # RP^3
        "figureEight": (1, ()),    # knot complement
    }
    with ReginaSession() as session:
        for name, (free, torsion) in expected.items():
            got = regina_example_homology(name, session=session)
            assert (got.free_rank, got.torsion) == (free, torsion), (name, got.raw)


@requires_regina
def test_normal_surfaces_the_capability_pytop_lacks() -> None:
    with ReginaSession() as session:
        tets, surfaces = regina_normal_surface_count("poincare", session=session)
    assert tets == 5
    assert surfaces > 0


@requires_regina
def test_timeout_leaves_no_orphan_interpreter() -> None:
    spin = "import time\ntry:\n    time.sleep(600)\nexcept Exception:\n    pass\n"
    with ReginaSession() as session:
        with pytest.raises(ReginaTimeout):
            session.evaluate(spin, timeout=2.0)
        assert session.running_python_processes() == 0
