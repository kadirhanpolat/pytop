"""P16 validation suite: benchmarks, oracle parity, statistical validation.

Phase 16 validation framework:
- P16.1: Benchmark suite (minimal triangulations, knot table, graphs)
- P16.2: Oracle parity framework (cross-system agreement matrices)
- P16.3: Statistical validation (10K random complexes)
"""

from tests.validation.fixtures import (
    BaselineResults,
    GraphExamples,
    GridGraphLibrary,
    KnotTable,
    MinimalTriangulations,
)
from tests.validation.oracle_agreement_builder import (
    AgreementMatrixReport,
    OracleAgreementBuilder,
    OracleComparison,
)
from tests.validation.oracle_integrations import (
    GudhiOracleAdapter,
    OracleAdapter,
    RipserOracleAdapter,
    SageOracleAdapter,
    SnapPyOracleAdapter,
    get_available_oracles,
)
from tests.validation.test_oracle_parity import AgreementMatrix, OracleAgreement

__all__ = [
    # Fixtures (P16.1)
    "MinimalTriangulations",
    "GraphExamples",
    "KnotTable",
    "GridGraphLibrary",
    "BaselineResults",
    # Oracle framework (P16.2)
    "OracleAdapter",
    "GudhiOracleAdapter",
    "RipserOracleAdapter",
    "SnapPyOracleAdapter",
    "SageOracleAdapter",
    "get_available_oracles",
    "OracleComparison",
    "AgreementMatrixReport",
    "OracleAgreementBuilder",
    "OracleAgreement",
    "AgreementMatrix",
]
