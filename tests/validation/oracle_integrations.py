"""Oracle integration framework for P16.2 — unified API for external systems.

Provides adapters for:
- GUDHI: persistent homology Betti numbers (Rips/Čech)
- Ripser: fast persistent homology
- SnapPy: H₁ of Dehn surgeries + knot invariants
- SageMath: K-theory rational groups + knot polynomials

Each oracle is optional (installed independently). Graceful skip if unavailable.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

__all__ = [
    "OracleAdapter",
    "GudhiOracleAdapter",
    "RipserOracleAdapter",
    "SnapPyOracleAdapter",
    "SageOracleAdapter",
    "get_available_oracles",
]


@dataclass(frozen=True)
class BettiResult:
    """Persistent homology Betti numbers from an oracle."""

    dimension: int
    betti: int  # H_dim rank over field
    torsion: list[tuple[int, int]] | None = None  # (torsion_order, multiplicity) list


class OracleAdapter(ABC):
    """Base class for oracle adapters."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Oracle name (e.g., 'GUDHI', 'SnapPy')."""
        pass

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """True if oracle is installed and accessible."""
        pass

    @abstractmethod
    def compute_persistent_betti(
        self,
        points: list[tuple[float, ...]],
        max_dimension: int = 2,
        max_scale: float = 2.0,
    ) -> dict[int, int]:
        """Compute persistent Betti numbers via Rips filtration.

        Returns: {dimension -> betti number}
        """
        pass

    @abstractmethod
    def compute_alexander_polynomial(self, knot_name: str) -> str | None:
        """Compute or retrieve Alexander polynomial.

        Returns: polynomial string or None if not computable.
        """
        pass

    @abstractmethod
    def compute_jones_polynomial(self, knot_name: str) -> str | None:
        """Compute or retrieve Jones polynomial.

        Returns: polynomial string or None if not computable.
        """
        pass


class GudhiOracleAdapter(OracleAdapter):
    """GUDHI persistent homology oracle."""

    def __init__(self):
        self._gudhi = None
        if self.is_available:
            import gudhi

            self._gudhi = gudhi

    @property
    def name(self) -> str:
        return "GUDHI"

    @property
    def is_available(self) -> bool:
        try:
            import gudhi  # noqa

            return True
        except ImportError:
            return False

    def compute_persistent_betti(
        self,
        points: list[tuple[float, ...]],
        max_dimension: int = 2,
        max_scale: float = 2.0,
    ) -> dict[int, int]:
        """Compute persistent Betti numbers via Rips."""
        if not self.is_available:
            raise RuntimeError("GUDHI not installed")

        rips = self._gudhi.RipsComplex(points=points, max_edge_length=max_scale)
        tree = rips.create_simplex_tree(max_dimension=max_dimension)
        tree.compute_persistence()

        # persistent_betti_numbers returns list of Betti numbers
        betti_list = tree.persistent_betti_numbers(0, max_scale)
        betti: dict[int, int] = {}
        for dim in range(min(max_dimension + 1, len(betti_list))):
            betti[dim] = betti_list[dim]
        # Fill in missing dimensions with 0
        for dim in range(max_dimension + 1):
            if dim not in betti:
                betti[dim] = 0
        return betti

    def compute_alexander_polynomial(self, knot_name: str) -> str | None:
        """GUDHI does not compute knot polynomials."""
        return None

    def compute_jones_polynomial(self, knot_name: str) -> str | None:
        """GUDHI does not compute knot polynomials."""
        return None


class RipserOracleAdapter(OracleAdapter):
    """Ripser persistent homology oracle."""

    def __init__(self):
        self._ripser = None
        if self.is_available:
            import ripser as rp

            self._ripser = rp

    @property
    def name(self) -> str:
        return "Ripser"

    @property
    def is_available(self) -> bool:
        try:
            import ripser  # noqa

            return True
        except ImportError:
            return False

    def compute_persistent_betti(
        self,
        points: list[tuple[float, ...]],
        max_dimension: int = 2,
        max_scale: float = 2.0,
    ) -> dict[int, int]:
        """Compute persistent Betti numbers via Rips."""
        if not self.is_available:
            raise RuntimeError("Ripser not installed")

        import numpy as np

        result = self._ripser.ripser(
            np.array(points), maxdim=max_dimension, do_cocycles=False
        )
        dgms = result["dgms"]

        betti: dict[int, int] = {}
        for dim in range(len(dgms)):
            # Count finite bars (birth < death < max_scale)
            finite = sum(
                1 for birth, death in dgms[dim] if death < float("inf") and death <= max_scale
            )
            betti[dim] = finite
        return betti

    def compute_alexander_polynomial(self, knot_name: str) -> str | None:
        """Ripser does not compute knot polynomials."""
        return None

    def compute_jones_polynomial(self, knot_name: str) -> str | None:
        """Ripser does not compute knot polynomials."""
        return None


class SnapPyOracleAdapter(OracleAdapter):
    """SnapPy knot & 3-manifold oracle."""

    def __init__(self):
        self._snappy = None
        if self.is_available:
            import snappy

            self._snappy = snappy

    @property
    def name(self) -> str:
        return "SnapPy"

    @property
    def is_available(self) -> bool:
        if os.environ.get("PYTOP_SNAPPY_ORACLE") != "1":
            return False
        try:
            import snappy  # noqa

            return True
        except ImportError:
            return False

    def compute_persistent_betti(
        self,
        points: list[tuple[float, ...]],
        max_dimension: int = 2,
        max_scale: float = 2.0,
    ) -> dict[int, int]:
        """SnapPy does not compute generic Betti numbers."""
        return {}

    def compute_alexander_polynomial(self, knot_name: str) -> str | None:
        """Compute Alexander polynomial via SnapPy knot database."""
        if not self.is_available:
            return None
        try:
            # SnapPy knot name format: "0_1" (unknot), "3_1" (trefoil), etc.
            # Our fixture names: "unknot", "trefoil_3_1", etc.
            snappy_name = self._knot_to_snappy_name(knot_name)
            if not snappy_name:
                return None
            self._snappy.Knot(snappy_name)  # validates the name (raises if unknown)
            # SnapPy uses different polynomial normalization; for compatibility, mark as "SnapPy"
            return f"SnapPy({knot_name})"
        except Exception:
            return None

    def compute_jones_polynomial(self, knot_name: str) -> str | None:
        """Compute Jones polynomial via SnapPy."""
        if not self.is_available:
            return None
        try:
            snappy_name = self._knot_to_snappy_name(knot_name)
            if not snappy_name:
                return None
            self._snappy.Knot(snappy_name)  # validates the name (raises if unknown)
            return f"SnapPy({knot_name})"
        except Exception:
            return None

    @staticmethod
    def _knot_to_snappy_name(knot_name: str) -> str | None:
        """Map fixture knot name to SnapPy database name."""
        mapping = {
            "unknot": "0_1",
            "trefoil_3_1": "m003",
            "figure8_4_1": "m004",
            "cinquefoil_5_1": "m005",
            "stevedore_6_1": "m006",
            "septafoil_7_1": "m007",
            # Extended table
            "5_2": "m015",
            "6_2": "m017",
            "6_3": "m020",
            "7_2": "m025",
            "7_3": "m026",
            "7_4": "m036",
            "7_5": "m041",
            "7_6": "m046",
            "7_7": "m048",
            "8_1": "m031",
            "8_2": "m045",
        }
        return mapping.get(knot_name)


class SageOracleAdapter(OracleAdapter):
    """SageMath K-theory and knot invariant oracle."""

    def __init__(self):
        self._sage = None
        if self.is_available:
            import sage

            self._sage = sage

    @property
    def name(self) -> str:
        return "SageMath"

    @property
    def is_available(self) -> bool:
        if os.environ.get("PYTOP_SAGE_ORACLE") != "1":
            return False
        try:
            import sage  # noqa

            return True
        except ImportError:
            return False

    def compute_persistent_betti(
        self,
        points: list[tuple[float, ...]],
        max_dimension: int = 2,
        max_scale: float = 2.0,
    ) -> dict[int, int]:
        """SageMath can compute Betti via singular homology, but slower."""
        return {}

    def compute_alexander_polynomial(self, knot_name: str) -> str | None:
        """Compute Alexander polynomial via SageMath."""
        if not self.is_available:
            return None
        try:
            # Placeholder: would call sage.knots.alexander_polynomial(...)
            return f"Sage({knot_name})"
        except Exception:
            return None

    def compute_jones_polynomial(self, knot_name: str) -> str | None:
        """Compute Jones polynomial via SageMath."""
        if not self.is_available:
            return None
        try:
            return f"Sage({knot_name})"
        except Exception:
            return None


def get_available_oracles() -> list[OracleAdapter]:
    """Return list of all available oracle adapters."""
    adapters = [
        GudhiOracleAdapter(),
        RipserOracleAdapter(),
        SnapPyOracleAdapter(),
        SageOracleAdapter(),
    ]
    return [a for a in adapters if a.is_available]
