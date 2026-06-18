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
    assert len(reps) == 67


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
