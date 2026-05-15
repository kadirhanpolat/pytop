"""Tests for v0.1.51 Cilt III neighborhood systems corridor.

Covers neighborhood_systems.py: axiom checks, N(x) computation,
local base verification, character, topology recovery, and analyze entry-point.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from pytop.neighborhood_systems import (
    neighborhood_system_axioms,
    neighborhood_system,
    local_base_check,
    character_at_point,
    topology_from_neighborhood_system,
    analyze_neighborhood_system,
)
import pytop

# Shared test spaces
SIERPINSKI_CARRIER = [0, 1]
SIERPINSKI_TOPOLOGY = [frozenset(), frozenset([1]), frozenset([0, 1])]

DISCRETE2 = [frozenset(), frozenset(['a']), frozenset(['b']), frozenset(['a', 'b'])]
CARRIER2 = ['a', 'b']

THREE_CARRIER = ['a', 'b', 'c']
THREE_TOPOLOGY = [
    frozenset(), frozenset(['a']), frozenset(['a', 'b']), frozenset(['a', 'b', 'c'])
]

# ---------------------------------------------------------------------------
# neighborhood_system_axioms
# ---------------------------------------------------------------------------

class TestNeighborhoodSystemAxioms:
    def test_sierpinski_1_all_pass(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.is_true
        assert r.value["all_axioms"] is True

    def test_sierpinski_0_all_pass(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 0)
        assert r.is_true
        assert r.value["all_axioms"] is True

    def test_n1_x_in_N(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.value["N1_x_in_N"] is True

    def test_n2_X_in_Nx(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 0)
        assert r.value["N2_X_in_Nx"] is True

    def test_n3_finite_intersection(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.value["N3_finite_intersection"] is True

    def test_n4_superset_closed(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.value["N4_superset_closed"] is True

    def test_three_point_a(self):
        r = neighborhood_system_axioms(THREE_CARRIER, THREE_TOPOLOGY, 'a')
        assert r.is_true and r.value["all_axioms"] is True

    def test_three_point_c(self):
        r = neighborhood_system_axioms(THREE_CARRIER, THREE_TOPOLOGY, 'c')
        assert r.is_true and r.value["all_axioms"] is True

    def test_invalid_point_unknown(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 99)
        assert not r.is_true

    def test_metadata_carrier_size(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.metadata["carrier_size"] == 2

    def test_metadata_corridor(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.metadata["cilt_iii_corridor"] == "neighborhood-systems"

    def test_v051_flag(self):
        r = neighborhood_system_axioms(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.metadata["v0_1_51_corridor_record"] is True


# ---------------------------------------------------------------------------
# neighborhood_system
# ---------------------------------------------------------------------------

class TestNeighborhoodSystem:
    def test_sierpinski_N1_count(self):
        # N(1) = {{1}, {0,1}} — two neighborhoods
        r = neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.is_true
        assert r.metadata["neighborhood_count"] == 2

    def test_sierpinski_N0_count(self):
        # N(0) = {{0,1}} — only the whole space
        r = neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 0)
        assert r.metadata["neighborhood_count"] == 1

    def test_discrete_full_neighborhoods(self):
        # In discrete topology every superset of {x} is a neighborhood
        disc = [frozenset(), frozenset(['a']), frozenset(['b']), frozenset(['a','b'])]
        r = neighborhood_system(['a','b'], disc, 'a')
        assert r.metadata["neighborhood_count"] >= 2

    def test_invalid_point(self):
        r = neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 99)
        assert not r.is_true

    def test_v051_flag(self):
        r = neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.metadata["v0_1_51_corridor_record"] is True


# ---------------------------------------------------------------------------
# local_base_check
# ---------------------------------------------------------------------------

class TestLocalBaseCheck:
    def test_singleton_is_local_base_at_1(self):
        # {1} is a local base at 1 in Sierpinski
        r = local_base_check(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY,
                             1, [frozenset([1])])
        assert r.is_true and r.value is True

    def test_full_N1_is_local_base(self):
        # {{1},{0,1}} is a local base at 1
        r = local_base_check(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY,
                             1, [frozenset([1]), frozenset([0,1])])
        assert r.is_true and r.value is True

    def test_non_neighborhood_fails_cond1(self):
        # {0} alone is not a neighborhood of 1
        r = local_base_check(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY,
                             1, [frozenset([0])])
        assert r.is_true and r.value is False
        assert r.metadata["cond1_all_neighborhoods"] is False

    def test_insufficient_base_fails_cond2(self):
        # At point 0: N(0)={{0,1}}; candidate {} (empty family) fails cond2
        r = local_base_check(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY,
                             0, [])
        assert r.value is False

    def test_three_point_open_base(self):
        # {a} is in the topology and contains a, so it's a neighborhood and a local base
        r = local_base_check(THREE_CARRIER, THREE_TOPOLOGY,
                             'a', [frozenset(['a'])])
        assert r.value is True

    def test_metadata_fields(self):
        r = local_base_check(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY,
                             1, [frozenset([1])])
        assert "cond1_all_neighborhoods" in r.metadata
        assert "cond2_cofinal" in r.metadata
        assert "is_local_base" in r.metadata

    def test_v051_flag(self):
        r = local_base_check(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY,
                             1, [frozenset([1])])
        assert r.metadata["v0_1_51_corridor_record"] is True


# ---------------------------------------------------------------------------
# character_at_point
# ---------------------------------------------------------------------------

class TestCharacterAtPoint:
    def test_sierpinski_chi_1(self):
        # Open neighborhoods of 1: {1} and {0,1} → χ=2
        r = character_at_point(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.is_true and r.value == 2

    def test_sierpinski_chi_0(self):
        # Open neighborhoods of 0: only {0,1} → χ=1
        r = character_at_point(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 0)
        assert r.value == 1

    def test_indiscrete_chi(self):
        # Indiscrete: only X is open and contains x → χ=1 for each point
        indisc = [frozenset(), frozenset(['a','b'])]
        for pt in ['a', 'b']:
            r = character_at_point(['a','b'], indisc, pt)
            assert r.value == 1

    def test_discrete_chi(self):
        # Discrete on {a,b}: open neighborhoods of a: {a}, {a,b} → χ=2
        disc = [frozenset(), frozenset(['a']), frozenset(['b']), frozenset(['a','b'])]
        r = character_at_point(['a','b'], disc, 'a')
        assert r.value == 2

    def test_invalid_point(self):
        r = character_at_point(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 99)
        assert not r.is_true

    def test_metadata_open_neighborhoods(self):
        r = character_at_point(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert "open_neighborhoods" in r.metadata
        assert len(r.metadata["open_neighborhoods"]) == 2

    def test_v051_flag(self):
        r = character_at_point(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.metadata["v0_1_51_corridor_record"] is True


# ---------------------------------------------------------------------------
# topology_from_neighborhood_system
# ---------------------------------------------------------------------------

class TestTopologyFromNeighborhoodSystem:
    def _build_nbhd(self, carrier, topology):
        open_sets = [frozenset(u) for u in topology]
        nbhd = {}
        for x in carrier:
            all_s = []
            n = len(carrier)
            for i in range(1 << n):
                s = frozenset(carrier[j] for j in range(n) if i & (1 << j))
                if any(x in u and u <= s for u in open_sets):
                    all_s.append(s)
            nbhd[x] = all_s
        return nbhd

    def test_sierpinski_recovery(self):
        nbhd = self._build_nbhd(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY)
        r = topology_from_neighborhood_system(SIERPINSKI_CARRIER, nbhd)
        assert r.is_true
        assert r.metadata["open_set_count"] == 3  # ∅, {1}, {0,1}

    def test_three_point_recovery(self):
        nbhd = self._build_nbhd(THREE_CARRIER, THREE_TOPOLOGY)
        r = topology_from_neighborhood_system(THREE_CARRIER, nbhd)
        assert r.is_true
        assert r.metadata["open_set_count"] == 4

    def test_v051_flag(self):
        nbhd = self._build_nbhd(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY)
        r = topology_from_neighborhood_system(SIERPINSKI_CARRIER, nbhd)
        assert r.metadata["v0_1_51_corridor_record"] is True


# ---------------------------------------------------------------------------
# analyze_neighborhood_system
# ---------------------------------------------------------------------------

class TestAnalyzeNeighborhoodSystem:
    def test_full_profile(self):
        r = analyze_neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY)
        assert r.is_true
        assert r.metadata["carrier_size"] == 2
        assert "max_character" in r.metadata

    def test_profile_values(self):
        r = analyze_neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY)
        # χ(0)=1, χ(1)=2
        assert r.metadata["max_character"] == 2
        assert r.metadata["min_character"] == 1

    def test_with_point(self):
        r = analyze_neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 1)
        assert r.is_true
        assert r.value["point"] == 1
        assert r.value["axioms"]["all_axioms"] is True
        assert r.value["character"] == 2

    def test_with_point_0(self):
        r = analyze_neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY, 0)
        assert r.value["character"] == 1

    def test_three_point_profile(self):
        r = analyze_neighborhood_system(THREE_CARRIER, THREE_TOPOLOGY)
        assert r.is_true
        assert r.metadata["carrier_size"] == 3

    def test_corridor_metadata(self):
        r = analyze_neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY)
        assert r.metadata["cilt_iii_corridor"] == "neighborhood-systems"

    def test_v051_flag(self):
        r = analyze_neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY)
        assert r.metadata["v0_1_51_corridor_record"] is True


# ---------------------------------------------------------------------------
# pytop public API
# ---------------------------------------------------------------------------

class TestPytopPublicApi:
    def test_all_exports(self):
        for name in ["neighborhood_system_axioms", "neighborhood_system",
                     "local_base_check", "character_at_point",
                     "topology_from_neighborhood_system",
                     "analyze_neighborhood_system"]:
            assert hasattr(pytop, name), f"Missing: {name}"

    def test_via_pytop(self):
        r = pytop.analyze_neighborhood_system(SIERPINSKI_CARRIER, SIERPINSKI_TOPOLOGY)
        assert r.is_true and r.metadata["v0_1_51_corridor_record"] is True
