from pytop import FiniteMap, FiniteTopologicalSpace, map_taxonomy_profile, render_map_taxonomy_report


def _space(points, opens):
    return FiniteTopologicalSpace(carrier=tuple(points), topology=tuple(frozenset(item) for item in opens))


def test_map_taxonomy_profile_separates_continuity_and_openness_on_identity_maps():
    points = ('a', 'b')
    discrete = _space(points, [set(), {'a'}, {'b'}, {'a', 'b'}])
    indiscrete = _space(points, [set(), {'a', 'b'}])

    cont_map = FiniteMap(domain=discrete, codomain=indiscrete, name='id_d_to_i', mapping={'a': 'a', 'b': 'b'})
    open_map = FiniteMap(domain=indiscrete, codomain=discrete, name='id_i_to_d', mapping={'a': 'a', 'b': 'b'})

    profile_cont = map_taxonomy_profile(cont_map)
    profile_open = map_taxonomy_profile(open_map)

    assert profile_cont == {
        'continuous': True,
        'open': False,
        'closed': False,
        'bijective': True,
        'homeomorphism': False,
    }
    assert profile_open == {
        'continuous': False,
        'open': True,
        'closed': True,
        'bijective': True,
        'homeomorphism': False,
    }

    report = render_map_taxonomy_report(open_map)
    assert 'Map taxonomy report for id_i_to_d' in report
    assert '- open: yes' in report
    assert 'warning-line: openness did not imply continuity' in report
