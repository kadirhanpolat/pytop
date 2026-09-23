"""Tests for :mod:`pytop.experimental.homeomorphism`.

The decision procedure is cross-validated against brute-force enumeration of all
bijections on every small space in the fixture set: for finite spaces "is there a
homeomorphism" has a definitive answer, so the test can check the real thing
rather than a proxy.
"""

from __future__ import annotations

from itertools import permutations

import pytest

from pytop.experimental.homeomorphism import (
    HomeomorphismResult,
    HomeoVerdict,
    finite_homeomorphic,
    homeomorphism_obstruction,
    preorder_isomorphism,
    specialization_preorder,
)
from pytop.experimental.spaces import FiniteSpace

# name -> (carrier, opens)
SPACES = {
    "sierpinski": ((0, 1), [(), (0,), (0, 1)]),
    "sierpinski_relabelled": (("x", "y"), [(), ("y",), ("x", "y")]),
    "discrete2": ((0, 1), [(), (0,), (1,), (0, 1)]),
    "indiscrete2": ((0, 1), [(), (0, 1)]),
    "chain3": ((0, 1, 2), [(), (0,), (0, 1), (0, 1, 2)]),
    "V3": ((0, 1, 2), [(), (0,), (1,), (0, 1), (0, 1, 2)]),
    "Lambda3": ((0, 1, 2), [(), (0,), (0, 1), (0, 2), (0, 1, 2)]),
    "discrete3": (
        (0, 1, 2),
        [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)],
    ),
    "indiscrete3": ((0, 1, 2), [(), (0, 1, 2)]),
    "point_plus_indiscrete2": ((0, 1, 2), [(), (0,), (1, 2), (0, 1, 2)]),
}


def _space(name: str) -> FiniteSpace:
    carrier, opens = SPACES[name]
    return FiniteSpace(name, carrier, opens)


def _brute_force_homeomorphic(a: str, b: str) -> bool:
    """Enumerate every bijection and check whether one carries the topology."""
    c1, o1 = SPACES[a]
    c2, o2 = SPACES[b]
    if len(c1) != len(c2):
        return False
    left = [frozenset(o) for o in o1]
    right = {frozenset(o) for o in o2}
    for image in permutations(c2):
        f = dict(zip(c1, image, strict=True))
        if {frozenset(f[x] for x in o) for o in left} == right:
            return True
    return False


# ---------------------------------------------------------------------------
# The decision procedure, against brute force
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("left", sorted(SPACES))
@pytest.mark.parametrize("right", sorted(SPACES))
def test_agrees_with_brute_force_on_every_pair(left: str, right: str) -> None:
    expected = _brute_force_homeomorphic(left, right)
    got = finite_homeomorphic(_space(left), _space(right))
    assert bool(got) is expected, (left, right, got.reason)
    assert got.verdict is (
        HomeoVerdict.HOMEOMORPHIC if expected else HomeoVerdict.DISTINCT
    )


def test_never_returns_inconclusive_for_finite_spaces() -> None:
    """Finite homeomorphism is decidable; an 'I don't know' would be a defect."""
    for left in SPACES:
        for right in SPACES:
            verdict = finite_homeomorphic(_space(left), _space(right)).verdict
            assert verdict is not HomeoVerdict.INCONCLUSIVE


def test_positive_result_carries_a_verified_bijection() -> None:
    a, b = _space("sierpinski"), _space("sierpinski_relabelled")
    result = finite_homeomorphic(a, b)
    assert result.witness is not None
    f = result.witness
    left_opens = {frozenset(o) for o in SPACES["sierpinski"][1]}
    right_opens = {frozenset(o) for o in SPACES["sierpinski_relabelled"][1]}
    assert {frozenset(f[x] for x in o) for o in left_opens} == right_opens


def test_negative_result_carries_an_obstruction() -> None:
    result = finite_homeomorphic(_space("sierpinski"), _space("discrete2"))
    assert result.verdict is HomeoVerdict.DISTINCT
    assert result.obstruction is not None
    assert result.witness is None


def test_dual_posets_are_distinguished() -> None:
    """V and Lambda have the same cardinality and open-set count.

    They are the case a coarse invariant check would wave through, so the
    preorder comparison has to do the work.
    """
    v, lam = _space("V3"), _space("Lambda3")
    assert len(SPACES["V3"][1]) == len(SPACES["Lambda3"][1])
    assert not finite_homeomorphic(v, lam)


def test_identity_is_always_a_homeomorphism() -> None:
    for name in SPACES:
        assert finite_homeomorphic(_space(name), _space(name))


def test_symmetry() -> None:
    names = sorted(SPACES)
    for i, a in enumerate(names):
        for b in names[i:]:
            forward = bool(finite_homeomorphic(_space(a), _space(b)))
            backward = bool(finite_homeomorphic(_space(b), _space(a)))
            assert forward is backward, (a, b)


# ---------------------------------------------------------------------------
# Preorder machinery
# ---------------------------------------------------------------------------


def test_specialization_preorder_is_reflexive_and_transitive() -> None:
    for carrier, opens in SPACES.values():
        rel = specialization_preorder(carrier, opens)
        for x in carrier:
            assert (x, x) in rel
        for x in carrier:
            for y in carrier:
                for z in carrier:
                    if (x, y) in rel and (y, z) in rel:
                        assert (x, z) in rel


def test_preorder_isomorphism_rejects_size_mismatch() -> None:
    assert preorder_isomorphism([0], [(0, 0)], [0, 1], [(0, 0), (1, 1)]) is None


def test_preorder_isomorphism_finds_a_relabelling() -> None:
    f = preorder_isomorphism(
        [0, 1], [(0, 0), (1, 1), (0, 1)],
        ["a", "b"], [("a", "a"), ("b", "b"), ("a", "b")],
    )
    assert f == {0: "a", 1: "b"}


# ---------------------------------------------------------------------------
# Invariant obstructions
# ---------------------------------------------------------------------------


def test_differing_invariant_proves_distinctness() -> None:
    result = homeomorphism_obstruction(
        {"betti": (1, 2, 1), "euler": 0}, {"betti": (1, 0, 1), "euler": 2}
    )
    assert result.verdict is HomeoVerdict.DISTINCT
    assert result.obstruction is not None
    assert result.obstruction.invariant in {"betti", "euler"}


def test_agreeing_invariants_never_claim_homeomorphic() -> None:
    """The central honesty property: agreement proves nothing."""
    same = {"betti": (1, 2, 1), "euler": 0, "torsion": ()}
    result = homeomorphism_obstruction(same, dict(same))
    assert result.verdict is HomeoVerdict.INCONCLUSIVE
    assert not result
    assert "proves nothing" in result.reason


def test_no_shared_invariants_is_inconclusive_not_distinct() -> None:
    result = homeomorphism_obstruction({"betti": 1}, {"euler": 2})
    assert result.verdict is HomeoVerdict.INCONCLUSIVE
    assert "nothing was" in result.reason


def test_missing_invariant_on_one_side_is_not_a_difference() -> None:
    """Absence means 'not computed', not 'different'."""
    result = homeomorphism_obstruction(
        {"betti": (1, 1), "genus": 3}, {"betti": (1, 1)}
    )
    assert result.verdict is HomeoVerdict.INCONCLUSIVE


def test_order_controls_which_obstruction_is_reported() -> None:
    left = {"euler": 0, "betti": (1, 2, 1)}
    right = {"euler": 2, "betti": (1, 0, 1)}
    first = homeomorphism_obstruction(left, right, order=["betti", "euler"])
    assert first.obstruction is not None
    assert first.obstruction.invariant == "betti"


def test_result_is_falsy_unless_proven_homeomorphic() -> None:
    for verdict in (HomeoVerdict.DISTINCT, HomeoVerdict.INCONCLUSIVE):
        assert not HomeomorphismResult(verdict, None, None, "")
    assert HomeomorphismResult(HomeoVerdict.HOMEOMORPHIC, {}, None, "")


def test_obstruction_renders_readably() -> None:
    result = homeomorphism_obstruction({"euler": 0}, {"euler": 2})
    assert str(result.obstruction) == "euler: 0 vs 2"
