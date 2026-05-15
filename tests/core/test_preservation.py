"""Tests for preservation.py."""

import pytest
from pytop.maps import FiniteMap
from pytop.preservation import (
    analyze_preservation,
    compact_closed_subspace,
    compact_under_continuous_image,
    connected_under_continuous_image,
    homeomorphic_invariant_transfer,
    separation_inherited_by_subspace,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _map_with_domain(domain_tags=(), map_tags=()):
    domain = TopologicalSpace(carrier=None, tags=set(domain_tags))
    codomain = TopologicalSpace(carrier=None, tags=set())
    return FiniteMap(domain=domain, codomain=codomain, name="f", tags=set(map_tags))


def _map_only(map_tags=()):
    domain = TopologicalSpace(carrier=None, tags=set())
    codomain = TopologicalSpace(carrier=None, tags=set())
    return FiniteMap(domain=domain, codomain=codomain, name="f", tags=set(map_tags))


class _Sub:
    def __init__(self, *tags):
        self.tags = set(tags)
        self.metadata = {}


class TestCompactUnderContinuousImage:
    def test_continuous_compact_domain_is_true(self):
        m = _map_with_domain(["compact"], ["continuous"])
        assert compact_under_continuous_image(m).is_true

    def test_not_continuous_gives_false(self):
        m = _map_with_domain(["compact"], ["not_continuous"])
        assert compact_under_continuous_image(m).is_false

    def test_unknown_continuity_gives_unknown(self):
        m = _map_with_domain(["compact"], [])
        assert compact_under_continuous_image(m).is_unknown

    def test_continuous_non_compact_domain_gives_unknown(self):
        m = _map_with_domain([], ["continuous"])
        assert compact_under_continuous_image(m).is_unknown

    def test_returns_result(self):
        assert isinstance(compact_under_continuous_image(_map_only()), Result)

    def test_metadata_preservation_key(self):
        m = _map_with_domain(["compact"], ["continuous"])
        assert "preservation" in compact_under_continuous_image(m).metadata


class TestConnectedUnderContinuousImage:
    def test_continuous_connected_domain_is_true(self):
        m = _map_with_domain(["connected"], ["continuous"])
        assert connected_under_continuous_image(m).is_true

    def test_not_continuous_gives_false(self):
        m = _map_with_domain(["connected"], ["not_continuous"])
        assert connected_under_continuous_image(m).is_false

    def test_unknown_continuity_gives_unknown(self):
        m = _map_with_domain(["connected"], [])
        assert connected_under_continuous_image(m).is_unknown

    def test_continuous_non_connected_gives_unknown(self):
        m = _map_with_domain([], ["continuous"])
        assert connected_under_continuous_image(m).is_unknown

    def test_metadata_preservation_key(self):
        m = _map_with_domain(["connected"], ["continuous"])
        assert "preservation" in connected_under_continuous_image(m).metadata


class TestCompactClosedSubspace:
    def test_closed_subspace_ambient_compact_is_true(self):
        assert compact_closed_subspace(_Sub("closed_subspace", "ambient_compact")).is_true

    def test_closed_plus_compact_is_mixed(self):
        r = compact_closed_subspace(_Sub("closed_subspace", "compact"))
        assert r.status == "true" and r.mode == "mixed"

    def test_no_tags_gives_unknown(self):
        assert compact_closed_subspace(_Sub()).is_unknown

    def test_metadata_preservation_key(self):
        r = compact_closed_subspace(_Sub("closed_subspace", "ambient_compact"))
        assert "preservation" in r.metadata


class TestSeparationInheritedBySubspace:
    def test_subspace_ambient_hausdorff_is_true(self):
        r = separation_inherited_by_subspace(_Sub("subspace", "ambient_hausdorff"), "hausdorff")
        assert r.is_true

    def test_already_has_hausdorff_tag(self):
        r = separation_inherited_by_subspace(_Sub("hausdorff"), "hausdorff")
        assert r.is_true and r.mode == "mixed"

    def test_not_hausdorff_tag_gives_false(self):
        r = separation_inherited_by_subspace(_Sub("not_hausdorff"), "hausdorff")
        assert r.is_false

    def test_no_info_gives_unknown(self):
        assert separation_inherited_by_subspace(_Sub(), "hausdorff").is_unknown

    def test_alias_t2(self):
        r = separation_inherited_by_subspace(_Sub("subspace", "ambient_hausdorff"), "t2")
        assert r.is_true

    def test_t1_inheritance(self):
        r = separation_inherited_by_subspace(_Sub("subspace", "ambient_t1"), "t1")
        assert r.is_true

    def test_closed_subspace_tag_recognized(self):
        r = separation_inherited_by_subspace(_Sub("closed_subspace", "ambient_hausdorff"), "hausdorff")
        assert r.is_true

    def test_unknown_feature_raises(self):
        with pytest.raises(ValueError):
            separation_inherited_by_subspace(_Sub(), "not_real")


class TestHomeomorphicInvariantTransfer:
    def test_homeomorphism_compact_is_true(self):
        m = _map_only(["homeomorphism"])
        assert homeomorphic_invariant_transfer(m, "compact").is_true

    def test_homeomorphism_connected_is_true(self):
        m = _map_only(["homeomorphism"])
        assert homeomorphic_invariant_transfer(m, "connected").is_true

    def test_not_homeomorphism_gives_false(self):
        m = _map_only(["not_homeomorphism"])
        assert homeomorphic_invariant_transfer(m, "compact").is_false

    def test_unknown_map_gives_unknown(self):
        assert homeomorphic_invariant_transfer(_map_only(), "compact").is_unknown

    def test_unsupported_feature_gives_unknown(self):
        m = _map_only(["homeomorphism"])
        assert homeomorphic_invariant_transfer(m, "paracompact").is_unknown

    def test_hausdorff_supported(self):
        m = _map_only(["homeomorphism"])
        assert homeomorphic_invariant_transfer(m, "hausdorff").is_true

    def test_t0_supported(self):
        m = _map_only(["homeomorphism"])
        assert homeomorphic_invariant_transfer(m, "t0").is_true


class TestAnalyzePreservation:
    def test_compact_continuous_image_context(self):
        m = _map_with_domain(["compact"], ["continuous"])
        assert analyze_preservation("compact_under_continuous_image", m).is_true

    def test_alias_continuous_image_compact(self):
        m = _map_with_domain(["compact"], ["continuous"])
        assert analyze_preservation("continuous_image_compact", m).is_true

    def test_connected_continuous_image_context(self):
        m = _map_with_domain(["connected"], ["continuous"])
        assert analyze_preservation("connected_under_continuous_image", m).is_true

    def test_compact_closed_subspace_context(self):
        s = _Sub("closed_subspace", "ambient_compact")
        assert analyze_preservation("compact_closed_subspace", s).is_true

    def test_subspace_separation_context(self):
        s = _Sub("subspace", "ambient_hausdorff")
        r = analyze_preservation("subspace_separation", s, feature="hausdorff")
        assert r.is_true

    def test_homeomorphic_invariant_context(self):
        m = _map_only(["homeomorphism"])
        assert analyze_preservation("homeomorphic_invariant", m, feature="compact").is_true

    def test_unknown_context_raises(self):
        with pytest.raises(ValueError):
            analyze_preservation("nonexistent_context", {})
