"""Coverage-targeted tests for alexandroff.py (v0.5.1)."""
import pytest
from pytop.alexandroff import (
    AlexandroffError,
    normalize_carrier,
    normalize_relation,
    transitive_closure,
    principal_upset,
    principal_downset,
    is_upper_set,
    upper_sets,
    alexandroff_space_from_preorder,
    minimal_open_neighborhood,
    specialization_preorder,
    preorder_from_space,
    preorder_kernel_relation,
    preorder_t0_reduction_data,
    t0_reduction_profile,
    analyze_alexandroff,
    is_alexandroff_space,
    alexandroff_report,
    poset_mobius,
    poset_mobius_report,
    poset_isomorphic,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# normalize_carrier errors  (line 27)
# ---------------------------------------------------------------------------

def test_normalize_carrier_duplicates():
    with pytest.raises(AlexandroffError, match="distinct"):
        normalize_carrier([1, 2, 1])


# ---------------------------------------------------------------------------
# normalize_relation errors  (lines 37, 40)
# ---------------------------------------------------------------------------

def test_normalize_relation_bad_pair_length():
    with pytest.raises(AlexandroffError, match="length 2"):
        normalize_relation([1, 2], [(1,)])  # triple missing second element


def test_normalize_relation_element_outside_carrier():
    with pytest.raises(AlexandroffError, match="outside the carrier"):
        normalize_relation([1, 2], [(1, 3)])


# ---------------------------------------------------------------------------
# transitive_closure  (lines 63, 65-66)
# ---------------------------------------------------------------------------

def test_transitive_closure_chain():
    # a <= b <= c  →  must infer a <= c
    carrier = [1, 2, 3]
    relation = [(1, 2), (2, 3)]
    result = transitive_closure(carrier, relation)
    assert (1, 3) in result
    assert (1, 2) in result
    assert (2, 3) in result


def test_transitive_closure_diamond():
    carrier = [1, 2, 3, 4]
    relation = [(1, 2), (1, 3), (2, 4), (3, 4)]
    result = transitive_closure(carrier, relation)
    assert (1, 4) in result


# ---------------------------------------------------------------------------
# principal_upset / principal_downset errors  (lines 104, 109-113)
# ---------------------------------------------------------------------------

def test_principal_upset_point_not_in_carrier():
    with pytest.raises(AlexandroffError, match="not in the carrier"):
        principal_upset([1, 2], [(1, 2)], 99)


def test_principal_downset_point_not_in_carrier():
    with pytest.raises(AlexandroffError, match="not in the carrier"):
        principal_downset([1, 2], [(1, 2)], 99)


def test_principal_upset_basic():
    carrier = [1, 2, 3]
    relation = [(1, 2), (2, 3)]
    result = principal_upset(carrier, relation, 1)
    assert 1 in result
    assert 2 in result
    assert 3 in result


def test_principal_downset_basic():
    carrier = [1, 2, 3]
    relation = [(1, 2), (2, 3)]
    result = principal_downset(carrier, relation, 3)
    assert 1 in result
    assert 2 in result
    assert 3 in result


# ---------------------------------------------------------------------------
# upper_sets  (lines 120, 136)
# ---------------------------------------------------------------------------

def test_upper_sets_chain():
    # Linear order 1 <= 2 <= 3
    carrier = [1, 2, 3]
    relation = [(1, 2), (2, 3)]
    us = upper_sets(carrier, relation)
    # All upper sets: {}, {3}, {2,3}, {1,2,3}
    carrier_set = set(carrier)
    assert any(len(s) == 0 for s in us)
    assert carrier_set in [set(s) for s in us]


def test_upper_sets_antichain():
    # Antichain: no comparable pairs except reflexive
    carrier = [1, 2]
    relation = []
    us = upper_sets(carrier, relation)
    # All subsets are upper sets: {}, {1}, {2}, {1,2}
    assert len(us) >= 3


# ---------------------------------------------------------------------------
# minimal_open_neighborhood errors  (lines 165, 167, 170)
# ---------------------------------------------------------------------------

def test_minimal_open_neighborhood_no_topology():
    class Bare:
        pass
    with pytest.raises(AlexandroffError, match="explicit topology"):
        minimal_open_neighborhood(Bare(), 1)


def test_minimal_open_neighborhood_point_not_in_carrier():
    space = alexandroff_space_from_preorder([1, 2], [(1, 2)])
    with pytest.raises(AlexandroffError, match="not in the carrier"):
        minimal_open_neighborhood(space, 99)


# ---------------------------------------------------------------------------
# specialization_preorder error  (line 181)
# ---------------------------------------------------------------------------

def test_specialization_preorder_no_topology():
    class Bare:
        pass
    with pytest.raises(AlexandroffError, match="explicit topology"):
        specialization_preorder(Bare())


# ---------------------------------------------------------------------------
# preorder_from_space  (line 192)
# ---------------------------------------------------------------------------

def test_preorder_from_space_equals_specialization():
    space = alexandroff_space_from_preorder([1, 2], [(1, 2)])
    sp1 = specialization_preorder(space)
    sp2 = preorder_from_space(space)
    assert sp1 == sp2


# ---------------------------------------------------------------------------
# t0_reduction_profile error  (line 230)
# ---------------------------------------------------------------------------

def test_t0_reduction_profile_no_topology():
    class Bare:
        pass
    with pytest.raises(AlexandroffError, match="explicit finite topology"):
        t0_reduction_profile(Bare())


def test_t0_reduction_profile_basic():
    # Non-T0: two points share all open neighborhoods
    carrier = frozenset({1, 2})
    topology = frozenset([frozenset(), frozenset({1, 2})])
    space = FiniteTopologicalSpace(carrier=carrier, topology=topology)
    p = t0_reduction_profile(space)
    assert "carrier_size" in p
    assert "quotient_size" in p
    assert p["carrier_size"] == 2
    assert p["quotient_size"] == 1  # both points collapse


# ---------------------------------------------------------------------------
# analyze_alexandroff — tag path  (lines 257-264)
# ---------------------------------------------------------------------------

def test_analyze_alexandroff_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(
        description="test",
        tags=["alexandroff", "compact"],
    )
    r = analyze_alexandroff(space)
    assert r.is_true
    assert r.mode == "symbolic"


def test_analyze_alexandroff_unknown():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="bare")
    r = analyze_alexandroff(space)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# poset_mobius  (lines 312-333)
# ---------------------------------------------------------------------------

def test_poset_mobius_chain():
    # Chain 1 <= 2 <= 3
    carrier = [1, 2, 3]
    relation = [(1, 2), (2, 3)]
    mu = poset_mobius(carrier, relation)
    assert mu[(1, 1)] == 1
    assert mu[(2, 2)] == 1
    assert mu[(3, 3)] == 1
    assert mu[(1, 2)] == -1
    assert mu[(2, 3)] == -1
    assert mu[(1, 3)] == 0  # chain: μ(1,3)=0 (skips two steps)
    assert mu[(3, 1)] == 0  # not comparable


def test_poset_mobius_antichain():
    carrier = [1, 2]
    relation = []
    mu = poset_mobius(carrier, relation)
    assert mu[(1, 1)] == 1
    assert mu[(2, 2)] == 1
    assert mu[(1, 2)] == 0  # not comparable
    assert mu[(2, 1)] == 0


def test_poset_mobius_not_partial_order_raises():
    # Cycle is not antisymmetric
    carrier = [1, 2]
    relation = [(1, 2), (2, 1)]
    with pytest.raises(AlexandroffError, match="partial order"):
        poset_mobius(carrier, relation)


# ---------------------------------------------------------------------------
# poset_mobius_report  (lines 341-344)
# ---------------------------------------------------------------------------

def test_poset_mobius_report_chain():
    carrier = [1, 2, 3]
    relation = [(1, 2), (2, 3)]
    report = poset_mobius_report(carrier, relation)
    assert report["carrier_size"] == 3
    assert "mobius_function" in report
    assert "nonzero_entries" in report
    assert report["nonzero_count"] > 0
    assert "zeta_inverse_check" in report


def test_poset_mobius_report_single():
    report = poset_mobius_report([1], [])
    assert report["carrier_size"] == 1
    assert report["nonzero_count"] == 1  # only mu(1,1)=1


# ---------------------------------------------------------------------------
# poset_isomorphic  (lines 372-416)
# ---------------------------------------------------------------------------

def test_poset_isomorphic_identical_chains():
    c1 = [1, 2, 3]
    r1 = [(1, 2), (2, 3)]
    c2 = ["a", "b", "c"]
    r2 = [("a", "b"), ("b", "c")]
    assert poset_isomorphic(c1, r1, c2, r2) is True


def test_poset_isomorphic_different_structure():
    # chain vs antichain
    c1 = [1, 2, 3]
    r1 = [(1, 2), (2, 3)]
    c2 = ["a", "b", "c"]
    r2 = []
    assert poset_isomorphic(c1, r1, c2, r2) is False


def test_poset_isomorphic_different_sizes():
    c1 = [1, 2]
    r1 = [(1, 2)]
    c2 = [1, 2, 3]
    r2 = [(1, 2), (2, 3)]
    assert poset_isomorphic(c1, r1, c2, r2) is False


def test_poset_isomorphic_antichains():
    c1 = [1, 2]
    r1 = []
    c2 = ["x", "y"]
    r2 = []
    assert poset_isomorphic(c1, r1, c2, r2) is True


def test_poset_isomorphic_two_element_chain():
    c1 = [1, 2]
    r1 = [(1, 2)]
    c2 = ["a", "b"]
    r2 = [("a", "b")]
    assert poset_isomorphic(c1, r1, c2, r2) is True


def test_poset_isomorphic_diamond():
    # Two diamonds should be isomorphic
    c1 = [1, 2, 3, 4]
    r1 = [(1, 2), (1, 3), (2, 4), (3, 4)]
    c2 = ["a", "b", "c", "d"]
    r2 = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    assert poset_isomorphic(c1, r1, c2, r2) is True
