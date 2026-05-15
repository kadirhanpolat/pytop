from pytop.examples import finite_chain_space, naturals_cofinite
from pytop.subspaces import finite_subspace, subspace
from pytop.compactness import is_compact


def test_finite_subspace_topology_is_computed_exactly():
    X = finite_chain_space()
    A = finite_subspace(X, {1, 2})
    assert A.is_finite()
    assert set(A.carrier) == {1, 2}
    assert is_compact(A).is_true


def test_symbolic_subspace_preserves_stable_tags():
    X = naturals_cofinite()
    A = subspace(X, 'A', closed=True)
    assert 'closed_subspace' in A.tags
    assert 't1' in A.tags
