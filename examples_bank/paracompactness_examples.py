"""
Examples for Paracompactness.
Added in v0.1.88
"""

def example_metric_space_paracompact():
    """Every metric space is paracompact (Stone's Theorem)."""
    return {"space_type": "Metric", "is_paracompact": True}

def example_sorgenfrey_line_paracompact():
    """The Sorgenfrey line is paracompact."""
    return {"space_type": "Sorgenfrey Line", "is_paracompact": True}
