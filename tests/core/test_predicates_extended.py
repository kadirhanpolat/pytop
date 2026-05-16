"""Extended tests for predicates.py — branches not covered by existing tests."""

import pytest
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import InfiniteTopologicalSpace
from pytop.predicates import (
    PredicateError,
    UnknownSubsetError,
    analyze_predicate,
    is_clopen_subset,
    is_closed_subset,
    is_dense_subset,
    is_nowhere_dense_subset,
    is_open_subset,
    normalize_predicate_name,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _discrete(a, b):
    return FiniteTopologicalSpace(
        carrier=(a, b),
        topology=[set(), {a}, {b}, {a, b}],
    )


def _symbolic():
    return InfiniteTopologicalSpace(carrier="X", metadata={"representation": "infinite_T2"})


class _SubsetWithTags:
    def __init__(self, *tags):
        self.tags = set(tags)


class _SubsetWithLabel:
    label = "symbolic_A"


# ---------------------------------------------------------------------------
# normalize_predicate_name (line 48)
# ---------------------------------------------------------------------------

class TestNormalizePredicateName:
    def test_invalid_raises_predicate_error(self):
        with pytest.raises(PredicateError, match="Unsupported"):
            normalize_predicate_name("foobar")

    def test_alias_openness(self):
        assert normalize_predicate_name("openness") == "open"

    def test_alias_closedness(self):
        assert normalize_predicate_name("closedness") == "closed"

    def test_alias_nowheredense(self):
        assert normalize_predicate_name("nowheredense") == "nowhere_dense"

    def test_alias_clopenness(self):
        assert normalize_predicate_name("clopenness") == "clopen"


# ---------------------------------------------------------------------------
# UnknownSubsetError for symbolic subset on finite space (lines 61-62)
# ---------------------------------------------------------------------------

class TestSymbolicSubsetOnFiniteSpace:
    def test_label_subset_falls_through_to_symbolic(self):
        X = _discrete(1, 2)
        subset = _SubsetWithLabel()
        r = analyze_predicate(X, "open", subset)
        assert not r.is_true and not r.is_false

    def test_unsupported_subset_type_falls_through(self):
        X = _discrete(1, 2)
        r = analyze_predicate(X, "open", 42)
        assert not r.is_true and not r.is_false


# ---------------------------------------------------------------------------
# Clopen symbolic tag branches (lines 70-85)
# ---------------------------------------------------------------------------

class TestClopenSymbolicTags:
    def test_clopen_tag_returns_true(self):
        s = _symbolic()
        subset = _SubsetWithTags("clopen")
        assert analyze_predicate(s, "clopen", subset).is_true

    def test_open_and_closed_tags_returns_true(self):
        s = _symbolic()
        subset = _SubsetWithTags("open", "closed")
        assert analyze_predicate(s, "clopen", subset).is_true

    def test_not_open_tag_returns_false(self):
        s = _symbolic()
        subset = _SubsetWithTags("not_open")
        assert analyze_predicate(s, "clopen", subset).is_false

    def test_not_closed_tag_returns_false(self):
        s = _symbolic()
        subset = _SubsetWithTags("not_closed")
        assert analyze_predicate(s, "clopen", subset).is_false


# ---------------------------------------------------------------------------
# Negative tag for non-clopen predicates (lines 101-109)
# ---------------------------------------------------------------------------

class TestNegativeTagSymbolic:
    def test_not_open_tag_on_open_predicate(self):
        s = _symbolic()
        subset = _SubsetWithTags("not_open")
        assert analyze_predicate(s, "open", subset).is_false

    def test_not_dense_tag(self):
        s = _symbolic()
        subset = _SubsetWithTags("not_dense")
        assert analyze_predicate(s, "dense", subset).is_false

    def test_positive_open_tag_returns_true(self):
        s = _symbolic()
        subset = _SubsetWithTags("open")
        assert analyze_predicate(s, "open", subset).is_true

    def test_positive_dense_tag_returns_true(self):
        s = _symbolic()
        subset = _SubsetWithTags("dense")
        assert analyze_predicate(s, "dense", subset).is_true


# ---------------------------------------------------------------------------
# _as_finite_subset alternative input types (lines 241-248, 250)
# ---------------------------------------------------------------------------

class TestAsFiniteSubsetVariants:
    def test_frozenset_input(self):
        X = _discrete(1, 2)
        r = analyze_predicate(X, "open", frozenset({1}))
        assert r.is_true

    def test_list_input(self):
        X = _discrete(1, 2)
        r = analyze_predicate(X, "open", [1])
        assert r.is_true

    def test_tuple_input(self):
        X = _discrete(1, 2)
        r = analyze_predicate(X, "open", (1,))
        assert r.is_true

    def test_subset_outside_carrier_falls_through(self):
        X = _discrete(1, 2)
        r = analyze_predicate(X, "open", {99})
        assert not r.is_true and not r.is_false


# ---------------------------------------------------------------------------
# _extract_subset_tags dict branch (line 286)
# ---------------------------------------------------------------------------

class TestExtractSubsetTagsDict:
    def test_dict_with_tags_key(self):
        s = _symbolic()
        subset = {"tags": ["open"]}
        r = analyze_predicate(s, "open", subset)
        assert r.is_true


# ---------------------------------------------------------------------------
# _representation_of fallback (line 295)
# ---------------------------------------------------------------------------

class TestRepresentationOfFallback:
    def test_space_without_metadata_uses_fallback(self):
        class BareSpace:
            carrier = (1, 2)
            topology = [set(), {1}, {2}, {1, 2}]
            def is_finite(self):
                return True
        r = analyze_predicate(BareSpace(), "open", {1})
        assert r.is_true


# ---------------------------------------------------------------------------
# _space_is_finite exception path (lines 232-233)
# ---------------------------------------------------------------------------

class TestSpaceIsFiniteException:
    def test_space_without_is_finite_returns_symbolic(self):
        class NoFiniteMethod:
            pass
        s = NoFiniteMethod()
        r = analyze_predicate(s, "open", _SubsetWithTags("open"))
        assert r.is_true


# ---------------------------------------------------------------------------
# Finite exact predicate results (coverage of exact branches)
# ---------------------------------------------------------------------------

class TestFinitePredicates:
    def setup_method(self):
        self.X = _discrete(1, 2)

    def test_open_true(self):
        assert is_open_subset(self.X, {1}).is_true

    def test_open_false(self):
        X = FiniteTopologicalSpace(carrier=(1, 2), topology=[set(), {1, 2}])
        assert is_open_subset(X, {1}).is_false

    def test_closed_true(self):
        assert is_closed_subset(self.X, {1}).is_true

    def test_closed_false(self):
        X = FiniteTopologicalSpace(carrier=(1, 2, 3), topology=[set(), {1}, {1, 2, 3}])
        assert is_closed_subset(X, {1}).is_false

    def test_clopen_true(self):
        assert is_clopen_subset(self.X, {1}).is_true

    def test_clopen_false(self):
        sier = FiniteTopologicalSpace(carrier=(1, 2), topology=[set(), {1}, {1, 2}])
        assert is_clopen_subset(sier, {1}).is_false

    def test_dense_true(self):
        ind = FiniteTopologicalSpace(carrier=(1, 2), topology=[set(), {1, 2}])
        assert is_dense_subset(ind, {1}).is_true

    def test_dense_false(self):
        assert is_dense_subset(self.X, {1}).is_false

    def test_nowhere_dense_true(self):
        assert is_nowhere_dense_subset(self.X, {1}).is_false

    def test_nowhere_dense_on_sierpinski(self):
        # {2} in Sierpinski: closure={2}, interior(closure)=∅ → nowhere dense
        sier = FiniteTopologicalSpace(carrier=(1, 2), topology=[set(), {1}, {1, 2}])
        assert is_nowhere_dense_subset(sier, {2}).is_true
