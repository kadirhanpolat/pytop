"""
Examples for Uniform Spaces.
Added in v0.1.94
"""

def example_metric_uniformity():
    """Every metric space naturally induces a uniform space structure."""
    return {"space_type": "Metric Uniformity", "is_uniform_space": True, "is_uniformly_complete": True}

def example_discrete_uniformity():
    """The discrete uniformity where every subset of X x X containing the diagonal is an entourage."""
    return {"space_type": "Discrete Uniformity", "is_uniform_space": True}
