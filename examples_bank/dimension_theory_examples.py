"""
Examples for Dimension Theory.
Added in v0.1.91
"""

def example_euclidean_space_dimension(n):
    """Euclidean space R^n has ind = Ind = dim = n."""
    return {"space_type": f"R^{n}", "ind": n, "Ind": n, "dim": n}

def example_cantor_set_dimension():
    """The Cantor set is a classic zero-dimensional space."""
    return {"space_type": "Cantor Set", "ind": 0, "Ind": 0, "dim": 0, "is_zero_dimensional": True}
