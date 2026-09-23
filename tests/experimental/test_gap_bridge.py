"""Tests for :mod:`pytop.experimental.gap_bridge`.

Most tests need no Docker: code generation, validation, parsing and result
semantics are all exercised offline. Only the round-trips are opt-in via
``PYTOP_GAP_BRIDGE=1``, following the existing ``PYTOP_SAGE_ORACLE`` pattern.

Several tests name the review finding they guard; those are regression tests for
defects that a security/correctness review reproduced live, and they must not be
simplified away.
"""

from __future__ import annotations

import os

import pytest

from pytop.experimental.gap_bridge import (
    GapGroupInfo,
    GapSession,
    GapTimeout,
    GapUnavailableError,
    _generate_query,
    _parse_response,
    _relator_to_gap,
    gap_abelian_invariants,
    gap_available,
    gap_group_info,
)
from pytop.van_kampen import GroupPresentation

requires_gap = pytest.mark.skipif(
    os.environ.get("PYTOP_GAP_BRIDGE") != "1",
    reason="set PYTOP_GAP_BRIDGE=1 to run the (slow, Docker-based) GAP bridge",
)

TORUS = GroupPresentation(
    generators=("a", "b"),
    relators=((("a", 1), ("b", 1), ("a", -1), ("b", -1)),),
)
KLEIN = GroupPresentation(
    generators=("a", "b"),
    relators=((("a", 1), ("b", 1), ("a", 1), ("b", -1)),),
)
RP2 = GroupPresentation(generators=("a",), relators=((("a", 2),),))
TRIVIAL = GroupPresentation(generators=(), relators=())


# ---------------------------------------------------------------------------
# Code generation and injection safety
# ---------------------------------------------------------------------------


def test_generators_are_emitted_positionally() -> None:
    """No generator name may appear in generated source."""
    src = _generate_query(TORUS)
    assert "FreeGroup(2)" in src
    assert "f.1" in src and "f.2" in src
    assert '"a"' not in src and '"b"' not in src


def test_generator_name_payload_never_reaches_the_source() -> None:
    """Guard: names are user-controlled and are never interpolated."""
    payload = 'x"); Exec("id > /tmp/PWNED"); f := FreeGroup("y'
    evil = GroupPresentation(
        generators=(payload, "b"), relators=(((payload, 1), ("b", 1)),)
    )
    src = _generate_query(evil)
    assert "Exec" not in src
    assert "PWNED" not in src
    assert payload not in src


def test_exponent_payload_is_rejected_before_any_container_is_touched() -> None:
    """Guard: the defect a security review demonstrated as container RCE.

    `GroupPresentation` does not validate exponents and Python does not enforce
    the `int` annotation, so a string exponent used to flow straight into the
    generated source and execute.
    """
    payload = '1 ];; Exec("id > /tmp/PWNED");; g := f / [ f.1'
    evil = GroupPresentation(generators=("a",), relators=((("a", payload),),))
    with pytest.raises(ValueError, match="exponent"):
        _generate_query(evil)


@pytest.mark.parametrize("bad", [1.0, "2", None, True, False, complex(1, 0)])
def test_non_integer_exponents_are_rejected(bad: object) -> None:
    """`bool` is excluded deliberately: True would silently render as 1."""
    pres = GroupPresentation(generators=("a",), relators=((("a", bad),),))
    with pytest.raises(ValueError, match="exponent"):
        _generate_query(pres)


def test_absurd_exponent_magnitude_is_rejected() -> None:
    pres = GroupPresentation(generators=("a",), relators=((("a", 10**9),),))
    with pytest.raises(ValueError, match="magnitude"):
        _generate_query(pres)


def test_unknown_generator_is_rejected_by_the_emitter() -> None:
    """The emitter does not delegate this to GroupPresentation.__post_init__."""
    with pytest.raises(ValueError, match="unknown generator"):
        _relator_to_gap(((("z"), 1),), {"a": 1})


def test_relator_rendering() -> None:
    assert _relator_to_gap(TORUS.relators[0], {"a": 1, "b": 2}) == (
        "f.1^1*f.2^1*f.1^-1*f.2^-1"
    )


def test_trivial_presentation_generates_free_group_zero() -> None:
    assert "FreeGroup(0)" in _generate_query(TRIVIAL)


# ---------------------------------------------------------------------------
# Generated-script mechanics that a review found load-bearing
# ---------------------------------------------------------------------------


def test_script_never_puts_a_newline_escape_inside_a_gap_string() -> None:
    """A newline inside a GAP string is a syntax error, and parser recovery then
    swallows the rest of the input -- producing empty stdout with exit code 0."""
    src = _generate_query(TORUS)
    assert "\\n" not in src
    assert "Chr(10)" in src


def test_script_sets_size_screen_to_defeat_column_wrapping() -> None:
    """Without this GAP wraps at 80 columns, splitting long invariant lists."""
    assert "SizeScreen(" in _generate_query(TORUS)


def test_script_guards_idgroup_by_order() -> None:
    """SmallGroups does not cover every order; an unguarded IdGroup break-loops."""
    src = _generate_query(TORUS)
    assert "IdGroup" in src
    assert "512" in src and "1024" in src


def test_script_ends_with_the_sentinel() -> None:
    """Success is detected by the sentinel; GAP exits 0 on errors too."""
    assert "@@PYTOP_GAP_OK@@" in _generate_query(TORUS)


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------


def test_parse_finite_group_with_small_group_id() -> None:
    info = _parse_response("SIZE=8|ABI=[ 2, 2 ]|ID=[ 8, 4 ]|@@PYTOP_GAP_OK@@")
    assert info.order == 8
    assert info.is_finite is True
    assert info.abelian_invariants == (2, 2)
    assert info.small_group_id == (8, 4)


def test_parse_infinite_group() -> None:
    info = _parse_response("SIZE=infinity|ABI=[ 0, 0 ]|ID=NONE|@@PYTOP_GAP_OK@@")
    assert info.is_finite is False
    assert info.order is None
    assert info.abelian_invariants == (0, 0)
    assert info.small_group_id is None


def test_parse_trivial_group_has_empty_not_none_invariants() -> None:
    """`()` is a legitimate value; it must not double as "not determined"."""
    info = _parse_response("SIZE=1|ABI=[  ]|ID=[ 1, 1 ]|@@PYTOP_GAP_OK@@")
    assert info.abelian_invariants == ()
    assert info.abelian_invariants is not None
    assert info.order == 1


def test_parse_order_without_small_groups_coverage() -> None:
    body = "SIZE=512|ABI=[ 2, 2, 2, 2, 2, 2, 2, 2, 2 ]|ID=NONE|@@PYTOP_GAP_OK@@"
    info = _parse_response(body)
    assert info.order == 512
    assert info.small_group_id is None
    assert len(info.abelian_invariants or ()) == 9


def test_missing_sentinel_is_a_failure_even_with_plausible_content() -> None:
    """GAP exits 0 on break loops and writes its prompt into stdout."""
    broken = (
        "SIZE=512|ABI=[ 2, 2 ]|you can 'quit;' to quit to outer loop, or\n"
        "you can 'return;' to continue\n\x1b[1m\x1b[34m"
    )
    with pytest.raises(ValueError, match="sentinel"):
        _parse_response(broken)


def test_parse_tolerates_wrapped_continuations() -> None:
    """Defence in depth: SizeScreen should prevent this, parsing survives it."""
    info = _parse_response(
        "SIZE=1|ABI=[ 0, 0, 0,\n  0, 0 ]|ID=NONE|@@PYTOP_GAP_OK@@"
    )
    assert info.abelian_invariants == (0, 0, 0, 0, 0)


# ---------------------------------------------------------------------------
# Result semantics
# ---------------------------------------------------------------------------


def test_undetermined_is_distinguishable_from_every_legitimate_value() -> None:
    undetermined = GapGroupInfo(
        abelian_invariants=None,
        is_finite=None,
        order=None,
        structure_description=None,
        small_group_id=None,
    )
    trivial = GapGroupInfo(
        abelian_invariants=(),
        is_finite=True,
        order=1,
        structure_description="1",
        small_group_id=(1, 1),
    )
    assert undetermined.abelian_invariants is None
    assert trivial.abelian_invariants == ()
    assert not undetermined.determined
    assert trivial.determined


# ---------------------------------------------------------------------------
# Availability degrades gracefully
# ---------------------------------------------------------------------------


def test_gap_available_never_raises() -> None:
    assert isinstance(gap_available(), bool)


def test_unavailable_error_is_actionable() -> None:
    err = GapUnavailableError("x")
    assert isinstance(err, RuntimeError)


# ---------------------------------------------------------------------------
# Opt-in round trips
# ---------------------------------------------------------------------------


@requires_gap
def test_session_round_trip_torus() -> None:
    with GapSession() as session:
        info = gap_group_info(TORUS, session=session)
    assert info.is_finite is False
    assert info.abelian_invariants == (0, 0)


@requires_gap
def test_differential_abelianization_matches_pytop() -> None:
    """GAP as an independent oracle for pytop's own SNF abelianization.

    The two sides report the same group in different shapes: pytop returns
    ``HomologyResult(betti, torsion)`` while GAP returns a flat invariant list in
    which ``0`` marks an infinite cyclic factor. The correspondence asserted here
    is ``(0,) * betti + torsion``.
    """
    from pytop.van_kampen import _abelianize

    with GapSession() as session:
        for pres in (TORUS, KLEIN, RP2, TRIVIAL):
            ours = _abelianize(list(pres.generators), list(pres.relators))
            expected = (0,) * ours.betti + tuple(ours.torsion)
            theirs = gap_abelian_invariants(pres, session=session)
            assert tuple(sorted(theirs)) == tuple(sorted(expected)), pres.generators


@requires_gap
def test_identifies_a_group_pytop_cannot_name() -> None:
    q8 = GroupPresentation(
        generators=("a", "b"),
        relators=(
            (("a", 2), ("b", -2)),
            (("a", 2), ("a", -1), ("b", -1), ("a", -1), ("b", -1)),
        ),
    )
    with GapSession() as session:
        info = gap_group_info(q8, session=session)
    assert info.order == 8
    assert info.small_group_id == (8, 4)


@requires_gap
def test_long_invariant_list_is_not_wrapped() -> None:
    free40 = GroupPresentation(
        generators=tuple(f"g{i}" for i in range(40)), relators=()
    )
    with GapSession() as session:
        inv = gap_abelian_invariants(free40, session=session)
    assert len(inv) == 40


@requires_gap
def test_timeout_leaves_no_orphan_gap_process() -> None:
    """A client-side timeout does not stop GAP; the session must reap it."""
    spin = GroupPresentation(
        generators=("a", "b", "c"),
        relators=(
            (("a", -1), ("b", 1), ("a", 1), ("b", -2)),
            (("b", -1), ("c", 1), ("b", 1), ("c", -2)),
            (("c", -1), ("a", 1), ("c", 1), ("a", -2)),
        ),
    )
    with GapSession() as session:
        with pytest.raises(GapTimeout):
            session.evaluate(_generate_query(spin), timeout=1.0)
        assert session.running_gap_processes() == 0
