"""Tests for pi_base_representations — concrete Space instances for pi-Base spaces."""

from __future__ import annotations

from fractions import Fraction

import pytest

from fractions import Fraction

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
    is_second_countable,
    is_t0,
    is_t1,
    list_representable,
)
from pytop.experimental.spaces.pi_base_representations import (
    _CertifiedSpace,
    _MetricWithCerts,
)


# ---------------------------------------------------------------------------
# list_representable / is_representable
# ---------------------------------------------------------------------------

def test_list_representable_count():
    reps = list_representable()
    assert len(reps) == 155


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


# ---------------------------------------------------------------------------
# Batch 2 — _MetricWithCerts type checks
# ---------------------------------------------------------------------------

class TestMetricWithCertsTypes:
    @pytest.mark.parametrize("uid", [
        "S000003",   # Discrete on ℝ
        "S000133",   # Post office metric
        "S000158",   # [0,1]
        "S000176",   # ℝ²
        "S000210",   # [0,1)
        "S000225",   # upper half-plane
    ])
    def test_is_metric_with_certs(self, uid):
        assert isinstance(best_space(uid), _MetricWithCerts)

    def test_post_office_metric_separation(self):
        sp = best_space("S000133")
        # d(1/2, 1/3) = |1/2| + |1/3| = 5/6  → radius = 5/12
        v = sp.point_separation(Fraction(1, 2), Fraction(1, 3))
        assert v.value is True

    def test_post_office_metric_at_origin(self):
        # d(0, x) = 0 + |x| = |x|; open ball at 0 contains any |x| < r
        sp = best_space("S000133")
        v = sp.point_separation(Fraction(0), Fraction(1, 4))
        assert v.value is True

    def test_unit_interval_membership(self):
        sp = best_space("S000158")
        assert sp.contains(Fraction(0))
        assert sp.contains(Fraction(1))
        assert sp.contains(Fraction(1, 2))
        assert not sp.contains(Fraction(3, 2))

    def test_unit_interval_compact(self):
        sp = best_space("S000158")
        assert is_compact(sp).value is True

    def test_half_open_interval_membership(self):
        sp = best_space("S000210")
        assert sp.contains(Fraction(0))
        assert not sp.contains(Fraction(1))
        assert sp.contains(Fraction(1, 2))

    def test_half_open_interval_not_compact(self):
        sp = best_space("S000210")
        assert is_compact(sp).value is False

    def test_euclidean_plane_membership(self):
        sp = best_space("S000176")
        assert sp.contains((Fraction(0), Fraction(0)))
        assert sp.contains((Fraction(1, 2), Fraction(-3, 4)))
        assert not sp.contains((1, 2, 3))   # not a 2-tuple
        assert not sp.contains("xy")

    def test_euclidean_plane_separation(self):
        sp = best_space("S000176")
        # max-norm: d((0,0),(1,0)) = max(1,0) = 1 → radius 1/2
        v = sp.point_separation((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)))
        assert v.value is True

    def test_upper_half_plane_membership(self):
        sp = best_space("S000225")
        assert sp.contains((Fraction(0), Fraction(0)))      # y=0 ok
        assert sp.contains((Fraction(3), Fraction(1, 2)))   # y>0 ok
        assert not sp.contains((Fraction(0), Fraction(-1))) # y<0 excluded

    def test_discrete_reals_point_separation(self):
        # Discrete metric: d(x,y)=1 for x≠y → balls of radius 1/2 are singletons
        sp = best_space("S000003")
        v = sp.point_separation(Fraction(1), Fraction(2))
        assert v.value is True

    # _MetricWithCerts uses pi-Base certs for specific properties
    def test_metric_with_certs_second_countable_from_pi_base(self):
        # Post office ℝ is NOT second-countable (pi-Base says False)
        sp = best_space("S000133")
        assert is_second_countable(sp).value is False

    def test_unit_interval_second_countable_from_pi_base(self):
        sp = best_space("S000158")
        assert is_second_countable(sp).value is True


# ---------------------------------------------------------------------------
# Batch 2 — _CertifiedSpace type checks and properties
# ---------------------------------------------------------------------------

class TestCertifiedSpaceTypes:
    @pytest.mark.parametrize("uid", [
        "S000005",   # Odd-Even
        "S000008",   # Particular point on ω
        "S000009",   # Particular point on ℝ
        "S000012",   # Excluded point on ω
        "S000013",   # Excluded point on ℝ
        "S000016",   # Cofinite on ℝ
        "S000017",   # Cocountable on ℝ
        "S000049",   # Divisor topology
        "S000051",   # Khalimsky line
        "S000052",   # Relatively prime integers
        "S000053",   # Prime integer topology
        "S000193",   # Indiscrete ω
        "S000199",   # Left ray ω
        "S000200",   # Right ray ω
    ])
    def test_is_certified_space(self, uid):
        assert isinstance(best_space(uid), _CertifiedSpace)

    def test_certified_membership_omega(self):
        for uid in ["S000008", "S000012", "S000193", "S000199", "S000200"]:
            sp = best_space(uid)
            assert sp.contains(0)
            assert sp.contains(42)
            assert not sp.contains(-1)
            assert not sp.contains("x")

    def test_certified_membership_pos_int(self):
        for uid in ["S000005", "S000049", "S000052", "S000053"]:
            sp = best_space(uid)
            assert sp.contains(1)
            assert sp.contains(100)
            assert not sp.contains(0)
            assert not sp.contains(-5)

    def test_certified_membership_integer(self):
        sp = best_space("S000051")   # Khalimsky on ℤ
        assert sp.contains(0)
        assert sp.contains(-3)
        assert not sp.contains(Fraction(1, 2))

    def test_certified_membership_real(self):
        for uid in ["S000009", "S000013", "S000016", "S000017"]:
            sp = best_space(uid)
            assert sp.contains(Fraction(1, 3))
            assert sp.contains(0)
            assert not sp.contains("pi")

    # pi-Base certs flow through _CertifiedSpace
    def test_cofinite_reals_t1_not_hausdorff(self):
        sp = best_space("S000016")
        assert is_t1(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_cofinite_reals_not_second_countable(self):
        sp = best_space("S000016")
        assert is_second_countable(sp).value is False

    def test_cofinite_reals_compact(self):
        sp = best_space("S000016")
        assert is_compact(sp).value is True

    def test_particular_point_omega_not_hausdorff(self):
        sp = best_space("S000008")
        assert is_hausdorff(sp).value is False

    def test_khalimsky_line_not_hausdorff(self):
        sp = best_space("S000051")
        assert is_hausdorff(sp).value is False

    def test_indiscrete_omega_connected(self):
        sp = best_space("S000193")
        assert is_connected(sp).value is True

    def test_indiscrete_omega_not_t0(self):
        sp = best_space("S000193")
        assert is_t0(sp).value is False


# ---------------------------------------------------------------------------
# Batch 3 — _MetricWithCerts: radial plane + disjoint union
# ---------------------------------------------------------------------------

class TestBatch3MetricWithCerts:
    def test_radial_plane_type(self):
        assert isinstance(best_space("S000134"), _MetricWithCerts)

    def test_disjoint_union_reals_singleton_type(self):
        assert isinstance(best_space("S000198"), _MetricWithCerts)

    def test_radial_plane_membership(self):
        sp = best_space("S000134")
        assert sp.contains((Fraction(1), Fraction(0)))
        assert sp.contains((Fraction(0), Fraction(0)))
        assert not sp.contains((1, 2, 3))
        assert not sp.contains("xy")

    def test_radial_plane_hausdorff_connected(self):
        sp = best_space("S000134")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is True

    def test_radial_plane_same_ray_distance(self):
        sp = best_space("S000134")
        # (1,0) and (2,0) are on the same ray; distance = |1-2| = 1
        v = sp.point_separation((Fraction(1), Fraction(0)), (Fraction(2), Fraction(0)))
        assert v.value is True

    def test_radial_plane_different_ray_distance(self):
        sp = best_space("S000134")
        # (1,0) and (0,1): different rays — d = 1 + 1 = 2
        v = sp.point_separation((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
        assert v.value is True

    def test_disjoint_union_membership(self):
        sp = best_space("S000198")
        assert sp.contains(Fraction(0))
        assert sp.contains(Fraction(1, 2))
        assert sp.contains("*")
        assert not sp.contains("x")
        assert not sp.contains((1, 2))

    def test_disjoint_union_not_connected(self):
        sp = best_space("S000198")
        assert is_connected(sp).value is False

    def test_disjoint_union_hausdorff(self):
        sp = best_space("S000198")
        assert is_hausdorff(sp).value is True

    def test_disjoint_union_cross_component_separation(self):
        sp = best_space("S000198")
        # ∗ vs 0: different components — always separated
        v = sp.point_separation("*", Fraction(0))
        assert v.value is True


# ---------------------------------------------------------------------------
# Batch 3 — _CertifiedSpace type checks
# ---------------------------------------------------------------------------

class TestBatch3CertifiedSpaceTypes:
    @pytest.mark.parametrize("uid", [
        "S000023",  # Arens-Fort
        "S000029",  # OPC of Q
        "S000033",  # ordinal ω+ω
        "S000034",  # ordinal ω+ω+1
        "S000042",  # right ray reals
        "S000047",  # countable sum of Sierpinski spaces
        "S000048",  # cofinite ω + generic point
        "S000050",  # Q focal point
        "S000054",  # double pointed reals
        "S000083",  # line two origins
        "S000096",  # Appert space
        "S000097",  # OPC sequential fan
        "S000098",  # minimal Hausdorff
        "S000100",  # David Gao's space
        "S000118",  # integer broom
        "S000150",  # right closed-ray Q∩[0,1]
        "S000151",  # right open-ray Q∩[0,1]
        "S000160",  # right open-ray ω+1
        "S000165",  # OPC Arens-Fort
        "S000166",  # left ray ω+1
        "S000185",  # OPC metric fan
        "S000186",  # converging seq non-Hausdorff
        "S000194",  # indiscrete ℝ
    ])
    def test_is_certified_space(self, uid):
        assert isinstance(best_space(uid), _CertifiedSpace)


# ---------------------------------------------------------------------------
# Batch 3 — membership correctness per carrier type
# ---------------------------------------------------------------------------

class TestBatch3Membership:
    def test_ordinal_ww_membership(self):
        sp = best_space("S000033")
        assert sp.contains((0, 0))
        assert sp.contains((1, 42))
        assert not sp.contains((2, 0))  # only copy 0 or 1
        assert not sp.contains("ω")
        assert not sp.contains(0)

    def test_ordinal_ww1_membership(self):
        sp = best_space("S000034")
        assert sp.contains((0, 0))
        assert sp.contains((1, 5))
        assert sp.contains("Ω")  # the limit point
        assert not sp.contains("ω")
        assert not sp.contains(0)

    def test_arens_fort_membership(self):
        sp = best_space("S000023")
        assert sp.contains((0, 0))
        assert sp.contains((3, 7))
        assert sp.contains("∞")
        assert not sp.contains(0)
        assert not sp.contains((-1, 0))

    def test_opc_arens_fort_membership(self):
        sp = best_space("S000165")
        assert sp.contains((0, 0))
        assert sp.contains("∞")
        assert not sp.contains(0)

    def test_two_origins_membership(self):
        sp = best_space("S000083")
        assert sp.contains("0a")
        assert sp.contains("0b")
        assert sp.contains(Fraction(1, 2))
        assert sp.contains(-3)
        assert not sp.contains(0)     # 0 is replaced by "0a"/"0b"
        assert not sp.contains("0c")

    def test_double_pointed_reals_membership(self):
        sp = best_space("S000054")
        assert sp.contains((Fraction(1, 2), 0))
        assert sp.contains((Fraction(1, 2), 1))
        assert sp.contains((0, 0))
        assert not sp.contains((Fraction(1), 2))  # b not in {0,1}
        assert not sp.contains(Fraction(1))        # must be pair

    def test_sierpinski_sum_membership(self):
        sp = best_space("S000047")
        assert sp.contains((0, 0))
        assert sp.contains((0, 1))
        assert sp.contains((5, 1))
        assert not sp.contains((0, 2))  # b not in {0,1}
        assert not sp.contains((-1, 0))

    def test_cofinite_omega_star_membership(self):
        sp = best_space("S000048")
        assert sp.contains(0)
        assert sp.contains(42)
        assert sp.contains("*")
        assert not sp.contains(-1)
        assert not sp.contains("x")

    def test_opc_Q_membership(self):
        sp = best_space("S000029")
        assert sp.contains(Fraction(1, 3))
        assert sp.contains(0)
        assert sp.contains("*")   # _FOCAL_MEMBER uses "*" for the ideal point
        assert not sp.contains("x")

    def test_Q_focal_point_membership(self):
        sp = best_space("S000050")
        assert sp.contains(Fraction(1, 3))
        assert sp.contains(0)
        assert sp.contains("*")
        assert not sp.contains("x")

    def test_right_ray_reals_membership(self):
        sp = best_space("S000042")
        assert sp.contains(0)
        assert sp.contains(Fraction(-1, 2))
        assert not sp.contains("x")

    def test_indiscrete_reals_membership(self):
        sp = best_space("S000194")
        assert sp.contains(0)
        assert sp.contains(Fraction(1, 3))
        assert not sp.contains("x")

    def test_omega1_membership(self):
        for uid in ["S000160", "S000166"]:
            sp = best_space(uid)
            assert sp.contains(0)
            assert sp.contains(10)
            assert sp.contains("ω")
            assert not sp.contains(-1)
            assert not sp.contains("Ω")

    def test_q01_membership(self):
        for uid in ["S000150", "S000151"]:
            sp = best_space(uid)
            assert sp.contains(Fraction(0))
            assert sp.contains(Fraction(1))
            assert sp.contains(Fraction(1, 2))
            assert not sp.contains(Fraction(-1, 2))
            assert not sp.contains(Fraction(3, 2))

    def test_appert_membership(self):
        sp = best_space("S000096")
        assert sp.contains(1)
        assert sp.contains(100)
        assert not sp.contains(0)
        assert not sp.contains(-1)

    def test_omega_based_membership(self):
        for uid in ["S000098", "S000100"]:
            sp = best_space(uid)
            assert sp.contains(0)
            assert sp.contains(7)
            assert not sp.contains(-1)
            assert not sp.contains("x")

    def test_integer_broom_membership(self):
        sp = best_space("S000118")
        assert sp.contains((-3, Fraction(0)))
        assert sp.contains((0, Fraction(1, 2)))
        assert sp.contains((5, Fraction(1)))
        assert not sp.contains((0, Fraction(3, 2)))    # t > 1
        assert not sp.contains((Fraction(1, 2), Fraction(0)))  # n not int

    def test_seq_fan_membership(self):
        for uid in ["S000097", "S000185"]:
            sp = best_space(uid)
            assert sp.contains((0, 0))
            assert sp.contains((3, 7))
            assert sp.contains("∞")
            assert not sp.contains((-1, 0))
            assert not sp.contains(0)

    def test_conv_seq_membership(self):
        sp = best_space("S000186")
        assert sp.contains((0, 0))
        assert sp.contains((2, 1))
        assert sp.contains("∞")
        assert not sp.contains((0, 2))  # b not in {0,1}
        assert not sp.contains(0)


# ---------------------------------------------------------------------------
# Batch 3 — property certificate checks via pi-Base
# ---------------------------------------------------------------------------

class TestBatch3Properties:
    def test_right_ray_reals_t0_not_t1(self):
        sp = best_space("S000042")
        assert is_t0(sp).value is True
        assert is_t1(sp).value is False

    def test_right_ray_reals_connected(self):
        sp = best_space("S000042")
        assert is_connected(sp).value is True

    def test_double_pointed_reals_not_t0(self):
        sp = best_space("S000054")
        assert is_t0(sp).value is False

    def test_line_two_origins_t1_not_hausdorff(self):
        sp = best_space("S000083")
        assert is_t1(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_arens_fort_hausdorff_not_compact(self):
        sp = best_space("S000023")
        assert is_hausdorff(sp).value is True
        assert is_compact(sp).value is False

    def test_opc_seq_fan_compact(self):
        sp = best_space("S000097")
        assert is_compact(sp).value is True

    def test_ordinal_ww_hausdorff(self):
        sp = best_space("S000033")
        assert is_hausdorff(sp).value is True

    def test_sierpinski_sum_not_t1(self):
        sp = best_space("S000047")
        assert is_t1(sp).value is False

    def test_cofinite_omega_star_compact(self):
        sp = best_space("S000048")
        assert is_compact(sp).value is True

    def test_converging_seq_compact_not_hausdorff(self):
        sp = best_space("S000186")
        assert is_compact(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_indiscrete_reals_not_t0(self):
        sp = best_space("S000194")
        assert is_t0(sp).value is False

    def test_disjoint_union_not_connected(self):
        sp = best_space("S000198")
        assert is_connected(sp).value is False


# ---------------------------------------------------------------------------
# Batch 4 — _CertifiedSpace type checks
# ---------------------------------------------------------------------------

class TestBatch4CertifiedSpaceTypes:
    @pytest.mark.parametrize("uid", [
        "S000006",  # deleted integer topology
        "S000014",  # either-or topology
        "S000019",  # compact complement topology
        "S000020",  # Fort space on ω
        "S000022",  # Fortissimo on ℝ
        "S000024",  # modified Fort on ℝ
        "S000044",  # nested interval
        "S000045",  # overlapping interval
        "S000046",  # interlocking interval
        "S000055",  # countable complement extension
        "S000056",  # Smirnov deleted sequence
        "S000057",  # rational sequence
        "S000063",  # Michael line
        "S000065",  # telophase topology
        "S000066",  # double origin plane
        "S000076",  # Sorgenfrey plane
        "S000093",  # double arrow space
        "S000131",  # sequential fan ω-many spines
        "S000140",  # ℝ + co-countable point
        "S000154",  # Fort space on ℝ
        "S000159",  # right open-ray [0,1]
        "S000202",  # metric fan ω-many spines
        "S000206",  # deleted sequence of intervals
    ])
    def test_is_certified_space(self, uid):
        assert isinstance(best_space(uid), _CertifiedSpace)


# ---------------------------------------------------------------------------
# Batch 4 — membership correctness
# ---------------------------------------------------------------------------

class TestBatch4Membership:
    def test_deleted_integer_topology(self):
        sp = best_space("S000006")
        assert sp.contains(Fraction(1, 2))      # non-integer rational
        assert sp.contains(Fraction(-3, 7))
        assert not sp.contains(0)               # integer
        assert not sp.contains(5)               # integer
        assert not sp.contains("x")

    def test_either_or_topology(self):
        sp = best_space("S000014")
        assert sp.contains(Fraction(0))
        assert sp.contains(Fraction(1))
        assert sp.contains(Fraction(-1))
        assert sp.contains(Fraction(1, 2))
        assert not sp.contains(Fraction(3, 2))  # outside [-1,1]
        assert not sp.contains("x")

    def test_real_member_spaces(self):
        for uid in ["S000019", "S000044", "S000045", "S000046",
                    "S000055", "S000056", "S000057", "S000063",
                    "S000140", "S000206"]:
            sp = best_space(uid)
            assert sp.contains(0)
            assert sp.contains(Fraction(1, 3))
            assert not sp.contains("x")

    def test_focal_member_spaces(self):
        for uid in ["S000022", "S000024", "S000154"]:
            sp = best_space(uid)
            assert sp.contains(Fraction(1, 2))
            assert sp.contains(0)
            assert sp.contains("*")
            assert not sp.contains("x")

    def test_fort_space_omega_membership(self):
        sp = best_space("S000020")
        assert sp.contains(0)
        assert sp.contains(42)
        assert sp.contains("*")
        assert not sp.contains(-1)
        assert not sp.contains("x")

    def test_telophase_membership(self):
        sp = best_space("S000065")
        assert sp.contains(Fraction(0))
        assert sp.contains(Fraction(1, 2))
        assert sp.contains("1a")
        assert sp.contains("1b")
        assert not sp.contains(1)          # 1 itself is not in carrier
        assert not sp.contains(Fraction(1))
        assert not sp.contains(Fraction(3, 2))

    def test_double_origin_plane_membership(self):
        sp = best_space("S000066")
        assert sp.contains((Fraction(1), Fraction(0)))
        assert sp.contains("0a")
        assert sp.contains("0b")
        assert not sp.contains((Fraction(0), Fraction(0)))   # origin excluded
        assert not sp.contains("xy")

    def test_sorgenfrey_plane_membership(self):
        sp = best_space("S000076")
        assert sp.contains((Fraction(0), Fraction(0)))
        assert sp.contains((Fraction(1, 2), Fraction(-3, 4)))
        assert not sp.contains((1, 2, 3))
        assert not sp.contains("xy")

    def test_double_arrow_membership(self):
        sp = best_space("S000093")
        assert sp.contains((0, Fraction(0)))
        assert sp.contains((1, Fraction(1)))
        assert sp.contains((0, Fraction(1, 2)))
        assert not sp.contains((2, Fraction(0)))      # first coord must be 0 or 1
        assert not sp.contains((0, Fraction(3, 2)))   # second must be in [0,1]

    def test_seq_fan_membership_batch4(self):
        for uid in ["S000131", "S000202"]:
            sp = best_space(uid)
            assert sp.contains((0, 0))
            assert sp.contains((3, 5))
            assert sp.contains("∞")
            assert not sp.contains((-1, 0))
            assert not sp.contains(0)

    def test_right_open_ray_01_membership(self):
        sp = best_space("S000159")
        assert sp.contains(Fraction(0))
        assert sp.contains(Fraction(1))
        assert sp.contains(Fraction(1, 2))
        assert not sp.contains(Fraction(-1, 4))
        assert not sp.contains(Fraction(3, 2))


# ---------------------------------------------------------------------------
# Batch 4 — property certificate checks via pi-Base
# ---------------------------------------------------------------------------

class TestBatch4Properties:
    def test_deleted_integer_not_t0(self):
        sp = best_space("S000006")
        assert is_t0(sp).value is False

    def test_either_or_t0_not_t1(self):
        sp = best_space("S000014")
        assert is_t0(sp).value is True
        assert is_t1(sp).value is False

    def test_either_or_compact(self):
        sp = best_space("S000014")
        assert is_compact(sp).value is True

    def test_compact_complement_t1_not_hausdorff(self):
        sp = best_space("S000019")
        assert is_t1(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_compact_complement_compact_connected(self):
        sp = best_space("S000019")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_fort_omega_hausdorff_compact(self):
        sp = best_space("S000020")
        assert is_hausdorff(sp).value is True
        assert is_compact(sp).value is True

    def test_fortissimo_hausdorff_not_compact(self):
        sp = best_space("S000022")
        assert is_hausdorff(sp).value is True
        assert is_compact(sp).value is False

    def test_modified_fort_t1_not_hausdorff(self):
        sp = best_space("S000024")
        assert is_t1(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_overlapping_interval_compact_connected(self):
        sp = best_space("S000045")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_smirnov_hausdorff_connected(self):
        sp = best_space("S000056")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is True

    def test_michael_line_hausdorff_not_connected(self):
        sp = best_space("S000063")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is False

    def test_telophase_t1_not_hausdorff_compact(self):
        sp = best_space("S000065")
        assert is_t1(sp).value is True
        assert is_hausdorff(sp).value is False
        assert is_compact(sp).value is True

    def test_double_origin_plane_hausdorff_connected(self):
        sp = best_space("S000066")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is True

    def test_sorgenfrey_plane_hausdorff_not_compact(self):
        sp = best_space("S000076")
        assert is_hausdorff(sp).value is True
        assert is_compact(sp).value is False

    def test_double_arrow_compact_not_connected(self):
        sp = best_space("S000093")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is False

    def test_right_open_ray_01_compact_connected(self):
        sp = best_space("S000159")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_right_open_ray_01_not_hausdorff(self):
        sp = best_space("S000159")
        assert is_hausdorff(sp).value is False

    def test_fort_space_reals_compact(self):
        sp = best_space("S000154")
        assert is_compact(sp).value is True


# ---------------------------------------------------------------------------
# Batch 5 — type checks, membership, and properties
# ---------------------------------------------------------------------------

class TestBatch5CertifiedSpaceTypes:
    @pytest.mark.parametrize("uid", [
        "S000018",  # double pointed cocountable
        "S000031",  # square of OPC(Q)
        "S000041",  # lex ordered unit square
        "S000067",  # irrational slope topology
        "S000068",  # deleted diameter
        "S000069",  # deleted radius
        "S000070",  # half-disc topology
        "S000071",  # irregular lattice
        "S000074",  # Niemytzki plane
        "S000075",  # rational tangent disc
        "S000084",  # line with countably many origins
        "S000086",  # everywhere doubled line
        "S000094",  # strong parallel line
        "S000095",  # concentric circles
        "S000099",  # Alexandroff square
        "S000112",  # nested rectangles
        "S000116",  # infinite broom
        "S000117",  # closed infinite broom
        "S000119",  # nested angles
    ])
    def test_is_certified_space(self, uid):
        assert isinstance(best_space(uid), _CertifiedSpace)


class TestBatch5Membership:
    def test_double_pointed_cocountable(self):
        sp = best_space("S000018")
        assert sp.contains((Fraction(1, 2), 0))
        assert sp.contains((Fraction(0), 1))
        assert not sp.contains((Fraction(0), 2))
        assert not sp.contains(Fraction(0))

    def test_square_opc_Q(self):
        sp = best_space("S000031")
        assert sp.contains((Fraction(1, 2), Fraction(0)))
        assert sp.contains(("∞", Fraction(1, 3)))
        assert sp.contains(("∞", "∞"))
        assert not sp.contains((Fraction(0),))    # not a pair
        assert not sp.contains((Fraction(0), "x"))

    def test_unit_square_member(self):
        for uid in ["S000041", "S000099"]:
            sp = best_space(uid)
            assert sp.contains((Fraction(0), Fraction(0)))
            assert sp.contains((Fraction(1), Fraction(1)))
            assert sp.contains((Fraction(1, 2), Fraction(1, 3)))
            assert not sp.contains((Fraction(3, 2), Fraction(0)))  # x > 1
            assert not sp.contains((Fraction(0), Fraction(-1, 2))) # y < 0

    def test_plane_member_spaces(self):
        for uid in ["S000067", "S000068", "S000069", "S000075",
                    "S000094", "S000095", "S000112", "S000119"]:
            sp = best_space(uid)
            assert sp.contains((Fraction(0), Fraction(0)))
            assert sp.contains((Fraction(1, 2), Fraction(-3, 4)))
            assert not sp.contains((1, 2, 3))
            assert not sp.contains("xy")

    def test_upper_half_member_spaces(self):
        for uid in ["S000070", "S000074"]:
            sp = best_space(uid)
            assert sp.contains((Fraction(0), Fraction(0)))      # x-axis
            assert sp.contains((Fraction(1), Fraction(1, 2)))   # y > 0
            assert not sp.contains((Fraction(0), Fraction(-1))) # y < 0

    def test_integer_lattice_member(self):
        sp = best_space("S000071")
        assert sp.contains((0, 0))
        assert sp.contains((-3, 5))
        assert not sp.contains((0, Fraction(1, 2)))  # not int
        assert not sp.contains(0)

    def test_line_countable_origins(self):
        sp = best_space("S000084")
        assert sp.contains(Fraction(1, 2))
        assert sp.contains(-1)
        assert sp.contains((0, 0))    # origin copy 0
        assert sp.contains((0, 3))    # origin copy 3
        assert not sp.contains(0)     # actual 0 not in carrier
        assert not sp.contains((0, -1))  # negative copy not in carrier
        assert not sp.contains("x")

    def test_everywhere_doubled_line(self):
        sp = best_space("S000086")
        assert sp.contains((Fraction(1, 2), 0))
        assert sp.contains((Fraction(1, 2), 1))
        assert sp.contains((0, 0))
        assert not sp.contains((Fraction(0), 2))

    def test_infinite_broom(self):
        sp = best_space("S000116")
        assert sp.contains((Fraction(0), Fraction(0)))    # base point
        assert sp.contains((Fraction(1), Fraction(1, 2))) # spoke 1/1
        assert sp.contains((Fraction(1, 2), Fraction(1))) # spoke 1/2
        assert sp.contains((Fraction(1, 3), Fraction(0))) # spoke 1/3
        assert not sp.contains((Fraction(1, 2), Fraction(-1)))  # y < 0
        assert not sp.contains((Fraction(2, 3), Fraction(0)))   # 2/3 not 1/n
        assert not sp.contains((Fraction(0), Fraction(1)))      # not at base

    def test_closed_infinite_broom(self):
        sp = best_space("S000117")
        assert sp.contains((Fraction(0), Fraction(0)))
        assert sp.contains((Fraction(0), Fraction(1, 2)))  # spine point
        assert sp.contains((Fraction(0), Fraction(1)))     # spine endpoint
        assert sp.contains((Fraction(1), Fraction(1, 2))) # spoke 1/1
        assert not sp.contains((Fraction(2, 3), Fraction(0)))  # 2/3 not 1/n
        assert not sp.contains((Fraction(0), Fraction(-1)))


class TestBatch5Properties:
    def test_double_pointed_cocountable_not_t0(self):
        sp = best_space("S000018")
        assert is_t0(sp).value is False

    def test_lex_unit_square_compact_connected(self):
        sp = best_space("S000041")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_deleted_diameter_hausdorff_connected(self):
        sp = best_space("S000068")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is True

    def test_deleted_radius_hausdorff(self):
        sp = best_space("S000069")
        assert is_hausdorff(sp).value is True

    def test_half_disc_hausdorff_connected(self):
        sp = best_space("S000070")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is True

    def test_irregular_lattice_hausdorff_not_connected(self):
        sp = best_space("S000071")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is False

    def test_niemytzki_hausdorff_connected(self):
        sp = best_space("S000074")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is True

    def test_concentric_circles_compact(self):
        sp = best_space("S000095")
        assert is_compact(sp).value is True

    def test_alexandroff_square_compact_connected(self):
        sp = best_space("S000099")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_infinite_broom_connected_not_compact(self):
        sp = best_space("S000116")
        assert is_connected(sp).value is True
        assert is_compact(sp).value is False

    def test_closed_infinite_broom_compact_connected(self):
        sp = best_space("S000117")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_line_countable_origins_t1_not_hausdorff(self):
        sp = best_space("S000084")
        assert is_t1(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_everywhere_doubled_t1_not_hausdorff(self):
        sp = best_space("S000086")
        assert is_t1(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_square_opc_Q_compact_connected(self):
        sp = best_space("S000031")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True


# ---------------------------------------------------------------------------
# Batch 6 — type checks, membership, and properties
# ---------------------------------------------------------------------------

class TestBatch6CertifiedSpaceTypes:
    @pytest.mark.parametrize("uid", [
        "S000060",  # pointed rational extension
        "S000062",  # discrete rational extension
        "S000072",  # Arens square
        "S000073",  # simplified Arens square
        "S000080",  # B. Scott's modified Arens square
        "S000129",  # wheel without hub
        "S000135",  # radial interval topology
        "S000139",  # countable bouquet of circles
        "S000143",  # butterfly space
        "S000145",  # free ultrafilter topology on ω
        "S000152",  # poset broom Alexandroff
        "S000156",  # Arens space
        "S000169",  # sphere S²
        "S000170",  # circle S¹
        "S000175",  # radial plane
        "S000192",  # modified telophase
        "S000201",  # infinite earring
        "S000205",  # Warsaw circle
        "S000209",  # circle with two origins
    ])
    def test_is_certified_space(self, uid):
        assert isinstance(best_space(uid), _CertifiedSpace)


class TestBatch6Membership:
    def test_pointed_rational_ext(self):
        sp = best_space("S000060")
        assert sp.contains(0)
        assert sp.contains(Fraction(1, 2))
        assert sp.contains((Fraction(1, 3), 1))   # copy of rational
        assert sp.contains((0, 1))                  # copy of 0
        assert not sp.contains((Fraction(1, 2), 2))  # wrong tag
        assert not sp.contains("x")

    def test_discrete_rational_ext(self):
        sp = best_space("S000062")
        assert sp.contains(0)
        assert sp.contains((Fraction(1, 3), 1))
        assert not sp.contains((Fraction(1), 2))
        assert not sp.contains("x")

    def test_unit_square_arens(self):
        for uid in ["S000072", "S000073", "S000080"]:
            sp = best_space(uid)
            assert sp.contains((Fraction(0), Fraction(0)))
            assert sp.contains((Fraction(1, 2), Fraction(1, 2)))
            assert not sp.contains((Fraction(3, 2), Fraction(0)))
            assert not sp.contains("xy")

    def test_plane_member_batch6(self):
        for uid in ["S000129", "S000135", "S000143", "S000175", "S000201", "S000205"]:
            sp = best_space(uid)
            assert sp.contains((Fraction(0), Fraction(0)))
            assert sp.contains((Fraction(1, 2), Fraction(-1, 3)))
            assert not sp.contains((1, 2, 3))
            assert not sp.contains("xy")

    def test_bouquet_membership(self):
        sp = best_space("S000139")
        assert sp.contains((0, Fraction(0)))
        assert sp.contains((3, Fraction(1, 2)))
        assert not sp.contains((0, Fraction(1)))    # q must be < 1
        assert not sp.contains((-1, Fraction(0)))   # n must be ≥ 0

    def test_ultrafilter_omega_membership(self):
        sp = best_space("S000145")
        assert sp.contains(0)
        assert sp.contains(42)
        assert not sp.contains(-1)
        assert not sp.contains("x")

    def test_poset_broom_membership(self):
        sp = best_space("S000152")
        assert sp.contains(-1)
        assert sp.contains("0a")
        assert sp.contains("0b")
        assert sp.contains(Fraction(1))        # 1/1
        assert sp.contains(Fraction(1, 2))     # 1/2
        assert sp.contains(Fraction(1, 10))    # 1/10
        assert not sp.contains(Fraction(2, 3)) # 2/3 is not 1/n
        assert sp.contains(Fraction(-1))       # -1 IS in carrier (minimum element)
        assert not sp.contains(Fraction(-2))   # -2 not in carrier
        assert not sp.contains(0)              # 0 not in carrier

    def test_arens_space_membership(self):
        sp = best_space("S000156")
        assert sp.contains((0, 0))
        assert sp.contains((3, 7))
        assert sp.contains("∞")
        assert not sp.contains(0)

    def test_circle_S1_membership(self):
        sp = best_space("S000170")
        assert sp.contains((Fraction(1), Fraction(0)))    # (1,0) on circle
        assert sp.contains((Fraction(-1), Fraction(0)))   # (-1,0)
        assert sp.contains((Fraction(3, 5), Fraction(4, 5)))  # Pythagorean
        assert not sp.contains((Fraction(1, 2), Fraction(1, 2)))  # 1/4+1/4 ≠ 1
        assert not sp.contains("x")

    def test_sphere_S2_membership(self):
        sp = best_space("S000169")
        assert sp.contains((Fraction(1), Fraction(0), Fraction(0)))   # poles
        assert sp.contains((Fraction(0), Fraction(0), Fraction(-1)))
        assert sp.contains((Fraction(3, 5), Fraction(4, 5), Fraction(0)))  # equatorial
        assert not sp.contains((Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)))  # 3/4≠1
        assert not sp.contains("x")

    def test_circle_two_origins_membership(self):
        sp = best_space("S000209")
        assert sp.contains("0a")
        assert sp.contains("0b")
        assert sp.contains((Fraction(-1), Fraction(0)))  # (-1,0) on circle
        assert sp.contains((Fraction(3, 5), Fraction(4, 5)))
        assert not sp.contains((Fraction(1), Fraction(0)))  # doubled point excluded
        assert not sp.contains((1, 0))
        assert not sp.contains("x")

    def test_modified_telophase_membership(self):
        sp = best_space("S000192")
        assert sp.contains(Fraction(0))
        assert sp.contains(Fraction(1, 2))
        assert sp.contains(Fraction(1))
        assert not sp.contains(Fraction(-1))
        assert not sp.contains(Fraction(3, 2))


class TestBatch6Properties:
    def test_pointed_rational_ext_hausdorff(self):
        sp = best_space("S000060")
        assert is_hausdorff(sp).value is True

    def test_discrete_rational_ext_not_connected(self):
        sp = best_space("S000062")
        assert is_connected(sp).value is False

    def test_arens_square_hausdorff_not_compact(self):
        sp = best_space("S000072")
        assert is_hausdorff(sp).value is True
        assert is_compact(sp).value is False

    def test_simplified_arens_square_connected(self):
        sp = best_space("S000073")
        assert is_connected(sp).value is True

    def test_poset_broom_compact_not_t1(self):
        sp = best_space("S000152")
        assert is_compact(sp).value is True
        assert is_t1(sp).value is False

    def test_circle_S1_compact_connected(self):
        sp = best_space("S000170")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_sphere_S2_compact_connected(self):
        sp = best_space("S000169")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_circle_two_origins_t1_not_hausdorff(self):
        sp = best_space("S000209")
        assert is_t1(sp).value is True     # pi-Base: T1=True
        assert is_hausdorff(sp).value is False
        assert is_compact(sp).value is True

    def test_warsaw_circle_compact_connected(self):
        sp = best_space("S000205")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_infinite_earring_compact_connected(self):
        sp = best_space("S000201")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_modified_telophase_compact_not_hausdorff(self):
        sp = best_space("S000192")
        assert is_compact(sp).value is True
        assert is_hausdorff(sp).value is False

    def test_ultrafilter_not_hausdorff(self):
        sp = best_space("S000145")
        assert is_hausdorff(sp).value is False


# ---------------------------------------------------------------------------
# Batch 7 — type checks, membership, and properties
# ---------------------------------------------------------------------------

class TestBatch7CertifiedSpaceTypes:
    @pytest.mark.parametrize("uid", [
        "S000058",  # indiscrete rational extension
        "S000059",  # indiscrete irrational extension
        "S000061",  # pointed irrational extension
        "S000064",  # rational extension of plane
        "S000113",  # topologist's sine curve
        "S000114",  # closed topologist's sine
        "S000115",  # extended topologist's sine
        "S000120",  # infinite cage
        "S000122",  # Gustin's sequence space
        "S000123",  # Roy's lattice space
        "S000124",  # Roy's lattice subspace
        "S000125",  # KK fan
        "S000126",  # punctured KK fan
        "S000130",  # Tangora's connected space
        "S000132",  # Duncan's space
        "S000161",  # Van Douwen's space
        "S000167",  # right open-ray ω+1+ω*
        "S000171",  # Brian's Example
        "S000183",  # KP Hart's modified
    ])
    def test_is_certified_space(self, uid):
        assert isinstance(best_space(uid), _CertifiedSpace)


class TestBatch7Membership:
    def test_real_member_batch7(self):
        for uid in ["S000058", "S000059", "S000061", "S000171"]:
            sp = best_space(uid)
            assert sp.contains(0)
            assert sp.contains(Fraction(1, 3))
            assert not sp.contains("x")

    def test_rat_ext_plane(self):
        sp = best_space("S000064")
        assert sp.contains((Fraction(0), Fraction(0)))           # original plane point
        assert sp.contains((Fraction(1, 2), Fraction(-1, 3)))    # original plane point
        assert sp.contains((Fraction(1, 2), Fraction(0), 1))     # rational copy
        assert sp.contains((Fraction(0), Fraction(1), 1))
        assert not sp.contains((Fraction(1), Fraction(0), 2))    # wrong tag
        assert not sp.contains("x")

    def test_plane_member_batch7(self):
        for uid in ["S000113", "S000114", "S000115", "S000120"]:
            sp = best_space(uid)
            assert sp.contains((Fraction(0), Fraction(0)))
            assert sp.contains((Fraction(1, 2), Fraction(1, 3)))
            assert not sp.contains("xy")

    def test_omega_member_batch7(self):
        for uid in ["S000122", "S000130", "S000132", "S000183"]:
            sp = best_space(uid)
            assert sp.contains(0)
            assert sp.contains(10)
            assert not sp.contains(-1)
            assert not sp.contains("x")

    def test_int_plane_member_batch7(self):
        for uid in ["S000123", "S000124"]:
            sp = best_space(uid)
            assert sp.contains((0, 0))
            assert sp.contains((-3, 5))
            assert not sp.contains((Fraction(1, 2), 0))
            assert not sp.contains(0)

    def test_unit_square_batch7(self):
        for uid in ["S000125", "S000126"]:
            sp = best_space(uid)
            assert sp.contains((Fraction(0), Fraction(0)))
            assert sp.contains((Fraction(1, 2), Fraction(1, 2)))
            assert not sp.contains((Fraction(3, 2), Fraction(0)))

    def test_van_douwen_membership(self):
        sp = best_space("S000161")
        assert sp.contains((0, 0))
        assert sp.contains((3, 5))
        assert sp.contains("∞")
        assert not sp.contains(0)

    def test_right_open_ray_w1_wstar(self):
        sp = best_space("S000167")
        assert sp.contains((0, 0))    # first ω copy
        assert sp.contains((1, 3))    # reverse ω copy
        assert sp.contains("∞")       # limit point
        assert not sp.contains("Ω")
        assert not sp.contains(0)

    def test_kp_hart_omega(self):
        sp = best_space("S000183")
        assert sp.contains(0)
        assert sp.contains(42)
        assert not sp.contains(-1)


class TestBatch7Properties:
    def test_indiscrete_rational_ext_hausdorff(self):
        sp = best_space("S000058")
        assert is_hausdorff(sp).value is True

    def test_rat_ext_plane_hausdorff_not_connected(self):
        sp = best_space("S000064")
        assert is_hausdorff(sp).value is True
        assert is_connected(sp).value is False

    def test_closed_topologist_sine_compact(self):
        sp = best_space("S000114")
        assert is_compact(sp).value is True
        assert is_connected(sp).value is True

    def test_topologist_sine_connected(self):
        sp = best_space("S000113")
        assert is_connected(sp).value is True
        assert is_compact(sp).value is False

    def test_kk_fan_connected_not_compact(self):
        sp = best_space("S000125")
        assert is_connected(sp).value is True
        assert is_compact(sp).value is False

    def test_punctured_kk_fan_not_connected(self):
        sp = best_space("S000126")
        assert is_connected(sp).value is False

    def test_gustin_connected_hausdorff(self):
        sp = best_space("S000122")
        assert is_connected(sp).value is True
        assert is_hausdorff(sp).value is True

    def test_right_open_ray_w1_wstar_t1_false(self):
        sp = best_space("S000167")
        assert is_t1(sp).value is False
        assert is_compact(sp).value is True

    def test_van_douwen_not_hausdorff_compact(self):
        sp = best_space("S000161")
        assert is_hausdorff(sp).value is False
        assert is_compact(sp).value is True


# ---------------------------------------------------------------------------
# Batch 8: sequence/function spaces and RP²
# ---------------------------------------------------------------------------

class TestBatch8CertifiedSpaceTypes:
    @pytest.mark.parametrize("uid", [
        "S000021", "S000030", "S000032", "S000105", "S000107", "S000146", "S000168",
    ])
    def test_is_certified_space(self, uid: str) -> None:
        assert isinstance(best_space(uid), _CertifiedSpace)

    def test_erdos_is_metric(self) -> None:
        assert isinstance(best_space("S000142"), _MetricWithCerts)


class TestBatch8SequenceMembership:
    def test_seq_frac_member_basic(self) -> None:
        for uid in ("S000021", "S000030", "S000107", "S000146"):
            sp = best_space(uid)
            assert sp.contains(())                           # empty = zero sequence
            assert sp.contains((Fraction(1), Fraction(0)))
            assert sp.contains((Fraction(1, 2), Fraction(-3)))
            assert not sp.contains(42)
            assert not sp.contains("x")
            assert not sp.contains((1.0, 2.0))              # float, not Fraction

    def test_hilbert_cube_unit_bounds(self) -> None:
        sp = best_space("S000032")
        assert sp.contains(())
        assert sp.contains((Fraction(0), Fraction(1, 2), Fraction(1)))
        assert not sp.contains((Fraction(0), Fraction(3, 2)))   # > 1
        assert not sp.contains((Fraction(-1, 4),))               # < 0
        assert not sp.contains((Fraction(1, 2), 0.5))            # float

    def test_helly_space_monotone(self) -> None:
        sp = best_space("S000105")
        assert sp.contains(())
        assert sp.contains((Fraction(0), Fraction(1, 2), Fraction(1)))   # non-decreasing
        assert sp.contains((Fraction(1, 4), Fraction(1, 4)))              # equal is ok
        assert not sp.contains((Fraction(1), Fraction(0)))                # decreasing
        assert not sp.contains((Fraction(0), Fraction(3, 2)))             # > 1

    def test_erdos_space_membership(self) -> None:
        sp = best_space("S000142")
        assert sp.contains(())
        assert sp.contains((Fraction(1), Fraction(0)))
        assert sp.contains((Fraction(1, 3), Fraction(-1, 3)))
        assert not sp.contains((1.0, 2.0))
        assert not sp.contains("x")

    def test_rp2_membership(self) -> None:
        sp = best_space("S000168")
        assert sp.contains((Fraction(1), Fraction(0), Fraction(0)))       # [1:0:0]
        assert sp.contains((Fraction(0), Fraction(1), Fraction(0)))       # [0:1:0]
        assert sp.contains((Fraction(1), Fraction(1), Fraction(1)))       # [1:1:1]
        assert sp.contains((Fraction(1), Fraction(-1, 2), Fraction(3)))   # [1:-1/2:3]
        assert not sp.contains((Fraction(2), Fraction(0), Fraction(0)))   # not canonical
        assert not sp.contains((Fraction(0), Fraction(2), Fraction(0)))   # not canonical
        assert not sp.contains((Fraction(0), Fraction(0), Fraction(0)))   # zero vector
        assert not sp.contains("x")
        assert not sp.contains((Fraction(1), Fraction(1)))                # wrong length
        assert not sp.contains((Fraction(1), Fraction(1), Fraction(1), Fraction(0)))  # len 4


class TestBatch8Properties:
    def test_hilbert_cube_compact(self) -> None:
        sp = best_space("S000032")
        cert = sp.certificate("compact")
        assert cert is not None
        assert cert.value is True

    def test_rp2_compact_connected(self) -> None:
        sp = best_space("S000168")
        assert sp.certificate("compact") is not None
        assert sp.certificate("compact").value is True  # type: ignore[union-attr]
        assert sp.certificate("connected") is not None
        assert sp.certificate("connected").value is True  # type: ignore[union-attr]

    def test_erdos_separable(self) -> None:
        sp = best_space("S000142")
        cert = sp.certificate("separable")
        assert cert is not None
        assert cert.value is True

    def test_real_omega_connected(self) -> None:
        sp = best_space("S000030")
        cert = sp.certificate("connected")
        assert cert is not None
        assert cert.value is True
