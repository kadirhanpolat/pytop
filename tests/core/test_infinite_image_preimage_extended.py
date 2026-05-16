"""Extended tests for infinite_image_preimage.py — covers all remaining branches."""

from pytop.examples import reals_cocountable, reals_indiscrete, real_line_metric
from pytop.infinite_image_preimage import (
    SymbolicSubset,
    compact_image_result,
    connected_image_result,
    image_space,
    image_subset,
    preimage_subset,
)
from pytop.infinite_maps import ContinuousMap, QuotientMap, SymbolicMap


# ===========================================================================
# SymbolicSubset.add_tags — lines 27-31
# ===========================================================================

class TestSymbolicSubsetAddTags:
    def test_add_tags_populates_tags_set(self):
        s = SymbolicSubset(ambient='X', label='A')
        s.add_tags('open', 'bounded')
        assert s.has_tag('open')
        assert s.has_tag('bounded')

    def test_add_tags_updates_metadata_tags(self):
        s = SymbolicSubset(ambient='X', label='A')
        s.add_tags('closed')
        assert 'closed' in s.metadata['tags']

    def test_add_tags_ignores_empty_string(self):
        s = SymbolicSubset(ambient='X', label='A')
        s.add_tags('', '  ')
        assert s.tags == set()


# ===========================================================================
# image_space — surjective path (line 55)
# ===========================================================================

class TestImageSpaceSurjective:
    def test_surjective_continuous_map_adds_realized_as_codomain(self):
        X = reals_indiscrete()   # compact domain
        Y = reals_cocountable()
        q = QuotientMap(domain=X, codomain=Y, name='q')
        image = image_space(q)
        assert 'realized_as_codomain' in image.tags

    def test_surjective_map_also_propagates_compact_from_domain(self):
        X = reals_indiscrete()
        Y = reals_cocountable()
        q = QuotientMap(domain=X, codomain=Y, name='q')
        image = image_space(q)
        assert 'compact' in image.tags


# ===========================================================================
# preimage_subset — closed tag path (line 70)
# ===========================================================================

class TestPreimageSubset:
    def test_preimage_of_closed_subset_is_closed_under_continuous_map(self):
        f = ContinuousMap(domain='X', codomain='Y', name='f')
        F = SymbolicSubset(ambient='Y', label='F', tags={'closed'})
        pre = preimage_subset(f, F)
        assert pre.has_tag('closed')

    def test_preimage_of_open_and_closed_subset_has_both_tags(self):
        f = ContinuousMap(domain='X', codomain='Y', name='f')
        A = SymbolicSubset(ambient='Y', label='A', tags={'open', 'closed'})
        pre = preimage_subset(f, A)
        assert pre.has_tag('open')
        assert pre.has_tag('closed')


# ===========================================================================
# image_subset — connected and path_connected paths (lines 84, 86)
# ===========================================================================

class TestImageSubset:
    def test_continuous_image_of_connected_subset_is_connected(self):
        f = ContinuousMap(domain='X', codomain='Y', name='f')
        A = SymbolicSubset(ambient='X', label='A', tags={'connected'})
        img = image_subset(f, A)
        assert img.has_tag('connected')

    def test_continuous_image_of_path_connected_subset_is_path_connected(self):
        f = ContinuousMap(domain='X', codomain='Y', name='f')
        A = SymbolicSubset(ambient='X', label='A', tags={'path_connected'})
        img = image_subset(f, A)
        assert img.has_tag('path_connected')

    def test_continuous_image_propagates_all_preserved_tags(self):
        f = ContinuousMap(domain='X', codomain='Y', name='f')
        A = SymbolicSubset(ambient='X', label='A', tags={'compact', 'connected', 'path_connected'})
        img = image_subset(f, A)
        assert img.has_tag('compact')
        assert img.has_tag('connected')
        assert img.has_tag('path_connected')


# ===========================================================================
# compact_image_result — unknown path (lines 104-105)
# ===========================================================================

class TestCompactImageResult:
    def test_non_continuous_map_returns_unknown(self):
        m = SymbolicMap(domain='X', codomain='Y')
        r = compact_image_result(m)
        assert not r.is_true

    def test_continuous_map_non_compact_domain_returns_unknown(self):
        # real_line_metric() is not compact
        X = real_line_metric()
        Y = reals_cocountable()
        f = ContinuousMap(domain=X, codomain=Y, name='f')
        r = compact_image_result(f)
        assert not r.is_true


# ===========================================================================
# connected_image_result — unknown path (lines 119-120)
# ===========================================================================

class TestConnectedImageResult:
    def test_non_continuous_map_returns_unknown(self):
        m = SymbolicMap(domain='X', codomain='Y')
        r = connected_image_result(m)
        assert not r.is_true

    def test_map_with_no_tags_returns_unknown(self):
        # plain string codomain has no tags — image cannot inherit 'connected'
        m = SymbolicMap(domain='X', codomain='Y')
        r = connected_image_result(m)
        assert not r.is_true
