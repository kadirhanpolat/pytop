"""Tests for pi_base_representations — concrete Space instances for pi-Base spaces."""

from __future__ import annotations

from fractions import Fraction

import pytest

from pytop.experimental.spaces import (
    AlexandroffSpace,
    CofiniteSpace,
    DiscreteCountableSpace,
    FiniteSpace,
    MetricTopologySpace,
    OrderTopologySpace,
    PiBaseSpace,
    SorgenfreyLineSpace,
    best_space,
    derive,
    is_compact,
    is_connected,
    is_hausdorff,
    is_representable,
    is_t0,
    is_t1,
    list_representable,
)


# ---------------------------------------------------------------------------
# list_representable / is_representable
# ---------------------------------------------------------------------------

def test_list_representable_count():
    reps = list_representable()
    assert len(reps) == 22


def test_list_representable_structure():
    for uid, name in list_representable():
        assert uid.startswith("S")
        assert isinstance(name, str) and name


def test_is_representable_known():
    for uid in ["S000001", "S000010", "S000043", "S000025", "S000002"]:
        assert is_representable(uid)


def test_is_representable_fallback():
    # Long line, Cantor space — no concrete representation
    for uid in ["S000038", "S000026"]:  # Long ray, Cantor space 2^omega
        assert not is_representable(uid)


def test_is_representable_by_name():
    assert is_representable("Sierpinski space")
    assert is_representable("Sorgenfrey line")


# ---------------------------------------------------------------------------
# best_space — return type dispatch
# ---------------------------------------------------------------------------

class TestBestSpaceTypes:
    def test_sierpinski_is_finite(self):
        sp = best_space("S000010")
        assert isinstance(sp, FiniteSpace)

    def test_discrete_2pt_is_finite(self):
        assert isinstance(best_space("S000001"), FiniteSpace)

    def test_indiscrete_2pt_is_finite(self):
        assert isinstance(best_space("S000004"), FiniteSpace)

    def test_particular_point_3pt_is_finite(self):
        assert isinstance(best_space("S000007"), FiniteSpace)

    def test_excluded_point_3pt_is_finite(self):
        assert isinstance(best_space("S000011"), FiniteSpace)

    def test_diamond_is_alexandroff(self):
        assert isinstance(best_space("S000144"), AlexandroffSpace)

    def test_singleton_is_finite(self):
        assert isinstance(best_space("S000162"), FiniteSpace)

    def test_empty_is_finite(self):
        assert isinstance(best_space("S000163"), FiniteSpace)

    def test_sum_singleton_indiscrete_is_finite(self):
        assert isinstance(best_space("S000164"), FiniteSpace)

    def test_sum_two_indiscrete_is_finite(self):
        assert isinstance(best_space("S000184"), FiniteSpace)

    def test_right_ray_3pt_is_alexandroff(self):
        assert isinstance(best_space("S000187"), AlexandroffSpace)

    def test_sum_singleton_sierpinski_is_finite(self):
        assert isinstance(best_space("S000188"), FiniteSpace)

    def test_discrete_3pt_is_finite(self):
        assert isinstance(best_space("S000189"), FiniteSpace)

    def test_indiscrete_3pt_is_finite(self):
        assert isinstance(best_space("S000190"), FiniteSpace)

    def test_three_pt_basis_singleton_is_finite(self):
        assert isinstance(best_space("S000203"), FiniteSpace)

    def test_three_pt_basis_pair_is_finite(self):
        assert isinstance(best_space("S000204"), FiniteSpace)

    def test_pseudocircle_is_alexandroff(self):
        assert isinstance(best_space("S000213"), AlexandroffSpace)

    def test_discrete_omega_is_discrete_countable(self):
        assert isinstance(best_space("S000002"), DiscreteCountableSpace)

    def test_cofinite_omega_is_cofinite(self):
        assert isinstance(best_space("S000015"), CofiniteSpace)

    def test_euclidean_reals_is_metric(self):
        assert isinstance(best_space("S000025"), MetricTopologySpace)

    def test_rationals_is_order(self):
        assert isinstance(best_space("S000027"), OrderTopologySpace)

    def test_sorgenfrey_is_sorgenfrey(self):
        assert isinstance(best_space("S000043"), SorgenfreyLineSpace)

    def test_fallback_is_pi_base_space(self):
        assert isinstance(best_space("S000038"), PiBaseSpace)   # Long ray
        assert isinstance(best_space("S000026"), PiBaseSpace)   # Cantor space 2^omega


# ---------------------------------------------------------------------------
# Topology correctness — finite spaces
# ---------------------------------------------------------------------------

class TestFiniteSpaceTopologies:
    def test_sierpinski_opens(self):
        sp = best_space("S000010")
        opens = sp.open_sets()
        assert frozenset() in opens
        assert frozenset({0, 1}) in opens
        # exactly one of the singletons is open
        assert len(opens) == 3

    def test_discrete_2pt_opens(self):
        sp = best_space("S000001")
        assert len(sp.open_sets()) == 4  # all subsets of {0,1}

    def test_indiscrete_2pt_opens(self):
        sp = best_space("S000004")
        assert len(sp.open_sets()) == 2  # ∅ and {0,1}

    def test_particular_point_3pt_opens(self):
        sp = best_space("S000007")
        # particular point topology on 3 points: 5 opens
        assert len(sp.open_sets()) == 5
        # particular point (0) is in every nonempty open
        for o in sp.open_sets():
            if o:
                assert 0 in o

    def test_excluded_point_3pt_opens(self):
        sp = best_space("S000011")
        # excluded point (2) never appears in proper open sets except X
        assert len(sp.open_sets()) == 5
        for o in sp.open_sets():
            if o and o != frozenset({0, 1, 2}):
                assert 2 not in o

    def test_singleton_opens(self):
        sp = best_space("S000162")
        assert len(sp.open_sets()) == 2

    def test_empty_opens(self):
        sp = best_space("S000163")
        assert sp.open_sets() == frozenset({frozenset()})

    def test_sum_singleton_indiscrete_opens(self):
        sp = best_space("S000164")
        assert len(sp.open_sets()) == 4

    def test_sum_two_indiscrete_opens(self):
        sp = best_space("S000184")
        assert len(sp.open_sets()) == 4

    def test_sum_singleton_sierpinski_opens(self):
        sp = best_space("S000188")
        assert len(sp.open_sets()) == 6

    def test_discrete_3pt_opens(self):
        sp = best_space("S000189")
        assert len(sp.open_sets()) == 8

    def test_indiscrete_3pt_opens(self):
        sp = best_space("S000190")
        assert len(sp.open_sets()) == 2

    def test_three_pt_basis_singleton_opens(self):
        sp = best_space("S000203")
        assert len(sp.open_sets()) == 3

    def test_three_pt_basis_pair_opens(self):
        sp = best_space("S000204")
        assert len(sp.open_sets()) == 3

    def test_topologies_closed_under_unions(self):
        """All finite space topologies are closed under pairwise unions."""
        finite_uids = [
            "S000001", "S000004", "S000007", "S000010", "S000011",
            "S000162", "S000163", "S000164", "S000184", "S000188",
            "S000189", "S000190", "S000203", "S000204",
        ]
        for uid in finite_uids:
            sp = best_space(uid)
            opens = sp.open_sets()
            for a in opens:
                for b in opens:
                    assert (a | b) in opens, f"{uid}: {a} | {b} not in topology"

    def test_topologies_closed_under_intersections(self):
        """All finite space topologies are closed under pairwise intersections."""
        finite_uids = [
            "S000001", "S000004", "S000007", "S000010", "S000011",
            "S000164", "S000184", "S000188", "S000189", "S000190",
            "S000203", "S000204",
        ]
        for uid in finite_uids:
            sp = best_space(uid)
            opens = sp.open_sets()
            for a in opens:
                for b in opens:
                    assert (a & b) in opens, f"{uid}: {a} & {b} not in topology"


# ---------------------------------------------------------------------------
# AlexandroffSpace topologies
# ---------------------------------------------------------------------------

class TestAlexandroffSpaces:
    def test_diamond_opens(self):
        sp = best_space("S000144")
        opens = sp.open_sets()
        # ∅, {top}, {a,top}, {b,top}, {a,b,top}, {bot,a,b,top}
        assert len(opens) == 6
        assert frozenset() in opens
        assert frozenset({"bot", "a", "b", "top"}) in opens

    def test_right_ray_opens(self):
        sp = best_space("S000187")
        opens = sp.open_sets()
        # ∅, {2}, {1,2}, {0,1,2}
        assert len(opens) == 4
        assert frozenset({2}) in opens
        assert frozenset({1, 2}) in opens

    def test_pseudocircle_opens(self):
        sp = best_space("S000213")
        opens = sp.open_sets()
        # ∅, {a}, {b}, {a,b}, {a,b,c}, {a,b,d}, {a,b,c,d}
        assert len(opens) == 7
        assert frozenset({"a"}) in opens
        assert frozenset({"b"}) in opens
        assert frozenset({"a", "b"}) in opens


# ---------------------------------------------------------------------------
# Separation axioms via predicates — agree with pi-Base
# ---------------------------------------------------------------------------

class TestPredicateAgreement:
    """Concrete representations give the same verdicts as pi-Base."""

    @pytest.mark.parametrize("uid,t0,t1,t2", [
        ("S000001", True, True, True),    # discrete {0,1}
        ("S000004", False, False, False), # indiscrete {0,1}
        ("S000010", True, False, False),  # Sierpinski
        ("S000011", True, False, False),  # excluded point 3-pt: T0 but not T1
    ])
    def test_separation_finite(self, uid, t0, t1, t2):
        sp = best_space(uid)
        assert is_t0(sp).value is t0
        assert is_t1(sp).value is t1
        assert is_hausdorff(sp).value is t2

    def test_discrete_2pt_compact_and_connected(self):
        sp = best_space("S000001")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is False

    def test_indiscrete_2pt_compact_and_connected(self):
        sp = best_space("S000004")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_sierpinski_compact_connected(self):
        sp = best_space("S000010")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_singleton_compact_connected(self):
        sp = best_space("S000162")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_empty_space_compact(self):
        sp = best_space("S000163")
        assert is_compact(sp).value is True

    def test_discrete_omega_hausdorff_not_compact(self):
        sp = best_space("S000002")
        assert is_hausdorff(sp).value is True
        assert is_compact(sp).value is False

    def test_cofinite_omega_t1_not_hausdorff(self):
        sp = best_space("S000015")
        assert is_t1(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_sorgenfrey_hausdorff_not_compact(self):
        sp = best_space("S000043")
        assert is_hausdorff(sp).value is True
        assert is_compact(sp).value is False

    def test_euclidean_reals_hausdorff(self):
        sp = best_space("S000025")
        assert is_hausdorff(sp).value is True

    def test_rationals_hausdorff_not_compact(self):
        sp = best_space("S000027")
        assert is_hausdorff(sp).value is True
        assert is_compact(sp).value is False
        assert is_connected(sp).value is False


# ---------------------------------------------------------------------------
# Euclidean ℝ — point separation uses exact Fraction arithmetic
# ---------------------------------------------------------------------------

def test_euclidean_reals_point_separation():
    sp = best_space("S000025")
    v = sp.point_separation(Fraction(1, 3), Fraction(2, 3))
    assert v.value is True
    # radius should be (2/3 - 1/3)/2 = 1/6
    _, (_, r) = v.witness
    assert r == Fraction(1, 6)


def test_euclidean_reals_membership():
    sp = best_space("S000025")
    assert sp.contains(Fraction(1, 2))
    assert sp.contains(0)
    assert not sp.contains("x")


# ---------------------------------------------------------------------------
# Reasoning engine integration — concrete spaces feed into derive()
# ---------------------------------------------------------------------------

def test_derive_sierpinski_t0():
    sp = best_space("S000010")
    result = derive(sp, "T0")
    assert result.verdict.value is True


def test_derive_sorgenfrey_normal():
    sp = best_space("S000043")
    result = derive(sp, "normal")
    assert result.verdict.value is True


def test_derive_pseudocircle_not_hausdorff():
    # Pseudocircle is T0 but not T1/T2
    sp = best_space("S000213")
    assert is_t0(sp).value is True
    assert is_hausdorff(sp).value is False


# ---------------------------------------------------------------------------
# Lookup by name (not just UID)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,uid", [
    ("Sierpinski space", "S000010"),
    ("Sorgenfrey line", "S000043"),
    ("Rational numbers $\\mathbb Q$", "S000027"),
])
def test_lookup_by_name(name, uid):
    sp = best_space(name)
    assert is_representable(name)
    assert sp.name  # non-empty name
