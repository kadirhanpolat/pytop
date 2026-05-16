"""Coverage-targeted tests for cell_complexes.py (v0.5.1)."""
import pytest
from pytop.cell_complexes import (
    Cell,
    CellComplexError,
    CellComplexProfile,
    cell,
    simplex_as_cell_profile,
)


# ---------------------------------------------------------------------------
# Cell.__post_init__ — line 25 (empty name raises)
# ---------------------------------------------------------------------------

def test_cell_empty_name_raises():
    with pytest.raises(CellComplexError, match="nonempty name"):
        Cell(name="   ", dimension=0)


# ---------------------------------------------------------------------------
# CellComplexProfile.__post_init__ — line 49 (empty profile name raises)
# ---------------------------------------------------------------------------

def test_cell_complex_profile_empty_name_raises():
    c = cell("v0", 0)
    with pytest.raises(CellComplexError, match="nonempty name"):
        CellComplexProfile(name="  ", cells=(c,))


# ---------------------------------------------------------------------------
# CellComplexProfile.__post_init__ — line 52 (no cells raises)
# ---------------------------------------------------------------------------

def test_cell_complex_profile_empty_cells_raises():
    with pytest.raises(CellComplexError, match="at least one cell"):
        CellComplexProfile(name="my_complex", cells=())


# ---------------------------------------------------------------------------
# simplex_as_cell_profile — line 139 (negative dimension raises)
# ---------------------------------------------------------------------------

def test_simplex_as_cell_profile_negative_dimension_raises():
    with pytest.raises(CellComplexError, match="nonneg"):
        simplex_as_cell_profile(-1)
