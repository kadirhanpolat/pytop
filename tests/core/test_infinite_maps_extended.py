"""Extended tests for infinite_maps.py — covers all remaining branches."""

import pytest
from pytop.infinite_maps import (
    MAP_PROPERTIES,
    ConstantMap,
    EmbeddingMap,
    HomeomorphismMap,
    SymbolicMap,
    analyze_infinite_map_property,
    compose_maps,
    identity_map,
    infinite_map_report,
    initial_topology_descriptor,
    is_bijective_map,
    is_closed_map,
    is_embedding_map,
    is_homeomorphism_map,
    is_injective_map,
    is_open_map,
    is_surjective_map,
    normalize_map_property,
)
from pytop.examples import real_line_metric


# ===========================================================================
# EmbeddingMap and ConstantMap constructors
# ===========================================================================

class TestSpecialMapConstructors:
    def test_embedding_map_has_required_tags(self):
        m = EmbeddingMap(domain='X', codomain='Y')
        assert m.has_tag('embedding')
        assert m.has_tag('continuous')
        assert m.has_tag('injective')
        assert m.metadata['representation'] == 'embedding_map'

    def test_constant_map_has_required_tags(self):
        m = ConstantMap(domain='X', codomain='Y')
        assert m.has_tag('constant')
        assert m.has_tag('continuous')
        assert m.metadata['representation'] == 'constant_map'


# ===========================================================================
# normalize_map_property — invalid name raises ValueError
# ===========================================================================

class TestNormalizeMapProperty:
    def test_unknown_property_raises(self):
        with pytest.raises(ValueError, match="Unsupported map property"):
            normalize_map_property('teleportation')

    def test_alias_one_to_one_resolves(self):
        assert normalize_map_property('one_to_one') == 'injective'

    def test_alias_onto_resolves(self):
        assert normalize_map_property('onto') == 'surjective'


# ===========================================================================
# is_* shortcut functions not yet covered
# ===========================================================================

class TestIsStarShortcuts:
    def test_is_closed_map_true(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'closed'})
        assert is_closed_map(m).is_true

    def test_is_injective_map_true(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'injective'})
        assert is_injective_map(m).is_true

    def test_is_surjective_map_true(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'surjective'})
        assert is_surjective_map(m).is_true

    def test_is_bijective_map_true(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'bijective'})
        assert is_bijective_map(m).is_true

    def test_is_embedding_map_true(self):
        m = EmbeddingMap(domain='X', codomain='Y')
        assert is_embedding_map(m).is_true


# ===========================================================================
# infinite_map_report — returns a result for every MAP_PROPERTY
# ===========================================================================

class TestInfiniteMapReport:
    def test_homeomorphism_report_all_true(self):
        m = HomeomorphismMap(domain='X', codomain='Y')
        report = infinite_map_report(m)
        assert set(report.keys()) == MAP_PROPERTIES
        assert all(r.is_true for r in report.values())

    def test_report_keys_match_map_properties(self):
        m = SymbolicMap(domain='X', codomain='Y')
        report = infinite_map_report(m)
        assert set(report.keys()) == MAP_PROPERTIES


# ===========================================================================
# compose_maps — embedding branch (lines 228-229)
# ===========================================================================

class TestIdentityMap:
    def test_identity_map_is_homeomorphism(self):
        space = real_line_metric()
        m = identity_map(space)
        assert isinstance(m, HomeomorphismMap)
        assert m.domain is space
        assert m.codomain is space
        assert is_homeomorphism_map(m).is_true

    def test_identity_map_custom_name(self):
        m = identity_map('X', name='id_X')
        assert m.name == 'id_X'


class TestComposeMaps:
    def test_compose_embeddings_propagates_embedding_tag(self):
        m1 = EmbeddingMap(domain='X', codomain='Y')
        m2 = EmbeddingMap(domain='Y', codomain='Z')
        composite = compose_maps(m1, m2)
        assert 'embedding' in composite.tags

    def test_compose_embeddings_does_not_add_homeomorphism(self):
        m1 = EmbeddingMap(domain='X', codomain='Y')
        m2 = EmbeddingMap(domain='Y', codomain='Z')
        composite = compose_maps(m1, m2)
        assert 'homeomorphism' not in composite.tags


# ===========================================================================
# initial_topology_descriptor — error branches
# ===========================================================================

class TestInitialTopologyDescriptor:
    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="at least one defining map"):
            initial_topology_descriptor([])

    def test_different_domains_raises(self):
        X = real_line_metric()
        Y = real_line_metric()
        f = SymbolicMap(domain=X, codomain=Y)
        g = SymbolicMap(domain=Y, codomain=X)  # different domain object
        with pytest.raises(ValueError, match="same domain"):
            initial_topology_descriptor([f, g])


# ===========================================================================
# _has_positive_tag — metadata True path (line 259)
# ===========================================================================

class TestHasPositiveTagViaMetadata:
    def test_metadata_true_returns_true_result(self):
        m = SymbolicMap(domain='X', codomain='Y', metadata={'continuous': True})
        r = analyze_infinite_map_property(m, 'continuous')
        assert r.is_true
        assert r.metadata['source'] == 'tags'  # _has_positive_tag found it, reported as 'tags'

    def test_metadata_false_returns_false_result(self):
        m = SymbolicMap(domain='X', codomain='Y', metadata={'continuous': False})
        r = analyze_infinite_map_property(m, 'continuous')
        assert r.is_false


# ===========================================================================
# _theorem_map_property — theorem implication paths
# ===========================================================================

class TestTheoremMapProperty:
    def test_homeomorphism_tag_implies_open_via_theorem(self):
        # 'homeomorphism' in tags but 'open' not → theorem path
        m = SymbolicMap(domain='X', codomain='Y', tags={'homeomorphism'})
        r = is_open_map(m)
        assert r.is_true
        assert r.metadata['source'] == 'theorem_homeomorphism'

    def test_homeomorphism_tag_implies_closed_via_theorem(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'homeomorphism'})
        r = is_closed_map(m)
        assert r.is_true
        assert r.metadata['source'] == 'theorem_homeomorphism'

    def test_embedding_tag_implies_injective_via_theorem(self):
        # 'embedding' only → injective derives from theorem
        m = SymbolicMap(domain='X', codomain='Y', tags={'embedding'})
        r = is_injective_map(m)
        assert r.is_true
        assert r.metadata['source'] == 'theorem_embedding'

    def test_embedding_tag_implies_continuous_via_theorem(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'embedding'})
        r = analyze_infinite_map_property(m, 'continuous')
        assert r.is_true
        assert r.metadata['source'] == 'theorem_embedding'

    def test_quotient_tag_implies_surjective_via_theorem(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'quotient'})
        r = is_surjective_map(m)
        assert r.is_true
        assert r.metadata['source'] == 'theorem_quotient'

    def test_quotient_tag_implies_continuous_via_theorem(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'quotient'})
        r = analyze_infinite_map_property(m, 'continuous')
        assert r.is_true
        assert r.metadata['source'] == 'theorem_quotient'

    def test_continuous_bijective_closed_implies_homeomorphism(self):
        m = SymbolicMap(domain='X', codomain='Y', tags={'continuous', 'bijective', 'closed'})
        r = analyze_infinite_map_property(m, 'homeomorphism')
        assert r.is_true
        assert r.metadata['source'] == 'theorem_closed_inverse'

    def test_unknown_returned_when_no_theorem_applies(self):
        m = SymbolicMap(domain='X', codomain='Y')
        r = analyze_infinite_map_property(m, 'open')
        assert not r.is_true
        assert not r.is_false
