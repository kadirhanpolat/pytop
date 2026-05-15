"""Tests for infinite_quotients.py."""

import pytest
from pytop.infinite_quotients import (
    analyze_quotient_map,
    make_quotient_map,
    quotient_space,
    quotient_space_from_map,
)
from pytop.infinite_maps import QuotientMap
from pytop.infinite_spaces import InfiniteTopologicalSpace


def _inf_space(carrier="X", tags=(), representation="infinite_T2"):
    return InfiniteTopologicalSpace(
        carrier=carrier,
        metadata={"representation": representation},
        tags=set(tags),
    )


# ---------------------------------------------------------------------------
# quotient_space
# ---------------------------------------------------------------------------

class TestQuotientSpace:
    def test_carrier_is_domain_slash_relation(self):
        domain = _inf_space("X")
        qs = quotient_space(domain, "equiv")
        assert qs.carrier == "X/equiv"

    def test_has_quotient_space_tag(self):
        qs = quotient_space(_inf_space("Y"), "sim")
        assert "quotient_space" in qs.tags

    def test_infinite_tag_added_for_infinite_representation(self):
        domain = _inf_space("X", representation="infinite_T2")
        qs = quotient_space(domain, "R")
        assert "infinite" in qs.tags
    def test_returns_infinite_topological_space(self):
        qs = quotient_space(_inf_space("Z"), "tilde")
        assert isinstance(qs, InfiniteTopologicalSpace)

    def test_metadata_description_default(self):
        domain = _inf_space("X")
        qs = quotient_space(domain, "equiv")
        desc = qs.metadata.get("description", "")
        assert "equiv" in desc

    def test_metadata_construction_key(self):
        qs = quotient_space(_inf_space("X"), "R")
        assert qs.metadata.get("construction") == "quotient"

    def test_custom_metadata_merged(self):
        qs = quotient_space(_inf_space("X"), "R", metadata={"extra": "value"})
        assert qs.metadata.get("extra") == "value"

    def test_relation_label_in_metadata(self):
        qs = quotient_space(_inf_space("X"), "myrel")
        assert qs.metadata.get("relation_label") == "myrel"


# ---------------------------------------------------------------------------
# make_quotient_map
# ---------------------------------------------------------------------------

class TestMakeQuotientMap:
    def setup_method(self):
        self.domain = _inf_space("X")
        self.codomain = _inf_space("X/~", tags=["quotient_space"])

    def test_returns_quotient_map(self):
        qm = make_quotient_map(self.domain, self.codomain)
        assert isinstance(qm, QuotientMap)

    def test_default_name_is_q(self):
        qm = make_quotient_map(self.domain, self.codomain)
        assert qm.name == "q"

    def test_custom_name(self):
        qm = make_quotient_map(self.domain, self.codomain, name="pi")
        assert qm.name == "pi"

    def test_domain_assigned(self):
        qm = make_quotient_map(self.domain, self.codomain)
        assert qm.domain is self.domain

    def test_codomain_assigned(self):
        qm = make_quotient_map(self.domain, self.codomain)
        assert qm.codomain is self.codomain

    def test_custom_metadata(self):
        qm = make_quotient_map(self.domain, self.codomain, metadata={"fiber": "circle"})
        assert qm.metadata.get("fiber") == "circle"


# ---------------------------------------------------------------------------
# analyze_quotient_map
# ---------------------------------------------------------------------------

class TestAnalyzeQuotientMap:
    def test_quotient_map_gives_true(self):
        domain = _inf_space("X")
        codomain = _inf_space("X/~")
        qm = make_quotient_map(domain, codomain, name="pi")
        r = analyze_quotient_map(qm)
        assert r.is_true

    def test_returns_result_object(self):
        from pytop.result import Result
        domain = _inf_space("X")
        codomain = _inf_space("X/~")
        qm = make_quotient_map(domain, codomain)
        r = analyze_quotient_map(qm)
        assert isinstance(r, Result)


# ---------------------------------------------------------------------------
# quotient_space_from_map
# ---------------------------------------------------------------------------

class TestQuotientSpaceFromMap:
    def setup_method(self):
        self.domain = _inf_space("X", representation="infinite_T2")
        self.codomain = _inf_space("X/~", tags=["quotient_space"])
        self.qmap = make_quotient_map(self.domain, self.codomain, name="pi")

    def test_returns_infinite_topological_space(self):
        qs = quotient_space_from_map(self.qmap)
        assert isinstance(qs, InfiniteTopologicalSpace)

    def test_carrier_from_codomain(self):
        qs = quotient_space_from_map(self.qmap)
        assert qs.carrier == "X/~"

    def test_has_quotient_space_tag(self):
        qs = quotient_space_from_map(self.qmap)
        assert "quotient_space" in qs.tags

    def test_realized_by_quotient_map_tag(self):
        qs = quotient_space_from_map(self.qmap)
        assert "realized_by_quotient_map" in qs.tags

    def test_metadata_map_name(self):
        qs = quotient_space_from_map(self.qmap)
        assert qs.metadata.get("map_name") == "pi"

    def test_metadata_construction_key(self):
        qs = quotient_space_from_map(self.qmap)
        assert qs.metadata.get("construction") == "quotient_from_map"

    def test_custom_metadata_merged(self):
        qs = quotient_space_from_map(self.qmap, metadata={"fiber": "S1"})
        assert qs.metadata.get("fiber") == "S1"
