"""Coverage-targeted tests for infinite_spaces.py (v0.5.1)."""
from pytop.infinite_spaces import CofiniteSpace, CocountableSpace


# ---------------------------------------------------------------------------
# _has_standard_countable_subset — line 28 (standard token → return True)
# ---------------------------------------------------------------------------

def test_cofinite_space_standard_uncountable_carrier_has_countable_subset():
    # carrier="R" is in STANDARD_UNCOUNTABLE_CARRIERS → line 28 fires → separable tag added
    space = CofiniteSpace(carrier="R")
    assert space.has_tag("separable")


# ---------------------------------------------------------------------------
# CocountableSpace.__post_init__ — line 164 (countable carrier adds discrete tag)
# ---------------------------------------------------------------------------

def test_cocountable_space_countable_carrier_gets_discrete_tag():
    # carrier="N" → countable tag → line 164 fires → discrete tag added
    space = CocountableSpace(carrier="N")
    assert space.has_tag("discrete")


# ---------------------------------------------------------------------------
# _has_standard_countable_subset — line 28 (non-standard token → metadata fallback)
# ---------------------------------------------------------------------------

def test_cofinite_space_nonstandard_carrier_metadata_countable_subset():
    # "custom_carrier" is not in any standard set → line 28 fires
    # metadata has_countable_subset=True → returns True → separable tag added
    space = CofiniteSpace(carrier="custom_carrier", metadata={"has_countable_subset": True})
    assert space.has_tag("separable")


def test_cofinite_space_nonstandard_carrier_no_metadata():
    # "custom_carrier" not in standard sets, no metadata → line 28 → returns False
    space = CofiniteSpace(carrier="custom_carrier")
    assert not space.has_tag("separable")
