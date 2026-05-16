"""Coverage-targeted tests for construction_contracts.py (v0.5.1)."""
from pytop.construction_contracts import (
    finite_product_contract,
    FiniteConstructionContract,
)


# ---------------------------------------------------------------------------
# finite_product_contract — lines 46-47 (factor not iterable → status=unknown)
# ---------------------------------------------------------------------------

def test_finite_product_contract_non_iterable_factor():
    contract = finite_product_contract(42)
    assert contract.status == "unknown"
    assert contract.kind == "product"
    assert "not an explicit finite finite iterable" in contract.warnings[0] or "not an explicit" in contract.warnings[0]


def test_finite_product_contract_no_factors():
    contract = finite_product_contract()
    assert contract.status == "false"


def test_finite_product_contract_empty_factor():
    contract = finite_product_contract([])
    assert contract.status == "false"


def test_finite_product_contract_valid():
    contract = finite_product_contract([1, 2], [3, 4])
    assert contract.status == "true"
    assert contract.carrier_size == 4
