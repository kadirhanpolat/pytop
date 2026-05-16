"""Tests for symbolic_convergence.py (v0.5.0)."""
import pytest
from pytop.symbolic_convergence import (
    SymbolicNetDescriptor,
    SymbolicFilterDescriptor,
    net_converges_symbolically,
    filter_converges_symbolically,
    ultrafilter_theorem_descriptor,
    convergence_equivalence_profile,
    analyze_symbolic_convergence,
)


# ---------------------------------------------------------------------------
# SymbolicNetDescriptor
# ---------------------------------------------------------------------------

class TestSymbolicNetDescriptor:
    def test_default_index_type(self):
        nd = SymbolicNetDescriptor(space={"tags": ["compact"]})
        assert nd.index_type == "chain"

    def test_invalid_index_type_falls_back(self):
        nd = SymbolicNetDescriptor(space={}, index_type="bogus")
        assert nd.index_type == "directed"

    def test_value_tags_normalized(self):
        nd = SymbolicNetDescriptor(space={}, value_tags={"  Compact ", "HAUSDORFF"})
        assert "compact" in nd.value_tags
        assert "hausdorff" in nd.value_tags

    def test_space_tags_dict(self):
        nd = SymbolicNetDescriptor(space={"tags": ["compact", "hausdorff"]})
        assert "compact" in nd.space_tags
        assert "hausdorff" in nd.space_tags

    def test_space_tags_empty(self):
        nd = SymbolicNetDescriptor(space={})
        assert nd.space_tags == set()

    def test_convergence_result_delegates(self):
        nd = SymbolicNetDescriptor(
            space={"tags": ["compact", "hausdorff"]},
            value_tags={"convergent"},
        )
        r = nd.convergence_result()
        assert r.is_true


# ---------------------------------------------------------------------------
# SymbolicFilterDescriptor
# ---------------------------------------------------------------------------

class TestSymbolicFilterDescriptor:
    def test_default_filter_type(self):
        fd = SymbolicFilterDescriptor(space={})
        assert fd.filter_type == "general"

    def test_invalid_filter_type_falls_back(self):
        fd = SymbolicFilterDescriptor(space={}, filter_type="fancy")
        assert fd.filter_type == "general"

    def test_base_tags_normalized(self):
        fd = SymbolicFilterDescriptor(space={}, base_tags={"Convergent"})
        assert "convergent" in fd.base_tags

    def test_space_tags_from_object(self):
        class Sp:
            tags = {"compact", "hausdorff"}
        fd = SymbolicFilterDescriptor(space=Sp())
        assert "compact" in fd.space_tags

    def test_convergence_result_delegates(self):
        fd = SymbolicFilterDescriptor(
            space={"tags": ["compact"]},
            filter_type="neighborhood",
        )
        r = fd.convergence_result()
        assert r.is_true


# ---------------------------------------------------------------------------
# net_converges_symbolically
# ---------------------------------------------------------------------------

class TestNetConvergesSymbolically:
    def test_convergent_tag(self):
        nd = SymbolicNetDescriptor(space={}, value_tags={"convergent"})
        r = net_converges_symbolically(nd)
        assert r.is_true
        assert r.value == "net_converges"

    def test_eventually_in_every_open_tag(self):
        nd = SymbolicNetDescriptor(
            space={}, value_tags={"eventually_in_every_open"}
        )
        r = net_converges_symbolically(nd)
        assert r.is_true

    def test_not_convergent_tag(self):
        nd = SymbolicNetDescriptor(space={}, value_tags={"not_convergent"})
        r = net_converges_symbolically(nd)
        assert r.is_false
        assert r.value == "net_not_convergent"

    def test_indiscrete_space(self):
        nd = SymbolicNetDescriptor(space={"tags": ["indiscrete"]})
        r = net_converges_symbolically(nd)
        assert r.is_true
        assert "indiscrete" in r.justification[0].lower()

    def test_compact_hausdorff(self):
        nd = SymbolicNetDescriptor(
            space={"tags": ["compact", "hausdorff"]},
            index_type="directed",
        )
        r = net_converges_symbolically(nd)
        assert r.is_true
        assert "cluster" in r.value

    def test_compact_non_hausdorff(self):
        nd = SymbolicNetDescriptor(space={"tags": ["compact"]})
        r = net_converges_symbolically(nd)
        assert r.is_true
        assert "cluster" in r.value

    def test_sequentially_compact_chain(self):
        nd = SymbolicNetDescriptor(
            space={"tags": ["sequentially_compact"]}, index_type="chain"
        )
        r = net_converges_symbolically(nd)
        assert r.is_true
        assert "subsequence" in r.justification[0].lower()

    def test_first_countable_chain_unknown(self):
        nd = SymbolicNetDescriptor(
            space={"tags": ["first_countable"]}, index_type="chain"
        )
        r = net_converges_symbolically(nd)
        assert r.is_unknown

    def test_no_tags_unknown(self):
        nd = SymbolicNetDescriptor(space={})
        r = net_converges_symbolically(nd)
        assert r.is_unknown

    def test_metadata_contains_index_type(self):
        nd = SymbolicNetDescriptor(space={}, index_type="uncountable")
        r = net_converges_symbolically(nd)
        assert r.metadata["index_type"] == "uncountable"


# ---------------------------------------------------------------------------
# filter_converges_symbolically
# ---------------------------------------------------------------------------

class TestFilterConvergesSymbolically:
    def test_neighborhood_filter_always_converges(self):
        fd = SymbolicFilterDescriptor(space={}, filter_type="neighborhood")
        r = filter_converges_symbolically(fd)
        assert r.is_true
        assert "neighborhood filter" in r.justification[0].lower()

    def test_convergent_base_tag(self):
        fd = SymbolicFilterDescriptor(space={}, base_tags={"convergent"})
        r = filter_converges_symbolically(fd)
        assert r.is_true

    def test_not_convergent_base_tag(self):
        fd = SymbolicFilterDescriptor(space={}, base_tags={"not_convergent"})
        r = filter_converges_symbolically(fd)
        assert r.is_false

    def test_indiscrete_space(self):
        fd = SymbolicFilterDescriptor(space={"tags": ["indiscrete"]})
        r = filter_converges_symbolically(fd)
        assert r.is_true

    def test_ultrafilter_compact_converges(self):
        fd = SymbolicFilterDescriptor(
            space={"tags": ["compact"]}, filter_type="ultrafilter"
        )
        r = filter_converges_symbolically(fd)
        assert r.is_true
        assert "ultrafilter" in r.justification[0].lower()

    def test_ultrafilter_noncompact_unknown(self):
        fd = SymbolicFilterDescriptor(space={}, filter_type="ultrafilter")
        r = filter_converges_symbolically(fd)
        assert r.is_unknown

    def test_cofinite_compact_t1_converges(self):
        fd = SymbolicFilterDescriptor(
            space={"tags": ["compact", "t1"]}, filter_type="cofinite"
        )
        r = filter_converges_symbolically(fd)
        assert r.is_true

    def test_compact_general_cluster_point(self):
        fd = SymbolicFilterDescriptor(
            space={"tags": ["compact"]}, filter_type="general"
        )
        r = filter_converges_symbolically(fd)
        assert r.is_true
        assert "cluster" in r.value

    def test_no_info_unknown(self):
        fd = SymbolicFilterDescriptor(space={})
        r = filter_converges_symbolically(fd)
        assert r.is_unknown

    def test_metadata_contains_filter_type(self):
        fd = SymbolicFilterDescriptor(space={}, filter_type="principal")
        r = filter_converges_symbolically(fd)
        assert r.metadata["filter_type"] == "principal"


# ---------------------------------------------------------------------------
# ultrafilter_theorem_descriptor
# ---------------------------------------------------------------------------

class TestUltrafilterTheoremDescriptor:
    def test_returns_dict(self):
        d = ultrafilter_theorem_descriptor()
        assert isinstance(d, dict)

    def test_required_keys(self):
        d = ultrafilter_theorem_descriptor()
        for key in ("theorem", "statement", "compactness_equivalence",
                    "tychonoff_connection", "stone_cech_connection",
                    "net_filter_equivalence", "version"):
            assert key in d

    def test_theorem_name_present(self):
        d = ultrafilter_theorem_descriptor()
        assert "ultrafilter" in d["theorem"].lower()

    def test_compactness_equivalence_mentions_compact(self):
        d = ultrafilter_theorem_descriptor()
        assert "compact" in d["compactness_equivalence"].lower()


# ---------------------------------------------------------------------------
# convergence_equivalence_profile
# ---------------------------------------------------------------------------

class TestConvergenceEquivalenceProfile:
    def test_returns_dict(self):
        p = convergence_equivalence_profile({"tags": ["metrizable"]})
        assert isinstance(p, dict)

    def test_required_keys(self):
        p = convergence_equivalence_profile({})
        for key in ("equivalences", "sequential_sufficiency",
                    "nets_advantage", "filters_advantage", "metadata"):
            assert key in p

    def test_metrizable_sequential_sufficiency(self):
        p = convergence_equivalence_profile({"tags": ["metrizable"]})
        assert p["metadata"]["sequential_sufficiency"] is True

    def test_first_countable_sequential_sufficiency(self):
        p = convergence_equivalence_profile({"tags": ["first_countable"]})
        assert p["metadata"]["sequential_sufficiency"] is True

    def test_no_tags_sequential_not_sufficient(self):
        p = convergence_equivalence_profile({})
        assert p["metadata"]["sequential_sufficiency"] is False

    def test_compact_ultrafilter_note(self):
        p = convergence_equivalence_profile({"tags": ["compact"]})
        assert p["ultrafilter_note"] is not None
        assert "ultrafilter" in p["ultrafilter_note"].lower()

    def test_non_compact_no_ultrafilter_note(self):
        p = convergence_equivalence_profile({})
        assert p["ultrafilter_note"] is None

    def test_compact_hausdorff_limit_in_note(self):
        p = convergence_equivalence_profile({"tags": ["compact", "hausdorff"]})
        assert p["ultrafilter_note"] is not None
        note = p["ultrafilter_note"].lower()
        assert "hausdorff" in note or "one" in note or "exactly" in note


# ---------------------------------------------------------------------------
# analyze_symbolic_convergence
# ---------------------------------------------------------------------------

class TestAnalyzeSymbolicConvergence:
    def test_returns_dict_with_keys(self):
        result = analyze_symbolic_convergence({"tags": ["compact"]})
        for key in ("space_tags", "net_result", "filter_result",
                    "equivalence_profile", "ultrafilter_descriptor", "version"):
            assert key in result

    def test_no_net_or_filter_gives_none(self):
        result = analyze_symbolic_convergence({})
        assert result["net_result"] is None
        assert result["filter_result"] is None

    def test_with_net(self):
        nd = SymbolicNetDescriptor(space={}, value_tags={"convergent"})
        result = analyze_symbolic_convergence({}, net=nd)
        assert result["net_result"] is not None
        assert result["net_result"].is_true

    def test_with_filter(self):
        fd = SymbolicFilterDescriptor(space={}, filter_type="neighborhood")
        result = analyze_symbolic_convergence({}, filt=fd)
        assert result["filter_result"] is not None
        assert result["filter_result"].is_true

    def test_space_tags_sorted(self):
        result = analyze_symbolic_convergence({"tags": ["compact", "hausdorff"]})
        assert result["space_tags"] == sorted(result["space_tags"])
