"""Coverage-targeted tests for separation.py (v0.5.1)."""
import pytest
from pytop.separation import (
    SeparationError,
    normalize_separation_property,
    analyze_separation,
    is_t2,
    is_urysohn,
    is_t2_5,
    is_perfectly_normal,
    _finite_separation,
    _finite_normal,
    _separate_closed_sets,
    _metric_justification,
    _negative_tag_implication,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _discrete2():
    carrier = frozenset({1, 2})
    topology = frozenset([frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})])
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


class _Sym:
    """Minimal symbolic space stub."""
    def __init__(self, tags=(), rep="symbolic_general"):
        self.tags = set(tags)
        self.metadata = {"representation": rep} if rep != "symbolic_general" else {}


# ---------------------------------------------------------------------------
# normalize_separation_property — unsupported name (line 102)
# ---------------------------------------------------------------------------

def test_normalize_unsupported_raises():
    with pytest.raises(SeparationError):
        normalize_separation_property("garbage_property")


# ---------------------------------------------------------------------------
# analyze_separation — negative implication path (line 142)
# ---------------------------------------------------------------------------

def test_negative_implication_t3_not_t1():
    # "not_t1" not in FALSE_TAGS["t3"], but _negative_tag_implication returns non-empty
    result = analyze_separation(_Sym(tags={"not_t1"}), "t3")
    assert result.is_false


# ---------------------------------------------------------------------------
# is_t2 — alias (line 183)
# ---------------------------------------------------------------------------

def test_is_t2():
    result = is_t2(_discrete2())
    assert result.is_true


# ---------------------------------------------------------------------------
# is_urysohn — alias (line 211)
# ---------------------------------------------------------------------------

def test_is_urysohn():
    result = is_urysohn(_Sym(tags={"metric"}))
    assert result.is_true


# ---------------------------------------------------------------------------
# is_t2_5 — alias (line 215)
# ---------------------------------------------------------------------------

def test_is_t2_5():
    result = is_t2_5(_Sym(tags={"metric"}))
    assert result.is_true


# ---------------------------------------------------------------------------
# is_perfectly_normal — alias (line 219)
# ---------------------------------------------------------------------------

def test_is_perfectly_normal():
    result = is_perfectly_normal(_Sym(tags={"metric"}))
    assert result.is_true


# ---------------------------------------------------------------------------
# _finite_separation — topology is None/falsy (line 254)
# ---------------------------------------------------------------------------

def test_finite_separation_none_topology():
    class NoneTopoSpace:
        topology = None
        carrier = frozenset({1})

    result = _finite_separation(NoneTopoSpace(), "t0")
    assert result is None


# ---------------------------------------------------------------------------
# _finite_separation — truthy topology but empty opens (line 257)
# ---------------------------------------------------------------------------

def test_finite_separation_empty_opens():
    class AlwaysTrueEmptyIter:
        def __bool__(self):
            return True
        def __iter__(self):
            return iter([])

    class EmptyOpensTopo:
        topology = AlwaysTrueEmptyIter()
        carrier = frozenset({1})

    result = _finite_separation(EmptyOpensTopo(), "t0")
    assert result is None


# ---------------------------------------------------------------------------
# _finite_separation — completely_regular returns None for non-T1 (line 280)
# ---------------------------------------------------------------------------

def test_finite_separation_completely_regular_non_t1():
    # Sierpinski space: not T1, so completely_regular returns None
    class Sierpinski:
        topology = [frozenset(), frozenset({1}), frozenset({1, 2})]
        carrier = frozenset({1, 2})

    result = _finite_separation(Sierpinski(), "completely_regular")
    assert result is None


# ---------------------------------------------------------------------------
# _finite_separation — unknown property fallthrough (line 283)
# ---------------------------------------------------------------------------

def test_finite_separation_unknown_property():
    class Sierpinski:
        topology = [frozenset(), frozenset({1}), frozenset({1, 2})]
        carrier = frozenset({1, 2})

    result = _finite_separation(Sierpinski(), "unknown_property_xyz")
    assert result is None


# ---------------------------------------------------------------------------
# _finite_normal — returns False (line 340)
# Particular-point topology on {1,2,3}: {2} and {3} are disjoint closed sets
# that cannot be separated (every open containing {3} also contains 1,
# but every open containing {2} also contains 1 → always share 1).
# ---------------------------------------------------------------------------

_PARTICULAR_OPENS = [set(), {1}, {1, 2}, {1, 3}, {1, 2, 3}]
_THREE_POINTS = [1, 2, 3]


def test_finite_normal_returns_false():
    result = _finite_normal(_PARTICULAR_OPENS, _THREE_POINTS)
    assert result is False


# ---------------------------------------------------------------------------
# _separate_closed_sets — returns False (line 361)
# ---------------------------------------------------------------------------

def test_separate_closed_sets_returns_false():
    # {2} and {3} cannot be separated in the particular-point topology
    result = _separate_closed_sets(_PARTICULAR_OPENS, {2}, {3})
    assert result is False


def test_separate_closed_sets_returns_true():
    # Discrete opens: {2} and {3} ARE separable
    discrete_opens = [set(), {2}, {3}, {2, 3}]
    result = _separate_closed_sets(discrete_opens, {2}, {3})
    assert result is True


# ---------------------------------------------------------------------------
# _theorem_level_separation — hausdorff via positive tag (line 408)
# ---------------------------------------------------------------------------

def test_hausdorff_via_urysohn_tag():
    # "urysohn" is stronger than "hausdorff" → hits line 408
    result = analyze_separation(_Sym(tags={"urysohn"}), "hausdorff")
    assert result.is_true


# ---------------------------------------------------------------------------
# _theorem_level_separation — completely_regular via tychonoff tag (line 416)
# ---------------------------------------------------------------------------

def test_completely_regular_via_tychonoff_tag():
    # "tychonoff" implies completely_regular → hits line 416
    result = analyze_separation(_Sym(tags={"tychonoff"}), "completely_regular")
    assert result.is_true


# ---------------------------------------------------------------------------
# _metric_justification — fallback (line 441)
# ---------------------------------------------------------------------------

def test_metric_justification_fallback():
    result = _metric_justification("unknown_sep_property")
    assert "Metric structure" in result


# ---------------------------------------------------------------------------
# _negative_tag_implication — all branches (lines 463-475)
# ---------------------------------------------------------------------------

def test_neg_tag_not_t1_for_t3():
    msg = _negative_tag_implication({"not_t1"}, "t3")
    assert msg and "not_t1" in msg or "T1" in msg


def test_neg_tag_not_hausdorff_for_urysohn():
    msg = _negative_tag_implication({"not_hausdorff"}, "urysohn")
    assert msg and "Hausdorff" in msg or "hausdorff" in msg.lower()


def test_neg_tag_t1_not_hausdorff_for_regular():
    msg = _negative_tag_implication({"t1", "not_hausdorff"}, "regular")
    assert msg and "hausdorff" in msg.lower()


def test_neg_tag_not_regular_for_t3():
    # "not_t1" must be absent so line 463 doesn't fire first
    msg = _negative_tag_implication({"not_regular"}, "t3")
    assert msg and "regular" in msg.lower()


def test_neg_tag_not_normal_for_t4():
    msg = _negative_tag_implication({"not_normal"}, "t4")
    assert msg and "normal" in msg.lower()


def test_neg_tag_not_normal_for_perfectly_normal():
    msg = _negative_tag_implication({"not_normal"}, "perfectly_normal")
    assert msg and "normal" in msg.lower()


def test_neg_tag_not_completely_regular_for_tychonoff():
    msg = _negative_tag_implication({"not_completely_regular"}, "tychonoff")
    assert msg and "completely_regular" in msg.lower() or "Tychonoff" in msg


def test_neg_tag_empty_returns_empty():
    msg = _negative_tag_implication(set(), "t0")
    assert msg == ""
