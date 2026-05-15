from pytop import (
    analyze_filter,
    filter_cluster_points,
    filter_clusters_at,
    filter_converges_to,
    finite_chain_space,
    generated_filter,
    is_filter,
    is_filter_base,
    is_finer_filter,
    neighborhood_filter_base,
    sierpinski_space,
)


def test_filter_base_and_generated_filter_are_exact():
    carrier = {1, 2, 3}
    base = [{1}]

    base_result = is_filter_base(carrier, base)
    generated = generated_filter(carrier, base)

    assert base_result.is_true and base_result.is_exact
    assert generated.is_true and generated.is_exact
    assert frozenset({1}) in generated.value
    assert frozenset({1, 2, 3}) in generated.value


def test_is_filter_detects_full_upward_closed_family():
    carrier = {1, 2}
    family = [{1}, {1, 2}]
    result = is_filter(carrier, family)

    assert result.is_true and result.is_exact


def test_neighborhood_filter_base_and_convergence_match_finite_local_check():
    space = finite_chain_space(3)
    base = neighborhood_filter_base(space, 1)
    generated = generated_filter(space.carrier, base.value)
    convergence = filter_converges_to(space, generated.value, 1)

    assert base.is_true and base.is_exact
    assert frozenset({1}) in base.value
    assert convergence.is_true and convergence.is_exact



def test_filter_axiom_checker_rejects_empty_intersection_closure_gap():
    carrier = {1, 2}
    family = [{1}, {2}, {1, 2}]
    result = is_filter(carrier, family)
    assert result.is_false and result.is_exact
    assert result.metadata["failed_f2_pairs"] > 0


def test_filter_refinement_compares_reverse_family_inclusion():
    carrier = {0, 1}
    principal_zero = generated_filter(carrier, [{0}]).value
    trivial = generated_filter(carrier, [{0, 1}]).value
    result = is_finer_filter(carrier, principal_zero, trivial)
    assert result.is_true and result.is_exact


def test_filter_cluster_points_detect_adherence_without_convergence():
    space = sierpinski_space()
    principal_zero = generated_filter(space.carrier, [{0}]).value
    clusters = filter_cluster_points(space, principal_zero)
    clusters_at_one = filter_clusters_at(space, principal_zero, 1)
    convergence_to_one = filter_converges_to(space, principal_zero, 1)
    assert clusters.is_true and clusters.is_exact
    assert 0 in clusters.value
    assert 1 not in clusters.value
    assert clusters_at_one.is_false
    assert convergence_to_one.is_false


def test_analyze_filter_collects_convergence_cluster_and_refinement_data():
    space = finite_chain_space(3)
    base = neighborhood_filter_base(space, 1).value
    generated = generated_filter(space.carrier, base).value
    analysis = analyze_filter(space, generated, point=1, coarser=generated)
    assert analysis.is_true and analysis.is_exact
    assert analysis.value["converges_to_point"].is_true
    assert analysis.value["clusters_at_point"].is_true
    assert analysis.value["is_finer_than_coarser"].is_true
    assert 1 in analysis.value["cluster_points"].value
